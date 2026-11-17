/* O Girrr · Caricatore dei temi evento (Claude, 17 novembre 2026). Proposta per il lavoro di ChatGPT sul tema evento.
   Va incluso UNA volta per pagina, il prima possibile (per esempio da tv.js, che è già in tutte le pagine di Lega, Stadio e
   Spogliatoio): accende il tema solo dentro la sua finestra di date, in ora italiana, e lo decide il browser all'apertura.
   Dopo la fine il tema si spegne da solo, senza rilasci e anche nella copia offline (il service worker conserva i file, ma
   la data la legge la pagina). Lega e Stadio non cambiano: il tema è solo l'attributo data-event-theme e il suo CSS.
   Per provarlo prima o dopo: ?evento=on | off | auto oppure ?evento=<nome del tema> (ricordato per la sessione) e
   ?evento-data=2026-11-19T12:00 per simulare il giorno (vale solo per quella pagina). Con l'attributo data-solo-manuale sul
   <script> (anteprima del Lab) il tema si accende solo a mano, mai per data. Se qualcosa va storto resta la grafica di sempre. */
(function () {
  'use strict';
  var EVENTI = [
    /* id, inizio e fine (fine esclusa) in ora italiana, foglio di stile accanto a questo file */
    { id: 'vice-city', inizio: '2026-11-18T00:00:00+01:00', fine: '2026-11-21T00:00:00+01:00', css: 'vice-city.css' },
    { id: 'notte-tropicale', inizio: '2026-11-18T00:00:00+01:00', fine: '2026-11-21T00:00:00+01:00', css: 'notte-tropicale/notte-tropicale.css', js: 'notte-tropicale/notte-tropicale.js',
      /* la Curva ha la sua grafica chiara/scura da app (iPhone e Android): il tema non la tocca, lì il testo diventava illeggibile */
      escludi: /\/curva\.html$/ }
  ];
  try {
    var me = document.currentScript, base = me && me.src ? me.src : location.href;
    var q = new URLSearchParams(location.search), K = 'girrr-evento';
    var modo = q.get('evento'), manuale = !!(me && me.hasAttribute('data-solo-manuale'));
    var nomi = EVENTI.map(function (x) { return x.id; });
    if (modo === 'on' || modo === 'off' || nomi.indexOf(modo) >= 0) { try { sessionStorage.setItem(K, modo); } catch (e) {} }
    else if (modo === 'auto') { try { sessionStorage.removeItem(K); } catch (e) {} modo = null; }
    if (!modo) { try { modo = sessionStorage.getItem(K); } catch (e) {} }
    var ora = new Date(), sim = q.get('evento-data');
    if (sim) { var d = new Date(/[zZ]|[+-]\d\d:?\d\d$/.test(sim) ? sim : sim + '+01:00'); if (!isNaN(d)) ora = d; }
    var ev = null;
    for (var i = 0; i < EVENTI.length; i++) {
      var e = EVENTI[i];
      if (modo === e.id) { ev = e; break; }
      if (nomi.indexOf(modo) >= 0) continue;   /* scelto un altro tema per nome */
      if (modo === 'on' || (!manuale && modo !== 'off' && ora >= new Date(e.inizio) && ora < new Date(e.fine))) { ev = e; break; }
    }
    window.OGirrrEvento = Object.freeze({ attivo: ev ? ev.id : null, modo: modo || 'auto', ora: ora.toISOString() });
    if (!ev || modo === 'off') return;
    if (ev.escludi && ev.escludi.test(location.pathname)) { window.OGirrrEvento = Object.freeze({ attivo: null, modo: modo || 'auto', ora: ora.toISOString(), escluso: ev.id }); return; }
    var h = document.documentElement;
    h.setAttribute('data-event-theme', ev.id);
    /* variante dello sfondo (Notte Tropicale): ?evento-sfondo=notte|tramonto|scena; senza, la foto predefinita del tema, ricordata per la sessione */
    var sf = q.get('evento-sfondo');
    if (sf) { try { sessionStorage.setItem(K + '-sfondo', sf); } catch (e) {} } else { try { sf = sessionStorage.getItem(K + '-sfondo'); } catch (e) {} }
    if (sf && /^[a-z-]{1,20}$/.test(sf)) h.setAttribute('data-event-sfondo', sf);
    var l = document.createElement('link');
    l.rel = 'stylesheet'; l.href = new URL(ev.css, base).href; l.setAttribute('data-evento', ev.id);
    l.onerror = function () { h.removeAttribute('data-event-theme'); };   /* senza CSS niente tema a metà */
    (document.head || h).appendChild(l);
    /* script facoltativo del tema (per esempio la barra in basso di Notte Tropicale): parte dopo il CSS, se il CSS non arriva no */
    if (ev.js) {
      var s = document.createElement('script'); s.src = new URL(ev.js, base).href; s.async = true; s.setAttribute('data-evento', ev.id);
      l.addEventListener('load', function () { (document.head || h).appendChild(s); });
    }
  } catch (err) { try { document.documentElement.removeAttribute('data-event-theme'); } catch (e2) {} }
})();
