#!/usr/bin/env python3
"""6.2.4 · Correzioni minori sopra la 6.2.3 pubblicata (Claude, 17 novembre 2026; richieste di Gianluca del 16 sera).

- «‹ O Girrr» senza fondo: nelle pagine con la testata v55 (Versioni, Notifiche e altre) il link .v55-return prendeva un fondo
  grigio chiaro con gli angoli arrotondati al passaggio del mouse e dopo il tocco (regola .v55-header a:hover di v55/ui.css).
  Ora nessun link indietro (.v55-return, .back, .oback) ha fondo, contorno o alone in nessuno stato, e il link perde il fuoco
  al tocco e al ritorno. In tv.js, che è in tutte le pagine (tv.js?v=624).
- Totogirrr, schede in alto: sono pulsanti separati, non un interruttore. Il colore non scivola più da una scheda all'altra:
  quella lasciata lo perde e quella toccata lo prende con una dissolvenza breve (0,18 s, transizione della 6.2.3). Restano
  la scheda toccata che si vede tutta e il tocco senza rimpicciolimento (pillole.js?v=624).
- Spogliatoio › Calendario: cambiando giornata (‹ ›) o competizione la freccia resta dove l'hai toccata (prima su Safari la
  pagina saltava), l'altezza resta ferma durante il cambio e la nuova giornata entra con una dissolvenza che scivola dal lato
  della freccia. Con «riduci movimento» cambia e basta.
- Spogliatoio senza salti da allenatore: il breve «Carico…» delle schede pesanti compare solo entrando nella scheda, non a
  ogni cambio di giornata, ruolo o filtro (assets/spogliatoio-lazy.js?v=624).

Uso: python3 rilascio/r624/applica.py COPIA_GH_PAGES_6_2_3
Si ferma se il sito non è la 6.2.3 pubblicata (gh-pages 4b0fc71). Rieseguibile: la seconda volta non cambia niente.
"""
import json, pathlib, re, sys

V = '624'

PILL = ("  var FERME = '.at,.dtab,.pt-competition,.oro-scroll';",
        "  /* 6.2.4 (Gianluca): anche le schede del Totogirrr (nav .nvi) sono pulsanti separati: il colore non scivola, passa con una\n"
        "     dissolvenza; lo scorrimento della fila resta quello della 6.2.3 (mostra). */\n"
        "  var FERME = '.at,.dtab,.pt-competition,.oro-scroll,nav .nvi';")

TV = ('/* 6.2.4 · «‹ O Girrr» senza fondo', """/* 6.2.4 · «‹ O Girrr» senza fondo (Gianluca: «avevo detto che quell'alone non lo volevo più»). Nelle pagine con la testata v55
   (Versioni, Notifiche…) il link indietro .v55-return prendeva un fondo grigio con gli angoli arrotondati al passaggio del mouse
   e, sul telefono, dopo il tocco (.v55-header a:hover di v55/ui.css). Nessun link indietro ha più fondo, contorno o alone. */
(function () { try {
  var L = '.v55-return,.back,.oback', S = function (q) { return L.split(',').map(function (x) { return x + q; }).join(','); };
  var s = document.createElement('style');
  s.textContent = S('') + '{-webkit-tap-highlight-color:transparent!important;-webkit-touch-callout:none}'
    + S(':hover') + ',' + S(':active') + ',' + S(':focus') + ',' + S(':focus-visible')
    + ',.v55-header a.v55-return:hover,.v55-header a.v55-return:active,.v55-header a.v55-return:focus'
    + '{background:transparent!important;background-color:transparent!important;box-shadow:none!important;outline:none!important}'
    + '.v55-return:active{opacity:.7}';
  (document.head || document.documentElement).appendChild(s);
  var giu = function () { var a = document.activeElement; if (a && a.matches && a.matches(L)) a.blur(); };
  document.addEventListener('click', function (e) { var a = e.target && e.target.closest && e.target.closest(L); if (a) setTimeout(function () { a.blur(); }, 0); }, true);
  addEventListener('pageshow', giu);
} catch (e) {} })();""")

CAL_FN = ("var calComp='lega',calIdx=null;",
          "/* 6.2.4 (Gianluca): cambiando giornata o competizione la freccia resta dove l'hai toccata (su Safari la pagina saltava),\n"
          "   l'altezza resta ferma durante il cambio e la nuova giornata entra con una dissolvenza dal lato della freccia. */\n"
          "function calCambia(dir){var nav=document.querySelector('.calnav'),y0=nav?nav.getBoundingClientRect().top:null;app.style.minHeight=app.offsetHeight+'px';render();"
          "var n2=document.querySelector('.calnav');if(n2&&y0!==null){var d=n2.getBoundingClientRect().top-y0;if(Math.abs(d)>1)window.scrollBy(0,d)}"
          "clearTimeout(calCambia.t);calCambia.t=setTimeout(function(){app.style.minHeight=''},500);"
          "var rid=false;try{rid=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}if(rid||!n2||!n2.animate)return;"
          "for(var el=n2.nextElementSibling;el;el=el.nextElementSibling){el.animate([{opacity:0,transform:'translateX('+(dir*18)+'px)'},{opacity:1,transform:'none'}],{duration:260,easing:'cubic-bezier(.22,.61,.36,1)'})}"
          "var nm=n2.querySelector('.name');if(nm&&nm.animate)nm.animate([{opacity:.25},{opacity:1}],{duration:220,easing:'ease-out'})}\n"
          "var calComp='lega',calIdx=null;")
CAL_FRECCE = ("b=t.closest('[data-cal]');if(b){calIdx+=+b.dataset.cal;render();return}",
              "b=t.closest('[data-cal]');if(b){calIdx+=+b.dataset.cal;calCambia(+b.dataset.cal);return}")
CAL_COMP = ("b=t.closest('[data-comp]');if(b){calComp=b.dataset.comp;calIdx=null;render();return}",
            "b=t.closest('[data-comp]');if(b){calComp=b.dataset.comp;calIdx=null;calCambia(0);return}")

# 6.2.4 · Spogliatoio senza salti (trovato provando da allenatore): assets/spogliatoio-lazy.js, nelle schede «pesanti»
# (Calendario, Svincolati, Mercato, Chi scambiare, Sostituzioni, Borsino, Statistiche), a OGNI cambio dentro la scheda
# (giornata, ruolo, filtro…) sostituiva la pagina con un breve «Carico…» alto pochi pixel: la pagina si accorciava, il
# browser riportava su e due fotogrammi dopo arrivava il contenuto. Ora il «Carico…» compare solo entrando in una scheda.
LAZY = [
    ("var pending = 0, lastSig = null, lastData = null;",
     "var pending = 0, lastSig = null, lastData = null, lastTab = null;   /* 6.2.4: il caricamento solo entrando in una scheda */"),
    ("      if (!state || !state.authed) {\n        lastSig = null;\n        return original.apply(this, arguments);\n      }",
     "      if (!state || !state.authed) {\n        lastSig = null; lastTab = null;\n        return original.apply(this, arguments);\n      }"),
    ("      if (!HEAVY[state.tab] || !target || signature === lastSig) {\n        lastSig = signature;\n",
     "      if (!HEAVY[state.tab] || !target || signature === lastSig || state.tab === lastTab) {\n        lastSig = signature; lastTab = state.tab;   /* 6.2.4: dentro la stessa scheda si ridisegna subito, senza «Carico…» */\n"),
    ("          lastSig = signature;\n          original.apply(context,args);",
     "          lastSig = signature; lastTab = state.tab;\n          original.apply(context,args);"),
]


def sostituisci(t, rel, vecchio, nuovo):
    if nuovo in t:
        return t
    if t.count(vecchio) != 1:
        raise SystemExit('%s: atteso una volta «%s…», trovato %d volte: il sito non è la 6.2.3 pubblicata' % (rel, vecchio[:60], t.count(vecchio)))
    return t.replace(vecchio, nuovo)


def versioni(t):
    t = re.sub(r'pillole\.js\?v=\w+"', 'pillole.js?v=%s"' % V, t)
    t = re.sub(r'([\"/])tv\.js(\?v=\w+)?(?=[\"\'])', r'\1tv.js?v=' + V, t)
    t = re.sub(r'spogliatoio-lazy\.js\?v=\w+', 'spogliatoio-lazy.js?v=' + V, t)
    return t


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    base = pathlib.Path(argv[0])
    v = json.loads((base / 'versioni.json').read_text(encoding='utf-8'))['versioni'][0]['v']
    if v not in ('6.2.3', '6.2.4'):
        raise SystemExit('La copia deve avere la 6.2.3 pubblicata (trovata ' + v + ')')
    cambiati = 0

    def scrivi(rel, fn):
        nonlocal cambiati
        f = base / rel; t = f.read_text(encoding='utf-8'); n = fn(t, rel)
        if n != t:
            f.write_text(n, encoding='utf-8'); cambiati += 1

    scrivi('pillole.js', lambda t, rel: sostituisci(t, rel, *PILL))
    scrivi('tv.js', lambda t, rel: t if TV[0] in t else t.rstrip('\n') + '\n' + TV[1] + '\n')

    def spogliatoio(t, rel):
        for a, b in (CAL_FN, CAL_FRECCE, CAL_COMP):
            t = sostituisci(t, rel, a, b)
        return versioni(t)
    scrivi('index.html', spogliatoio)

    def lazy(t, rel):
        for a, b in LAZY:
            t = sostituisci(t, rel, a, b)
        return t
    scrivi('assets/spogliatoio-lazy.js', lazy)
    for html in sorted(base.rglob('*.html')):
        rel = str(html.relative_to(base))
        if rel == 'index.html' or rel.startswith(('v5', 'prova/')) or '/v5' in rel:
            continue
        scrivi(rel, lambda t, rel: versioni(t))
    print('6.2.4 applicata · File cambiati:', cambiati)


if __name__ == '__main__':
    main(sys.argv[1:])
