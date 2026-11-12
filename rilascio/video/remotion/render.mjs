// Calcola i dati veri da data.json e fa il video con Remotion (usando il Chromium già installato).
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import fs from 'fs';
const D = JSON.parse(fs.readFileSync('/tmp/claude-0/srv/o-fant-a-girrr/data.json', 'utf8'));
const L = D.cal.lega, gi = L.filter(x => x.m.every(m => m[4] && m[4] !== '-')), n = gi[gi.length - 1].n, g = L.find(x => x.n === n), dopo = L.find(x => x.n === n + 1);
const T = {}; gi.filter(x => x.n <= n).forEach(x => x.m.forEach(m => { const r = m[4].split('-').map(Number); [[m[0], r[0], r[1], m[1]], [m[3], r[1], r[0], m[2]]].forEach(([s, a, b, fp]) => { const t = T[s] = T[s] || { n: s, pt: 0, fp: 0 }; t.fp += fp; t.pt += a > b ? 3 : a === b ? 1 : 0; }); }));
const C = Object.values(T).sort((a, b) => b.pt - a.pt || b.fp - a.fp);
const bm = dopo.m.find(m => m[0] === C[0].n || m[3] === C[0].n) || dopo.m[0];
const props = { n, m: g.m, c: C.slice(0, 3).map(t => ({ n: t.n, pt: t.pt })), big: [bm[0], bm[3]], altre: dopo.m.filter(m => m !== bm).map(m => [m[0], m[3]]) };
fs.mkdirSync('public', { recursive: true }); fs.copyFileSync('/tmp/claude-0/srv/o-fant-a-girrr/assets/loghi/logo-lega-o-fant-a-girrr.png', 'public/logo.png');
const browserExecutable = process.argv[2];
const serveUrl = await bundle({ entryPoint: './src/index.jsx', publicDir: './public' });
const composition = await selectComposition({ serveUrl, id: 'Giornata', inputProps: props, browserExecutable });
await renderMedia({ composition, serveUrl, codec: 'h264', outputLocation: '/home/user/o-girrr-registro/lab/video-giornata/strada-b-remotion.mp4', inputProps: props, browserExecutable, crf: 22 });
console.log('fatto', JSON.stringify(props.c));
