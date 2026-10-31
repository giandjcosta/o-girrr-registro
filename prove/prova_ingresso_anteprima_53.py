#!/usr/bin/env python3
"""Ingresso abituale del Registro e cambio skin dentro la cornice dell'Anteprima."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from rete_browser import installa,browser
ROOT='http://127.0.0.1:8765'
OUT=Path('qa_artifacts');OUT.mkdir(exist_ok=True)
report=[]
with sync_playwright() as pw:
    b=browser(pw)
    for width in (320,390,768,1280,1440):
        ctx=b.new_context(viewport={'width':width,'height':950});installa(ctx)
        page=ctx.new_page();errors=[];http=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.on('response',lambda r:http.append([r.status,r.url]) if r.status>=400 else None)
        # L'URL salvata dalla vecchia Anteprima deve essere migrata al Tabellone nuovo.
        page.add_init_script("""if(!sessionStorage.getItem('ingresso-test')){
          localStorage.setItem('orr_gv','a');localStorage.setItem('orr_gu',location.origin+'/ufficiale/girrr/index.html');
          sessionStorage.setItem('ingresso-test','1')}
        """)
        page.goto(ROOT+'/aggiornamenti.html',wait_until='networkidle')
        page.get_by_role('link',name='Anteprima 5.3',exact=True).click()
        page.wait_for_url('**/ufficiale/')
        def frame():return page.frame_locator('#f')
        def check(label):
            page.wait_for_timeout(600)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,label,'overflow cornice')
            assert frame().locator('html').evaluate('(e)=>e.scrollWidth<=window.innerWidth+1'),(width,label,'overflow pagina')
            assert not errors,(width,label,errors)
            assert not http,(width,label,http)
        def skin(m):
            expected='true' if m=='stadio' else 'false'
            if page.locator('#tg').get_attribute('aria-checked')!=expected:page.locator('#tg').click()
            page.wait_for_function('(v)=>document.getElementById("tg").getAttribute("aria-checked")===v',arg=expected)
        frame().locator('a.c').filter(has_text='Tabellone').click()
        frame().locator('#tab .numpos').first.wait_for()
        for grafica in ('lega','stadio'):
            skin(grafica)
            page.wait_for_function('(s)=>document.getElementById("f").contentWindow.location.pathname.endsWith("tabellone-"+s+".html")',arg=grafica)
            frame().locator('#tab .numpos').first.wait_for();check('Tabellone '+grafica)
            assert frame().locator('#tab tbody tr').count()==10
            page.screenshot(path=str(OUT/f'ingresso-tabellone-{grafica}-{width}.png'))
        frame().locator('#campo-link').click();frame().locator('.pitch svg').wait_for();check('Campo')
        frame().locator('#matches button').last.click();frame().locator('#prev').click()
        for grafica in ('lega','stadio'):
            skin(grafica)
            frame().locator('.pitch svg').wait_for()
            page.wait_for_function('(s)=>document.getElementById("f").contentWindow.document.body.dataset.skin===s',arg=grafica)
            assert frame().locator('#roundtitle').inner_text()=='Giornata 4'
            check('Campo '+grafica)
            page.screenshot(path=str(OUT/f'ingresso-campo-{grafica}-{width}.png'))
        frame().locator('#ritorno-tabellone').click();frame().locator('#tab .numpos').first.wait_for()
        frame().locator('a.back').click();frame().locator('a.c').filter(has_text="Albo d'oro").click()
        frame().locator('[data-oro=annuario]').click()
        for grafica in ('lega','stadio'):
            skin(grafica);frame().locator('.oro-scroll').wait_for();check('Albo '+grafica)
            assert frame().locator('.oro-scroll').evaluate('(e)=>getComputedStyle(e).flexWrap')=='nowrap'
        frame().locator('a.oback').click();frame().locator('a.c').filter(has_text='Tabellone').wait_for()
        # Riapertura della cornice: conserva la Home e la grafica correnti.
        page.reload(wait_until='networkidle');frame().locator('a.c').filter(has_text='Tabellone').wait_for();check('Riapertura')
        report.append({'larghezza':width,'esito':'PASS','ingresso':'Registro → Anteprima 5.3 → Home → Tabellone → Campo → Albo → Home','grafiche':['lega','stadio'],'memoria_vecchio_ingresso':'migrata'})
        print('PASS ingresso Anteprima dal Registro e cambio grafica',width,flush=True);ctx.close()
    b.close()
(OUT/'ingresso-anteprima-53.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
