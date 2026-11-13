/* Cornice dell'ultima versione pubblicata, distinta dai prototipi del Laboratorio. */
(function () {
  'use strict';
  var base = new URL('pubblicata/', document.currentScript.src);
  var frame = document.getElementById('f'), toggle = document.getElementById('tg'), pending, recovered = false;
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
    document.dispatchEvent(new Event('registro:grafica'));
  }
  function current() { try { return new URL(frame.contentWindow.location.href); } catch (e) { return new URL('girrr/index.html', base); } }
  function recover() {
    try { localStorage.removeItem('registro-anteprima-online'); } catch (e) {}
    document.documentElement.dataset.anteprimaRipristinata = 'true';
    if (recovered) return; // Un errore anche sulla Home non deve creare un ciclo di richieste.
    recovered = true;
    load(new URL('girrr/index.html', base), toggle.getAttribute('aria-checked') === 'true' ? 'n' : 'a');
  }
  function load(u, m) {
    mark(m); clearTimeout(pending);
    // La prima pagina parte subito, prima dell’evento load della cornice.
    if (!frame.getAttribute('src')) { frame.src = convert(u, m).href; return; }
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    frame.style.transition = reduced ? 'none' : '';
    if (!reduced) frame.classList.add('out');
    pending = setTimeout(function () { frame.src = convert(u, m).href; }, reduced ? 0 : 160);
  }
  toggle.addEventListener('click', function () { load(current(), toggle.getAttribute('aria-checked') === 'true' ? 'a' : 'n'); });
  window.addEventListener('message', function (event) {
    if (event.origin !== location.origin || event.source !== frame.contentWindow) return;
    var m = event.data && event.data.orrGrafica;
    if (m === 'a' || m === 'n') load(current(), m);
  });
  frame.addEventListener('load', function () {
    var u = current();
    if (!inside(u)) return;
    try {
      var doc = frame.contentDocument, nav = frame.contentWindow.performance.getEntriesByType('navigation')[0];
      if ((nav && nav.responseStatus === 404) || /^404$/.test((doc.querySelector('h1')?.textContent || '').trim()) || /^(?:404|page not found|file not found)/i.test(doc.title)) { recover(); return; }
    } catch (e) {}
    if (!/\/girrr\/index\.html$/.test(u.pathname)) delete document.documentElement.dataset.anteprimaRipristinata;
    // La cornice gestisce la dissolvenza: evita doppie transizioni native nei frame annidati.
    try { var style = frame.contentDocument.createElement('style'); style.textContent = '@view-transition{navigation:none}'; frame.contentDocument.head.appendChild(style); } catch (e) {}
    mark(mode(u)); try { localStorage.setItem('registro-anteprima-online', u.href); } catch (e) {}
    requestAnimationFrame(function () { frame.classList.remove('out'); });
  });
  var first = new URL('girrr/index.html', base), m = 'a', restored = false;
  try { var saved = new URL(localStorage.getItem('registro-anteprima-online')); if (inside(saved)) { first = saved; restored = true; } m = localStorage.getItem('orr_gv') === 'n' ? 'n' : 'a'; } catch (e) {}
  if (restored) {
    // Il vecchio indirizzo può essere rimasto in memoria dopo una pagina rimossa.
    mark(m);
    fetch(convert(first, m).href, { cache: 'no-cache' }).then(function (r) {
      if (r.status === 404) recover(); else load(first, m);
    }).catch(function () { load(first, m); });
  } else load(first, m);
})();
