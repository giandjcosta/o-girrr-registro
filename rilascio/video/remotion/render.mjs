// Calcola i dati veri da data.json e fa il video con Remotion (usando il Chromium già installato).
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import fs from 'fs';
const D = JSON.parse(fs.readFileSync('/tmp/claude-0/srv/o-fant-a-girrr/data.json', 'utf8'));
const L = D.cal.lega, gi = L.filter(x => x.m.every(m => m[4] && m[4] !== '-')), n = gi[gi.length - 1].n, g = L.find(x => x.n === n), dopo = L.find(x => x.n === n + 1);
const T = {}; gi.filter(x => x.n <= n).forEach(x => x.m.forEach(m => { const r = m[4].split('-').map(Number); [[m[0], r[0], r[1], m[1]], [m[3], r[1], r[0], m[2]]].forEach(([s, a, b, fp]) => { const t = T[s] = T[s] || { n: s, pt: 0, fp: 0 }; t.fp += fp; t.pt += a > b ? 3 : a === b ? 1 : 0; }); }));
const C = Object.values(T).sort((a, b) => b.pt - a.pt || b.fp - a.fp);
const bm = dopo.m.find(m => m[0] === C[0].n || m[3] === C[0].n) || dopo.m[0];
// Champions Cup: l'ultima giornata giocata fino allo stesso turno di Serie A (righe: girone, A, fantapunti A, fantapunti B, B, risultato)
const CU = D.cal.cup, cg = CU.filter(x => x.m.every(m => m[5] && m[5] !== '-') && x.sa <= g.sa), nc = cg[cg.length - 1].n, gc = cg[cg.length - 1];
const TC = {}; cg.forEach(x => { x.m.forEach(m => { const r = m[5].split('-').map(Number); [[m[1], r[0], r[1], m[2]], [m[4], r[1], r[0], m[3]]].forEach(([s, a, b, fp]) => { const t = TC[s] = TC[s] || { n: s, g: m[0], pt: 0, fp: 0 }; t.fp += fp; t.pt += a > b ? 3 : a === b ? 1 : 0; }); }); (x.rest || []).forEach(([gr, s]) => { TC[s] = TC[s] || { n: s, g: gr, pt: 0, fp: 0 }; }); });
const gir = {}; Object.values(TC).sort((a, b) => b.pt - a.pt || b.fp - a.fp).forEach(t => { (gir[t.g] = gir[t.g] || []).push({ n: t.n, pt: t.pt }); });
const prossC = CU.find(x => x.n === nc + 1), capi = Object.keys(gir).map(k => gir[k][0].n), bc = prossC ? (prossC.m.find(m => capi.indexOf(m[1]) >= 0 || capi.indexOf(m[4]) >= 0) || prossC.m[0]) : null;
const props = { cl: C.map(t => ({ n: t.n, pt: t.pt })), nc2: prossC ? prossC.n : null, bigC: bc ? [bc[1], bc[4]] : null, n, nc, m: g.m.map(m => ({ a: m[0], b: m[3], sc: m[4] })), mc: gc.m.map(m => ({ g: m[0], a: m[1], b: m[4], sc: m[5] })), c: C.slice(0, 3).map(t => ({ n: t.n, pt: t.pt })), gir, big: [bm[0], bm[3]] };
fs.mkdirSync('public', { recursive: true }); const LG = '/tmp/claude-0/srv/o-fant-a-girrr/assets/loghi/';
[['logo-lega-o-fant-a-girrr.png', 'logo-lega.png'], ['logo-cup-champions-cup.png', 'logo-coppa.png'], ['logo-tv-girrr-sport-live.png', 'tv-lega.png'], ['logo-tv-cup-girrr-live.png', 'tv-coppa.png']].forEach(([a, b]) => fs.copyFileSync(LG + a, 'public/' + b));
const browserExecutable = process.argv[2];
const serveUrl = await bundle({ entryPoint: './src/index.jsx', publicDir: './public' });
const composition = await selectComposition({ serveUrl, id: 'Giornata', inputProps: props, browserExecutable });
await renderMedia({ composition, serveUrl, codec: 'h264', outputLocation: '/home/user/o-girrr-registro/lab/video-giornata/strada-b-remotion.mp4', inputProps: props, browserExecutable, crf: 22 });
console.log('fatto', JSON.stringify({ c: props.c, nc, gir }));
