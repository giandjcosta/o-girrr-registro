/* Ingresso unico O Girrr — Grok
 * Un solo posto: entra con codice squadra oppure continua come ospite.
 * Esci: toglie il codice, le pagine pubbliche restano usabili.
 * Usa localStorage.fg (stesso di Spogliatoio / Curva / Totogirrr).
 */
(function () {
  function hsh(s) {
    var h = 2166136261, i;
    for (i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return (h >>> 0).toString(36);
  }
  function loadFg() {
    try {
      return JSON.parse(localStorage.getItem('fg') || '{}') || {};
    } catch (e) {
      return {};
    }
  }
  function saveFg(o) {
    try {
      localStorage.setItem('fg', JSON.stringify(o));
    } catch (e) {}
  }
  function isGuest() {
    try {
      return sessionStorage.getItem('ospite') === '1';
    } catch (e) {
      return false;
    }
  }
  function setGuest(on) {
    try {
      if (on) sessionStorage.setItem('ospite', '1');
      else sessionStorage.removeItem('ospite');
    } catch (e) {}
  }

  function resolveTeam(d, fg) {
    if (!d || !d.lock || !fg || !fg.team || !fg.code) return null;
    var k = hsh(fg.team + '|' + String(fg.code).toUpperCase());
    if (d.lock[fg.team] === k) return fg.team;
    return null;
  }

  function mount(host, d) {
    if (!host) return;
    var fg = loadFg();
    var team = resolveTeam(d, fg);
    var guest = isGuest();

    host.innerHTML = '';
    host.className = 'auth-box';

    if (team) {
      host.innerHTML =
        '<div class="auth-ok">' +
        '<span>Sei <b>' +
        team.replace(/[<>&]/g, '') +
        '</b> · il telefono ricorda il codice</span>' +
        '<button type="button" class="auth-out">Esci</button>' +
        '</div>';
      host.querySelector('.auth-out').onclick = function () {
        var o = loadFg();
        delete o.code;
        delete o.team;
        saveFg(o);
        setGuest(false);
        mount(host, d);
      };
      return;
    }

    if (guest) {
      host.innerHTML =
        '<div class="auth-ok guest">' +
        '<span>Modalità <b>ospite</b> · sola lettura (niente Spogliatoio / Totogirrr)</span>' +
        '<button type="button" class="auth-out">Esci dall\'ospite</button>' +
        '</div>';
      host.querySelector('.auth-out').onclick = function () {
        setGuest(false);
        mount(host, d);
      };
      return;
    }

    var teams = (d && d.teams) || [];
    var opts = teams
      .map(function (t) {
        return '<option value="' + String(t.name).replace(/"/g, '') + '">' + String(t.name).replace(/[<>&]/g, '') + '</option>';
      })
      .join('');

    host.innerHTML =
      '<div class="auth-gate">' +
      '<div class="auth-t">Un solo ingresso</div>' +
      '<p class="auth-p">Entra con il codice della tua squadra, oppure continua come ospite (solo lettura).</p>' +
      '<div class="auth-row">' +
      '<select id="auth-team" aria-label="Squadra">' +
      '<option value="">Squadra…</option>' +
      opts +
      '</select>' +
      '<input id="auth-code" type="text" autocomplete="off" spellcheck="false" placeholder="Codice" maxlength="24" aria-label="Codice">' +
      '<button type="button" class="auth-in" id="auth-go">Entra</button>' +
      '</div>' +
      '<button type="button" class="auth-guest" id="auth-guest">Continua come ospite</button>' +
      '<div class="auth-err" id="auth-err" hidden>Codice non valido per questa squadra.</div>' +
      '</div>';

    host.querySelector('#auth-go').onclick = function () {
      var sel = host.querySelector('#auth-team');
      var inp = host.querySelector('#auth-code');
      var err = host.querySelector('#auth-err');
      var t = (sel.value || '').trim();
      var c = (inp.value || '').trim().toUpperCase();
      err.hidden = true;
      if (!t || !c) {
        err.textContent = 'Scegli la squadra e inserisci il codice.';
        err.hidden = false;
        return;
      }
      var o = loadFg();
      o.team = t;
      o.code = c;
      if (resolveTeam(d, o)) {
        saveFg(o);
        setGuest(false);
        mount(host, d);
      } else {
        err.textContent = 'Codice non valido per questa squadra.';
        err.hidden = false;
      }
    };
    host.querySelector('#auth-guest').onclick = function () {
      setGuest(true);
      mount(host, d);
    };
    host.querySelector('#auth-code').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') host.querySelector('#auth-go').click();
    });
  }

  function injectStyles() {
    if (document.getElementById('auth-ingresso-css')) return;
    var st = document.createElement('style');
    st.id = 'auth-ingresso-css';
    st.textContent =
      '.auth-box{margin:0 0 18px;border:1px solid rgba(255,255,255,.12);border-radius:16px;background:rgba(0,0,0,.22);padding:14px 16px}' +
      '.auth-t{font:900 11px/1 Inter,system-ui,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--hi,#ffd166);margin-bottom:6px}' +
      '.auth-p{font:600 13px/1.4 Inter,system-ui,sans-serif;color:var(--chiaro,#ffe2e6);margin:0 0 12px;opacity:.92}' +
      '.auth-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}' +
      '.auth-row select,.auth-row input{flex:1;min-width:120px;border:1px solid rgba(255,255,255,.18);border-radius:10px;background:rgba(0,0,0,.35);color:#fff;font:700 14px Inter,system-ui,sans-serif;padding:10px 12px}' +
      '.auth-row input{text-transform:uppercase;letter-spacing:.06em}' +
      '.auth-in{border:0;border-radius:10px;background:var(--acc,#d62839);color:#fff;font:900 12px Inter,system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:11px 16px;cursor:pointer}' +
      '.auth-guest{display:block;margin-top:10px;border:0;background:none;color:var(--chiaro,#ffe2e6);font:800 12px Inter,system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;text-decoration:underline;cursor:pointer;opacity:.85}' +
      '.auth-err{margin-top:10px;color:#ffb4b4;font:700 13px Inter,system-ui,sans-serif}' +
      '.auth-ok{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;font:600 14px Inter,system-ui,sans-serif;color:var(--chiaro,#ffe2e6)}' +
      '.auth-ok b{font-weight:900;color:#fff}' +
      '.auth-ok.guest{border-left:3px solid var(--hi,#ffd166);padding-left:10px}' +
      '.auth-out{border:0;border-radius:999px;background:rgba(255,255,255,.14);color:#fff;font:800 12px Inter,system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;padding:8px 14px;cursor:pointer}';
    document.head.appendChild(st);
  }

  function boot() {
    var host = document.getElementById('auth-ingresso');
    if (!host) return;
    injectStyles();
    var dataUrl = host.getAttribute('data-json') || '../data.json';
    fetch(dataUrl, { cache: 'no-store' })
      .then(function (r) {
        return r.json();
      })
      .then(function (d) {
        if (window.CVPUB) d = CVPUB(d);
        mount(host, d);
      })
      .catch(function () {
        host.innerHTML =
          '<div class="auth-gate"><p class="auth-p">Non riesco a caricare le squadre. Riprova più tardi.</p></div>';
        injectStyles();
      });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
