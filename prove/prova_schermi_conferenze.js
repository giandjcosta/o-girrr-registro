// Novità delle conferenze su 16 schermi (Claude, 10 novembre 2026): Conferenza (con l'avversario), Promesse, Testa a testa, Curva con ?scrivi=.
// Uso: servire una copia di gh-pages con rilascio/conferenze/applica.py applicato su http://localhost:8771/o-fant-a-girrr/, poi:
//   node prove/prova_schermi_conferenze.js CARTELLA_FOTO      (foto su PC 1920 e TV per Gianluca)
// Il database si legge soltanto: le funzioni che scrivono sono intercettate e non partono.
const { chromium, devices } = require('playwright');
const B = 'http://localhost:8771/o-fant-a-girrr/';
const D = process.argv[2];
const TV = 'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36';
const SCHERMI = [
  ['iPhone SE (1ª gen) iOS', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }],
  ['iPhone SE iOS', devices['iPhone SE']], ['iPhone 15 Pro iOS', devices['iPhone 15 Pro']], ['iPhone 15 Pro Max iOS', devices['iPhone 15 Pro Max']],
  ['Galaxy S8 Android', devices['Galaxy S8']], ['Pixel 7 Android', devices['Pixel 7']], ['Galaxy S24 Android', devices['Galaxy S24'] || devices['Galaxy S9+']],
  ['iPad Mini iOS', devices['iPad Mini']], ['iPad (gen 7) orizzontale iOS', devices['iPad (gen 7) landscape']], ['iPad Pro 11 iOS', devices['iPad Pro 11']],
  ['Galaxy Tab S4 Android', devices['Galaxy Tab S4']], ['Galaxy Tab S4 orizzontale Android', devices['Galaxy Tab S4 landscape']],
  ['PC 1280', { viewport: { width: 1280, height: 800 } }], ['PC 1920', { viewport: { width: 1920, height: 1080 } }],
  ['Monitor 2560', { viewport: { width: 2560, height: 1440 } }], ['Smart TV 4K', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: TV }]
];
const PAGINE = [
  ['Conferenza Lega', 'girrr/app.html#conf', '.cf-avv'], ['Conferenza Stadio', 'stadio/girrr/app.html#conf', '.cf-avv'], ['Sala stampa e dopo partita Lega', 'girrr/app.html#conf', '.cf-dopo'], ['Sala stampa e dopo partita Stadio', 'stadio/girrr/app.html#conf', '.cf-sala-dopo'],
  ['Promesse Lega', 'girrr/app.html#carriera', '.cf-pr'], ['Promesse Stadio', 'stadio/girrr/app.html#carriera', '.cf-pr'],
  ['Derby Lega', 'girrr/app.html#derby', '.cf-tt'], ['Derby Stadio', 'stadio/girrr/app.html#derby', '.cf-tt'],
  ['Curva Lega', 'girrr/curva.html?come=Oranje%20VC&scrivi=%40mariana_coneja%20', '#tx']
];
const SCRIVE = /salva|scrivi|lancia|rispondi|vota|reagisci|registra|cancella|proponi|riscuoti|duello_|toto_|push_|segui|sondaggio|carriera_/;
(async () => {
  const browser = await chromium.launch();
  let ko = 0;
  for (const [nome, opz] of SCHERMI) {
    const ctx = await browser.newContext(opz);
    await ctx.addInitScript(() => { try { localStorage.setItem('fg', JSON.stringify({ team: 'Oranje VC', code: 'PROVA' })); } catch (e) {} });
    await ctx.route('**/rest/v1/rpc/**', async (route) => {
      const n = route.request().url().split('/rpc/')[1].split('?')[0];
      if (n === 'derby_stato') return route.fulfill({ json: { ok: true, sfide: [], voti: [], miei: [], conf: [] } });
      if (n === 'curva_feed') { const r = await route.fetch(); const j = await r.json(); return route.fulfill({ json: Object.assign(j, { ok: true }) }); }
      if (SCRIVE.test(n) && !/_(stato|pubblico|lista)$/.test(n)) return route.fulfill({ json: null });
      return route.continue();
    });
    const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(e.message.slice(0, 80)));
    const problemi = [];
    for (const [pn, u, sel] of PAGINE) {
      try {
        await page.goto(B + u); await page.waitForTimeout(1200);
        if (pn.startsWith('Promesse')) await page.click('[data-ctab="prom"]');
        await page.waitForSelector(sel, { timeout: 15000 }); await page.waitForTimeout(500);
        const m = await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
        if (m[0] > m[1] + 1) problemi.push(pn + ': scorre di lato ' + m[0] + '>' + m[1]);
        const fuori = await page.$eval(sel, e => { const r = e.getBoundingClientRect(); return r.right > innerWidth + 1 || r.left < -1; });
        if (fuori) problemi.push(pn + ': riquadro fuori dallo schermo');
        if (D && /^(PC 1920|Smart TV 4K)$/.test(nome) && !pn.startsWith('Curva')) {
          await page.$eval(sel, e => e.scrollIntoView({ block: 'start' })); await page.waitForTimeout(300);
          await page.screenshot({ path: D + '/' + pn.replace(/\W+/g, '_') + '-' + nome.replace(/\W+/g, '_') + '.png' });
        }
      } catch (e) { problemi.push(pn + ': ' + e.message.split('\n')[0].slice(0, 90)); }
    }
    if (errs.length) problemi.push('errori JS: ' + errs.join(' / '));
    ko += problemi.length;
    console.log((problemi.length ? '✗ ' : '✓ ') + nome + (problemi.length ? ' → ' + problemi.join(' | ') : ': tutte le ' + PAGINE.length + ' pagine a posto'));
    await ctx.close();
  }
  console.log('Problemi in tutto:', ko);
  await browser.close();
  process.exit(ko ? 1 : 0);
})();
