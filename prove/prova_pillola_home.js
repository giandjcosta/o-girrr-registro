const { chromium, devices } = require('playwright');
(async () => {
  const D = process.argv[2], B = 'http://localhost:8774/o-fant-a-girrr/';
  const browser = await chromium.launch();
  const SCHERMI = [
    ['iPhone SE 1ª gen', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone SE', devices['iPhone SE']], ['iPhone 15 Pro', devices['iPhone 15 Pro']], ['iPhone 15 Pro Max', devices['iPhone 15 Pro Max']],
    ['Galaxy S8', devices['Galaxy S8']], ['Pixel 7', devices['Pixel 7']], ['Galaxy S24', devices['Galaxy S24'] || devices['Galaxy S9+']],
    ['iPad Mini', devices['iPad Mini']], ['iPad orizzontale', devices['iPad (gen 7) landscape']], ['iPad Pro 11', devices['iPad Pro 11']],
    ['Galaxy Tab S4', devices['Galaxy Tab S4']], ['Galaxy Tab S4 orizzontale', devices['Galaxy Tab S4 landscape']],
    ['PC 1280', { viewport: { width: 1280, height: 800 } }], ['PC 1920', { viewport: { width: 1920, height: 1080 } }], ['Monitor 2560', { viewport: { width: 2560, height: 1440 } }],
    ['Smart TV 4K', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 }]
  ];
  let ko = 0;
  for (const [n, opz] of SCHERMI) {
    const ctx = await browser.newContext(opz); const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(e.message));
    const pr = [];
    for (const sk of ['girrr', 'stadio/girrr']) {
      const nome = sk === 'girrr' ? 'Lega' : 'Stadio';
      await page.goto(B + sk + '/'); await page.waitForTimeout(2200);
      const r = await page.evaluate(() => {
        const p = document.querySelector('.vv-fondo'), sp = document.querySelector('.sp');
        if (!p) return { manca: true };
        const a = p.getBoundingClientRect(), b = sp ? sp.getBoundingClientRect() : null, w = (p.parentNode).getBoundingClientRect();
        return { testo: p.textContent, sopra: b ? a.bottom <= b.top + 1 : null, destra: Math.abs(a.right - w.right) < 2, prima: p.nextElementSibling && p.nextElementSibling.className, sw: document.documentElement.scrollWidth, vw: innerWidth };
      });
      if (r.manca) { pr.push(nome + ': manca'); continue; }
      if (r.testo !== 'V5.6 ›') pr.push(nome + ': «' + r.testo + '»');
      if (!r.sopra || r.prima !== 'sp') pr.push(nome + ': non sopra gli sponsor');
      if (!r.destra) pr.push(nome + ': non a destra');
      if (r.sw > r.vw + 1) pr.push(nome + ': scorre di lato');
      const nt = await page.$('a.vv-fondo'); await nt.click(); await page.waitForTimeout(1500);
      if (!/versioni\.html$/.test(new URL(page.url()).pathname)) pr.push(nome + ': il tocco non apre Versioni');
      await page.goto(B + sk + '/notifiche.html'); await page.waitForTimeout(1500);
      if (await page.$('.vv-fondo')) pr.push(nome + ': ancora nelle Notifiche');
      if (['iPhone 15 Pro', 'PC 1920', 'Smart TV 4K', 'iPad Mini'].includes(n)) {
        await page.goto(B + sk + '/'); await page.waitForTimeout(1800);
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); await page.waitForTimeout(400);
        await page.screenshot({ path: D + '/home-pill-' + nome + '-' + n.replace(/\W+/g, '_') + '.png' });
      }
    }
    if (errs.length) pr.push('errori ' + errs.join(' / '));
    ko += pr.length;
    console.log((pr.length ? '✗ ' : '✓ ') + n + (pr.length ? ' → ' + pr.join(' | ') : ': V5.6 › in fondo a destra sopra gli sponsor, Lega e Stadio, apre Versioni'));
    await ctx.close();
  }
  console.log('Problemi:', ko);
  await browser.close();
})();
