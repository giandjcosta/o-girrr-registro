const { chromium, devices } = require('playwright');
const fs = require('fs');
(async () => {
  const D = process.argv[2], B = process.argv[3] || 'http://localhost:8774/o-fant-a-girrr/';
  const vero = /github\.io/.test(B);
  const browser = await chromium.launch(vero ? { proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] } : {});
  let ko = 0;
  for (const [n, opz] of [['iPhone 15 Pro', devices['iPhone 15 Pro']], ['Pixel 7', devices['Pixel 7']], ['PC 1440', { viewport: { width: 1440, height: 900 } }]]) {
    for (const sk of ['girrr', 'stadio/girrr']) {
      const ctx = await browser.newContext({ ...opz, acceptDownloads: true }); const page = await ctx.newPage();
      const errs = []; page.on('pageerror', e => { if (!/ViewTransition/.test(e.message)) errs.push(e.message.slice(0, 90)); });
      await page.goto(B + sk + '/curva.html'); await page.waitForTimeout(5000);
      let chiavi = [];
      for (let i = 0; i < 40 && chiavi.length < 2; i++) {
        chiavi = await page.$$eval('article.post[data-k]', a => a.filter(x => /Fine giornata/.test(x.textContent) && x.querySelector('.pimg img')).map(x => x.dataset.k).slice(0, 2));
        if (chiavi.length >= 2) break;
        await page.evaluate(() => window.scrollBy(0, 2500)); await page.waitForTimeout(700);
      }
      const righe = [];
      for (const k of chiavi) {
        const art = await page.$('article.post[data-k="' + k + '"]');
        await art.scrollIntoViewIfNeeded(); await page.waitForTimeout(1500);
        const visibile = await art.$eval('.pimg img', i => i.complete && i.naturalWidth > 0 && i.offsetParent !== null ? i.getAttribute('src') : 'non caricata').catch(() => 'nessuna');
        const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 15000 }), art.$eval('[data-a="shr"]', b => b.click())]);
        const f = D + '/curva-cond-' + sk.replace('/', '-') + '-' + k.replace(/\W+/g, '_') + '-' + n.replace(/\W+/g, '_') + '.png';
        await dl.saveAs(f);
        const buf = fs.readFileSync(f), h = buf.readUInt32BE(20);
        righe.push(k + ': immagine nel post ' + visibile + ' → condivisa alta ' + h + ' px');
        if (h < 900) { ko++; righe.push('  SENZA IMMAGINE'); }
      }
      if (!chiavi.length) righe.push('nessun post dei risultati trovato');
      if (errs.length) { ko++; righe.push('errori ' + errs.join(' / ')); }
      console.log(n + ' · ' + (sk === 'girrr' ? 'Lega' : 'Stadio') + ': ' + righe.join(' | '));
      await ctx.close();
    }
  }
  console.log('Problemi:', ko);
  await browser.close();
})();
