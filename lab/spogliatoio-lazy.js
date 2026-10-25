/* Spogliatoio — lazy loading tab (Grok)
 *
 * Cosa fa:
 * 1) Prima paint della tab attiva, poi costruisce il contenuto pesante (requestAnimationFrame).
 * 2) Invalida la cache quando cambiano dati o filtri rilevanti.
 * 3) Borsino e Statistiche restano già lazy nel codice originale.
 *
 * Uso: dopo lo <script> principale di index.html dello Spogliatoio:
 *   <script src="…/spogliatoio-lazy.js?v=1"></script>
 *
 * Richiede che render, tab, app, vRosa… siano nello scope globale (come oggi).
 */
(function () {
  if (typeof render !== 'function') return;

  var HEAVY = { swap: 1, mkt: 1, fa: 1, pitch: 1, bor: 1, lega: 1, stat: 1 };
  var orig = render;
  var pending = 0;
  var lastSig = '';

  function sig() {
    try {
      return [
        tab,
        team,
        typeof D !== 'undefined' && D && D.updated,
        typeof filter !== 'undefined' ? filter : '',
        typeof role !== 'undefined' ? role : '',
        typeof sortBy !== 'undefined' ? sortBy : '',
        typeof open !== 'undefined' ? open : '',
        typeof mkV !== 'undefined' ? mkV : '',
        typeof mkT !== 'undefined' ? mkT : '',
        typeof calComp !== 'undefined' ? calComp : '',
        typeof calIdx !== 'undefined' ? calIdx : ''
      ].join('|');
    } catch (e) {
      return String(Date.now());
    }
  }

  function skeleton(name) {
    return (
      '<div class="card" style="padding:28px;text-align:center">' +
      '<div class="meta" style="margin-bottom:8px">Carico ' +
      String(name || 'sezione') +
      '…</div>' +
      '<div style="height:8px;border-radius:99px;background:rgba(255,255,255,.08);overflow:hidden">' +
      '<div style="height:100%;width:40%;background:linear-gradient(90deg,transparent,#a78bfa,transparent);animation:spglazy 1s linear infinite"></div>' +
      '</div></div>'
    );
  }

  if (!document.getElementById('spg-lazy-css')) {
    var st = document.createElement('style');
    st.id = 'spg-lazy-css';
    st.textContent =
      '@keyframes spglazy{from{transform:translateX(-100%)}to{transform:translateX(250%)}}';
    document.head.appendChild(st);
  }

  render = function () {
    var ok = typeof authed === 'function' ? authed() : true;
    var tabsEl = document.getElementById('tabs');
    if (tabsEl) tabsEl.hidden = !ok;

    // gate login: lascia il render originale (form di ingresso)
    if (!ok) {
      lastSig = '';
      return orig();
    }

    var s = sig();
    var heavy = HEAVY[tab];
    var appEl = document.getElementById('app');

    // Tab pesanti: prima skeleton, poi contenuto al frame successivo
    if (heavy && appEl && s !== lastSig) {
      var my = ++pending;
      // aggiorna subito stato tab selezionata
      try {
        if (tab === 'stat' && team !== 'Oranje VC') tab = 'rosa';
        [].forEach.call(document.querySelectorAll('#tabs button'), function (b) {
          b.setAttribute('aria-selected', b.dataset.t === tab);
          if (b.dataset.t === 'stat') b.hidden = team !== 'Oranje VC';
        });
      } catch (e) {}

      var labels = {
        swap: 'Chi scambiare',
        mkt: 'Mercato Scambi',
        fa: 'Svincolati',
        pitch: 'Sostituzioni',
        bor: 'Borsino',
        lega: 'Calendario',
        stat: 'Statistiche'
      };
      appEl.innerHTML = skeleton(labels[tab] || tab);

      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          if (my !== pending) return; // un click più recente ha vinto
          lastSig = sig();
          orig();
        });
      });
      return;
    }

    lastSig = s;
    return orig();
  };

  // Se data.json si aggiorna in background, invalida
  var _D = typeof D !== 'undefined' ? D : null;
  try {
    Object.defineProperty(window, 'D', {
      configurable: true,
      get: function () {
        return _D;
      },
      set: function (v) {
        _D = v;
        lastSig = '';
      }
    });
  } catch (e) {}
})();
