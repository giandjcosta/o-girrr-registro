#!/usr/bin/env python3
"""PDF locale con il generatore del sito letto via HTTPS, mai eseguito come CLI.
Scarica i tre sorgenti in qa_artifacts/pdf-src, usa dati pubblici e verifica
la cronaca nella seconda pagina e il controllo d'impaginazione originale.
"""
import importlib.util
import json
import sys
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
from rete_browser import browser,installa
R=Path(__file__).resolve().parent.parent
OUT=R/'qa_artifacts';SRC=OUT/'pdf-src/scripts';SRC.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'calcoli'))
from giornale_classifica import integra
from zone_classifica import evento

def leggi(url):
    with urllib.request.urlopen(url,timeout=30) as r:return r.read()
for f in ('pdf_giornale.py','pdf_settimana.py','toto_quote.py'):
    (SRC/f).write_bytes(leggi('https://raw.githubusercontent.com/giandjcosta/o-fant-a-girrr/gh-pages/scripts/'+f))
d=leggi('https://giandjcosta.github.io/o-fant-a-girrr/data.json')
(SRC.parent/'data.json').write_bytes(d);d=json.loads(d)
att=json.loads((R/'calcoli/aspettative.json').read_text())
e=evento(d,att)
assert e,'Questa prova richiede una giornata pubblica con cronaca significativa'
t=integra({'titolone':'Il punto della classifica'},d,att)
sys.path.insert(0,str(SRC))
spec=importlib.util.spec_from_file_location('pdf_giornale_riferimento',SRC/'pdf_giornale.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
h,n=g.costruisci(t)
(OUT/'giornale-cronaca.html').write_text(h)
with sync_playwright() as pw:
    b=browser(pw);c=b.new_context(viewport={'width':1000,'height':1200});installa(c);p=c.new_page()
    p.set_content(h);p.emulate_media(media='print');p.wait_for_timeout(500)
    assert e['testo'] in p.locator('.pg').nth(1).inner_text()
    fit=p.evaluate(g.FIT_JS)
    assert len(fit)==4 and all(x['ci_sta'] for x in fit),fit
    p.locator('.pg').nth(1).screenshot(path=str(OUT/'cronaca-giornale-pagina2.png'))
    p.pdf(path=str(OUT/'cronaca-giornale-prova.pdf'),format='A4',prefer_css_page_size=True,print_background=True)
    b.close()
(OUT/'pdf-cronaca-esito.json').write_text(json.dumps({'giornata':n,'evento':e,'impaginazione':fit},ensure_ascii=False,indent=2))
print('PASS generatore PDF originale: cronaca nella pagina 2, quattro pagine nei margini',fit)
