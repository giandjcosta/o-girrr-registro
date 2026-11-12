// Blocco delle scritture nel database per le prove automatiche (Claude, 12 novembre 2026).
// Le prove intercettano le funzioni che scrivono con context.route, ma in WebKit le richieste di una pagina servita
// da un service worker (lo specchio del Lab) passano dal service worker e l'intercettazione non le vede: una scrittura
// arrivava al database vero (rifiutata con «Codice non valido», niente scritto). Questo script, messo con addInitScript,
// blocca le scritture dentro la pagina, prima che partano, con qualunque motore. Le letture passano.
// Uso: await context.addInitScript(require('./blocca_scritture').script);
//      poi window.__scrittureBloccate dice quante ne ha fermate.
const SCRIVE = 'salva|scrivi|lancia|rispondi|vota|reagisci|registra|segui|push_|cancella|proponi|riscuoti|duello_|toto_|sondaggio|carriera_';
const script = `(() => {
  const S = new RegExp('${SCRIVE}'), f0 = window.fetch;
  window.__scrittureBloccate = 0;
  window.fetch = function (u, o) {
    try {
      const url = typeof u === 'string' ? u : (u && u.url) || '';
      const m = /\\/rest\\/v1\\/rpc\\/([^?]+)/.exec(url);
      if (m && S.test(m[1]) && !/_(stato|pubblico|lista)$/.test(m[1])) {
        window.__scrittureBloccate++;
        return Promise.resolve(new Response('null', { status: 200, headers: { 'content-type': 'application/json' } }));
      }
    } catch (e) {}
    return f0.apply(this, arguments);
  };
})();`;
module.exports = { script, SCRIVE };
