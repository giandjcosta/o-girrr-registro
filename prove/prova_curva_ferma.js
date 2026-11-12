// Curva aggiornata pezzo per pezzo e Notifiche divise (Claude, 12 novembre 2026).
// iPhone e iPad si provano con WebKit (il motore di Safari), Android e PC con Chromium.
// Controlla che:
//   - cambiando scheda, ricaricando e dopo un ridisegno, intestazione, barra in basso, loghi e cori già disegnati
//     restino gli stessi elementi (non ricreati) e non ripartano le dissolvenze (fx-in di transizioni.js);
//   - il testo che stai scrivendo resti; la pagina non scorra di lato; non ci siano errori;
//   - le Notifiche abbiano «Attività» (senza menzioni) e «Menzioni» (solo menzioni).
// Uso: servire la cartella che contiene o-girrr-registro e una copia di gh-pages come o-fant-a-girrr su http://localhost:8771/, poi
//   WEBKIT=/percorso/di/pw_run.sh node prove/prova_curva_ferma.js      (SOLO=Pixel per un solo schermo)
// Senza WEBKIT gli iPhone si provano con Chromium (e lo dice). Il database si legge soltanto: le scritture sono intercettate.
const { chromium, webkit, devices } = require('playwright');
const L = 'http://localhost:8771/o-girrr-registro/lab/offline/';
const WK = process.env.WEBKIT;
const SCH = [
  ['iPhone SE 320', 'ios', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone 15 Pro', 'ios', devices['iPhone 15 Pro']],
  ['iPad Mini', 'ios', devices['iPad Mini']],
  ['Galaxy S8', 'android', devices['Galaxy S8']], ['Pixel 7', 'android', devices['Pixel 7']], ['Galaxy Tab S4', 'android', devices['Galaxy Tab S4']],
  ['PC 1280', 'altro', { viewport: { width: 1280, height: 800 } }], ['PC 1920', 'altro', { viewport: { width: 1920, height: 1080 } }]
];
const SCRIVE = /salva|scrivi|lancia|rispondi|vota|reagisci|registra|segui|push_|cancella|proponi/;
(async () => {
  const bc = await chromium.launch(), bw = WK ? await webkit.launch({ executablePath: WK }) : null;
  if (!bw) console.log('Attenzione: WebKit non indicato, gli iPhone si provano con Chromium');
  let ko = 0;
  for (const [sn, att, o] of SCH) {
    if (process.env.SOLO && !sn.includes(process.env.SOLO)) continue;
    const motore = att === 'ios' && bw ? 'WebKit' : 'Chromium';
    const c = await (motore === 'WebKit' ? bw : bc).newContext(o);
    await c.route('**/rest/v1/rpc/**', async r => { const n = r.request().url().split('/rpc/')[1].split('?')[0]; if (SCRIVE.test(n) && !/_(stato|pubblico|lista)$/.test(n)) return r.fulfill({ json: null }); return r.continue(); });
    const p = await c.newPage(); const errs = [], pr = [];
    let fase = 'apertura';
    const interrotte = [];
    // Cambiando pagina WebKit segnala le richieste ancora in corso della pagina che si chiude come «access control checks»:
    // non sono errori della Curva, si contano a parte (e si dicono)
    p.on('pageerror', e => (fase === 'cambio pagina' && /access control checks/.test(e.message) ? interrotte : errs).push(fase + ': ' + e.message.slice(0, 90)));
    await p.goto(L); await p.waitForTimeout(3000);
    for (const [pn, u] of [['Lega', 'sito/girrr/curva.html'], ['Stadio', 'sito/stadio/girrr/curva.html']]) {
      try {
        fase = 'cambio pagina'; await p.goto(L + u); fase = pn + ' apertura'; await p.waitForSelector('#nav button', { timeout: 25000 }); await p.waitForTimeout(2200);
        if (await p.evaluate(() => !window.__curvaProva)) { pr.push(pn + ': pagina vecchia (manca l\'aggancio __curvaProva: rilascio/curva-os/applica.py --lab)'); continue; }
        // Segno gli elementi che devono restare
        await p.evaluate(() => {
          const s = (sel, k) => { const e = document.querySelector(sel); if (e) e.__segno = k; };
          s('#top .bar', 'bar'); s('#top .tabs', 'tabs'); s('#top .lg', 'logo'); s('#nav .sito img', 'logoNav'); s('#nav button[data-v=home]', 'home');
          document.querySelectorAll('#vista article.post').forEach((a, i) => { if (i < 3) a.__segno = 'post' + i; });
        });
        const stessi = (cosa) => p.evaluate((cosa) => {
          const out = [], q = (sel, k) => { const e = document.querySelector(sel); if (!e || e.__segno !== k) out.push(k); };
          q('#top .bar', 'bar'); q('#top .tabs', 'tabs'); q('#top .lg', 'logo'); q('#nav .sito img', 'logoNav'); q('#nav button[data-v=home]', 'home');
          if (cosa === 'cori') { const ks = [...document.querySelectorAll('#vista article.post')].filter(a => /^post/.test(a.__segno || '')).length; if (ks < 3) out.push('cori ' + ks + '/3'); }
          const fx = [...document.querySelectorAll('#top .fx-in, #nav .fx-in, #top.fx-in, #nav.fx-in')].map(e => e.className);
          if (fx.length) out.push('dissolvenza: ' + fx.join(','));
          return out;
        }, cosa);
        fase = pn + ' ridisegno';
        // 1. Ridisegno senza cambi (come dopo un applauso o l'aggiornamento di ogni minuto)
        await p.evaluate(() => __curvaProva.render()); await p.waitForTimeout(60);
        let d = await stessi('cori'); if (d.length) pr.push(pn + ' ridisegno: ricreati ' + d.join(' '));
        fase = pn + ' ricarica';
        // 2. Ricarica (pulsante Aggiorna)
        await p.click('[aria-label="Aggiorna"]'); await p.waitForSelector('.ptrb:not(.sp)', { state: 'attached', timeout: 20000 }); await p.waitForTimeout(80);
        d = await stessi('cori'); if (d.length) pr.push(pn + ' ricarica: ricreati ' + d.join(' '));
        fase = pn + ' schede';
        // 3. Cambio di scheda e ritorno: intestazione e barra restano, i cori della prima scheda tornano gli stessi
        await (await p.$$('.tabs button'))[3].click(); await p.waitForTimeout(60);
        d = await stessi(); if (d.length) pr.push(pn + ' cambio di scheda: ricreati ' + d.join(' '));
        await (await p.$$('.tabs button'))[0].click(); await p.waitForTimeout(60);
        d = await stessi(); if (d.length) pr.push(pn + ' ritorno: ricreati ' + d.join(' '));
        const sw = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]); if (sw[0] > sw[1] + 1) pr.push(pn + ': scorre di lato');
        fase = pn + ' entrata come squadra';
        // 4. Entro come squadra (dentro la pagina) per il campo di scrittura e le Notifiche
        const ok = await p.evaluate(() => { try { __curvaProva.entra('Oranje VC'); return !!document.getElementById('tx'); } catch (e) { return e.message; } });
        if (ok !== true) { pr.push(pn + ': non riesco a entrare come squadra ' + ok); continue; }
        await p.fill('#tx', 'Prova di scrittura'); await p.evaluate(() => { document.getElementById('tx').__segno = 'tx'; __curvaProva.render(); });
        const tx = await p.evaluate(() => { const t = document.getElementById('tx'); return [t.__segno === 'tx', t.value]; });
        if (!tx[0] || tx[1] !== 'Prova di scrittura') pr.push(pn + ': il testo che scrivi non resta ' + JSON.stringify(tx));
        await p.fill('#tx', '');
        // Notifiche: Attività e Menzioni
        fase = pn + ' notifiche';
        // Notifiche vere della squadra (calcolate dalla pagina): Attività senza menzioni, Menzioni solo menzioni
        await p.evaluate(() => { __curvaProva.vai('notifiche', 'tutte'); });
        const nt = async () => p.evaluate(() => { const tutte = __curvaProva.notifiche(), testo = document.getElementById('vista').innerText;
          return { schede: [...document.querySelectorAll('.tabs button')].map(b => b.textContent + (b.classList.contains('on') ? '*' : '')).join(' | '),
            men: (testo.match(/ti ha menzionato/g) || []).length, totMen: tutte.filter(o => o.tp === 'men').length, totAtt: tutte.filter(o => o.tp !== 'men').length, vuoto: !!document.querySelector('#vista .vuoto') }; });
        let n1 = await nt();
        if (!/^Attività\* \| Menzioni$/.test(n1.schede) || n1.men) pr.push(pn + ': scheda Attività ' + JSON.stringify(n1));
        if (!n1.totAtt && !n1.vuoto) pr.push(pn + ': Attività vuota senza messaggio');
        await p.evaluate(() => { __curvaProva.vai('notifiche', 'men'); });
        n1 = await nt();
        if (!/^Attività \| Menzioni\*$/.test(n1.schede) || n1.men !== n1.totMen) pr.push(pn + ': scheda Menzioni ' + JSON.stringify(n1));
        if (pn === 'Stadio' && /Pixel 7|iPhone 15/.test(sn)) console.log('   Notifiche di Oranje VC: ' + n1.totAtt + ' in Attività, ' + n1.totMen + ' in Menzioni');
        await p.evaluate(() => { __curvaProva.vai('home'); });
        await p.waitForLoadState('networkidle').catch(() => {});   // WebKit segnala come errore le richieste interrotte cambiando pagina
      } catch (e) { pr.push(pn + ': ' + e.message.split('\n')[0].slice(0, 100)); }
    }
    if (errs.length) pr.push('errori JS: ' + [...new Set(errs)].join(' / '));
    ko += pr.length;
    console.log((pr.length ? '✗ ' : '✓ ') + sn + ' (' + motore + ')' + (pr.length ? ' → ' + pr.join(' | ') : '') + (interrotte.length ? '  [richieste interrotte cambiando pagina: ' + interrotte.length + ']' : ''));
    await c.close();
  }
  console.log(ko ? 'Problemi: ' + ko : 'Tutto a posto'); await bc.close(); if (bw) await bw.close();
})();
