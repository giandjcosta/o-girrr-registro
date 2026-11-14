// Periodi, competizione e contenuti coerenti: motori reali, schermi emulati, nessuna scrittura.
const fs=require('fs'),path=require('path'),os=require('os'),assert=require('assert/strict'),{devices}=require('playwright');
const {browser}=require('./browser_certificato'),{script}=require('./blocca_scritture');
const M=process.env.MOTORE||'chromium',B=process.env.REGISTRO||'http://127.0.0.1:8890/o-girrr-registro/',F=process.env.FOTO||'/tmp/bilanci-61';
const schermi=[['iPhone320',{...devices['iPhone SE'],viewport:{width:320,height:568}}],...['iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape'].map(n=>[n,devices[n]]),...[1280,1920,2560].map(w=>['PC'+w,{viewport:{width:w,height:1080}}]),['TV',{viewport:{width:1920,height:1080},deviceScaleFactor:2}]];
async function lato(p){await p.waitForFunction(()=>document.documentElement.scrollWidth<=innerWidth+1,{},{timeout:2000}).catch(()=>{});const r=await p.evaluate(()=>({w:innerWidth,sw:document.documentElement.scrollWidth,comp:document.querySelector('[data-gb-comp]')?.value,ambito:document.querySelector('[data-gb-ambito]')?.value,fuori:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.right>innerWidth+1;}).slice(0,5).map(e=>({tag:e.tagName,cl:e.className,right:e.getBoundingClientRect().right}))}));assert(r.sw<=r.w+1,'Scorrimento orizzontale: '+JSON.stringify(r));}
(async()=>{fs.mkdirSync(F,{recursive:true});const br=await browser(M),record=[];let errori=0;
for(const [nome,o] of schermi.filter(([n])=>!process.env.SCHERMO||n===process.env.SCHERMO))for(const skin of ['lega','stadio']){
 const c=await br.newContext({...o,serviceWorkers:'block'});await c.addInitScript(script);await c.addInitScript(()=>{window.__inviati=[];navigator.canShare=()=>true;navigator.share=x=>{__inviati.push({keys:Object.keys(x),files:x.files.map(f=>({nome:f.name,tipo:f.type,byte:f.size}))});return Promise.resolve();};});
 const p=await c.newPage(),err=[];p.on('pageerror',e=>err.push(e.message));
 try{
  await p.goto(B+'lab/giro-di-boa-61/');await p.waitForSelector('[data-pronto="1"]');await p.evaluate(s=>document.documentElement.dataset.skin=s,skin);
  const j=await p.evaluate(()=>GirrrBoa.carica(new URL('../giro-di-boa-602/esempio.json',location.href).href));assert.equal(j.ultima_pubblicata,7);
  assert.deepEqual(await p.locator('[data-gb-periodo] option').evaluateAll(es=>es.map(e=>e.value)),['finora','inizio','tappa_5']);
  assert.equal(await p.locator('[data-gb-periodo]').inputValue(),'finora');
  for(const comp of ['campionato','coppa','entrambe']){
   const v=comp==='campionato'?j.periodi.finora:j.periodi.finora.competizioni[comp];
   await p.selectOption('[data-gb-comp]',comp);await p.selectOption('[data-gb-ambito]','squadra');await p.selectOption('[data-gb-squadra]','Oranje VC');await p.click('[data-gb-vista="0"]');await lato(p);
   const kpi=await p.locator('.gb-kpi>div strong,.gb-totale>strong').evaluateAll(es=>es.map(e=>e.textContent));
   assert(kpi.some(t=>t.replace(/\s/g,'')===v.squadre['Oranje VC'].bilancio.gol_fatti+':'+v.squadre['Oranje VC'].bilancio.gol_subiti));
   if(comp==='coppa')assert.equal(await p.locator('.gb-kpi>div').first().evaluate(e=>getComputedStyle(e).borderLeftColor),'rgb(61, 147, 214)');
   if(comp==='entrambe')assert.equal(await p.locator('.gb-due-competizioni>[data-comp]').count(),2);
   await p.click('[data-gb-vista="1"]');const voce=await p.locator('[data-gb-pagina="1"]').textContent();assert(voce.includes(v.squadre['Oranje VC'].voci.redazione.testo));
   for(const q of v.squadre['Oranje VC'].voci.curva)assert(voce.includes(q.testo));await lato(p);
   await p.selectOption('[data-gb-ambito]','lega');await p.click('[data-gb-vista="0"]');await lato(p);
   if(comp==='coppa')assert.equal(await p.locator('.gb-girone').count(),2);
   await p.click('[data-gb-vista="1"]');const generale=await p.locator('[data-gb-pagina="1"]').textContent();assert(generale.includes(v.voci.redazione[0].testo));
   const pr=(v.campionato||v.riepilogo).primati;assert(generale.includes(pr.attacco.gol+' gol fatti'));assert(generale.includes(pr.difesa.gol+' gol subiti'));await lato(p);
   // Ogni vista cambia davvero al selettore delle tappe, anche nelle voci della redazione.
   await p.selectOption('[data-gb-periodo]','inizio');const vi=comp==='campionato'?j.periodi.inizio:j.periodi.inizio.competizioni[comp];assert((await p.locator('[data-gb-pagina="1"]').textContent()).includes(vi.voci.redazione[0].testo));
   await p.selectOption('[data-gb-periodo]','finora');
   // Album di entrambe in tutti i profili; anche i due album singoli sul telefono minimo.
   if(comp==='entrambe'||nome==='iPhone320'){
    await p.click('[data-gb-album]');const n=comp==='entrambe'?3:2;
    await p.waitForFunction(n=>document.querySelectorAll('.gb-album img').length===n&&[...document.querySelectorAll('.gb-album img')].every(i=>i.complete&&i.naturalWidth),n);
    assert.deepEqual(await p.locator('.gb-album img').evaluateAll(es=>es.map(e=>[e.naturalWidth,e.naturalHeight])),Array.from({length:n},()=>[1080,1350]));
    assert.deepEqual(await p.locator('[data-gb-k] option').evaluateAll(es=>es.map(e=>e.value)),['finora','inizio','tappa_5']);await lato(p);
    await p.click('[data-gb-invia]');const invio=await p.evaluate(()=>__inviati.at(-1));assert.deepEqual(invio.keys,['files']);assert.equal(invio.files.length,n);assert(invio.files.every(f=>f.tipo==='image/png'&&f.byte>10000&&f.nome.includes(comp)));
    await p.keyboard.press('Escape');
   }
  }
  for(const k of ['tappa_10','andata','fine'])assert(await p.evaluate(async k=>{try{await GirrrBoa.album(await GirrrBoa.carica(new URL('../giro-di-boa-602/esempio.json',location.href).href),{k,squadra:'Oranje VC'});return false;}catch(e){return /sbloccato|disponibile/.test(e.message);}},k),'Periodo futuro accessibile: '+k);
  assert.deepEqual(err,[]);record.push({schermo:nome,grafica:skin,problemi:[]});console.log('OK '+M+' '+nome+' '+skin);
 }catch(e){errori++;record.push({schermo:nome,grafica:skin,problemi:[e.message,...err]});console.log('KO '+M+' '+nome+' '+skin+': '+e.message);}
 await c.close();
}
await br.close();fs.writeFileSync(path.join(F,'filtri-61-'+M+'.json'),JSON.stringify({motore:M,visite:record.length,problemi:errori,record},null,2));process.exitCode=errori?1:0;
})().catch(e=>{console.error(e);process.exitCode=1;});
