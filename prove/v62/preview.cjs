/* Collaudo della preview esportata: le preferenze vere del browser non cambiano. */
const assert=require('assert/strict'),fs=require('fs'),{browser}=require('../browser_certificato');
const BASE=process.env.LAB62||'http://127.0.0.1:8898/lab/integrata-62/',M=process.env.MOTORE||'chromium';
(async()=>{let b=await browser(M),prove=[];for(const sk of ['girrr','stadio/girrr']){const c=await b.newContext({viewport:{width:320,height:568},serviceWorkers:'allow'}),p=await c.newPage(),errors=[],db=[];
 await c.addInitScript(()=>{localStorage.setItem('fg','sessione-personale-da-preservare')});p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(new URL(r.url()).hostname.endsWith('.supabase.co'))db.push(r.url())});p.on('response',r=>{if(r.status()>=400&&!r.url().includes('cronache.json'))errors.push(r.status()+' '+r.url())});
 await p.goto(BASE+sk+'/curva.html?squadra=Oranje%20VC&risultati=B');await p.waitForSelector('[data-v62-poll]');assert.equal(await p.locator('[data-v62-closed]').getAttribute('open'),null);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 let f=p.locator('[data-v62-poll]').first().locator('form');if(await f.count()){await f.locator('input').first().check();await f.locator('button').click();await p.waitForFunction(()=>document.querySelector('[data-v62-poll]').textContent.includes('Hai già votato:'))}
 await p.goto(BASE+sk+'/app.html?sezione=sondaggi&risultati=A#sport');await p.waitForSelector('[data-v62-poll]');assert((await p.locator('[data-v62-poll]').first().innerText()).includes('Hai già votato:'));assert.equal(await p.locator('[data-v62-closed]').count(),1);
 await p.goto(BASE+sk+'/app.html#conf');await p.locator('[data-v62-precedenti] summary').click();await p.selectOption('[data-v62-team]','Oranje VC');await p.selectOption('[data-v62-day]','7');assert((await p.locator('[data-v62-conferenza]').innerText()).includes('vittoria meritata'));
 await p.goto(BASE+sk+'/campo.html?squadra=');await p.waitForSelector('#matches .gamebtn');assert.equal(await p.locator('#matches .mia').count(),0);
 await p.goto(BASE+sk+'/campo.html?squadra=Oranje%20VC');await p.waitForSelector('#matches .mia');
 assert.equal(await p.evaluate(()=>Storage.prototype.getItem.toString().includes('N+k')),true);assert.equal(await p.evaluate(()=>Object.getOwnPropertyDescriptor(localStorage,'fg')?.value),'sessione-personale-da-preservare');
 assert.deepEqual(db,[]);assert.deepEqual(errors,[]);prove.push({grafica:sk,esito:'superato',supabaseRichieste:db.length,sessionePreservata:true});await c.close()}
 await b.close();fs.writeFileSync(__dirname+'/risultati-preview-'+M+'.json',JSON.stringify({motore:M,prove},null,2)+'\n');console.log(prove)})().catch(e=>{console.error(e);process.exit(1)});
