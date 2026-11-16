// 6.2.3 · Pillola «Esci» in fondo alla Home (Claude, 16 novembre 2026).
// Uso: node prove/v623/prova_esci623.js URL_BASE   (copia di gh-pages con rilascio/r623/applica.py, per esempio http://localhost:8766/sito/)
// Con squadra, da ospite e senza accesso; Lega e Stadio; iPhone SE 320 (tocco vero) e PC. Due tocchi per uscire.
const { chromium, devices } = require('playwright');
(async () => {
  const B = process.argv[2]; const b = await chromium.launch(); let ko = 0;
  for (const [nome, opz] of [['iPhone SE 320', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['PC 1280', { viewport: { width: 1280, height: 800 } }]])
    for (const g of ['girrr', 'stadio/girrr']) for (const stato of ['squadra', 'ospite', 'nessuno']) {
      const ctx = await b.newContext(opz);
      await ctx.addInitScript(s => { try { if (sessionStorage.getItem('fatto')) return; sessionStorage.setItem('fatto', '1');
        if (s === 'squadra') localStorage.setItem('fg', JSON.stringify({ team: 'Atletico ma non troppo', code: 'PROVA' }));
        if (s === 'ospite') sessionStorage.setItem('ospite', '1'); } catch (e) {} }, stato);
      const p = await ctx.newPage(); const err = []; p.on('pageerror', e => err.push(e.message.slice(0, 80)));
      await p.goto(B + g + '/index.html', { waitUntil: 'networkidle' }); await p.waitForTimeout(1200);
      await p.evaluate(() => scrollTo(0, document.body.scrollHeight)); await p.waitForTimeout(400);
      const r = await p.evaluate(() => { const e = document.querySelector('.vv-esci'), v = document.querySelector('.vv-fondo');
        return { esci: e && e.textContent, riga: e && v ? Math.abs(e.getBoundingClientRect().top - v.getBoundingClientRect().top) < 4 && e.getBoundingClientRect().left < v.getBoundingClientRect().left : null,
          lat: document.documentElement.scrollWidth - innerWidth }; });
      let ok = r.lat <= 0 && !err.length && (stato === 'nessuno' ? !r.esci : r.riga && r.esci === (stato === 'squadra' ? 'Esci da Atletico ma non troppo' : 'Esci'));
      if (ok && r.esci) {
        const tocca = async () => { const bb = await (await p.$('.vv-esci')).boundingBox(); if (nome.startsWith('iPhone')) await p.touchscreen.tap(bb.x + bb.width / 2, bb.y + bb.height / 2); else await p.click('.vv-esci'); };
        await tocca(); await p.waitForTimeout(250);
        const conferma = await p.textContent('.vv-esci');
        await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), tocca()]); await p.waitForTimeout(800);
        const fine = await p.evaluate(() => ({ fg: JSON.parse(localStorage.getItem('fg') || 'null'), osp: sessionStorage.getItem('ospite'), esci: !!document.querySelector('.vv-esci') }));
        ok = conferma === 'Tocca di nuovo per uscire' && !fine.esci && !fine.osp && (!fine.fg || !fine.fg.code);
      }
      if (!ok) ko++;
      console.log((ok ? 'OK ' : 'KO ') + nome + ' · ' + (g === 'girrr' ? 'Lega' : 'Stadio') + ' · ' + stato + ' · ' + JSON.stringify(r) + (err.length ? ' · errori: ' + err.join(' | ') : ''));
      await ctx.close();
    }
  await b.close(); console.log(ko ? ko + ' prove non superate' : 'Tutte le prove superate'); process.exit(ko ? 1 : 0);
})();
