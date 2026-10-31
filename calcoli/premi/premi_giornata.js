// Premi sponsor della giornata: legge la logica di lab/index.html (la stessa dell'Anteprima e della Carriera)
// con i dati veri del sito, e scrive la lista dei premi raggiunti in JSON.
// Uso: node calcoli/premi/premi_giornata.js DATA_JSON LAB_DATI_JSON LAB_HTML USCITA_JSON
// Non scrive nel database: lo fa registra_premi.py.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [dataFile, labDatiFile, labHtmlFile, outFile] = process.argv.slice(2);
if (!outFile) { console.error('Uso: node premi_giornata.js DATA_JSON LAB_DATI_JSON LAB_HTML USCITA_JSON'); process.exit(2); }

const PORTA = 8817;
const labHtml = fs.readFileSync(labHtmlFile, 'utf8');
const data = fs.readFileSync(dataFile, 'utf8');
const dati = JSON.stringify(Object.assign(JSON.parse(fs.readFileSync(labDatiFile, 'utf8')), { img: {} }));

// Il Lab ha la logica dentro una funzione chiusa: prima della chiusura espongo le funzioni che servono.
// Il Lab non cambia: la modifica vive solo in questa pagina temporanea.
const iDati = labHtml.indexOf('<script id="dati"');
const aDati = labHtml.indexOf('>', iDati) + 1;
const bDati = labHtml.indexOf('</script>', iDati);
const coda = '\nrender();\n})();\n</script>';
const k = labHtml.lastIndexOf(coda);
if (k < 0) throw new Error('Fine dello script del Lab non trovata: il Lab è cambiato, va aggiornato questo script');
const esposizione = '\nwindow.__P={teams:function(){return D.teams},fascia:fascia,sponsorDi:sponsorDi,premi52:premi52,premioSponsor:premioSponsor,premioSponsorCoppa:premioSponsorCoppa,mg:mg,get CL(){return CL}};\nrender();\n})();\n</script>';
const html = labHtml.slice(0, aDati) + dati + labHtml.slice(bDati, k) + esposizione + labHtml.slice(k + coda.length);

(async () => {
  const server = require('http').createServer((req, res) => {
    if (req.url.startsWith('/lab/index.html')) { res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); res.end(html); }
    else { res.writeHead(404); res.end(); }
  });
  await new Promise(r => server.listen(PORTA, r));

  const br = await chromium.launch();
  try {
    const p = await br.newPage();
    await p.route('**/*', r => {
      const u = r.request().url();
      if (u.startsWith(`http://localhost:${PORTA}/`)) return r.continue();
      if (u.includes('giandjcosta.github.io/o-fant-a-girrr/data.json')) return r.fulfill({ contentType: 'application/json', body: data });
      return r.abort();
    });
    await p.goto(`http://localhost:${PORTA}/lab/index.html`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await p.waitForFunction(() => window.__P && window.__P.CL, null, { timeout: 30000 });

    const righe = await p.evaluate(() => window.__P.teams().map(t => ({
      team: t,
      manager: window.__P.mg(t),
      fascia: window.__P.fascia(t),
      // premi52 applica il filtro "raggiunto" e registra in sessionStorage della pagina di test: va bene, la pagina è monouso
      premi: window.__P.premi52(t),
    })));

    const premi = [];
    for (const r of righe) {
      for (const pr of r.premi) {
        premi.push({
          team: r.team,
          manager: r.manager,
          objective: pr.obiettivo,
          sponsor: pr.sponsor,
          credits: pr.crediti,
          reputation: pr.reputazione,
        });
      }
    }
    fs.mkdirSync(path.dirname(outFile), { recursive: true });
    fs.writeFileSync(outFile, JSON.stringify({ premi, squadre: righe.length }, null, 1), 'utf8');
    console.log(`premi raggiunti: ${premi.length} su ${righe.length} squadre`);
    for (const x of premi) console.log(`  ${x.team} · ${x.sponsor} · ${x.credits} crediti (${x.objective})`);
  } finally {
    await br.close();
    server.close();
  }
})().catch(e => { console.error('FALLITO:', e.message); process.exit(1); });
