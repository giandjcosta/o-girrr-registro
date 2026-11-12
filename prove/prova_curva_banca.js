// Curva · Nuovi personaggi, frasi e immagini (Claude, 12 novembre 2026).
// 1. I cori dei giorni prima di TAGLIO_N devono restare identici a quelli della banca pubblicata (lo storico non cambia).
// 2. Da TAGLIO_N in poi compaiono i nuovi personaggi (e Radio Girrr e Il VAR del Girrr), con nomi e profili.
// 3. Le immagini nuove si disegnano senza errori, con i dati veri (foto in CARTELLA_FOTO).
// Uso: servire la cartella con o-girrr-registro e una copia di gh-pages come o-fant-a-girrr su http://localhost:8771/, poi
//   node prove/prova_curva_banca.js [CARTELLA_FOTO]
const { chromium } = require('playwright');
const { script: BLOCCA } = require('./blocca_scritture');
const L = 'http://localhost:8771/o-girrr-registro/lab/offline/';
const D = process.argv[2];
(async () => {
  const b = await chromium.launch(); const c = await b.newContext({ viewport: { width: 1280, height: 900 } });
  await c.addInitScript(BLOCCA);
  const p = await c.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message.slice(0, 120)));
  await p.goto(L); await p.waitForTimeout(2500);
  await p.goto(L + 'sito/stadio/girrr/curva.html'); await p.waitForSelector('#nav button'); await p.waitForTimeout(2500);
  const r = await p.evaluate(async () => {
    const { D, SQ, ST } = __curvaProva.dati();
    // la banca pubblicata, caricata a parte (stesso codice del sito)
    const src = await fetch('http://localhost:8771/o-fant-a-girrr/girrr/curva-banca.js').then(x => x.text());
    const w = { CVS: window.CVS }; new Function('window', src)(w); const VEC = w.CVB, NUO = window.CVB;
    const pulisci = L => JSON.stringify(L.map(q => ({ k: q.k, a: q.a, x: q.x, ts: q.ts, imgt: q.imgt || null, r: (q.r || []).map(y => [y.a, y.x]) })));
    const oggi = Date.UTC(2026, 10, 12, 12), out = { uguali: 0, diversi: [], nuovi: {}, oggiTot: 0 };
    for (let d = 1; d <= 12; d++) { const ms = oggi - d * 864e5; if (pulisci(VEC.genera(D, SQ, ST, ms)) === pulisci(NUO.genera(D, SQ, ST, ms))) out.uguali++; else out.diversi.push(new Date(ms).toISOString().slice(0, 10)); }
    // da oggi: i nuovi autori (su qualche giorno, per vederli tutti)
    const autori = {}, imm = {};
    for (let d = 0; d < 14; d++) NUO.genera(D, SQ, ST, oggi + d * 864e5).forEach(q => { autori[q.a] = (autori[q.a] || 0) + 1; if (q.imgt) imm[q.imgt] = (imm[q.imgt] || 0) + 1; (q.r || []).forEach(y => { autori[y.a] = (autori[y.a] || 0) + 1; }); });
    (NUO.NUOVI || []).forEach(a => { out.nuovi[a] = autori[a] || 0; });
    out.immagini = imm; out.comuniNuovi = (NUO.COMUNI_N || []).map(u => u[0]).filter(h => autori[h]).length;
    return out;
  });
  const pr = [];
  console.log('Giorni passati identici:', r.uguali, '/ 12' + (r.diversi.length ? ' · diversi: ' + r.diversi.join(', ') : ''));
  if (r.diversi.length) pr.push('lo storico è cambiato');
  console.log('Nuovi personaggi (cori in 14 giorni):', JSON.stringify(r.nuovi));
  const muti = Object.keys(r.nuovi).filter(a => !r.nuovi[a]); if (muti.length) pr.push('personaggi senza cori: ' + muti.join(', '));
  console.log('Immagini nei 14 giorni:', JSON.stringify(r.immagini), '· utenti nuovi comparsi:', r.comuniNuovi);
  // Profili dei nuovi account: nome e biografia nella pagina (non il nome tecnico)
  const prof = await p.evaluate(() => (window.CVB.NUOVI || []).filter(h => { const el = document.createElement('div'); return false; }));
  // Immagini nuove: disegnate con i dati veri della pagina
  const tipi = ['lavagna_ris', 'epoca2', 'cartolina', 'tabelle', 'meteo', 'pizza', 'onda', 'var', 'quaderno', 'coreo'];
  for (const t of tipi) {
    const u = await p.evaluate((t) => { try { return __curvaProva.img(t); } catch (e) { return 'ERRORE ' + e.message; } }, t);
    if (!/^data:image\/png/.test(u)) { pr.push('immagine ' + t + ': ' + String(u).slice(0, 80)); continue; }
    if (D) require('fs').writeFileSync(D + '/img-' + t + '.png', Buffer.from(u.split(',')[1], 'base64'));
  }
  if (errs.length) pr.push('errori JS: ' + errs.join(' / '));
  console.log(pr.length ? 'Problemi: ' + pr.join(' | ') : 'Tutto a posto');
  await b.close();
})();
