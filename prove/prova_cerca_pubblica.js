// Forza Cerca a montarsi dopo il render: nessuna quarta scheda pubblica per errore.
const assert=require('assert/strict'),{browser}=require('./browser_certificato'),{script}=require('./blocca_scritture');
const M=process.env.MOTORE||'chromium',B=process.env.BASE||'http://127.0.0.1:8890/o-fant-a-girrr/';
(async()=>{const b=await browser(M);let n=0;
 for(const width of [320,768,1920])for(const chi of ['ospite','anonimo','squadra']){
  const c=await b.newContext({viewport:{width,height:900},serviceWorkers:'block'});await c.addInitScript(script);
  if(chi==='ospite')await c.addInitScript(()=>sessionStorage.setItem('ospite','1'));
  if(chi==='squadra'){
   await c.addInitScript(()=>localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'PROVA'})));
   await c.route(/\/index\.html$/,async rt=>{const r=await rt.fetch(),t=await r.text();assert(t.includes('function authed(){'));await rt.fulfill({response:r,body:t.replace('function authed(){','function authed(){return true;')});});
  }
  await c.route('**/cerca.js',async rt=>{await new Promise(r=>setTimeout(r,600));await rt.continue();});
  const p=await c.newPage();await p.goto(B+'index.html');await p.waitForSelector('#tabs [data-t=cerca]',{state:'attached'});
  assert.equal(await p.locator('#tabs [data-t=cerca]').isVisible(),chi==='squadra');
  const vis=await p.locator('#tabs button').evaluateAll(es=>es.filter(e=>!e.hidden&&e.offsetParent).map(e=>e.dataset.t));
  if(chi!=='squadra')assert.deepEqual(vis,chi==='ospite'?['fa','inj','lega']:['entra','fa','inj','lega']);
  else assert(vis.includes('rosa')&&vis.includes('cerca'));
  await p.click('#tabs [data-t=inj]');assert.equal(await p.locator('#tabs [data-t=cerca]').isVisible(),chi==='squadra');
  await c.close();n++;
 }
 await b.close();console.log(M+': '+n+' casi, 0 problemi');
})().catch(e=>{console.error(e);process.exitCode=1;});
