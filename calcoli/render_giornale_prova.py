#!/usr/bin/env python3
"""Render locale del pacchetto cronache con il generatore PDF di riferimento.

Esegue costruisci/FIT_JS, non la CLI originale né alcun workflow. La rete
del browser è bloccata: il giornale usa il contenuto locale del pacchetto.
"""
import importlib.util
import json
import os
import sys
from pathlib import Path


def main():
    cartella = Path(sys.argv[1]).resolve()
    scripts = cartella/'scripts'
    sys.path.insert(0, str(scripts))
    spec = importlib.util.spec_from_file_location('giornale_riferimento', scripts/'pdf_giornale.py')
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    # Il generatore originale considera giocato anche un turno parziale.
    # Nel solo render di prova adottiamo la stessa chiusura degli altri canali,
    # senza modificare né il suo sorgente né i risultati nel JSON.
    from zone_classifica import _giornate
    import pdf_settimana
    chiuse = _giornate(g.D)
    validi = {id(x) for x in chiuse}
    lega = {id(x) for x in g.D['cal']['lega']}
    sa = chiuse[-1].get('sa') if chiuse else None
    def confermata(turno):
        if id(turno) in lega:
            return id(turno) in validi
        return bool(sa and turno.get('sa') and turno['sa'] <= sa and turno.get('m')
                    and all(m[-1] != '-' for m in turno['m']))
    g.giocata = pdf_settimana.giocata = confermata
    testi = json.loads((cartella/'testi-giornale.json').read_text())
    h, n = g.costruisci(testi)
    radio = json.loads((cartella/'radio-dati.json').read_text())
    if n != radio['aw'][-1]['n']:
        raise RuntimeError('Giornale e Radio non allineati alla stessa giornata')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        exe = Path(os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'))
        b = pw.chromium.launch(headless=True, args=['--no-sandbox'],
            **({'executable_path': str(exe)} if exe.exists() else {}))
        c = b.new_context(service_workers='block')
        c.route('**/*', lambda route: route.abort())
        p = c.new_page()
        p.set_content(h)
        p.emulate_media(media='print')
        fit = p.evaluate(g.FIT_JS)
        if len(fit) != 4 or not all(x['ci_sta'] for x in fit):
            raise RuntimeError('PDF fuori margine: '+json.dumps(fit))
        p.pdf(path=str(cartella/'giornale.pdf'), format='A4', prefer_css_page_size=True, print_background=True)
        (cartella/'giornale.html').write_text(p.content(), encoding='utf-8')
        p.locator('.pg').nth(1).screenshot(path=str(cartella/'giornale-pagina2.png'))
        b.close()
    (cartella/'pdf-esito.json').write_text(json.dumps({'giornata':n,'impaginazione':fit},indent=2)+'\n')
    print('PASS PDF locale: quattro pagine nei margini')


if __name__ == '__main__':
    main()
