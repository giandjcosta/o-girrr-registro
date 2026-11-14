// Identità Tizen e schermo TV emulati; non equivale a Samsung Internet su dispositivo.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{browser}=require('./browser_certificato'),{script}=require('./blocca_scritture');
const M=process.env.MOTORE||'chromium',B=process.env.BASE||'http://127.0.0.1:8890/o-fant-a-girrr/';
(async()=>{const br=await browser(M);for(const skin of ['girrr/','stadio/girrr/']){
 const c=await br.newContext({viewport:{width:1920,height:1080},deviceScaleFactor:2,userAgent:'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36',serviceWorkers:'block'});await c.addInitScript(script);
 await c.route('https://*.supabase.co/**',r=>r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:'{"votazione":null,"archivio":[],"coppie":[],"voti":[],"sfide":[]}'}));
 const p=await c.newPage();await p.goto(B+skin+'app.html?boa=1#carriera');await p.waitForSelector('[data-pronto="1"]');await p.waitForLoadState('networkidle');
 assert(await p.locator('html').evaluate(e=>e.classList.contains('tv-grande')));assert.equal(await p.locator('html').evaluate(e=>getComputedStyle(e).zoom),'1.3');
 await p.selectOption('[data-gb-squadra]','Oranje VC');assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 if(M==='chromium'&&process.env.FOTO){fs.mkdirSync(process.env.FOTO,{recursive:true});await p.screenshot({path:path.join(process.env.FOTO,`tv-${skin[0]==='s'?'stadio':'lega'}.jpg`),quality:85});}
 await p.click('[data-gb-album]');await p.waitForFunction(()=>document.querySelectorAll('.gb-album img').length===3);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 if(M==='chromium'&&process.env.FOTO)await p.screenshot({path:path.join(process.env.FOTO,`tv-${skin[0]==='s'?'stadio':'lega'}-album.jpg`),quality:85});await c.close();
}await br.close();console.log(M+': TV emulata, Lega e Stadio, 0 problemi');})().catch(e=>{console.error(e);process.exitCode=1;});
