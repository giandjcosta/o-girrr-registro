// Prova della 6.6 su 16 schermi (Claude, 24 novembre 2026), sul Lab: Spogliatoio › Mercato Scambi con le richieste,
// Notifiche Lega e Stadio (icona dell'app), Tabellone. Uso: servire la radice del registro su http://localhost:8773/, poi
// node prove/v66/prova_schermi_66.js CARTELLA_FOTO   (scrive le foto di PC e TV e stampa scorrimento laterale ed errori in console)
const { chromium, devices } = require('playwright');
(async () => {
  const D = process.argv[2], B = 'http://localhost:8773/lab/integrata-62/';
  const browser = await chromium.launch();
  const SCHERMI = [
    ['iPhone SE (1ª gen) iOS', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone SE iOS', devices['iPhone SE']],
    ['iPhone 15 Pro iOS', devices['iPhone 15 Pro']], ['iPhone 15 Pro Max iOS', devices['iPhone 15 Pro Max']],
    ['Galaxy S8 Android', devices['Galaxy S8']], ['Pixel 7 Android', devices['Pixel 7']], ['Galaxy S9+ Android', devices['Galaxy S9+']],
    ['iPad Mini iOS', devices['iPad Mini']], ['iPad (gen 7) orizzontale iOS', devices['iPad (gen 7) landscape']], ['iPad Pro 11 iOS', devices['iPad Pro 11']],
    ['Galaxy Tab S4 Android', devices['Galaxy Tab S4']], ['Galaxy Tab S4 orizzontale Android', devices['Galaxy Tab S4 landscape']],
    ['PC 1280', { viewport: { width: 1280, height: 800 } }], ['PC 1920', { viewport: { width: 1920, height: 1080 } }],
    ['Monitor 2560', { viewport: { width: 2560, height: 1440 } }],
    ['Smart TV', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36' }]
  ];
  const PAGINE = [['spogliatoio', 'index.html?squadra=Oranje%20VC', true], ['notifiche-lega', 'girrr/notifiche.html?demo'], ['notifiche-stadio', 'stadio/girrr/notifiche.html?demo'], ['tabellone', 'girrr/tabellone.html']];
  let male = 0;
  for (const [nome, prof] of SCHERMI) for (const [pn, u, mkt] of PAGINE) {
    const c = await browser.newContext({ ...prof }); const p = await c.newPage(); const err = [];
    p.on('pageerror', e => err.push(e.message)); p.on('console', m => { if (m.type() === 'error') err.push(m.text()); });
    await p.goto(B + u, { waitUntil: 'networkidle' }); await p.waitForTimeout(900);
    if (mkt) { await p.click('#tabs button[data-t="mkt"]'); await p.waitForTimeout(1300); }
    if (pn.startsWith('notifiche')) { const x = p.locator('#ic66'); if (await x.count()) await x.scrollIntoViewIfNeeded(); }
    const sw = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
    const ok = mkt ? await p.locator('#sc66 article').count() : pn.startsWith('notifiche') ? await p.locator('#ic66').count() : 1;
    if (/PC|TV|Monitor/.test(nome)) await p.screenshot({ path: `${D}/${pn}-${nome.replace(/\W+/g, '-')}.png` });
    const r = !sw && ok && !err.length; if (!r) male++;
    console.log(`${r ? 'ok  ' : 'MALE'} ${nome} · ${pn} | scorre di lato: ${sw} | contenuto 6.6: ${ok} | ${err.join(' ; ') || 'console pulita'}`);
    await c.close();
  }
  console.log(male ? `${male} casi da guardare` : 'Tutti i casi a posto'); await browser.close();
})();
