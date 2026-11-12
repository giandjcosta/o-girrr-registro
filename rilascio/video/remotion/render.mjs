// Calcola i dati veri da data.json e fa il video con Remotion (usando il Chromium già installato).
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import fs from 'fs';
const SITO = process.env.SITO || '/tmp/claude-0/srv/o-fant-a-girrr/';
const CHIAVE = 'sb_publishable_qPhimkrF4iUvIad7JPoH8A_i-eOqG7n';   /* chiave pubblica delle pagine, solo lettura */
const D = JSON.parse(fs.readFileSync(SITO + 'data.json', 'utf8'));
const L = D.cal.lega, gi = L.filter(x => x.m.every(m => m[4] && m[4] !== '-')), n = gi[gi.length - 1].n, g = L.find(x => x.n === n), dopo = L.find(x => x.n === n + 1);
const T = {}; gi.filter(x => x.n <= n).forEach(x => x.m.forEach(m => { const r = m[4].split('-').map(Number); [[m[0], r[0], r[1], m[1]], [m[3], r[1], r[0], m[2]]].forEach(([s, a, b, fp]) => { const t = T[s] = T[s] || { n: s, pt: 0, fp: 0 }; t.fp += fp; t.pt += a > b ? 3 : a === b ? 1 : 0; }); }));
const C = Object.values(T).sort((a, b) => b.pt - a.pt || b.fp - a.fp);

// La partita da non perdere (criteri di Gianluca, 12 novembre 2026), in quest'ordine:
// 1. Derby: la stessa regola del Tabellone (votato dalla lega o nato da una sfida accettata col nome; altrimenti rivalità da 80 in su, se i più non l'hanno bocciato);
// 2. 1ª contro 2ª; 3. 3ª contro 4ª;
// 4. l'ultima che può sorpassare: ultima da almeno 3 giornate, che ha ripreso punti (almeno 4 nelle ultime 3) e gioca contro una squadra a 3 punti o meno;
// 5. una lunga storia: sfida con almeno 5 anni di storia (rivalità della pagina Rivalità).
// In Champions Cup le posizioni sono quelle del girone. Se nessuna partita rientra, quella competizione non va nel video; se non rientra niente in tutte e due, la scena «Da non perdere» non c'è.
global.window = {}; await import(SITO + 'girrr/novita-dati.js'); const RIV = {}; const dk = (a, b) => [a, b].map(x => String(x).toLowerCase()).sort().join('|');
(window.NOV.riv || []).forEach(o => { RIV[dk(o.a, o.b)] = o; });
const DV = {}, DX = {}, DN = {};
try { const r = await (await fetch('https://qmjqfgmvimsuxvghetgi.supabase.co/rest/v1/rpc/derby_stato', { method: 'POST', headers: { apikey: CHIAVE, Authorization: 'Bearer ' + CHIAVE, 'Content-Type': 'application/json' }, body: '{}' })).json();   /* sola lettura, come il Tabellone */
  (r.voti || []).forEach(x => { const k = dk(x.a, x.b); if (x.si > x.no) DV[k] = 1; else if (x.no > x.si) DX[k] = 1; });
  (r.sfide || []).slice().reverse().forEach(x => { if (x.stato === 'accettata' && x.nome_ok) { const k = dk(x.da, x.a); DV[k] = 1; delete DX[k]; DN[k] = x.nome; } });
} catch (e) { console.log('Derby votati non letti, uso solo le rivalità:', e.message); }
const derby = (a, b) => { const k = dk(a, b), o = RIV[k]; if (DX[k] || !(DV[k] || (o && o.r >= 80))) return null; return DN[k] || (o && o.n) || ''; };
// classifiche dopo ogni giornata: storia[i] = { squadra: [posizione, punti] }
const storia = (giornate, riga, gruppo) => { const S = {}, out = []; giornate.forEach(x => { x.m.forEach(m => { const [a, fa, fb, b, sc] = riga(m), r = sc.split('-').map(Number);
    [[a, r[0], r[1], fa], [b, r[1], r[0], fb]].forEach(([s, g1, g2, fp]) => { const t = S[s] = S[s] || { n: s, g: gruppo(m), pt: 0, fp: 0 }; t.fp += fp; t.pt += g1 > g2 ? 3 : g1 === g2 ? 1 : 0; }); });
  (x.rest || []).forEach(([gr, s]) => { S[s] = S[s] || { n: s, g: gr, pt: 0, fp: 0 }; });
  const P = {}; const per = {}; Object.values(S).forEach(t => (per[t.g] = per[t.g] || []).push(t));
  Object.values(per).forEach(L => { L.sort((a, b) => b.pt - a.pt || b.fp - a.fp).forEach((t, i) => { P[t.n] = [i + 1, t.pt, L.length]; }); }); out.push(P); }); return out; };
const scegli = (partite, ST) => { const P = ST[ST.length - 1], el = [];
  partite.forEach(([a, b]) => { const pa = P[a], pb = P[b]; if (!pa || !pb) return; const d = derby(a, b);
    if (d !== null) return el.push({ a, b, v: 5, k: 'derby', nome: d });
    const pos = [pa[0], pb[0]].sort((x, y) => x - y);
    if (pos[0] === 1 && pos[1] === 2) return el.push({ a, b, v: 4, k: '1ª contro 2ª' });
    if (pos[0] === 3 && pos[1] === 4) return el.push({ a, b, v: 3, k: '3ª contro 4ª' });
    for (const [u, o] of [[a, b], [b, a]]) { const pu = P[u], po = P[o]; if (pu[0] !== pu[2] || ST.length < 3) continue;
      const da3 = ST.slice(-3).every(S => S[u] && S[u][0] === S[u][2]), presi = pu[1] - ((ST[ST.length - 4] || {})[u] || [0, 0])[1];
      if (da3 && presi >= 4 && po[1] - pu[1] <= 3) return el.push({ a, b, v: 2, k: "L'ultima all'inseguimento" }); }
    const o = RIV[dk(a, b)]; if (o && o.h >= 5) return el.push({ a, b, v: 1, k: 'Una lunga storia' }); });
  return el.sort((x, y) => y.v - x.v)[0] || null; };
const STL = storia(gi.filter(x => x.n <= n), m => [m[0], m[1], m[2], m[3], m[4]], () => 'L');
const bmS = dopo ? scegli(dopo.m.map(m => [m[0], m[3]]), STL) : null;
// Champions Cup: l'ultima giornata giocata fino allo stesso turno di Serie A (righe: girone, A, fantapunti A, fantapunti B, B, risultato)
const CU = D.cal.cup, cg = CU.filter(x => x.m.every(m => m[5] && m[5] !== '-') && x.sa <= g.sa), nc = cg[cg.length - 1].n, gc = cg[cg.length - 1];
const TC = {}; cg.forEach(x => { x.m.forEach(m => { const r = m[5].split('-').map(Number); [[m[1], r[0], r[1], m[2]], [m[4], r[1], r[0], m[3]]].forEach(([s, a, b, fp]) => { const t = TC[s] = TC[s] || { n: s, g: m[0], pt: 0, fp: 0 }; t.fp += fp; t.pt += a > b ? 3 : a === b ? 1 : 0; }); }); (x.rest || []).forEach(([gr, s]) => { TC[s] = TC[s] || { n: s, g: gr, pt: 0, fp: 0 }; }); });
const gir = {}; Object.values(TC).sort((a, b) => b.pt - a.pt || b.fp - a.fp).forEach(t => { (gir[t.g] = gir[t.g] || []).push({ n: t.n, pt: t.pt }); });
const prossC = CU.find(x => x.n === nc + 1), bcS = prossC ? scegli(prossC.m.map(m => [m[1], m[4]]), storia(cg, m => [m[1], m[2], m[3], m[4], m[5]], m => m[0])) : null;
const props = { cl: C.map(t => ({ n: t.n, pt: t.pt })), nc2: prossC ? prossC.n : null, bigC: bcS,  n, nc, m: g.m.map(m => ({ a: m[0], b: m[3], sc: m[4] })), mc: gc.m.map(m => ({ g: m[0], a: m[1], b: m[4], sc: m[5] })), c: C.slice(0, 3).map(t => ({ n: t.n, pt: t.pt })), gir, big: bmS };
fs.mkdirSync('public', { recursive: true }); const LG = SITO + 'assets/loghi/';
[['logo-lega-o-fant-a-girrr.png', 'logo-lega.png'], ['logo-cup-champions-cup.png', 'logo-coppa.png'], ['logo-tv-girrr-sport-live.png', 'tv-lega.png'], ['logo-tv-cup-girrr-live.png', 'tv-coppa.png']].forEach(([a, b]) => fs.copyFileSync(LG + a, 'public/' + b));
const browserExecutable = process.argv[2];
const serveUrl = await bundle({ entryPoint: './src/index.jsx', publicDir: './public' });
const composition = await selectComposition({ serveUrl, id: 'Giornata', inputProps: props, browserExecutable });
await renderMedia({ composition, serveUrl, codec: 'h264', outputLocation: process.env.USCITA || '/home/user/o-girrr-registro/lab/video-giornata/strada-b-remotion.mp4', inputProps: props, browserExecutable, crf: 22 });
// tempi delle scene per la musica (rilascio/video/musica.py): stessa scaletta di src/index.jsx
const SCENE = eval(/const SC = (\[.*?\]);/s.exec(fs.readFileSync('./src/index.jsx', 'utf8'))[1]).filter(([k]) => k !== 'prossime' || props.big || props.bigC);
fs.writeFileSync('scene.json', JSON.stringify({ fps: 30, scene: SCENE, m: props.m.length, mc: props.mc.length, cl: props.cl.length, derby: !!((props.big && props.big.k === 'derby') || (props.bigC && props.bigC.k === 'derby')) }));   /* per gli effetti di monta_musica.py */
console.log('fatto', JSON.stringify({ big: props.big, bigC: props.bigC }));
