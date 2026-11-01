#!/usr/bin/env python3
"""Prova completa: calendario → post/commento → copione → testi → PDF locale.
Le sole richieste remote leggono dati e sorgenti pubblici. Nessun invio o audio.
"""
import json
import copy
import shutil
import sys
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
from rete_browser import browser
R=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(R/'calcoli'))
from prepara_cronache import prepara
from zone_classifica import evento
OUT=R/'qa_artifacts';SRC=OUT/'cronache-input';SITE=SRC/'sito'
(SITE/'girrr/dati').mkdir(parents=True,exist_ok=True)
(SRC/'scripts').mkdir(exist_ok=True)
def leggi(url):
    with urllib.request.urlopen(url,timeout=30) as r:return r.read()
for name in ('data.json','girrr/dati/lab-dati.json'):
    (SITE/name).write_bytes(leggi('https://giandjcosta.github.io/o-fant-a-girrr/'+name))
for name in ('pdf_giornale.py','pdf_settimana.py','toto_quote.py'):
    (SRC/'scripts'/name).write_bytes(leggi('https://raw.githubusercontent.com/giandjcosta/o-fant-a-girrr/gh-pages/scripts/'+name))
(SRC/'eventi.json').write_text('[]')
(SRC/'testi.json').write_text(json.dumps({'titolone':'Il punto della classifica','classifiche':'Il commento della redazione.'}))
dest=prepara(SITE,SRC/'eventi.json',SRC/'testi.json',OUT/'pacchetto-cronache',SRC/'scripts')
manifest=json.loads((dest/'manifest.json').read_text())
assert manifest['stato']=='pronto',manifest
assert manifest['invii'] is False and manifest['audio'] is False
cronaca=manifest['cronaca'];posts=json.loads((dest/'post-curva.json').read_text())
radio=json.loads((dest/'radio-dati.json').read_text())
assert radio['cronache_classifica_attive'] is True and radio['zona_classifica']==cronaca
if cronaca:
    assert len(posts)==3 and all(p['cronaca']==cronaca['chiave'] for p in posts)
    assert posts[2]['re']==posts[0]['chiave']
    assert (dest/'radio-copione.txt').read_text().count(cronaca['testo'])==1
else:
    assert posts==[]
fit=json.loads((dest/'pdf-esito.json').read_text())
assert len(fit['impaginazione'])==4 and all(x['ci_sta'] for x in fit['impaginazione'])
with sync_playwright() as pw:
    b=browser(pw);c=b.new_context();c.route('**/*',lambda r:r.abort());p=c.new_page()
    p.set_content((dest/'giornale.html').read_text())
    if cronaca:assert p.locator('.pg').nth(1).inner_text().count(cronaca['testo'])==1
    b.close()
for src,name in [('giornale.pdf','cronaca-giornale-prova.pdf'),('giornale-pagina2.png','cronaca-giornale-pagina2.png'),('pdf-esito.json','pdf-cronaca-esito.json')]:
    shutil.copyfile(dest/src,OUT/name)
print('PASS flusso completo: post/commento, copione, Giornale e PDF di quattro pagine; nessun invio o audio')

# Anche se nel turno successivo è finita una partita, l'edizione resta sul turno chiuso.
prova=copy.deepcopy(json.loads((SITE/'data.json').read_text()))
prossimo=next((g for g in prova['cal']['lega'] if g['n']>manifest['giornata']),None)
if prossimo:
    prossimo['m'][0][1:3]=[71,68]
    prossimo['m'][0][4]='2-1'
    parziale=SRC/'sito-parziale';(parziale/'girrr/dati').mkdir(parents=True,exist_ok=True)
    (parziale/'data.json').write_text(json.dumps(prova))
    shutil.copyfile(SITE/'girrr/dati/lab-dati.json',parziale/'girrr/dati/lab-dati.json')
    prima=(parziale/'data.json').read_bytes()
    dest2=prepara(parziale,SRC/'eventi.json',SRC/'testi.json',OUT/'pacchetto-parziale',SRC/'scripts')
    esito=json.loads((dest2/'pdf-esito.json').read_text())
    assert esito['giornata']==manifest['giornata']
    assert (parziale/'data.json').read_bytes()==prima
    print('PASS PDF con turno successivo parziale: resta sulla giornata chiusa, input invariato')
