"""Filtri combinati, date di Roma e panoramica completa nel portale del Registro."""
import json
import mimetypes
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from playwright.sync_api import sync_playwright, expect
from rete_browser import installa

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa_artifacts/filtri-panorama'; OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:8797/o-girrr-registro/'
SNAP=json.loads((ROOT/'ramificazioni-dati.json').read_text())
FIX=[['2026-11-12T22:30:00Z','Curva: Regolamento serale'],['2026-11-12T23:30:00Z','Curva: Sondaggio di mezzanotte'],['2026-11-13T09:00:00Z','Home: Apertura del mattino'],['2026-07-12T22:30:00Z','Curva: Notizia estiva'],['2026-11-13T08:00:00Z','Tabellone: Risultati della giornata']]
expect.set_options(timeout=15000)
results=[]
with sync_playwright() as p:
    screens=[('iPhone320',dict(p.devices['iPhone SE'],viewport={'width':320,'height':568}))]
    screens += [(n,dict(p.devices[n])) for n in ['iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape']]
    screens += [(f'PC{w}',{'viewport':{'width':w,'height':900}}) for w in (1280,1920,2560)]
    screens += [('TV',{'viewport':{'width':1920,'height':1080},'device_scale_factor':2,'user_agent':'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 Chrome/94.0 TV Safari/537.36'})]
    if os.environ.get('SCHERMI'): screens=[s for s in screens if s[0] in os.environ['SCHERMI'].split(',')]
    for engine in os.environ.get('MOTORI','chromium,webkit,firefox').split(','):
        opts={'executable_path':os.environ['WEBKIT_PATH']} if engine=='webkit' and os.environ.get('WEBKIT_PATH') else {}
        b=getattr(p,engine).launch(**opts)
        for screen,config in screens:
            config=dict(config);config.pop('default_browser_type',None)
            if engine=='firefox': config.pop('is_mobile',None)
            c=b.new_context(**config,service_workers='block',locale='it-IT');installa(c)
            c.route('https://api.github.com/repos/giandjcosta/o-fant-a-girrr/commits?*',lambda r:r.fulfill(status=200,content_type='application/json',headers={'Access-Control-Allow-Origin':'*'},body='[]'))
            c.route('https://raw.githubusercontent.com/giandjcosta/o-girrr-registro/chatgpt/dati-ramificazioni/**',lambda r:r.fulfill(status=200,content_type='application/json',headers={'Access-Control-Allow-Origin':'*'},body=json.dumps(SNAP)))
            def local(r):
                path=unquote(urlsplit(r.request.url).path).removeprefix('/o-girrr-registro/')
                f=(ROOT/path).resolve()
                if f.is_dir():f/='index.html'
                if not f.is_relative_to(ROOT) or not f.is_file():r.fulfill(status=404,body='Non trovato');return
                r.fulfill(status=200,content_type=mimetypes.guess_type(f.name)[0] or 'application/octet-stream',body=f.read_bytes())
            c.route(re.compile(r'^http://127\.0\.0\.1:8797/.*'),local)
            page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(BASE+'registro.html#changelog',wait_until='load')
            content=page.frame_locator('#contenuto')
            expect(content.locator('#area-filter option')).not_to_have_count(1)
            expect(content.locator('.fs,.f')).to_have_count(0)
            assert content.locator('.r').count()>100
            if screen in ('PC1920','TV'):
                page.screenshot(path=str(OUT/(engine+'-changelog-'+screen+'.png')))
            def fits():
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(engine,screen,'portale')
                assert content.locator('html').evaluate('(e)=>e.scrollWidth<=innerWidth+1'),(engine,screen,'contenuto')
            fits()
            content.locator('html').evaluate('(_,data)=>prep(data)',FIX+[FIX[0],['2026-11-13T10:00:00Z','Aggiorna dati automatici']])
            expect(content.locator('.r')).to_have_count(5)
            content.locator('#area-filter').select_option('Curva');expect(content.locator('.r')).to_have_count(3)
            content.locator('#date-filter').fill('2026-11-13');expect(content.locator('.r')).to_have_count(1)
            expect(content.locator('.r')).to_contain_text('Sondaggio di mezzanotte')
            content.locator('#q').fill('sondaggio');expect(content.locator('.r')).to_have_count(1)
            content.locator('html').evaluate('(_,data)=>prep(data)',FIX+[['2026-11-13T15:00:00Z','Curva: Altro sondaggio']])
            expect(content.locator('#area-filter')).to_have_value('Curva');expect(content.locator('#date-filter')).to_have_value('2026-11-13');expect(content.locator('.r')).to_have_count(2)
            content.locator('#q').fill('Non esiste');expect(content.locator('.r')).to_have_count(0)
            expect(content.locator('#l')).to_contain_text('Nessuna modifica')
            content.locator('#reset').click();expect(content.locator('.r')).to_have_count(6);expect(content.locator('#reset')).to_be_disabled()
            content.locator('#date-filter').fill('2026-07-13');expect(content.locator('.r')).to_have_count(1)
            expect(content.locator('.r')).to_contain_text('Notizia estiva')
            fits()
            page.evaluate("location.hash='ramificazioni'")
            expect(content.locator('[data-overview]')).to_have_count(2)
            for repo in SNAP['repositories']:
                host=content.locator('[data-repository="'+repo['id']+'"]');overview=host.locator('[data-overview]')
                expect(overview.locator('[data-overview-branch]')).to_have_count(len(repo['branches']))
                assert overview.locator('svg').first.evaluate('(e)=>e.getBoundingClientRect().right<=innerWidth+1')
                independent=[v for v in repo['branches'] if v['name']!='main' and not v['base']]
                for v in independent:expect(overview.locator('[data-overview-branch="'+v['name']+'"] .overview-link')).to_have_count(0)
                pick=next(v for v in repo['branches'] if v['name']!='main' and not v['name'].startswith('claude/o-girrr-versione-6-0-'))
                overview.locator('[data-overview-select]').select_option(pick['name'])
                expect(overview.locator('[data-detail]')).to_be_visible();expect(overview.locator('[data-detail]')).to_contain_text(pick['name'])
                expect(host.locator('[data-drawer][open]')).to_have_count(0)
                overview.locator('[data-close]').click();expect(overview.locator('[data-detail]')).to_be_hidden()
                main=overview.locator('[data-overview-branch="main"] .overview-tip');main.click()
                expect(overview.locator('[data-detail]')).to_be_visible();overview.locator('[data-close]').click()
                host.locator('[data-select=main]').click();expect(host.locator('[data-map-branch]')).to_have_count(1)
                expect(overview.locator('[data-overview-branch]')).to_have_count(len(repo['branches']))
                host.locator('[data-select=active]').click()
                expect(host.locator('[data-detail]')).to_have_count(1)
                fits()
            if screen in ('PC1920','TV','iPhone320'):
                content.locator('[data-overview]').first.scroll_into_view_if_needed()
                page.screenshot(path=str(OUT/(engine+'-panorama-'+screen+'.png')))
            assert not errors,(engine,screen,errors)
            results.append({'motore':engine,'versione':b.version,'schermo':screen,'esito':'PASS'})
            print('PASS',engine,screen,flush=True);c.close()
        b.close()
(OUT/('esiti-'+os.environ.get('MOTORI','tutti')+'.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
