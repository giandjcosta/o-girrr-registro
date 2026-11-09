/* Prova della copia offline nel Lab (Claude, 9 novembre 2026).
   Le pagine di lab/offline/sito/… sono quelle vere del sito (/o-fant-a-girrr/…), prese al momento e servite qui
   con la copia offline attiva. Il sito vero non cambia. Il service worker è lo stesso che andrà sul sito:
   rilascio/offline/sw.js (qui sotto con importScripts), con questo «specchio» davanti. */
self.GIRRR_SPECCHIO = (function () {
  var qui = new URL('./', self.location.href).href;              /* …/o-girrr-registro/lab/offline/ */
  var sito = qui + 'sito/';
  var perc = new URL(sito).pathname;                              /* /o-girrr-registro/lab/offline/sito/ */
  var origine = new URL('/o-fant-a-girrr/', self.location.href).href;
  var locali = {
    'offline.js': new URL('../../rilascio/offline/offline.js', self.location.href).href,
    'cerca.js': new URL('../../rilascio/cerca/cerca.js', self.location.href).href, /* Cerca un giocatore nello Spogliatoio */
    'versioni.js': new URL('../../rilascio/versioni/versioni.js', self.location.href).href, /* pagina Versioni */
    'versioni.json': new URL('../../rilascio/versioni/versioni.json', self.location.href).href,
    'girrr/versioni.html': new URL('../../rilascio/versioni/pagine/girrr/versioni.html', self.location.href).href,
    'stadio/girrr/versioni.html': new URL('../../rilascio/versioni/pagine/stadio/girrr/versioni.html', self.location.href).href,
    'push.js': new URL('../../rilascio/push/push.js', self.location.href).href, /* notifiche sul telefono */
    'apri.html': new URL('../../rilascio/scorciatoie/apri.html', self.location.href).href,
    'manifest.webmanifest': new URL('../../rilascio/scorciatoie/manifest.webmanifest', self.location.href).href /* con le scorciatoie */
  };
  var percEsc = perc.replace(/\//g, '\\/');
  /* Gli indirizzi del sito vero diventano quelli dello specchio (anche nella regola che riconosce il sito) */
  var dominio = 'https://giandjcosta.github.io/', qua = self.location.origin + '/';
  function riscrivi(t) {
    t = t.split('\\/o-fant-a-girrr\\/').join(percEsc).split('/o-fant-a-girrr/').join(perc);
    return qua === dominio ? t : t.split(dominio + perc.slice(1)).join(qua + perc.slice(1)); /* solo per le prove in locale */
  }
  return {
    base: sito,
    prendi: function (href, init) {
      var dest = href, loc = false;
      if (href.indexOf(sito) === 0) {
        var rel = href.slice(sito.length), p = rel.split('?')[0];
        if (locali[p]) { dest = locali[p]; loc = true; } else dest = origine + rel;
      }
      return fetch(dest, { cache: init.cache || 'default', credentials: 'same-origin' }).then(function (r) {
        var ct = r.headers.get('content-type') || '';
        if (!r.ok || !/text\/html|javascript|json|text\/css|manifest/.test(ct)) return r;
        return r.text().then(function (t) {
          if (!loc) t = riscrivi(t);
          if (/text\/html/.test(ct) && t.indexOf('offline.js') < 0) t = t.replace(/<\/head>/i, '<script src="' + sito + 'offline.js" defer></script></head>');
          if (/text\/html/.test(ct) && /\/o-fant-a-girrr\/(stadio\/)?girrr\/(index\.html)?$/.test(dest.split('?')[0]) && t.indexOf('versioni.js') < 0) t = t.replace(/<\/head>/i, '<script src="' + sito + 'versioni.js" defer></script></head>');
          if (/text\/html/.test(ct) && /\/o-fant-a-girrr\/(index\.html)?$/.test(dest.split('?')[0]) && t.indexOf('cerca.js') < 0) t = t.replace(/<\/head>/i, '<script src="' + sito + 'cerca.js" defer></script></head>');
          if (/text\/html/.test(ct) && /\/notifiche\.html$/.test(dest.split('?')[0]) && t.indexOf('push.js') < 0) t = t.replace(/<\/head>/i, '<script src="' + sito + 'push.js" defer></script></head>');
          return new Response(t, { status: r.status, headers: { 'content-type': ct } });
        });
      });
    }
  };
})();
importScripts('../../rilascio/offline/sw.js');
