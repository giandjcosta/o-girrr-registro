// Versioni: nessuna emoji da sola su una riga, su 16 schermi (Claude, 9 novembre 2026). Serve la copia di gh-pages con rilascio56.py su http://localhost:8771/o-fant-a-girrr/
const { chromium, devices } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const SCHERMI = [
    ['iPhone SE 1ª gen', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone SE', devices['iPhone SE']],
    ['iPhone 15 Pro', devices['iPhone 15 Pro']], ['iPhone 15 Pro Max', devices['iPhone 15 Pro Max']],
    ['Galaxy S8', devices['Galaxy S8']], ['Pixel 7', devices['Pixel 7']], ['Galaxy S24', devices['Galaxy S24'] || devices['Galaxy S9+']],
    ['iPad Mini', devices['iPad Mini']], ['iPad orizzontale', devices['iPad (gen 7) landscape']], ['iPad Pro 11', devices['iPad Pro 11']],
    ['Galaxy Tab S4', devices['Galaxy Tab S4']], ['Galaxy Tab S4 orizzontale', devices['Galaxy Tab S4 landscape']],
    ['PC 1280', { viewport: { width: 1280, height: 800 } }], ['PC 1920', { viewport: { width: 1920, height: 1080 } }],
    ['Monitor 2560', { viewport: { width: 2560, height: 1440 } }], ['Smart TV 4K', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 }]
  ];
  let tot = 0;
  for (const [n, opz] of SCHERMI) {
    const ctx = await browser.newContext(opz); const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(e.message));
    const sole = [];
    for (const sk of ['girrr', 'stadio/girrr']) {
      await page.goto('http://localhost:8771/o-fant-a-girrr/' + sk + '/versioni.html'); await page.waitForTimeout(1500);
      await page.evaluate(() => document.querySelectorAll('.vv-v:not(.aperta) .vv-h').forEach(b => b.click()));
      await page.waitForTimeout(700);
      const r = await page.evaluate(() => {
        const re = /(?:\p{Extended_Pictographic}|️|‍)+/gu, out = [];
        document.querySelectorAll('.vv-msg').forEach(msg => {
          const v = msg.closest('.vv-v').dataset.v;
          const tw = document.createTreeWalker(msg, NodeFilter.SHOW_TEXT); let nodo;
          const testi = []; while ((nodo = tw.nextNode())) testi.push(nodo);
          testi.forEach(t => {
            let m; re.lastIndex = 0;
            while ((m = re.exec(t.data))) {
              const rg = document.createRange(); rg.setStart(t, m.index); rg.setEnd(t, m.index + m[0].length);
              const er = rg.getClientRects()[0]; if (!er) continue;
              /* la riga dell'emoji: tutti i pezzi di testo del messaggio sulla stessa altezza */
              const tutto = document.createRange(); tutto.selectNodeContents(msg);
              const stessa = Array.from(tutto.getClientRects()).filter(q => Math.abs(q.top - er.top) < 4 && q.width > 0);
              const larg = stessa.reduce((a, q) => a + q.width, 0);
              if (larg <= er.width + 6) out.push(v + ': «' + m[0] + '» da sola');
            }
          });
        });
        return out;
      });
      r.forEach(x => sole.push(sk.replace('/girrr', '').replace('girrr', 'Lega') + ' ' + x));
    }
    tot += sole.length;
    console.log((sole.length ? '✗ ' : '✓ ') + n + (sole.length ? ' → ' + sole.join(' | ') : ': nessuna emoji da sola') + (errs.length ? ' ERRORI ' + errs : ''));
    if (n === 'iPhone SE 1ª gen') { await page.evaluate(() => document.querySelector('.vv-v[data-v="3.0"]').scrollIntoView()); await page.screenshot({ path: process.argv[2] + '/emoji-320.png' }); }
    await ctx.close();
  }
  console.log('Emoji da sole in tutto:', tot);
  await browser.close();
})();
