// 6.3 · Totogirrr su 16 schermi, Lega e Stadio (Claude, 16 novembre 2026).
// Uso: node prove/v63/prova_toto63.js URL_BASE [CARTELLA_FOTO]
//   URL_BASE = indirizzo di una copia di gh-pages con rilascio/r63/applica.py (per esempio http://localhost:8766/sito/)
// Controlla: niente scorrimento laterale, nessun errore, colonne delle partite (1 sul telefono, 2-4 sugli schermi larghi),
// schede in alto che vanno via scorrendo, scheda toccata (tocco vero) tutta in vista sul telefono.
const { chromium, devices } = require('playwright');
(async () => {
  const B = process.argv[2], FOTO = process.argv[3];
  const SCHERMI = [
    ['iPhone SE 320', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }, 1],
    ['iPhone SE', devices['iPhone SE'], 1],
    ['iPhone 15 Pro', devices['iPhone 15 Pro'], 1],
    ['iPhone 15 Pro Max', devices['iPhone 15 Pro Max'], 1],
    ['Galaxy S8', devices['Galaxy S8'], 1],
    ['Pixel 7', devices['Pixel 7'], 1],
    ['Galaxy S24', devices['Galaxy S24'] || devices['Galaxy S9+'], 1],
    ['iPad Mini', devices['iPad Mini'], 2],
    ['iPad orizzontale', devices['iPad (gen 7) landscape'], 2],
    ['iPad Pro 11', devices['iPad Pro 11'], 2],
    ['Galaxy Tab S4', devices['Galaxy Tab S4'], 2],
    ['Galaxy Tab S4 orizzontale', devices['Galaxy Tab S4 landscape'], 2],
    ['PC 1280', { viewport: { width: 1280, height: 800 } }, 3],
    ['PC 1920', { viewport: { width: 1920, height: 1080 } }, 4],
    ['Monitor 2560', { viewport: { width: 2560, height: 1440 } }, 4],
    ['Smart TV', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0.4606.31 TV Safari/537.36' }, 4],
  ];
  const b = await chromium.launch(); let ko = 0;
  for (const [nome, opz, col] of SCHERMI) for (const g of ['girrr', 'stadio/girrr']) {
    const ctx = await b.newContext(opz); const p = await ctx.newPage(); const err = [];
    p.on('pageerror', e => err.push(e.message.slice(0, 90)));
    await p.goto(B + g + '/totogirrr.html?demo', { waitUntil: 'networkidle' }); await p.waitForTimeout(900);
    const m = await p.evaluate(() => {
      const cs = [...document.querySelectorAll('.pane>.card.m')].map(c => Math.round(c.getBoundingClientRect().left));
      return { lat: document.documentElement.scrollWidth - innerWidth, col: new Set(cs).size,
        pos: getComputedStyle(document.querySelector('nav')).position };
    });
    const navVia = await p.evaluate(async () => {   // la fila scorre con la pagina (non resta attaccata in alto)
      const n = document.querySelector('nav'), t0 = n.getBoundingClientRect().top + scrollY; document.body.style.paddingBottom = '3000px'; scrollTo(0, t0 + 200);
      await new Promise(r => setTimeout(r, 250)); const ok = Math.abs(n.getBoundingClientRect().top - (t0 - scrollY)) < 2 && scrollY > t0; scrollTo(0, 0); document.body.style.paddingBottom = ''; return ok; });
    if (FOTO && /SE 320|15 Pro$|iPad Pro|PC|Monitor|TV/.test(nome)) {
      await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(200);
      await p.screenshot({ path: FOTO + '/' + nome.replace(/ /g, '_') + '-' + g.replace('/', '_') + '.png' });
    }
    let vis = true;
    if (col === 1) {   // tocco vero sull'ultima scheda tagliata a destra
      await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(200);
      const t = await p.evaluate(() => { const n = document.querySelector('nav'), e = n.getBoundingClientRect();
        const bb = [...n.querySelectorAll('button')].find(x => x.getBoundingClientRect().right > e.right && x.getBoundingClientRect().left < e.right - 12); if (!bb) return null;
        const r = bb.getBoundingClientRect(); return { x: (r.left + e.right) / 2, y: r.top + r.height / 2, t: bb.dataset.tab }; });
      if (t) { await p.touchscreen.tap(t.x, t.y); await p.waitForTimeout(900);
        vis = await p.evaluate(t => { const n = document.querySelector('nav'), bb = n.querySelector('button.on'), r = bb.getBoundingClientRect(), e = n.getBoundingClientRect();
          return bb.dataset.tab === t && r.left >= e.left - 1 && r.right <= e.right + 1; }, t.t); }
    }
    const ok = m.lat <= 0 && !err.length && m.col === col && m.pos !== 'sticky' && navVia && vis;
    if (!ok) ko++;
    console.log((ok ? 'OK ' : 'KO ') + nome + ' · ' + (g === 'girrr' ? 'Lega' : 'Stadio') + ' · colonne ' + m.col + '/' + col + ' · laterale ' + m.lat + ' · schede ' + m.pos + (navVia ? ' (vanno via)' : ' (restano)') + (vis ? '' : ' · scheda toccata tagliata') + (err.length ? ' · errori: ' + err.join(' | ') : ''));
    await ctx.close();
  }
  await b.close(); console.log(ko ? ko + ' prove non superate' : 'Tutte le prove superate'); process.exit(ko ? 1 : 0);
})();
