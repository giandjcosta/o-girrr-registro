#!/usr/bin/env node
/* Immagini per i profili social della Lega (Instagram, TikTok, Facebook, X, YouTube).
   Uso: node social/genera.js  (scrive i PNG in social/). Logo e colori sono quelli del sito; la classifica è quella vera. */
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const QUI = __dirname, LOGO = 'https://giandjcosta.github.io/o-fant-a-girrr/assets/loghi/logo-lega-o-fant-a-girrr.png';
const CL = JSON.parse(fs.readFileSync(process.env.CLASSIFICA || path.join(QUI, 'classifica.json'), 'utf8'));
const FONT = '<link href="https://fonts.googleapis.com/css2?family=Lobster&family=Inter:wght@500;700;800;900&display=swap" rel="stylesheet">';
const BASE = `*{box-sizing:border-box;margin:0}body{width:100vw;height:100vh;overflow:hidden;font-family:Inter,system-ui,sans-serif;color:#fbf6ec}
.righe{background:repeating-linear-gradient(115deg,rgba(255,255,255,.045) 0 46px,transparent 46px 92px),radial-gradient(1200px 800px at 80% -10%,#2c3f7c 0,#1d2a52 55%,#141d3d 100%)}
.stadio{background:radial-gradient(900px 600px at 85% -10%,rgba(214,40,57,.45),transparent 62%),radial-gradient(1000px 700px at -10% 20%,rgba(61,147,214,.32),transparent 60%),linear-gradient(180deg,#2c3f7c,#1d2a52 45%,#141d3d)}
.lobster{font-family:Lobster,'Brush Script MT',cursive;font-weight:400}
.oro{color:#ffd166}.rosso{color:#d62839}
.striscia{height:12px;border-radius:2px;transform:skewX(-45deg);background:linear-gradient(90deg,#d62839 0 30%,#ffd166 30% calc(30% + 14px),transparent calc(30% + 14px))}
.logo{filter:drop-shadow(0 18px 30px rgba(0,0,0,.45))}`;

const IMG = {
  'profilo-lega-1080': [1080, 1080, `<body class="righe" style="display:grid;place-items:center"><img class="logo" src="${LOGO}" style="height:760px"></body>`],
  'profilo-stadio-1080': [1080, 1080, `<body style="display:grid;place-items:center;background:radial-gradient(circle at 50% 40%,#e2404f 0,#d62839 45%,#9e1a28 100%)"><img class="logo" src="${LOGO}" style="height:760px"></body>`],
  'copertina-facebook-1640x624': [1640, 624, `<body class="righe" style="display:flex;align-items:center;gap:70px;padding:0 120px">
     <img class="logo" src="${LOGO}" style="height:470px">
     <div><div style="font:800 26px Inter;letter-spacing:.32em" class="oro">LA LEGA · STAGIONE 2026/27</div>
     <div style="font:900 118px/1 Inter;letter-spacing:-.02em;margin:14px 0 18px">O Fant A <span class="rosso">Girrr</span></div>
     <div class="striscia" style="width:640px;margin:0 0 26px 10px"></div>
     <div style="font:700 34px Inter;color:#bfe3ff">Risultati, classifica, Derby e la Curva</div></div></body>`],
  'copertina-x-1500x500': [1500, 500, `<body class="righe" style="display:flex;align-items:center;justify-content:flex-end;gap:56px;padding:0 110px 0 0">
     <div style="text-align:right"><div style="font:800 22px Inter;letter-spacing:.3em" class="oro">LA LEGA · 2026/27</div>
     <div style="font:900 96px/1 Inter;letter-spacing:-.02em;margin:12px 0 18px">O Fant A <span class="rosso">Girrr</span></div>
     <div style="font:700 30px Inter;color:#bfe3ff">Risultati, classifica, Derby e la Curva</div></div>
     <img class="logo" src="${LOGO}" style="height:380px"></body>`],
  'copertina-youtube-2560x1440': [2560, 1440, `<body class="stadio" style="display:grid;place-items:center">
     <div style="width:1546px;height:423px;display:flex;align-items:center;gap:60px;justify-content:center">
     <img class="logo" src="${LOGO}" style="height:400px">
     <div><div style="font:800 28px Inter;letter-spacing:.32em" class="oro">RADIO GIRRR · GIRRR SPORT</div>
     <div class="lobster" style="font-size:150px;line-height:1.05;margin:6px 0">O Fant A Girrr</div>
     <div style="font:700 36px Inter;color:#bfe3ff">Le partite, le voci e le storie della Lega</div></div></div></body>`],
  'post-classifica-1080x1350': [1080, 1350, `<body class="righe" style="padding:70px 72px">
     <div style="display:flex;align-items:center;gap:30px"><img class="logo" src="${LOGO}" style="height:150px">
     <div><div style="font:800 22px Inter;letter-spacing:.3em" class="oro">O FANT A GIRRR · 2026/27</div>
     <div style="font:900 64px/1.02 Inter;margin-top:8px">Classifica dopo<br>la ${CL.g}ª giornata</div></div></div>
     <div class="striscia" style="width:480px;margin:34px 0 30px 10px"></div>
     <div style="display:grid;grid-template-columns:60px 1fr 80px 90px;gap:0 14px;font:700 22px Inter;color:#bfe3ff;padding:0 18px 10px"><span>Pos.</span><span>Squadra</span><span style="text-align:right">DR</span><span style="text-align:right">Pt</span></div>
     ${CL.cl.map((r, i) => `<div style="display:grid;grid-template-columns:60px 1fr 80px 90px;gap:0 14px;align-items:center;padding:15px 18px;margin:0 0 8px;border-radius:14px;background:${i < 3 ? 'rgba(99,188,233,.2)' : i === CL.cl.length - 1 ? 'rgba(239,100,118,.22)' : 'rgba(255,255,255,.07)'};box-shadow:inset 6px 0 ${i < 3 ? '#63bce9' : i === CL.cl.length - 1 ? '#ef6476' : 'transparent'}">
       <b style="font:900 34px Inter;color:${['#ffd166', '#cbd5e1', '#dca17a'][i] || (i === CL.cl.length - 1 ? '#ff7286' : '#fbf6ec')}">${i + 1}</b>
       <b style="font:800 32px Inter;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${r[0]}</b>
       <span style="font:800 30px Inter;text-align:right">${r[2] > 0 ? '+' + r[2] : r[2]}</span><b style="font:900 40px Inter;text-align:right">${r[1]}</b></div>`).join('')}
     <div style="font:700 24px Inter;color:#bfe3ff;margin-top:22px;text-align:center">Tutti i risultati sul sito della Lega · link in bio</div></body>`],
  'storia-1080x1920': [1080, 1920, `<body class="stadio" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 80px">
     <img class="logo" src="${LOGO}" style="height:620px">
     <div style="font:800 30px Inter;letter-spacing:.3em;margin-top:70px" class="oro">LA LEGA · STAGIONE 2026/27</div>
     <div class="lobster" style="font-size:132px;line-height:1.05;margin:20px 0 30px">O Fant A Girrr</div>
     <div style="font:700 44px/1.35 Inter;color:#bfe3ff">Risultati, classifica,<br>Derby e la Curva</div>
     <div style="margin-top:80px;padding:26px 46px;border-radius:999px;background:#ffd166;color:#1d2a52;font:900 36px Inter">Entra nel sito della Lega</div>
     <div style="font:700 28px Inter;margin-top:26px;color:#fbf6ec">Link in bio</div></body>`],
};

(async () => {
  const b = await chromium.launch();
  for (const [nome, [w, h, corpo]] of Object.entries(IMG)) {
    const p = await b.newPage({viewport: {width: w, height: h}});
    await p.setContent(`<!doctype html><html lang="it"><head><meta charset="utf-8">${FONT}<style>${BASE}</style></head>${corpo}</html>`, {waitUntil: 'networkidle'});
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({path: path.join(QUI, nome + '.png')});
    console.log('scritta', nome + '.png', w + 'x' + h);
    await p.close();
  }
  await b.close();
})();
