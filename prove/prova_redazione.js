// Prova della redazione di Girrr Sport nella Conferenza (Claude, 11 novembre 2026, versione 5.8).
// Uso: servire una copia di gh-pages con rilascio/conferenze/applica.py e rilascio/redazione/applica.py applicati e con
// lab/redazione/redazione.json in girrr/dati/ su http://localhost:8771/o-fant-a-girrr/, poi: node prove/prova_redazione.js CARTELLA_FOTO
// Il database si legge soltanto: derby_stato e conf_salva sono simulati, le altre scritture intercettate.
const { chromium, devices } = require('playwright');
const B='http://localhost:8771/o-fant-a-girrr/',D=process.argv[2];
(async()=>{const b=await chromium.launch();let ko=0;const ok=(c,m)=>{if(!c)ko++;console.log((c?'✓ ':'✗ ')+m)};
async function ctx(team,conf,opz){const c=await b.newContext(opz||devices['iPhone 15 Pro']);await c.addInitScript(t=>localStorage.setItem('fg',JSON.stringify({team:t,code:'PROVA'})),team);
 const st={salva:null};await c.route('**/rest/v1/rpc/**',async r=>{const n=r.request().url().split('/rpc/')[1];
  if(n==='derby_stato')return r.fulfill({json:{ok:true,sfide:[],voti:[],miei:[],conf:st.salva?[st.salva]:conf}});
  if(n==='conf_salva'){const x=JSON.parse(r.request().postData());st.salva={team:x.p_team,giornata:x.p_giornata,risposte:x.p_risposte,libera:x.p_libera,promessa:x.p_promessa,pesa:x.p_pesa,esito:null};return r.fulfill({status:204,body:''})}
  if(/salva|scrivi/.test(n))return r.fulfill({json:null});return r.continue()});return {c,st}}
// Apo team: niente conferenza ancora -> domande della redazione
let {c,st}=await ctx('Apo team',[]);let p=await c.newPage();const e=[];p.on('pageerror',x=>e.push(x.message));
await p.goto(B+'girrr/app.html#conf');await p.waitForSelector('.cf-dopo',{timeout:20000});await p.waitForTimeout(1500);
let tx=await p.innerText('body');ok(/Domande della redazione di Girrr Sport/.test(tx),'Apo team · etichetta della redazione');
ok(/scontro diretto/.test(tx)&&/Atletico ma non troppo, nono con i vostri stessi 6 punti/.test(tx),'Apo team · domande su misura (scontro diretto con l\'Atletico)');
ok(/Il giornalista ha letto/i.test(tx)&&/Non riportata/i.test(tx)&&!/gay/.test(tx),'Apo team · giudizio della 7ª, frase offensiva non riportata');
await p.$eval('.q',x=>x.scrollIntoView({block:'start'}));await p.waitForTimeout(300);await p.screenshot({path:D+'/red-domande.png'});
await p.$eval('.cf-giudizio',x=>x.scrollIntoView({block:'start'}));await p.waitForTimeout(300);await p.screenshot({path:D+'/red-giudizio.png'});
for(const [i,j] of [[0,0],[1,2],[2,1]]){await p.click(`[data-cq="${i}"][data-ca="${j}"]`);await p.waitForTimeout(150)}
await p.click('#cpub');await p.waitForTimeout(2500);
ok(st.salva&&st.salva.risposte[1].t==='In casa nostra l\'Atletico non passa.'&&st.salva.promessa==='Si torna su vincendo, e si comincia domani.'&&st.salva.pesa===2,'Apo team · salvate le frasi della redazione, promessa e peso giusti ('+(st.salva&&st.salva.promessa)+', '+(st.salva&&st.salva.pesa)+')');
await p.reload();await p.waitForTimeout(3000);tx=await p.innerText('body');
console.log(tx.split('\n').filter(l=>/Pubblicata|redazione/i.test(l)));ok(/Pubblicata · Non si cambia più/i.test(tx)&&/Domande della redazione/.test(tx),'Apo team · dopo la pubblicazione restano le stesse domande, bloccate');
const pr=await p.$$eval('[data-cq][aria-pressed="true"]',x=>x.map(y=>y.dataset.cq+y.dataset.ca).join(','));ok(pr==='00,12,21','Apo team · risposte scelte ricaricate ('+pr+')');
await c.close();
// Oranje VC: conferenza già pubblicata con le domande di sempre -> restano quelle
const R=[{a:1,k:1,t:'Una partita alla volta, con umiltà.',w:0},{a:1,k:1,t:'Mariana Coneja è un ottimo avversario: serve attenzione.',w:0},{a:2,k:2,t:'Chi non crede in noi può restare a casa.',w:1}];
({c}=await ctx('Oranje VC',[{team:'Oranje VC',giornata:8,risposte:R,promessa:R[2].t,pesa:2,esito:null}]));p=await c.newPage();p.on('pageerror',x=>e.push(x.message));
await p.goto(B+'stadio/girrr/app.html#conf');await p.waitForSelector('.cf-dopo',{timeout:20000});await p.waitForTimeout(1500);tx=await p.innerText('body');
ok(!/Domande della redazione/.test(tx)&&/Una partita alla volta, con umiltà/.test(tx),'Oranje VC · conferenza già pubblicata: restano le domande di sempre');
await c.close();
// 320 px
({c}=await ctx('WOA',[],{...devices['iPhone SE'],viewport:{width:320,height:568}}));p=await c.newPage();p.on('pageerror',x=>e.push(x.message));
await p.goto(B+'stadio/girrr/app.html#conf');await p.waitForSelector('.cf-dopo',{timeout:20000});await p.waitForTimeout(1500);tx=await p.innerText('body');
ok(/Campioni in carica/.test(tx),'WOA · domande su misura (campioni in carica, ultimi)');const w=await p.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]);ok(w[0]<=w[1]+1,'WOA · 320 px senza scorrimento laterale '+w);
await c.close();ok(!e.length,'nessun errore JS '+e.join(' / '));console.log('PROBLEMI: '+ko);await b.close()})();
