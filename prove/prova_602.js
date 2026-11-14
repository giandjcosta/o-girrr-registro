// Prova della 6.0.2 (Claude, 13 novembre 2026): condivisione singola nelle pagine e scelta della squadra nel Tabellone.
// Copia di gh-pages con 6.0.1 e 6.0.2 applicate, servita su localhost:8773.
//   MOTORE=chromium|webkit node prove/prova_602.js [CARTELLA_FOTO]   (BASE per un altro indirizzo)
// Condivisione simulata (navigator.share registrato): si controllano file, nomi e tipi. Scritture nel database bloccate.
const pw = require('playwright'), { devices } = pw;
const { script: BLOCCA } = require('./blocca_scritture');
const M = process.env.MOTORE || 'chromium', B = process.env.BASE || 'http://localhost:8773/o-fant-a-girrr/', D = process.argv[2];
const SCH = [['iPhone SE 320', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone 15 Pro', devices['iPhone 15 Pro']], ['PC 1280', { viewport: { width: 1280, height: 800 } }]];
(async () => {
  const br = await require('./browser_certificato').browser(M); let ko = 0;
  for (const [sn, o0] of SCH) for (const chi of ['ospite', 'squadra']) for (const g of ['girrr/', 'stadio/girrr/']) {
    const o = { ...o0, serviceWorkers: 'block' }; delete o.defaultBrowserType;
    const c = await br.newContext(o); await c.addInitScript(BLOCCA);
    await c.addInitScript(() => { window.__inv = []; navigator.canShare = () => true; navigator.share = d => { window.__inv.push({ f: d.files.map(f => f.name + '|' + f.type), t: d.text || '' }); return Promise.resolve(); }; });
    if (chi === 'squadra') await c.addInitScript(() => { try { localStorage.setItem('fg', JSON.stringify({ team: 'Oranje VC', code: 'PROVA' })); } catch (e) {} });
    const p = await c.newPage(), pr = []; p.on('pageerror', e => pr.push('errore: ' + e.message.slice(0, 100)));
    if (chi === 'ospite') { await p.goto(B + g + '?ospite=1'); await p.waitForTimeout(800); }
    const lato = async w => { if (await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) pr.push(w + ': scorre di lato'); };
    const inv = [];
    for (const comp of ['lega', 'coppa']) {
      if (comp === 'coppa') inv.push(...await p.evaluate(() => window.__inv));   /* la pagina si ricarica: si tiene quello che è già stato condiviso */
      await p.goto(B + g + 'tabellone.html'); await p.waitForTimeout(2200);
      if (comp === 'coppa') { const sw = p.locator('[data-m="coppa"], .sw button').last(); if (await sw.count()) { await sw.click(); await p.waitForTimeout(900); } }
      await p.locator('button.cd-btn').first().click(); await p.waitForSelector('.cd-sq select', { timeout: 15000 }).catch(() => pr.push(comp + ': manca la scelta della squadra'));
      await p.waitForTimeout(800);
      const st = await p.evaluate(() => ({ uff: !document.querySelector('[data-t=ufficiale]').hidden, sq: document.querySelector('.cd-sq select').value, tit: document.querySelector('[data-tit=partita]').textContent, n: document.querySelectorAll('.cd-sq option').length, p: document.querySelector('.cd-box p').textContent }));
      if (!st.uff) pr.push(comp + ': manca il Tabellone ufficiale');
      if (comp === 'coppa' && !/Champions Cup/.test(st.p)) pr.push('coppa: il pannello dice ' + st.p);
      if (st.n < 8) pr.push(comp + ': squadre ' + st.n);
      if (chi === 'squadra' && (st.sq !== 'Oranje VC' || st.tit !== 'La mia partita')) pr.push(comp + ': squadra ' + st.sq + ' / ' + st.tit);
      if (chi === 'ospite' && !/^La partita di /.test(st.tit)) pr.push(comp + ': ospite ' + st.tit);
      await lato(g + comp + ' pannello');
      if (D && comp === 'lega' && M === 'chromium' && /iPhone 15/.test(sn)) await p.screenshot({ path: D + '/pannello-' + chi + '-' + g.replace(/\W+/g, '') + '.png' });
      // Tabellone ufficiale
      await p.click('[data-t=ufficiale]'); await p.waitForSelector('[data-a=sh]', { timeout: 15000 }).catch(() => {}); await p.click('[data-a=sh]').catch(() => pr.push(comp + ': niente Condividi del Tabellone ufficiale'));
      await p.waitForTimeout(300); await p.keyboard.press('Escape'); await p.waitForTimeout(400);
      // Le ultime 5 e la partita di un'altra squadra
      for (const t of ['ultime5', 'mia']) {
        await p.locator('button.cd-btn').first().click(); await p.waitForSelector('.cd-sq select'); await p.waitForTimeout(500);
        await p.selectOption('.cd-sq select', { index: 2 }); await p.click('[data-t=' + t + ']');
        await p.waitForSelector('.cd-ant img', { timeout: 15000 }).catch(async () => pr.push(comp + ' ' + t + ': nessuna immagine (' + await p.evaluate(() => (document.querySelector('.cd-err') || {}).textContent) + ')'));
        if (D && M === 'chromium' && /iPhone 15/.test(sn) && chi === 'ospite' && g === 'girrr/') { const im = await p.$('.cd-ant img'); if (im) await im.screenshot({ path: D + '/' + t + '-' + comp + '.png' }); }
        await p.keyboard.press('Escape'); await p.waitForTimeout(400);
      }
    }
    inv.push(...await p.evaluate(() => window.__inv));
    const nomi = inv.map(x => x.f.join(',')).join(' ; ');
    if (!/tabellone-lega-\d\d\.png\|image\/png/.test(nomi) || !/tabellone-coppa-\d\d\.png\|image\/png/.test(nomi)) pr.push('Tabelloni ufficiali condivisi: ' + nomi);
    // Girrr Sport: Radio e Video
    for (const [sp, sel, re] of [['radio', 'Condividi la puntata', /radio-girrr-\d+\.mp3\|audio\/mpeg/], ['video', 'Condividi il video', /o-girrr-video-\d\d\.mp4\|video\/mp4/]]) {
      await p.goto(B + g + 'app.html#' + sp); await p.waitForTimeout(2500);
      const bt = p.locator('button[data-cd-file]', { hasText: sel }).first();
      if (!(await bt.count())) { pr.push(sp + ': manca «' + sel + '»'); continue; }
      await lato(g + sp); await bt.scrollIntoViewIfNeeded(); await bt.click(); await p.waitForSelector('[data-a=sh]', { timeout: 20000 }).catch(() => {});
      await p.click('[data-a=sh]').catch(() => pr.push(sp + ': niente Condividi')); await p.waitForTimeout(300);
      const ult = await p.evaluate(() => window.__inv[window.__inv.length - 1]);
      if (!ult || !re.test(ult.f.join(',')) || ult.t) pr.push(sp + ': condiviso ' + JSON.stringify(ult));
      if (D && M === 'chromium' && /iPhone 15/.test(sn) && chi === 'ospite') await p.screenshot({ path: D + '/' + sp + '-' + g.replace(/\W+/g, '') + '.png' });
      await p.keyboard.press('Escape'); await p.waitForTimeout(300);
    }
    console.log((pr.length ? 'KO ' : 'OK ') + M + ' · ' + sn + ' · ' + chi + ' · ' + (g[0] === 's' ? 'Stadio' : 'Lega') + (pr.length ? '\n   ' + pr.join('\n   ') : ''));
    ko += pr.length; await c.close();
  }
  await br.close(); console.log(M + ': ' + ko + ' problemi'); process.exit(ko ? 1 : 0);
})();
