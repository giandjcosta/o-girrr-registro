"""Prova isolata: server da /workspace su 8765. Nessun sito o database scritto."""
from pathlib import Path
import json, os, tempfile
from playwright.sync_api import sync_playwright
BASE=os.environ.get('TIFOSI_BASE','http://127.0.0.1:8765/o-girrr-registro/lab/prova-tifosi/')
ROOT=Path(__file__).resolve().parents[1]
PHOTO=ROOT/'lab/prova-tifosi/foto';PHOTO.mkdir(exist_ok=True)
TEMP=Path(tempfile.mkdtemp(prefix='tifosi-foto-'))
PAGES=[('home','index.html','pt-mvp-notice'),('mvp','curva.html','pt-mvp'),('derby','derby.html','pt-derby'),('carriera','app.html','pt-storia'),('giornale','giornale.html','pt-articolo'),('archivio','albo.html','pt-archivio')]
report={'motori':{},'problemi':[],'schermate':0,'visite':0,'verifiche':[]}
if os.environ.get('TIFOSI_SOLO_PERCORSI') or os.environ.get('TIFOSI_FOTO'):
    report=json.loads((ROOT/'lab/prova-tifosi/collaudo.json').read_text())
    if os.environ.get('TIFOSI_SOLO_PERCORSI'):
        report['tentativi_precedenti_interazioni']=report.get('tentativi_precedenti_interazioni',[])+[x for x in report['problemi'] if '/Interazioni:' in x]
        report['problemi']=[x for x in report['problemi'] if '/Interazioni:' not in x]
def fonts(ctx):
    cache=Path(os.environ.get('TIFOSI_FONT_CACHE','/tmp/tifosi-font-cache'))
    if (cache/'fonts.json').exists():
        mapping=json.loads((cache/'fonts.json').read_text())
        ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=(cache/'fonts.css').read_text()))
        ctx.route('https://fonts.gstatic.com/**',lambda r:r.fulfill(status=200,content_type='font/ttf',body=Path(mapping[r.request.url]).read_bytes()) if r.request.url in mapping else r.continue_())
    else:
        ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=''))
with sync_playwright() as p:
    profiles=[('SE320',{'viewport':{'width':320,'height':568}}),('SE',p.devices['iPhone SE']),('iPhone15',p.devices['iPhone 15 Pro']),('iPhoneMax',p.devices['iPhone 15 Pro Max']),('AndroidS8',p.devices['Galaxy S8']),('Pixel7',p.devices['Pixel 7']),('AndroidS9',p.devices['Galaxy S9+']),('iPadMini',p.devices['iPad Mini']),('iPadLandscape',p.devices['iPad (gen 7) landscape']),('iPadPro',p.devices['iPad Pro 11']),('AndroidTab',p.devices['Galaxy Tab S4']),('AndroidTabLandscape',p.devices['Galaxy Tab S4 landscape']),('PC1280',{'viewport':{'width':1280,'height':850}}),('PC1920',{'viewport':{'width':1920,'height':1080}}),('Monitor2560',{'viewport':{'width':2560,'height':1440}}),('TV',{'viewport':{'width':1920,'height':1080},'device_scale_factor':2}),('390',{'viewport':{'width':390,'height':844}}),('768',{'viewport':{'width':768,'height':1024}}),('1440',{'viewport':{'width':1440,'height':900}})]
    if os.environ.get('TIFOSI_FOTO'):
        profiles=[x for x in profiles if x[0] in ['SE320','PC1280','390']]
        report['schermate']=0
        report['font_originali']='Riprova 320/390/1280 con cache temporanea Inter, Lobster e Lora usati dal sito'
    if os.environ.get('TIFOSI_SOLO_PERCORSI'):profiles=[]
    browsers=[]
    for engine in ['chromium','webkit','firefox']:
        try:
            opts={'executable_path':'/usr/bin/chromium','args':['--no-sandbox']} if engine=='chromium' else {}
            browser=getattr(p,engine).launch(**opts);browsers.append((engine,browser));report['motori'][engine]='Eseguito'
        except Exception:
            report['motori'][engine]='Non disponibile: eseguibile Playwright assente'
    for engine,browser in browsers:
        for pn,options in profiles:
            options=dict(options);options.pop('default_browser_type',None)
            if engine=='firefox':options.pop('is_mobile',None)
            ctx=browser.new_context(**options);fonts(ctx);page=ctx.new_page();errors=[];bad=[];external=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('response',lambda r:bad.append(str(r.status)+' '+r.url) if r.status>=400 else None)
            page.on('request',lambda r:external.append(r.url) if 'supabase.' in r.url else None)
            # Non dipendere dai font remoti per misure e assenza errori di rete.
            # I font vengono predisposti dal contesto, prima della prima pagina.
            for skin in ['lega','stadio']:
                for slug,file,target in PAGES:
                    errors.clear();bad.clear();external.clear()
                    u=BASE+skin+'/'+file+'?novita=1&squadra=Oranje%20VC'+('#carriera' if slug=='carriera' else '')
                    try:
                        page.goto(u,wait_until='load');page.evaluate('document.fonts.ready');page.locator('#'+target).wait_for(state='attached');page.wait_for_timeout(120)
                        if slug=='mvp':
                            # La Curva inserisce il sondaggio nel proprio menu: aprirlo dal richiamo Home usa l'ancora.
                            page.evaluate("document.getElementById('pt-mvp').scrollIntoView()")
                        if slug=='archivio':
                            page.evaluate("location.hash='pt-archivio'");page.wait_for_timeout(100)
                        overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                        if overflow:raise AssertionError('Scorrimento orizzontale')
                        if errors or bad or external:raise AssertionError(json.dumps({'js':errors,'http':bad,'supabase':external}))
                        report['visite']+=1
                        if engine=='chromium' and pn in ['390','PC1280']:
                            w=options['viewport']['width']
                            page.evaluate('(id)=>{let el=document.getElementById(id);window.scrollTo(0,el.getBoundingClientRect().top+scrollY-150)}',target);page.wait_for_timeout(220)
                            after=TEMP/f'{slug}-{skin}-{w}-dopo.png';page.screenshot(path=str(after))
                            # Il comando Prima deve eliminare tutte le aggiunte conservando la pagina nativa.
                            page.goto(u.replace('?novita=1','?prima=1&novita=1'),wait_until='load');page.evaluate('document.fonts.ready');page.wait_for_timeout(350)
                            assert page.locator('.pt-box').count()==0
                            before=TEMP/f'{slug}-{skin}-{w}-prima.png';page.screenshot(path=str(before))
                            # Affiancamento di screenshot integrali, senza alterare le pagine.
                            from PIL import Image,ImageDraw
                            a=Image.open(before);b=Image.open(after);canvas=Image.new('RGB',(a.width+b.width,max(a.height,b.height)+32),'#10192f');canvas.paste(a,(0,32));canvas.paste(b,(a.width,32));draw=ImageDraw.Draw(canvas);draw.text((12,8),'PRIMA',fill='white');draw.text((a.width+12,8),'CON PROPOSTE',fill='white');canvas.save(PHOTO/f'{slug}-{skin}-{w}.png');report['schermate']+=1
                    except Exception as e:report['problemi'].append(f'{engine}/{pn}/{skin}/{slug}: {str(e)[:500]}')
            ctx.close()
            print(engine,pn,'Visite',report['visite'],'Problemi',len(report['problemi']),flush=True)
        # Percorsi e interazione nel browser reale.
        ctx=browser.new_context(viewport={'width':390,'height':844});fonts(ctx);page=ctx.new_page()
        try:
            for skin in ['lega','stadio']:
                page.goto(BASE+skin+'/index.html?novita=1&squadra=Oranje%20VC');page.locator('#pt-mvp-notice').click();page.locator('#pt-mvp').wait_for(state='visible')
                assert '/prova-tifosi/'+skin+'/curva.html' in page.url
                page.locator('[data-pt-vote="Oranje VC"]').click();assert page.locator('[data-pt-vote="Oranje VC"]').get_attribute('aria-pressed')=='true'
                page.reload();page.locator('[data-pt-vote="Oranje VC"][aria-pressed="true"]').wait_for()
                page.locator('[data-pt-vote="stif dc"]').click();assert page.locator('[data-pt-vote][aria-pressed=true]').count()==1
                page.locator('[data-pt-abstain]').click();assert page.locator('[data-pt-vote][aria-pressed=true]').count()==0
                page.locator('#pt-mvp a').filter(has_text='Il verdetto').click();page.locator('#pt-articolo').wait_for(state='visible')
                page.locator('#pt-articolo a').click();page.locator('#pt-mvp').wait_for(state='visible')
                page.locator('#pt-mvp a').filter(has_text='Archivio').click();page.locator('#pt-archivio').wait_for(state='visible')
                page.goto(BASE+skin+'/index.html?novita=1');assert page.locator('#pt-storia-home,#pt-home').count()==0;assert page.locator('.v53-home a[href*="derby.html"]').count()==0
                page.locator('#pt-mvp-notice').get_by_text('Letta',exact=True).wait_for(state='visible')
                page.goto(BASE+skin+'/albo.html');page.locator('[data-at="derby"]').click();page.locator('#pt-derby-access a').click();page.locator('#pt-derby').wait_for(state='visible')
                page.locator('#lg').click();page.locator('#pt-mvp-notice').wait_for(state='visible')
                page.goto(BASE+skin+'/app.html?novita=1&squadra=Oranje%20VC#carriera');page.locator('#pt-storia').wait_for(state='visible');assert page.locator('#pt-storia .pt-revision').is_visible()
                page.locator('#olg').click();page.locator('#pt-mvp-notice').wait_for(state='visible')
                for _,file,target in PAGES:
                    fragment='carriera' if file=='app.html' else target
                    page.goto(BASE+skin+'/'+file+'?novita=1#'+fragment)
                    selector='#pt-mvp-notice .pt-new-badge' if file=='index.html' else '#'+target+' .pt-revision'
                    page.locator(selector).wait_for(state='visible');page.wait_for_timeout(1900)
                    rect=page.locator(selector).bounding_box();assert rect and 0<=rect['y']<600,(file,rect)
                report['verifiche'].append(engine+'/'+skin+': Sei link diretti con targhetta Novità nel viewport')
                report['verifiche'].append(engine+'/'+skin+': Home→Voto→Giornale→Voto→Archivio; notifica letta; voto/cambio/ritiro/persistenza; Albo→Derby; Carriera→Logo Home; nessun riepilogo/Derby aggiunto in Home')
        except Exception as e:
            import traceback
            report['problemi'].append(engine+'/Interazioni: '+traceback.format_exc()[-1800:])
        ctx.close();browser.close()
report['verifiche']=list(dict.fromkeys(report['verifiche']))
(ROOT/'lab/prova-tifosi/collaudo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(report['problemi']))
