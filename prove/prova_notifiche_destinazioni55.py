#!/usr/bin/env python3
"""Clic su tutta la scheda → contenuto preciso; RPC controllate, nessuna scrittura."""
import copy
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from rete_browser import browser, installa
R=Path(__file__).resolve().parent.parent
ROOT=os.environ.get('GIRRR_TEST_URL','http://127.0.0.1:8765')
OUT=R/'qa_artifacts';OUT.mkdir(exist_ok=True)
D=json.loads((R/'lab/cronache-prova/prova-dda1bc9a84fd84fa/data.json').read_text())
CODE='CODICE_DI_PROVA'
h=2166136261
for ch in 'Oranje VC|'+CODE:h=((h^ord(ch))*16777619)&0xffffffff
digits='0123456789abcdefghijklmnopqrstuvwxyz';hashed=''
while h:hashed=digits[h%36]+hashed;h//=36
D.setdefault('lock',{})['Oranje VC']=hashed
NOW=1793534400000
def event(key,title,detail,tipo='curva'):
 return {'chiave':key,'tipo':tipo,'ic':'💬','titolo':title,'testo':detail,'quando':'2026-11-01T12:00:00Z','nuova':True}
EVENTS=[
 event('risp-901','Risposta al coro','Risposta precisa di Grodah'),
 event('app-p17-2','Applausi al coro','Il coro preciso'),
 event('app-r902-1','Applauso alla risposta','La risposta precisa'),
 event('prest-44-richiesta','Richiesta di prestito','Grodah · 150 · Tocca a te rispondere','totogirrr'),
 event('mov-55','Totogirrr: +50','Rimborso registrato','totogirrr'),
 event('sfida-66','Grodah ti ha sfidato','La sfida precisa','derby'),
 event('sfida-r-67','WOA ha accettato la tua sfida','Il nome della sfida','derby')]
def feed(posts=None):
 return {'v':5,'ok':True,'posts':posts if posts is not None else [
  {'id':17,'team':'Oranje VC','body':'Il coro preciso','ts':NOW,'hi':False},
  {'id':18,'team':'Grodah','body':'Il secondo coro','ts':NOW-1000,'hi':False}],
  'replies':[{'id':901,'k':'p17','team':'Grodah','body':'Risposta precisa di Grodah','ts':NOW+1000},
             {'id':902,'k':'a57','team':'Oranje VC','body':'La risposta precisa','ts':NOW+2000}],
  'react':[],'mine':[],'follow':[],'prof':{},'polls':[],
  'adm':[{'id':57,'h':'girrr_sport','body':'Il coro ufficiale','ts':NOW-2000,'hi':False}],
  'rt':[],'lk':[]}
report=[]
with sync_playwright() as pw:
 b=browser(pw)
 for w in tuple(map(int,os.environ.get('GIRRR_TEST_WIDTHS','320,390,768,1280,1440').split(','))):
  for skin in ('lega','stadio'):
   c=b.new_context(viewport={'width':w,'height':950});installa(c)
   c.route('https://giandjcosta.github.io/o-fant-a-girrr/data.json',lambda r:r.fulfill(json=D))
   p=c.new_page();errors=[];http=[]
   p.on('pageerror',lambda e:errors.append(str(e)))
   p.on('response',lambda r:http.append((r.status,r.url)) if r.status>=400 else None)
   url=ROOT+'/anteprima/5.5/notifiche-'+skin+'.html'
   def center():p.goto(url,wait_until='networkidle');p.locator('.v55-notiflink').first.wait_for()
   def click(title):
    card=p.locator('.v53-notifcard').filter(has=p.locator('b',has_text=title)).first
    a=card.locator('a');box=card.bounding_box();ab=a.bounding_box()
    assert abs(ab['width']-box['width'])<=3 and abs(ab['height']-box['height'])<=3
    card.click(position={'x':box['width']-8,'y':box['height']-8})
   center()
   assert p.locator('#v53notifications').bounding_box()['width']<=880
   if w in (390,1440):p.screenshot(path=str(OUT/f'notifiche-compatte55-{skin}-{w}.png'),full_page=True)
   click('Classifica aggiornata');expect(p.locator('#tab')).to_have_attribute('data-v55-destinazione','classifica')
   assert p.url.endswith('#lega-5') and p.evaluate('document.activeElement.id')=='tab'
   center();click('Risultati della 5ª');expect(p.locator('#board')).to_have_attribute('data-v55-destinazione','risultati')
   center();click('Prossimo turno');expect(p.locator('#board')).to_have_attribute('data-v55-destinazione','risultati')
   assert p.url.endswith('#lega-6')
   center();click('CRISI IMPREVISTA');p.locator('#v55cronaca').wait_for()
   assert 'WOA' in p.locator('#v55cronaca').inner_text() and p.evaluate('document.activeElement.id')=='v55cronaca'
   center();click('Sondaggio della Curva');expect(p.locator('#v53poll')).to_have_attribute('data-giornata','6')
   assert p.locator('#v53vote').is_visible() and p.evaluate('document.activeElement.id')=='v53poll'
   center();click('Annuario 2026/27')
   target=p.locator('[data-v55-stagione="2026/27"]');target.wait_for()
   assert target.evaluate('(e)=>e.open') and p.locator('[data-oro=annuario]').get_attribute('aria-pressed')=='true'
   assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   assert not errors and not http,(skin,w,errors,http)
   report.append({'skin':skin,'larghezza':w,'esito':'PASS','destinazioni':['risultati G5','classifica G5','calendario G6','cronaca WOA','sondaggio G6','Annuario 2026/27']})
   print('PASS schede intere e destinazioni pubbliche',skin,w,flush=True);c.close()
 # Dati personali: risposte, applausi, prestiti, movimenti e sfide specifici.
 for skin in ('lega','stadio'):
  c=b.new_context(viewport={'width':390,'height':950});installa(c)
  c.route('https://giandjcosta.github.io/o-fant-a-girrr/data.json',lambda r:r.fulfill(json=D))
  c.add_init_script("localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'CODICE_DI_PROVA'}))")
  calls=[]
  def rpc(route):
   name=route.request.url.split('/')[-1];body=route.request.post_data_json;calls.append((name,body))
   assert name in ('notifiche_stato','curva_feed'),('Nessuna scrittura o lettura con effetti',name)
   assert body['p_team']=='Oranje VC' and body['p_code']==CODE
   route.fulfill(json={'chiavi':[],'eventi':EVENTS} if name=='notifiche_stato' else feed())
  c.route('https://*.supabase.co/rest/v1/rpc/*',rpc)
  p=c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
  for e in EVENTS:
   p.goto(ROOT+'/anteprima/5.5/notifiche-'+skin+'.html',wait_until='networkidle')
   card=p.locator('.v53-notifcard').filter(has=p.locator('b',has_text=e['titolo'])).first
   card.locator('a').focus();card.locator('a').press('Enter')
   dest=p.locator('[data-v55-destinazione="'+e['chiave']+'"]');dest.wait_for()
   assert dest.is_visible()
   assert e['testo'] in dest.inner_text() or e['chiave']=='app-p17-2'
   assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   if e['tipo']=='curva':
    assert p.locator('#vista').is_visible()
    assert p.evaluate("""async()=>{let r=await fetch('https://qmjqfgmvimsuxvghetgi.supabase.co/rest/v1/rpc/curva_scrivi',{method:'POST',body:'{}'});return r.status}""")==403
   else:
    assert p.locator('#v55record').get_attribute('data-notifica')==e['chiave']
   assert not errs,(skin,e['chiave'],errs)
  report.append({'skin':skin,'larghezza':390,'esito':'PASS','personali':[e['chiave'] for e in EVENTS],'RPC':'solo letture simulate'})
  p.goto(ROOT+'/anteprima/'+('attuale.html' if skin=='lega' else 'index.html')+'?notifica=sfida-66&skin='+skin+'#sport',wait_until='networkidle')
  p.locator('[data-v55-destinazione="sfida-66"]').wait_for()
  p.locator('.v55-record-nav a').last.click()
  p.locator('#v53notifications article').first.wait_for()
  assert p.locator('#v55record').count()==0
  print('PASS sette contenuti personali specifici',skin,flush=True);c.close()
 # Archivio e contenuto assente: mai ricadere sulla pagina generale.
 for missing in (False,True):
  c=b.new_context(viewport={'width':390,'height':950});installa(c)
  c.route('https://giandjcosta.github.io/o-fant-a-girrr/data.json',lambda r:r.fulfill(json=D))
  c.add_init_script("localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'CODICE_DI_PROVA'}))")
  pages=[]
  def archive(route):
   body=route.request.post_data_json;pages.append(body)
   posts=[] if missing else ([{'id':i,'team':'Grodah','body':'Coro precedente '+str(i),'ts':NOW+i*10000,'hi':False} for i in range(300,150,-1)] if 'p_before' not in body else feed()['posts'])
   route.fulfill(json=feed(posts))
  c.route('https://*.supabase.co/rest/v1/rpc/curva_feed',archive)
  p=c.new_page();p.goto(ROOT+'/anteprima/5.5/curva-lega.html?notifica=risp-901',wait_until='networkidle')
  if missing:
   expect(p.locator('.v55-curva-target')).to_contain_text('Coro non disponibile');assert p.locator('#vista').is_hidden()
   p.locator('#nav [data-v=home]').first.click();assert p.locator('#vista').is_visible()
  else:
   p.locator('[data-v55-destinazione="risp-901"]').wait_for();assert len(pages)==2,'Cerca anche in archivio'
  c.close()
 # Una chiave assente e credenziali mancanti non mostrano i prestiti simulati.
 for logged in (False,True):
  c=b.new_context(viewport={'width':320,'height':950});installa(c)
  if logged:c.add_init_script("localStorage.setItem('fg',JSON.stringify({team:'Grodah',code:'CODICE_DI_PROVA'}))")
  c.route('https://*.supabase.co/rest/v1/rpc/notifiche_stato',lambda r:r.fulfill(json={'chiavi':[],'eventi':[]}))
  p=c.new_page();p.goto(ROOT+'/anteprima/totogirrr-52.html?skin=lega&t=prestiti&notifica=prest-44-richiesta',wait_until='networkidle')
  expect(p.locator('#v55record')).to_contain_text('non disponibile' if logged else 'Entra con la tua squadra')
  assert p.locator('[data-pr]').count()==0 and p.locator('#pr_send').count()==0
  c.close()
 b.close()
(OUT/'notifiche-destinazioni55-esiti.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('PASS notifiche: aree cliccabili, destinazioni precise, archivio, contenuto assente e nessuna scrittura')
