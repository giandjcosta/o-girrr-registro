/* Interruttore d'emergenza della copia offline (Claude, 9 novembre 2026).
   Se la copia offline desse problemi: copiare QUESTO file sul sito al posto di sw.js (stesso nome, sw.js).
   Al primo controllo il telefono lo scarica, cancella le copie salvate, si toglie da solo e ricarica le pagine aperte. */
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (event) {
  event.waitUntil(caches.keys().then(function (n) {
    return Promise.all(n.filter(function (x) { return x.indexOf('girrr-') === 0 && x.indexOf('girrr-prova-') !== 0; }).map(function (x) { return caches.delete(x); }));
  }).then(function () { return self.registration.unregister(); }).then(function () {
    return self.clients.matchAll({ type: 'window' });
  }).then(function (c) { c.forEach(function (w) { w.navigate(w.url); }); }));
});
