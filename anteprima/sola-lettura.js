/* Copia pubblicata nel Registro: blocco dentro la pagina, prima di ogni altro script.
   Nessun service worker e nessuna scrittura, anche con WebKit. */
(function () {
  'use strict';
  var nativeFetch = window.fetch.bind(window);
  var reads = new Set(['curva_feed', 'curva_img', 'curva_adm_img', 'curva_pimg', 'curva_adm_lista',
    'derby_stato', 'conf_pubbliche', 'conf_promesse', 'conf_dopo_pubbliche',
    'carriera_stato', 'toto_stato', 'toto_pr_stato', 'toto_pr_pubblico', 'duello_stato', 'notifiche_stato', 'push_stato']);
  function allowed(url, method) {
    var u = new URL(url, location.href);
    if (/(^|\.)supabase\.co$/i.test(u.hostname)) {
      var rpc = /^\/rest\/v1\/rpc\/([a-z_]+)$/.exec(u.pathname);
      return (method === 'GET' && /^\/storage\/v1\/object\/public\//.test(u.pathname)) ||
        ((method === 'GET' || method === 'POST') && rpc && reads.has(rpc[1]));
    }
    return method === 'GET' || method === 'HEAD';
  }
  window.fetch = function (resource, options) {
    var url = typeof resource === 'string' || resource instanceof URL ? String(resource) : resource.url;
    var method = String(options && options.method || resource.method || 'GET').toUpperCase();
    if (!allowed(url, method)) return Promise.resolve(new Response(JSON.stringify({message: 'Anteprima · Sola lettura: nessuna modifica salvata'}), {status: 403, headers: {'Content-Type': 'application/json'}}));
    return nativeFetch(resource, options);
  };
  var open = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (method, url) {
    if (!allowed(url, String(method).toUpperCase())) throw new Error('Anteprima · Scrittura bloccata');
    return open.apply(this, arguments);
  };
  if (navigator.sendBeacon) navigator.sendBeacon = function () { return false; };
  if (navigator.serviceWorker) navigator.serviceWorker.register = function () { return Promise.reject(new Error('Anteprima · Copia offline disattivata')); };
  window.__registroSolaLettura = true;
})();
