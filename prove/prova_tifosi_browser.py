"""Preview integrata: tre motori reali, sedici profili e interazioni locali.
PLAYWRIGHT_BROWSERS_PATH e WEBKIT_PATH permettono installazioni portatili.
Non contatta Supabase: qualsiasi richiesta al servizio fallisce il collaudo.
"""
from pathlib import Path
import json, os, sys, re, mimetypes, traceback
from urllib.parse import urlsplit,unquote
from playwright.sync_api import sync_playwright, expect
from rete_browser import installa
R=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('TIFOSI_OUT',str(R/'qa_artifacts/tifosi')));OUT.mkdir(parents=True,exist_ok=True)
BASE=os.environ.get('TIFOSI_BASE','http://127.0.0.1:8899/lab/prova-tifosi/')
def routes(c):
 installa(c)
 def repo(route):
  path=unquote(urlsplit(route.request.url).path).removeprefix('/o-girrr-registro/')
  f=(R/'.preview-site'/path).resolve()
  if not f.is_relative_to(R/'.preview-site') or not f.is_file():route.fulfill(status=404,body='File non trovato');return
  route.fulfill(status=200,content_type=mimetypes.guess_type(f.name)[0] or 'application/octet-stream',body=f.read_bytes())
 c.route(re.compile(r'http://127\.0\.0\.1:8899/o-girrr-registro/.*'),repo)
PAGES=[('home','index.html','#pt-home-story'),('mvp','app.html?sezione=mvp#sport','#pt-mvp'),('derby','derby.html#pt-derby','#pt-derby'),('curva','curva.html#pt-mvp','#pt-mvp'),('settimana','app.html?sezione=settimana#carriera','#pt-storia'),('archivio','albo.html#pt-archivio','#pt-archivio')]
report={'motori':{},'visite':0,'problemi':[],'interazioni':[],'schermi_per_motore':16,'browser_di_marca':'Samsung Internet, Safari su dispositivo, Chrome ed Edge di marca non disponibili. Profili emulati, motori effettivi.'}
with sync_playwright() as p:
 screens=[('iPhone320',dict(p.devices['iPhone SE'],viewport={'width':320,'height':568}))]+[(n,p.devices[n]) for n in ['iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape']]+[(f'PC{w}',{'viewport':{'width':w,'height':900}}) for w in [1280,1920,2560]]+[('TV',{'viewport':{'width':1920,'height':1080},'device_scale_factor':2})]
 if os.environ.get('TIFOSI_SCHERMI'):screens=[x for x in screens if x[0] in os.environ['TIFOSI_SCHERMI'].split(',')]
 report['schermi_per_motore']=len(screens)
 for engine in os.environ.get('MOTORI','chromium,webkit,firefox').split(','):
  opts={}
  if engine=='webkit' and os.environ.get('WEBKIT_PATH'):opts['executable_path']=os.environ['WEBKIT_PATH']
  try:b=getattr(p,engine).launch(**opts);report['motori'][engine]={'stato':'Eseguito','versione':b.version}
  except Exception as e:report['motori'][engine]={'stato':'Non disponibile','errore':str(e)[:350]};continue
  for screen,options in screens:
   options=dict(options);options.pop('default_browser_type',None)
   if engine=='firefox':options.pop('is_mobile',None)
   c=b.new_context(**options,service_workers='block');routes(c);page=c.new_page();page.set_default_timeout(8000)
   errors=[];bad=[];external=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:bad.append(str(r.status)+' '+r.url) if r.status>=400 else None)
   page.on('request',lambda r:external.append(r.url) if '.supabase.co/' in r.url or r.method not in ['GET','HEAD'] else None)
   for skin in ['lega','stadio']:
    for slug,path,target in PAGES:
     errors.clear();bad.clear();external.clear()
     try:
      page.goto(BASE+skin+'/'+path,wait_until='load');page.locator(target).wait_for(state='visible');page.evaluate('document.fonts.ready');page.wait_for_timeout(60)
      assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Scorrimento orizzontale'
      assert not errors and not bad and not external,json.dumps({'js':errors,'http':bad,'rete':external})
      if slug=='settimana':
       expect(page.locator('[data-pt-week]')).to_have_attribute('aria-pressed','true')
       expect(page.locator('#view>.card:visible')).to_have_count(0)
      if slug=='mvp':expect(page.locator('[data-pt-sport]')).to_have_attribute('aria-pressed','true')
      if engine=='chromium' and screen in ['PC1920','TV','iPhone320'] and slug in ['mvp','derby','settimana']:
       page.locator(target).scroll_into_view_if_needed();page.wait_for_timeout(500);page.screenshot(path=str(OUT/f'{skin}-{slug}-{screen}.png'))
      report['visite']+=1
     except Exception as e:
      issue=f'{engine}/{screen}/{skin}/{slug}: {e!s}'[:1000];report['problemi'].append(issue);print(issue,flush=True)
   c.close();print(engine,screen,'Visite',report['visite'],'Problemi',len(report['problemi']),flush=True)
  c=b.new_context(viewport={'width':390,'height':844},service_workers='block');routes(c);page=c.new_page();page.set_default_timeout(8000)
  for skin in ['lega','stadio']:
   try:
    page.goto(BASE,wait_until='load');page.evaluate("localStorage.setItem('fg',JSON.stringify({team:'Non modificare',code:'sentinella-locale'}))")
    page.goto(BASE+skin+'/index.html',wait_until='networkidle')
    page.locator('#pt-mvp-notice').click();page.wait_for_url('**/app.html?**#sport');page.locator('#pt-mvp').wait_for(state='visible')
    page.locator('[data-pt-vote]').first.click();assert page.locator('[data-pt-vote][aria-pressed=true]').count()==1
    assert '40%' in page.locator('.pt-jury').inner_text()
    chosen=page.locator('[data-pt-vote][aria-pressed=true]').get_attribute('data-pt-vote')
    page.locator('[data-pt-vote][aria-pressed=false]').first.click();assert page.locator('[data-pt-vote][aria-pressed=true]').get_attribute('data-pt-vote')!=chosen
    page.reload(wait_until='networkidle');assert page.locator('[data-pt-withdraw]').count()==1
    page.locator('[data-pt-withdraw]').click();assert page.locator('[data-pt-vote][aria-pressed=true]').count()==0;assert '50%' in page.locator('.pt-jury').inner_text()
    page.locator('[data-sp=giornale]').click();page.locator('#pt-mvp').wait_for(state='detached');page.locator('[data-pt-sport]').click();page.locator('#pt-mvp').wait_for(state='visible')
    page.goto(BASE+skin+'/app.html?sezione=settimana#carriera',wait_until='networkidle');page.locator('[data-pt-day="7"]').wait_for(state='visible')
    assert '2 incontri' in page.locator('[data-pt-day="7"]').inner_text()
    titles=page.locator('[data-pt-day] .pt-week-title small').all_text_contents();assert len(set(titles))==7
    page.locator('[data-pt-day="6"]>summary').click();assert 'Champions Cup' in page.locator('[data-pt-day="6"]').inner_text()
    page.locator('[data-ctab=pan]').first.click();page.locator('#pt-storia').wait_for(state='detached');page.locator('[data-pt-week]').click();page.locator('#pt-storia').wait_for(state='visible')
    with page.expect_navigation(wait_until='load'):page.locator('#pt-team').select_option('stif dc')
    expect(page.locator('[data-pt-day="7"]')).to_contain_text('1 incontro giocato')
    with page.expect_navigation(wait_until='load'):page.locator('a[data-pt-skin]').click()
    assert 'sezione=settimana' in page.url;page.locator('#pt-storia').wait_for(state='visible')
    page.goto(BASE+skin+'/derby.html',wait_until='networkidle');assert page.locator('#pt-derby tbody tr').count()==5
    page.locator('[data-pt-comp=cup]').click();assert page.locator('#pt-derby tbody tr').count()==4
    assert 'rgb(61, 147, 214)'==page.locator('[data-pt-comp=cup]').evaluate('e=>getComputedStyle(e).backgroundColor')
    page.locator('[data-pt-comp=lega]').click();assert 'rgb(214, 40, 57)'==page.locator('[data-pt-comp=lega]').evaluate('e=>getComputedStyle(e).backgroundColor')
    page.goto(BASE+skin+'/index.html?prima=1',wait_until='networkidle');assert page.locator('.pt-box').count()==0
    page.goto(BASE,wait_until='load');assert page.evaluate("JSON.parse(localStorage.getItem('fg')).code")=="sentinella-locale"
    report['interazioni'].append(engine+'/'+skin+': PASS · Home→Sport, voto/cambio/ritiro/persistenza, schede native, sette racconti, Coppa/riposo, squadra, grafica, Derby, Prima')
   except Exception as e:report['problemi'].append(engine+'/'+skin+'/Interazioni: '+traceback.format_exc()[-1800:]);print(traceback.format_exc(),flush=True)
  c.close();b.close()
(OUT/'collaudo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(bool(report['problemi']) or any(v['stato']!='Eseguito' for v in report['motori'].values()))
