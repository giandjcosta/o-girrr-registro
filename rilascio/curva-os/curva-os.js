/* Curva · Uno stile per iPhone e uno per Android (Claude, 12 novembre 2026). Prototipo del Lab, il sito vero non cambia.
   1. Riconosce il telefono e scrive <html data-os="ios|android|altro">: iPhone e iPad → Liquid Glass, Android → Material 3,
      PC e il resto → la Curva di sempre. Per provare l'altro stile: ?os=ios, ?os=android (resta ricordato), ?os=auto torna al riconoscimento.
   2. Segna per mezzo secondo quando cambia la voce attiva della barra in basso o la scheda in alto (data-cambio-nav, data-cambio-tabs):
      la Curva ridisegna tutto anche dopo un applauso, così l'animazione parte solo quando cambi davvero sezione.
   Va caricato nella <head>, prima che la pagina si disegni. Lo stile è in curva-os.css. */
(function () {
  var r = document.documentElement, os = null;
  try {
    var m = location.search.match(/[?&]os=(ios|android|auto)\b/);
    if (m) { if (m[1] === 'auto') localStorage.removeItem('girrrOS'); else localStorage.setItem('girrrOS', m[1]); }
    os = localStorage.getItem('girrrOS');
  } catch (e) {}
  if (os !== 'ios' && os !== 'android') {
    var u = navigator.userAgent || '';
    os = /Android/i.test(u) ? 'android'
      : (/iPhone|iPad|iPod/.test(u) || (/Macintosh/.test(u) && navigator.maxTouchPoints > 1)) ? 'ios' : 'altro'; /* l'iPad si presenta come un Mac */
  }
  r.setAttribute('data-os', os);
  if (os === 'altro') return;

  var ultimo = {}, timer = {};
  function segna(nome) {
    r.setAttribute('data-cambio-' + nome, '');
    clearTimeout(timer[nome]);
    timer[nome] = setTimeout(function () { r.removeAttribute('data-cambio-' + nome); }, 600);
  }
  function controlla() {
    [['nav', '#nav .on'], ['tabs', '.tabs .on']].forEach(function (x) {
      var e = document.querySelector(x[1]), k = e ? (e.getAttribute('data-v') || e.textContent) : '';
      if (ultimo[x[0]] && k && k !== ultimo[x[0]]) segna(x[0]); /* non all'apertura della pagina */
      ultimo[x[0]] = k;
    });
  }
  function parti() { controlla(); new MutationObserver(controlla).observe(document.body, { childList: true, subtree: true }); }
  if (document.body) parti(); else document.addEventListener('DOMContentLoaded', parti);
})();
