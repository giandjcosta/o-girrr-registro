#!/usr/bin/env python3
"""6.3 · Totogirrr per tutti gli schermi (Claude, 16 novembre 2026; richiesta di Gianluca dopo la 6.2.2).

- Totogirrr, schede in alto:
  * la scheda toccata si sposta quanto basta per vedersi tutta (prima restava tagliata: la fila che scorre è il <nav>,
    ma pillole.js controllava il contenitore interno .nvi, che non scorre mai, e la pagina la spostava solo nei ridisegni completi);
  * tocco breve e fluido: niente più rimpicciolimento «da pulsante tenuto premuto», il colore scivola in 220 ms invece di 380;
  * più trasparenti, senza la fascia scura dietro;
  * non restano attaccate in alto: scorrendo verso il basso vanno via con la pagina.
- Totogirrr su tablet, PC, monitor grandi e TV: pagina più larga e partite (e schedine) affiancate su due, tre o quattro colonne;
  sul telefono non cambia niente.
- Carriera › Giro di boa: tolta la targhetta «6.1 · Bilancio della stagione».
- Home: pillola «Esci da (squadra)» in fondo a sinistra, di fronte a quella della versione (due tocchi per uscire);
  nel Totogirrr non c'è più «Esci». Totogirrr con lo sfondo un po' più grigio in Lega e Stadio.

Uso: python3 rilascio/r63/applica.py COPIA_GH_PAGES_6_2_2
Si ferma se il sito non è la 6.2.2 pubblicata (gh-pages 64a243b). Rieseguibile: la seconda volta non cambia niente.
"""
import json, pathlib, re, sys

V = '63'

PILL = [
    # 1. una funzione che mostra per intero la scheda toccata nella fila che scorre davvero
    ("  function contenuto(c) {",
     "  /* 6.3 (Gianluca): nel Totogirrr la fila che scorre è il <nav>, non .nvi (largo quanto le schede, non scorre mai). La scheda\n"
     "     toccata si sposta quanto basta per vedersi tutta, con un margine, senza andare al centro. */\n"
     "  function fila(c) { return c.matches && c.matches('nav .nvi') ? c.parentElement : null; }\n"
     "  function mostra(s, b, subito) {\n"
     "    if (!scorri(s)) return;\n"
     "    var r = b.getBoundingClientRect(), e = s.getBoundingClientRect(), m = 14, d = 0;\n"
     "    if (r.left < e.left + m) d = r.left - e.left - m; else if (r.right > e.right - m) d = r.right - e.right + m;\n"
     "    if (Math.abs(d) < 1) return;\n"
     "    var to = Math.max(0, Math.min(s.scrollWidth - s.clientWidth, s.scrollLeft + d));\n"
     "    if (subito || ridotto()) s.scrollLeft = to; else s.scrollTo({ left: to, behavior: 'smooth' });\n"
     "  }\n"
     "  function contenuto(c) {"),
    # 2. al tocco: nel Totogirrr scorre il <nav>
    ("      var ferma = c2.matches && c2.matches(FERME);\n      if (ferma) {",
     "      var ferma = c2.matches && c2.matches(FERME), _nv = fila(c2);\n"
     "      if (_nv) mostra(_nv, n);   /* 6.3: Totogirrr, un solo codice muove la fila */\n"
     "      else if (ferma) {"),
    # 3. colore che scivola più breve nel Totogirrr
    ("        ], { duration: 380, easing: EASE });",
     "        ], { duration: _nv ? 220 : 380, easing: EASE });   /* 6.3: nel Totogirrr più corto (Gianluca) */"),
    # 4. all'apertura (anche con ?t=movimenti) la scheda scelta è in vista
    ("      var a = attiva(c); if (!a || !scorri(c)) return;",
     "      var a = attiva(c), _s = fila(c); if (_s) { if (a) mostra(_s, a, true); return; }   /* 6.3: Totogirrr */\n"
     "      if (!a || !scorri(c)) return;"),
]

NAVPOST = (
    "  var b=n.querySelector('button.on');\n"
    "  if(b){var sl=n.scrollLeft,cw=n.clientWidth,l=b.offsetLeft,r=l+b.offsetWidth,m=10,to=null;\n"
    "    if(l-m<sl)to=Math.max(0,l-m);else if(r+m>sl+cw)to=Math.min(n.scrollWidth-cw,r+m-cw);\n"
    "    if(to!==null&&Math.abs(to-sl)>1)n.scrollTo({left:to,behavior:'smooth'})}\n",
    "  /* 6.3: la scheda toccata la porta in vista solo pillole.js (prima due codici muovevano la stessa fila) */\n",
)

STILE = '''<style data-toto63>/* 6.3 · Totogirrr (Claude, 16 novembre 2026, richieste di Gianluca dopo la 6.2.2) */
/* Sfondo un po' più grigio, in Lega e Stadio (Gianluca): un velo sopra il blu, sotto le strisce; l'oro resta */
html::after{content:'';position:fixed;inset:0;z-index:-2;pointer-events:none;background:rgba(88,94,110,.30)}
/* Schede in alto: scorrono via con la pagina, più trasparenti, tocco breve (niente rimpicciolimento) */
nav{position:relative;top:auto;background:none;padding:4px 0}
nav button{background:rgba(255,255,255,.07);box-shadow:inset 0 0 0 1px rgba(255,255,255,.13);transition:background-color .18s ease,color .18s ease,opacity .12s ease}
nav button:active{transform:none;opacity:.78}
nav button.on{box-shadow:none}
@media (prefers-reduced-motion:reduce){nav button{transition:none}}
/* Telefoni piccoli (iPhone SE 320): il titolo «Totogirrr» resta su una riga (prima andava a capo dopo la T) */
@media (max-width:360px){.top{gap:8px}.top img{height:38px}.top h1{font-size:29px;white-space:nowrap}.bal{padding:5px 9px}.bal b{font-size:18px}}
/* Tablet, PC, monitor grandi e TV: pagina più larga, partite e schedine affiancate. Sul telefono non cambia niente. */
@media (min-width:700px){
  .wrap{max-width:1060px;padding-left:24px;padding-right:24px}
  .slip .in{max-width:1012px}
  .pane{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:14px;align-items:start}
  .pane>*{grid-column:1/-1;min-width:0}
  .pane>.card.m,.pane>.card.bet{grid-column:auto}
}
@media (min-width:1240px){
  .wrap{max-width:1320px;padding-left:32px;padding-right:32px}
  .slip .in{max-width:1256px}
  .pane{grid-template-columns:repeat(3,minmax(0,1fr));column-gap:16px}
}
@media (min-width:1760px){
  .wrap{max-width:1680px}
  .slip .in{max-width:1616px}
  .pane{grid-template-columns:repeat(4,minmax(0,1fr))}
}
@media (min-width:2200px){
  .wrap,.slip .in{zoom:1.25}
}
</style>
'''

TOTO = ['girrr/totogirrr.html', 'stadio/girrr/totogirrr.html']
ESCI_TOTO = ('<button class="x" id="out">Esci</button>', '')   # 6.3: si esce dalla Home (pillola in fondo a sinistra)

VERS_VECCHIO = '''  function inFondoHome(x) {
    if (document.querySelector('.vv-fondo')) return;
    var sp = document.querySelector('.wrap > .sp') || document.querySelector('.sp') || document.querySelector('.foot');
    if (sp && sp.parentNode) sp.parentNode.insertBefore(pillola(x), sp);
  }'''
VERS_NUOVO = '''  /* 6.3 · «Esci» (Gianluca, 16 novembre 2026): prima si usciva solo dal Totogirrr. Ora in fondo alla Home, a sinistra,
     sulla stessa riga della pillola della versione e con lo stesso aspetto. Si vede solo se sei entrato con la tua squadra
     o come ospite. Primo tocco: «Tocca di nuovo per uscire» per 3 secondi; secondo tocco: esci (il nome della squadra resta
     solo come proposta nella schermata di accesso, come faceva il Totogirrr) e la Home si ricarica. */
  function esci() {
    var fg = {}, osp = false;
    try { fg = JSON.parse(localStorage.getItem('fg') || '{}') || {}; } catch (e) {}
    try { osp = sessionStorage.getItem('ospite') === '1'; } catch (e) {}
    if (!(fg.team && fg.code) && !osp) return null;
    var b = document.createElement('button'); b.type = 'button'; b.className = 'vv-esci';
    var testo = fg.team && fg.code ? 'Esci da ' + fg.team : 'Esci';
    b.textContent = testo; b.setAttribute('aria-label', 'Esci da O Girrr');
    b.style.cssText = 'display:block;max-width:62%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding:7px 13px;font:800 12px/1 Inter,system-ui,sans-serif;letter-spacing:.06em;color:inherit;opacity:.8;border:1px solid rgba(255,255,255,.35);border-radius:999px;background:rgba(255,255,255,.06);cursor:pointer;-webkit-tap-highlight-color:transparent;transition:opacity .25s,background-color .25s,border-color .25s';
    var tm = 0;
    b.onclick = function () {
      if (!b.dataset.conferma) {
        b.dataset.conferma = '1'; b.textContent = 'Tocca di nuovo per uscire'; b.style.opacity = '1'; b.style.borderColor = 'rgba(255,255,255,.7)';
        clearTimeout(tm); tm = setTimeout(function () { delete b.dataset.conferma; b.textContent = testo; b.style.opacity = '.8'; b.style.borderColor = 'rgba(255,255,255,.35)'; }, 3000);
        return;
      }
      try { var o = JSON.parse(localStorage.getItem('fg') || 'null'); if (o && o.code) { o.code = ''; localStorage.setItem('fg', JSON.stringify(o)); } } catch (e) {}
      try { sessionStorage.removeItem('ospite'); } catch (e) {}
      /* si riapre la Home senza ?squadra= (accesso di prova del Lab) e senza un codice nell'indirizzo, che farebbero rientrare */
      try { var u = new URL(location.href); u.searchParams.delete('squadra'); u.hash = ''; location.replace(u.href); } catch (e) { location.reload(); }
    };
    return b;
  }
  function inFondoHome(x) {
    if (document.querySelector('.vv-fondo')) return;
    var sp = document.querySelector('.wrap > .sp') || document.querySelector('.sp') || document.querySelector('.foot');
    if (!sp || !sp.parentNode) return;
    var riga = document.createElement('div'); riga.className = 'vv-riga';
    riga.style.cssText = 'display:flex;align-items:center;justify-content:space-between;gap:10px;margin:18px 0 10px';
    var e = esci(), v = pillola(x); v.style.margin = '0 0 0 auto';
    if (e) riga.appendChild(e);
    riga.appendChild(v);
    sp.parentNode.insertBefore(riga, sp);
  }'''

BOA = ('<small class="gb-versione">6.1 · Bilancio della stagione</small>', '')


def sostituisci(t, rel, vecchio, nuovo):
    if nuovo and nuovo in t:
        return t
    if t.count(vecchio) != 1:
        if not nuovo and vecchio not in t:
            return t  # già tolto
        raise SystemExit('%s: atteso una volta «%s…», trovato %d volte: il sito non è la 6.2.2 pubblicata' % (rel, vecchio[:60], t.count(vecchio)))
    return t.replace(vecchio, nuovo)


def versioni(t):
    t = re.sub(r'pillole\.js\?v=\w+"', 'pillole.js?v=%s"' % V, t)
    t = re.sub(r'giro-di-boa\.js\?v=\w+', 'giro-di-boa.js?v=' + V, t)
    t = re.sub(r'condividi\.js\?v=\w+', 'condividi.js?v=' + V, t)
    t = re.sub(r'versioni\.js(\?v=\w+)?"', 'versioni.js?v=%s"' % V, t)
    return t


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    base = pathlib.Path(argv[0])
    v = json.loads((base / 'versioni.json').read_text(encoding='utf-8'))['versioni'][0]['v']
    if v not in ('6.2.2', '6.3'):
        raise SystemExit('La copia deve avere la 6.2.2 pubblicata (trovata ' + v + ')')
    cambiati = 0

    def scrivi(rel, fn):
        nonlocal cambiati
        f = base / rel; t = f.read_text(encoding='utf-8'); n = fn(t, rel)
        if n != t:
            f.write_text(n, encoding='utf-8'); cambiati += 1

    def pill(t, rel):
        for a, b in PILL:
            t = sostituisci(t, rel, a, b)
        return t
    scrivi('pillole.js', pill)

    def toto(t, rel):
        t = sostituisci(t, rel, *NAVPOST)
        t = sostituisci(t, rel, *ESCI_TOTO)
        if 'data-toto63' not in t:
            t = sostituisci(t, rel, '</head>', STILE + '</head>')
        return t
    for rel in TOTO:
        scrivi(rel, toto)

    scrivi('giro-di-boa.js', lambda t, rel: sostituisci(t, rel, *BOA))
    scrivi('condividi.js', lambda t, rel: versioni(t))
    scrivi('versioni.js', lambda t, rel: sostituisci(t, rel, VERS_VECCHIO, VERS_NUOVO))
    for html in sorted(base.rglob('*.html')):
        rel = str(html.relative_to(base))
        if rel.startswith(('v5', 'prova/')) or '/v5' in rel:
            continue
        scrivi(rel, lambda t, rel: versioni(t))
    print('6.3 applicata · File cambiati:', cambiati)


if __name__ == '__main__':
    main(sys.argv[1:])
