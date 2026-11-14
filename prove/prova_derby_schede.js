// Derby in tre schede (6.0.1, Claude, 13 novembre 2026): Derby della Lega, Le rivalità, Classifica dei Derby.
//   BASE=http://localhost:8772/o-fant-a-girrr/ MOTORE=chromium|webkit|firefox node prove/prova_derby_schede.js [CARTELLA_FOTO]
// Controlla, in Lega e Stadio: le tre schede stanno direttamente in Albo › Derby (niente cambio di pagina), una sola visibile;
// derby.html, derby.html#rivalita, #pt-derby e rivalita.html portano lì sulla scheda giusta; Classifica dei Derby dentro la terza
// scheda; le altre schede dell'Albo funzionano ancora; niente scorrimento di lato a 320 px, nessun errore.
const pw = require('playwright'), { devices } = pw;
const { script: BLOCCA } = require('./blocca_scritture');
const B = process.env.BASE || 'http://localhost:8772/o-fant-a-girrr/', MOTORE = process.env.MOTORE || 'chromium', D = process.argv[2];
const SCH = [['iPhone SE 320', { viewport: { width: 320, height: 568 } }], ['Pixel 7', { viewport: { width: 412, height: 915 } }], ['iPad', { viewport: { width: 820, height: 1180 } }], ['PC 1920', { viewport: { width: 1920, height: 1080 } }], ['Smart TV', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 }]];
(async () => {
  const br = await require('./browser_certificato').browser(MOTORE); let ko = 0;
  for (const [sn, o] of SCH) for (const g of ['girrr/', 'stadio/girrr/']) {
    const c = await br.newContext(o); await c.addInitScript(BLOCCA); const p = await c.newPage(), pr = [];
    p.on('pageerror', e => pr.push('errore: ' + e.message.slice(0, 100)));
    p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) pr.push('console: ' + m.text().slice(0, 100)); });
    p.on('response', r => { if (r.status() >= 400 && !/notifiche_stato/.test(r.url())) pr.push('risposta ' + r.status() + ' ' + r.url().slice(-60)); });
    const casi = [['derby.html', 'lega'], ['derby.html#rivalita', 'rivalita'], ['derby.html#pt-derby', 'classifica'], ['rivalita.html', 'rivalita'], ['albo.html#derby', 'lega'], ['albo.html?sez=classifica#derby', 'classifica']];
    for (const [u, atteso] of casi) {
      await p.goto('about:blank'); await p.goto(B + g + u, { waitUntil: 'load' }); await p.waitForSelector('#der-root [data-dsez]', { timeout: 20000 }).catch(() => {});
      await p.waitForTimeout(1800);
      const r = await p.evaluate(() => ({ n: document.querySelectorAll('#der-root [data-dsez]').length, sel: (document.querySelector('[data-dsez][aria-selected=true]') || {}).dataset?.dsez,
        vis: [...document.querySelectorAll('[data-dp]')].filter(x => !x.hidden).map(x => x.dataset.dp), cls: !!document.querySelector('#der-cls #pt-derby'),
        fuori: document.querySelectorAll('#pt-derby').length, lato: document.documentElement.scrollWidth > innerWidth + 1, pag: location.pathname.split('/').pop(),
        albo: (document.querySelector('[data-at][aria-selected=true]') || {}).dataset?.at, carte: document.querySelectorAll('[data-ap="derby"] a.card').length }));
      if (r.pag !== 'albo.html') pr.push(u + ': resta su ' + r.pag);
      if (r.albo !== 'derby') pr.push(u + ': scheda dell\'Albo ' + r.albo);
      if (r.n !== 3) pr.push(u + ': ' + r.n + ' schede');
      if (r.carte) pr.push(u + ': ancora ' + r.carte + ' riquadri-collegamento in Albo › Derby');
      if (r.sel !== atteso || r.vis.join() !== atteso) pr.push(u + ': scheda ' + r.sel + ' / visibile ' + r.vis + ' invece di ' + atteso);
      if (!r.cls || r.fuori !== 1) pr.push(u + ': Classifica dei Derby fuori dalla sua scheda');
      if (r.lato) pr.push(u + ': scorre di lato');
      if (D && u === 'albo.html?sez=classifica#derby' && /PC 1920|Smart TV|iPhone SE 320/.test(sn) && MOTORE === 'chromium') await p.screenshot({ path: D + '/classifica-' + sn.replace(/\W+/g, '-') + '-' + (g[0] === 's' ? 'stadio' : 'lega') + '.png' });
    }
    // clic sulle schede (senza cambiare pagina), cambio di competizione, poi le altre schede dell'Albo
    await p.goto(B + g + 'albo.html#derby', { waitUntil: 'load' }); await p.waitForSelector('#der-root [data-dsez]'); await p.waitForTimeout(1500);
    for (const k of ['rivalita', 'classifica', 'lega']) {
      await p.click('[data-dsez="' + k + '"]'); await p.waitForTimeout(300);
      const v = await p.evaluate(() => [...document.querySelectorAll('[data-dp]')].filter(x => !x.hidden).map(x => x.dataset.dp).join() + location.search + location.hash + location.pathname.split('/').pop());
      if (v !== k + '?sez=' + k + '#derbyalbo.html') pr.push('clic su ' + k + ': ' + v);
      if (D && /PC 1920|iPhone SE 320/.test(sn) && MOTORE === 'chromium') await p.screenshot({ path: D + '/albo-' + k + '-' + sn.replace(/\W+/g, '-') + '-' + (g[0] === 's' ? 'stadio' : 'lega') + '.png' });
    }
    await p.click('[data-dsez="classifica"]'); await p.waitForTimeout(200);
    const cup = p.locator('[data-pt-comp="cup"]'); if (await cup.count()) { await cup.click(); await p.waitForTimeout(300); if (!(await p.locator('#der-cls #pt-derby[data-pt-competition=cup]').count())) pr.push('Champions Cup nella Classifica non va'); } else pr.push('manca il cambio Campionato/Champions Cup');
    await p.click('[data-at="titoli"]'); await p.waitForTimeout(300);
    if (!(await p.locator('[data-ap="titoli"]:not([hidden])').count()) || (await p.locator('[data-ap="derby"]:not([hidden])').count())) pr.push('le altre schede dell\'Albo non vanno');
    await p.click('[data-at="derby"]'); await p.waitForTimeout(300);
    if ((await p.locator('#der-root [data-dsez]').count()) !== 3) pr.push('tornando su Derby le schede spariscono');
    console.log((pr.length ? 'KO ' : 'OK ') + MOTORE + ' · ' + sn + ' · ' + (g[0] === 's' ? 'Stadio' : 'Lega') + (pr.length ? '\n   ' + [...new Set(pr)].join('\n   ') : ''));
    ko += pr.length; await c.close();
  }
  await br.close(); process.exit(ko ? 1 : 0);
})();
