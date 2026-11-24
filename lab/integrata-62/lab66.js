/* Lab 6.6 · Scambi simulati (Claude, 24 novembre 2026). Solo nel Lab, dopo lab62.js: niente database vero.
   Fa le veci di sql/scambi-66.sql (scambio_stato, scambio_proponi, scambio_rispondi) con la memoria del browser,
   con le stesse regole: niente conferma da chi registra, vale la prima conferma, rifiuta solo l'altra squadra.
   Alla prima apertura c'è già una richiesta di esempio tra due altre squadre, per provare la conferma come testimone.
   ?scambi=vuoto riparte da zero. */
(function () {
  'use strict';
  var PRIMA = window.fetch, K = 'sc66-lab';
  if (/[?&]scambi=vuoto/.test(location.search)) { try { localStorage.removeItem(K); } catch (e) {} }
  function leggi() { try { return JSON.parse(localStorage.getItem(K) || 'null'); } catch (e) { return null; } }
  function scrivi(x) { try { localStorage.setItem(K, JSON.stringify(x)); } catch (e) {} }
  function esempio(team) {
    var c = window.SC66 && window.SC66.ctx && window.SC66.ctx(); if (!c) return [];
    var al = c.D.teams.filter(function (t) { return t.name !== team; }), a = al[0], b = al[1];
    function primo(t, r) { var x = t.pl.filter(function (p) { var q = c.D.P[p.id]; return q && q.r === r; })[0]; return x && String(x.id); }
    var g = primo(a, 'C'), r = primo(b, 'C'); if (!g || !r) return [];
    var n = {}; [g, r].forEach(function (i) { var p = c.D.P[i]; n[i] = { n: p.n, t: p.t, r: p.r }; });
    return [{ id: 1, da: a.name, a: b.name, dai: [g], ricevi: [r], nomi: n, stato: 'attesa', creato: new Date(Date.now() - 3600e3).toISOString() }];
  }
  function err(m) { return Promise.resolve(new Response(JSON.stringify({ message: m }), { status: 400, headers: { 'Content-Type': 'application/json' } })); }
  function ok(j) { return Promise.resolve(new Response(JSON.stringify(j), { status: 200, headers: { 'Content-Type': 'application/json' } })); }
  window.fetch = function (input, opts) {
    var u = String(typeof input === 'string' ? input : input && input.url || ''), m = /\/rpc\/(scambio_[a-z_]+)/.exec(u);
    if (!m || !/\.supabase\.co\//.test(u)) return PRIMA.apply(this, arguments);
    var a = {}; try { a = JSON.parse(opts && opts.body || '{}'); } catch (e) {}
    var L = leggi(); if (!L) { L = { n: 1, scambi: esempio(a.p_team) }; scrivi(L); }
    var dentro = a.p_code === 'codice-solo-del-test';
    if (m[1] === 'scambio_stato') return ok({ ok: dentro, team: dentro ? a.p_team : null, scambi: L.scambi.slice().reverse() });
    if (!dentro) return err('Codice non valido');
    if (m[1] === 'scambio_proponi') {
      var tutti = (a.p_dai || []).concat(a.p_ricevi || []);
      if (!a.p_dai || !a.p_dai.length || a.p_dai.length !== (a.p_ricevi || []).length) return err('Servono gli stessi giocatori da tutte e due le parti');
      if (L.scambi.some(function (s) { return s.stato === 'attesa' && s.dai.concat(s.ricevi).some(function (i) { return tutti.indexOf(i) >= 0; }); })) return err('Uno di questi giocatori è già in uno scambio in attesa di conferma');
      var id = ++L.n; L.scambi.push({ id: id, da: a.p_team, a: a.p_a, dai: a.p_dai, ricevi: a.p_ricevi, nomi: a.p_nomi || {}, stato: 'attesa', creato: new Date().toISOString() });
      scrivi(L); return ok({ id: id, stato: 'attesa' });
    }
    if (m[1] === 'scambio_rispondi') {
      var s = L.scambi.filter(function (x) { return x.id === a.p_id; })[0];
      if (!s) return err('Scambio non trovato');
      if (s.stato !== 'attesa') return ok({ stato: s.stato, gia: true, conferma: s.conferma, confermato_da: s.confermato_da });
      if (a.p_azione === 'conferma') {
        if (a.p_team === s.da) return err('Lo scambio lo deve confermare un altro allenatore');
        s.stato = 'confermato'; s.conferma = a.p_team === s.a ? 'squadra' : a.p_team === 'Oranje VC' ? 'lega' : 'testimone'; s.confermato_da = a.p_team;
      } else if (a.p_azione === 'rifiuta') { if (a.p_team !== s.a) return err('Può rifiutarlo solo ' + s.a); s.stato = 'rifiutato'; s.confermato_da = a.p_team; }
      else if (a.p_azione === 'annulla') { if (a.p_team !== s.da) return err('Può annullarlo solo ' + s.da); s.stato = 'annullato'; }
      else return err('Azione non valida');
      s.chiuso = new Date().toISOString(); scrivi(L); return ok({ stato: s.stato, conferma: s.conferma });
    }
    return err('Nel Lab questa operazione non viene inviata alla Lega');
  };
})();
