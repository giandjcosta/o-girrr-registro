/* Spogliatoio · Cerca un giocatore (Claude, 9 novembre 2026, richiesta di Gianluca: «lo metterei sempre in Spogliatoio»).
   Va nella radice del sito (/o-fant-a-girrr/cerca.js), incluso dallo Spogliatoio (index.html).
   Casella sopra le schede: scrivi un nome e vedi chi lo ha in rosa, stato per la prossima giornata, infortunio,
   voti e fantavoti, statistiche della stagione, Borsino e Moviola. Usa i colori della grafica scelta (variabili del tema). */
(function () {
  if (window.__girrrCerca) return; window.__girrrCerca = 1;
  var io = document.currentScript, ROOT = new URL('./', io && io.src ? io.src : location.href).href;
  var RUOLI = { P: 'Portiere', D: 'Difensore', C: 'Centrocampista', A: 'Attaccante' };
  var PROSSIMA = { T: 'Titolare', B: 'Titolare, ballottaggio', R: 'Riserva, ballottaggio', D: 'In dubbio', P: 'Panchina', I: 'Fuori' };
  var GIOCATA = { T: 'Titolare', S: 'Subentrato', P: 'In panchina', I: 'Fuori' };
  var D = null, BOR = {}, MOV = {}, ELENCO = [], carica = null, scelto = -1;

  function E(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function piano(s) { return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
  function num(x, d) { return x == null || isNaN(x) ? '–' : Number(x).toFixed(d == null ? 2 : d).replace('.', ','); }
  function chi() { try { var o = JSON.parse(localStorage.getItem('fg') || '{}'); return o && o.team ? o.team : null; } catch (e) { return null; } }

  function dati() {
    if (carica) return carica;
    var j = function (u) { return fetch(ROOT + u, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
    carica = Promise.all([j('data.json'), j('girrr/dati/borsino.json'), j('girrr/dati/moviola.json')]).then(function (x) {
      D = x[0] || {};
      var rosa = {};
      (D.teams || []).forEach(function (t) { (t.pl || []).forEach(function (p) { rosa[p.id] = { team: t.name, c: p.c }; }); });
      var P = D.P || {};
      ELENCO = Object.keys(P).map(function (id) {
        var p = P[id]; return { id: id, n: p.n, t: p.t, r: p.r, q: p.q, chiave: piano(p.n), rosa: rosa[id] || null };
      }).sort(function (a, b) { return a.n.localeCompare(b.n, 'it'); });
      var b = x[1] || {};
      Object.keys(b.squadre || {}).forEach(function (sq) { (b.squadre[sq] || []).forEach(function (g) { BOR[g.id] = g; }); });
      var m = x[2] || {};
      Object.keys(m.giornate || {}).forEach(function (g) {
        var gg = m.giornate[g];
        (gg.episodi || []).concat(gg.automatici || []).forEach(function (e) { if (e && e.id) (MOV[e.id] = MOV[e.id] || []).push(+g); });
      });
    });
    return carica;
  }

  function stile() {
    var s = document.createElement('style');
    s.textContent =
      '.gc{position:relative;margin:10px 0 12px}' +
      '.gc-in{display:flex;align-items:center;gap:8px;background:linear-gradient(160deg,var(--card,#22135a),var(--card2,#170c40));border:1px solid var(--line,#4a2bd6);border-radius:var(--rad,16px);padding:0 12px;min-height:46px}' +
      '.gc-in svg{flex:none;opacity:.75}.gc-in input{flex:1;min-width:0;border:0;background:transparent;color:var(--ink,#f3efff);font:inherit;font-weight:700;font-size:16px;padding:11px 0;outline:0}' +
      '.gc-in input::placeholder{color:var(--mute,#cdc6f0);opacity:.85;font-weight:600}.gc-in:focus-within{border-color:var(--hl,#ffc63a)}' +
      '.gc-x{flex:none;border:0;background:none;color:var(--mute,#cdc6f0);font-size:18px;cursor:pointer;padding:6px;line-height:1}' +
      '.gc-lista{position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:60;background:var(--card2,#170c40);border:1px solid var(--line,#4a2bd6);border-radius:var(--rad,16px);overflow:hidden;box-shadow:0 14px 30px rgba(0,0,0,.35);opacity:0;transform:translateY(-4px);transition:opacity .2s,transform .2s;pointer-events:none}' +
      '.gc-lista.su{opacity:1;transform:none;pointer-events:auto}' +
      '.gc-lista button{display:flex;align-items:center;gap:10px;width:100%;text-align:left;border:0;background:none;color:var(--ink,#f3efff);font:inherit;padding:10px 12px;cursor:pointer}' +
      '.gc-lista button+button{border-top:1px solid rgba(127,127,127,.2)}.gc-lista button[aria-selected=true],.gc-lista button:hover{background:rgba(127,127,127,.16)}' +
      '.gc-r{flex:none;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:12px;background:var(--accA,#b3246f);color:var(--acc-ink,#fff)}' +
      '.gc-lista b{display:block;font-weight:800}.gc-lista small{display:block;color:var(--mute,#cdc6f0);font-size:12px;font-weight:600}.gc-lista .gc-mio b{color:var(--hl-name,var(--hl,#ffc63a))}' +
      '.gc-vuoto{padding:12px;color:var(--mute,#cdc6f0);font-size:13px}' +
      '.gc-card{margin-top:10px;opacity:0;transform:translateY(6px);transition:opacity .3s,transform .3s}.gc-card.su{opacity:1;transform:none}' +
      '.gc-card h3{display:flex;align-items:flex-start;gap:10px;margin:0 0 4px;font-size:20px;line-height:1.15}.gc-card h3 span{flex:1}' +
      '.gc-card .gc-sub{color:var(--mute,#cdc6f0);font-weight:700;font-size:13px}' +
      '.gc-tags{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}.gc-tag{font-weight:800;font-size:12px;padding:4px 10px;border-radius:999px;background:rgba(127,127,127,.18)}' +
      '.gc-tag.ok{background:var(--ok,#9cf24a);color:#10220a}.gc-tag.no{background:var(--bad,#ff4f6d);color:#fff}.gc-tag.mid{background:var(--warn,#ffc63a);color:#2b1d00}.gc-tag.mio{background:var(--hl,#ffc63a);color:var(--hl-ink,#2b1d00)}' +
      '.gc-sez{margin-top:12px}.gc-sez h4{margin:0 0 6px;font-size:11px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;color:var(--mute,#cdc6f0)}' +
      '.gc-num{display:grid;grid-template-columns:repeat(auto-fit,minmax(78px,1fr));gap:6px}.gc-num div{background:rgba(127,127,127,.12);border-radius:10px;padding:7px 8px}' +
      '.gc-num b{display:block;font-size:18px;font-weight:900;font-variant-numeric:tabular-nums}.gc-num small{font-size:11px;font-weight:700;color:var(--mute,#cdc6f0)}' +
      '.gc-voti{display:grid;gap:4px}.gc-voti div{display:grid;grid-template-columns:34px 1fr;column-gap:8px;align-items:baseline;font-size:13px;padding:5px 0;border-top:1px solid rgba(127,127,127,.18)}.gc-voti small{grid-column:2}.gc-voti small:empty{display:none}' +
      '.gc-voti div:first-child{border-top:0}.gc-voti b{font-variant-numeric:tabular-nums}.gc-voti small{color:var(--mute,#cdc6f0)}' +
      '.gc-card p{margin:4px 0 0;font-size:13px;line-height:1.45}' +
      '@media (prefers-reduced-motion: reduce){.gc-lista,.gc-card{transition:opacity .15s linear;transform:none!important}}';
    document.head.appendChild(s);
  }

  function risultati(q) {
    var p = piano(q).trim(); if (p.length < 2) return [];
    var inizio = [], dentro = [];
    ELENCO.forEach(function (x) { var i = x.chiave.indexOf(p); if (i === 0 || x.chiave.indexOf(' ' + p) > 0) inizio.push(x); else if (i > 0) dentro.push(x); });
    return inizio.concat(dentro).slice(0, 8);
  }

  function scheda(x) {
    var id = x.id, mio = chi(), pr = D.st && D.st[id] ? D.st[id].s : null;
    var inf = (D.inj || []).filter(function (j) { return String(j.id) === String(id); })[0];
    var ps = (D.ps || {})[id], v = (D.votes || {})[id] || {}, lg = (D.log || {})[id] || {}, b = BOR[id], mv = MOV[id] || [];
    var h = '<h3><span>' + E(x.n) + '</span><button type="button" class="gc-x" aria-label="Chiudi la scheda">✕</button></h3>' +
      '<div class="gc-sub">' + E(x.t) + ' · ' + (RUOLI[x.r] || x.r) + (x.q != null ? ' · Quotazione ' + E(x.q) : '') + '</div><div class="gc-tags">';
    if (x.rosa) h += '<span class="gc-tag' + (x.rosa.team === mio ? ' mio' : '') + '">' + E(x.rosa.team) + ' · pagato ' + E(x.rosa.c) + ' fantacrediti</span>';
    else h += '<span class="gc-tag">Svincolato</span>';
    if (pr) h += '<span class="gc-tag ' + (pr === 'T' ? 'ok' : pr === 'I' ? 'no' : pr === 'D' || pr === 'B' || pr === 'R' ? 'mid' : '') + '">' + (D.nx ? D.nx + 'ª di Serie A: ' : 'Prossima: ') + E(PROSSIMA[pr] || pr) + '</span>';
    h += '</div>';
    if (inf) h += '<p><b>Infortunio:</b> ' + E(inf.w || '') + (inf.b ? ' · Rientro previsto: ' + E(inf.b) : '') + '</p>';
    if (ps) h += '<div class="gc-sez"><h4>Stagione</h4><div class="gc-num">' +
      '<div><b>' + E(ps.pg) + '</b><small>Presenze</small></div><div><b>' + num(ps.mv) + '</b><small>Media voto</small></div>' +
      '<div><b>' + num(ps.fmv) + '</b><small>Fantamedia</small></div><div><b>' + E(ps.g || 0) + '</b><small>Gol</small></div><div><b>' + E(ps.as || 0) + '</b><small>Assist</small></div></div></div>';
    var giornate = Object.keys(Object.assign({}, v, lg)).map(Number).sort(function (a, b) { return b - a; }).slice(0, 5);
    if (giornate.length) {
      h += '<div class="gc-sez"><h4>Ultime giornate di Serie A</h4><div class="gc-voti">' + giornate.map(function (g) {
        var r = v[g];
        if (r) return '<div><b>' + g + 'ª</b><span>Voto <b>' + num(r.v, 1) + '</b> · Fantavoto <b>' + num(r.f, 1) + '</b></span><small>' + E((r.b || []).join(', ')) + '</small></div>';
        return '<div><b>' + g + 'ª</b><span>' + E(GIOCATA[lg[g]] || 'Senza voto') + '</span><small></small></div>';
      }).join('') + '</div></div>';
    }
    if (b) h += '<div class="gc-sez"><h4>Borsino</h4><p>Valore <b>' + num(b.valore, 1) + '</b>' + (b.variazione != null ? ' (' + (b.variazione >= 0 ? '+' : '') + num(b.variazione, 1) + ' nelle ultime giornate)' : '') + (b.consiglio ? '<br>' + E(b.consiglio) : '') + '</p></div>';
    if (mv.length) h += '<div class="gc-sez"><h4>Moviola</h4><p>' + (mv.length === 1 ? '1 episodio' : mv.length + ' episodi') + ' (giornate ' + mv.sort(function (a, b) { return a - b; }).join(', ') + ').</p></div>';
    return h;
  }

  function monta() {
    var dopo = document.querySelector('details.skin-menu') || document.getElementById('tabs');
    if (!dopo || document.querySelector('.gc')) return;
    stile();
    var w = document.createElement('div'); w.className = 'gc';
    w.innerHTML = '<label class="gc-in"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input type="search" placeholder="Cerca un giocatore" autocomplete="off" enterkeyhint="search" aria-label="Cerca un giocatore" role="combobox" aria-expanded="false" aria-controls="gc-lista">' +
      '<button type="button" class="gc-x" aria-label="Cancella" hidden>✕</button></label><div class="gc-lista" id="gc-lista" role="listbox"></div><div class="gc-card card" hidden></div>';
    dopo.parentNode.insertBefore(w, dopo.nextSibling);
    var inp = w.querySelector('input'), lista = w.querySelector('.gc-lista'), card = w.querySelector('.gc-card'), x = w.querySelector('.gc-in .gc-x'), trovati = [];
    function apri(su) { lista.classList.toggle('su', su); inp.setAttribute('aria-expanded', String(su)); }
    function mostra() {
      var q = inp.value; x.hidden = !q;
      if (piano(q).trim().length < 2) { apri(false); return; }
      dati().then(function () {
        trovati = risultati(inp.value); scelto = -1; var mio = chi();
        lista.innerHTML = trovati.length ? trovati.map(function (p, i) {
          return '<button type="button" role="option" data-i="' + i + '" aria-selected="false"' + (p.rosa && p.rosa.team === mio ? ' class="gc-mio"' : '') + '><span class="gc-r">' + E(p.r) + '</span><span><b>' + E(p.n) + '</b><small>' + E(p.t) + ' · ' + (p.rosa ? E(p.rosa.team) : 'Svincolato') + '</small></span></button>';
        }).join('') : '<div class="gc-vuoto">Nessun giocatore con questo nome.</div>';
        Array.prototype.forEach.call(lista.querySelectorAll('button'), function (b) { b.onmousedown = function (e) { e.preventDefault(); }; b.onclick = function () { scegli(+b.dataset.i); }; });
        apri(true);
      });
    }
    function scegli(i) {
      var p = trovati[i]; if (!p) return;
      apri(false); inp.blur();
      card.classList.remove('su'); card.innerHTML = scheda(p); card.hidden = false;
      card.querySelector('.gc-x').onclick = function () { card.classList.remove('su'); setTimeout(function () { card.hidden = true; }, 300); };
      requestAnimationFrame(function () { requestAnimationFrame(function () { card.classList.add('su'); }); });
    }
    inp.addEventListener('focus', function () { dati(); if (inp.value) mostra(); });
    inp.addEventListener('input', mostra);
    inp.addEventListener('blur', function () { setTimeout(function () { apri(false); }, 150); });
    inp.addEventListener('keydown', function (e) {
      var bs = lista.querySelectorAll('button');
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault(); if (!bs.length) return;
        scelto = (scelto + (e.key === 'ArrowDown' ? 1 : -1) + bs.length) % bs.length;
        Array.prototype.forEach.call(bs, function (b, i) { b.setAttribute('aria-selected', String(i === scelto)); });
      } else if (e.key === 'Enter') { e.preventDefault(); scegli(scelto >= 0 ? scelto : 0); }
      else if (e.key === 'Escape') { apri(false); }
    });
    x.onclick = function () { inp.value = ''; x.hidden = true; apri(false); inp.focus(); };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', monta); else monta();
})();
