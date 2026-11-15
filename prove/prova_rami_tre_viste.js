// Ramificazioni (Claude, 14-15 novembre 2026): la pagina principale è rami.html, a tutta larghezza nel portale del Registro;
// la mappa del confronto con main (ramificazioni.html) si apre dal suo collegamento.
//   BASE=http://localhost:8790/o-girrr-registro/ MOTORE=chromium|webkit|firefox node prove/prova_rami_tre_viste.js [CARTELLA_FOTO]
// Controlla: tre viste che si disegnano, cambio di repository, tocco su un ramo con i dettagli, niente scorrimento di lato,
// l'altezza del riquadro che segue il contenuto dentro Ramificazioni, nessun errore nella console.
const pw = require('playwright'), {browser}=require('./browser_certificato');
const B = process.env.BASE || 'http://localhost:8790/o-girrr-registro/', M = process.env.MOTORE || 'chromium', D = process.argv[2];
const SCH = [['iPhone SE 320', { viewport: { width: 320, height: 568 }, isMobile: M !== 'firefox', hasTouch: true }], ['iPad', { viewport: { width: 820, height: 1180 } }], ['PC 1280', { viewport: { width: 1280, height: 800 } }], ['TV', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 }]];
(async () => {
  const br = await browser(M); let ko = 0;
  for (const [sn, o] of SCH) {
    const c = await br.newContext(o), p = await c.newPage(), pr = [];
    p.on('pageerror', e => pr.push('errore: ' + e.message.slice(0, 100)));
    p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|raw\.githubusercontent|CORS request did not succeed/.test(m.text())) pr.push('console: ' + m.text().slice(0, 100)); });
    // da sola
    await p.goto(B + 'rami.html?nel-registro=1' + (process.env.REMOTI ? '' : '&dati=locale'), { waitUntil: 'load' }); await p.waitForTimeout(1500);
    for (const v of ['albero', 'metro', 'ventaglio']) {
      await p.click('#vista [data-v=' + v + ']'); await p.waitForTimeout(700);
      const n = await p.evaluate(() => document.querySelectorAll('#box .nodo-s, #box .riga').length);
      if (n < 3) pr.push(v + ': ' + n + ' rami disegnati');
      if (await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) pr.push(v + ': scorre di lato');
    }
    // Entrambi: sito e registro insieme, in tutte e tre le viste
    await p.click('#repo [data-r="2"]'); await p.waitForTimeout(600);
    for (const v of ['albero', 'metro', 'ventaglio']) {
      await p.click('#vista [data-v=' + v + ']'); await p.waitForTimeout(700);
      const e = await p.evaluate(() => ({ n: document.querySelectorAll('#box .nodo-s, #box .riga').length, t: document.getElementById('box').innerText, piede: document.getElementById('piede').textContent, lato: document.documentElement.scrollWidth > innerWidth + 1 }));
      if (e.n < 6) pr.push('Entrambi ' + v + ': ' + e.n + ' rami');
      if (v === 'albero' && !(/Sito › main/.test(e.t) && /Registro › main/.test(e.t))) pr.push('Entrambi: mancano i due main');
      if (!/^Sul sito la \d/.test(e.piede)) pr.push('piè di pagina: ' + e.piede.slice(0, 60));
      if (e.lato) pr.push('Entrambi ' + v + ': scorre di lato');
    }
    await p.click('#vista [data-v=albero]'); await p.waitForTimeout(400);
    const lk = p.locator('#box .riga').nth(3); if (await lk.count()) { await lk.click(); await p.waitForTimeout(600); const h = await p.evaluate(() => [...document.querySelectorAll('.dettagli a')].map(a => a.href).join(' ')); if (/%E2%80%BA|›/.test(h)) pr.push('link a GitHub con «›» nel nome: ' + h.slice(0, 120)); }
    // unioni (Gianluca, 15 novembre 2026): con «Tutti» si vedono dove e quando i rami rientrano; la vista parte dall'inizio e non va oltre
    await p.keyboard.press('Escape'); await p.waitForTimeout(300);   // nessun ramo scelto: la vista parte dall'inizio
    await p.click('#stato [data-s="tutti"]'); await p.click('#vista [data-v=metro]'); await p.waitForTimeout(900);
    const un = await p.evaluate(() => ({ frecce: document.querySelectorAll('#box path[stroke-dasharray]').length, vb: document.querySelector('.tela svg').getAttribute('viewBox') }));
    if (!un.frecce) pr.push('Linea del tempo: nessuna unione disegnata'); if (!/^0 0 /.test(un.vb)) pr.push('Linea del tempo non parte dall\'inizio: ' + un.vb);
    const tb = await p.locator('.tela svg').boundingBox(); await p.mouse.move(tb.x + tb.width / 2, tb.y + tb.height / 2); await p.mouse.down(); await p.mouse.move(tb.x + tb.width / 2 + 300, tb.y + tb.height / 2 + 200, { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(300);
    const vb2 = (await p.evaluate(() => document.querySelector('.tela svg').getAttribute('viewBox'))).split(' ').map(Number); if (vb2[0] < 0 || vb2[1] < 0) pr.push('trascinando si va prima dell\'inizio: ' + vb2.join(' '));
    await p.click('#vista [data-v=albero]'); await p.waitForFunction(() => [...document.querySelectorAll('.chip')].some(c => /Unito in/.test(c.textContent)), null, { timeout: 5000 }).catch(() => pr.push('Albero: nessun «Unito in»'));
    await p.click('#stato [data-s="aperti"]'); await p.waitForTimeout(300);
    await p.click('#repo [data-r="1"]'); await p.waitForTimeout(600);
    await p.click('#vista [data-v=albero]'); await p.waitForTimeout(500);
    const nodo = p.locator('#box .riga, #box .nodo-s').nth(1); if (await nodo.count()) { await nodo.click(); await p.waitForTimeout(700); if (!(await p.evaluate(() => /commit|Commit/.test((document.querySelector('.dettagli') || {}).innerText || '')))) pr.push('dettagli del ramo non aperti'); }
    // dal portale: il menu Ramificazioni apre la pagina grande; il vecchio indirizzo rami.html porta lì
    await p.goto(B + 'rami.html', { waitUntil: 'load' }); await p.waitForTimeout(3500);
    if (!/registro\.html#ramificazioni$/.test(p.url())) pr.push('rami.html non entra nel portale: ' + p.url());
    const fr = p.frames().find(x => /rami\.html/.test(x.url()));
    if (!fr) pr.push('il portale non apre rami.html'); else {
      const f = await fr.evaluate(() => ({ n: document.querySelectorAll('#box .nodo-s, #box .riga').length, h1: (document.querySelector('h1') || {}).textContent, link: !!document.querySelector('.mappa-confronto a'), lato: document.documentElement.scrollWidth > innerWidth + 1, largo: document.querySelector('.w').getBoundingClientRect().width }));
      if (f.n < 3) pr.push('nel portale ' + f.n + ' rami'); if (f.h1 !== 'Ramificazioni') pr.push('titolo ' + f.h1); if (!f.link) pr.push('manca il collegamento alla mappa del confronto');
      if (f.lato) pr.push('rami.html scorre di lato nel portale');
      if (await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) pr.push('il portale scorre di lato');
      if (D && /PC|TV|SE/.test(sn) && M === 'chromium') await p.screenshot({ path: D + '/ramificazioni-' + sn.replace(/\W+/g, '') + '.png' });
      await fr.click('.mappa-confronto a'); await p.waitForTimeout(3000);
      const fm = p.frames().find(x => /ramificazioni\.html/.test(x.url()));
      if (!fm) pr.push('la mappa del confronto non si apre'); else if (!(await fm.evaluate(() => !!document.getElementById('repositories') && !!document.querySelector('a[href^="rami.html"]')))) pr.push('mappa del confronto senza il ritorno ai rami');
    }
    console.log((pr.length ? 'KO ' : 'OK ') + M + ' · ' + sn + (pr.length ? '\n   ' + pr.join('\n   ') : '')); ko += pr.length; await c.close();
  }
  await br.close(); process.exit(ko ? 1 : 0);
})();
