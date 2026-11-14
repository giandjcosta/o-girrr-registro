// Prova di lab/prove-grafiche/rami-alternative.html (Claude, 13 novembre 2026): in ogni vista tocca un pallino e controlla zoom, dettagli e link ai commit. Uso: servire la cartella che contiene o-girrr-registro su localhost:8771, poi MOTORE=chromium|firefox|webkit node prove/prova_rami_interattivi.js
const pw = require('playwright'), { devices } = pw, fs = require('fs');
const M = process.env.MOTORE || 'chromium', U = 'http://localhost:8771/o-girrr-registro/lab/prove-grafiche/rami-alternative.html';
(async () => { let ko = 0;
 for (const [n, o0] of [['iPhone SE 320', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone 15 Pro', devices['iPhone 15 Pro']], ['iPad', devices['iPad Mini']], ['PC 1440', { viewport: { width: 1440, height: 900 } }], ['TV', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 }]]) {
  const o = { ...o0 }; delete o.defaultBrowserType; if (M === 'firefox') delete o.isMobile;
  let c, chiudi; if (M === 'firefox') { const d = fs.mkdtempSync('/tmp/ffp-'); c = await pw.firefox.launchPersistentContext(d, { executablePath: '/tmp/claude-0/pw/firefox-1543/firefox/firefox', ...o }); chiudi = () => c.close(); } else { const b = await pw[M].launch(); c = await b.newContext(o); chiudi = () => b.close(); }
  const p = await c.newPage(), pr = [], err = []; p.on('pageerror', e => err.push(e.message.slice(0, 120))); p.on('console', m => m.type() === 'error' && err.push(m.text().slice(0, 120)));
  await p.goto(U); await p.waitForTimeout(1000);
  const lato = async q => { if (await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) pr.push(q + ': scorre di lato'); };
  for (const v of ['albero', 'metro', 'ventaglio']) {
   await p.click('#vista [data-v="' + v + '"]'); await p.click('#stato [data-s="tutti"]'); await p.waitForTimeout(500);
   await lato(v);
   if (v === 'albero') {
    const z = p.locator('[data-zoom="claude/coppe-simboli-ere-descrizioni-4jn4ss"]').first();
    await z.scrollIntoViewIfNeeded(); await z.click(); await p.waitForTimeout(700);
    const r = await p.evaluate(() => ({ bric: !!document.querySelector('.briciole'), righe: document.querySelectorAll('.albero .riga').length, det: !document.getElementById('det').hidden, link: document.querySelectorAll('#det .commit a[href*="/commit/"]').length }));
    if (!r.bric || r.righe < 2 || !r.det || !r.link) pr.push('albero zoom: ' + JSON.stringify(r));
    await lato('albero zoom');
    if (/15 Pro|PC/.test(n) && M === 'chromium') await p.screenshot({ path: '/tmp/claude-0/foto/int-' + n.replace(/\W+/g, '') + '-albero.png' });
    await p.click('.briciole [data-zoom=""]'); await p.waitForTimeout(400);
   } else {
    const vb0 = await p.evaluate(() => document.querySelector('.tela svg').getAttribute('viewBox'));
    await p.evaluate(() => document.querySelector('.tela').scrollIntoView({ block: 'start' })); await p.waitForTimeout(300);
    const scelto = await p.evaluate(() => { const t0 = document.querySelector('.tela').getBoundingClientRect(), t = { top: t0.top, bottom: Math.min(t0.bottom, innerHeight), left: t0.left, right: t0.right }; const L = [...document.querySelectorAll('.nodo-s')].filter(g => { const b = g.querySelector('circle.p').getBoundingClientRect(); return b.top > t.top + 10 && b.bottom < t.bottom - 30 && b.left > t.left && b.right < t.right; }); const g = L[Math.min(5, L.length - 1)]; return g && g.getAttribute('data-n'); });
    if (!scelto) { pr.push(v + ': nessun pallino visibile'); continue; }
    const bb = await p.locator('.nodo-s[data-n="' + scelto + '"] circle.p').boundingBox();
    const sotto = await p.evaluate(([x, y]) => { const e = document.elementFromPoint(x, y); return e ? e.tagName + '.' + (e.getAttribute('class') || '') + (e.closest('.nodo-s') ? ' nodo' : '') : null; }, [bb.x + bb.width / 2, bb.y + bb.height / 2]);
    if (v === 'metro') console.log('    ', n, scelto, JSON.stringify(bb), sotto);
    await p.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2); await p.waitForTimeout(900);
    const r = await p.evaluate(() => ({ vb: document.querySelector('.tela svg').getAttribute('viewBox'), det: !document.getElementById('det').hidden, link: document.querySelectorAll('#det .commit a[href*="/commit/"]').length || (/Nessun commit proprio/.test(document.getElementById('det').textContent) ? 1 : 0), spenti: document.querySelectorAll('.tela .spento').length, punti: document.querySelectorAll('#commit-sel a').length }));
    console.log('   ', n, v, JSON.stringify(r).slice(0, 160));
    if (r.vb === vb0) pr.push(v + ': lo zoom non si muove'); if (!r.det || !r.link) pr.push(v + ': dettagli ' + JSON.stringify(r)); if (!r.spenti) pr.push(v + ': nessun ramo spento');
    if (v === 'metro' && !r.punti) pr.push('metro: nessun commit sulla riga');
    await lato(v + ' zoom');
    if (/15 Pro|PC/.test(n) && M === 'chromium') await p.screenshot({ path: '/tmp/claude-0/foto/int-' + n.replace(/\W+/g, '') + '-' + v + '.png' });
    // dettagli: vai al padre dal riquadro
    const padre = p.locator('#det [data-vai]').first(); if (await padre.isVisible().catch(() => false)) { await padre.click(); await p.waitForTimeout(700); }
    await p.keyboard.press('Escape'); await p.waitForTimeout(300);
   }
  }
  err.forEach(e => pr.push(e)); console.log((pr.length ? 'KO ' : 'OK ') + M + ' · ' + n + (pr.length ? '\n   ' + pr.join('\n   ') : '')); ko += pr.length; await chiudi(); }
 console.log(M + ': ' + ko + ' problemi'); })();
