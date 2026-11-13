"""6.0 di Claude + modulo tifosi + Ramificazioni. RPC simulate, nessuna richiesta al DB vero."""
from pathlib import Path
import copy
import datetime as dt
import json
import mimetypes
import os
import re
import sys
from urllib.parse import unquote,urlsplit
from playwright.sync_api import sync_playwright,expect
from rete_browser import installa

ROOT=Path(__file__).resolve().parents[1]
SITE=Path(os.environ.get('SITO_60','/workspace/girrr-site60'))
OUT=Path(os.environ.get('QA_OUT',str(ROOT/'qa_artifacts/integrazione60')));OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:8765/o-fant-a-girrr/';REG='http://127.0.0.1:8766/o-girrr-registro/'
sys.path.insert(0,str(ROOT/'redazione'));from tifosi import context
DERBY=json.loads((ROOT/'lab/prova-tifosi/dati.json').read_text())['derby_ufficiali']
CTX,_=context(SITE,DERBY);WEEK=CTX['giornate'][-1];ED=json.loads((SITE/'girrr/dati/tifosi-settimane.json').read_text())
CODE='solo-browser';TEAM='Oranje VC'


def h32(s):
    v=2166136261
    for c in s:v=((v^ord(c))*16777619)&0xffffffff
    alphabet='0123456789abcdefghijklmnopqrstuvwxyz';out=''
    while v:out=alphabet[v%36]+out;v//=36
    return out or '0'


class Database:
    def __init__(self):self.votes={};self.calls=[];self.fail=False
    def state(self):
        red=ED['giornate']['7']['redazione'];bots=WEEK['personaggi'];n=len(self.votes);rows=[]
        for c in WEEK['candidati']:
            r=sum(v['scelta']==c['team'] for v in red);b=sum(v['scelta']==c['team'] for v in bots);h=sum(v==c['team'] for v in self.votes.values())
            rows.append({**c,'red':r,'personaggi':b,'umani':h,'humanCount':n,'total':100*((.4 if n else .5)*r/len(red)+(.4 if n else .5)*b/len(bots)+(.2*h/n if n else 0))})
        rows.sort(key=lambda r:(-r['total'],-r['red'],r['team'].lower()))
        return {'votazione':{'stagione':'2026/27','giornata':7,'firma':WEEK['firma'],'chiude':(dt.datetime.now(dt.timezone.utc)+dt.timedelta(days=2)).isoformat(),'chiusa':None,'classifica':rows,'redazione':red,'personaggi':bots},'archivio':[]}
    def route(self,r):
        cors={'Access-Control-Allow-Origin':r.request.headers.get('origin','*'),'Access-Control-Allow-Methods':'GET, POST, OPTIONS','Access-Control-Allow-Headers':'apikey, authorization, content-type, x-client-info','Access-Control-Allow-Credentials':'true'}
        if r.request.method=='OPTIONS':r.fulfill(status=204,headers=cors);return
        fn=urlsplit(r.request.url).path.split('/')[-1];body=r.request.post_data_json or {};self.calls.append((fn,body))
        if fn=='mvp_stato':j=self.state()
        elif fn=='mvp_derby':j=DERBY
        elif fn=='mvp_mio':j={'scelta':self.votes.get(body.get('p_team'))}
        elif fn=='mvp_vota':
            if self.fail:r.fulfill(status=503,headers=cors,content_type='application/json',body='{"error":"Errore simulato"}');return
            assert body['p_team']==TEAM and body['p_code']==CODE,'Il voto deve appartenere alla squadra autenticata'
            if body['p_scelta'] is None:self.votes.pop(TEAM,None)
            else:self.votes[TEAM]=body['p_scelta']
            j={**self.state(),'scelta':body['p_scelta']}
        elif fn=='derby_stato':
            snap=json.loads((ROOT/'lab/prova-tifosi/derby-ufficiali.json').read_text());j={'ok':True,'voti':snap.get('voti',[]),'sfide':snap.get('sfide',[])}
        else:
            j={'ok':True,'posts':[],'post':[],'replies':[],'react':[],'mine':[],'follow':[],'prof':{},'commenti':[],'eventi':[],'notifiche':[],'voti':[],'sfide':[],'conf':[]}
        r.fulfill(status=200,headers=cors,content_type='application/json',body=json.dumps(j))


def routes(c,db):
    installa(c)
    c.route('https://*.supabase.co/**',db.route)
    c.route('https://*.goatcounter.com/**',lambda r:r.fulfill(status=200,content_type='application/javascript',body=''))
    def local(r):
        url=urlsplit(r.request.url);base=ROOT if url.port==8766 else SITE
        path=unquote(url.path).lstrip('/');path=path.removeprefix('o-girrr-registro/') if base==ROOT else path.removeprefix('o-fant-a-girrr/')
        f=(base/path).resolve()
        if f.is_dir():f=f/'index.html'
        if not f.is_relative_to(base) or not f.is_file():r.fulfill(status=404,body='File non trovato: '+str(f));return
        b=f.read_bytes();mime=mimetypes.guess_type(f.name)[0] or 'application/octet-stream'
        if f==SITE/'data.json':
            d=json.loads(b);d['lock'][TEAM]=h32(TEAM+'|'+CODE);b=json.dumps(d).encode()
        rg=r.request.headers.get('range')
        if rg and f.suffix in ('.mp4','.mp3'):
            m=re.fullmatch(r'bytes=(\d+)-(\d*)',rg)
            if m:
                start=int(m[1]);end=min(int(m[2]) if m[2] else len(b)-1,len(b)-1);r.fulfill(status=206,content_type=mime,headers={'Content-Range':f'bytes {start}-{end}/{len(b)}','Accept-Ranges':'bytes'},body=b[start:end+1]);return
        r.fulfill(status=200,content_type=mime,body=b)
    c.route(re.compile(r'^http://127\.0\.0\.1:876[56]/.*'),local)
    live={'value':json.loads((ROOT/'ramificazioni-dati.json').read_text()),'fail':False}
    def graph(r):r.fulfill(status=503 if live['fail'] else 200,content_type='application/json',body=json.dumps(live['value']))
    c.route('https://raw.githubusercontent.com/giandjcosta/o-girrr-registro/chatgpt/dati-ramificazioni/**',graph)
    c.add_init_script("localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'solo-browser'}))")
    return live


def main():
    report={'motori':{},'visite':0,'problemi':[],'interazioni':[],'browser_fisici':'Non disponibili: Samsung Internet, Safari su dispositivo, Chrome/Edge di marca. Schermi e identità emulati.'}
    with sync_playwright() as p:
        screens=[('iPhone320',dict(p.devices['iPhone SE'],viewport={'width':320,'height':568}))]+[(n,p.devices[n]) for n in ['iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape']]+[(f'PC{w}',{'viewport':{'width':w,'height':900}}) for w in [1280,1920,2560]]+[('TV',{'viewport':{'width':1920,'height':1080},'device_scale_factor':2,'user_agent':'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36'})]
        if os.environ.get('SCHERMI'):screens=[s for s in screens if s[0] in os.environ['SCHERMI'].split(',')]
        report['profili']=len(screens)
        for engine in os.environ.get('MOTORI','chromium,webkit,firefox').split(','):
            opts={'executable_path':os.environ['WEBKIT_PATH']} if engine=='webkit' and os.environ.get('WEBKIT_PATH') else {}
            b=getattr(p,engine).launch(**opts);report['motori'][engine]=b.version
            for screen,options in screens:
                options=dict(options);options.pop('default_browser_type',None)
                if engine=='firefox':options.pop('is_mobile',None)
                db=Database();c=b.new_context(**options,service_workers='block');live=routes(c,db);page=c.new_page();page.set_default_timeout(12000);errors=[];bad=[]
                page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append(str(r.status)+' '+r.url) if r.status>=400 else None)
                for skin,folder in [('lega','girrr/'),('stadio','stadio/girrr/')]:
                    for slug,path,target in [('home','','#pt-home-story'),('mvp','app.html?sezione=mvp#sport','#pt-mvp'),('carriera','app.html?sezione=settimana#carriera','#pt-storia'),('derby','derby.html','#pt-derby'),('curva','curva.html#pt-mvp','#pt-mvp'),('archivio','albo.html#pt-archivio','#pt-archivio'),('video','app.html#video','.vid-i'),('giornale','giornale.html','button.cd-btn'),('tabellone','tabellone.html','body')]:
                        errors.clear();bad.clear()
                        try:
                            page.goto(BASE+folder+path,wait_until='load');page.locator(target).first.wait_for(state='visible');page.evaluate('document.fonts.ready');page.wait_for_load_state('networkidle')
                            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Scorrimento orizzontale'
                            assert not errors and not bad,{'js':errors,'http':bad}
                            if screen=='TV':assert 'tv-grande' in (page.locator('html').get_attribute('class') or ''),'Modalità TV non attiva'
                            if slug=='video':expect(page.locator('.vid-i')).to_have_count(7)
                            if slug=='curva':
                                ua=options.get('user_agent','');expected='ios' if any(n in ua for n in ['iPhone','iPad']) else 'android' if 'Android' in ua else 'altro'
                                assert page.locator('html').get_attribute('data-os')==expected,'Stile Curva non coerente con il sistema'
                            if slug=='giornale':expect(page.locator('button.cd-btn')).to_have_count(2)
                            if slug=='home':
                                page.locator('#big .cd-gio').click();expect(page.locator('.cd-pz')).to_have_count(5);page.wait_for_function("()=>{const b=document.querySelector('.cd-box');return b&&getComputedStyle(b).transform==='none'}");page.wait_for_timeout(400)
                                assert page.locator('.cd-box').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1'),'Condividi: scorrimento orizzontale'
                                assert page.locator('.cd-az.fis').evaluate('(e)=>{let r=e.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight+1}'),'Condividi: azioni fuori schermo'
                                page.keyboard.press('Escape')
                            if slug=='mvp':expect(page.locator('[data-pt-vote]')).to_have_count(3)
                            if slug=='carriera':expect(page.locator('[data-pt-day]')).to_have_count(7);expect(page.locator('#view>.card:visible')).to_have_count(0)
                            if engine=='chromium' and screen in ['PC1920','TV'] and slug in ['mvp','carriera','derby']:
                                page.locator(target).scroll_into_view_if_needed();page.wait_for_timeout(450);page.screenshot(path=str(OUT/f'{skin}-{slug}-{screen}.png'))
                            report['visite']+=1
                        except Exception as e:report['problemi'].append(f'{engine}/{screen}/{skin}/{slug}: {e}'[:1200]);print(report['problemi'][-1],flush=True)
                try:
                    errors.clear();bad.clear();page.goto(REG+'ramificazioni.html',wait_until='load');expect(page.locator('.repo')).to_have_count(2);expect(page.locator('#repositories svg')).to_have_count(2)
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Mappa fuori schermo'
                    assert not errors and not bad,{'js':errors,'http':bad}
                    if engine=='chromium' and screen in ['PC1920','TV']:
                        page.screenshot(path=str(OUT/f'ramificazioni-{screen}.png'))
                    report['visite']+=1
                except Exception as e:report['problemi'].append(f'{engine}/{screen}/Ramificazioni: {e}'[:1200]);print(report['problemi'][-1],flush=True)
                c.close();print(engine,screen,'Visite',report['visite'],'Problemi',len(report['problemi']),flush=True)
            c=b.new_context(viewport={'width':390,'height':844},service_workers='block');db=Database();live=routes(c,db);page=c.new_page();page.set_default_timeout(12000)
            for folder in ['girrr/','stadio/girrr/']:
                try:
                    page.goto(BASE+folder+'app.html?sezione=mvp#sport',wait_until='load');expect(page.locator('[data-pt-vote]')).to_have_count(3)
                    page.locator('[data-pt-vote]').first.click();expect(page.locator('[data-pt-withdraw]')).to_be_visible();assert len(db.votes)==1
                    page.reload(wait_until='load');expect(page.locator('[data-pt-withdraw]')).to_be_visible()
                    page.locator('[data-pt-vote][aria-pressed=false]').first.click();expect(page.locator('[data-pt-vote][aria-pressed=true]')).to_have_count(1)
                    page.locator('[data-pt-withdraw]').click();expect(page.locator('[data-pt-vote][aria-pressed=true]')).to_have_count(0);assert not db.votes
                    db.fail=True;page.locator('[data-pt-vote]').first.click();expect(page.locator('#pt-mvp [role=status]')).to_contain_text('non è stato confermato');assert not db.votes;db.fail=False
                    page.locator('[data-sp=video]').click();expect(page.locator('.vid-i')).to_have_count(7);expect(page.locator('#pt-mvp')).to_have_count(0)
                    page.locator('[data-pt-sport]').click();page.locator('#pt-mvp').wait_for(state='visible')
                    page.goto(BASE+folder+'app.html?sezione=settimana#carriera',wait_until='load');expect(page.locator('[data-pt-day="7"]')).to_contain_text('2 incontri giocati')
                    page.locator('[data-ctab=pan]').first.click();expect(page.locator('#pt-storia')).to_have_count(0);page.locator('[data-pt-week]').click();page.locator('#pt-storia').wait_for(state='visible')
                    page.goto(BASE+folder+'albo.html',wait_until='load');page.locator('[data-at=derby]').click();page.locator('#pt-derby-access').click();page.locator('#pt-derby').wait_for(state='visible');page.locator('[data-pt-comp=cup]').click();expect(page.locator('#pt-derby tbody tr')).to_have_count(4)
                    assert page.evaluate("JSON.parse(localStorage.getItem('fg')).code") == CODE
                    report['interazioni'].append(engine+'/'+folder+': PASS · Voto/cambio/ritiro/persistenza/errore, Video conservato, Carriera e Derby nei menu, identità intatta')
                except Exception as e:report['problemi'].append(engine+'/'+folder+'/Interazioni: '+str(e)[:1200]);print(report['problemi'][-1],flush=True)
            try:
                page.goto(REG+'ramificazioni.html');expect(page.locator('.repo')).to_have_count(2);page.locator('#repo-filter').select_option('registro');expect(page.locator('[data-repository=sito]')).to_be_hidden()
                page.locator('#branch-search').fill('versione-6-0');branch=page.locator('[data-repository=registro] .branch:visible [data-branch]').first;branch.click();expect(page.locator('[data-detail=registro]')).to_contain_text('Preparazione della 6.0')
                node=page.locator('[data-repository=registro] [data-node]').first;node.focus();node.press('Enter');expect(page.locator('[data-detail=registro]')).to_contain_text('Commit Git')
                svg=page.locator('[data-repository=registro] svg');old=svg.bounding_box()['width'];page.locator('[data-repository=registro] [data-zoom="+"]').click();assert svg.bounding_box()['width']>old
                live['fail']=True;page.locator('#refresh').click();expect(page.locator('#update-status')).to_contain_text('ultima copia');expect(page.locator('.repo')).to_have_count(2)
                live['fail']=False;live['value']['fingerprint']='simulazione-aggiornamento';live['value']['repositories'][1]['version']='6.1';page.locator('#refresh').click();expect(page.locator('[data-repository=registro]')).to_contain_text('6.1')
                report['interazioni'].append(engine+'/Ramificazioni: PASS · Filtri, ramo/dettaglio, tastiera, zoom, errore di rete, nuova versione senza ricaricare')
            except Exception as e:report['problemi'].append(engine+'/Ramificazioni/Interazioni: '+str(e)[:1200]);print(report['problemi'][-1],flush=True)
            c.close();b.close()
    (OUT/'collaudo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(report['problemi']))


if __name__=='__main__':main()
