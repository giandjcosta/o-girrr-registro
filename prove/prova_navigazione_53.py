#!/usr/bin/env python3
"""Home → Tabellone → Campo → Home → Albo, nelle due skin e cinque viewport.
Rete pubblica via TLS verificato; RPC simulate, mai inoltrate. Screenshot reali.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from rete_browser import installa,browser
ROOT='http://127.0.0.1:8765'
OUT=Path('qa_artifacts');OUT.mkdir(exist_ok=True)
esiti=[]
with sync_playwright() as pw:
    b=browser(pw)
    for w in (320,390,768,1280,1440):
        for skin in ('lega','stadio'):
            c=b.new_context(viewport={'width':w,'height':950},device_scale_factor=1)
            installa(c);p=c.new_page();errori=[];risposte=[]
            p.on('pageerror',lambda e:errori.append(str(e)))
            p.on('console',lambda m:errori.append(m.text) if m.type=='error' else None)
            p.on('response',lambda r:risposte.append([r.status,r.url]) if r.status>=400 else None)
            def check(nome):
                p.wait_for_timeout(800)
                assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(skin,w,nome,'overflow')
                assert not errori,(skin,w,nome,errori)
                assert not risposte,(skin,w,nome,risposte)
            p.goto(ROOT+'/lab/index.html',wait_until='networkidle')
            p.get_by_role('link',name='Anteprima 5.3 · '+skin.title(),exact=True).click()
            p.wait_for_url('**/home-'+skin+'.html');check('Home dal Lab')
            # Anche il vecchio ingresso dell’app deve arrivare alla stessa Home aggiornata.
            app='attuale.html' if skin=='lega' else 'index.html'
            p.goto(ROOT+'/anteprima/'+app,wait_until='networkidle');p.wait_for_url('**/home-'+skin+'.html')
            p.locator('a.c').filter(has_text='Tabellone').click()
            p.wait_for_url('**/tabellone-'+skin+'.html');p.locator('#tab .numpos').first.wait_for();check('Tabellone')
            assert p.locator('#tab tbody tr').count()==10
            assert p.locator('#tab .zona-1 .numpos').evaluate('(e)=>getComputedStyle(e).color')=='rgb(255, 209, 102)'
            assert p.locator('#tab .zona-last .numpos').evaluate('(e)=>getComputedStyle(e).color')=='rgb(255, 114, 134)'
            for selector in ('.dr','.pt','.fp'):
                assert p.locator('#tab tbody '+selector).first.evaluate('(e)=>getComputedStyle(e).color')=='rgb(251, 246, 236)'
            th=p.locator('#tab th.w').first
            assert th.is_visible()==(w>=560)
            p.screenshot(path=str(OUT/f'integrato-tabellone-{skin}-{w}.png'),full_page=True)
            # Coppa resta navigabile con regole e risultati; Campo riguarda il Campionato.
            p.get_by_role('tab',name='Champions Cup',exact=True).click();check('Champions Cup')
            assert p.locator('#campo-link').is_hidden()
            p.get_by_role('tab',name='Campionato',exact=True).click()
            p.locator('#campo-link').click();p.locator('.pitch svg').wait_for();check('Campo dal Tabellone')
            assert p.locator('.club').count()==2
            assert p.locator('.dial').count()==2
            assert p.locator('.spark svg').count()==2
            p.locator('#matches button').last.click();check('Cambia partita')
            assert 'partita=4' in p.url
            g=p.locator('#roundtitle').inner_text()
            p.locator('#prev').click();assert p.locator('#roundtitle').inner_text()!=g
            p.get_by_role('button',name='Grafica '+('Stadio' if skin=='lega' else 'Lega'),exact=True).click()
            assert p.locator('body').get_attribute('data-skin')!=skin
            assert 'partita=0' in p.url and 'giornata=' in p.url
            p.get_by_role('button',name='Grafica '+skin.title(),exact=True).click()
            p.screenshot(path=str(OUT/f'integrato-campo-{skin}-{w}.png'),full_page=True)
            p.locator('#ritorno-tabellone').click();p.wait_for_url('**/tabellone-'+skin+'.html#lega-*');check('Ritorno Tabellone')
            p.locator('a.back').click();p.wait_for_url('**/home-'+skin+'.html')
            p.locator('a.c').filter(has_text="Albo d'oro").click();p.locator('.oro-scroll').wait_for();check('Albo dalla Home')
            btns=p.locator('.oro-scroll button');assert btns.count()>=8
            for i in range(btns.count()):
                btns.nth(i).click();p.wait_for_timeout(180)
                active=p.locator('.oro-scroll [aria-pressed=true]');assert active.count()==1
                assert active.evaluate('(e)=>e.offsetHeight>=44')
                assert p.locator('.oro-scroll').evaluate('(e)=>getComputedStyle(e).flexWrap')=='nowrap'
                assert active.evaluate('(e)=>{let a=e.getBoundingClientRect(),r=e.parentElement.getBoundingClientRect();return a.left>=r.left-2 && a.right<=r.right+2}'),(skin,w,'attivo fuori vista')
            check('Tab Albo')
            p.locator('a.oback').click();p.wait_for_url('**/home-'+skin+'.html');check('Ritorno Home')
            esiti.append({'skin':skin,'larghezza':w,'percorso':'Lab → Home → Tabellone → Coppa → Campo → Tabellone → Home → Albo → Home','esito':'PASS'})
            print('PASS percorso reale',skin,w,flush=True);c.close()
    b.close()
(OUT/'percorsi-53.json').write_text(json.dumps(esiti,ensure_ascii=False,indent=2))
