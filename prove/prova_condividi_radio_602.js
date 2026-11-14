// Radio 6.0.2: centratura rispetto al lettore e condivisione simulata, senza invii o scritture reali.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{devices}=require('playwright'),{browser}=require('./browser_certificato'),{script}=require('./blocca_scritture');
const M=process.env.MOTORE||'chromium',B=process.env.BASE||'http://127.0.0.1:8890/o-fant-a-girrr/',F=process.env.FOTO||'/tmp/radio-602';
const schermi=[['iPhone320',{...devices['iPhone SE'],viewport:{width:320,height:568}}],...['iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape'].map(n=>[n,devices[n]]),...[1280,1920,2560].map(w=>['PC'+w,{viewport:{width:w,height:1080}}]),['TV',{viewport:{width:1920,height:1080},deviceScaleFactor:2,userAgent:'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36'}]];
(async()=>{const b=await browser(M),record=[];fs.mkdirSync(F,{recursive:true});
 for(const [nome,o] of schermi){const c=await b.newContext({...o,serviceWorkers:'block'});await c.addInitScript(script);await c.addInitScript(()=>{sessionStorage.setItem('ospite','1');navigator.canShare=()=>true;window.__radioInvii=[];navigator.share=d=>{__radioInvii.push({files:d.files.map(f=>({name:f.name,type:f.type})),text:d.text,url:d.url});return Promise.resolve();};});
 await c.route('https://*.supabase.co/**',r=>r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:'{"votazione":null,"archivio":[],"coppie":[],"voti":[],"sfide":[]}'}));
 await c.route('**/voci/*.mp3',r=>r.fulfill({status:200,contentType:'audio/mpeg',body:Buffer.from('ID3-riferimento-di-prova')}));
 for(const skin of ['girrr/','stadio/girrr/']){const p=await c.newPage(),errori=[];const errore=e=>errori.push(e.message);p.on('pageerror',errore);
 try{await p.goto(B+skin+'app.html#radio',{waitUntil:'domcontentloaded'});await p.waitForSelector('button[data-cd-nome^="radio-"]');await p.evaluate(()=>document.fonts.ready);
 const misure=await p.locator('button[data-cd-nome^="radio-"]').evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect(),a=e.parentElement.querySelector('audio').getBoundingClientRect();const range=document.createRange();range.selectNodeContents(e);const t=range.getBoundingClientRect();return {scarto:Math.abs(r.x+r.width/2-a.x-a.width/2),testo:Math.abs(t.x+t.width/2-r.x-r.width/2),altezza:r.height,nelLettore:r.left>=a.left-1&&r.right<=a.right+1};}));
 assert(misure.length>0);assert(misure.every(m=>m.scarto<1.1&&m.testo<1.1&&m.altezza>=43&&m.nelLettore),'Pulsante decentrato: '+JSON.stringify(misure));assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 if(M==='chromium'&&['PC1920','TV'].includes(nome)){await p.locator('button[data-cd-nome^="radio-"]').first().scrollIntoViewIfNeeded();await p.waitForTimeout(350);await p.screenshot({path:path.join(F,'radio-'+nome+'-'+(skin[0]==='s'?'stadio':'lega')+'.jpg'),quality:85});}
 if(nome==='iPhone320'){
  await p.locator('button[data-cd-nome^="radio-"]').first().click();await p.waitForSelector('.cd-box [data-a=sh]');await p.waitForTimeout(350);
  assert(await p.locator('.cd-az').evaluate(e=>{const r=e.getBoundingClientRect(),a=[...e.children].map(v=>v.getBoundingClientRect());return Math.abs((a[0].left+a.at(-1).right)/2-r.x-r.width/2)<1.1;}),'Comandi della finestra decentrati');
  await p.locator('.cd-box [data-a=sh]').click();const inv=await p.evaluate(()=>__radioInvii.at(-1));assert.equal(inv.files.length,1);assert.equal(inv.files[0].type,'audio/mpeg');assert.match(inv.files[0].name,/^radio-girrr-\d+\.mp3$/);assert.equal(inv.text,undefined);assert.equal(inv.url,undefined);await p.locator('.cd-box [data-a=x]').click();
 }
 assert.deepEqual(errori,[]);record.push({schermo:nome,grafica:skin,puntate:misure.length,scarto_massimo:Math.max(...misure.map(m=>m.scarto)),problemi:[]});console.log('OK '+M+' '+nome+' '+skin);
 }catch(e){record.push({schermo:nome,grafica:skin,problemi:[e.message,...errori]});console.log('KO '+M+' '+nome+' '+skin+': '+e.message);}p.off('pageerror',errore);await p.close();}
 await c.close();}
 await b.close();const problemi=record.filter(r=>r.problemi.length).length;fs.writeFileSync(path.join(F,'radio-'+M+'.json'),JSON.stringify({motore:M,visite:record.length,problemi,record},null,2));console.log(M+': '+problemi+' problemi');process.exitCode=problemi?1:0;
})().catch(e=>{console.error(e);process.exitCode=1});
