#!/usr/bin/env python3
"""Percorsi e regressioni della 5.3 completa: dati pubblici, RPC isolate, cinque viewport."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from rete_browser import installa,browser
ROOT='http://127.0.0.1:8765/anteprima/5.3/'
OUT=Path('qa_artifacts');OUT.mkdir(exist_ok=True)
reports=[]
with sync_playwright() as pw:
 b=browser(pw)
 for w in (320,390,768,1280,1440):
  for skin in ('lega','stadio'):
   c=b.new_context(viewport={'width':w,'height':950});installa(c);p=c.new_page();errs=[];bad=[];db=[]
   p.on('pageerror',lambda e:errs.append(str(e)))
   p.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
   p.on('response',lambda r:bad.append([r.status,r.url]) if r.status>=400 else None)
   p.on('request',lambda r:db.append(r.url) if '.supabase.co/' in r.url else None)
   def check(section):
    p.wait_for_timeout(600)
    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(skin,w,section,'overflow')
    assert not errs,(skin,w,section,errs[:5],bad[:5])
    assert not bad,(skin,w,section,bad[:5])
    assert not db,(skin,w,section,'richieste al database',db)
   p.goto(ROOT+'index-'+skin+'.html',wait_until='networkidle')
   p.locator('#v53metrics .v53-metric').first.wait_for();assert p.locator('.cards').count()==1
   assert p.locator('.v53-menu').count()==0
   check('Home');p.screenshot(path=str(OUT/f'53-home-{skin}-{w}.png'),full_page=True)
   p.locator('.cards a.c').filter(has_text='Tabellone').click();p.locator('#tab .numpos').first.wait_for()
   # Tutte le funzioni precedenti devono sopravvivere all'integrazione.
   assert p.locator('#tab .clubgraph').count()==10
   assert p.locator('#tab .formadots').count()>0
   p.locator('#tab .clubgraph').first.click();p.locator('.grafpos svg').wait_for()
   p.locator('#v53boardtabs [data-view=center]').click();p.locator('#v53matchstats .score').first.wait_for()
   assert 'Fantapunti' in p.locator('#v53matchstats').inner_text()
   assert 'Punti in classifica assegnati' in p.locator('#v53matchstats').inner_text()
   p.locator('#v53boardtabs [data-view=compare]').click();p.locator('#v53from').select_option(index=0)
   p.get_by_role('tab',name='Champions Cup',exact=True).click();p.locator('#chips [data-n="11"]').click();p.wait_for_timeout(350)
   assert 'quarti' in p.locator('#tit').inner_text().lower(),p.locator('#tit').inner_text()
   p.get_by_role('tab',name='Campionato',exact=True).click();check('Tabellone')
   p.screenshot(path=str(OUT/f'53-tabellone-{skin}-{w}.png'),full_page=True)
   p.locator('#campo-link').click();p.locator('.pitch svg').wait_for();check('Campo')
   p.screenshot(path=str(OUT/f'53-campo-{skin}-{w}.png'),full_page=True)
   p.locator('#matches button').last.click();assert 'partita=4' in p.url
   p.locator('#ritorno-tabellone').click();p.locator('a.back').click()
   p.locator('.cards a.c').filter(has_text="Albo d'oro").click();p.locator('.oro-scroll').wait_for()
   p.locator('[data-oro=annuario]').click();p.locator('.ann-anno').first.wait_for()
   # Le stagioni storiche compaiono prima della risposta del calendario corrente.
   expect(p.locator('#view')).to_contain_text('Da assegnare',timeout=20000)
   assert p.locator('.ann-anno').count()>=10
   assert p.locator('.oro-scroll').evaluate('(e)=>getComputedStyle(e).flexWrap')=='nowrap'
   check('Albo');p.screenshot(path=str(OUT/f'53-albo-{skin}-{w}.png'),full_page=True)
   p.locator('a.oback').click();p.locator('a.cvw').click()
   p.locator('#v53vote input').first.wait_for();p.locator('#v53vote input').first.check();p.locator('#v53vote button').click()
   assert '1 voti di prova' in p.locator('#v53poll').inner_text()
   p.locator('#v53vote button').click();assert '2 voti di prova' not in p.locator('#v53poll').inner_text()
   p.locator('#v53message').fill('Una partita da seguire <b>davvero</b>');p.locator('#v53comment button').click()
   assert '<b>davvero</b>' in p.locator('#v53usercomments').inner_text()
   assert p.locator('#v53dialog .v53-comment').count()>=10
   assert p.locator('#vista').count()==1 and p.locator('#nav').count()==1
   # Anche una chiamata costruita a mano deve restare locale.
   r=p.evaluate("""async()=>{const r=await fetch(new Request('https://qmjqfgmvimsuxvghetgi.supabase.co/rest/v1/rpc/curva_scrivi',{method:'POST',body:'{}'}));return r.status}""")
   assert r==403
   assert p.evaluate("navigator.sendBeacon('https://qmjqfgmvimsuxvghetgi.supabase.co/rest/v1/rpc/curva_scrivi','{}')")==False
   check('Curva');p.screenshot(path=str(OUT/f'53-curva-{skin}-{w}.png'),full_page=True)
   p.get_by_role('link',name='Notifiche',exact=True).first.click();p.locator('#v53notifications article').first.wait_for()
   body=p.locator('body').inner_text().lower();assert 'automazion' not in body and 'debug' not in body
   p.locator('#v53filters [data-f=curva]').click();assert 'Sondaggio della Curva' in p.locator('#v53notifications').inner_text()
   p.locator('#v53markread').click();assert p.locator('#v53notifications [data-read=false]').count()==0
   check('Notifiche');p.screenshot(path=str(OUT/f'53-notifiche-{skin}-{w}.png'),full_page=True)
   reports.append({'skin':skin,'larghezza':w,'esito':'PASS','sezioni':['Home','Tabellone','Campo','Albo','Curva','Notifiche'],'database':'0 richieste'})
   print('PASS 5.3 completa',skin,w,flush=True);c.close()
 b.close()
(OUT/'53-completa-esiti.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
