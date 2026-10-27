from playwright.sync_api import sync_playwright
errors=[]
with sync_playwright() as p:
 for engine in ('chromium','webkit'):
  browser=getattr(p,engine).launch(headless=True)
  for route in ('girrr/app.html','stadio/girrr/app.html'):
   for width in (320,390,768,1440):
    page=browser.new_page(viewport={'width':width,'height':900})
    page.add_init_script("localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'TEST-ONLY'}))")
    try:
     page.goto('http://127.0.0.1:8765/prod/'+route+'#carriera',wait_until='domcontentloaded',timeout=30000)
     page.locator('.trust-visual .trust-fill').wait_for(timeout=14000)
     gauge=page.locator('.trust-visual')
     assert gauge.locator('circle').count()==0
     assert page.locator('select#fg').input_value()=='2'
     assert page.locator('select#fp').input_value()=='5'
     assert page.locator('.ob > .pbar').count()>=4
     assert page.locator('h3').filter(has_text='Reputazione permanente').count()>=1
     page.locator('#fp').select_option('8')
     page.locator('#cteam').select_option(label='Apo team')
     assert page.locator('#fg').input_value()=='2'
     assert page.locator('#fp').input_value()=='1'
     page.wait_for_function("""() => {const e=document.querySelector('.trust-visual');return e&&Math.abs(Number(e.querySelector('.trust-fill').getAttribute('stroke-dasharray').split(' ')[0])-Number(e.dataset.target))<.1}""",timeout=9000)
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
     print('CAREER-PASS',engine,route,width)
    except Exception as e:errors.append((engine,route,width,str(e)));print('CAREER-FAIL',engine,route,width,str(e))
    page.close()
  for width in (320,1440):
   page=browser.new_page(viewport={'width':width,'height':900})
   try:
    page.goto('http://127.0.0.1:8765/prod/girrr/totogirrr.html?demo',wait_until='domcontentloaded')
    page.locator('#riscatta-sponsor').wait_for(timeout=16000)
    page.locator('#riscatta-sponsor').click()
    page.locator('.prize-corner.claimed').wait_for(timeout=12000)
    page.wait_for_timeout(900)
    assert '550' in page.locator('.bal b').inner_text()
    print('CLAIM-PASS',engine,width)
   except Exception as e:errors.append((engine,'Totogirrr',width,str(e)));print('CLAIM-FAIL',engine,width,str(e))
   page.close()
  browser.close()
assert not errors,errors
