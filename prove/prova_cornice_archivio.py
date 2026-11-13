"""Versione leggibile, interruttore su più pagine e schede dell’Archivio."""
import json
import mimetypes
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from playwright.sync_api import sync_playwright, expect
from rete_browser import installa

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa_artifacts/cornice-archivio';OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:8798/o-girrr-registro/'
VERSION=json.loads((ROOT/'registro-stato.json').read_text())['versione']
VERSIONS=json.loads((ROOT/'rilascio/versioni/versioni.json').read_text())['versioni']
expect.set_options(timeout=25000)
report=[]
with sync_playwright() as p:
    screens=[('iPhone320',dict(p.devices['iPhone SE'],viewport={'width':320,'height':568}))]
    screens += [(n,dict(p.devices[n])) for n in ['iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape']]
    screens += [(f'PC{w}',{'viewport':{'width':w,'height':900}}) for w in (1280,1920,2560)]
    screens += [('TV',{'viewport':{'width':1920,'height':1080},'device_scale_factor':2,'user_agent':'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 Chrome/94.0 TV Safari/537.36'})]
    if os.environ.get('SCHERMI'):screens=[s for s in screens if s[0] in os.environ['SCHERMI'].split(',')]
    for engine in os.environ.get('MOTORI','chromium,webkit,firefox').split(','):
        opts={'executable_path':os.environ['WEBKIT_PATH']} if engine=='webkit' and os.environ.get('WEBKIT_PATH') else {}
        b=getattr(p,engine).launch(**opts)
        for screen,options in screens:
            options=dict(options);options.pop('default_browser_type',None)
            if engine=='firefox':options.pop('is_mobile',None)
            ctx=b.new_context(**options,service_workers='block',locale='it-IT');installa(ctx)
            def local(r):
                path=unquote(urlsplit(r.request.url).path).removeprefix('/o-girrr-registro/')
                f=(ROOT/path).resolve()
                if f.is_dir():f/='index.html'
                if not f.is_relative_to(ROOT) or not f.is_file():r.fulfill(status=404,body='Non trovato');return
                r.fulfill(status=200,content_type=mimetypes.guess_type(f.name)[0] or 'application/octet-stream',body=f.read_bytes())
            ctx.route(re.compile(r'^http://127\.0\.0\.1:8798/.*'),local)
            page=ctx.new_page();page.set_default_timeout(25000);errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('pageerror',lambda e:print('ERRORE_PAGINA',str(e),e.stack,page.evaluate('()=>document.getElementById("contenuto").contentDocument.getElementById("f")?.contentWindow.location.href'),flush=True))
            if screen=='iPhone320':
                ctx.add_init_script("if(!localStorage.getItem('qa404-seed')){localStorage.setItem('qa404-seed','1');localStorage.setItem('registro-anteprima-online',"+json.dumps(BASE+'anteprima/pubblicata/girrr/pagina-rimossa.html')+");}")
            page.goto(BASE+'registro.html#anteprima',wait_until='load')
            expect(page.locator('#versione')).to_have_text(VERSION)
            assert page.locator('#versione').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)>=28')
            expect(page.get_by_role('switch',name='Grafica Stadio')).to_be_visible()
            expect(page.locator('#grafica')).to_be_enabled()
            if screen=='iPhone320':
                expect(page.locator('#stato')).to_contain_text('riaperta sulla Home')
                assert page.evaluate("!localStorage.getItem('registro-anteprima-online').includes('pagina-rimossa')")
            positions=page.locator('.versione-box').bounding_box()
            filenames=['index.html','tabellone.html','albo.html','curva.html','app.html'] if screen in ('iPhone320','PC1920') else ['index.html']
            for filename in filenames:
                print('PAGINA',engine,screen,filename,flush=True)
                fragment='#carriera' if filename=='app.html' else ''
                expected=BASE+'anteprima/pubblicata/girrr/'+filename+'?prova=versione'+fragment
                page.evaluate('(url)=>document.getElementById("contenuto").contentDocument.getElementById("f").src=url',expected)
                def wait_current(stadio,search=None):
                    page.wait_for_function('''([file,stadio,hash,search])=>{
                        const o=document.getElementById('contenuto'),f=o.contentDocument.getElementById('f');
                        const w=f.contentWindow,d=f.contentDocument;
                        return d && d.readyState==='complete' && w.location.pathname.endsWith('/'+file) && w.location.pathname.includes('/stadio/')===stadio && new URL(w.location.href).searchParams.get('prova')==='versione' && (!search||w.location.search===search) && w.location.hash===hash && w.__registroSolaLettura===true;
                    }''',arg=[filename,stadio,fragment,search],timeout=30000)
                    # Aspetta le transizioni finite prima di passare alla pagina successiva.
                    page.evaluate('''async()=>{
                        const w=document.getElementById('contenuto').contentDocument.getElementById('f').contentWindow;
                        await new Promise(resolve=>w.requestAnimationFrame(()=>w.requestAnimationFrame(resolve)));
                        await Promise.allSettled(w.document.getAnimations().filter(a=>a.effect && a.effect.getComputedTiming().iterations!==Infinity).map(a=>a.finished));
                    }''')
                    expect(page.locator('#grafica')).to_have_attribute('aria-checked',str(stadio).lower())
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(engine,screen,filename)
                try:
                    wait_current(False)
                except Exception:
                    print('STATO',page.evaluate('''()=>{const o=document.getElementById('contenuto'),f=o.contentDocument.getElementById('f');return {url:f.contentWindow.location.href,ready:f.contentDocument.readyState,guard:f.contentWindow.__registroSolaLettura,toggle:document.getElementById('grafica').outerHTML}}'''),flush=True)
                    raise
                search=page.evaluate('()=>document.getElementById("contenuto").contentDocument.getElementById("f").contentWindow.location.search')
                for stadio in (True,False):
                    if filename=='index.html' and stadio:
                        page.frame_locator('#contenuto').frame_locator('#f').locator('#gsw [data-m="n"]').click()
                    else:
                        page.locator('#grafica').click()
                    wait_current(stadio,search)
                    expect(page.locator('#versione')).to_be_visible()
                assert page.locator('.versione-box').bounding_box()==positions
            assert page.evaluate("async()=>{const w=document.getElementById('contenuto').contentDocument.getElementById('f').contentWindow;return (await w.fetch('https://qmjqfgmvimsuxvghetgi.supabase.co/rest/v1/rpc/curva_scrivi',{method:'POST',body:'{}'})).status===403}")
            if screen in ('PC1920','TV','iPhone320'):page.screenshot(path=str(OUT/(engine+'-anteprima-'+screen+'.png')))
            page.evaluate("location.hash='archivio'")
            # Leggiamo il documento reale: Firefox può cambiare l’identità del
            # Frame nel protocollo dopo molte navigazioni dell’iframe interno.
            page.wait_for_function("count=>{const f=document.getElementById('contenuto'),d=f.contentDocument;return !f.hasAttribute('aria-busy')&&d?.readyState==='complete'&&d.documentElement.dataset.registroCollegato==='true'&&d.querySelectorAll('.release-card').length===count}",arg=len(VERSIONS))
            archive=page.evaluate('''()=>{const d=document.getElementById('contenuto').contentDocument;return {count:d.querySelectorAll('.release-card').length,open:d.querySelectorAll('.release-card details[open]').length,latest:d.querySelector('.release-latest').innerText,fits:d.documentElement.scrollWidth<=d.defaultView.innerWidth+1,prototypes:d.querySelectorAll('.archive-prototypes a').length}}''')
            assert archive['count']==len(VERSIONS) and archive['open']==1
            assert VERSION in archive['latest'] and archive['fits'] and archive['prototypes']==4
            if screen in ('PC1920','TV','iPhone320'):page.screenshot(path=str(OUT/(engine+'-archivio-'+screen+'.png')))
            page.evaluate("()=>document.getElementById('contenuto').contentDocument.querySelectorAll('.release-card summary')[1].scrollIntoView({block:'center',behavior:'instant'})")
            page.evaluate('''async()=>{const w=document.getElementById('contenuto').contentWindow;await new Promise(resolve=>w.requestAnimationFrame(()=>w.requestAnimationFrame(resolve)))}''')
            point=page.evaluate('''()=>{const f=document.getElementById('contenuto'),d=f.contentDocument,s=d.querySelectorAll('.release-card summary')[1],p=s.getBoundingClientRect(),r=f.getBoundingClientRect();return {x:r.left+p.left+p.width/2,y:r.top+p.top+p.height/2}}''')
            page.mouse.click(point['x'],point['y'])
            page.wait_for_function("()=>document.getElementById('contenuto').contentDocument.querySelectorAll('.release-card details')[1].open")
            page.evaluate("()=>document.getElementById('contenuto').contentDocument.querySelectorAll('.release-card summary')[1].focus()")
            page.keyboard.press('Enter')
            page.wait_for_function("()=>!document.getElementById('contenuto').contentDocument.querySelectorAll('.release-card details')[1].open")
            page.evaluate("()=>{const d=document.getElementById('contenuto').contentDocument;d.activeElement?.blur();d.defaultView.scrollTo(0,0)}")
            page.wait_for_function("()=>document.getElementById('contenuto').contentDocument.scrollingElement.scrollTop===0")
            assert not errors,(engine,screen,errors)
            report.append({'motore':engine,'schermo':screen,'esito':'PASS','pagine_con_toggle':len(filenames)})
            print('PASS',engine,screen,flush=True);ctx.close()
        b.close()
(OUT/('esiti-'+os.environ.get('MOTORI','tutti')+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
