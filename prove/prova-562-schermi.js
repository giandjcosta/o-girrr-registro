const { chromium, devices } = require('playwright');
(async () => {
  const D = process.argv[2], B = 'https://giandjcosta.github.io/o-fant-a-girrr/';
  const browser = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
  const S = [['iPhone SE', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone 15 Pro', devices['iPhone 15 Pro']], ['Android piccolo', devices['Galaxy S5']], ['Android grande', devices['Pixel 7']],
    ['iPad verticale', devices['iPad (gen 7)']], ['iPad orizzontale', devices['iPad (gen 7) landscape']], ['Tablet Android verticale', devices['Galaxy Tab S4']], ['Tablet Android orizzontale', devices['Galaxy Tab S4 landscape']],
    ['PC 1280', { viewport: { width: 1280, height: 800 } }], ['PC 1920', { viewport: { width: 1920, height: 1080 } }], ['Monitor 2560', { viewport: { width: 2560, height: 1440 } }], ['TV 1920x1080 @2x', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 }]];
  const P = ['girrr/', 'stadio/girrr/', 'girrr/squadre.html', 'stadio/girrr/versioni.html', 'girrr/curva.html'];
  let ko = 0;
  for (const [n, o] of S) {
    const ctx = await browser.newContext(o), page = await ctx.newPage(), pr = [];
    page.on('pageerror', e => { if (!/ViewTransition/.test(e.message)) pr.push('errore ' + e.message.slice(0, 70)); });
    for (const u of P) {
      await page.goto(B + u); await page.waitForTimeout(u.includes('curva') ? 4000 : 2500);
      const r = await page.evaluate(() => ({ lato: document.documentElement.scrollWidth - innerWidth, vecchio: /The Blue brothers|THE BLUE BROTHERS/.test(document.body.innerText), nuovo: /Blues Brothers|BLUES BROTHERS/.test(document.body.innerText) }));
      if (r.lato > 1) pr.push(u + ' scorre di lato ' + r.lato + 'px');
      if (r.vecchio) pr.push(u + ' nome vecchio');
      if (/^(PC 1920|TV)/.test(n) && /^(girrr\/|stadio\/girrr\/|girrr\/squadre.html|stadio\/girrr\/versioni.html)$/.test(u))
        await page.screenshot({ path: D + '/' + n.replace(/\W+/g, '_') + '-' + u.replace(/\W+/g, '_') + '.png' });
    }
    ko += pr.length; console.log((pr.length ? '✗ ' : '✓ ') + n + (pr.length ? ' → ' + pr.join(' | ') : ''));
    await ctx.close();
  }
  console.log('Problemi:', ko); await browser.close();
})();
