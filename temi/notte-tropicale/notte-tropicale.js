/* O Girrr · Notte Tropicale, barra in basso (Claude, 17 novembre 2026; idea dal bozzetto di ChatGPT mostrato da Gianluca).
   Solo durante l'evento e solo sul telefono (il CSS la nasconde sopra i 760 px): Home, Tabellone, il pallone al centro per il
   Totogirrr, Curva e Giornale, nella cartella della grafica in cui sei (Lega o Stadio). Non cambia link, dati né pagine:
   aggiunge solo una scorciatoia. Non compare nella Curva (ha già la sua barra) e si nasconde quando c'è la schedina. */
(function () {
  'use strict';
  try {
    var p = location.pathname;
    if (!/\/girrr\/([a-z0-9-]+\.html)?$/.test(p)) return;          /* solo le pagine di Lega e Stadio, non lo Spogliatoio */
    var pag = (p.match(/\/([a-z0-9-]+\.html)$/) || [])[1] || 'index.html';
    if (pag === 'curva.html') return;
    /* grafica unica: il Campo ha la sua scelta Lega/Stadio nella pagina; durante l'evento resta Lega, senza salvare niente */
    if (/^campo/.test(pag)) {
      var lega = function () { if (document.body && document.body.dataset.skin && document.body.dataset.skin !== 'lega') document.body.dataset.skin = 'lega'; };
      if (document.body) lega(); else document.addEventListener('DOMContentLoaded', lega);
    }
    /* la barra è messa da parte (Gianluca, 17 novembre): compare solo con ?evento-extra=barra */
    if (!/(^| )barra( |$)/.test(document.documentElement.getAttribute('data-event-extra') || '')) return;
    var I = {
      home: '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 9.5V20h13V9.5"/>',
      tab: '<path d="M7 4h10v4a5 5 0 0 1-10 0z"/><path d="M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4M12 13v4M8 20h8"/>',
      curva: '<path d="M4 5h16v10H9l-5 4z"/>',
      gio: '<path d="M5 4h11v16H6a2 2 0 0 1-2-2V6"/><path d="M16 8h3v10a2 2 0 0 1-2 2M8 8h5M8 12h5M8 16h3"/>',
      palla: '<circle cx="12" cy="12" r="9"/><path d="m12 7 4 3-1.5 5h-5L8 10z"/><path d="M12 3v4M16 10l4.5-1.5M14.5 15l2.5 4M9.5 15 7 19M8 10 3.5 8.5"/>'
    };
    var V = [['index.html', 'Home', 'home'], ['tabellone.html', 'Tabellone', 'tab'], ['totogirrr.html', 'Totogirrr', 'palla'],
             ['curva.html', 'Curva', 'curva'], ['giornale.html', 'Giornale', 'gio']];
    var nav = document.createElement('nav');
    nav.className = 'nt-barra'; nav.setAttribute('aria-label', 'Notte Tropicale · Scorciatoie');
    nav.innerHTML = V.map(function (v) {
      var qui = v[0] === pag;
      return '<a href="' + v[0] + '"' + (v[2] === 'palla' ? ' class="nt-palla"' : '') + (qui ? ' aria-current="page"' : '') + '>' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + I[v[2]] + '</svg>' +
        '<span>' + v[1] + '</span></a>';
    }).join('');
    function metti() {
      if (document.querySelector('.nt-barra')) return;
      document.body.appendChild(nav);
      document.documentElement.classList.add('nt-con-barra');
      requestAnimationFrame(function () { requestAnimationFrame(function () { nav.classList.add('su'); }); });
    }
    if (document.body) metti(); else document.addEventListener('DOMContentLoaded', metti);
  } catch (e) {}
})();
