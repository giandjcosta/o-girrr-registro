const { chromium, devices } = require('playwright');
(async () => {
  const D = process.argv[2], B = process.argv[3] || 'http://localhost:8774/o-fant-a-girrr/';
  const vero = /github\.io/.test(B);
  const browser = await chromium.launch(vero ? { proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] } : {});
  const PAGINE = ['girrr/', 'stadio/girrr/', 'girrr/tabellone.html', 'stadio/girrr/tabellone.html', 'girrr/curva.html', 'girrr/squadre.html', 'girrr/albo.html', 'girrr/app.html#carriera', 'girrr/notifiche.html', 'girrr/versioni.html', 'girrr/statistiche.html', 'girrr/totogirrr.html', 'riepilogo.html', 'index.html'];
  let ko = 0;
  for (const [n, opz] of [['iPhone SE 1ª gen', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['Pixel 7', devices['Pixel 7']], ['iPad Mini', devices['iPad Mini']], ['PC 1920', { viewport: { width: 1920, height: 1080 } }]]) {
    const ctx = await browser.newContext(opz);
    await ctx.addInitScript(() => { try { localStorage.setItem('fg', JSON.stringify({ team: 'The Blue brothers', code: 'PROVA' })); } catch (e) {} });
    const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => { if (!/ViewTransition/.test(e.message)) errs.push(e.message.slice(0, 80)); });
    const pr = [];
    for (const u of PAGINE) {
      await page.goto(B + u); await page.waitForTimeout(u.indexOf('curva') >= 0 ? 4500 : 2500);
      const r = await page.evaluate(() => {
        const t = document.body.innerText;
        return { vecchio: (t.match(/The Blue brothers|THE BLUE BROTHERS|The Blue Brothers/g) || []).length, nuovo: (t.match(/The Blues Brothers|THE BLUES BROTHERS/g) || []).length,
          opzioni: Array.from(document.querySelectorAll('option')).filter(o => /Blues Brothers/.test(o.text)).map(o => o.value) };
      });
      if (r.vecchio) pr.push(u + ': ancora ' + r.vecchio + '× il nome vecchio');
      if (r.opzioni.some(v => v !== 'The Blue brothers')) pr.push(u + ': valore del menu cambiato ' + r.opzioni.join(','));
      if (u === 'index.html#PROVA') {
        const dentro = await page.$('#tabs [data-t=cerca]').then(x => x && x.isVisible()).catch(() => false);
        if (!dentro) pr.push('Spogliatoio: accesso con il codice non riuscito');
        const nome = await page.$eval('#who', e => e.innerText).catch(() => '');
        if (!/Blues Brothers/.test(nome)) pr.push('Spogliatoio: in alto «' + nome.slice(0, 40) + '»');
      }
    }
    if (errs.length) pr.push('errori ' + errs.join(' / '));
    ko += pr.length;
    console.log((pr.length ? '✗ ' : '✓ ') + n + (pr.length ? ' → ' + pr.join(' | ') : ': nome nuovo su ' + PAGINE.length + ' pagine, chiavi e accesso intatti'));
    if (n === 'Pixel 7') { await page.goto(B + 'girrr/tabellone.html'); await page.waitForTimeout(2500); await page.screenshot({ path: D + '/nomi-tabellone.png' }); }
    await ctx.close();
  }
  console.log('Problemi:', ko);
  await browser.close();
})();
