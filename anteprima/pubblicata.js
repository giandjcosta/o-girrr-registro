/* Cornice dell'ultima versione pubblicata, distinta dai prototipi del Laboratorio. */
(function () {
  'use strict';
  var base = new URL('pubblicata/', document.currentScript.src);
  var frame = document.getElementById('f'), toggle = document.getElementById('tg');
  function mode(u) { return /\/stadio\/girrr\//.test(u.pathname) ? 'n' : 'a'; }
  function inside(u) { return u.origin === base.origin && u.pathname.startsWith(base.pathname); }
  function convert(u, m) {
    if (!inside(u)) u = new URL('girrr/index.html', base);
    var rel = u.pathname.slice(base.pathname.length).replace(/^stadio\//, '');
    if (!rel.startsWith('girrr/')) return u;
    u.pathname = base.pathname + (m === 'n' ? 'stadio/' : '') + rel;
    return u;
  }
  function mark(m) {
    toggle.setAttribute('aria-checked', String(m === 'n'));
    document.getElementById('la').className = m === 'a' ? 'on' : '';
    document.getElementById('ln').className = m === 'n' ? 'on' : '';
    // Anche grafica.js e transizioni.js della copia devono conoscere la scelta.
    try { localStorage.setItem('orr_gv', m); } catch (e) {}
  }
  function current() { try { return new URL(frame.contentWindow.location.href); } catch (e) { return new URL('girrr/index.html', base); } }
  function load(u, m) { mark(m); frame.src = convert(u, m).href; }
  toggle.addEventListener('click', function () { load(current(), toggle.getAttribute('aria-checked') === 'true' ? 'a' : 'n'); });
  frame.addEventListener('load', function () {
    var u = current();
    if (inside(u)) { mark(mode(u)); try { localStorage.setItem('registro-anteprima-online', u.href); } catch (e) {} }
  });
  var first = new URL('girrr/index.html', base), m = 'a';
  try { var saved = new URL(localStorage.getItem('registro-anteprima-online')); if (inside(saved)) first = saved; m = localStorage.getItem('orr_gv') === 'n' ? 'n' : 'a'; } catch (e) {}
  load(first, m);
})();
