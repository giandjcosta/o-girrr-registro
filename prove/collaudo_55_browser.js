#!/usr/bin/env node
/* Collaudo dell'Anteprima 5.5 su telefono, tablet e PC, con Chromium e WebKit (Safari).
   Uso: node prove/collaudo_55_browser.js [chromium,webkit]   (serve il registro su http://127.0.0.1:8765)
   Scrive le foto in prove/risultati-55-browser/ e termina con errore se qualcosa non va. */
const {chromium, webkit} = require('playwright');
const fs = require('fs'), path = require('path');
const BASE = 'http://127.0.0.1:8765/';
const OUT = path.join(__dirname, 'risultati-55-browser');
fs.mkdirSync(OUT, {recursive: true});
const MOTORI = (process.argv[2] || 'chromium,webkit').split(',');
const SCHERMI = [['SE', 320, 640], ['iPhone', 390, 844], ['tablet', 768, 1024], ['PC', 1280, 800], ['PC-grande', 1440, 900]];

// Ogni pagina: indirizzo, controlli specifici (devono restituire '' se va bene, altrimenti il problema)
const PAGINE = [
  ['home-lega', 'anteprima/5.5/index-lega.html', async p => (await p.locator('#v53metrics .v55-summary').count()) === 1 && (await p.locator('#v53news a').count()) > 0 ? '' : 'Riepilogo unico o collegamenti delle notifiche mancanti'],
  ['home-stadio', 'anteprima/5.5/index-stadio.html', async p => (await p.locator('#v53metrics .v55-summary').count()) === 1 && (await p.locator('#v53news a').count()) > 0 ? '' : 'Riepilogo unico o collegamenti delle notifiche mancanti'],
  ['notifiche', 'anteprima/5.5/notifiche-lega.html', async p => (await p.locator('.v53-notifcard').count()) > 0 ? '' : 'nessuna notifica'],
  ['tabellone-lega', 'anteprima/5.5/tabellone-lega.html', async p => {
    if (!(await p.locator('.panel tr.zona-1').count())) return 'classifica senza fasce';
    const x = await p.evaluate(() => [...new Set([...document.querySelectorAll('.panel td.n .formadots')].map(e => Math.round(e.getBoundingClientRect().left)))].length);
    if (x !== 1) return 'pallini non allineati (' + x + ' colonne)';
    await p.click('.v55-schede button[data-sez=risultati]'); await p.waitForTimeout(600);
    // risultati su PC: cinque partite tre a sinistra e due a destra, le due di destra con lo stesso spazio sopra e sotto
    const sc = await p.evaluate(() => { const m = [...document.querySelectorAll('#board>.m')].filter(e => e.offsetParent).map(e => e.getBoundingClientRect()); if (m.length !== 5) return ''; const s = m.filter(r => r.left < innerWidth / 2), d = m.filter(r => r.left >= innerWidth / 2); if (!d.length) return ''; if (s.length !== 3 || d.length !== 2) return 'colonne ' + s.length + '+' + d.length; const sopra = d[0].top - s[0].top, sotto = s[2].bottom - d[1].bottom; return Math.abs(sopra - sotto) <= 3 ? '' : 'spazio sopra ' + Math.round(sopra) + ' px e sotto ' + Math.round(sotto) + ' px' });
    return sc ? 'partite su PC non disposte 3 + 2: ' + sc : '';
  }],
  ['tabellone-stadio', 'anteprima/5.5/tabellone-stadio.html', async p => (await p.locator('#campo-link').count()) ? '' : 'manca il link al Campo'],
  // Versione C: tre schede alte uguali in Campionato e Coppa, freccia accanto a «Campo», azzurre in coppa; fase finale a tabellone di tennis
  ['tabellone-c', 'anteprima/5.5/tabellone-lega.html', async p => {
    const misura = () => p.evaluate(() => [...document.querySelectorAll('.v55-schede>button,.v55-schede>a')].filter(e => e.offsetParent).map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.height), Math.round(r.width), Math.round(r.top)] }));
    const lega = await misura();
    if (lega.length !== 3 || new Set(lega.map(x => x[0] + '|' + x[2])).size !== 1) return 'schede del Campionato non su una riga o di altezza diversa: ' + JSON.stringify(lega);
    await p.click('.sw button[data-m=coppa]'); await p.waitForTimeout(500);
    const coppa = await misura();
    if (JSON.stringify(coppa.map(x => x.slice(0, 2))) !== JSON.stringify(lega.map(x => x.slice(0, 2))) || new Set(coppa.map(x => x[2])).size !== 1) return 'schede della Coppa diverse dal Campionato: ' + JSON.stringify(coppa);
    if (!/coppa=1/.test(await p.getAttribute('#campo-link', 'href'))) return 'Campo non porta alla Coppa';
    const sel = await p.evaluate(() => getComputedStyle(document.querySelector('.v55-schede>button[aria-selected=true]')).backgroundColor);
    if (sel !== 'rgb(61, 147, 214)') return 'scheda attiva della Coppa non azzurra: ' + sel;
    await p.click('#chips button[data-n="11"]'); await p.waitForTimeout(900);
    const q = await p.evaluate(() => { const b = document.getElementById('v55ko'); return b && !b.hidden && b.dataset.fase === 'q' && b.querySelectorAll('.v55-ko-col[data-c=q] .v55-ko-m').length === 4 });
    if (!q) return 'tabellone dei quarti assente';
    await p.click('#chips button[data-n="13"]'); await p.waitForTimeout(1200);
    const f = await p.evaluate(() => document.getElementById('v55ko').dataset.fase === 'f' && document.querySelector('.v55-ko-col[data-c=q]').getBoundingClientRect().width < 2);
    return f ? '' : 'in Finale le colonne precedenti non si chiudono';
  }],
  ['spogliatoio', 'lab/prova-spogliatoio-55.html', async p => {
    await p.click('.skin-menu summary'); await p.waitForTimeout(300);
    if ((await p.locator('.skin-menu .skin button').count()) !== 6) return 'il menu non elenca le sei grafiche';
    await p.click('.skin button[data-skin=stadio]'); await p.waitForTimeout(400);
    const ok = await p.evaluate(() => document.documentElement.dataset.skin === 'stadio' && !document.querySelector('.skin-menu').open);
    return ok ? '' : 'la grafica Stadio non si applica o il menu resta aperto';
  }],
  ['campo-coppa', 'anteprima/5.5/campo-lega.html?skin=lega&coppa=1&giornata=2', async p => (await p.locator('.pitch .pl').count()) === 22 && /Champions Cup · Girone/.test(await p.textContent('.phase')) ? '' : 'Campo della Coppa senza formazioni o senza girone'],
  ['campo-lega', 'anteprima/5.5/campo-lega.html?skin=lega&giornata=5&partita=3', async p => {
    if ((await p.locator('.pitch .pl').count()) !== 22) return 'formazioni incomplete';
    const det = p.locator('details.campo-legend');
    if (await det.evaluate(e => e.open)) return 'legenda aperta all\'inizio';
    await det.locator('summary').click();
    if (!(await det.evaluate(e => e.open))) return 'la legenda non si apre';
    const righe = await p.evaluate(() => { const r = {}; document.querySelectorAll('.pitch .pl').forEach(e => { const c = e.querySelector('b').getBoundingClientRect(); (r[e.style.top] = r[e.style.top] || []).push(c.top + c.height / 2) }); return Math.max(...Object.values(r).map(v => Math.max(...v) - Math.min(...v))) });
    if (righe > 1) return 'reparti non allineati (' + righe.toFixed(1) + ' px)';
    return (await p.locator('svg.andamento text.val').count()) ? '' : 'grafico senza numeri';
  }],
  ['campo-stadio', 'anteprima/5.5/campo-stadio.html?skin=stadio&giornata=2&partita=1', async p => (await p.locator('.pitch .pl').count()) >= 20 ? '' : 'formazioni mancanti'],
  ['albo-annuario', 'anteprima/5.5/albo-lega.html', async p => {
    await p.getByText('Annuario', {exact: true}).first().click(); await p.waitForTimeout(800);
    const m = await p.evaluate(() => { const s = document.querySelector('.seg.oro-scroll'), a = s && s.querySelector('[aria-pressed=true]'); if (!a) return null; const rs = s.getBoundingClientRect(), ra = a.getBoundingClientRect(); return [rs.height, ra.height] });
    if (!m) return 'schede dell\'Albo mancanti';
    return m[0] - m[1] <= 12 ? '' : 'scheda attiva troppo piccola rispetto alla riga (' + Math.round(m[0]) + '/' + Math.round(m[1]) + ' px)';
  }],
  ['albo-stadio', 'anteprima/5.5/albo-stadio.html', async p => (await p.locator('.seg.oro-scroll button').count()) > 3 ? '' : 'schede mancanti'],
  ['curva', 'anteprima/5.5/curva-lega.html', async p => (await p.locator('#v53poll').count()) ? '' : 'sondaggio mancante'],
  ['carriera', 'anteprima/attuale.html?come=Grodah#carriera', async p => (await p.getByText('Carriera da allenatore').count()) ? '' : 'Carriera non aperta'],
  ['totogirrr-stadio', 'anteprima/totogirrr-52.html?skin=stadio', null],
  ['novita', 'lab/novita-5-5.html', async p => (await p.locator('article.card').count()) >= 10 ? '' : 'schede della vetrina mancanti'],
];

(async () => {
  const esiti = [], problemi = [];
  for (const nome of MOTORI) {
    const tipo = {chromium, webkit}[nome];
    let b;
    try { b = await tipo.launch() } catch (e) { problemi.push(nome + ': browser non disponibile (' + e.message.split('\n')[0] + ')'); continue }
    for (const [sch, w, h] of SCHERMI) {
      const c = await b.newContext({viewport: {width: w, height: h}, deviceScaleFactor: 1, isMobile: nome === 'chromium' && w < 768, hasTouch: w < 768});
      for (const [chiave, url, controllo] of PAGINE) {
        const p = await c.newPage(), err = [];
        p.on('pageerror', e => err.push('JS: ' + e.message.slice(0, 140)));
        p.on('response', r => { if (r.status() >= 400 && r.url().startsWith(BASE)) err.push(r.status() + ' ' + r.url().slice(BASE.length)) });
        let nota = '';
        try {
          await p.goto(BASE + url, {waitUntil: 'networkidle', timeout: 45000});
          await p.waitForTimeout(700);
          if (controllo) nota = await controllo(p);
          // menu a tendina: l'elenco aperto deve avere uno sfondo pieno (su PC è bianco se il menu è trasparente)
          const menu = await p.evaluate(() => [...document.querySelectorAll('select')].filter(x => x.offsetParent).some(x => { const o = x.options[0]; if (!o) return false; const bg = getComputedStyle(o).backgroundColor, sb = getComputedStyle(x).backgroundColor; return (bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') && /rgba\(.*, 0\.?\d*\)$/.test(sb) && !/, 1\)$/.test(sb) }));
          if (menu) nota = (nota ? nota + '; ' : '') + 'menu a tendina illeggibile su PC';
          const ov = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
          if (ov > 1) nota = (nota ? nota + '; ' : '') + 'scorre di lato di ' + ov + ' px';
          await p.screenshot({path: path.join(OUT, `${nome}-${sch}-${chiave}.jpg`), type: 'jpeg', quality: 55});
        } catch (e) { nota = 'errore: ' + e.message.split('\n')[0].slice(0, 160) }
        const esito = {motore: nome, schermo: sch + ' ' + w + 'px', pagina: chiave, ok: !nota && !err.length, nota, errori: err};
        esiti.push(esito);
        console.log((esito.ok ? 'OK   ' : 'NO   ') + nome.padEnd(8) + (sch + ' ' + w).padEnd(15) + chiave.padEnd(18) + (nota || '') + (err.length ? ' | ' + err.join(' | ') : ''));
        if (!esito.ok) problemi.push(`${nome} ${sch} ${chiave}: ${nota} ${err.join(' | ')}`.trim());
        await p.close();
      }
      await c.close();
    }
    await b.close();
  }
  fs.writeFileSync(path.join(OUT, 'esiti.json'), JSON.stringify({quando: new Date().toISOString(), esiti, problemi}, null, 1));
  console.log('\nPagine provate: ' + esiti.length + ' · problemi: ' + problemi.length);
  problemi.forEach(x => console.log(' - ' + x));
  process.exit(problemi.length ? 1 : 0);
})();
