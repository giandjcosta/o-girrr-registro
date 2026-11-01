#!/usr/bin/env python3
"""Prepara in una cartella di prova Curva, Radio testuale e Giornale.

Non importa publisher, generatori vocali o client database. Gli input sono
copiati in un sito temporaneo; gli archivi reali delle puntate restano intatti.
"""
import argparse
import hashlib
import html
import importlib.util
import json
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

R = Path(__file__).resolve().parent.parent
from giornale_classifica import integra


def leggi(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def scrivi(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def prepara(sito, eventi, testi, uscita, scripts_pdf=None):
    sito, eventi, testi, uscita = (Path(p).resolve() for p in (sito, eventi, testi, uscita))
    if uscita == sito or sito in uscita.parents:
        raise ValueError('La cartella di prova deve essere esterna al sito sorgente')
    marker = uscita / '.cronache-prova.json'
    if uscita.exists() and any(uscita.iterdir()) and not marker.exists():
        raise ValueError('Cartella non vuota e non appartenente alla prova cronache')
    d, snapshot, ev, t = (leggi(p) for p in (sito/'data.json', sito/'girrr/dati/lab-dati.json', eventi, testi))
    att = leggi(R/'calcoli/aspettative.json')
    firma = hashlib.sha256(json.dumps([d, snapshot, ev, t, att, leggi(R/'voci-src/nomi.json'), leggi(R/'voci-src/regole.json'), leggi(R/'voci-src/curva.json')], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    uscita.mkdir(parents=True, exist_ok=True)
    scrivi(marker, {'tipo': 'cronache-solo-prova', 'versione': 1})
    cartella = 'prova-' + firma[:16]
    dest = uscita / cartella
    dest.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        src = work/'sito'
        (src/'girrr/dati').mkdir(parents=True)
        scrivi(src/'data.json', d)
        scrivi(src/'girrr/dati/lab-dati.json', snapshot)
        scrivi(work/'eventi.json', ev)
        scrivi(work/'moviola.json', {})
        # Nessun archivio reale viene alterato o copiato: questa è una prova di soli testi.
        radio = subprocess.run([sys.executable, str(R/'voci-src/prepara_dati.py'), str(src),
            str(work/'eventi.json'), '--cronache-classifica', '--uscita', str(work/'radio')],
            check=True, capture_output=True, text=True)
        pronto = (work/'radio/dati.json').exists()
        manifest = {'modalita': 'solo_prova', 'invii': False, 'audio': False,
                    'firma_input': firma, 'cartella': cartella,
                    'stato': 'pronto' if pronto else 'in_attesa', 'giornata': None,
                    'cronaca': None, 'nota': radio.stdout.strip(), 'pdf': False}
        if pronto:
            radio_dati = leggi(work/'radio/dati.json')
            evento = radio_dati['zona_classifica']
            manifest.update(giornata=radio_dati['aw'][-1]['n'], cronaca=evento)
            subprocess.run([sys.executable, str(R/'calcoli/post_curva.py'), str(work/'eventi.json'),
                str(dest/'post-curva.json'), str(work/'moviola.json'), str(src/'data.json'),
                '--cronache-classifica'], check=True, capture_output=True, text=True)
            for name in ('dati.json', 'conferenze.json', 'curva.json'):
                shutil.copyfile(work/'radio'/name, dest/('radio-'+name))
            sys.path.insert(0, str(R/'voci-src'))
            spec = importlib.util.spec_from_file_location('copione_prova_cronache', R/'voci-src/copione.py')
            copione = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(copione)
            battute = copione.build(radio_dati, random.Random(manifest['giornata']), [],
                nomi=leggi(R/'voci-src/nomi.json'), conf=leggi(dest/'radio-conferenze.json'),
                curva_=leggi(dest/'radio-curva.json'), regole=leggi(R/'voci-src/regole.json'))
            scrivi(dest/'radio-copione.json', battute)
            nomi = leggi(R/'voci-src/nomi.json')
            (dest/'radio-copione.txt').write_text('\n\n'.join(nomi.get(k,k)+': '+tx for k,tx,_ in battute)+'\n', encoding='utf-8')
            # Stessa notizia e stessa chiave dei post e del copione, una sola inclusione.
            scrivi(dest/'testi-giornale.json', integra(t, d, att))
            scrivi(dest/'data.json', d)
            if scripts_pdf:
                scripts = dest/'scripts'
                scripts.mkdir(exist_ok=True)
                for name in ('pdf_giornale.py', 'pdf_settimana.py', 'toto_quote.py'):
                    shutil.copyfile(Path(scripts_pdf)/name, scripts/name)
                subprocess.run([sys.executable, str(R/'calcoli/render_giornale_prova.py'), str(dest)], check=True)
                manifest['pdf'] = True
            posts = leggi(dest/'post-curva.json')
            sezioni = '<h2>Curva · Testi preparati</h2>' + ''.join(
                '<article><h3>'+html.escape(p['h'])+(' · Commento' if p.get('re') else '')+
                '</h3><p>'+html.escape(p['body'])+'</p></article>' for p in posts)
            sezioni += '<h2>Radio · Copione testuale</h2><pre>'+html.escape((dest/'radio-copione.txt').read_text())+'</pre>'
            sezioni += '<h2>Giornale</h2><p>'+html.escape(leggi(dest/'testi-giornale.json').get('classifiche',''))+'</p>'
            if scripts_pdf:
                sezioni += '<p><a href="giornale.pdf">Apri il PDF di prova</a></p>'
        else:
            sezioni = '<p>Giornata non pronta: attesa della chiusura o dell’allineamento dei calcoli.</p>'
        pagina = ('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>O Girrr 5.5 · Cronache di prova</title><style>body{margin:0;background:#1d2a52;color:#fbf6ec;font:16px/1.6 system-ui}'
            'main{max-width:1000px;margin:auto;padding:24px}a{color:#ffd166}h1,h2{color:#ffd166}article{padding:16px;border:1px solid #ffffff40;'
            'border-radius:12px;margin:10px 0}p,pre{white-space:pre-wrap;overflow-wrap:anywhere}pre{font:inherit}small{color:#bfe3ff}</style>'
            '<main><a href="../../../index.html">‹ Registro</a><h1>Cronache di classifica · Anteprima 5.5</h1>'
            '<p><small>Preparazione locale dei testi. Nessun post inviato e nessun audio generato.</small></p>'+sezioni+'</main></html>')
        (dest/'index.html').write_text(pagina, encoding='utf-8')
        scrivi(dest/'manifest.json', manifest)
        scrivi(uscita/'manifest.json', manifest)
        (uscita/'index.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Cronache 5.5 · Prova</title><p><a href="'+cartella+'/index.html">Apri le cronache di prova 5.5</a></p></html>', encoding='utf-8')
    return dest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('sito', type=Path)
    p.add_argument('eventi', type=Path)
    p.add_argument('testi', type=Path)
    p.add_argument('uscita', type=Path)
    p.add_argument('--scripts-pdf', type=Path)
    a = p.parse_args()
    print(prepara(a.sito, a.eventi, a.testi, a.uscita, a.scripts_pdf))


if __name__ == '__main__':
    main()
