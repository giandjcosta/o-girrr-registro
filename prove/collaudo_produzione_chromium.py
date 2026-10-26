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
    page=browser.new_page()
    page.goto(BASE+'/index.html',wait_until='domcontentloaded',timeout=30000)
    page.wait_for_timeout(500)
    if page.evaluate('typeof window.spgLazyWrap')!='function':
        failures.append('Lazy wrapper non caricato sulla pagina principale')
    page.close()
    browser.close()
print('QA', 'PASS' if not failures else 'FAIL',failures)
sys.exit(1 if failures else 0)
