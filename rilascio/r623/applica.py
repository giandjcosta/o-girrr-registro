#!/usr/bin/env python3
"""6.2.3 · Totogirrr per tutti gli schermi (Claude, 16 novembre 2026; richiesta di Gianluca dopo la 6.2.2).

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
- Condividi: pulsanti con il testo al centro in tutte le finestre; l'anteprima (video, Radio, immagini) sta tutta nella finestra.
- «‹ O Girrr» senza alone in tutte le pagine, anche nell'app (.oback).
- Cambio Lega/Stadio della Home senza pezzi che compaiono di colpo; Spogliatoio con sfondi diversi per Lega e Stadio,
  cambio di stile con dissolvenza e, nella Lega, rosso e azzurro alternati al posto dell'oro.
- Curva: la «C» in alto non porta più alla Home.

Uso: python3 rilascio/r623/applica.py COPIA_GH_PAGES_6_2_2
Si ferma se il sito non è la 6.2.2 pubblicata (gh-pages 64a243b). Rieseguibile: la seconda volta non cambia niente.
"""
import json, pathlib, re, sys

V = '623'

PILL = [
    # 1. una funzione che mostra per intero la scheda toccata nella fila che scorre davvero
    ("  function contenuto(c) {",
     "  /* 6.2.3 (Gianluca): nel Totogirrr la fila che scorre è il <nav>, non .nvi (largo quanto le schede, non scorre mai). La scheda\n"
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
     "      if (_nv) mostra(_nv, n);   /* 6.2.3: Totogirrr, un solo codice muove la fila */\n"
     "      else if (ferma) {"),
    # 3. colore che scivola più breve nel Totogirrr
    ("        ], { duration: 380, easing: EASE });",
     "        ], { duration: _nv ? 220 : 380, easing: EASE });   /* 6.2.3: nel Totogirrr più corto (Gianluca) */"),
    # 4. all'apertura (anche con ?t=movimenti) la scheda scelta è in vista
    ("      var a = attiva(c); if (!a || !scorri(c)) return;",
     "      var a = attiva(c), _s = fila(c); if (_s) { if (a) mostra(_s, a, true); return; }   /* 6.2.3: Totogirrr */\n"
     "      if (!a || !scorri(c)) return;"),
]

NAVPOST = (
    "  var b=n.querySelector('button.on');\n"
    "  if(b){var sl=n.scrollLeft,cw=n.clientWidth,l=b.offsetLeft,r=l+b.offsetWidth,m=10,to=null;\n"
    "    if(l-m<sl)to=Math.max(0,l-m);else if(r+m>sl+cw)to=Math.min(n.scrollWidth-cw,r+m-cw);\n"
    "    if(to!==null&&Math.abs(to-sl)>1)n.scrollTo({left:to,behavior:'smooth'})}\n",
    "  /* 6.2.3: la scheda toccata la porta in vista solo pillole.js (prima due codici muovevano la stessa fila) */\n",
)

STILE = '''<style data-toto623>/* 6.2.3 · Totogirrr (Claude, 16 novembre 2026, richieste di Gianluca dopo la 6.2.2) */
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
ESCI_TOTO = ('<button class="x" id="out">Esci</button>', '')   # 6.2.3: si esce dalla Home (pillola in fondo a sinistra)

VERS_VECCHIO = '''  function inFondoHome(x) {
    if (document.querySelector('.vv-fondo')) return;
    var sp = document.querySelector('.wrap > .sp') || document.querySelector('.sp') || document.querySelector('.foot');
    if (sp && sp.parentNode) sp.parentNode.insertBefore(pillola(x), sp);
  }'''
VERS_NUOVO = '''  /* 6.2.3 · «Esci» (Gianluca, 16 novembre 2026): prima si usciva solo dal Totogirrr. Ora in fondo alla Home, a sinistra,
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

# 6.2.3 · Condividi (Gianluca, foto del 16 novembre): «Condividi» non centrato in tutte le finestre dell'app (il pulsante usa la
# classe .pr, che in app.html è una riga a griglia con una colonna da 34 px) e anteprima del video più alta dello schermo.
CD_CSS = ("      '.cd-sf{margin:8px 0 0}' +\n",
          "      '.cd-sf{margin:8px 0 0}' +\n"
          "      '.cd-az a,.cd-az button{display:inline-flex;align-items:center;justify-content:center;text-align:center;grid-template-columns:none;border-top-width:0}' +   /* 6.2.3: testo centrato, niente righe .pr dell'app */\n")
CD_FN = ("  function anteprima(f, r, titolo) {\n",
         "  /* 6.2.3 (Gianluca): l'anteprima sta tutta nella finestra, senza scorrere: l'immagine prende l'altezza che resta\n"
         "     dopo titolo, testo e pulsanti (un video verticale era più alto dello schermo). Si riadatta se lo schermo cambia. */\n"
         "  function stringi(box) {\n"
         "    var img = box.querySelector('.cd-ant img'); if (!img) return;\n"
         "    img.style.width = 'auto'; img.style.maxWidth = 'min(100%, 360px)';\n"
         "    var fai = function () {\n"
         "      if (!img.isConnected) { removeEventListener('resize', fai); return; }\n"
         "      img.style.maxHeight = '';\n"
         "      var mx = parseFloat(getComputedStyle(box).maxHeight) || innerHeight, alto = Math.min(mx, innerHeight * 0.92);\n"
         "      var resto = box.scrollHeight - img.getBoundingClientRect().height;\n"
         "      img.style.maxHeight = Math.max(140, Math.floor(alto - resto - 2)) + 'px';\n"
         "    };\n"
         "    if (img.complete && img.naturalWidth) fai(); else img.addEventListener('load', fai);\n"
         "    addEventListener('resize', fai);\n"
         "  }\n"
         "  function anteprima(f, r, titolo) {\n")
CD_SH = ("\n    var sh = f.box.querySelector('[data-a=sh]');\n", "\n    stringi(f.box);   /* 6.2.3 */\n    var sh = f.box.querySelector('[data-a=sh]');\n")
CD_SH2 = ("\n      var sh = f.box.querySelector('[data-a=sh]');\n", "\n      stringi(f.box);   /* 6.2.3 */\n      var sh = f.box.querySelector('[data-a=sh]');\n")

# 6.2.3 · Niente alone su «‹ O Girrr» (Gianluca: «avevo già detto di togliere l'alone… in tutte le pagine»). La 6.2.2 copriva .back;
# nell'app il link si chiama .oback. Niente evidenziazione, contorno, menu del tocco lungo, e il fuoco non resta sul link.
TV = ('/* 6.2.3 · alone', """/* 6.2.3 · alone su «‹ O Girrr» (Gianluca): nell'app il link indietro si chiama .oback (la 6.2.2 copriva solo .back). Né evidenziazione
   del tocco né contorno né anteprima del tocco lungo; dopo il tocco e al ritorno con «Indietro» il link non resta col fuoco. */
(function () { try {
  var s = document.createElement('style');
  s.textContent = '.back,.oback{-webkit-tap-highlight-color:transparent!important;-webkit-touch-callout:none;outline:none!important;box-shadow:none!important}'
    + '.back:focus,.oback:focus,.back:focus-visible,.oback:focus-visible{outline:none!important;box-shadow:none!important;background:transparent!important}.oback:active{opacity:.7}';
  (document.head || document.documentElement).appendChild(s);
  var giu = function () { var a = document.activeElement; if (a && a.matches && a.matches('.back,.oback')) a.blur(); };
  document.addEventListener('click', function (e) { var a = e.target && e.target.closest && e.target.closest('.back,.oback'); if (a) a.blur(); }, true);
  addEventListener('pageshow', giu); document.addEventListener('visibilitychange', giu);
} catch (e) {} })();""")

# 6.2.3 · Cambio di grafica Lega/Stadio senza scatti (Gianluca: «le transizioni per tutti i cambi di grafica sono scattose»).
# Registrato: dopo la dissolvenza la Home nuova arrivava mezza vuota e mezzo secondo dopo comparivano di colpo l'avviso della
# versione e le Notifiche, con «Oggi al Girrr» che saltava giù. Ora, arrivando dall'interruttore, sotto il titolo la pagina
# resta trasparente finché smette di cambiare (al massimo 1,2 secondi) e poi entra con una dissolvenza.
GRAFICA = ('/* 6.2.3 · arrivo', """/* 6.2.3 · arrivo dall'interruttore Lega/Stadio senza scatti (Gianluca): sotto il titolo la pagina entra con una dissolvenza
   quando ha finito di disegnarsi (avviso della versione, Notifiche, «Oggi al Girrr»), invece di comparire a pezzi. */
(function () { try {
  document.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('#gsw button[aria-pressed=false]')) try { sessionStorage.setItem('gsw_arrivo', '1'); } catch (x) {} }, true);
  var arrivo = false; try { arrivo = sessionStorage.getItem('gsw_arrivo') === '1'; sessionStorage.removeItem('gsw_arrivo'); } catch (x) {}
  if (!arrivo || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
  var h = document.documentElement, s = document.createElement('style');
  s.textContent = 'html.gsw-attesa .wrap>:not(.hero),html.gsw-attesa .hero h1{opacity:0}html.gsw-pronta .wrap>:not(.hero),html.gsw-pronta .hero h1{transition:opacity .38s ease}';
  (document.head || h).appendChild(s); h.classList.add('gsw-attesa');
  var t0 = Date.now(), ultimo = Date.now(), fatto = false;
  var mostra = function () { if (fatto) return; fatto = true; h.classList.add('gsw-pronta'); requestAnimationFrame(function () { h.classList.remove('gsw-attesa'); setTimeout(function () { h.classList.remove('gsw-pronta'); }, 450); }); };
  var guarda = function () {
    if (window.MutationObserver && document.body) new MutationObserver(function () { ultimo = Date.now(); }).observe(document.body, { childList: true, subtree: true });
    (function controlla() { var ora = Date.now(), font = !document.fonts || document.fonts.status === 'loaded'; if ((ora - ultimo > 200 && font) || ora - t0 > 1200) mostra(); else setTimeout(controlla, 60); })();   /* anche il carattere del titolo (Lobster nello Stadio) */
  };
  if (document.body) guarda(); else document.addEventListener('DOMContentLoaded', guarda);
} catch (e) {} })();""")

# 6.2.3 · Spogliatoio: Lega e Stadio avevano lo stesso sfondo (una regola comune ai due stili); ora come nelle pagine del sito:
# Lega blu con le strisce, Stadio con i riflessi rosso e azzurro. E il cambio di stile entra con una dissolvenza.
SPO_CSS = ('</head>', """<style data-spogliatoio623>/* 6.2.3 (Gianluca): sfondi diversi per Lega e Stadio, come nelle pagine del sito; cambio di stile con dissolvenza */
:root[data-skin="girrr"]{--body:repeating-linear-gradient(115deg,rgba(255,255,255,.04) 0 36px,transparent 36px 72px),radial-gradient(1200px 700px at 80% -10%,#2c3f7c 0,#1d2a52 55%,#141d3d 100%)}
:root[data-skin="stadio"]{--body:radial-gradient(900px 520px at 85% -8%,rgba(214,40,57,.26),transparent 62%),radial-gradient(1000px 640px at -10% 18%,rgba(61,147,214,.26),transparent 60%),linear-gradient(180deg,#2c3f7c,#1d2a52 45%,#141d3d)}
::view-transition-old(root),::view-transition-new(root){animation-duration:.35s;animation-timing-function:ease}
/* Grafica Lega: rosso e azzurro al posto di rosso e oro (Gianluca). Lo Stadio resta oro. Le schede e i pulsanti si alternano:
   la scheda scelta è rossa o azzurra secondo la posizione; Svincolati: ruolo rosso, ordine azzurro; Calendario: Classic League
   rossa, Champions Cup azzurra (come nel sito); tra due pulsanti vicini il secondo è azzurro. I colori dello stato («In dubbio»…) restano. */
:root[data-skin="girrr"]{--hl:#8fd0ff;--hl-ink:#0d1f3c;--hl-bg:rgba(61,147,214,.18);--hl-name:#8fd0ff;--num:#8fd0ff}
:root[data-skin="girrr"] header .sub{color:#8fd0ff}
:root[data-skin="girrr"] header::after{background:linear-gradient(90deg,#d62839 0 60%,#3d93d6 60% 100%)}
:root[data-skin="girrr"] nav button[data-alt="az"][aria-selected=true],:root[data-skin="girrr"] .seg button[data-sort][aria-pressed=true],:root[data-skin="girrr"] .seg button[data-comp="cup"][aria-pressed=true]{background:#3d93d6;border-color:#3d93d6;color:#fff;box-shadow:none}
:root[data-skin="girrr"] .btn:not(.o):not(.ghost)+.btn:not(.o):not(.ghost):nth-of-type(even){background:#3d93d6;border-color:#3d93d6;color:#fff}
:root[data-skin="girrr"] nav button,:root[data-skin="girrr"] .seg button{transition:background-color .25s ease,border-color .25s ease,color .25s ease}
</style>
<script>/* 6.2.3: alternanza rosso / azzurro delle schede visibili (da ospite alcune sono nascoste) */(function(){function alt(){var t=document.getElementById('tabs');if(!t)return;var i=0;[].forEach.call(t.querySelectorAll('button'),function(b){var v=b.hidden?null:(i++%2?'az':'ro');if(b.getAttribute('data-alt')!==v){if(v)b.setAttribute('data-alt',v);else b.removeAttribute('data-alt')}})}
document.addEventListener('DOMContentLoaded',function(){alt();var t=document.getElementById('tabs');if(t&&window.MutationObserver)new MutationObserver(alt).observe(t,{subtree:true,childList:true,attributes:true,attributeFilter:['hidden']})})})()</script>
</head>""")
SPO_JS = ("try{document.cookie='gskin='+LS.skin+'; max-age=31536000; path=/; SameSite=Lax'}catch(e){}render()}});",
          "try{document.cookie='gskin='+LS.skin+'; max-age=31536000; path=/; SameSite=Lax'}catch(e){}/* 6.2.3: cambio di stile con dissolvenza */var _rid=false;try{_rid=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}if(!_rid&&document.startViewTransition){document.startViewTransition(function(){render()})}else if(!_rid&&document.body.animate){var _a=document.body.animate([{opacity:1},{opacity:0}],{duration:140,easing:'ease-in'});_a.onfinish=function(){render();document.body.animate([{opacity:0},{opacity:1}],{duration:240,easing:'ease-out'})}}else render()}});")

# 6.2.3 · Curva: la «C» in alto a sinistra non porta più alla Home (aveva data-lega): alla Home si va da «O Girrr» nella barra
# in basso. (Il corsivo della Curva nello Stadio resta: Gianluca ci ha ripensato, «lo manteniamo».)
CURVA_C = ('<i class="lg" data-lega="1" style="width:28px;height:28px;cursor:pointer"></i>',
           '<i class="lg" aria-hidden="true" style="width:28px;height:28px"></i>')

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
    t = re.sub(r'([\"/])tv\.js(\?v=\w+)?(?=[\"\'])', r'\1tv.js?v=' + V, t)
    t = re.sub(r'"grafica\.js(\?v=\w+)?"', '"grafica.js?v=%s"' % V, t)
    return t


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    base = pathlib.Path(argv[0])
    v = json.loads((base / 'versioni.json').read_text(encoding='utf-8'))['versioni'][0]['v']
    if v not in ('6.2.2', '6.2.3'):
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
        if 'data-toto623' not in t:
            t = sostituisci(t, rel, '</head>', STILE + '</head>')
        return t
    for rel in TOTO:
        scrivi(rel, toto)

    scrivi('giro-di-boa.js', lambda t, rel: sostituisci(t, rel, *BOA))
    def cd(t, rel):
        t = versioni(t)
        for a, b in (CD_CSS, CD_FN):
            t = sostituisci(t, rel, a, b)
        if 'stringi(f.box);' not in t:
            if t.count(CD_SH[0]) != 1 or t.count(CD_SH2[0]) != 1:
                raise SystemExit('condividi.js: finestre di anteprima diverse da quelle della 6.2.2')
            t = t.replace(CD_SH[0], CD_SH[1]).replace(CD_SH2[0], CD_SH2[1])
        return t
    scrivi('condividi.js', cd)

    def tv(t, rel):
        if TV[0] not in t:
            t = t.rstrip('\n') + '\n' + TV[1] + '\n'
        return t
    scrivi('tv.js', tv)

    def grafica(t, rel):
        if GRAFICA[0] not in t:
            t = t.rstrip('\n') + '\n' + GRAFICA[1] + '\n'
        return t
    for rel in ('girrr/grafica.js', 'stadio/girrr/grafica.js'):
        scrivi(rel, grafica)

    def spogliatoio(t, rel):
        if 'data-spogliatoio623' not in t:
            t = sostituisci(t, rel, *SPO_CSS)
        return sostituisci(t, rel, *SPO_JS)
    scrivi('index.html', spogliatoio)

    def curva(t, rel):
        t = sostituisci(t, rel, *CURVA_C)
        return t
    for rel in ('girrr/curva.html', 'stadio/girrr/curva.html'):
        scrivi(rel, curva)
    scrivi('versioni.js', lambda t, rel: sostituisci(t, rel, VERS_VECCHIO, VERS_NUOVO))
    for html in sorted(base.rglob('*.html')):
        rel = str(html.relative_to(base))
        if rel.startswith(('v5', 'prova/')) or '/v5' in rel:
            continue
        scrivi(rel, lambda t, rel: versioni(t))
    print('6.2.3 applicata · File cambiati:', cambiati)


if __name__ == '__main__':
    main(sys.argv[1:])
