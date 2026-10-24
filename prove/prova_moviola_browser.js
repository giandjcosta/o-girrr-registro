// Uso: servire il sito di oggi su :8001, il candidato al rilascio su :8002 (cartelle con dentro o-fant-a-girrr/) e il registro su :8003, poi
// node prove/prova_moviola_browser.js <cartella per le schermate, con dentro pw/>
// Prova nel browser della Moviola (passo 4): Lab, Anteprima Lega e Stadio, sito vero dopo il rilascio (copia locale), pagina dei video,
// e confronto degli errori in console tra il sito com'è oggi (vivo) e il candidato al rilascio (nuovo).
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const S = process.argv[2], OUT = path.join(S, 'pw');
// quanti episodi deve mostrare l'ultima giornata: quelli di moviola.json del registro (prima erano sempre 3)
const MJ = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'calcoli', 'moviola.json'), 'utf8')), NEP = MJ.giornate[String(MJ.giocate[MJ.giocate.length - 1])].episodi.length;
const VIVO = 'http://127.0.0.1:8001/o-fant-a-girrr/', NUOVO = 'http://127.0.0.1:8002/o-fant-a-girrr/', REG = 'http://127.0.0.1:8003/';
const DEV = [['iPhone SE 320', 320, 568, true], ['iPhone SE', 375, 667, true], ['iPhone 13', 390, 844, true], ['PC', 1366, 768, false], ['TV', 1920, 1080, false]];
const esiti = [];
function ok(c, x) { esiti.push([!!c, x]); console.log((c ? 'OK   ' : 'NO   ') + x); }
const FEED = { v: 3, ok: false, posts: [], replies: [], rt: [], react: [], mine: [], follow: [], polls: [], pv: {}, prof: {}, lk: {},
  adm: [{ id: 9001, h: 'girrr_sport', hi: false, ts: Date.UTC(2026, 9, 20, 12, 40),
    body: "MOVIOLA · Giornata 3\nRigore sbagliato. De Bruyne va sul dischetto e non trova la porta. Il rigore era netto, l'errore pure: sulla panchina di apo nessuno ci crede. Verdetto: Regolare. #GirrrSport #Moviola" }] };

async function contesto(b, dev, base) {
  const c = await b.newContext({ viewport: { width: dev[1], height: dev[2] }, isMobile: dev[3], hasTouch: dev[3], deviceScaleFactor: 1 });
  await c.route('**/*', r => {
    const u = r.request().url();
    if (u.startsWith('https://giandjcosta.github.io/o-fant-a-girrr/')) return r.fetch({ url: base + u.slice('https://giandjcosta.github.io/o-fant-a-girrr/'.length).split('?')[0] }).then(x => r.fulfill({ response: x })).catch(() => r.abort());
    if (u.includes('.supabase.co/rest/v1/rpc/curva_feed')) return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(FEED) });
    if (u.includes('.supabase.co')) return r.fulfill({ status: 200, contentType: 'application/json', body: '[]' });
    if (u.startsWith('http://127.0.0.1')) return r.continue();
    return r.abort();   // font e servizi esterni: niente rete qui (uguale per vivo e nuovo)
  });
  return c;
}

// controlli di impaginazione nella zona della Moviola (o in tutta la pagina dei video)
async function impaginazione(p, scope) {
  return p.evaluate(sc => {
    const W = innerWidth, r = { scroll: document.documentElement.scrollWidth > W + 1, fuori: [], minuscole: [] };
    const root = document.querySelectorAll(sc);
    root.forEach(z => z.querySelectorAll('*').forEach(e => {
      if (!e.offsetParent && getComputedStyle(e).position !== 'fixed') return;
      if (e.closest('.hm')) return;   // riquadro "Cosa cambia in Home": c'è solo nel Lab
      for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) { const o = getComputedStyle(a).overflowX; if (o === 'auto' || o === 'scroll') { const ab = a.getBoundingClientRect(); if (ab.left >= -1 && ab.right <= W + 1) return; } }   // dentro una striscia che scorre: si vede scorrendo
      const t = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
      if (!t) return;
      const b = e.getBoundingClientRect();
      if (b.width && (b.right > W + 1 || b.left < -1)) r.fuori.push(t.slice(0, 40) + ' (' + Math.round(b.left) + '-' + Math.round(b.right) + ')');
      const card = e.closest('.card');
      if (card) { const cb = card.getBoundingClientRect(); if (b.width && (b.right > cb.right + 1 || b.left < cb.left - 1)) r.fuori.push('fuori dalla card: ' + t.slice(0, 40)); }
      if (e.matches('h1,h2,h3,h4,label,button,a,small,b,.rbadge,option,th') && /^\p{L}/u.test(t) && t[0] !== t[0].toUpperCase()) r.minuscole.push(t.slice(0, 40));
    }));
    return r;
  }, scope);
}

async function tab(b, dev, nome, url, base) {
  const c = await contesto(b, dev, base), p = await c.newPage(), err = [];
  p.on('pageerror', e => err.push(String(e)));
  await p.goto(url, { waitUntil: 'load' });
  try { await p.waitForSelector('.mv, .mvq', { timeout: 15000 }); } catch (e) { }
  await p.waitForTimeout(1200);   // la striscia delle tab scorre fino a quella aperta
  const st = await p.evaluate(() => {
    const bt = document.querySelector('[data-sp="moviola"]');
    const giornate = [...document.querySelectorAll('#mvg option')].map(o => o.value);
    const card = [...document.querySelectorAll('.card.mv')].map(x => ({ t: (x.querySelector('h4') || {}).textContent, v: (x.querySelector('.mvv b') || {}).textContent, x: (x.querySelector('.mvx') || {}).textContent, video: !!x.querySelector('a.mvbtn') }));
    return { premuto: bt && bt.getAttribute('aria-pressed'), disattivato: bt && bt.disabled, giornate, card, q: (document.querySelector('.mvq') || {}).textContent || '' };
  });
  const lay = await impaginazione(p, '#view');
  const tag = `${nome} · ${dev[0]}`;
  ok(st.premuto === 'true' && !st.disattivato && st.card.length === NEP, `${tag}: tab Moviola aperta da #moviola, giornata ${st.giornate[0]}, ${st.card.length} episodi`);
  ok(!lay.scroll && !lay.fuori.length, `${tag}: niente scroll orizzontale né testi fuori` + (lay.fuori.length ? ' → ' + lay.fuori.slice(0, 3).join(' | ') : ''));
  ok(!lay.minuscole.length, `${tag}: etichette con la maiuscola` + (lay.minuscole.length ? ' → ' + lay.minuscole.slice(0, 4).join(' | ') : ''));
  const altre = {};
  for (const g of st.giornate.slice(1)) {   // le altre giornate: messaggi e card
    await p.selectOption('#mvg', g); await p.waitForTimeout(150);
    altre[g] = await p.evaluate(() => ({ n: document.querySelectorAll('.card.mv').length, q: [...document.querySelectorAll('.mvq')].map(x => x.textContent).join(' ') }));
    const l2 = await impaginazione(p, '#view');
    if (l2.scroll || l2.fuori.length || l2.minuscole.length) ok(false, `${tag}: giornata ${g} impaginazione → ${l2.fuori.concat(l2.minuscole).slice(0, 3).join(' | ')}`);
  }
  if (dev[0] === 'iPhone SE 320' || dev[0] === 'TV') await p.screenshot({ path: path.join(OUT, (nome + '-' + dev[0]).replace(/[^\w]+/g, '_') + '.png'), fullPage: true });
  ok(!err.length, `${tag}: nessun errore JavaScript` + (err.length ? ' → ' + err.slice(0, 2).join(' | ') : ''));
  await c.close();
  return { card: st.card, altre };
}

async function errori(b, base, rel) {
  const c = await contesto(b, DEV[3], base), p = await c.newPage(), e = [];
  p.on('pageerror', x => e.push('JS: ' + String(x).split('\n')[0]));
  p.on('console', m => { if (m.type() === 'error') e.push('console: ' + m.text().replace(/https?:\/\/127\.0\.0\.1:800\d/g, '').slice(0, 140)); });
  try { await p.goto(base + rel, { waitUntil: 'load', timeout: 30000 }); await p.waitForTimeout(2500); } catch (x) { e.push('apertura: ' + x.message.split('\n')[0]); }
  const titolo = await p.title();
  await c.close();
  return { e, titolo };
}

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome' }).catch(() => chromium.launch());
  // 1) tab Moviola su tutti i dispositivi
  const PAG = [['Lab', REG + 'lab/index.html#moviola', NUOVO], ['Anteprima Lega', REG + 'anteprima/attuale.html#moviola', NUOVO], ['Anteprima Stadio', REG + 'anteprima/index.html#moviola', NUOVO],
               ['Sito vero Lega', NUOVO + 'girrr/app.html#moviola', NUOVO], ['Sito vero Stadio', NUOVO + 'stadio/girrr/app.html#moviola', NUOVO]];
  const ris = {};
  for (const dev of DEV) for (const [n, u, base] of PAG) ris[n + dev[0]] = await tab(b, dev, n, u, base);
  // 2) stesso comportamento: sito vero e anteprima mostrano gli stessi episodi e gli stessi messaggi
  const rif = JSON.stringify(ris['Anteprima LegaPC']);
  for (const n of ['Lab', 'Anteprima Stadio', 'Sito vero Lega', 'Sito vero Stadio']) ok(JSON.stringify(ris[n + 'PC']) === rif, `${n}: stessi episodi, testi, verdetti e messaggi dell'Anteprima Lega (giornate 1-3)`);
  console.log('   giornate 1 e 2:', JSON.stringify(ris['Sito vero LegaPC'].altre));
  // 3) pagina dei video
  for (const dev of DEV) {
    const c = await contesto(b, dev, NUOVO), p = await c.newPage(), err = [];
    p.on('pageerror', e => err.push(String(e)));
    await p.goto(REG + 'moviola-video.html', { waitUntil: 'load' });
    const lay = await impaginazione(p, 'body');
    ok(!lay.scroll && !lay.fuori.length && !lay.minuscole.length && !err.length, `Pagina dei video · ${dev[0]}: impaginazione, maiuscole, nessun errore` + (lay.fuori.concat(lay.minuscole, err).length ? ' → ' + lay.fuori.concat(lay.minuscole, err).slice(0, 3).join(' | ') : ''));
    if (dev[0] === 'iPhone SE 320') await p.screenshot({ path: path.join(OUT, 'video-SE320.png'), fullPage: true });
    await c.close();
  }
  // 4) il resto del sito: errori nuovi rispetto a oggi
  const R = ['girrr/index.html', 'girrr/curva.html', 'girrr/giornale.html', 'girrr/app.html#radio', 'girrr/app.html#spog', 'girrr/albo.html', 'girrr/app.html#oro', 'girrr/totogirrr.html', 'girrr/tabellone.html', 'girrr/app.html#sport',
             'stadio/girrr/index.html', 'stadio/girrr/curva.html', 'stadio/girrr/giornale.html', 'stadio/girrr/app.html#radio', 'stadio/girrr/app.html#spog', 'stadio/girrr/albo.html', 'stadio/girrr/totogirrr.html'];
  for (const r of R) {
    const v = await errori(b, VIVO, r), n = await errori(b, NUOVO, r);
    const nuovi = n.e.filter(x => !v.e.includes(x));
    ok(!nuovi.length && !n.e.some(x => x.startsWith('JS:')) && n.titolo, `${r}: apre ("${n.titolo}"), nessun errore nuovo` + (nuovi.length ? ' → ' + nuovi.slice(0, 3).join(' | ') : '') + (n.e.length ? ` (rete bloccata qui, uguali a oggi: ${n.e.length})` : ''));
  }
  // 5) Curva: il post Moviola rimanda alla tab, e niente più vecchio post automatico
  for (const sito of ['girrr', 'stadio/girrr']) {
    const c = await contesto(b, DEV[2], NUOVO), p = await c.newPage();
    await p.goto(NUOVO + sito + '/curva.html', { waitUntil: 'load' }); await p.waitForTimeout(2500);
    const l = await p.evaluate(() => [...document.querySelectorAll('a.lnk')].filter(a => /Moviola/.test(a.textContent)).map(a => [a.getAttribute('href'), a.textContent]));
    const vecchi = await p.evaluate(() => [...document.querySelectorAll('article.post')].filter(a => /Moviola: /.test(a.textContent)).length);
    ok(l.length === 1 && l[0][0] === 'app.html#moviola' && l[0][1] === 'Apri la Moviola ›', `Curva ${sito}: il post Moviola ha "Apri la Moviola ›" verso app.html#moviola`);
    ok(vecchi === 0, `Curva ${sito}: nessun vecchio post "Moviola: …" automatico`);
    if (l.length) {
      await p.click('a.lnk[href="app.html#moviola"]'); await p.waitForSelector('.mv, .mvq', { timeout: 15000 }).catch(() => { });
      const s = await p.evaluate(() => ({ u: location.pathname + location.hash, pr: (document.querySelector('[data-sp="moviola"]') || {}).getAttribute && document.querySelector('[data-sp="moviola"]').getAttribute('aria-pressed'), n: document.querySelectorAll('.card.mv').length }));
      ok(/app\.html#moviola$/.test(s.u) && s.pr === 'true' && s.n === NEP, `Curva ${sito}: il link apre la tab Moviola (${s.n} episodi)`);
    }
    await c.close();
  }
  const cv = await contesto(b, DEV[3], VIVO), pv = await cv.newPage();
  await pv.goto(VIVO + 'girrr/curva.html', { waitUntil: 'load' }); await pv.waitForTimeout(2500);
  console.log('   (oggi, prima del rilascio, la Curva ha', await pv.evaluate(() => [...document.querySelectorAll('article.post')].filter(a => /Moviola: /.test(a.textContent)).length), 'post "Moviola: …" automatici)');
  await b.close();
  const no = esiti.filter(x => !x[0]);
  console.log(no.length ? `\n${no.length} controlli NON passati su ${esiti.length}.` : `\nTutti i ${esiti.length} controlli passati.`);
  process.exit(no.length ? 1 : 0);
})();
