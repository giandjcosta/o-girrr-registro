"""Ramificazioni: tutti i rami, selezione collettiva e leggibilità senza scorrimento laterale."""
import copy
import json
import mimetypes
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote,urlsplit
from playwright.sync_api import sync_playwright,expect
from rete_browser import installa

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('RAMI_QA_OUT',str(ROOT/'qa_artifacts/ramificazioni-leggibili')));OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:8792/o-girrr-registro/'
SNAP=json.loads(Path(os.environ.get('RAMI_DATI',str(ROOT/'ramificazioni-dati.json'))).read_text())


def routes(c):
    installa(c)
    state={'data':copy.deepcopy(SNAP),'fail':False}
    def remote(r):r.fulfill(status=503 if state['fail'] else 200,content_type='application/json',headers={'Access-Control-Allow-Origin':'*'},body=json.dumps(state['data']))
    c.route('https://raw.githubusercontent.com/giandjcosta/o-girrr-registro/chatgpt/dati-ramificazioni/**',remote)
    def local(r):
        path=unquote(urlsplit(r.request.url).path).removeprefix('/o-girrr-registro/')
        f=(ROOT/path).resolve()
        if not f.is_relative_to(ROOT) or not f.is_file():r.fulfill(status=404,body='Non trovato');return
        data=json.dumps(SNAP).encode() if path=='ramificazioni-dati.json' else f.read_bytes()
        r.fulfill(status=200,content_type=mimetypes.guess_type(f.name)[0] or 'application/octet-stream',body=data)
    c.route(re.compile(r'^http://127\.0\.0\.1:8792/.*'),local)
    return state


def fits(page):
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'La pagina richiede scorrimento laterale'
    for graph in page.locator('[data-graph]:visible').all():
        assert graph.evaluate('(e)=>e.scrollWidth<=e.clientWidth+1'),'La mappa richiede scorrimento laterale'
        assert graph.evaluate('(e)=>getComputedStyle(e).overflowY!=="auto"'),'La mappa è chiusa in un riquadro da scorrere'


def main():
    result={'motori':{},'profili':16,'visite':0,'problemi':[],'interazioni':[],'browserFisici':'Samsung Internet e Safari su dispositivo non disponibili; schermi e identità emulati.'}
    with sync_playwright() as p:
        screens=[('iPhone320',dict(p.devices['iPhone SE'],viewport={'width':320,'height':568}))]+[(n,p.devices[n]) for n in ['iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape']]+[(f'PC{w}',{'viewport':{'width':w,'height':900}}) for w in [1280,1920,2560]]+[('TV',{'viewport':{'width':1920,'height':1080},'device_scale_factor':2,'user_agent':'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36'})]
        if os.environ.get('SCHERMI'):screens=[s for s in screens if s[0] in os.environ['SCHERMI'].split(',')]
        result['profili']=len(screens)
        for engine in os.environ.get('MOTORI','chromium,webkit,firefox').split(','):
            opts={'executable_path':os.environ['WEBKIT_PATH']} if engine=='webkit' and os.environ.get('WEBKIT_PATH') else {}
            b=getattr(p,engine).launch(**opts);result['motori'][engine]=b.version
            for screen,options in screens:
                options=dict(options);options.pop('default_browser_type',None)
                if engine=='firefox':options.pop('is_mobile',None)
                c=b.new_context(**options,service_workers='block');state=routes(c);page=c.new_page();page.set_default_timeout(12000);errors=[];bad=[]
                page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append(str(r.status)+' '+r.url) if r.status>=400 else None)
                try:
                    page.goto(BASE+'ramificazioni.html?nel-registro=1',wait_until='load');expect(page.locator('.repo')).to_have_count(2);page.evaluate('document.fonts.ready')
                    total=sum(len(r['branches']) for r in SNAP['repositories']);expect(page.locator('[data-map-branch]')).to_have_count(total);fits(page)
                    colors=page.locator('[data-map-branch]').evaluate_all('(es)=>es.map(e=>e.style.getPropertyValue("--branch"))');assert len(set(colors))==total,'Colori duplicati'
                    assert page.evaluate('document.documentElement.scrollHeight')<20000,'Vista iniziale troppo lunga'
                    if engine=='chromium' and screen in ['PC1920','TV']:
                        page.locator('.repo').first.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'ramificazioni-{screen}.png'))
                        page.locator('.repo').last.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'ramificazioni-registro-{screen}.png'))
                    for r in SNAP['repositories']:
                        repo=page.locator('[data-repository='+r['id']+']');count=len(r['branches'])
                        expect(repo.locator('[data-add]:checked')).to_have_count(count)
                        expect(repo.locator('[data-drawer][open]')).to_have_count(0)
                        expect(repo.locator('.map-release')).to_be_visible()
                        visible_default=repo.locator('[data-map-branch]:visible').count()
                        assert visible_default<count,'La vista iniziale mostra anche i cassetti'
                        assert repo.locator('.map-branch:visible').first.get_attribute('class').find('map-release')>=0,'6.0 non in cima'
                        dates=repo.locator('[data-graph]>.map-branch:not(.map-release) time').evaluate_all('(es)=>es.map(e=>Date.parse(e.dateTime))');assert dates==sorted(dates,reverse=True),'Rami non ordinati dal più recente'
                        expect(repo.locator('.work-meta time')).to_have_count(count)
                        assert all(repo.locator('.work-author').all_text_contents()),'Autore mancante'
                        expect(repo.locator('.branch-code')).to_have_count(0)
                        assert not re.search(r'\+\d+\s*/\s*[−-]\d+', ' '.join(repo.locator('.pending-changes,.branch-meta').all_text_contents())),'Conteggi in codice'
                        repo.locator('[data-select=main]').click();expect(repo.locator('[data-map-branch]')).to_have_count(1)
                        repo.locator('[data-select=all]').click();expect(repo.locator('[data-map-branch]:visible')).to_have_count(count)
                        fits(page)
                        repo.locator('[data-select=active]').click();expect(repo.locator('[data-map-branch]:visible')).to_have_count(visible_default)
                        expect(repo.locator('[data-drawer][open]')).to_have_count(0)
                        repo.locator('[data-select=all]').click()
                        old=repo.locator('.map-main strong').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)');repo.locator('[data-zoom="+"]').click();assert repo.locator('.map-main strong').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>old;fits(page)
                        repo.locator('[data-zoom=reset]').click()
                    page.locator('#select-all').click();expect(page.locator('[data-map-branch]')).to_have_count(total)
                    if engine=='chromium' and screen in ['PC1920','TV']:
                        page.locator('.repo').first.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'ramificazioni-tutti-{screen}.png'))
                    assert not errors and not bad,{'js':errors,'http':bad};result['visite']+=1
                    if screen==screens[0][0]:
                        page.locator('#repo-filter').select_option('registro');expect(page.locator('[data-repository=sito]')).to_be_hidden()
                        page.locator('#branch-search').fill('versione-6-0');repo=page.locator('[data-repository=registro]');repo.locator('.map-branch:visible [data-branch]').first.click();expect(repo.locator('[data-detail]')).to_contain_text('Preparazione della 6.0')
                        repo.locator('.commit-history summary').click();expect(repo.locator('.commit-history li')).not_to_have_count(0)
                        repo.locator('.commit-history li>button').first.focus();page.keyboard.press('Enter');expect(repo.locator('[data-detail]')).to_contain_text('Commit Git')
                        repo.locator('[data-close]').click();expect(repo.locator('[data-detail]')).to_be_hidden()
                        page.locator('#select-all').click();expect(page.locator('#branch-search')).to_have_value('');fits(page)
                        repo.locator('.branch-selector summary').click();checkbox=repo.locator('[data-add]:not([disabled])').first;checkbox.uncheck();expect(repo.locator('[data-map-branch]')).to_have_count(len(SNAP['repositories'][1]['branches'])-1);checkbox.check()
                        # Un ramo aggiunto dall'aggiornamento entra da solo quando sono selezionati tutti.
                        before_colors=repo.locator('[data-map-branch]').evaluate_all('(es)=>Object.fromEntries(es.map(e=>[e.dataset.mapBranch,e.style.getPropertyValue("--branch")]))');new=copy.deepcopy(state['data']['repositories'][1]['branches'][-1]);new['name']='chatgpt/ramo-nuovo-del-collaudo';new['title']='Nuovo ramo dal feed';state['data']['repositories'][1]['branches'].append(new);state['data']['fingerprint']='ramo-nuovo';page.locator('#refresh').click();expect(repo.locator('[data-map-branch]')).to_have_count(len(SNAP['repositories'][1]['branches'])+1);fits(page)
                        after_colors=repo.locator('[data-map-branch]').evaluate_all('(es)=>Object.fromEntries(es.map(e=>[e.dataset.mapBranch,e.style.getPropertyValue("--branch")]))');assert all(after_colors[n]==v for n,v in before_colors.items()),'Un ramo nuovo ha cambiato i colori esistenti';page.reload(wait_until='load');expect(repo.locator('[data-map-branch]')).to_have_count(len(SNAP['repositories'][1]['branches'])+1);after_reload=repo.locator('[data-map-branch]').evaluate_all('(es)=>Object.fromEntries(es.map(e=>[e.dataset.mapBranch,e.style.getPropertyValue("--branch")]))');assert after_reload==after_colors,'Colori cambiati al ricaricamento'
                        state['data']['updated']='2000-01-01T00:00:00Z';state['data']['fingerprint']='copia-vecchia';state['data']['repositories'][1]['version']='99.9';page.locator('#refresh').click();expect(page.locator('#update-status')).to_contain_text('più recente');expect(repo).not_to_contain_text('99.9');state['fail']=True;page.locator('#refresh').click();expect(page.locator('#update-status')).to_contain_text('ultima copia');expect(page.locator('.repo')).to_have_count(2)
                        result['interazioni'].append(engine+': Vista in corso ordinata, 6.0 in cima, cassetti, data/autore, parole senza codici, selezione collettiva/singola, dettagli, tastiera, A+, nuovi rami, colori e rete: PASS')
                except Exception as e:result['problemi'].append(f'{engine}/{screen}: {e!r}'[:1600]);print(result['problemi'][-1],flush=True)
                c.close();print(engine,screen,'Visite',result['visite'],'Problemi',len(result['problemi']),flush=True)
            b.close()
    (OUT/'collaudo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(result['problemi']))


if __name__=='__main__':main()
