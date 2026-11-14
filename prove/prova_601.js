// Prova della 6.0.1 (Claude, 13 novembre 2026) sulla copia di gh-pages con rilascio/r601/applica.py, servita su localhost:8771.
// MOTORE=chromium|firefox|webkit node prove/prova_601.js   (BASE per un altro indirizzo; FOTO=cartella per le foto)
const pw = require('playwright'), { devices } = pw, fs = require('fs');
const M = process.env.MOTORE || 'chromium', B = process.env.BASE || 'http://localhost:8771/o-fant-a-girrr/', FOTO = process.env.FOTO;
const { script: BLOCCA } = require('./blocca_scritture');
const SCH = [['iPhone SE 320', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone 15 Pro', devices['iPhone 15 Pro']], ['Pixel 7', devices['Pixel 7']], ['iPad', devices['iPad Mini']], ['PC 1280', { viewport: { width: 1280, height: 850 } }], ['PC 1920', { viewport: { width: 1920, height: 1080 } }], ['TV', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 }]].filter(s => !process.env.SOLO || s[0].includes(process.env.SOLO));
const MENU = process.env.VERSIONE === '602' ? 'Panoramica|Stagione|Giro di boa|Obiettivi|Fiducia|Promesse|Storia|La mia settimana|Regole' : 'Panoramica|Stagione|Obiettivi|Fiducia|Promesse|Storia|La mia settimana|Regole';
async function ctx(o0) { const o={...o0,serviceWorkers:'block'};delete o.defaultBrowserType;const b=await require('./browser_certificato').browser(M);return [await b.newContext(o),()=>b.close()]; }
(async () => { let ko = 0;
 for (const [sn, o] of SCH) { const pr = [];
  for (const chi of ['squadra', 'ospite', 'anonimo']) { const [c, chiudi] = await ctx(o); await c.addInitScript(BLOCCA);
   if (chi === 'squadra') await c.addInitScript(() => { try { localStorage.setItem('fg', JSON.stringify({ team: 'Oranje VC', code: 'PROVA' })); } catch (e) {} });
   const p = await c.newPage(), err = []; p.on('pageerror', e => err.push(e.message.slice(0, 100)));
   const lato = async q => { if (await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) pr.push(chi + ' ' + q + ': scorre di lato'); };
   const q = chi === 'ospite' ? '?ospite=1' : '';
   for (const sk of ['girrr/', 'stadio/girrr/']) {
    // Carriera
    await p.goto(B + sk + 'app.html' + q + '#carriera'); await p.waitForTimeout(2600); await lato(sk + ' Carriera');
    const menu = await p.evaluate(() => [...document.querySelectorAll('#view .seg button')].filter(b => b.dataset.ctab || b.hasAttribute('data-pt-week')).map(b => b.textContent));
    if (chi === 'squadra') { if (menu.join('|') !== MENU) pr.push(sk + ' menu squadra: ' + menu.join('|')); }
    else { if (menu.join('|') !== MENU) pr.push(chi + ' ' + sk + ' menu: ' + menu.join('|'));   // l'ospite vede tutte le schede (Gianluca, 13 novembre, sera)
     const sel = p.locator('#cteam'); if (!(await sel.count())) pr.push(chi + ' ' + sk + ': manca la scelta della squadra');
     else { await sel.selectOption({ index: 3 }); await p.waitForTimeout(800); const v = await sel.inputValue(); const tot = await p.evaluate(() => !!document.querySelector('.bolla52') || [...document.querySelectorAll('#view a')].some(a => /Vai a Totogirrr/.test(a.textContent)));
      if (tot) pr.push(chi + ' ' + sk + ': premi o Totogirrr visibili');
      await p.click('[data-pt-week]'); await p.waitForTimeout(900); const st = await p.evaluate(() => (document.querySelector('#pt-storia .pt-sub') || {}).textContent || '');
      if (!/La settimana di/.test(await p.evaluate(() => (document.querySelector('#pt-storia h2') || {}).textContent || ''))) pr.push(chi + ' ' + sk + ': titolo della settimana');
      if (!st.includes(v.replace('The Blue brothers', 'The Blues Brothers').replace('stif dc', 'STIF DC'))) pr.push(chi + ' ' + sk + ': La mia settimana non è della squadra scelta (' + v + ' / ' + st.slice(0, 40) + ')');
      await lato(sk + ' settimana'); if (FOTO && /PC 1280|SE/.test(sn) && M === 'chromium') await p.screenshot({ path: FOTO + '/601-' + sn.replace(/\W+/g, '') + '-' + chi + '-' + sk.replace(/\W+/g, '') + '-settimana.png' }); } }
    // Obiettivi: linea del tempo e loghi degli sponsor
    await p.click('[data-ctab="ob"]'); await p.waitForTimeout(900);
    const ob = await p.evaluate(() => { const l = document.querySelector('.ob-timeline'); const h = [...document.querySelectorAll('.card h3')].find(x => /Premi sponsor/.test(x.textContent)); return { primo: l ? l.children[1] && l.children[1].textContent.trim() : '', loghi: h ? h.closest('.card').querySelectorAll('img.sp-logo').length : -1 }; });
    if (!/^1ª\s*L.inizio/.test(ob.primo)) pr.push(chi + ' ' + sk + ' linea del tempo: ' + ob.primo); if (chi === 'squadra' && ob.loghi < 1) pr.push(chi + ' ' + sk + ' premi sponsor senza loghi ' + ob.loghi);
    if (chi !== 'squadra' && await p.evaluate(() => /Premi sponsor/.test(document.getElementById('view').innerText))) pr.push(chi + ' ' + sk + ': vede i premi degli sponsor');
    await lato(sk + ' Obiettivi'); if (FOTO && /PC 1280|SE/.test(sn) && M === 'chromium') await p.screenshot({ path: FOTO + '/601-' + sn.replace(/\W+/g, '') + '-' + chi + '-' + sk.replace(/\W+/g, '') + '-obiettivi.png', fullPage: true });
    // Home
    await p.goto(B + sk + q); await p.waitForTimeout(1800); await lato(sk + ' Home');
    const home = await p.evaluate(() => { const L = [...document.querySelectorAll('.cards > *')].filter(e => e.offsetParent); return { n: L.length, col: new Set(L.map(e => Math.round(e.getBoundingClientRect().left))).size, spog: L.some(e => /Spogliatoio/.test(e.textContent)) }; });
    if (!home.spog) pr.push(chi + ' ' + sk + ' Home senza Spogliatoio');
    const gm = await p.evaluate(() => ({ gm: document.querySelectorAll('.osp-gm').length, banda: document.querySelectorAll('.osp').length }));
    if (gm.banda || gm.gm !== (chi === 'ospite' ? 1 : 0)) pr.push(chi + ' ' + sk + ' Home: Guest Mode ' + gm.gm + ', bande ' + gm.banda); if (sk === 'girrr/' && home.col !== 1) pr.push(chi + ' Home Lega in ' + home.col + ' colonne');
    if (FOTO && /PC 1280|SE/.test(sn) && M === 'chromium' && chi !== 'anonimo') { const el = await p.$('.cards'); if (el) await el.screenshot({ path: FOTO + '/601-' + sn.replace(/\W+/g, '') + '-' + chi + '-' + sk.replace(/\W+/g, '') + '-home.png' }); }
   }
   // Spogliatoio senza codice
   await p.goto(B + 'index.html' + q); await p.waitForTimeout(2200); await lato('Spogliatoio');
   const tabs = await p.evaluate(() => [...document.querySelectorAll('#tabs button')].filter(b => !b.hidden && b.offsetParent).map(b => b.dataset.t).filter(x => x !== 'cerca').join(','));   // «Cerca un giocatore» (cerca.js, dati pubblici) può comparire anche senza codice
   const atteso = chi === 'ospite' ? 'fa,inj,lega' : 'entra,fa,inj,lega'; if (tabs !== atteso) pr.push(chi + ' Spogliatoio schede: ' + tabs);
   for (const t of ['inj', 'fa', 'lega']) { await p.click('#tabs [data-t="' + t + '"]'); await p.waitForTimeout(700); const txt = await p.evaluate(() => document.getElementById('app').innerText.slice(0, 200)); if (!txt.trim() || /Entra con la tua squadra/.test(txt)) pr.push(chi + ' Spogliatoio ' + t + ' vuoto'); if (t === 'inj' && /I tuoi/.test(await p.evaluate(() => document.getElementById('app').innerText))) pr.push(chi + ' Infortunati con «I tuoi»'); await lato('Spogliatoio ' + t);
    if (FOTO && /PC 1280|SE/.test(sn) && M === 'chromium' && t === 'inj') await p.screenshot({ path: FOTO + '/601-' + sn.replace(/\W+/g, '') + '-' + chi + '-spogliatoio.png' }); }
   // con il codice giusto (simulato): tutte le schede, niente «Entra»
   if (chi === 'squadra') {   // codice giusto simulato: la pagina è la stessa, solo authed() risponde sì
    await p.route(/\/o-fant-a-girrr\/index\.html/, async rt => { const r = await rt.fetch(); const t = (await r.text()).replace('function authed(){', 'function authed(){return true;'); rt.fulfill({ response: r, body: t }); });
    await p.goto(B + 'index.html'); await p.waitForTimeout(2200);
    const r = await p.evaluate(() => [...document.querySelectorAll('#tabs button')].filter(b => !b.hidden).map(b => b.dataset.t).join(','));
    if (/entra/.test(r) || !/rosa/.test(r) || !/stat/.test(r)) pr.push('Spogliatoio con il codice: ' + r); await lato('Spogliatoio con il codice'); }
   err.forEach(e => pr.push(chi + ': ' + e)); await chiudi(); }
  console.log((pr.length ? 'KO ' : 'OK ') + M + ' · ' + sn + (pr.length ? '\n   ' + pr.join('\n   ') : '')); ko += pr.length; }
 console.log(M + ': ' + ko + ' problemi'); })();
