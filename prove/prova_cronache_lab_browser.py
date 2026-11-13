#!/usr/bin/env python3
"""Dal Lab al dossier e al PDF: sola lettura locale, cinque larghezze."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from rete_browser import browser

ROOT = os.environ.get('GIRRR_TEST_URL', 'http://127.0.0.1:8765')
OUT = Path('qa_artifacts'); OUT.mkdir(exist_ok=True)
esiti = []
with sync_playwright() as pw:
    b = browser(pw)
    for w in (320, 390, 768, 1280, 1440):
        c = b.new_context(viewport={'width':w, 'height':950})
        # Il Lab iniziale legge font e dati pubblici: per questa prova dei link
        # i caricamenti remoti non servono e non vengono inoltrati.
        c.route('https://**/*', lambda r:r.fulfill(status=200,body='{}',content_type='application/json'))
        p = c.new_page(); errori = []; risposte = []
        p.goto(ROOT+'/lab/index.html?nel-registro', wait_until='domcontentloaded')
        p.get_by_role('link', name='Apri le cronache di prova', exact=True).click()
        p.on('pageerror', lambda e:errori.append(str(e)))
        p.on('response', lambda r:risposte.append(r.status) if r.status>=400 else None)
        p.get_by_role('link', name='Apri le cronache di prova 5.5', exact=True).click()
        p.get_by_role('heading', name='Radio · Copione testuale').wait_for()
        assert p.locator('article').count() == 3
        assert 'Beppe Rovesciata:' in p.locator('pre').inner_text()
        assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        p.screenshot(path=str(OUT/f'cronache-dossier-{w}.png'), full_page=True)
        pdf = p.get_by_role('link', name='Apri il PDF di prova')
        with p.expect_response(lambda r:r.url.endswith('/giornale.pdf')) as risposta:
            pdf.click()
        # Chromium può aprire il visualizzatore PDF: il controllo del contenuto
        # avviene sulla risposta locale, senza dipendere dal visualizzatore.
        assert risposta.value.status == 200
        assert p.request.get(risposta.value.url).body().startswith(b'%PDF-')
        assert not errori and not risposte, (errori, risposte)
        esiti.append({'larghezza':w, 'percorso':'Lab → Cronache → Dossier → PDF', 'esito':'PASS'})
        c.close()
    b.close()
(OUT/'cronache-percorsi.json').write_text(json.dumps(esiti,ensure_ascii=False,indent=2)+'\n')
print('PASS Lab → dossier → PDF a 320/390/768/1280/1440, nessun overflow o errore')
