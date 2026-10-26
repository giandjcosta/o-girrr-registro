import sys
from playwright.sync_api import sync_playwright

BASE='http://127.0.0.1:8765'
failures=[]
with sync_playwright() as p:
  for browser_name in ('chromium','webkit'):
    browser=getattr(p,browser_name).launch(headless=True)
    for route in ('girrr/app.html','stadio/girrr/app.html'):
      for width in (320,375,768,1440):
        page=browser.new_page(viewport={'width':width,'height':900})
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.add_init_script("localStorage.setItem('fg', JSON.stringify({team:'Oranje VC',code:'TEST-ONLY'}))")
        try:
          page.goto(BASE+'/'+route+'#carriera',wait_until='domcontentloaded',timeout=30000)
          page.locator('.ob').last.wait_for(timeout=12000)
          # Ultima scheda: sponsor (Termoidraulica Bepi per Oranje VC).
          card=page.locator('.ob').last
          result=card.evaluate("""el=>{
            const rect=e=>e.getBoundingClientRect();
            const title=el.querySelector('.grow>b'), badge=el.querySelector('.tag'),track=el.querySelector(':scope > .pbar'),fill=track?.querySelector('i'), logo=el.querySelector('img');
            const T=rect(title), B=rect(badge), P=track?rect(track):null, F=fill?rect(fill):null, C=rect(el);
            const css=track?getComputedStyle(track):null;
            return {text:title.textContent,titleWidth:T.width,titleHeight:T.height,titleRight:T.right,
              badgeTop:B.top,badgeBottom:B.bottom,badgeRight:B.right,
              progressWidth:P?.width,progressLeft:P?.left,progressTop:P?.top,fillWidth:F?.width,
              trackColor:css?.backgroundColor,
              cardWidth:C.width, cardLeft:C.left,logoWidth:logo?rect(logo).width:0,
              overflow:document.documentElement.scrollWidth>innerWidth};
          }""")
          mobile=width<=700
          # In mobile testo non deve essere schiacciato; badge sotto testo e barra sotto badge.
          checks=[
            result['text'].startswith('Resta nella metà alta'),
            result['titleWidth']>= (125 if width<=375 else 200),
            not result['overflow'],
            result['badgeRight']<=width,
            result['progressWidth']>=result['cardWidth']-3,
            result['fillWidth']>0 and result['fillWidth']<result['progressWidth'],
            result['trackColor'] not in (None,'rgba(0, 0, 0, 0)','transparent')
          ]
          if mobile:
            checks += [result['badgeTop']>=card.locator('.grow').bounding_box()['y']+result['titleHeight']-2,
               result['progressTop']>=result['badgeBottom']-1]
          print('CAREER',browser_name,route,width,result,'passed',all(checks))
          if not all(checks): failures.append(f'{browser_name} {route} {width}: {result} checks {checks}')
          if errors: failures.append(f'{browser_name} {route} {width}: JS errors {errors[:2]}')
        except Exception as e:
          failures.append(f'{browser_name} {route} {width}: {e}')
        page.close()
    browser.close()
print('QA', 'PASS' if not failures else 'FAIL', failures)
sys.exit(1 if failures else 0)
