// 6.5 nel Lab: pagine principali su tutti gli schermi, con e senza tema. Controlla errori nuovi e scorrimento laterale.
const {chromium,devices}=require('playwright');
const B='http://localhost:8767/lab/integrata-62/';
const PROF=[['iPhone SE',{...devices['iPhone SE']}],['iPhone 13',{...devices['iPhone 13']}],['Pixel 7',{...devices['Pixel 7']}],['Galaxy S9+',{...devices['Galaxy S9+']}],
 ['iPad verticale',{...devices['iPad (gen 7)']}],['iPad orizzontale',{...devices['iPad (gen 7) landscape']}],['Galaxy Tab',{...devices['Galaxy Tab S4']}],
 ['PC 1280',{viewport:{width:1280,height:800}}],['PC 1920',{viewport:{width:1920,height:1080}}],['Monitor 2560',{viewport:{width:2560,height:1440}}],['TV',{viewport:{width:1920,height:1080},deviceScaleFactor:2}]];
const PAG=['girrr/index.html?squadra=Oranje%20VC','girrr/tabellone.html?x=1','girrr/campo.html?x=1','girrr/app.html?squadra=Oranje%20VC#carriera','girrr/app.html?squadra=Oranje%20VC#sport','girrr/totogirrr.html?x=1','girrr/albo.html?x=1','stadio/girrr/index.html?x=1'];
(async()=>{const b=await chromium.launch();let prob=0,tot=0;
for(const [nome,o] of PROF){const c=await b.newContext(o);const p=await c.newPage();const er=[];p.on('pageerror',e=>er.push(e.message));
 for(const pg of PAG)for(const tema of ['off','notte-tropicale']){
  const [base,hash]=pg.split('#');const url=B+base+'&evento='+tema+(hash?'#'+hash:'');er.length=0;tot++;
  await p.goto(url,{waitUntil:'networkidle'}).catch(()=>{});await p.waitForTimeout(1200);
  const sx=await p.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth).catch(()=>-1);
  const e2=er.filter(e=>!/ViewTransition/.test(e));
  if(sx>0||e2.length){prob++;console.log('PROBLEMA',nome,pg,tema,'sx='+sx,e2.join(' | ').slice(0,160))}}
 await c.close()}
console.log('controlli',tot,'problemi',prob);await b.close()})();
