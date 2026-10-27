import sys
from playwright.sync_api import sync_playwright
base='http://127.0.0.1:8765/'
failures=[]
with sync_playwright() as p:
 for browser_name in ('chromium','webkit'):
  browser=getattr(p,browser_name).launch(headless=True)
  for route in ('lab/index.html','anteprima/index.html','anteprima/attuale.html'):
   for width in (320,390,768,1440):
    page=browser.new_page(viewport={'width':width,'height':900})
    page.add_init_script("localStorage.setItem('fg', JSON.stringify({team:'Oranje VC',code:'TEST-ONLY'}))")
    errors=[]
    page.on('pageerror',lambda x:errors.append(str(x)))
    try:
     page.goto(base+route+'#carriera',wait_until='domcontentloaded')
     page.locator('.trust-visual .trust-fill').wait_for(timeout=10000)
     before=page.locator('.trust-visual').get_attribute('data-target')
     options=page.locator('#cteam option').all_text_contents()
     other=next(t for t in options if t!='Oranje VC')
     page.locator('#cteam').select_option(label=other)
     page.wait_for_function("old => document.querySelector('.trust-visual')?.dataset.target !== old",arg=before,timeout=10000)
     page.wait_for_timeout(1500)
     page.wait_for_function("Math.abs(Number(document.querySelector('.trust-fill').getAttribute('stroke-dasharray').split(' ')[0])-Number(document.querySelector('.trust-visual').dataset.target))<0.06",timeout=6000)
     q=page.evaluate("""() => {
       const el=document.querySelector('.trust-visual'), path=el?.querySelector('.trust-fill'), num=el?.querySelector('.trust-number'),
       gray=el?.querySelector('svg>path'), text=el?.querySelector('svg[aria-label]');
       const rewards=document.querySelector('[aria-label="Premi Carriera in simulazione"]');
       return {value:+el?.dataset.target,dash:path?.getAttribute('stroke-dasharray'),
         label:text?.getAttribute('aria-label'),number:+num?.textContent,gray:gray?.getAttribute('stroke'),
         multicolor:!!el?.querySelector('linearGradient'),hasMarker:!!el?.querySelector('circle'),
         reputation:!!rewards,
         overflow:document.documentElement.scrollWidth>innerWidth};
     }""")
     checks=[abs(float(q['dash'].split(' ')[0])-q['value'])<0.06,q['value']==q['number'],q['gray']=='rgba(255,255,255,.22)',
       q['multicolor'],not q['hasMarker'],q['reputation'],not q['overflow'],not errors]
     if before==str(q['value']):checks.append(False)
     if not all(checks):failures.append((browser_name,route,width,q,errors,checks))
     print('ANIM',browser_name,route,width,'PASS' if all(checks) else 'FAIL',q)
    except Exception as ex:
     failures.append((browser_name,route,width,str(ex)))
    page.close()
  for width in (320,390,1440):
   page=browser.new_page(viewport={'width':width,'height':900})
   try:
    page.goto(base+'anteprima/totogirrr-52.html',wait_until='domcontentloaded')
    page.locator('#riscatta-sponsor').wait_for(timeout=18000)
    pre=page.locator('.bal b').inner_text()
    page.locator('#riscatta-sponsor').click()
    page.locator('.prize-corner.claimed').wait_for(timeout=10000)
    page.wait_for_timeout(850)
    post=page.locator('.bal b').inner_text()
    assert pre!=post,(browser_name,width,'balance unchanged',pre,post)
    assert not page.locator('#riscatta-sponsor').count()
    print('TOTOGIRRR-CLAIM',browser_name,width,'PASS',pre,post)
   except Exception as ex:
    failures.append(('TOTOGIRRR-CLAIM',browser_name,width,str(ex)))
    print('TOTOGIRRR-CLAIM',browser_name,width,'FAIL',str(ex))
   page.close()
  browser.close()
print('QA', 'PASS' if not failures else 'FAIL', failures[:5])
sys.exit(1 if failures else 0)
