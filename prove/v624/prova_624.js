// 6.2.4 · Prova delle correzioni (Claude, 17 novembre 2026). Uso: node prove/v624/prova_624.js URL_DEL_LAB_INTEGRATA
//   per esempio http://localhost:8767/lab/integrata-62/  (Lab rigenerato con rilascio/r624/lab.py: serve la squadra di prova)
// 1. «‹ O Girrr» senza fondo: mouse sopra (PC) e tocco (telefono) su Versioni, Notifiche, Albo, Totogirrr, Carriera.
// 2. Totogirrr: toccando una scheda non compare la pillola «fantasma» che scivola; la scheda toccata è tutta in vista.
// 3. Spogliatoio › Calendario da allenatore, simulando Safari (senza ancoraggio dello scorrimento): la freccia resta ferma
//    e la giornata nuova entra in dissolvenza.
// 4. Spogliatoio da allenatore: tutte le schede si aprono, niente scorrimento laterale, nessun errore.
const { chromium, devices } = require('playwright');
(async () => {
  const B = process.argv[2]; const b = await chromium.launch(); let ko = 0;
  const no = (m) => { ko++; console.log('KO ' + m); };
  const SCHERMI = [['iPhone SE 320', { ...devices['iPhone SE'], viewport: { width: 320, height: 568 } }], ['Pixel 7', devices['Pixel 7']], ['PC 1280', { viewport: { width: 1280, height: 800 } }]];
  for (const [nome, opz] of SCHERMI) for (const g of ['girrr', 'stadio/girrr']) {
    const gr = g === 'girrr' ? 'Lega' : 'Stadio', tel = !!opz.hasTouch;
    const ctx = await b.newContext(opz);
    await ctx.addInitScript(s => { try { localStorage.setItem('girrr_offline_pronta', '1'); document.cookie = 'gskin=' + s + '; path=/'; } catch (e) {} }, g === 'girrr' ? 'girrr' : 'stadio');
    const p = await ctx.newPage(); const err = []; p.on('pageerror', e => { if (!/ViewTransition/.test(e.message)) err.push(e.message.slice(0, 90)); });
    // 1. alone
    for (const u of ['versioni.html', 'notifiche.html', 'albo.html', 'totogirrr.html?demo', 'app.html#carriera']) {
      await p.goto(B + g + '/' + u, { waitUntil: 'networkidle' }); await p.waitForTimeout(700);
      const sel = await p.evaluate(() => { const a = [...document.querySelectorAll('.v55-return,.back,.oback')].find(x => /O Girrr/i.test(x.textContent) && x.getBoundingClientRect().width); if (!a) return null; a.id = a.id || 'prova-indietro'; return '#' + a.id; });
      if (!sel) { no(`${nome} ${gr} ${u}: nessun «‹ O Girrr»`); continue; }
      const bb = await p.locator(sel).boundingBox();
      if (tel) { await p.evaluate(s => document.querySelector(s).addEventListener('click', e => e.preventDefault(), { once: true }), sel); await p.touchscreen.tap(bb.x + bb.width / 2, bb.y + bb.height / 2); }
      else await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2);
      await p.waitForTimeout(250);
      const c = await p.evaluate(s => { const x = getComputedStyle(document.querySelector(s)); return [x.backgroundColor, x.boxShadow, x.outlineStyle]; }, sel);
      if (c[0] !== 'rgba(0, 0, 0, 0)' || c[1] !== 'none' || (c[2] !== 'none' && c[2] !== '')) no(`${nome} ${gr} ${u}: «‹ O Girrr» con fondo o contorno ${c.join(' / ')}`);
    }
    // 2. Totogirrr senza pillola che scivola
    await p.goto(B + g + '/totogirrr.html?demo', { waitUntil: 'networkidle' }); await p.waitForTimeout(800);
    const t = await p.evaluate(() => { const n = document.querySelector('nav'), e = n.getBoundingClientRect(); const bs = [...n.querySelectorAll('button')]; const bb = bs.find(x => !x.classList.contains('on') && x.getBoundingClientRect().left < e.right - 12) || bs[1]; const r = bb.getBoundingClientRect(); return { x: Math.min(r.left + r.width / 2, e.right - 8), y: r.top + r.height / 2, t: bb.dataset.tab }; });
    await p.evaluate(() => { window.__fantasma = 0; new MutationObserver(m => m.forEach(r => r.addedNodes.forEach(n => { if (n.tagName === 'I' && n.getAttribute('aria-hidden') === 'true') window.__fantasma++; }))).observe(document.querySelector('nav'), { childList: true, subtree: true }); });
    if (tel) await p.touchscreen.tap(t.x, t.y); else await p.mouse.click(t.x, t.y);
    await p.waitForTimeout(500);
    const tt = await p.evaluate(tab => { const n = document.querySelector('nav'), b = n.querySelector('button.on'), r = b.getBoundingClientRect(), e = n.getBoundingClientRect(); return { f: window.__fantasma, on: b.dataset.tab === tab, vis: r.left >= e.left - 1 && r.right <= e.right + 1, tr: getComputedStyle(b).transitionProperty }; }, t.t);
    if (tt.f) no(`${nome} ${gr} Totogirrr: pillola fantasma che scivola`);
    if (!tt.on || !tt.vis) no(`${nome} ${gr} Totogirrr: scheda toccata non attiva o tagliata`);
    if (!/background-color/.test(tt.tr)) no(`${nome} ${gr} Totogirrr: manca la dissolvenza del colore`);
    // 3 e 4. Spogliatoio da allenatore
    await ctx.addInitScript(() => { document.addEventListener('DOMContentLoaded', () => { const s = document.createElement('style'); s.textContent = '*{overflow-anchor:none!important}'; document.head.appendChild(s); }); });
    await p.goto(B + 'index.html?squadra=Oranje%20VC', { waitUntil: 'networkidle' }); await p.waitForTimeout(1000);
    const tabs = await p.evaluate(() => [...document.querySelectorAll('#tabs button')].filter(x => !x.hidden).map(x => x.dataset.t));
    if (tabs.length < 10) no(`${nome} ${gr} Spogliatoio: solo ${tabs.length} schede (squadra di prova non entrata?)`);
    for (const k of tabs) { await p.evaluate(k => document.querySelector(`#tabs button[data-t="${k}"]`).click(), k); await p.waitForTimeout(500);
      const r = await p.evaluate(() => ({ lat: document.documentElement.scrollWidth - innerWidth, len: document.getElementById('app').textContent.length }));
      if (r.lat > 0 || r.len < 40) no(`${nome} ${gr} Spogliatoio ${k}: laterale ${r.lat}, testo ${r.len}`); }
    await p.evaluate(() => document.querySelector('#tabs button[data-t="lega"]').click()); await p.waitForTimeout(600);
    await p.evaluate(() => { const c = document.querySelector('.calnav'); scrollTo(0, c.getBoundingClientRect().top + scrollY - 200); }); await p.waitForTimeout(400);
    for (const dir of ['1', '1', '-1']) {
      const pre = await p.evaluate(() => Math.round(document.querySelector('.calnav').getBoundingClientRect().top));
      await p.evaluate(() => { window.__o = []; const f = () => { const el = document.querySelector('.calnav'); const n = el && el.nextElementSibling; window.__o.push(n ? +getComputedStyle(n).opacity : 1); if (window.__o.length < 30) requestAnimationFrame(f); }; requestAnimationFrame(f); });
      const bb = await p.locator(`.calnav [data-cal="${dir}"]`).boundingBox();
      if (tel) await p.touchscreen.tap(bb.x + bb.width / 2, bb.y + bb.height / 2); else await p.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2);
      await p.waitForTimeout(600);
      const post = await p.evaluate(() => Math.round(document.querySelector('.calnav').getBoundingClientRect().top)); const op = Math.min(...await p.evaluate(() => window.__o));
      if (Math.abs(post - pre) > 2) no(`${nome} ${gr} Calendario: la freccia si è spostata da ${pre} a ${post}`);
      if (op > 0.5) no(`${nome} ${gr} Calendario: nessuna dissolvenza (opacità minima ${op})`);
    }
    if (err.length) no(`${nome} ${gr}: errori ${err.join(' | ')}`);
    console.log(`fatto ${nome} · ${gr}`);
    await ctx.close();
  }
  await b.close(); console.log(ko ? ko + ' prove non superate' : 'Tutte le prove superate'); process.exit(ko ? 1 : 0);
})();
