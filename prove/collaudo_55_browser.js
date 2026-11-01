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
    // risultati: con due colonne (PC) le partite di ogni riga partono alla stessa altezza
    const sc = await p.evaluate(() => { const m = [...document.querySelectorAll('#board>.m')].map(e => e.getBoundingClientRect()); const c = {}; m.forEach(r => { const k = r.left < innerWidth / 2 ? 's' : 'd'; (c[k] = c[k] || []).push(r.top) }); if (!c.s || !c.d) return 0; let d = 0; for (let i = 0; i < Math.min(c.s.length, c.d.length); i++) d = Math.max(d, Math.abs(c.s[i] - c.d[i])); return d });
    return sc <= 3 ? '' : 'partite sfalsate tra le due colonne (' + Math.round(sc) + ' px)';
  }],
  ['tabellone-stadio', 'anteprima/5.5/tabellone-stadio.html', async p => (await p.locator('#campo-link').count()) ? '' : 'manca il link al Campo'],
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
