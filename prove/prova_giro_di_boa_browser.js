// Matrice reale 16 schermi × Chromium/WebKit/Firefox. Solo copie locali.
// Le letture DB delle funzioni preesistenti sono fixture; il bilancio è quello reale generato dal calcolo.
// BASE=... MOTORE=... FIREFOX_CERT_PROFILE=... FOTO=... node prove/prova_giro_di_boa_browser.js
const fs=require('fs'),path=require('path'),os=require('os'),assert=require('assert/strict'),{devices}=require('playwright');
const {browser}=require('./browser_certificato'),{script:BLOCCA}=require('./blocca_scritture');
const B=process.env.BASE||'http://127.0.0.1:8890/o-fant-a-girrr/',M=process.env.MOTORE||'chromium',F=process.env.FOTO||'/tmp/boa-foto';
const SCH=[
 ['iPhone SE 320',{...devices['iPhone SE'],viewport:{width:320,height:568}}],['iPhone SE',devices['iPhone SE']],
 ['iPhone 15 Pro',devices['iPhone 15 Pro']],['iPhone 15 Pro Max',devices['iPhone 15 Pro Max']],
 ['Galaxy S8',devices['Galaxy S8']],['Pixel 7',devices['Pixel 7']],['Galaxy S24',devices['Galaxy S24']||devices['Galaxy S9+']],
 ['iPad Mini',devices['iPad Mini']],['iPad 7 orizzontale',devices['iPad (gen 7) landscape']],['iPad Pro 11',devices['iPad Pro 11']],
 ['Galaxy Tab S4',devices['Galaxy Tab S4']],['Galaxy Tab S4 orizzontale',devices['Galaxy Tab S4 landscape']],
 ['PC 1280',{viewport:{width:1280,height:800}}],['PC 1920',{viewport:{width:1920,height:1080}}],
 ['Monitor 2560',{viewport:{width:2560,height:1440}}],['Smart TV 4K',{viewport:{width:1920,height:1080},deviceScaleFactor:2}]
];
const record=[];let ko=0;
const FIXTURE=fs.mkdtempSync(path.join(os.tmpdir(),'girrr-boa-fixture-'));
require('child_process').execFileSync('python3',[path.join(__dirname,'fixture_giro_di_boa.py'),FIXTURE]);
async function rete(c){
 await c.addInitScript(BLOCCA);
 await c.route('https://*.supabase.co/**',r=>{
   const fn=(r.request().url().match(/rpc\/([^?]+)/)||[])[1];
   if(!fn||!/(?:_stato|_pubblico|_lista)$/.test(fn)&&!['mvp_derby','mvp_mio'].includes(fn))throw new Error('RPC non di lettura nella prova: '+fn);
   // mvp_mio verifica il codice e legge scelta; non esprime un voto.
   return r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:JSON.stringify(fn==='mvp_stato'?{votazione:null,archivio:[]}:fn==='mvp_mio'?{scelta:null}:{voti:[],sfide:[],coppie:[]})});
 });
 await c.addInitScript(()=>{window.__albumInviati=[];navigator.canShare=()=>true;navigator.share=x=>{window.__albumInviati.push({keys:Object.keys(x),files:x.files.map(f=>({nome:f.name,tipo:f.type,byte:f.size}))});return Promise.resolve();};});
}
async function noLato(p){assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'La pagina scorre di lato');}
async function invia(p){
 await p.waitForFunction(()=>document.querySelectorAll('.gb-album img').length===2);
 await p.waitForFunction(()=>[...document.querySelectorAll('.gb-album img')].every(e=>e.complete&&e.naturalWidth>0));
 assert.deepEqual(await p.locator('.gb-album img').evaluateAll(es=>es.map(e=>[e.naturalWidth,e.naturalHeight])),[[1080,1350],[1080,1350]]);
 await noLato(p);await p.click('[data-gb-invia]');
 const a=await p.evaluate(()=>window.__albumInviati.at(-1));assert.deepEqual(a.keys,['files']);assert.equal(a.files.length,2);
 assert(a.files.every(f=>f.tipo==='image/png'&&f.byte>10000));assert.equal(new Set(a.files.map(f=>f.nome)).size,2);
}
(async()=>{
 fs.mkdirSync(F,{recursive:true});const br=await browser(M);
 for(const [sn,o0] of (process.env.SOLO_EXTRA?[]:SCH))for(const skin of ['girrr/','stadio/girrr/']){
  const opts={...o0,serviceWorkers:'block'};delete opts.defaultBrowserType;
  const c=await br.newContext(opts);await rete(c);const p=await c.newPage(),err=[];p.on('pageerror',e=>err.push(e.message));
  await c.addInitScript(()=>sessionStorage.setItem('ospite','1'));
  try{
   // Ingresso pubblico diretto dal Lab. La navigazione Home è già coperta da prova_601/602.
   await p.goto(B+skin+'app.html#carriera',{waitUntil:'domcontentloaded'});await p.click('[data-ctab=boa]');await p.waitForSelector('[data-pronto="1"]');
   assert.match(await p.locator('[data-gb-tit]').textContent(),/Il punto dopo la 7ª giornata/);
   assert.equal(await p.locator('[data-gb-squadra] option').count(),10);
   await p.selectOption('[data-gb-squadra]','Oranje VC');
   assert.match(await p.locator('[data-gb-contenuto]').textContent(),/11 punti in classifica/);
   assert.match(await p.locator('[data-gb-contenuto]').textContent(),/Dato non conservato/);
   assert.equal(await p.locator('.gb-kpi>div').count(),3);assert(await p.locator('.gb-dati').evaluate(e=>!e.open));
   await p.click('[data-gb-vista="1"]');assert(await p.locator('[data-gb-pagina="0"]').isHidden());assert(await p.locator('[data-gb-pagina="1"]').isVisible());
   const voci=await p.evaluate(async()=>{const j=await GirrrBoa.carica();return j.periodi.finora.squadre['Oranje VC'].voci;});
   const racconto=await p.locator('[data-gb-pagina="1"]').textContent();
   if(voci?.redazione)assert(racconto.includes(voci.redazione.testo));else assert(racconto.includes('Dato non conservato'));
   if(voci?.curva?.length)assert(racconto.includes(voci.curva[0].testo));
   await p.click('[data-gb-vista="0"]');await p.locator('.gb-dati>summary').click();
   assert.equal(await p.locator('.gb-fatti>div').count(),19);await noLato(p);
   const style=await p.locator('.gb-fatti>div').first().evaluate(e=>[getComputedStyle(e).borderLeftWidth,getComputedStyle(e).borderLeftColor]);
   // Il testo TV usa zoom: il motore può quantizzare il bordo al pixel fisico.
   assert(Math.abs(parseFloat(style[0])-(skin[0]==='s'?6:8))<0.5,'Spessore della banda fuori tolleranza');
   assert.equal(style[1],skin[0]==='s'?'rgb(255, 209, 102)':'rgb(214, 40, 57)');
   for(const d of await p.locator('.gb-dati>details').all()){await d.locator('summary').click();await noLato(p);}
   await p.click('[data-gb-album]');await invia(p);await p.keyboard.press('Escape');
   await p.selectOption('[data-gb-squadra]','Atletico ma non troppo');assert.equal(await p.locator('[data-gb-contenuto]>h3').textContent(),'Atletico ma non troppo');
   await p.selectOption('[data-gb-ambito]','lega');assert.equal(await p.locator('.gb-classifica>div').count(),10);
   assert(await p.locator('[data-gb-scelta]').isHidden());await noLato(p);
   if(['PC 1920','Smart TV 4K'].includes(sn)&&M==='chromium'){
    const n=sn.startsWith('PC')?'pc':'tv';await p.screenshot({path:path.join(F,`${n}-${skin[0]==='s'?'stadio':'lega'}-pagina.png`)});
   }
   await p.click('[data-gb-album]');await invia(p);
   assert.equal(await p.evaluate(()=>window.__albumInviati.length),2);
   if(['PC 1920','Smart TV 4K'].includes(sn)&&M==='chromium'){
    const n=sn.startsWith('PC')?'pc':'tv';await p.screenshot({path:path.join(F,`${n}-${skin[0]==='s'?'stadio':'lega'}-album.png`)});
   }
   await p.keyboard.press('Escape');assert.deepEqual(err,[]);
   record.push({motore:M,schermo:sn,grafica:skin,problemi:[]});console.log(`OK ${M} · ${sn} · ${skin}`);
  }catch(e){ko++;record.push({motore:M,schermo:sn,grafica:skin,problemi:[e.message,...err]});console.log(`KO ${M} · ${sn} · ${skin}: ${e.message}`);}
  await c.close();
 }
 // L'ospite, la squadra con il codice e la scelta dal Tabellone usano lo stesso album.
 const c=await br.newContext({viewport:{width:1280,height:800}});await rete(c);await c.addInitScript(()=>localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'PROVA'})));const p=await c.newPage();
 try{
  await p.goto(B+'girrr/app.html#carriera',{waitUntil:'domcontentloaded'});await p.click('[data-ctab=boa]');await p.waitForSelector('[data-pronto="1"]');assert.equal(await p.locator('[data-gb-squadra]').inputValue(),'Oranje VC');
  await p.waitForLoadState('networkidle');await p.waitForFunction(()=>document.querySelectorAll('[data-gb-squadra] option').length===10);
  const squadre=await p.locator('[data-gb-squadra] option').evaluateAll(es=>es.map(e=>e.value));assert.equal(squadre.length,10);
  for(const t of squadre){console.log('Album della squadra: '+t);await p.selectOption('[data-gb-squadra]',t);await p.click('[data-gb-album]');try{await invia(p);}catch(e){throw Error(t+': '+e.message+' · Stato: '+await p.locator('.gb-dialogo [role=status]').textContent());}await p.keyboard.press('Escape');await p.waitForFunction(()=>!document.querySelector('.gb-dialogo'));}
  await p.goto(B+'girrr/tabellone.html',{waitUntil:'domcontentloaded'});await p.click('button.cd-btn');await p.waitForSelector('.cd-sq select');await p.selectOption('.cd-sq select','Oranje VC');await p.click('[data-t=girone]');await invia(p);await p.keyboard.press('Escape');
  // Valori di confine futuri con fixture dichiarate: nessuna foto presentata come risultato reale.
  for(const n of [16,17,19,34]){
   const j=JSON.parse(fs.readFileSync(path.join(FIXTURE,'giornata-'+n+'.json')));
   const res=await p.evaluate(async j=>{const all=[];for(const k of Object.keys(j.periodi))for(const stadio of [false,true]){const a=await GirrrBoa.album(j,{k,squadra:'A',stadio});all.push(a.length);a.forEach(v=>URL.revokeObjectURL(v.url));}return {all,tit:GirrrBoa.titolo(j,j.periodi.andata?'andata':'finora')};},j);
   assert(res.all.every(x=>x===2));assert.match(res.tit,n<17?/Il punto dopo/:/Giro di boa/);
  }
  const lungo=JSON.parse(fs.readFileSync(path.join(FIXTURE,'nomi-lunghi.json')));
  assert.equal(await p.evaluate(async j=>{let n=0;for(const k of Object.keys(j.periodi))for(const squadra of Object.keys(j.periodi[k].squadre))for(const stadio of [false,true]){const a=await GirrrBoa.album(j,{k,squadra,stadio});assertAlbum(a);n++;}return n;function assertAlbum(a){if(a.length!==2)throw Error('Album incompleto');a.forEach(v=>URL.revokeObjectURL(v.url));}},lungo),60);
 }catch(e){ko++;record.push({motore:M,caso:'Squadra, Tabellone e confini 16/17/19/34',problemi:[e.stack]});console.log('KO confini:',e.message);}
 await c.close();await br.close();fs.writeFileSync(path.join(F,`${process.env.SOLO_EXTRA?'extra':'risultati'}-${M}.json`),JSON.stringify({motore:M,profili:process.env.SOLO_EXTRA?0:16,visite:process.env.SOLO_EXTRA?0:32,album_stress:60,problemi:ko,record},null,2));fs.rmSync(FIXTURE,{recursive:true,force:true});console.log(M+': '+ko+' problemi');process.exitCode=ko?1:0;
})().catch(e=>{console.error(e);process.exitCode=1;});
