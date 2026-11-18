/* Studio transizione B 6.5 (Claude, 18 novembre 2026): misura e registra le varianti nel Lab, niente produzione.
   Uso (server locale sulla radice del registro, porta 8767):
     python3 -m http.server 8767 &
     node prove/v65/prova_transizioni_b.js misura   [--motore chromium|webkit] [--cpu 4]
     node prove/v65/prova_transizioni_b.js video    (fotogrammi a 1/60 s, poi ffmpeg → mp4 a 60 fps)
   Misura: tempi tra fotogrammi (requestAnimationFrame) DURANTE l'effetto, long task, ridisegni e ricalcoli (CDP, solo Chromium),
   stato finale (classi tolte, nessuno strato rimasto, pagina cliccabile). In headless il rendering è software: i numeri servono
   a confrontare le varianti tra loro, non promettono i 60 fps di un telefono vero.
   Video: le animazioni vengono messe in pausa e portate a t = i/60 s una per una, quindi il video a 60 fps mostra fotogramma per
   fotogramma ciò che il browser disegna; NON misura la fluidità (quella è nella misura). */
const pw = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const args = process.argv.slice(2), modo = args[0] || 'misura';
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const MOTORE = opt('motore', 'chromium'), CPU = Number(opt('cpu', '1'));
const OUT = path.resolve(opt('out', 'qa_artifacts/65-transizioni-b'));
const BASE = 'http://127.0.0.1:8767/lab/integrata-62/girrr/index.html?evento=notte-tropicale&evento-intro=trasformazione';
const VARIANTI = (opt('varianti', 'attuale,nuvola,vento,fumo,nuvola-morbida,nuvola-maskpos')).split(',');
const SCHERMI = {
  'iphone-se': { width: 320, height: 568, dpr: 2, mobile: true },
  'iphone': { width: 390, height: 844, dpr: 3, mobile: true },
  'ipad': { width: 1024, height: 768, dpr: 2, mobile: true },
  'pc': { width: 1440, height: 900, dpr: 1, mobile: false },
  'tv': { width: 1920, height: 1080, dpr: 2, mobile: false }
};
const schermiScelti = opt('schermi', 'iphone-se,iphone,ipad,pc,tv').split(',');
fs.mkdirSync(OUT, { recursive: true });

async function apri(browser, s, variante, extra) {
  const ctx = await browser.newContext({ viewport: { width: s.width, height: s.height }, deviceScaleFactor: modo === 'video' ? Math.min(s.dpr, 2) : s.dpr,
    isMobile: MOTORE === 'firefox' ? undefined : s.mobile, hasTouch: s.mobile, reducedMotion: extra && extra.ridotto ? 'reduce' : 'no-preference' });
  const page = await ctx.newPage();
  const errori = [];
  page.on('pageerror', e => errori.push(String(e.message || e)));
  await page.route('**/*', r => {
    const u = r.request().url();
    if (u.startsWith('http://127.0.0.1:8767/') || /fonts\.(googleapis|gstatic)\.com/.test(u)) return r.continue();
    return r.fulfill({ status: 204, body: '' });
  });
  await page.addInitScript(() => {
    window.__gb = { t: [], lt: [] };
    try { new PerformanceObserver(l => l.getEntries().forEach(e => window.__gb.lt.push([e.startTime, e.duration]))).observe({ type: 'longtask', buffered: true }); } catch (e) {}
    const loop = t => { window.__gb.t.push(t); requestAnimationFrame(loop); }; requestAnimationFrame(loop);
  });
  let cdp = null;
  if (MOTORE === 'chromium') { cdp = await ctx.newCDPSession(page); await cdp.send('Performance.enable'); if (CPU > 1) await cdp.send('Emulation.setCPUThrottlingRate', { rate: CPU }); }
  const url = BASE + (variante === 'attuale' ? '' : '&b=' + variante);
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  return { ctx, page, errori, cdp };
}
const metriche = async cdp => cdp ? Object.fromEntries((await cdp.send('Performance.getMetrics')).metrics.map(m => [m.name, m.value])) : null;

async function misura(browser, nomeSchermo, variante, ridotto) {
  const s = SCHERMI[nomeSchermo];
  const { ctx, page, errori, cdp } = await apri(browser, s, variante, { ridotto });
  await page.waitForFunction(() => ['transizione', 'completo'].includes(document.documentElement.getAttribute('data-intro-state')), null, { timeout: 15000 });
  const m0 = await metriche(cdp), t0 = await page.evaluate(() => performance.now());
  await page.waitForFunction(() => document.documentElement.getAttribute('data-intro-state') === 'completo', null, { timeout: 15000 });
  const t1 = await page.evaluate(() => performance.now()), m1 = await metriche(cdp);
  await page.waitForTimeout(400);
  const r = await page.evaluate(([t0, t1]) => {
    const h = document.documentElement;
    const mk = n => (performance.getEntriesByName('girrr-b:' + n)[0] || {}).startTime;
    const a = mk('inizio') || t0, b = mk('fine') || t1;
    const ts = window.__gb.t.filter(t => t >= a && t <= b), dt = ts.slice(1).map((t, i) => t - ts[i]).sort((x, y) => x - y);
    const q = p => dt.length ? +dt[Math.min(dt.length - 1, Math.floor(p * dt.length))].toFixed(1) : null;
    const el = document.elementFromPoint(innerWidth / 2, innerHeight / 2);
    return {
      effettoMs: Math.round(b - a), fotogrammi: dt.length, fpsMedio: dt.length ? +(1000 * dt.length / (ts[ts.length - 1] - ts[0])).toFixed(1) : null,
      frameMs: { mediana: q(.5), p95: q(.95), max: dt.length ? +dt[dt.length - 1].toFixed(1) : null }, sopra25ms: dt.filter(x => x > 25).length,
      longTask: window.__gb.lt.filter(([s, d]) => s + d >= a && s <= b).map(([s, d]) => Math.round(d)),
      stato: h.getAttribute('data-intro-state'), tema: h.getAttribute('data-event-theme'),
      residui: document.querySelectorAll('.girrr-b-fx').length + (h.classList.contains('girrr-b') ? 1 : 0) + (h.classList.contains('nt-intro-trasformazione') ? 1 : 0),
      cliccabile: !!el && !el.closest('.girrr-b-fx'), scorreDiLato: document.documentElement.scrollWidth > innerWidth + 1,
      vt: typeof document.startViewTransition === 'function'
    };
  }, [t0, t1]);
  if (m0 && m1) r.cdp = { ricalcoliStile: m1.RecalcStyleCount - m0.RecalcStyleCount, layout: m1.LayoutCount - m0.LayoutCount,
    stileMs: Math.round((m1.RecalcStyleDuration - m0.RecalcStyleDuration) * 1000), layoutMs: Math.round((m1.LayoutDuration - m0.LayoutDuration) * 1000),
    lavoroThreadMs: Math.round((m1.TaskDuration - m0.TaskDuration) * 1000) };
  r.errori = errori;
  await page.screenshot({ path: path.join(OUT, `finale-${MOTORE}-${variante}-${nomeSchermo}${ridotto ? '-ridotto' : ''}.png`) });
  await ctx.close();
  return r;
}

async function video(browser, nomeSchermo, variante) {
  const s = SCHERMI[nomeSchermo];
  const { ctx, page } = await apri(browser, s, variante, {});
  const dir = path.join(OUT, 'frame', `${variante}-${nomeSchermo}`); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  await page.waitForFunction(() => document.documentElement.getAttribute('data-intro-state') === 'grafica-originale', null, { timeout: 15000 });
  await page.waitForTimeout(250);
  let n = 0;
  const foto = async () => page.screenshot({ path: path.join(dir, String(n++).padStart(4, '0') + '.png'), animations: 'allow' });
  await foto();
  /* aspetta che l'effetto parta (texture pronte, skin accesa nel callback), poi blocca tutte le animazioni */
  await page.waitForFunction(() => document.getAnimations().some(a => a.effect && a.effect.pseudoElement && a.effect.pseudoElement.includes('view-transition')), null, { timeout: 15000, polling: 4 });
  /* solo le animazioni dell'effetto (pseudo-elementi della View Transition e strati girrr-b-fx), non quelle della pagina */
  await page.evaluate(() => { window.__gbAn = () => document.getAnimations().filter(a => a.effect && ((a.effect.pseudoElement || '').includes('view-transition') || (a.effect.target && a.effect.target.classList && a.effect.target.classList.contains('girrr-b-fx')))); });
  const durata = await page.evaluate(() => { const an = window.__gbAn(); an.forEach(a => a.pause());
    return Math.max(...an.map(a => { const t = a.effect.getComputedTiming(); return (t.delay || 0) + t.activeDuration; }).filter(isFinite)); });
  const fermo = Math.round(1.0 * 60); /* un secondo di Home normale prima dell'effetto */
  for (let i = 1; i < fermo; i++) fs.copyFileSync(path.join(dir, '0000.png'), path.join(dir, String(n++).padStart(4, '0') + '.png'));
  const passi = Math.ceil(durata / (1000 / 60));
  for (let i = 0; i <= passi; i++) {
    await page.evaluate(t => window.__gbAn().forEach(a => { try { a.currentTime = Math.min(t, a.effect.getComputedTiming().endTime); } catch (e) {} }), i * 1000 / 60);
    await foto();
  }
  await page.evaluate(() => window.__gbAn().forEach(a => a.play()));
  await page.waitForFunction(() => document.documentElement.getAttribute('data-intro-state') === 'completo', null, { timeout: 15000 });
  await page.waitForTimeout(300); await foto();
  const ultimo = path.join(dir, String(n - 1).padStart(4, '0') + '.png');
  for (let i = 0; i < 60; i++) fs.copyFileSync(ultimo, path.join(dir, String(n++).padStart(4, '0') + '.png'));
  await ctx.close();
  const mp4 = path.join(OUT, `video-${variante}-${nomeSchermo}.mp4`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', '60', '-i', path.join(dir, '%04d.png'), '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2', '-c:v', 'libx264', '-preset', 'slow', '-crf', '24', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-r', '60', mp4]);
  return { mp4, fotogrammi: n, durataEffettoMs: Math.round(durata) };
}

(async () => {
  const browser = await pw[MOTORE].launch();
  const rapporto = { motore: MOTORE, versione: browser.version(), cpu: CPU, modo, data: new Date().toISOString(), risultati: {} };
  for (const sc of schermiScelti) for (const v of VARIANTI) {
    const k = `${v}@${sc}`;
    try {
      rapporto.risultati[k] = modo === 'video' ? await video(browser, sc, v) : await misura(browser, sc, v, false);
      if (modo === 'misura' && sc === 'iphone') rapporto.risultati[k + '@ridotto'] = await misura(browser, sc, v, true);
    } catch (e) { rapporto.risultati[k] = { errore: String(e.message || e).split('\n')[0] }; }
    console.log(k, JSON.stringify(rapporto.risultati[k]));
  }
  await browser.close();
  const f = path.join(OUT, `rapporto-${modo}-${MOTORE}${CPU > 1 ? '-cpu' + CPU : ''}.json`);
  fs.writeFileSync(f, JSON.stringify(rapporto, null, 1));
  console.log('Rapporto:', f);
})();
