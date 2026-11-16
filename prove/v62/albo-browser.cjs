/* Browser Albo 6.2: stesso contratto della RPC v62_albo, nessuna rete Supabase. */
const assert=require('assert/strict'),{browser}=require('../browser_certificato'),{rete}=require('./native-network.cjs');
const M=process.env.MOTORE||'chromium',BASE=process.env.BASE62||'http://127.0.0.1:8896/o-fant-a-girrr/';
const dati={stagione:'2026/27',mvp:[{giornata:7,team:'stif dc',chiusa:'2026-11-21T14:00:00Z'}],mvp_classifica:[{team:'stif dc',mvp:1,giornate:[7]}],
 partite:[{id:'sfida:2026/27:8',giornata:8,partita:'Grodah – stif dc',voti:{allenatori:4,redazione:1,personaggi:5,totale:10}}],stagione_conclusa:false};
(async()=>{const b=await browser(M),checks=[];try{
 for(const skin of ['girrr','stadio/girrr'])for(const w of [320,1280])for(const stato of ['dati','mancanti','fine']){
 const c=await b.newContext({viewport:{width:w,height:800},serviceWorkers:'block'});await rete(c);
 await c.route('**/__rpc/v62_albo',r=>r.fulfill({json:stato==='mancanti'?{...dati,partite:null}:stato==='fine'?{...dati,stagione_conclusa:true}:dati}));
 const p=await c.newPage(),errs=[];p.on('pageerror',e=>errs.push(e.message));
 try{
  await p.goto(BASE+skin+'/albo.html',{waitUntil:'domcontentloaded'});
  await p.locator('[data-at="rec"]').click(); // Record è una scheda nascosta finché non viene aperta
  await p.waitForSelector('#al-mvp-campionato',{timeout:15000});
  await p.waitForSelector('#al-partita-seguita',{timeout:15000});
  assert.equal(await p.locator('#al-mvp').count(),1);
  assert.equal(await p.locator('#al-mvp-campionato').count(),1);
  assert.equal(await p.locator('#al-partita-seguita').count(),1);
  // textContent: il titolo è in maiuscolo solo per la grafica (text-transform), innerText restituirebbe il maiuscolo
  assert.equal((await p.locator('#al-mvp-campionato h3').textContent()).trim(),stato==='fine'?'MVP del campionato':'Corsa all’MVP del campionato');
  const k=await p.locator('#al-partita-seguita').innerText();
  if(stato==='mancanti')assert(k.includes('Dato non disponibile'));
  else {assert(k.includes('Grodah'));assert(k.includes('Allenatori 4'));assert(k.includes('Redazione 1'));assert(k.includes('Personaggi 5'))}
  assert(await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth)<=1,'Scorrimento laterale');
  assert.deepEqual(errs,[]);checks.push({skin,w,stato,ok:true});
 }finally{await c.close()}
 }
}finally{await b.close()}
console.log(JSON.stringify({motore:M,esiti:checks.length,problemi:0}));})().catch(e=>{console.error(e);process.exitCode=1});