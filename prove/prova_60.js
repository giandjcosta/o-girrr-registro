// Prova completa della 6.0 sulla copia di rilascio (Claude, 12 novembre 2026).
// Prima: copia di gh-pages con la 6.0 applicata (python3 rilascio/rilascio60.py COPIA), servita come o-fant-a-girrr
// su http://localhost:8771/ con le richieste a pezzi (Range), come GitHub Pages. Poi:
//   MOTORE=chromium|webkit|firefox node prove/prova_60.js [CARTELLA_FOTO]
//   (FIREFOX=eseguibile e FIREFOX_PROFILO=profilo con il certificato del proxy, nell'ambiente cloud; SOLO=Pixel per un solo schermo)
// 16 schermi × pagine della 6.0 (Home, Curva, Video, Giornale, Tabellone di Lega e Stadio) e «Condividi la giornata».
// Controlla: niente scorrimento di lato, nessun errore nuovo, stile della Curva per sistema, 7 video nella scheda Video,
// pulsanti e pacchetto di «Condividi la giornata» (video, Radio, Tabelloni ufficiali di Campionato e Coppa, Giornale). Le scritture nel database sono bloccate (blocca_scritture.js).
const pw = require('playwright'), { devices } = pw, fs = require('fs');
const { script: BLOCCA } = require('./blocca_scritture');
const MOTORE = process.env.MOTORE || 'chromium', D = process.argv[2];
const B = process.env.BASE || 'http://localhost:8771/o-fant-a-girrr/';   // BASE=https://giandjcosta.github.io/o-fant-a-girrr/ per il sito vero
const TV = 'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36';
const SCH = [
  ['iPhone SE 320', 'ios', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone SE', 'ios', devices['iPhone SE']],
  ['iPhone 15 Pro', 'ios', devices['iPhone 15 Pro']], ['iPhone 15 Pro Max', 'ios', devices['iPhone 15 Pro Max']],
  ['Galaxy S8', 'android', devices['Galaxy S8']], ['Pixel 7', 'android', devices['Pixel 7']], ['Galaxy S24', 'android', devices['Galaxy S24'] || devices['Galaxy S9+']],
  ['iPad Mini', 'ios', devices['iPad Mini']], ['iPad orizzontale', 'ios', devices['iPad (gen 7) landscape']], ['iPad Pro 11', 'ios', devices['iPad Pro 11']],
  ['Galaxy Tab S4', 'android', devices['Galaxy Tab S4']], ['Galaxy Tab S4 orizzontale', 'android', devices['Galaxy Tab S4 landscape']],
  ['PC 1280', 'altro', { viewport: { width: 1280, height: 800 } }], ['PC 1920', 'altro', { viewport: { width: 1920, height: 1080 } }],
  ['Monitor 2560', 'altro', { viewport: { width: 2560, height: 1440 } }],
  ['Smart TV', 'altro', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: TV }]
].filter(s => !process.env.SOLO || s[0].indexOf(process.env.SOLO) >= 0);
const PAG = [
  ['Home Lega', 'girrr/'], ['Home Stadio', 'stadio/girrr/'], ['Curva Lega', 'girrr/curva.html'], ['Curva Stadio', 'stadio/girrr/curva.html'],
  ['Video Lega', 'girrr/app.html#video'], ['Video Stadio', 'stadio/girrr/app.html#video'], ['Giornale Lega', 'girrr/giornale.html'],
  ['Giornale Stadio', 'stadio/girrr/giornale.html'], ['Tabellone Lega', 'girrr/tabellone.html'], ['Tabellone Stadio', 'stadio/girrr/tabellone.html']
];
// Errori che non dipendono dalla 6.0: con il codice di prova «PROVA» lo stato delle notifiche risponde 400 (anche sul sito di oggi)
const NOTI = process.env.SENZA_MVP ? /notifiche_stato|rpc\/mvp_/ : /notifiche_stato/;   // SENZA_MVP=1: schema MVP non ancora applicato sul database (serve il «Vai» alla SQL)
function nome(s) { return s.replace(/[^A-Za-z0-9]+/g, '-'); }
async function contesto(opz) {
  const o = { ...opz };
  if (MOTORE === 'firefox') { delete o.isMobile; delete o.defaultBrowserType; }
  if (MOTORE !== 'chromium') delete o.defaultBrowserType;
  if (MOTORE === 'firefox' && process.env.FIREFOX) {
    const dir = fs.mkdtempSync('/tmp/ffp-'); if (process.env.FIREFOX_PROFILO) fs.cpSync(process.env.FIREFOX_PROFILO, dir, { recursive: true });
    const c = await pw.firefox.launchPersistentContext(dir, { executablePath: process.env.FIREFOX, ...o }); return { c, chiudi: () => c.close() };
  }
  const br = await pw[MOTORE].launch(); const c = await br.newContext(o); return { c, chiudi: () => br.close() };
}
(async () => {
  let ko = 0, prove = 0;
  for (const [sn, os, opz] of SCH) {
    const { c, chiudi } = await contesto(opz);
    await c.addInitScript(BLOCCA);
    await c.addInitScript(() => { try { localStorage.setItem('fg', JSON.stringify({ team: 'Oranje VC', code: 'PROVA' })); } catch (e) {} });
    const p = await c.newPage(), probl = [];
    let errs = [], bad = new Set();
    p.on('pageerror', e => errs.push('errore: ' + e.message.slice(0, 90)));
    p.on('response', r => { if (r.status() >= 400 && !NOTI.test(r.url())) bad.add(r.status() + ' ' + r.url().replace(B, '').slice(0, 90)); });
    p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errs.push('console: ' + m.text().slice(0, 90)); });
    for (const [pn, u] of PAG) {
      errs = []; bad = new Set(); prove++;
      try { await p.goto(B + u, { waitUntil: 'load', timeout: 45000 }); } catch (e) { probl.push(pn + ': non si apre'); continue; }
      await p.waitForTimeout(1600);
      const r = await p.evaluate(() => ({ lato: document.documentElement.scrollWidth > innerWidth + 1, os: document.documentElement.getAttribute('data-os'),
        vid: document.querySelectorAll('.vid-i').length, player: !!document.getElementById('vid-player'), gio: document.querySelectorAll('.cd-gio, .cd-btn').length }));
      if (r.lato) probl.push(pn + ': scorre di lato');
      if (/Curva/.test(pn) && r.os !== os) probl.push(pn + ': stile ' + r.os + ' invece di ' + os);
      if (/Video/.test(pn)) { await p.waitForSelector('.vid-i', { timeout: 15000 }).catch(() => {}); const n = await p.locator('.vid-i').count(); if (n !== 7) probl.push(pn + ': ' + n + ' video invece di 7'); }
      if (/Home|Giornale/.test(pn) && !(await p.locator(/Home/.test(pn) ? '#big .cd-gio' : 'button.cd-btn').count())) probl.push(pn + ': manca «Condividi la giornata»');
      if (/Giornale/.test(pn) && (await p.locator('button.cd-btn').count()) !== 2) probl.push(pn + ': pulsanti di Condividi ' + (await p.locator('button.cd-btn').count()));
      // Condividi la giornata dalla Home
      if (/Home/.test(pn)) {
        await p.locator('#big .cd-gio').scrollIntoViewIfNeeded(); await p.locator('#big .cd-gio').click();
        await p.waitForSelector('.cd-pk', { timeout: 25000 }).catch(() => {});
        // la finestra sale con una transizione: si misura quando è ferma (in WebKit può partire più tardi)
        await p.waitForFunction(() => { const b = document.querySelector('.cd-box'); return b && getComputedStyle(b).transform === 'none'; }, null, { timeout: 5000 }).catch(() => {});
        await p.waitForTimeout(400);
        const k = await p.evaluate(() => ({ n: document.querySelectorAll('.cd-pz').length, lato: document.documentElement.scrollWidth > innerWidth + 1, box: (document.querySelector('.cd-box') || {}).scrollWidth > (document.querySelector('.cd-box') || {}).clientWidth + 1,
          az: (() => { const a = document.querySelector('.cd-az.fis'); if (!a) return false; const b = a.getBoundingClientRect(); return b.bottom <= innerHeight + 1 && b.top >= 0; })() }));
        if (k.n !== 5) probl.push(pn + ': Condividi la giornata con ' + k.n + ' pezzi invece di 5');
        if (k.lato || k.box) probl.push(pn + ': Condividi la giornata scorre di lato');
        if (!k.az) probl.push(pn + ': pulsanti di Condividi la giornata fuori dallo schermo');
        if (D && /PC 1920|Smart TV|iPhone 15 Pro$|Pixel 7/.test(sn) && MOTORE === 'chromium') await p.screenshot({ path: D + '/condividi-' + nome(sn) + '-' + nome(pn) + '.png' });
        await p.keyboard.press('Escape'); await p.waitForTimeout(400);
      }
      if (D && /PC 1920|Smart TV/.test(sn) && MOTORE === 'chromium') await p.screenshot({ path: D + '/' + nome(sn) + '-' + nome(pn) + '.png' });
      errs.forEach(e => probl.push(pn + ': ' + e)); bad.forEach(b => probl.push(pn + ': risposta ' + b));
    }
    const bloc = await p.evaluate(() => window.__scrittureBloccate || 0).catch(() => 0);
    console.log((probl.length ? 'KO ' : 'OK ') + MOTORE + ' · ' + sn + (probl.length ? '\n   ' + probl.join('\n   ') : '') + ' · scritture bloccate: ' + bloc);
    ko += probl.length; await chiudi();
  }
  console.log(MOTORE + ': ' + SCH.length + ' schermi, ' + prove + ' pagine aperte, ' + ko + ' problemi');
  process.exit(ko ? 1 : 0);
})();
