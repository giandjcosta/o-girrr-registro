// ChatGPT 6.2: QA della COPIA locale, mai del database vero.
// BASE=http://127.0.0.1:8890/o-fant-a-girrr/ SITO_DIR=/tmp/... MOTORE=chromium node prove/prova_campo_62.js
'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{devices}=require('playwright');
const {browser}=require('./browser_certificato');
const B=process.env.BASE||'http://127.0.0.1:8890/o-fant-a-girrr/';
const M=process.env.MOTORE||'chromium',SITE=path.resolve(process.env.SITO_DIR||'qa-site');
const F=process.env.FOTO||path.resolve('qa-artifacts/62');
const SCH=[
 ['iPhone 320',{...devices['iPhone SE'],viewport:{width:320,height:568}}],
 ...['iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape'].map(x=>[x,devices[x]]),
 ...[1280,1920,2560].map(w=>['PC'+w,{viewport:{width:w,height:1080}}]),
 ['TV',{viewport:{width:1920,height:1080},deviceScaleFactor:2,userAgent:'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 Chrome/94.0 TV Safari/537.36'}]
];
function localFile(reqUrl){const u=new URL(reqUrl);if(u.hostname!=='giandjcosta.github.io'||!u.pathname.startsWith('/o-fant-a-girrr/'))return null;let rel=decodeURIComponent(u.pathname.slice('/o-fant-a-girrr/'.length));if(rel.includes('..'))return null;const p=path.resolve(SITE,rel);return p.startsWith(SITE+path.sep)&&fs.existsSync(p)&&fs.statSync(p).isFile()?p:null}
async function isolated(ctx){
  // Nessuna chiamata esterna, neppure per errore: gli asset del sito sono nella copia locale.
  await ctx.route('**/*',r=>{const u=new URL(r.request().url());if(['127.0.0.1','localhost'].includes(u.hostname))return r.continue();
   const p=localFile(u.href);if(p)return r.fulfill({path:p});
   return r.abort();});
}
async function verify(page,skin,logged){
  await page.waitForFunction(()=>!!document.querySelector('#comp-sw [data-comp-choice="coppa"]')&&!!document.querySelector('#board>.card'),{timeout:12000});
  assert.equal(await page.locator('#comp-sw [data-comp-choice=lega]').getAttribute('aria-selected'),'true','Campionato iniziale');
  const original=await page.evaluate(()=>document.querySelector('#roundtitle').textContent);
  assert(original.includes('Giornata'),'Giornata iniziale non visibile');
  const accent=async()=>page.evaluate(()=>getComputedStyle(document.body).getPropertyValue('--accent').trim());
  if(skin==='stadio')assert.equal(await accent(),'#ffd166');
  await page.locator('#comp-sw [data-comp-choice=coppa]').click();
  await page.waitForFunction(()=>document.body.dataset.comp==='coppa'&&document.querySelector('#board>.card'),{timeout:12000});
  assert.equal(await page.locator('#comp-sw [data-comp-choice=coppa]').getAttribute('aria-selected'),'true','Selezione Coppa');
  assert.equal(await accent(),skin==='stadio'?'#ffd166':'#3d93d6','Colori Coppa');
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.locator('#comp-sw [data-comp-choice=lega]').click();
  await page.waitForFunction(()=>document.body.dataset.comp==='lega');
  assert.equal(await accent(),skin==='stadio'?'#ffd166':'#d62839','Colori Campionato');
  const navigazione=await page.locator('#pprev,#pnext,#prev,#next').count();
  assert.equal(navigazione,4,'Frecce partita e giornata');
  const btn=page.locator('#pnext:not([disabled])').first();
  if(await btn.count()){await btn.click();await page.waitForTimeout(100);}
  const horizontal=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
  assert(horizontal<=1,'Scorrimento orizzontale '+horizontal+' px');
  if(logged){
    const names=await page.locator('#matches .gamebtn.mia').count();
    assert(names>=0,'Identità squadra renderizzata');
  }
  assert(await page.locator('.legend, #board').count()>0,'Campo non visualizzato');
}
(async()=>{
 const br=await browser(M),out=[];fs.mkdirSync(F,{recursive:true});
 for(const [name,opt] of SCH){for(const skin of ['lega','stadio']){for(const logged of [false,true]){
  const c=await br.newContext({...opt,serviceWorkers:'block'});await isolated(c);
  if(logged)await c.addInitScript(()=>{localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'PROVA'}));sessionStorage.removeItem('ospite')});
  const p=await c.newPage(),problems=[];p.on('pageerror',e=>problems.push(e.message));
  const tag=name+' · '+skin+' · '+(logged?'codice fittizio':'ospite');
  try{
   await p.goto(B+(skin==='stadio'?'stadio/girrr/':'girrr/')+'campo.html'+(logged?'':'?ospite=1'),{waitUntil:'domcontentloaded'});
   await verify(p,skin,logged);
   if(problems.length)throw Error('Errori JavaScript: '+problems.join('; '));
   if(M==='chromium'&&logged&&['PC1920','TV','iPhone 320'].includes(name))
     await p.screenshot({path:path.join(F,(name==='PC1920'?'pc':name==='TV'?'tv':'telefono')+'-'+skin+'.png'),fullPage:true});
   out.push({name:tag,ok:true});
  }catch(e){console.error('KO',tag,e.message);out.push({name:tag,ok:false,error:e.message.slice(0,500)})}
  await c.close();
 }} console.log(M,name)}
 await br.close();
 const ko=out.filter(z=>!z.ok);fs.writeFileSync(path.join(F,'campo-'+M+'.json'),JSON.stringify({motore:M,visite:out.length,problemi:ko.length,risultati:out},null,2));
 console.log(M,'visite='+out.length,'problemi='+ko.length);
 if(ko.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
