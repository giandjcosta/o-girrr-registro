// Carriera (Claude, 13 novembre 2026): con la squadra «La mia settimana» prima di «Regole» (ultima voce); da ospite «La settimana delle squadre» con le 10 squadre. Uso: copia di gh-pages con rilascio/tifosi60 servita su localhost:8771 (BASE per un altro indirizzo), MOTORE=chromium|firefox|webkit node prove/prova_settimana_ospite.js
const pw = require('playwright'), { devices } = pw, fs = require('fs');
const M = process.env.MOTORE || 'chromium', B = process.env.BASE || 'http://localhost:8771/o-fant-a-girrr/';
(async () => { let ko = 0;
 for (const [n, o0] of [['iPhone SE 320', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['Pixel 7', devices['Pixel 7']], ['PC 1280', { viewport: { width: 1280, height: 800 } }], ['TV', { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 }]]) {
  for (const ospite of [false, true]) for (const sk of ['girrr/', 'stadio/girrr/']) {
   const o = { ...o0 }; delete o.defaultBrowserType; if (M === 'firefox') delete o.isMobile;
   let c, chiudi; if (M === 'firefox') { const d = fs.mkdtempSync('/tmp/ffp-'); fs.cpSync('/tmp/claude-0/ffprofilo', d, { recursive: true }); c = await pw.firefox.launchPersistentContext(d, { executablePath: '/tmp/claude-0/pw/firefox-1543/firefox/firefox', ...o }); chiudi = () => c.close(); } else { const b = await pw[M].launch(); c = await b.newContext(o); chiudi = () => b.close(); }
   await c.addInitScript(require('/home/user/o-girrr-registro/prove/blocca_scritture.js').script);
   if (!ospite) await c.addInitScript(() => { try { localStorage.setItem('fg', JSON.stringify({ team: 'Oranje VC', code: 'PROVA' })); } catch (e) {} });
   const p = await c.newPage(), pr = [], err = []; p.on('pageerror', e => err.push(e.message.slice(0, 100)));
   await p.goto(B + sk + 'app.html' + (ospite ? '?ospite=1' : '') + '#carriera'); await p.waitForTimeout(3000);
   const r = await p.evaluate(() => ({ menu: [...document.querySelectorAll('#view .seg button')].filter(b => b.dataset.ctab || b.hasAttribute('data-pt-week')).map(b => b.textContent), tutti: !!document.getElementById('pt-storia-tutti'), squadre: document.querySelectorAll('[data-pt-guest]').length, tendine: document.querySelectorAll('#pt-storia-tutti .pt-week').length, lato: document.documentElement.scrollWidth > innerWidth + 1 }));
   if (!ospite) { const i = r.menu.indexOf('La mia settimana'); if (i < 0 || r.menu[r.menu.length - 1] !== 'Regole' || i !== r.menu.length - 2) pr.push('menu: ' + r.menu.join(' | ')); if (r.tutti) pr.push('settimane di tutti con la squadra'); 
    await p.click('[data-pt-week]'); await p.waitForTimeout(800); if (!(await p.locator('#pt-storia .pt-week').count())) pr.push('La mia settimana vuota'); }
   else { if (!r.tutti || r.squadre !== 10 || !r.tendine) pr.push('ospite: ' + JSON.stringify(r));
    else { const t0 = await p.locator('#pt-storia-tutti h3').first().textContent(); await p.locator('[data-pt-guest]').nth(4).click(); await p.waitForTimeout(600);
     const r2 = await p.evaluate(() => ({ sel: document.querySelector('[data-pt-guest][aria-pressed="true"]').textContent, sub: document.querySelector('#pt-storia-tutti .pt-sub').textContent.slice(0, 40), h: document.querySelector('#pt-storia-tutti h3').textContent }));
     if (r2.h === t0) pr.push('cambio squadra non cambia il racconto ' + JSON.stringify(r2));
     if (/PC|SE/.test(n) && M === 'chromium') await p.screenshot({ path: '/tmp/claude-0/foto/ospite-sett-' + n.replace(/\W+/g, '') + '-' + sk.replace(/\W+/g, '') + '.png', fullPage: false }); } }
   if (r.lato || await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) pr.push('scorre di lato');
   err.forEach(e => pr.push(e));
   console.log((pr.length ? 'KO ' : 'OK ') + M + ' · ' + n + ' · ' + (ospite ? 'ospite' : 'squadra') + ' · ' + sk + (pr.length ? '\n   ' + pr.join('\n   ') : ''));
   ko += pr.length; await chiudi(); } }
 console.log(M + ': ' + ko + ' problemi'); })();
