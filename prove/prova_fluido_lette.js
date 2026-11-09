// Versioni: cambio Messaggio/Changelog fluido; Notifiche: lette rimpicciolite (Claude, 9 novembre 2026). Serve una copia di gh-pages con versioni.js e notifiche-lette.js su http://localhost:8774/o-fant-a-girrr/
const { chromium, devices } = require('playwright');
(async () => {
  const D = process.argv[2], B = 'http://localhost:8774/o-fant-a-girrr/';
  const browser = await chromium.launch();
  const SCHERMI = [
    ['iPhone SE 1ª gen', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone 15 Pro', devices['iPhone 15 Pro']],
    ['Galaxy S8', devices['Galaxy S8']], ['Pixel 7', devices['Pixel 7']], ['iPad Mini', devices['iPad Mini']], ['Galaxy Tab S4 orizzontale', devices['Galaxy Tab S4 landscape']],
    ['PC 1280', { viewport: { width: 1280, height: 800 } }], ['PC 1920', { viewport: { width: 1920, height: 1080 } }], ['Monitor 2560', { viewport: { width: 2560, height: 1440 } }],
    ['Smart TV 4K', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 }]
  ];
  let ko = 0;
  for (const [n, opz] of SCHERMI) {
    const ctx = await browser.newContext(opz); const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(e.message));
    const pr = [];
    /* Versioni: il cambio deve passare per altezze intermedie (niente salto) e le testate non si ridisegnano */
    await page.goto(B + 'girrr/versioni.html'); await page.waitForTimeout(1500);
    await page.evaluate(() => { window.__h = document.querySelector('.vv-v .vv-h'); });
    const altezze = await page.evaluate(() => new Promise(ok => {
      const el = document.querySelector('.vv-v.aperta .vv-in'), h = []; const t0 = performance.now();
      document.querySelector('.vv-seg button[data-m=changelog]').click();
      (function giro() { h.push(Math.round(el.getBoundingClientRect().height)); if (performance.now() - t0 < 900) requestAnimationFrame(giro); else ok(h); })();
    }));
    const distinti = [...new Set(altezze)];
    const stessaTestata = await page.evaluate(() => document.querySelector('.vv-v .vv-h') === window.__h);
    if (distinti.length < 4) pr.push('Versioni: cambio a scatto (' + distinti.length + ' altezze)');
    if (!stessaTestata) pr.push('Versioni: testate ridisegnate');
    const nuovo = await page.$eval('.vv-v.aperta .vv-in', e => e.querySelector('.vv-area') ? 'changelog' : 'messaggio');
    if (nuovo !== 'changelog') pr.push('Versioni: contenuto non cambiato');
    /* Notifiche: segna tutto come letto → gruppo «Già lette» chiuso, si apre e mostra le righe compatte */
    await page.goto(B + 'stadio/girrr/notifiche.html'); await page.waitForTimeout(2200);
    const h0 = await page.evaluate(() => document.documentElement.scrollHeight);
    await page.click('#v53markread'); await page.waitForTimeout(800);
    const g = await page.$eval('.nl-h span', e => e.textContent).catch(() => null);
    if (!g || !/^Già lette · \d+$/.test(g)) pr.push('Notifiche: gruppo «' + g + '»');
    const h1 = await page.evaluate(() => document.documentElement.scrollHeight);
    if (!(h1 < h0)) pr.push('Notifiche: pagina non più corta (' + h0 + '→' + h1 + ')');
    await page.click('.nl-h'); await page.waitForTimeout(600);
    const aperte = await page.$$eval('.nl-c .v53-notifcard', c => c.filter(x => x.getBoundingClientRect().height > 0 && x.getBoundingClientRect().height < 70).length);
    if (!aperte) pr.push('Notifiche: righe compatte non visibili');
    await page.click('.v53-pill[data-f="partita"]'); await page.waitForTimeout(500);
    const g2 = await page.$eval('.nl-h span', e => e.textContent).catch(() => null); if (!g2) pr.push('Notifiche: gruppo perso dopo il filtro');
    const m = await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]); if (m[0] > m[1] + 1) pr.push('scorre di lato');
    if (n === 'iPhone 15 Pro' || n === 'PC 1920') { await page.click('.v53-pill[data-f="tutte"]'); await page.waitForTimeout(500); await page.evaluate(() => document.querySelector('#v53notifications').scrollIntoView()); await page.screenshot({ path: D + '/lette-' + n.replace(/\W+/g, '_') + '.png' }); }
    if (errs.length) pr.push('errori ' + errs.join(' / '));
    ko += pr.length;
    console.log((pr.length ? '✗ ' : '✓ ') + n + (pr.length ? ' → ' + pr.join(' | ') : ': cambio fluido (' + distinti.length + ' altezze), gruppo «' + g + '», pagina da ' + h0 + ' a ' + h1 + ' px'));
    await ctx.close();
  }
  console.log('Problemi:', ko);
  await browser.close();
})();
