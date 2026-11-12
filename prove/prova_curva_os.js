// Curva · Stile e movimenti di iPhone e di Android (Claude, 12 novembre 2026).
// Controlla che ogni telefono riceva il suo stile (iPhone e iPad → ios, Android → android, PC e TV → altro), che la pagina
// non scorra di lato e che non ci siano errori; e che i movimenti partano quando devono:
//   cambio di scheda (indicatore che scivola, contenuto), cambio di sezione (barra in basso, contenuto), niente all'apertura dopo l'avvio,
//   ricarica (rotellina di iOS o forma di Android), onda al tocco su Android, barra che si rimpicciolisce scorrendo su iPhone.
// Uso: servire la cartella che contiene o-girrr-registro e una copia di gh-pages come o-fant-a-girrr su http://localhost:8771/, poi
//   node prove/prova_curva_os.js [CARTELLA_FOTO]      (SOLO=Pixel per provare solo gli schermi con quel nome)
// Il database si legge soltanto: le funzioni che scrivono sono intercettate.
const { chromium, devices } = require('playwright');
const L = 'http://localhost:8771/o-girrr-registro/lab/offline/';
const D = process.argv[2];
const TV = 'Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/94.0 TV Safari/537.36';
const SCH = [
  ['iPhone SE 320', 'ios', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['iPhone 15 Pro', 'ios', devices['iPhone 15 Pro']], ['iPhone 15 Pro Max', 'ios', devices['iPhone 15 Pro Max']],
  ['Galaxy S8', 'android', devices['Galaxy S8']], ['Pixel 7', 'android', devices['Pixel 7']], ['Galaxy S24', 'android', devices['Galaxy S24'] || devices['Galaxy S9+']],
  ['iPad Mini', 'ios', devices['iPad Mini']], ['iPad orizzontale', 'ios', devices['iPad (gen 7) landscape']], ['Galaxy Tab S4', 'android', devices['Galaxy Tab S4']], ['Galaxy Tab S4 orizzontale', 'android', devices['Galaxy Tab S4 landscape']],
  ['PC 1280', 'altro', { viewport: { width: 1280, height: 800 } }], ['PC 1920', 'altro', { viewport: { width: 1920, height: 1080 } }],
  ['Monitor 2560', 'altro', { viewport: { width: 2560, height: 1440 } }], ['Smart TV', 'altro', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: TV }]
];
const SCRIVE = /salva|scrivi|lancia|rispondi|vota|reagisci|registra|segui|push_|cancella|proponi/;
// Nome dell'animazione in corso su un elemento (o sul suo ::before / ::after)
const ANIM = (sel, ps) => { const e = document.querySelector(sel); return e ? getComputedStyle(e, ps || null).animationName : '-'; };
(async () => {
  const b = await chromium.launch(); let ko = 0;
  for (const [sn, att, o] of SCH) {
    if (process.env.SOLO && !sn.includes(process.env.SOLO)) continue;
    const c = await b.newContext(o);
    await c.route('**/rest/v1/rpc/**', async r => { const n = r.request().url().split('/rpc/')[1].split('?')[0]; if (SCRIVE.test(n) && !/_(stato|pubblico|lista)$/.test(n)) return r.fulfill({ json: null }); return r.continue(); });
    const p = await c.newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message.slice(0, 90)));
    await p.goto(L); await p.waitForTimeout(2500); const pr = [];
    const tel = o.viewport.width < 760, mob = att !== 'altro';
    for (const [pn, u] of [['Lega', 'sito/girrr/curva.html'], ['Stadio', 'sito/stadio/girrr/curva.html']]) {
      await p.goto(L + u); await p.waitForSelector('#nav button', { timeout: 20000 });
      if (mob) { const a = await p.evaluate(() => document.documentElement.hasAttribute('data-os-avvio')); if (!a) pr.push(pn + ': manca l\'entrata all\'apertura'); }
      await p.waitForTimeout(1600);
      const i = await p.evaluate(() => ({ os: document.documentElement.dataset.os, sw: document.documentElement.scrollWidth, w: innerWidth, c: ['data-cambio-nav', 'data-cambio-tabs', 'data-os-avvio'].some(a => document.documentElement.hasAttribute(a)) }));
      if (i.os !== att) pr.push(pn + ': stile ' + i.os); if (i.sw > i.w + 1) pr.push(pn + ': scorre di lato ' + i.sw); if (i.c) pr.push(pn + ': segni di cambio rimasti accesi');
      if (D) await p.screenshot({ path: D + '/curva-' + pn + '-' + sn.replace(/\W+/g, '_') + '.png' });

      // Cambio di scheda in alto: l'indicatore scivola e il contenuto si muove
      const tb = await p.$$('.tabs button');
      if (tb.length > 1) {
        await tb[2].click(); await p.waitForTimeout(40);
        for (const ms of [0, 120]) { await p.waitForTimeout(ms); const z = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth, innerHeight]); if (z[0] > z[1] + 1 || z[1] !== o.viewport.width) { pr.push(pn + ': durante il cambio di scheda la pagina si allarga ' + JSON.stringify(z)); break; } }
        const a = await p.evaluate(([f]) => { const os = document.documentElement.dataset.os, F = new Function('return ' + f)();
          return { c: document.documentElement.hasAttribute('data-cambio-tabs'), ind: F('.tabs .on', os === 'ios' ? '::before' : '::after'), vista: F('#vista'), dx: getComputedStyle(document.documentElement).getPropertyValue('--os-tabs-dx'), dir: getComputedStyle(document.documentElement).getPropertyValue('--os-dir') }; }, [ANIM.toString()]);
        if (mob && (!a.c || !/scivola/.test(a.ind) || !/laterale|asse/.test(a.vista) || !parseFloat(a.dx) || a.dir.trim() !== '1')) pr.push(pn + ': cambio di scheda ' + JSON.stringify(a));
        if (!mob && a.c) pr.push(pn + ': animazioni nuove anche sul PC');
        await p.waitForTimeout(900);
        // Applauso simulato: la Curva ridisegna senza cambiare scheda → niente animazione dell'indicatore
        await p.evaluate(() => { const v = document.querySelector('.tabs'); v.appendChild(document.createElement('i')); });
        await p.waitForTimeout(40);
        if (await p.evaluate(() => document.documentElement.hasAttribute('data-cambio-tabs'))) pr.push(pn + ': animazione senza cambio di scheda');
        await (await p.$$('.tabs button'))[0].click(); await p.waitForTimeout(40);
        const d2 = await p.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue('--os-dir').trim());
        if (mob && d2 !== '-1') pr.push(pn + ': direzione indietro sbagliata ' + d2);
        await p.waitForTimeout(900);
      }

      // Ricarica: rotellina (iOS) o forma (Android)
      await p.click('[aria-label="Aggiorna"]'); await p.waitForTimeout(150);
      const rc = await p.evaluate(([f]) => { const os = document.documentElement.dataset.os, F = new Function('return ' + f)(); return { sp: !!document.querySelector('.ptrb.sp'), an: F('.ptrb', os === 'ios' ? '::before' : '::after'), svg: F('.ptrb svg') }; }, [ANIM.toString()]);
      if (att === 'ios' && rc.sp && rc.an !== 'os-ios-raggi') pr.push(pn + ': rotellina di iOS ' + JSON.stringify(rc));
      if (att === 'android' && rc.sp && rc.an !== 'os-and-forma') pr.push(pn + ': forma di Android ' + JSON.stringify(rc));
      if (att === 'altro' && rc.sp && rc.svg !== 'giro') pr.push(pn + ': ricarica del PC cambiata ' + JSON.stringify(rc));
      await p.waitForSelector('.ptrb:not(.sp)', { timeout: 15000 }).catch(() => pr.push(pn + ': la ricarica non finisce'));
      await p.waitForTimeout(300);

      // Onda al tocco (solo Android)
      if (att === 'android' && tb.length) {
        const bx = await (await p.$$('.tabs button'))[1].boundingBox();
        await p.mouse.move(bx.x + 10, bx.y + 10); await p.mouse.down();
        const on = await p.evaluate(() => !!document.querySelector('.os-onda')); await p.mouse.up();
        if (!on) pr.push(pn + ': manca l\'onda al tocco');
        await p.waitForTimeout(900);
        await (await p.$$('.tabs button'))[0].click(); await p.waitForTimeout(900);
      }

      if (tel) {
        // Cambio di sezione in basso
        await p.click('#nav button[data-v=esplora]'); await p.waitForTimeout(40);
        const a = await p.evaluate(([f]) => { const os = document.documentElement.dataset.os, F = new Function('return ' + f)();
          return { c: document.documentElement.hasAttribute('data-cambio-nav'), ind: os === 'ios' ? F('#nav .on', '::before') : F('#nav .on svg'), vista: F('#vista') }; }, [ANIM.toString()]);
        if (mob && (!a.c || !/scivola|pillola/.test(a.ind) || !/appare|attraverso/.test(a.vista))) pr.push(pn + ': cambio di sezione ' + JSON.stringify(a));
        await p.waitForTimeout(900);
        const sw = await p.evaluate(() => document.documentElement.scrollWidth); if (sw > o.viewport.width + 1) pr.push(pn + ' Esplora: scorre di lato');
        if (D && /Pixel 7|iPhone 15 Pro$/.test(sn)) await p.screenshot({ path: D + '/curva-' + pn + '-' + sn.replace(/\W+/g, '_') + '-esplora.png' });
        await p.click('#nav button[data-v=home]'); await p.waitForTimeout(900);
        // iPhone: scorrendo in giù la barra si rimpicciolisce, risalendo torna grande
        if (att === 'ios') {
          await p.mouse.wheel(0, 900); await p.waitForTimeout(500);
          const giu = await p.evaluate(() => [document.documentElement.hasAttribute('data-giu'), getComputedStyle(document.querySelector('.nav')).scale]);
          await p.mouse.wheel(0, -300); await p.waitForTimeout(500);
          const su = await p.evaluate(() => document.documentElement.hasAttribute('data-giu'));
          if (!giu[0] || giu[1] === 'none' || su) pr.push(pn + ': barra che si rimpicciolisce ' + JSON.stringify([giu, su]));
          if (D && sn === 'iPhone 15 Pro' && pn === 'Stadio') { await p.mouse.wheel(0, 900); await p.waitForTimeout(700); await p.screenshot({ path: D + '/curva-Stadio-iPhone_15_Pro-giu.png' }); }
        }
      }
    }
    if (errs.length) pr.push('errori JS: ' + [...new Set(errs)].join(' / '));
    ko += pr.length;
    console.log((pr.length ? '✗ ' : '✓ ') + sn + ' (' + att + ')' + (pr.length ? ' → ' + pr.join(' | ') : ''));
    await c.close();
  }
  console.log(ko ? 'Problemi: ' + ko : 'Tutto a posto'); await b.close();
})();
