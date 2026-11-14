"""Portale completo: vecchi indirizzi, menu persistente, grafica e sola lettura.

Tre motori reali, 16 profili ciascuno; nessuna chiamata al database reale.
"""
import json
from contextlib import nullcontext
import mimetypes
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from playwright.sync_api import sync_playwright, expect
from rete_browser import installa

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'qa_artifacts/portale-registro'
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'http://127.0.0.1:8793/o-girrr-registro/'
expect.set_options(timeout=35000)
report = []
with sync_playwright() as p:
    screens = [('iPhone320', dict(p.devices['iPhone SE'], viewport={'width':320,'height':568}))]
    screens += [(n, dict(p.devices[n])) for n in ('iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape')]
    screens += [(f'PC{w}', {'viewport':{'width':w,'height':900}}) for w in (1280,1920,2560)]
    screens += [('TV', {'viewport':{'width':1920,'height':1080},'device_scale_factor':2,'user_agent':'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 Chrome/94.0 TV Safari/537.36'})]
    if os.environ.get('SCHERMI'): screens = [s for s in screens if s[0] in os.environ['SCHERMI'].split(',')]
    for engine in os.environ.get('MOTORI','chromium,webkit,firefox').split(','):
        options = {'executable_path':os.environ['WEBKIT_PATH']} if engine=='webkit' and os.environ.get('WEBKIT_PATH') else {}
        b = getattr(p,engine).launch(**options)
        for name, config in screens:
            config = dict(config)
            config.pop('default_browser_type',None)
            if engine=='firefox': config.pop('is_mobile',None)
            ctx = b.new_context(**config, service_workers='block')
            installa(ctx)
            ctx.route('https://raw.githubusercontent.com/giandjcosta/o-girrr-registro/chatgpt/dati-ramificazioni/**', lambda r:r.fulfill(status=200,content_type='application/json',headers={'Access-Control-Allow-Origin':'*'},body=(ROOT/'ramificazioni-dati.json').read_bytes()))
            def local(r):
                rel = unquote(urlsplit(r.request.url).path).removeprefix('/o-girrr-registro/')
                target = (ROOT/rel).resolve()
                if target.is_dir(): target /= 'index.html'
                if not target.is_relative_to(ROOT) or not target.is_file(): r.fulfill(status=404,body='Non trovato'); return
                r.fulfill(status=200,content_type=mimetypes.guess_type(target.name)[0] or 'application/octet-stream',body=target.read_bytes())
            ctx.route(re.compile(r'^http://127\.0\.0\.1:8793/.*'),local)
            page = ctx.new_page()
            page.set_default_timeout(20000)
            errors = []
            standalone_previews = []
            page.on('request',lambda r:standalone_previews.append(r.url) if r.is_navigation_request() and r.url.startswith(BASE+'anteprima/pubblicata/') and r.frame.parent_frame==page.main_frame else None)
            def published(f,path=''):
                return f.url.startswith(BASE+'anteprima/pubblicata/'+path) and f.parent_frame is not None and f.parent_frame.parent_frame==page.main_frame
            page.on('pageerror',lambda e:errors.append(str(e)))
            print('PROFILO',engine,name,flush=True)
            page.goto(BASE,wait_until='load')
            expect(page).to_have_url(BASE+'registro.html#changelog')
            shell = page.locator('#contenuto')
            def ready():
                expect(shell).not_to_have_attribute('aria-busy','true')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                # Dopo history.back Firefox può conservare il documento ma sostituire
                # l'identità del Frame nel protocollo di automazione. Controlliamo
                # il documento effettivamente mostrato, anche la sua destinazione.
                page.wait_for_function('''() => {
                    const f=document.getElementById('contenuto'),d=f.contentDocument;
                    return d && d.readyState==='complete' && d.documentElement.dataset.registroCollegato==='true' && d.location.href===f.dataset.src;
                }''',timeout=35000)
                assert page.evaluate('''() => {
                    const f=document.getElementById('contenuto');
                    return f.contentDocument.documentElement.scrollWidth<=f.contentWindow.innerWidth+1;
                }'''),(engine,name,page.url)
            ready()
            for key in os.environ.get('SEZIONI','lab,aggiornamenti,archivio,ramificazioni,anteprima').split(','):
                print('SEZIONE',engine,name,key,flush=True)
                navigation=page.expect_event('framenavigated',predicate=published,timeout=35000) if key=='anteprima' else nullcontext()
                with navigation as loaded:
                    if page.locator('#sezione').is_visible(): page.locator('#sezione').select_option(key)
                    else: page.locator('#menu a[href="#'+key+'"]').click()
                expect(shell).to_have_attribute('data-src',re.compile(re.escape({'lab':'lab/','aggiornamenti':'aggiornamenti.html','archivio':'archivio.html','ramificazioni':'ramificazioni.html','anteprima':'ufficiale/'}[key])+r'\?nel-registro=1$'))
                ready()
                expect(page.locator('#menu a[aria-current]')).to_have_attribute('href','#'+key)
                if key=='ramificazioni':
                    content = page.frame_locator('#contenuto')
                    expect(content.locator('.repo')).to_have_count(2)
                    content.locator('#select-all').click()
                    assert content.locator('[data-map-branch]:visible').count()>20
                    ready()
                    if name in ('PC1920','TV'):
                        page.screenshot(path=str(OUT/(engine+'-'+name+'.png')))
                if key=='anteprima':
                    page.wait_for_function('''()=>{
                        const outer=document.getElementById('contenuto'),f=outer.contentDocument?.getElementById('f');
                        return f?.contentDocument?.readyState==='complete' && f.contentDocument.querySelector('h1') && f.contentWindow.__registroSolaLettura===true;
                    }''',timeout=35000)
                    inner=loaded.value
                    inner.wait_for_load_state('domcontentloaded')
                    inner.locator('h1').first.wait_for()
                    # Attende anche le letture asincrone della pagina prima di cambiarla.
                    inner.wait_for_load_state('networkidle')
                    for stadio in (False,True):
                        if stadio:
                            page.locator('#grafica').click()
                        expect(page.locator('#grafica')).to_have_attribute('aria-checked',str(stadio).lower())
                        page.wait_for_function('''stadio => {
                            const outer=document.getElementById('contenuto'),f=outer.contentDocument.getElementById('f');
                            const h=f?.contentDocument?.querySelector('h1');
                            return h && h.getClientRects().length>0 && f.contentDocument.readyState==='complete' && f.contentWindow.location.pathname.includes('/stadio/')===stadio && f.contentWindow.__registroSolaLettura===true;
                        }''',arg=stadio,timeout=35000)
                        # Firefox può sostituire il frame: si controlla quello effettivamente visibile.
                        assert page.evaluate("()=>document.getElementById('contenuto').contentDocument.getElementById('f').contentWindow.__registroSolaLettura===true")
                        assert page.evaluate("async()=>{const w=document.getElementById('contenuto').contentDocument.getElementById('f').contentWindow;const r=await w.fetch('https://qmjqfgmvimsuxvghetgi.supabase.co/rest/v1/rpc/curva_scrivi',{method:'POST',body:'{}'});return r.status===403}")
                        page.wait_for_load_state('networkidle')
            if name in ('iPhone320','PC1920'):
                # Regressione Firefox: rientri ripetuti senza riferimenti al frame precedente.
                page.wait_for_load_state('networkidle')
                for _ in range(3):
                    page.evaluate("location.hash='archivio'")
                    expect(shell).to_have_attribute('data-src',BASE+'archivio.html?nel-registro=1')
                    ready()
                    with page.expect_event('framenavigated',predicate=published,timeout=35000) as returned:
                        page.evaluate("location.hash='anteprima'")
                    expect(shell).to_have_attribute('data-src',BASE+'ufficiale/?nel-registro=1')
                    ready()
                    returned.value.locator('h1').first.wait_for()
                    returned.value.wait_for_load_state('networkidle')
            page.wait_for_load_state('networkidle')
            # Il vecchio segnalibro Anteprima torna nello stesso portale.
            with page.expect_event('framenavigated',predicate=published,timeout=35000) as bookmark:
                page.goto(BASE+'ufficiale/',wait_until='load')
            expect(page).to_have_url(BASE+'registro.html#anteprima')
            ready()
            bookmark.value.locator('h1').first.wait_for()
            bookmark.value.wait_for_load_state('networkidle')
            page.evaluate("location.hash='ramificazioni'")
            expect(shell).to_have_attribute('data-src',BASE+'ramificazioni.html?nel-registro=1')
            ready()
            page.evaluate('history.back()')
            expect(page).to_have_url(BASE+'registro.html#anteprima')
            ready()
            page.wait_for_load_state('networkidle')
            assert not standalone_previews,(engine,name,'Caricamento prima del rinvio al portale',standalone_previews)
            assert not errors,(engine,name,errors)
            report.append({'motore':engine,'versione':b.version,'schermo':name,'esito':'PASS'})
            print('PASS',engine,name,flush=True)
            ctx.close()
        b.close()
(OUT/('esiti-'+os.environ.get('MOTORI','tutti')+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
