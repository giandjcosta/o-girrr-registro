// Prova della 5.6 su 16 schermi (Claude, 9 novembre 2026). Uso: servire una copia di gh-pages con rilascio56.py applicato su http://localhost:8771/o-fant-a-girrr/ (accesso di prova per lo Spogliatoio), poi: node prove/prova_schermi_56.js CARTELLA_FOTO
const { chromium, devices } = require('playwright');
(async () => {
  const D = process.argv[2];
  const browser = await chromium.launch();
  const B = 'http://localhost:8771/o-fant-a-girrr/';
  const SCHERMI = [
    ['iPhone SE (1ª gen) iOS', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }],
    ['iPhone SE iOS', devices['iPhone SE']],
    ['iPhone 15 Pro iOS', devices['iPhone 15 Pro']],
    ['iPhone 15 Pro Max iOS', devices['iPhone 15 Pro Max']],
    ['Galaxy S8 Android', devices['Galaxy S8']],
    ['Pixel 7 Android', devices['Pixel 7']],
    ['Galaxy S24 Android', devices['Galaxy S24'] || devices['Galaxy S9+']],
    ['iPad Mini iOS', devices['iPad Mini']],
    ['iPad (gen 7) orizzontale iOS', devices['iPad (gen 7) landscape']],
    ['iPad Pro 11 iOS', devices['iPad Pro 11']],
    ['Galaxy Tab S4 Android', devices['Galaxy Tab S4']],
    ['Galaxy Tab S4 orizzontale Android', devices['Galaxy Tab S4 landscape']],
    ['PC 1280', { viewport: { width: 1280, height: 800 } }],
    ['PC 1920', { viewport: { width: 1920, height: 1080 } }],
    ['Monitor 2560', { viewport: { width: 2560, height: 1440 } }],
    ['Smart TV 4K', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36' }]
  ];
  const PAGINE = [
    ['Home Lega', 'girrr/'], ['Home Stadio', 'stadio/girrr/'],
    ['Versioni Lega', 'girrr/versioni.html'], ['Versioni Stadio', 'stadio/girrr/versioni.html'],
    ['Notifiche Lega', 'girrr/notifiche.html'], ['Notifiche Stadio', 'stadio/girrr/notifiche.html?demo'],
    ['Spogliatoio Cerca', 'index.html#PROVA'],
    ['Tabellone Condividi', 'girrr/tabellone.html'], ['Giornale Condividi', 'stadio/girrr/giornale.html'],
    ['Carriera Stagione Lega', 'girrr/app.html#carriera'], ['Carriera Stagione Stadio', 'stadio/girrr/app.html#carriera']
  ];
  let ko = 0;
  for (const [nome, opz] of SCHERMI) {
    const ctx = await browser.newContext(opz);
    await ctx.addInitScript(() => { try { localStorage.setItem('fg', JSON.stringify({ team: 'The Blue brothers', code: 'PROVA' })); } catch (e) {} });
    const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(e.message.slice(0, 80)));
    const problemi = [];
    for (const [pn, u] of PAGINE) {
      try {
        await page.goto(B + u); await page.waitForTimeout(1600);
        if (pn === 'Spogliatoio Cerca') { await page.click('#tabs [data-t=cerca]'); await page.fill('#app .gc input', 'malen'); await page.waitForTimeout(700); await page.click('#app .gc-lista button'); await page.waitForTimeout(400); }
        if (pn.startsWith('Tabellone') || pn.startsWith('Giornale')) { await page.click('.cd-btn'); await page.waitForTimeout(400); if (pn.startsWith('Tabellone')) await page.click('.cd-sc button[data-t=classifica]'); await page.waitForSelector('.cd-ant img', { timeout: 15000 }); }
        if (pn.startsWith('Carriera')) { await page.click('[data-ctab="stag"]'); await page.waitForSelector('.ms-c', { timeout: 15000 }); }
        if (pn.startsWith('Notifiche')) {
          const v = await page.$('.vv-fondo'); if (!v) problemi.push(pn + ': manca V5.6');
          else {
            const t = await v.textContent(); const top = await v.evaluate(e => e.getBoundingClientRect().top), h = await page.evaluate(() => innerHeight);
            if (t !== 'V5.6') problemi.push(pn + ': scritta ' + t);
            if (top < h) problemi.push(pn + ': V5.6 visibile senza scorrere');
          }
          if (!(await page.$('.pt'))) problemi.push(pn + ': manca il riquadro notifiche');
        }
        const m = await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
        if (m[0] > m[1] + 1) problemi.push(pn + ': scorre di lato ' + m[0] + '>' + m[1]);
        if (['Versioni Lega', 'Notifiche Stadio', 'Carriera Stagione Stadio'].includes(pn)) {
          if (pn.startsWith('Notifiche')) await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          if (pn.startsWith('Carriera')) await page.evaluate(() => document.querySelector('.ms-scorri').scrollIntoView({ block: 'center' }));
          await page.waitForTimeout(300);
          await page.screenshot({ path: D + '/dev-' + pn.replace(/\W+/g, '_') + '-' + nome.replace(/\W+/g, '_') + '.png' });
        }
      } catch (e) { problemi.push(pn + ': ' + e.message.split('\n')[0].slice(0, 90)); }
    }
    if (errs.length) problemi.push('errori JS: ' + errs.join(' / '));
    ko += problemi.length;
    console.log((problemi.length ? '✗ ' : '✓ ') + nome + (problemi.length ? ' → ' + problemi.join(' | ') : ': tutte le 11 pagine a posto'));
    await ctx.close();
  }
  console.log('Problemi in tutto:', ko);
  await browser.close();
})();
