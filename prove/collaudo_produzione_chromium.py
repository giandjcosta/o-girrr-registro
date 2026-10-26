import sys
from playwright.sync_api import sync_playwright

BASE='http://127.0.0.1:8765'
failures=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    for width in (320,375,768):
        page=browser.new_page(viewport={'width':width,'height':850})
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        # Solo nell'harness locale: imposta una squadra esistente con codice fittizio.
        page.add_init_script("localStorage.setItem('fg', JSON.stringify({team:'Oranje VC',code:'TEST-ONLY'}))")
        page.goto(BASE+'/girrr/app.html#carriera',wait_until='domcontentloaded',timeout=30000)
        page.wait_for_timeout(2500)
        cards=page.locator('.ob')
        if cards.count()==0:
            failures.append(f'Carriera {width}: nessun obiettivo renderizzato')
        else:
            q=cards.first.evaluate('''el=>{
              const r=x=>x.getBoundingClientRect(),t=el.querySelector('.grow>b'),p=el.querySelector('.pbar'),b=el.querySelector('.tag');
              return {title:r(t).width,track:r(p).width,badgeRight:r(b).right,overflow:document.documentElement.scrollWidth>innerWidth};
            }''')
            if q['overflow'] or q['title']<85 or q['track']<85 or q['badgeRight']>width:
                failures.append(f'Carriera {width}: {q}')
            print('CAREER',width,q)
        if errors:failures.append(f'Carriera {width} JS errors: {errors[:2]}')
        page.close()
    for route in ('girrr/curva.html','stadio/girrr/curva.html'):
        page=browser.new_page(viewport={'width':320,'height':800})
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.goto(BASE+'/'+route,wait_until='domcontentloaded',timeout=30000)
        page.wait_for_timeout(3000)
        feed=page.locator('#vista article.post')
        before=feed.count()
        marker=page.locator('#piu-feed').count()
        if before>20:
            failures.append(f'{route}: {before} post renderizzati al primo caricamento (limite 20)')
        if before>=20 and marker:
            page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
            page.wait_for_timeout(1500)
            after=feed.count()
            if after<=before:
                failures.append(f'{route}: scroll non ha caricato altri cori ({before}→{after})')
        else:
            after=before
        overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth')
        if overflow:
            failures.append(f'{route}: overflow a 320px')
        print('CURVA',route,{'prima':before,'dopo':after,'marker':marker,'overflow':overflow,'js_errors':errors[:2]})
        if errors:failures.append(f'{route} JS errors: {errors[:2]}')
        page.close()
    page=browser.new_page()
    page.goto(BASE+'/index.html',wait_until='domcontentloaded',timeout=30000)
    page.wait_for_timeout(500)
    if page.evaluate('typeof window.spgLazyWrap')!='function':
        failures.append('Lazy wrapper non caricato sulla pagina principale')
    page.close()
    browser.close()
print('QA', 'PASS' if not failures else 'FAIL',failures)
sys.exit(1 if failures else 0)
