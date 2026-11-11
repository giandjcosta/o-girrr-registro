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
    'condividi.js': new URL('../../rilascio/condividi/condividi.js', self.location.href).href, /* Condividi come immagine */
    'stagione.js': new URL('../../rilascio/stagione/stagione.js', self.location.href).href, /* Carriera · La mia stagione */
    'girrr/app.html': new URL('../../rilascio/redazione/pagine/girrr/app.html', self.location.href).href, /* 5.8: domande della redazione di Girrr Sport (sopra la 5.7) */
    'stadio/girrr/app.html': new URL('../../rilascio/redazione/pagine/stadio/girrr/app.html', self.location.href).href,
    'girrr/dati/redazione.json': new URL('../redazione/redazione.json', self.location.href).href, /* scritto da Claude e controllato da redazione/controlla.py */
    'conferenze.js': new URL('../../rilascio/conferenze/conferenze.js', self.location.href).href,
    'tv.js': new URL('../../rilascio/conferenze/tv.js', self.location.href).href, /* testo più grande solo sulla TV (?tv per provarlo dal PC) */
    'notifiche-lette.js': new URL('../../rilascio/notifiche/notifiche-lette.js', self.location.href).href, /* lette rimpicciolite */
    'girrr/curva.html': new URL('../../rilascio/conferenze/pagine/girrr/curva.html', self.location.href).href, /* 5.6.3 (cuori e rilanci) più ?scrivi= della conferenza */
    'stadio/girrr/curva.html': new URL('../../rilascio/conferenze/pagine/stadio/girrr/curva.html', self.location.href).href,
    'push.js': new URL('../../rilascio/push/push.js', self.location.href).href, /* notifiche sul telefono */
    'apri.html': new URL('../../rilascio/scorciatoie/apri.html', self.location.href).href,
    'liquid-glass.css': new URL('../../rilascio/liquid-glass/liquid-glass.css', self.location.href).href, /* prototipo Liquid Glass dello Stadio (?stile=vetro) */
    'material.css': new URL('../../rilascio/liquid-glass/material.css', self.location.href).href, /* prototipo Android, Material 3, dello Stadio (?stile=android) */
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
        var rel = href.slice(sito.length).split('#')[0], p = rel.split('?')[0]; /* nelle navigazioni l'indirizzo arriva con il #: senza toglierlo la pagina di prova non si riconosceva */
        if (locali[p]) { dest = locali[p]; loc = true; } else dest = origine + rel;
      }
      return fetch(dest, { cache: init.cache || 'default', credentials: 'same-origin' }).then(function (r) {
        var ct = r.headers.get('content-type') || '';
        if (!r.ok || !/text\/html|javascript|json|text\/css|manifest/.test(ct)) return r;
        return r.text().then(function (t) {
          if (!loc || /\.html$/.test(dest.split('?')[0])) t = riscrivi(t); /* le pagine del sito preparate qui si riscrivono come le altre */
          /* La Carriera e la Conferenza leggono lab-dati.json con una richiesta sincrona, che il browser non fa passare dal
             service worker: nello specchio andrebbe persa e la pagina userebbe i dati incorporati, vecchi. Va diretta al sito. */
          if (/text\/html/.test(ct)) t = t.replace(/x\.open\('GET','(?:\.\.\/\.\.\/girrr\/|)dati\/lab-dati\.json\?'/g, "x.open('GET','" + origine + "girrr/dati/lab-dati.json?'");
          if (/text\/html/.test(ct) && t.indexOf('tv.js') < 0) t = t.replace(/<head[^>]*>/i, function (h) { return h + '<script src="' + sito + 'tv.js"></script>'; }); /* testo grande sulla TV, su ogni pagina */
          if (/text\/html/.test(ct) && t.indexOf('offline.js') < 0) t = t.replace(/<\/head>/i, '<script src="' + sito + 'offline.js" defer></script></head>');
          if (/text\/html/.test(ct) && /\/o-fant-a-girrr\/(stadio\/)?girrr\/(index\.html|notifiche\.html)?$/.test(dest.split('?')[0]) && t.indexOf('versioni.js') < 0) t = t.replace(/<\/head>/i, '<script src="' + sito + 'versioni.js" defer></script></head>');
          if (/text\/html/.test(ct) && /\/o-fant-a-girrr\/(index\.html)?$/.test(dest.split('?')[0]) && t.indexOf('cerca.js') < 0) t = t.replace(/<\/head>/i, '<script src="' + sito + 'cerca.js" defer></script></head>');
          if (/text\/html/.test(ct) && /\/(tabellone|giornale)\.html$/.test(dest.split('?')[0]) && t.indexOf('condividi.js') < 0) t = t.replace(/<\/head>/i, '<script src="' + sito + 'condividi.js" defer></script></head>');
          if (/text\/html/.test(ct) && /\/notifiche\.html$/.test(dest.split('?')[0]) && t.indexOf('notifiche-lette.js') < 0) t = t.replace(/<\/head>/i, '<script src="' + sito + 'notifiche-lette.js" defer></script></head>');
          if (/text\/html/.test(ct) && /\/notifiche\.html$/.test(dest.split('?')[0]) && t.indexOf('push.js') < 0) t = t.replace(/<\/head>/i, '<script src="' + sito + 'push.js" defer></script></head>');
          /* Prototipi grafici dello Stadio, uno alla volta: ?stile=vetro (Liquid Glass, iPhone), ?stile=android (Material 3), ?stile=0 li spegne.
             ?vetro e ?vetro=0 funzionano ancora. La scelta resta ricordata; il foglio va in fondo alla pagina, così vince sugli stili del sito */
          if (/text\/html/.test(ct) && href.indexOf(sito + 'stadio/girrr/') === 0 && t.indexOf('girrrStile') < 0) t = t.replace(/<\/head>/i, '<script>(function(){try{var q=location.search,m=q.match(/[?&]stile=(\\w+)/),s=m?m[1]:(/[?&]vetro=0/.test(q)?"0":(/[?&]vetro/.test(q)?"vetro":null));if(s==="0")localStorage.removeItem("girrrStile");else if(s==="vetro"||s==="android")localStorage.setItem("girrrStile",s);s=localStorage.getItem("girrrStile");if(!s)return;var f={vetro:"liquid-glass.css",android:"material.css"}[s];if(!f)return;document.documentElement.classList.add("lg-"+s);function m2(){var l=document.createElement("link");l.rel="stylesheet";l.href="' + sito + '"+f;document.body.appendChild(l)}if(document.body)m2();else document.addEventListener("DOMContentLoaded",m2)}catch(e){}})()</script></head>');
          return new Response(t, { status: r.status, headers: { 'content-type': ct } });
        });
      });
    }
  };
})();
importScripts('../../rilascio/offline/sw.js');
