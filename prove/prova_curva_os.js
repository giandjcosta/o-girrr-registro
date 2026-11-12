// Curva · Stile iPhone e stile Android (Claude, 12 novembre 2026).
// Controlla che ogni telefono riceva il suo stile (iPhone e iPad → ios, Android → android, PC e TV → altro), che la pagina
// non scorra di lato, che le animazioni partano quando cambi scheda o sezione e non all'apertura, e che non ci siano errori.
// Uso: servire la cartella che contiene o-girrr-registro e una copia di gh-pages come o-fant-a-girrr su http://localhost:8771/, poi
//   node prove/prova_curva_os.js [CARTELLA_FOTO]
// Il database si legge soltanto: le funzioni che scrivono sono intercettate.
const { chromium, devices } = require('playwright');
const L = 'http://localhost:8771/o-girrr-registro/lab/offline/';
const D = process.argv[2];
const TV = 'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36';
const SCH = [
  ['iPhone SE 320', 'ios', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone 15 Pro', 'ios', devices['iPhone 15 Pro']], ['iPhone 15 Pro Max', 'ios', devices['iPhone 15 Pro Max']],
  ['Galaxy S8', 'android', devices['Galaxy S8']], ['Pixel 7', 'android', devices['Pixel 7']], ['Galaxy S24', 'android', devices['Galaxy S24'] || devices['Galaxy S9+']],
  ['iPad Mini', 'ios', devices['iPad Mini']], ['iPad orizzontale', 'ios', devices['iPad (gen 7) landscape']], ['Galaxy Tab S4', 'android', devices['Galaxy Tab S4']], ['Galaxy Tab S4 orizzontale', 'android', devices['Galaxy Tab S4 landscape']],
  ['PC 1280', 'altro', { viewport: { width: 1280, height: 800 } }], ['PC 1920', 'altro', { viewport: { width: 1920, height: 1080 } }],
  ['Monitor 2560', 'altro', { viewport: { width: 2560, height: 1440 } }], ['Smart TV', 'altro', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: TV }]
];
const SCRIVE = /salva|scrivi|lancia|rispondi|vota|reagisci|registra|segui|push_|cancella|proponi/;
(async () => {
  const b = await chromium.launch(); let ko = 0;
  for (const [sn, att, o] of SCH) {
    const c = await b.newContext(o);
    await c.route('**/rest/v1/rpc/**', async r => { const n = r.request().url().split('/rpc/')[1].split('?')[0]; if (SCRIVE.test(n) && !/_(stato|pubblico|lista)$/.test(n)) return r.fulfill({ json: null }); return r.continue(); });
    const p = await c.newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message.slice(0, 90)));
    await p.goto(L); await p.waitForTimeout(2500); const pr = [];
    for (const [pn, u] of [['Lega', 'sito/girrr/curva.html'], ['Stadio', 'sito/stadio/girrr/curva.html']]) {
      await p.goto(L + u); await p.waitForSelector('#nav button', { timeout: 20000 }); await p.waitForTimeout(1500);
      const i = await p.evaluate(() => ({ os: document.documentElement.dataset.os, sw: document.documentElement.scrollWidth, w: innerWidth, c: document.documentElement.hasAttribute('data-cambio-nav') || document.documentElement.hasAttribute('data-cambio-tabs') }));
      if (i.os !== att) pr.push(pn + ': stile ' + i.os); if (i.sw > i.w + 1) pr.push(pn + ': scorre di lato ' + i.sw); if (i.c) pr.push(pn + ': animazione all\'apertura');
      if (D) await p.screenshot({ path: D + '/curva-' + pn + '-' + sn.replace(/\W+/g, '_') + '.png' });
      const tb = await p.$$('.tabs button');
      if (tb.length > 1) {
        await tb[1].click(); await p.waitForTimeout(60);
        const a = await p.evaluate(() => { const os = document.documentElement.dataset.os, e = document.querySelector('.tabs .on'); return { c: document.documentElement.hasAttribute('data-cambio-tabs'), an: e ? getComputedStyle(e, os === 'android' ? '::after' : null).animationName : '-' }; });
        if (att !== 'altro' && (!a.c || a.an === 'none')) pr.push(pn + ': niente animazione delle schede ' + JSON.stringify(a));
        await p.waitForTimeout(800);
      }
      if (o.viewport.width < 760) {
        await p.click('#nav button[data-v=esplora]'); await p.waitForTimeout(60);
        const a = await p.evaluate(() => { const os = document.documentElement.dataset.os, e = document.querySelector('#nav .on'); return { c: document.documentElement.hasAttribute('data-cambio-nav'), an: getComputedStyle(os === 'android' ? e.querySelector('svg') : e).animationName }; });
        if (att !== 'altro' && (!a.c || a.an === 'none')) pr.push(pn + ': niente animazione della barra ' + JSON.stringify(a));
        await p.waitForTimeout(800);
        const sw = await p.evaluate(() => document.documentElement.scrollWidth); if (sw > o.viewport.width + 1) pr.push(pn + ' Esplora: scorre di lato');
        if (D && /Pixel 7|iPhone 15 Pro$/.test(sn)) await p.screenshot({ path: D + '/curva-' + pn + '-' + sn.replace(/\W+/g, '_') + '-esplora.png' });
      }
    }
    if (errs.length) pr.push('errori JS: ' + [...new Set(errs)].join(' / '));
    ko += pr.length;
    console.log((pr.length ? '✗ ' : '✓ ') + sn + ' (' + att + ')' + (pr.length ? ' → ' + pr.join(' | ') : ''));
    await c.close();
  }
  console.log(ko ? 'Problemi: ' + ko : 'Tutto a posto'); await b.close();
})();
