#!/usr/bin/env python3
"""Due bozze, due skin, cinque larghezze: dati del calendario e nessun database."""
import json
import copy
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from rete_browser import browser, installa
R=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(R/'calcoli'))
from zone_classifica import storia
FIX=R/'lab/cronache-prova/prova-dda1bc9a84fd84fa/data.json'
d=json.loads(FIX.read_text());hist=storia(d)
ROOT=os.environ.get('GIRRR_TEST_URL','http://127.0.0.1:8765')
OUT=R/'qa_artifacts';OUT.mkdir(exist_ok=True)
esiti=[]
with sync_playwright() as pw:
 b=browser(pw)
 for w in (320,390,768,1280,1440):
  for skin in ('lega','stadio'):
   c=b.new_context(viewport={'width':w,'height':1000});installa(c)
   c.route('https://giandjcosta.github.io/o-fant-a-girrr/data.json',lambda r:r.fulfill(status=200,content_type='application/json',body=FIX.read_text()))
   p=c.new_page();errors=[];bad=[];scritture=[]
   p.on('pageerror',lambda e:errors.append(str(e)))
   p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   p.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
   p.on('request',lambda r:scritture.append(r.url) if r.method!='GET' or '.supabase.co' in r.url else None)
   p.goto(ROOT+'/lab/prova-home-unica55.html?skin='+skin,wait_until='networkidle')
   p.locator('.chart svg').wait_for()
   for mode in ('a','b'):
    p.locator('button[data-bozza='+mode+']').click()
    assert p.locator('.draft-card').count()==1 and p.locator('.v53-metric').count()==0
    assert p.locator('#team').input_value()=='Oranje VC'
    expected=[s['posizioni']['Oranje VC'] for s in hist[-5:]]
    if mode=='a':
     assert p.locator('.chart text.value').all_text_contents()==[str(n)+'º' for n in expected]
     assert p.locator('.position').inner_text().strip()=='6ª'
     assert p.locator('.points b').inner_text()=='7'
     assert p.locator('.fixture-line .result').inner_text()=='0–3'
    else:
     assert p.locator('.chart text.value').all_text_contents()==['V','P','V','N','P']
     assert p.locator('.big-score').inner_text()=='3–0'
    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(w,skin,mode,'overflow')
    assert not errors and not bad and not scritture,(errors,bad,scritture)
    assert p.locator('.actions a').first.get_attribute('href').endswith('tabellone-'+skin+'.html')
    assert p.locator('.chart svg a').count()==5
    p.locator('.draft-card').screenshot(path=str(OUT/f'home-unica-{mode}-{skin}-{w}.png'))
    if w in (390,1440):p.screenshot(path=str(OUT/f'home-unica-pagina-{mode}-{skin}-{w}.png'),full_page=True)
    esiti.append({'bozza':mode,'skin':skin,'larghezza':w,'esito':'PASS','database':'Nessuna richiesta'})
   if w==320:
    for t in d['teams']:
     p.locator('#team').select_option(t['name'])
     assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),t['name']
    p.locator('#team').select_option('Oranje VC')
    p.locator('button[data-skin='+('stadio' if skin=='lega' else 'lega')+']').click()
    assert p.locator('.actions a').first.get_attribute('href').endswith('tabellone-'+('stadio' if skin=='lega' else 'lega')+'.html')
    p.locator('#read').click();assert p.locator('#news-text').inner_text()=='Nessuna novità da leggere.'
   c.close()
 # Un turno parziale non deve far avanzare la linea o la classifica.
 for tipo in ('parziale','nessun_risultato','errore'):
  c=b.new_context(viewport={'width':320,'height':900});installa(c)
  fixture=copy.deepcopy(d)
  if tipo=='parziale':fixture['cal']['lega'][2]['m'][0][4]='-'
  if tipo=='nessun_risultato':fixture['cal']['lega'][0]['m'][0][4]='-'
  c.route('https://giandjcosta.github.io/o-fant-a-girrr/data.json',lambda r:r.fulfill(status=503,body='Non disponibile') if tipo=='errore' else r.fulfill(status=200,content_type='application/json',body=json.dumps(fixture)))
  p=c.new_page();p.goto(ROOT+'/lab/prova-home-unica55.html',wait_until='networkidle')
  if tipo=='errore':
   assert p.locator('#team').is_disabled() and 'non è raggiungibile' in p.locator('#contenuto').inner_text()
  elif tipo=='nessun_risultato':
   assert p.locator('.chart svg').count()==0 and 'Classifica in attesa' in p.locator('#contenuto').inner_text()
  else:
   assert p.locator('.chart text.value').all_text_contents()==['1º','5º']
   assert p.locator('#day').inner_text()=='Dopo la 2ª giornata'
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  c.close()
 b.close()
(OUT/'home-unica55-esiti.json').write_text(json.dumps(esiti,ensure_ascii=False,indent=2)+'\n')
print('PASS due bozze × due skin × cinque larghezze, grafici reali, cambio squadra e nessuna richiesta al database')
