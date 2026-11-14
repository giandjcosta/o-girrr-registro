// Ramificazioni con i tre disegni in cima (Claude, 14 novembre 2026): rami.html da solo e dentro ramificazioni.html.
//   BASE=http://localhost:8790/o-girrr-registro/ MOTORE=chromium|webkit|firefox node prove/prova_rami_tre_viste.js [CARTELLA_FOTO]
// Controlla: tre viste che si disegnano, cambio di repository, tocco su un ramo con i dettagli, niente scorrimento di lato,
// l'altezza del riquadro che segue il contenuto dentro Ramificazioni, nessun errore nella console.
const pw = require('playwright');
const B = process.env.BASE || 'http://localhost:8790/o-girrr-registro/', M = process.env.MOTORE || 'chromium', D = process.argv[2];
const SCH = [['iPhone SE 320', { viewport: { width: 320, height: 568 }, isMobile: M !== 'firefox', hasTouch: true }], ['iPad', { viewport: { width: 820, height: 1180 } }], ['PC 1280', { viewport: { width: 1280, height: 800 } }], ['TV', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 }]];
(async () => {
  const br = await pw[M].launch(); let ko = 0;
  for (const [sn, o] of SCH) {
    const c = await br.newContext(o), p = await c.newPage(), pr = [];
    p.on('pageerror', e => pr.push('errore: ' + e.message.slice(0, 100)));
    p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|raw\.githubusercontent/.test(m.text())) pr.push('console: ' + m.text().slice(0, 100)); });
    // da sola
    await p.goto(B + 'rami.html', { waitUntil: 'load' }); await p.waitForTimeout(1500);
    for (const v of ['albero', 'metro', 'ventaglio']) {
      await p.click('#vista [data-v=' + v + ']'); await p.waitForTimeout(700);
      const n = await p.evaluate(() => document.querySelectorAll('#box .nodo-s, #box .riga').length);
      if (n < 3) pr.push(v + ': ' + n + ' rami disegnati');
      if (await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) pr.push(v + ': scorre di lato');
    }
    await p.click('#repo [data-r="1"]'); await p.waitForTimeout(600);
    await p.click('#vista [data-v=albero]'); await p.waitForTimeout(500);
    const nodo = p.locator('#box .riga, #box .nodo-s').nth(1); if (await nodo.count()) { await nodo.click(); await p.waitForTimeout(700); if (!(await p.evaluate(() => /commit|Commit/.test((document.querySelector('.dettagli') || {}).innerText || '')))) pr.push('dettagli del ramo non aperti'); }
    // dentro Ramificazioni
    await p.goto(B + 'ramificazioni.html', { waitUntil: 'load' }); await p.waitForTimeout(3000);
    // Ramificazioni si apre dentro il portale del Registro (registro.html#ramificazioni): si cerca la sua cornice
    const fr = p.frames().find(x => /ramificazioni\.html/.test(x.url())) || p.mainFrame();
    const f = await fr.evaluate(() => { const i = document.getElementById('rami3'); return i ? { h: i.offsetHeight, dentro: i.contentDocument && i.contentDocument.documentElement.classList.contains('dentro'), tit: i.contentDocument && getComputedStyle(i.contentDocument.querySelector('.capo')).display, lato: document.documentElement.scrollWidth > innerWidth + 1 } : null; });
    if (!f) pr.push('manca il riquadro dei tre disegni'); else {
      if (!f.dentro || f.tit !== 'none') pr.push('dentro Ramificazioni il titolo si ripete');
      if (f.h < 620) pr.push('riquadro alto ' + f.h); if (f.lato) pr.push('Ramificazioni scorre di lato');
      if (await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) pr.push('il portale scorre di lato');
    }
    if (D && /PC|TV|SE/.test(sn) && M === 'chromium') await p.screenshot({ path: D + '/ramificazioni-' + sn.replace(/\W+/g, '') + '.png' });
    console.log((pr.length ? 'KO ' : 'OK ') + M + ' · ' + sn + (pr.length ? '\n   ' + pr.join('\n   ') : '')); ko += pr.length; await c.close();
  }
  await br.close(); process.exit(ko ? 1 : 0);
})();
