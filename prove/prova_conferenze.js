// Prova delle novità delle conferenze (Claude, 10 novembre 2026): conferenza bloccata dopo la pubblicazione, conferenza dell'avversario
// con «Rispondi in Curva», scheda Promesse della Carriera, Testa a testa nel Derby, ?scrivi= della Curva, testo grande solo sulla TV.
// Uso: servire una copia di gh-pages con rilascio/conferenze/applica.py applicato su http://localhost:8771/o-fant-a-girrr/, poi:
//   node prove/prova_conferenze.js [CARTELLA_FOTO]
// Il database vero si legge soltanto (conf_pubbliche, conf_promesse, feed): ogni funzione che scrive è intercettata e non parte.
const { chromium, devices } = require('playwright');
const B = 'http://localhost:8771/o-fant-a-girrr/';
const FOTO = process.argv[2];
const SCRIVE = /salva|scrivi|lancia|rispondi|vota|reagisci|registra|cancella|proponi|riscuoti|duello_|toto_|push_|segui|sondaggio|carriera_/;
const RISP = [{ a: 1, k: 1, t: 'Una partita alla volta, con umiltà.', w: 0 }, { a: 1, k: 1, t: 'Mariana Coneja è un ottimo avversario: serve attenzione.', w: 0 }, { a: 2, k: 2, t: 'Chi non crede in noi può restare a casa.', w: 1 }];
const AVV = { team: 'Mariana Coneja', giornata: 8, risposte: [{ a: 0, k: 0, t: 'Lo centriamo, senza dubbi.', w: 1 }, { a: 2, k: 2, t: 'Oranje VC? Chiedete a loro se hanno la formazione.', w: 1 }, { a: 1, k: 1, t: 'Grazie, continuiamo a lavorare a testa bassa.', w: 0 }], libera: null, promessa: 'Lo centriamo, senza dubbi.', pesa: 1 };

async function contesto(browser, opz, { bloccata, avversario, squadra = 'Oranje VC' } = {}) {
  const ctx = await browser.newContext(opz);
  await ctx.addInitScript(t => { try { localStorage.setItem('fg', JSON.stringify({ team: t, code: 'PROVA' })); } catch (e) {} }, squadra);
  const scritte = [];
  await ctx.route('**/rest/v1/rpc/**', async (route) => {
    const nome = route.request().url().split('/rpc/')[1].split('?')[0];
    if (nome === 'derby_stato') return route.fulfill({ json: { ok: true, sfide: [], voti: [], miei: [], conf: bloccata ? [{ team: squadra, giornata: 8, risposte: RISP, libera: null, promessa: RISP[2].t, pesa: 2, esito: null }] : [] } });
    if (nome === 'conf_pubbliche' && avversario) {
      const r = await route.fetch(); const j = await r.json();
      return route.fulfill({ json: j.filter(c => !(c.team === AVV.team && c.giornata === 8)).concat([AVV]) });
    }
    if (nome === 'curva_feed') { const r = await route.fetch(); const j = await r.json(); return route.fulfill({ json: Object.assign(j, { ok: true }) }); }   /* il codice di prova vale come vero */
    if (SCRIVE.test(nome) && !/_(stato|pubblico|lista)$/.test(nome)) { scritte.push(nome); return route.fulfill({ json: null }); }
    return route.continue();
  });
  return { ctx, scritte };
}

(async () => {
  const browser = await chromium.launch();
  const ko = [];
  const ok = (c, m) => { if (!c) ko.push(m); console.log((c ? '✓ ' : '✗ ') + m); };
  const lato = async (p, m) => { const w = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]); ok(w[0] <= w[1] + 1, m + ': nessuno scorrimento laterale (' + w.join('/') + ')'); };
  const err = p => { const e = []; p.on('pageerror', x => e.push(x.message.slice(0, 100))); return e; };

  for (const graf of ['girrr/', 'stadio/girrr/']) {
    const G = graf === 'girrr/' ? 'Lega' : 'Stadio';
    // 1-2. Conferenza libera, poi bloccata
    let { ctx, scritte } = await contesto(browser, devices['iPhone SE'], { bloccata: false, avversario: true });
    let p = await ctx.newPage(); let e = err(p);
    await p.goto(B + graf + 'app.html#conf'); await p.waitForSelector('#cpub'); await p.waitForTimeout(1800);
    ok(/Una volta pubblicata/.test(await p.textContent('#app, body')), G + ' · Conferenza libera: avviso prima di pubblicare');
    ok(await p.$('.cf-avv') !== null, G + ' · Riquadro della conferenza dell\'avversario');
    ok(/Cosa ha detto Mariana Coneja/.test(await p.textContent('.cf-avv')), G + ' · Titolo «Cosa ha detto Mariana Coneja»');
    const href = await p.getAttribute('.cf-avv a.btn', 'href');
    ok(href === 'curva.html?scrivi=' + encodeURIComponent('@mariana_coneja '), G + ' · Rispondi in Curva porta a ' + href);
    await lato(p, G + ' · Conferenza 320');
    if (FOTO) { await p.$eval('.cf-avv', x => x.scrollIntoView({ block: 'center' })); await p.screenshot({ path: `${FOTO}/conf-avversario-${G}.png` }); }
    ok(!e.length, G + ' · Nessun errore JS (conferenza libera) ' + e.join(' / '));
    await ctx.close();

    ({ ctx, scritte } = await contesto(browser, devices['iPhone SE'], { bloccata: true }));
    p = await ctx.newPage(); e = err(p);
    await p.goto(B + graf + 'app.html#conf'); await p.waitForTimeout(2500);
    const bt = await p.textContent('#cpub');
    ok(bt.trim() === 'Pubblicata · Non si cambia più', G + ' · Bottone bloccato: «' + bt.trim() + '»');
    const dis = await p.$$eval('[data-cq]', b => b.filter(x => !x.disabled).length);
    ok(dis === 0, G + ' · Risposte disattivate (attive: ' + dis + ')');
    const prima = await p.$$eval('[data-cq][aria-pressed="true"]', b => b.map(x => x.dataset.cq + x.dataset.ca).join(','));
    await p.click('[data-cq="0"][data-ca="0"]', { force: true }).catch(() => {});
    await p.waitForTimeout(300);
    const dopo = await p.$$eval('[data-cq][aria-pressed="true"]', b => b.map(x => x.dataset.cq + x.dataset.ca).join(','));
    ok(prima === dopo && prima === '01,11,22', G + ' · Il tocco non cambia la risposta (' + prima + ' → ' + dopo + ')');
    ok(/Come appare in Curva/.test(await p.textContent('body')), G + ' · Anteprima del post ancora visibile');
    ok(!scritte.length, G + ' · Nessuna scrittura nel database (' + scritte.join(',') + ')');
    if (FOTO) { await p.$eval('#cpub', x => x.scrollIntoView({ block: 'center' })); await p.screenshot({ path: `${FOTO}/conf-bloccata-${G}.png` }); }
    ok(!e.length, G + ' · Nessun errore JS (conferenza bloccata) ' + e.join(' / '));

    // 5. Promesse nella Carriera
    await p.goto(B + graf + 'app.html#carriera'); await p.waitForSelector('[data-ctab="prom"]'); await p.click('[data-ctab="prom"]');
    await p.waitForSelector('.cf-pr, .cf-sum', { timeout: 15000 }); await p.waitForTimeout(800);
    const tp = await p.textContent('body');
    ok(/Le promesse in conferenza stampa/.test(tp), G + ' · Scheda Promesse');
    ok(/Chi parla di obiettivi guardi la classifica/.test(tp), G + ' · Promessa della 4ª giornata');
    ok(/Giornata 4 · Contro Real Madrink/.test(tp), G + ' · Avversario della 4ª: Real Madrink');
    await lato(p, G + ' · Promesse 320');
    if (FOTO) { await p.$eval('.cf-sum', x => x.scrollIntoView({ block: 'start' })); await p.screenshot({ path: `${FOTO}/promesse-${G}.png` }); }

    // 6. Testa a testa nel Derby
    await p.goto(B + graf + 'app.html#derby'); await p.waitForSelector('.cf-tt', { timeout: 15000 });
    let tt = await p.textContent('.cf-tt');
    ok(/Oranje VC/.test(tt) && /Mariana Coneja/.test(tt), G + ' · Testa a testa parte da Oranje VC e Mariana Coneja');
    await p.selectOption('[data-tt="b"]', 'Apo team'); await p.waitForTimeout(400);
    tt = await p.textContent('.cf-tt');
    ok(/Apo team/.test(tt) && /Scontri della stagione/.test(tt) && /Classifica a confronto/.test(tt), G + ' · Cambio squadra: Oranje VC - Apo team');
    await lato(p, G + ' · Derby 320');
    if (FOTO) { await p.$eval('.cf-tt', x => x.scrollIntoView({ block: 'start' })); await p.screenshot({ path: `${FOTO}/testa-a-testa-${G}.png` }); }

    // ?scrivi= della Curva
    await p.goto(B + graf + 'curva.html?come=' + encodeURIComponent('Oranje VC') + '&scrivi=' + encodeURIComponent('@mariana_coneja ')); await p.waitForSelector('#tx', { timeout: 15000 }); await p.waitForTimeout(1500);
    ok((await p.inputValue('#tx')) === '@mariana_coneja ', G + ' · Curva con il testo già scritto');
    ok(!/scrivi=/.test(p.url()) && /come=Oranje%20VC/.test(p.url()), G + ' · Il parametro sparisce dall\'indirizzo, gli altri restano: ' + p.url().split('?')[1]);
    ok(!e.length, G + ' · Nessun errore JS ' + e.join(' / '));
    ok(!scritte.length, G + ' · Nessuna scrittura nel database (' + scritte.join(',') + ')');
    await ctx.close();
  }

  // 10. Testo grande solo sulla TV
  const TV = { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36' };
  const WEBOS = { viewport: { width: 1920, height: 1080 }, userAgent: 'Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 WebAppManager' };
  for (const [nome, opz, vuole] of [['Smart TV Tizen', TV, true], ['Smart TV webOS', WEBOS, true], ['PC 1920', { viewport: { width: 1920, height: 1080 } }, false],
    ['iPhone 15 Pro', devices['iPhone 15 Pro'], false], ['Pixel 7', devices['Pixel 7'], false], ['iPad Pro 11', devices['iPad Pro 11'], false], ['Galaxy Tab S4', devices['Galaxy Tab S4'], false]]) {
    const { ctx } = await contesto(browser, opz, {});
    const p = await ctx.newPage(); const e = err(p);
    for (const u of ['girrr/', 'stadio/girrr/', 'girrr/tabellone.html', 'girrr/curva.html', 'index.html#PROVA']) {
      await p.goto(B + u); await p.waitForTimeout(1200);
      const c = await p.evaluate(() => document.documentElement.classList.contains('tv-grande'));
      ok(c === vuole, nome + ' · ' + u + ': testo grande ' + (c ? 'sì' : 'no'));
      await lato(p, nome + ' · ' + u);
      if (FOTO && vuole && nome === 'Smart TV Tizen' && /^(girrr\/|stadio\/girrr\/)$/.test(u)) await p.screenshot({ path: `${FOTO}/tv-${u.replace(/\W+/g, '_')}.png` });
    }
    ok(!e.length, nome + ' · Nessun errore JS ' + e.join(' / '));
    await ctx.close();
  }
  console.log(ko.length ? '\nPROBLEMI: ' + ko.length : '\nTUTTO A POSTO');
  await browser.close();
  process.exit(ko.length ? 1 : 0);
})();
