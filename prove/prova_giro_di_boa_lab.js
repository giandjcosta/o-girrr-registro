// Lab navigabile, specchio con service worker e riapertura senza rete. Nessuna voce generata.
const assert=require('assert/strict'),{browser}=require('./browser_certificato'),{script}=require('./blocca_scritture');
const M=process.env.MOTORE||'chromium',B=process.env.REGISTRO||'http://127.0.0.1:8890/o-girrr-registro/';
(async()=>{const b=await browser(M);let n=0;const errori=[];
 for(const width of [320,1920]){
  const c=await b.newContext({viewport:{width,height:1080}});await c.addInitScript(script);
  await c.addInitScript(()=>sessionStorage.setItem('ospite','1'));
  const p=await c.newPage();p.on('pageerror',e=>errori.push(e.message));
  await p.goto(B+'lab/giro-di-boa-602/');await p.waitForSelector('[data-pronto="1"]');
  assert.match(await p.locator('[data-gb-tit]').textContent(),/7ª/);await p.click('#grafica');assert.equal(await p.locator('html').getAttribute('data-skin'),'stadio');
  await p.click('[data-gb-album]');await p.waitForFunction(()=>document.querySelectorAll('.gb-album img').length===3);await p.keyboard.press('Escape');
  for(const skin of ['girrr/','stadio/girrr/']){
   await p.goto(B+'lab/offline/?apri='+encodeURIComponent('sito/'+skin+'app.html?boa=1')+'#carriera');
   await p.waitForSelector('[data-pronto="1"]',{timeout:45000});assert.match(p.url(),/offline\/sito\//);
   assert.match(await p.locator('[data-gb-contenuto]').textContent(),/MVP dei tifosi/);
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   await p.waitForLoadState('networkidle');
   await p.waitForFunction(async()=>{const files=(await Promise.all((await caches.keys()).map(async k=>(await(await caches.open(k)).keys()).map(r=>r.url)))).flat();return ['giro-di-boa.js','giro-di-boa.css','giro-di-boa.json','app.html'].every(x=>files.some(u=>u.split('?')[0].endsWith(x)));},{},{timeout:30000});
   await c.setOffline(true);await p.reload({waitUntil:'domcontentloaded'});await p.waitForSelector('[data-pronto="1"]',{timeout:45000});
   await p.click('[data-gb-album]');await p.waitForFunction(()=>document.querySelectorAll('.gb-album img').length===3);
   await p.keyboard.press('Escape');await c.setOffline(false);n++;
  }
  await c.close();
 }
 await b.close();console.log(JSON.stringify({motore:M,casi:n,errori}));if(errori.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
