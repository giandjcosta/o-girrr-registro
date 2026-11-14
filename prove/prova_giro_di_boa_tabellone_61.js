// Il bilancio aperto dal Tabellone conserva la competizione vista, anche per l'ospite.
const assert=require('assert/strict'),{browser}=require('./browser_certificato'),{script}=require('./blocca_scritture');
const B=process.env.BASE||'http://127.0.0.1:8890/o-fant-a-girrr/',M=process.env.MOTORE||'chromium';
(async()=>{const b=await browser(M);for(const skin of ['girrr/','stadio/girrr/'])for(const comp of ['campionato','coppa']){
 const c=await b.newContext({viewport:{width:1280,height:800},serviceWorkers:'block'});await c.addInitScript(script);await c.addInitScript(()=>sessionStorage.setItem('ospite','1'));
 await c.route('https://*.supabase.co/**',r=>r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:'{"votazione":null,"archivio":[],"coppie":[],"voti":[],"sfide":[]}'}));
 const p=await c.newPage(),err=[];p.on('pageerror',e=>err.push(e.message));await p.goto(B+skin+'tabellone.html');
 if(comp==='coppa')await p.locator('[data-m="coppa"], .sw button').last().click();await p.click('button.cd-btn');await p.waitForSelector('.cd-sq select');await p.selectOption('.cd-sq select','Oranje VC');await p.click('[data-t=girone]');
 await p.waitForFunction(()=>document.querySelectorAll('.gb-album img').length===2&&[...document.querySelectorAll('.gb-album img')].every(i=>i.complete&&i.naturalWidth));
 assert.equal(await p.locator('[data-gb-c]').inputValue(),comp);assert.equal(await p.locator('[data-gb-k]').inputValue(),'finora');assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));assert.deepEqual(err,[]);
 await c.close();console.log('OK '+M+' '+skin+' '+comp);
}await b.close();})().catch(e=>{console.error(e);process.exitCode=1});
