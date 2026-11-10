const { chromium, devices } = require('playwright');
(async () => { const B = 'https://giandjcosta.github.io/o-fant-a-girrr/', LAB = process.argv[2], D = process.argv[3];
 const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
 for (const [n, d] of [['iPhone', devices['iPhone 15 Pro']], ['Android', devices['Pixel 7']]]) for (const sk of ['girrr', 'stadio/girrr']) for (const esito of ['ok', 'errore']) {
  const c = await b.newContext(d); await c.addInitScript(() => { try { localStorage.setItem('fg', JSON.stringify({ team: 'Grodah', code: 'PROVA' })) } catch (e) {} });
  if (LAB) await c.route(/\/curva\.html/, r => r.fulfill({ path: LAB + '/' + sk + '/curva.html', contentType: 'text/html' }));
  await c.route(/rpc\/curva_feed/, async r => { const res = await r.fetch(); const j = await res.json(); j.ok = true; j.mine = [...messi].map(x => ({ k: x.split('|')[0], kind: x.split('|')[1] })); await r.fulfill({ response: res, json: j }); });
  const messi = new Set();
  await c.route(/rpc\/curva_reagisci/, async r => { const q = r.request().postDataJSON(); if (esito === 'ok') { const x = q.p_k + '|' + q.p_kind; messi.has(x) ? messi.delete(x) : messi.add(x); } await new Promise(x => setTimeout(x, 1500)); esito === 'ok' ? r.fulfill({ status: 200, body: 'null', contentType: 'application/json' }) : r.fulfill({ status: 400, json: { message: 'Codice non valido' } }); });
  function hshF(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return (h>>>0).toString(36)}
  await c.route(/data\.json/, async r => { const res = await r.fetch(); const j = await res.json(); if (j.lock) j.lock['Grodah'] = hshF('Grodah|PROVA'); await r.fulfill({ response: res, json: j }); });
  const p = await c.newPage(); const errs = []; p.on('pageerror', e => { if (!/ViewTransition/.test(e.message)) errs.push(e.message) });
  await p.goto(B + sk + '/curva.html'); await p.waitForTimeout(5000);
  const a = await p.$('article.post[data-k="a48"]'); await a.scrollIntoViewIfNeeded();
  const r = [];
  for (const [cl, nome] of [['app', 'cuore'], ['ril', 'rilancio']]) {
   await p.tap('article.post[data-k="a48"] .acts .' + cl); await p.waitForTimeout(150);
   const s = await p.$eval('article.post[data-k="a48"] .acts .' + cl, x => [x.classList.contains('on'), getComputedStyle(x).color, getComputedStyle(x.querySelector('svg')).fill].join(' '));
   await p.waitForTimeout(2500);
   const f = await p.$eval('article.post[data-k="a48"] .acts .' + cl, x => x.classList.contains('on'));
   r.push(nome + ': subito ' + s + ' → dopo il database ' + f);
  }
  if (D && esito === 'ok' && sk === 'girrr') await (await p.$('article.post[data-k="a48"] .acts')).screenshot({ path: D + '/tocco-' + n + '.png' });
  console.log(n, sk, esito, errs.length ? 'ERRORI ' + errs : '', '| ' + r.join(' | ')); await c.close(); }
 await b.close(); })();
