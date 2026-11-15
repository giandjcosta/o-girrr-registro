// 6.1.1 · Copie locali, tre motori reali, nessuna scrittura o invio.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{devices}=require('playwright');
const {browser}=require('./browser_certificato'),{script:BLOCCA}=require('./blocca_scritture');
const R=path.resolve(__dirname,'..'),B=process.env.BASE||'http://127.0.0.1:8890/o-fant-a-girrr/',M=process.env.MOTORE||'chromium',F=process.env.FOTO||path.join(R,'lab/611-foto');
const SCH=[['iPhone 320',{...devices['iPhone SE'],viewport:{width:320,height:568}}],...['iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape'].map(n=>[n,devices[n]]),...[1280,1920,2560].map(w=>['PC'+w,{viewport:{width:w,height:1080}}]),['TV',{viewport:{width:1920,height:1080},deviceScaleFactor:2,userAgent:'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 Chrome/94.0 TV Safari/537.36'}]];
async function frame(p){await p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))))}
async function rete(c){
 await c.addInitScript(BLOCCA);
 await c.addInitScript(()=>localStorage.setItem('fg',JSON.stringify({team:'Oranje VC',code:'PROVA'})));
 await c.addInitScript(()=>{window.__movimenti=[];const a=Element.prototype.animate;Element.prototype.animate=function(f,o){window.__movimenti.push({classe:this.className,fotogrammi:f,durata:o.duration});return a.call(this,f,o)}});
 await c.route('https://*.supabase.co/**',r=>{
  const fn=(r.request().url().match(/rpc\/([^?]+)/)||[])[1];
  assert(fn,'Richiesta DB inattesa');
  assert(/_stato$|_pubblico$|_lista$|^curva_feed$|^mvp_mio$|^mvp_derby$|^v62_sondaggi$|^v62_finestre$|^conf_pubbliche$|^conf_dopo_pubbliche$/.test(fn),'RPC inattesa: '+fn);
  return r.fulfill({json:fn==='v62_sondaggi'?{aperti:[],chiusi:[]}:fn==='v62_finestre'?{server_ora:new Date().toISOString(),prima_giornata:8,finestre:[]}:fn==='conf_pubbliche'||fn==='conf_dopo_pubbliche'?[]:fn==='curva_feed'?{ok:true,v:5,posts:[],replies:[],react:[],mine:[],follow:[],prof:{}}:fn==='mvp_stato'?{votazione:null,archivio:[]}:fn==='mvp_mio'?{scelta:null}:fn==='toto_pr_pubblico'?[]:{voti:[],sfide:[],coppie:[]}});
 });
 await c.route('**/stagione.js*',r=>r.fulfill({path:R+'/rilascio/stagione/stagione.js',contentType:'text/javascript'}));
 for(const f of ['curva-os.js','curva-os.css'])await c.route('**/'+f+'*',r=>r.fulfill({path:R+'/rilascio/curva-os/'+f,contentType:f.endsWith('js')?'text/javascript':'text/css'}));
 await c.route('**/girrr/curva.html*',r=>{
  const skin=/\/stadio\//.test(r.request().url())?'stadio/girrr':'girrr';
  let s=fs.readFileSync(R+'/rilascio/curva-os/pagine/'+skin+'/curva.html','utf8');
  s=s.replace('</head>','<script src="'+B+'curva-os.js"></script><link rel="stylesheet" href="'+B+'curva-os.css"></head>');
  // Contatore solo nella prova: verifica che i cambi scheda non rigenerino i cori.
  s=s.replace('function costruisci(){','function costruisci(){window.__modelli=(window.__modelli||0)+1;');
  return r.fulfill({body:s,contentType:'text/html'});
 });
}
async function noLato(p){assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Scorrimento laterale')}
(async()=>{
 fs.mkdirSync(F,{recursive:true});const b=await browser(M),report=[];
 for(const [nome,o] of SCH){if(process.env.SOLO&&!nome.includes(process.env.SOLO))continue;
  const c=await b.newContext({...o,serviceWorkers:'block'});await rete(c);
  for(const skin of ['girrr','stadio/girrr']){
   const p=await c.newPage(),errori=[];p.on('pageerror',e=>errori.push(e.message));
   try{
    await p.goto(B+skin+'/app.html#carriera',{waitUntil:'domcontentloaded'});await p.click('[data-ctab=stag]');await p.waitForSelector('.ms-giornata');
    const graf=await p.locator('.ms-graf').evaluate(g=>({n:g.querySelectorAll('option').length,primo:g.querySelector('option').textContent,ultimo:g.querySelector('option:last-child').textContent,assi:g.querySelector('svg').textContent,lettura:g.querySelector('output').textContent}));
    assert(graf.n>=7);assert(graf.primo.startsWith('1ª giornata'));assert(graf.assi.includes('Posizione')&&graf.assi.includes('Giornata'));assert(graf.ultimo.includes('5ª posizione'));
    await p.selectOption('.ms-giornata','0');assert.match(await p.locator('.ms-lettura').textContent(),/Dopo la 1ª giornata: 1ª posizione/);
    await p.locator('.ms-giornata').press('ArrowDown');assert.match(await p.locator('.ms-lettura').textContent(),/Dopo la 2ª giornata:/);
    await p.selectOption('.ms-giornata',String(graf.n-1));await noLato(p);
    const leggibile=await p.locator('.ms-classifica .ms-txt').evaluate(e=>({colore:getComputedStyle(e).color,px:parseFloat(getComputedStyle(e).fontSize)}));assert.equal(leggibile.colore,'rgb(251, 246, 236)');assert(leggibile.px>=15);
    const posizioni=await p.locator('.ms-posizioni').evaluate(e=>({testo:e.textContent,righe:[...e.children].map(s=>{const r=document.createRange();r.selectNodeContents(s);return {righe:r.getClientRects().length,w:s.getBoundingClientRect().width,max:e.clientWidth,spazi:getComputedStyle(s).whiteSpace}})}));
    assert.match(posizioni.testo,/Migliore posizione: .*Peggiore: /);assert.equal(posizioni.righe.length,2);
    for(const [i,z] of posizioni.righe.entries()){if(o.viewport.width>=1000&&i===1){assert.equal(z.righe,1,'Posizione peggiore a capo sul PC');assert(z.w<=z.max+1,'Peggiore fuori dal riquadro');}if(o.viewport.width<1000)assert.equal(z.spazi,'normal','Visualizzazione mobile modificata');}
    if(M==='chromium'&&['PC1920','TV','iPhone 320'].includes(nome)){await p.locator('.ms-graf').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(F,(nome==='iPhone 320'?'telefono':nome==='TV'?'tv':'pc')+'-'+(skin==='girrr'?'lega':'stadio')+'.jpg'),quality:84});}
    await p.close();
    if(process.env.SOLO_STAGIONE){assert.deepEqual(errori,[]);report.push({schermo:nome,grafica:skin,problemi:[]});continue;}
    const q=await c.newPage();q.on('pageerror',e=>errori.push(e.message));
    await q.goto(B+skin+'/curva.html',{waitUntil:'domcontentloaded'});await q.waitForFunction(()=>window.__curvaProva&&window.__curvaProva.posts().length>20);await q.waitForTimeout(900);
    const modello=await q.evaluate(()=>window.__modelli);
    for(const f of ['squadre','notizie','tutti']){await q.click('[data-f='+f+']');await frame(q);assert.equal(await q.locator('.tabs .on').getAttribute('data-f'),f);await noLato(q)}
    assert.equal(await q.evaluate(()=>window.__modelli),modello,'Modello rigenerato navigando');
    // Un solo effetto per il feed, nessuna sfocatura o animazione sulle singole card.
    const anim=await q.evaluate(()=>({post:[...document.querySelectorAll('#vista .post')].some(e=>getComputedStyle(e).animationName!=='none'),feed:document.querySelector('.cv-flusso').getAnimations().length,ultimo:window.__movimenti.at(-1)}));
    assert(!anim.post);assert(anim.feed<=1);assert.equal(anim.ultimo.classe,'cv-flusso');assert.equal(anim.ultimo.durata,160);assert(anim.ultimo.fotogrammi.every(f=>!f.filter));
    await q.evaluate(()=>{__curvaProva.render()});await frame(q);assert.equal(await q.evaluate(()=>window.__modelli),modello+1,'Aggiornamento dati congelato');
    await q.evaluate(()=>__curvaProva.entra('Oranje VC'));await q.fill('#tx','Bozza della prova 6.1.1');
    await q.evaluate(()=>{document.querySelector('#tx').__segno=1;document.querySelectorAll('#top .tabs button').forEach(e=>e.__segno=1);for(const f of ['squadre','notizie','tutti','squadre','tutti'])document.querySelector('[data-f='+f+']').click()});await frame(q);
    assert.equal(await q.inputValue('#tx'),'Bozza della prova 6.1.1');assert(await q.evaluate(()=>document.querySelector('#tx').__segno===1&&[...document.querySelectorAll('#top .tabs button')].every(e=>e.__segno===1)));
    assert.equal(await q.locator('.tabs .on').getAttribute('data-f'),'tutti');
    // Le modifiche estranee alla navigazione non misurano di nuovo la barra.
    const letture=await q.evaluate(async()=>{let n=0;const d=Object.getOwnPropertyDescriptor(HTMLElement.prototype,'offsetLeft');Object.defineProperty(HTMLElement.prototype,'offsetLeft',{...d,get(){n++;return d.get.call(this)}});const s=document.createElement('span');document.body.append(s);await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));s.remove();return n});assert.equal(letture,0);
    await q.emulateMedia({reducedMotion:'reduce'});await q.click('[data-f=notizie]');await frame(q);assert(await q.evaluate(()=>!document.documentElement.hasAttribute('data-cambio-tabs')&&!document.querySelector('.cv-flusso').getAnimations().length));
    await q.emulateMedia({reducedMotion:'no-preference'});await q.click('[data-f=tutti]');await frame(q);
    await q.click('#nav [data-v=esplora]');await frame(q);assert(await q.locator('#qs').count());await q.click('#nav [data-v=home]');await frame(q);await noLato(q);
    await q.evaluate(()=>__curvaProva.vai('notifiche','tutte'));await q.click('[data-nf=men]');await frame(q);assert.equal(await q.locator('[data-nf=men]').getAttribute('class'),'on');
    await q.evaluate(()=>__curvaProva.vai('home'));await frame(q);
    if(M==='chromium'&&['PC1920','TV'].includes(nome))await q.screenshot({path:path.join(F,'curva-'+(nome==='TV'?'tv':'pc')+'-'+(skin==='girrr'?'lega':'stadio')+'.jpg'),quality:84});
    assert.deepEqual(errori,[]);report.push({schermo:nome,grafica:skin,problemi:[]});await q.close();
   }catch(e){report.push({schermo:nome,grafica:skin,problemi:[e.message]});console.error('KO',nome,skin,e.message);await p.close().catch(()=>{});}
  }
  await c.close();console.log(M+' '+nome);
 }
 // Casi limite: prima giornata, stagione completa, classifica con 14 squadre.
 for(const n of [1,34]){
  const c=await b.newContext({viewport:{width:320,height:700},serviceWorkers:'block'}),p=await c.newPage();
  const teams=Array.from({length:14},(_,i)=>({name:'Squadra '+i}));
  const D={teams,cal:{lega:Array.from({length:n},(_,i)=>({n:i+1,sa:i+1,m:Array.from({length:7},(_,j)=>['Squadra '+(j*2),80,j===6?65:70,'Squadra '+(j*2+1),'2-0'])})),cup:[]}};
  await c.route('**/data.json',r=>r.fulfill({json:D}));
  await c.route('**/formazioni.json',r=>r.fulfill({json:{}}));await c.route('**/borsino.json',r=>r.fulfill({json:{}}));
  await c.route('**/stagione.js*',r=>r.fulfill({path:R+'/rilascio/stagione/stagione.js',contentType:'text/javascript'}));
  await c.addInitScript(BLOCCA);await p.goto(B,{waitUntil:'domcontentloaded'});await p.setContent('<main id="mount" style="width:300px;background:#22305b;color:white"></main>');await p.addScriptTag({url:B+'stagione.js'});
  await p.waitForFunction(()=>{document.querySelector('#mount').innerHTML=GirrrStagione('Squadra 13');return !!document.querySelector('.ms-giornata')});
  assert.equal(await p.locator('.ms-giornata option').count(),n);assert.match(await p.locator('.ms-lettura').textContent(),new RegExp('Dopo la '+n+'ª giornata: 14ª posizione'));
  assert.equal(await p.locator('circle[data-attivo]').getAttribute('cy'),'170.0');await noLato(p);
  if(n===34){assert.equal(await p.locator('[data-ms-val][visibility=visible]').count(),1);await p.selectOption('.ms-giornata','0');assert.match(await p.locator('.ms-lettura').textContent(),/Dopo la 1ª giornata/)}
  report.push({schermo:'Caso limite '+n+' giornate, 14 squadre',grafica:'Modulo',problemi:[]});await c.close();
 }
 await b.close();const problemi=report.filter(x=>x.problemi.length).length;fs.writeFileSync(path.join(F,'risultati-'+M+'.json'),JSON.stringify({motore:M,visite:report.length,problemi,report},null,2));console.log({motore:M,visite:report.length,problemi});if(problemi)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
