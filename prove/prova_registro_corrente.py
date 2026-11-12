"""Versione corrente, archivio, navigazione Lega/Stadio e blocco scritture.
Serve i file locali con Playwright, senza richiedere un server HTTP.
"""
import json
import mimetypes
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from playwright.sync_api import sync_playwright
from rete_browser import installa, browser

R = Path(__file__).resolve().parents[1]
OUT = R / 'qa_artifacts/registro-corrente'
OUT.mkdir(parents=True, exist_ok=True)
V = json.loads((R / 'registro-stato.json').read_text())['versione']
BASE = 'http://127.0.0.1:8765'
report = []

with sync_playwright() as pw:
    for motore in os.environ.get('MOTORI', 'chromium').split(','):
        b = browser(pw) if motore == 'chromium' and not os.environ.get('PLAYWRIGHT_BROWSERS_PATH') else getattr(pw, motore).launch(headless=True)
        screens = [(n, pw.devices[n]) for n in ('iPhone SE', 'iPhone 15 Pro', 'iPhone 15 Pro Max', 'Galaxy S8', 'Pixel 7', 'Galaxy S9+', 'iPad Mini', 'iPad (gen 7) landscape', 'iPad Pro 11', 'Galaxy Tab S4', 'Galaxy Tab S4 landscape')]
        screens = [('iPhone 320', dict(pw.devices['iPhone SE'], viewport={'width':320,'height':568}))] + screens
        screens += [(f'PC {w}', {'viewport':{'width':w,'height':900}}) for w in (1280,1920,2560)]
        screens += [('TV', {'viewport':{'width':1920,'height':1080},'device_scale_factor':2,'user_agent':'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 Chrome/94.0 TV Safari/537.36'})]
        for name, options in screens:
            if motore == 'firefox': options = {k:v for k,v in options.items() if k != 'is_mobile'}
            ctx = b.new_context(**options, service_workers='block')
            installa(ctx)  # Le letture Supabase sono simulate, nessun database contattato.
            def local(route):
                path = unquote(urlsplit(route.request.url).path)
                path = path.removeprefix('/o-girrr-registro/') if path.startswith('/o-girrr-registro/') else path.lstrip('/')
                target = (R / path).resolve()
                if target.is_dir(): target /= 'index.html'
                if not target.is_relative_to(R) or not target.is_file():
                    route.fulfill(status=404, body='File non trovato: '+path); return
                route.fulfill(status=200, content_type=mimetypes.guess_type(target.name)[0] or 'application/octet-stream', body=target.read_bytes())
            ctx.route(re.compile(r'http://127\.0\.0\.1:8765/.*'), local)
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            for path in ('/', '/archivio.html', '/lab/changelog.html', '/ufficiale/'):
                page.goto(BASE + path, wait_until='networkidle', timeout=45000)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (name,path,'overflow')
                if path == '/archivio.html': assert V in page.locator('main').inner_text()
                if path == '/lab/changelog.html': page.locator('.vv-v').first.wait_for(timeout=10000)
                if path == '/ufficiale/':
                    f = page.frame_locator('#f')
                    f.locator('h1').first.wait_for()
                    assert V in page.title()
                    for stadio in (False, True):
                        if stadio: page.locator('#tg').click()
                        page.wait_for_function('(s)=>document.getElementById("f").contentWindow.location.pathname.includes("/stadio/")===s',arg=stadio)
                        f.locator('h1').first.wait_for()
                        assert f.locator('html').evaluate('(e)=>e.scrollWidth<=innerWidth+1'), (name,'frame overflow',stadio)
                        assert f.locator('html').evaluate('()=>window.__registroSolaLettura===true')
                        assert f.locator('html').evaluate("async()=>{let r=await fetch('https://qmjqfgmvimsuxvghetgi.supabase.co/rest/v1/rpc/curva_scrivi',{method:'POST',body:'{}'});return r.status===403}")
                    if name in ('PC 1920','TV'):
                        page.screenshot(path=str(OUT / (motore+'-'+name.replace(' ','-')+'.png')))
            assert not errors, (name,errors)
            report.append({'motore':motore,'schermo':name,'esito':'PASS'})
            print('PASS',motore,name,flush=True)
            ctx.close()
        b.close()
(OUT/('esiti-'+os.environ.get('MOTORI','chromium').replace(',','-')+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2))
