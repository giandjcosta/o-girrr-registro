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
            p.goto(ROOT+'/lab/index.html?nel-registro',wait_until='networkidle')
            p.get_by_role('link',name='Anteprima 5.5 · '+skin.title(),exact=True).click()
            p.wait_for_url('**/5.5/index-'+skin+'.html');p.locator('.v55-summary').wait_for();check('Home dal Lab')
            # I vecchi segnalibri arrivano alla Home corrente senza perdere la query.
            p.goto(ROOT+'/anteprima/home-'+skin+'.html?da=segnalibro',wait_until='networkidle')
            p.wait_for_url('**/5.5/index-'+skin+'.html?da=segnalibro');p.locator('.v55-summary').wait_for()
            # Anche il vecchio ingresso dell’app deve arrivare alla stessa Home aggiornata.
            app='attuale.html' if skin=='lega' else 'index.html'
            p.goto(ROOT+'/anteprima/'+app,wait_until='networkidle');p.wait_for_url('**/5.5/index-'+skin+'.html');p.locator('.v55-summary').wait_for()
            p.locator('a.c').filter(has_text='Tabellone').click()
            p.wait_for_url('**/tabellone-'+skin+'.html');p.locator('#tab .numpos').first.wait_for();check('Tabellone')
            assert p.locator('#tab tbody tr').count()==10
            assert p.locator('#tab .zona-1 .numpos').evaluate('(e)=>getComputedStyle(e).color')=='rgb(255, 209, 102)'
            assert p.locator('#tab .zona-last .numpos').evaluate('(e)=>getComputedStyle(e).color')=='rgb(255, 114, 134)'
            for selector in ('.dr','.pt'):
                assert p.locator('#tab tbody '+selector).first.evaluate('(e)=>getComputedStyle(e).color')=='rgb(251, 246, 236)'
            # Fantapunti azzurri, come nella grafica originale richiesta da Gianluca.
            assert p.locator('#tab tbody .fp').first.evaluate('(e)=>getComputedStyle(e).color')=='rgb(191, 227, 255)'
            th=p.locator('#tab th.w').first
            assert th.is_visible()==(w>=560)
            p.screenshot(path=str(OUT/f'integrato-tabellone-{skin}-{w}.png'),full_page=True)
            # Dalla 5.5 il Campo è disponibile anche in Champions Cup.
            p.get_by_role('tab',name='Champions Cup',exact=True).click();check('Champions Cup')
            assert p.locator('#campo-link').is_visible()
            assert 'coppa=1' in p.locator('#campo-link').get_attribute('href')
            p.get_by_role('tab',name='Campionato',exact=True).click()
            p.locator('#campo-link').click();p.locator('.pitch svg').wait_for();check('Campo dal Tabellone')
            assert p.locator('.club').count()==2
            assert p.locator('.dial').count()==2
            assert p.locator('.spark svg').count()==2
            p.locator('#matches button').last.click();check('Cambia partita')
            assert 'partita=4' in p.url
            g=p.locator('#roundtitle').inner_text()
            p.locator('#prev').click();assert p.locator('#roundtitle').inner_text()!=g
            # In 5.5 il selettore locale del Campo è nascosto: il cambio sta nella cornice.
            p.evaluate('''([url,skin])=>{localStorage.setItem('orr_gu',url);localStorage.setItem('orr_gv',skin==='stadio'?'n':'a')}''',arg=[p.url,skin])
            p.goto(ROOT+'/anteprima/storica55.html',wait_until='networkidle')
            campo=p.frame_locator('#f')
            campo.locator('.pitch svg').wait_for()
            p.locator('#tg').click()
            p.wait_for_function("skin=>document.getElementById('f').contentDocument?.body?.dataset.skin!==skin && document.getElementById('f').contentDocument?.querySelector('.pitch svg')",arg=skin)
            assert campo.locator('body').get_attribute('data-skin')!=skin
            current=p.evaluate("()=>document.getElementById('f').contentWindow.location.href")
            assert 'partita=0' in current and 'giornata=' in current
            p.locator('#tg').click()
            p.wait_for_function("skin=>document.getElementById('f').contentDocument?.body?.dataset.skin===skin && document.getElementById('f').contentDocument?.querySelector('.pitch svg')",arg=skin)
            current=p.evaluate("()=>document.getElementById('f').contentWindow.location.href")
            p.goto(current,wait_until='networkidle');p.locator('.pitch svg').wait_for()
            assert p.locator('body').get_attribute('data-skin')==skin
            p.screenshot(path=str(OUT/f'integrato-campo-{skin}-{w}.png'),full_page=True)
            p.get_by_role('link',name='Torna a Tabellone',exact=True).click();p.wait_for_url('**/tabellone-'+skin+'.html#lega-*');check('Ritorno Tabellone')
            p.get_by_role('link',name='Home O Girrr',exact=True).filter(visible=True).click();p.wait_for_url('**/5.5/index-'+skin+'.html')
            p.locator('a.c').filter(has_text="Albo d'oro").click();p.locator('.oro-scroll').wait_for();check('Albo dalla Home')
            btns=p.locator('.oro-scroll button');assert btns.count()>=8
            for i in range(btns.count()):
                btns.nth(i).click();p.wait_for_timeout(180)
                active=p.locator('.oro-scroll [aria-pressed=true]');assert active.count()==1
                h=active.evaluate('(e)=>e.offsetHeight')
                assert h>=(44 if w<=768 else 28),(skin,w,'Area della scheda',h)
                assert p.locator('.oro-scroll').evaluate('(e)=>getComputedStyle(e).flexWrap')=='nowrap'
                assert active.evaluate('(e)=>{let a=e.getBoundingClientRect(),r=e.parentElement.getBoundingClientRect();return a.left>=r.left-2 && a.right<=r.right+2}'),(skin,w,'attivo fuori vista')
            check('Tab Albo')
            p.get_by_role('link',name='Home O Girrr',exact=True).filter(visible=True).click();p.wait_for_url('**/5.5/index-'+skin+'.html');check('Ritorno Home')
            esiti.append({'skin':skin,'larghezza':w,'percorso':'Lab → Home → Tabellone → Coppa → Campo → Tabellone → Home → Albo → Home','esito':'PASS'})
            print('PASS percorso reale',skin,w,flush=True);c.close()
    b.close()
(OUT/'percorsi-53.json').write_text(json.dumps(esiti,ensure_ascii=False,indent=2))
