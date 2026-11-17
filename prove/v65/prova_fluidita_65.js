// Dettaglio: Conferenze stampa (salto) e opacità solo dei blocchi grandi e visibili, con il valore di partenza.
const {chromium,devices}=require('playwright');
const SITI={vero:'https://giandjcosta.github.io/o-fant-a-girrr/girrr/app.html?ospite=1',lab:'http://localhost:8767/lab/integrata-62/girrr/app.html?ospite=1&evento=off'};
(async()=>{const b=await chromium.launch();
for(const [nome,base] of Object.entries(SITI)){
 const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();
 await p.goto(base+'#sport',{waitUntil:'networkidle'});await p.waitForTimeout(2500);
 await p.evaluate(()=>scrollTo(0,160));await p.waitForTimeout(600);
 for(const v of ['Squadra della settimana','Conferenze stampa','Sondaggi']){
  await p.evaluate(()=>{window.__l=[];const t0=performance.now();(function f(){const vw=document.querySelector('#view');let mo=1;[].forEach.call(vw.querySelectorAll(':scope > *, :scope > * > *'),k=>{if(k.offsetHeight<40||k.getBoundingClientRect().bottom<0||k.getBoundingClientRect().top>innerHeight)return;const o=parseFloat(getComputedStyle(k).opacity);if(o<mo)mo=o});window.__l.push([Math.round(performance.now()-t0),Math.round(scrollY),document.documentElement.scrollHeight,+mo.toFixed(2),document.activeElement&&document.activeElement.tagName]);if(performance.now()-t0<1100)requestAnimationFrame(f)})()});
  await p.locator('.seg:visible button',{hasText:v}).first().scrollIntoViewIfNeeded().catch(()=>{});
  await p.evaluate(()=>{const r=[...document.querySelectorAll('.seg')].find(x=>x.offsetHeight);});
  const bb=await p.locator('.seg:visible button',{hasText:v}).first().boundingBox();
  await p.touchscreen.tap(bb.x+bb.width/2,bb.y+bb.height/2);await p.waitForTimeout(1250);
  const l=await p.evaluate(()=>window.__l);
  const camb=l.filter((z,i)=>i===0||z[1]!==l[i-1][1]||z[3]!==l[i-1][3]||z[2]!==l[i-1][2]).slice(0,14).map(z=>z.join('/'));
  console.log(nome,v,'(t/scrollY/altezza/opacità/fuoco):',camb.join('  '));
  await p.evaluate(()=>scrollTo(0,160));await p.waitForTimeout(500);
 }
 await c.close()}
await b.close()})();
