// Prova del caricatore dei temi evento (Claude, 17 novembre 2026). Uso: node temi/prova_evento.js URL_DELLA_CARTELLA_TEMI
//   per esempio: (cd o-girrr-registro && python3 -m http.server 8768) e poi node temi/prova_evento.js http://localhost:8768/temi/
// Controlla: spento prima del 18 alle 00:00 (ora italiana), acceso il 18, 19 e 20, spento dal 24 alle 00:00 in poi;
// ?evento=on lo accende fuori dalla finestra, ?evento=off lo spegne dentro, e la scelta resta per la sessione fino a ?evento=auto;
// col tema acceso il CSS dell'evento è caricato; senza parametri usa la data vera del computer.
const { chromium } = require('playwright');
(async () => {
  const B = process.argv[2]; const b = await chromium.launch(); const ctx = await b.newContext(); const p = await ctx.newPage();
  const err = []; p.on('pageerror', e => err.push(e.message)); let ko = 0;
  const stato = async (qs) => { await p.goto(B + 'prova-evento.html' + qs, { waitUntil: 'load' }); await p.waitForTimeout(150);
    return p.evaluate(() => ({ tema: document.documentElement.dataset.eventTheme || null, css: !!document.querySelector('link[data-evento]'),
      caricato: [...document.styleSheets].some(s => (s.href || '').includes('notte-tropicale/notte-tropicale.css')) })); };
  const casi = [
    ['?evento-data=2026-11-17T23:59', null], ['?evento-data=2026-11-18T00:00', 'notte-tropicale'], ['?evento-data=2026-11-19T12:00', 'notte-tropicale'],
    ['?evento-data=2026-11-23T23:59', 'notte-tropicale'], ['?evento-data=2026-11-24T00:00', null], ['?evento-data=2026-12-25T10:00', null],
    ['?evento-data=2026-11-23T23:30:00Z', null],                         // 00:30 del 24 in Italia: già spento
    ['?evento=on&evento-data=2026-12-01T10:00', 'notte-tropicale'], ['?evento-data=2026-12-01T10:00', 'notte-tropicale'],   // «on» ricordato
    ['?evento=off&evento-data=2026-11-19T12:00', null], ['?evento-data=2026-11-19T12:00', null],               // «off» ricordato
    ['?evento=auto&evento-data=2026-11-19T12:00', 'notte-tropicale'], ['?evento-data=2026-11-25T12:00', null],
  ];
  for (const [qs, atteso] of casi) {
    const s = await stato(qs); const ok = s.tema === atteso && (!atteso || (s.css && s.caricato)) && (atteso || !s.css);
    if (!ok) ko++; console.log((ok ? 'OK ' : 'KO ') + qs.padEnd(48) + ' → ' + (s.tema || 'spento') + (s.tema ? (s.caricato ? ' (CSS caricato)' : ' (CSS mancante)') : ''));
  }
  const oggi = await stato('?evento=auto'); const d = new Date(), on = d >= new Date('2026-11-18T00:00:00+01:00') && d < new Date('2026-11-24T00:00:00+01:00');
  if ((oggi.tema === 'notte-tropicale') !== on) ko++; console.log(((oggi.tema === 'notte-tropicale') === on ? 'OK ' : 'KO ') + 'data vera del computer → ' + (oggi.tema || 'spento'));
  if (err.length) { ko++; console.log('KO errori: ' + err.join(' | ')); }
  await b.close(); console.log(ko ? ko + ' prove non superate' : 'Tutte le prove superate'); process.exit(ko ? 1 : 0);
})();
