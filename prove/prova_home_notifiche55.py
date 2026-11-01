#!/usr/bin/env python3
"""Home reale, notifiche e navigazione: fonti pubbliche/risposte personali controllate."""
import copy
import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from rete_browser import browser, installa
R=Path(__file__).resolve().parent.parent
ROOT=os.environ.get('GIRRR_TEST_URL','http://127.0.0.1:8765')
OUT=R/'qa_artifacts';OUT.mkdir(exist_ok=True)
FIX=(R/'lab/cronache-prova/prova-dda1bc9a84fd84fa/data.json').read_text()
esiti=[]
with sync_playwright() as pw:
 b=browser(pw)
 for w in (320,390,768,1280,1440):
  for skin in ('lega','stadio'):
   c=b.new_context(viewport={'width':w,'height':950});installa(c)
   c.route('https://giandjcosta.github.io/o-fant-a-girrr/data.json',lambda r:r.fulfill(status=200,content_type='application/json',body=FIX))
   c.add_init_script("localStorage.setItem('og:53:team',JSON.stringify('Oranje VC'))")
   p=c.new_page();err=[];bad=[];db=[]
   p.on('pageerror',lambda e:err.append(str(e)))
   p.on('console',lambda m:err.append(m.text) if m.type=='error' else None)
   p.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
   p.on('request',lambda r:db.append(r.url) if '.supabase.co/' in r.url else None)
   p.goto(ROOT+'/anteprima/5.5/index-'+skin+'.html',wait_until='networkidle')
   p.locator('.v55-formgame').first.wait_for()
   assert p.locator('.v55-notice').bounding_box()['y']<p.locator('.v53-homehead').bounding_box()['y']
   assert p.locator('.v55-notice').bounding_box()['y']<450,(w,skin,'Notifiche troppo in basso')
   assert p.locator('#v53metrics .v53-metric').count()==0
   assert p.locator('.v55-points strong').inner_text()=='7'
   assert p.locator('.v55-last strong').inner_text()=='0–3'
   assert p.locator('.v55-formgame b').all_text_contents()==['5–1','0–2','2–1','2–2','0–3']
   assert 'Oranje VC' in p.locator('.v55-near .v55-me').inner_text()
   assert p.locator('.v55-header .v55-home-logo').is_visible()
   for summary in ('Le prossime tre sfide','Il rendimento degli allenatori','La storia dei tuoi allenatori','Le competizioni'):
    p.locator('.v55-more').filter(has=p.locator('summary').filter(has_text=summary)).locator('summary').click()
   assert p.locator('.v55-upcoming a').count()==3
   coach=p.locator('.v55-coaches a').first.inner_text()
   assert '40%' in coach and '2 vittorie / 5 gare' in coach and '1,4 punti a partita' in coach,coach
   assert p.locator('.v55-history .v55-value').all_text_contents()==['5','6']
   assert p.locator('.v55-history .v55-trace').count()==0,'Non collegare stagioni mancanti'
   assert p.locator('.v55-competitions a').nth(1).get_attribute('href').endswith('#coppa-2')
   assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(w,skin,'overflow')
   if w in (390,1280,1440):
    p.locator('.v53-home').screenshot(path=str(OUT/f'home-notifiche55-{skin}-{w}.png'))
    p.locator('.v55-more').filter(has=p.locator('summary').filter(has_text='La storia dei tuoi allenatori')).screenshot(path=str(OUT/f'storico-home55-{skin}-{w}.png'))
   if w in (390,1440):
    p.locator('#v55dashboard>summary').click()
    assert not p.locator('#v55dashboard').evaluate('(e)=>e.open')
    assert p.locator('.v55-summary').is_hidden() and p.locator('#v53news').is_visible()
    p.reload(wait_until='networkidle');p.locator('#v55compact').wait_for()
    assert not p.locator('#v55dashboard').evaluate('(e)=>e.open'),'Ricorda il riepilogo chiuso'
    assert 'Oranje VC' in p.locator('#v55compact').inner_text()
    p.locator('.v53-home').screenshot(path=str(OUT/f'home-richiusa55-{skin}-{w}.png'))
    p.locator('#v55dashboard>summary').focus();p.locator('#v55dashboard>summary').press('Enter')
    assert p.locator('.v55-summary').is_visible()
   p.locator('#v53news a').first.click();p.wait_for_url('**/tabellone-'+skin+'.html#lega-5')
   assert p.locator('.v55-return').is_visible()
   p.locator('.v55-return').click();p.wait_for_url('**/index-'+skin+'.html')
   p.locator('.cards a.c').filter(has_text='Tabellone').click();p.locator('#campo-link').click()
   p.wait_for_url('**/campo-'+skin+'.html?**');p.locator('.v55-header').wait_for()
   assert p.locator('.v55-return').get_attribute('href').split('#')[0].endswith('tabellone-'+skin+'.html')
   p.locator('#matches button').last.click()
   p.locator('.v55-skin-link').focus()
   assert 'partita=4' in p.locator('.v55-skin-link').get_attribute('href')
   p.locator('.v55-home-logo').click();p.wait_for_url('**/index-'+skin+'.html')
   assert not err and not bad and not db,(w,skin,err,bad,db)
   esiti.append({'skin':skin,'larghezza':w,'esito':'PASS','percorso':'Home → notifica → Tabellone → Indietro → Campo → Logo → Home'})
   c.close()
 # Notifiche personali: RPC esistenti simulate, mai inoltrate al database reale.
 for tipo in ('normale','errore','cambio_squadra'):
  c=b.new_context(viewport={'width':390,'height':950});installa(c)
  c.route('https://giandjcosta.github.io/o-fant-a-girrr/data.json',lambda r:r.fulfill(status=200,content_type='application/json',body=FIX))
  c.add_init_script("localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'CODICE_DI_PROVA'}));localStorage.setItem('og:53:team',JSON.stringify('Oranje VC'))")
  calls=[]
  def rpc(route):
   name=route.request.url.split('/')[-1];body=route.request.post_data_json;calls.append((name,body))
   assert body['p_team']=='Oranje VC' and body['p_code']=='CODICE_DI_PROVA'
   if tipo=='errore':route.fulfill(status=403,content_type='application/json',body='{"message":"Codice non valido"}');return
   if name=='notifiche_segna_lette':route.fulfill(status=200,content_type='application/json',body='{"chiavi":[]}');return
   assert name=='notifiche_stato'
   route.fulfill(status=200,content_type='application/json',body=json.dumps({'chiavi':[],'eventi':[
    {'chiave':'risp-999','tipo':'curva','ic':'💬','titolo':'Risposta di prova','testo':'Messaggio controllato','nuova':True},
    {'chiave':'prest-999-richiesta','tipo':'totogirrr','ic':'🤝','titolo':'Prestito di prova','testo':'Richiesta controllata','nuova':True},
    {'chiave':'sfida-999','tipo':'derby','ic':'⚔️','titolo':'Derby di prova','testo':'Sfida controllata','nuova':True}]}))
  c.route('https://*.supabase.co/rest/v1/rpc/notifiche_*',rpc)
  p=c.new_page();p.goto(ROOT+'/anteprima/5.5/index-lega.html',wait_until='networkidle');p.locator('.v55-formgame').first.wait_for()
  assert not any(x[0]=='notifiche_segna_lette' for x in calls),'Nessuna lettura automatica'
  if tipo=='normale':
   assert 'Risposta di prova' in p.locator('#v53news').inner_text()
   links=p.locator('#v53news a');assert links.first.get_attribute('href').endswith('/curva-lega.html')
   assert 't=prestiti' in links.nth(1).get_attribute('href') and 'o-fant-a-girrr' not in links.nth(1).get_attribute('href')
   p.locator('#v53read').click();p.wait_for_timeout(100)
   assert sum(x[0]=='notifiche_segna_lette' for x in calls)==1
  elif tipo=='errore':
   assert 'Risposta di prova' not in p.locator('#v53news').inner_text()
   assert p.locator('#v53news a').count()>0
  else:
   p.locator('#v53team').select_option('AFA SELECCION')
   assert 'Risposta di prova' not in p.locator('#v53news').inner_text()
   assert len(calls)==1
  c.close()
 # La modalità ospite di Claude prevale anche su credenziali già salvate.
 for skin in ('lega','stadio'):
  for w in (390,1440):
   c=b.new_context(viewport={'width':w,'height':950});installa(c)
   c.add_init_script("localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'CODICE_DI_PROVA'}))")
   p=c.new_page();db=[]
   p.on('request',lambda r:db.append(r.url) if '.supabase.co/' in r.url else None)
   p.goto(ROOT+'/anteprima/5.5/index-'+skin+'.html?ospite=1',wait_until='networkidle')
   p.locator('.v55-summary').wait_for()
   assert p.locator('html').get_attribute('class').find('v53-ospite')>=0
   assert p.locator('a.c').filter(has_text='Totogirrr').is_hidden()
   assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   p.locator('#v53read').click()
   p.locator('.v55-notifications-link').click();p.locator('#v53notifstato').wait_for()
   assert p.locator('#v53notifstato').inner_text().startswith('Modalità ospite:')
   assert not db,('Ospite con credenziali salvate: nessuna RPC',skin,w,db)
   c.close()
 # Percorso fuori dal Registro: nessun selettore di altri club per la futura Home.
 from urllib.parse import urlparse
 for skin in ('lega','stadio'):
  for accesso in (False,True):
   c=b.new_context(viewport={'width':390,'height':950});installa(c)
   c.route('https://giandjcosta.github.io/o-fant-a-girrr/data.json',lambda r:r.fulfill(status=200,content_type='application/json',body=FIX))
   c.add_init_script("localStorage.setItem('og:53:team',JSON.stringify('AFA SELECCION'))"+ (";localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'CODICE_DI_PROVA'}))" if accesso else ''))
   def futuro(route):
    name=Path(urlparse(route.request.url).path).name
    f=R/'anteprima/5.5'/name
    if name=='preview-guard.js':f=R/'anteprima'/name
    assert f.is_file(),name
    route.fulfill(path=str(f))
   c.route(ROOT+'/sito-futuro/**',futuro)
   p=c.new_page();p.goto(ROOT+'/sito-futuro/girrr/index-'+skin+'.html',wait_until='networkidle')
   p.locator('#v55dashboard').wait_for();s=p.locator('#v53team')
   assert s.is_disabled() and s.locator('option').count()==1
   if accesso:
    assert s.input_value()=='Oranje VC','Ignora una squadra diversa rimasta nella prova'
    assert p.locator('.v55-near .v55-me th').inner_text()=='Oranje VC'
    s.evaluate("e=>{e.add(new Option('AFA SELECCION','AFA SELECCION'));e.value='AFA SELECCION';e.dispatchEvent(new Event('change'))}")
    assert s.input_value()=='Oranje VC'
   else:
    assert p.locator('.v55-summary').count()==0
    assert 'Entra con la tua squadra' in p.locator('#v53metrics').inner_text()
   c.close()
 b.close()
(OUT/'home-notifiche55-esiti.json').write_text(json.dumps(esiti,ensure_ascii=False,indent=2)+'\n')
print('PASS Home integrata × due skin × cinque larghezze; tendina persistente e tastiera, sola squadra personale, prova anonima, notifiche, navigazione e ospite')
