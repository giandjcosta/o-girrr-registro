// Foto esportate dall'interfaccia reale del Lab, senza condividere verso applicazioni esterne.
const fs=require('fs'),path=require('path'),{chromium}=require('playwright');
const OUT=process.argv[2]||'lab/giro-di-boa-602/foto';
(async()=>{fs.mkdirSync(OUT,{recursive:true});const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
 await p.goto((process.env.REGISTRO||'http://127.0.0.1:8890/o-girrr-registro/')+'lab/giro-di-boa-602/');await p.waitForSelector('[data-pronto="1"]');
 for(const skin of ['lega','stadio']){
  await p.evaluate(s=>document.documentElement.dataset.skin=s,skin);
  for(const comp of ['campionato','coppa','entrambe'])for(const ambito of ['squadra','lega']){
   await p.selectOption('[data-gb-comp]',comp);
   await p.selectOption('[data-gb-ambito]','squadra');await p.selectOption('[data-gb-squadra]','Oranje VC');await p.selectOption('[data-gb-ambito]',ambito);await p.click('[data-gb-album]');
   await p.waitForFunction(n=>document.querySelectorAll('.gb-album img').length===n&&[...document.querySelectorAll('.gb-album img')].every(i=>i.complete),comp==='entrambe'?3:2);
   const encoded=await p.locator('.gb-album img').evaluateAll(es=>es.map(e=>{const c=document.createElement('canvas');c.width=e.naturalWidth;c.height=e.naturalHeight;c.getContext('2d').drawImage(e,0,0);return c.toDataURL('image/jpeg',0.92).split(',')[1];}));
   for(let i=0;i<encoded.length;i++)fs.writeFileSync(path.join(OUT,`${comp==='campionato'?'':comp+'-'}${ambito}-${skin}-${i+1}.jpg`),Buffer.from(encoded[i],'base64'));
   await p.screenshot({path:path.join(OUT,`pc-${comp==='campionato'?'':comp+'-'}${ambito}-${skin}.jpg`),quality:85});
   if(comp==='entrambe'&&ambito==='lega'){await p.setViewportSize({width:1920,height:1080});await p.evaluate(()=>document.documentElement.style.zoom='1.3');await p.screenshot({path:path.join(OUT,`tv-entrambe-${skin}.jpg`),quality:85});await p.evaluate(()=>document.documentElement.style.zoom='');}
   await p.keyboard.press('Escape');await p.waitForFunction(()=>!document.querySelector('.gb-dialogo'));
  }
 }
 await b.close();console.log('Foto reali salvate:',OUT);
})().catch(e=>{console.error(e);process.exitCode=1});
