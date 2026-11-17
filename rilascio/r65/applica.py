#!/usr/bin/env python3
"""6.5 · Correzioni sopra la 6.2.4 pubblicata (parte «fluidità» della 6.5; Gianluca: «non 6.2.5 ma 6.5, visto il grande cambiamento di grafica») (Claude, 17 novembre 2026; richieste di Gianluca del 17 sera).

- Girrr Sport, pillole bloccate: aprendo «Conferenze stampa» con un codice che il database non riconosce (o non ancora
  caricato) la pagina andava in errore (DBS.conf mancante) e da lì le pillole non cambiavano più. Ora le conferenze salvate
  si leggono solo se ci sono.
- Carriera (e le altre schede di app.html), cambio di scheda senza salti: la pagina teneva l'altezza solo finché il nuovo
  contenuto era pronto; se per un attimo era più corto (Giro di boa, Stagione, dati in arrivo) la pagina si accorciava, il
  browser riportava in cima e poi il contenuto ricompariva («viene su, trema, sparisce per un attimo»). Ora durante il cambio
  l'altezza resta ferma e, se il nuovo contenuto è più corto, la pagina si accorcia con calma (0,35 s), come nel Totogirrr.
- Carriera e Albo d'oro, pillole che scorrono: il colore passa dalla pillola di prima alla nuova scivolando, come in Girrr
  Sport e nel Tabellone (prima cambiava di colpo, come un pulsante). Lo scorrimento della fila resta quello della 6.2.2.
- Contenuto che entra con un rimbalzo morbido e un po' più lungo (0,56 s: sale di poco, supera appena e si ferma) invece della
  dissolvenza che partiva quasi trasparente e sembrava una sparizione. Il Totogirrr resta com'è (Gianluca: «fluidissimo»).
- Niente più «sparisce per un attimo»: dopo un tocco su una pillola i pezzi nuovi della pagina entravano anche con una seconda
  animazione, da completamente trasparenti e a scaletta fino a quasi mezzo secondo, insieme alla dissolvenza delle pillole. Ora,
  quando il cambio lo anima già pillole.js, la seconda animazione non parte (app.html e transizioni.js; misurato sul sito vero:
  il contenuto restava invisibile per circa un decimo di secondo).
- Con «riduci movimento» niente animazioni, come prima.

Uso: python3 rilascio/r65/applica.py COPIA_GH_PAGES_6_2_4
Si ferma se il sito non è la 6.2.4 pubblicata. Rieseguibile: la seconda volta non cambia niente.
"""
import json, pathlib, re, sys

V = '65'

APP = [
    # 1. conferenze salvate solo se ci sono
    ('DBS.conf.filter(', '(DBS.conf||[]).filter('),
    ('S.cf.a.some(', '(S.cf.a||[]).some('),
    # 2. altezza ferma durante il cambio di scheda, poi accorciamento morbido
    ("  morphDom(_vw,_nv);",
     "  /* 6.5 (Gianluca): durante il cambio di scheda l'altezza resta ferma (prima, se il nuovo contenuto era più corto per un\n"
     "     attimo, la pagina tornava su e tremava); poi, se serve, si accorcia con calma */\n"
     "  var _h0=_vw.offsetHeight;if(_h0>0){_vw.style.minHeight=_h0+'px';clearTimeout(render._mh);render._mh=setTimeout(function(){var _a=parseFloat(_vw.style.minHeight)||0;_vw.style.minHeight='';var _h1=_vw.offsetHeight;if(_h1<_a-2&&_vw.animate&&!matchMedia('(prefers-reduced-motion: reduce)').matches){_vw.style.minHeight=_h1+'px';var _an=_vw.animate([{minHeight:_a+'px'},{minHeight:_h1+'px'}],{duration:350,easing:'cubic-bezier(.22,.61,.36,1)'});_an.onfinish=_an.oncancel=function(){_vw.style.minHeight=''}}else _vw.style.minHeight=''},800)}\n"
     "  morphDom(_vw,_nv);"),
]
FX = ("  if(Date.now()-last>800)return;",
      "  if(Date.now()-last>800||Date.now()-(window.__pilloleT||0)<900)return;   /* 6.5: il cambio lo anima già pillole.js */")
PILL = [
    ("  var FERME = '.at,.dtab,.pt-competition,.oro-scroll,nav .nvi';",
     "  var FERME = '.at,.dtab,.pt-competition,.oro-scroll,nav .nvi';\n"
     "  /* 6.5 (Gianluca): nella Carriera e nell'Albo (.oro-scroll) il colore torna a scivolare come nelle altre file; la fila resta\n"
     "     ferma come dalla 6.2.1 (la sposta solo l'app). Nelle altre file ferme il colore passa con una dissolvenza. */\n"
     "  var NOSCIVOLO = '.at,.dtab,.pt-competition,nav .nvi';"),
    ("        try { el.animate([{ opacity: 0.25, transform: 'translateY(6px)' }, { opacity: 1, transform: 'none' }], { duration: 260, easing: EASE }); } catch (e) {}",
     "        /* 6.5 (Gianluca): fuori dal Totogirrr il contenuto entra con un rimbalzo morbido e più lungo, senza sparire */\n"
     "        try { if (_nv) el.animate([{ opacity: 0.25, transform: 'translateY(6px)' }, { opacity: 1, transform: 'none' }], { duration: 260, easing: EASE });\n"
     "          else el.animate([{ opacity: 0.6, transform: 'translateY(14px)' }, { opacity: 1, transform: 'translateY(-3px)', offset: 0.62 }, { opacity: 1, transform: 'none' }], { duration: 560, easing: 'cubic-bezier(.25,.8,.3,1)' }); } catch (e) {}"),
    ("      if (c2.matches && c2.matches(FERME)) return;", "      if (c2.matches && c2.matches(NOSCIVOLO)) return;"),
    ("  var NOSCIVOLO = '.at,.dtab,.pt-competition,nav .nvi';",
     "  var NOSCIVOLO = '.at,.dtab,.pt-competition,nav .nvi';\n"
     "  /* 6.5: un tocco su una pillola nuova lo segna subito (in cattura, prima che la pagina ridisegni): le altre animazioni\n"
     "     d'entrata (app.html, transizioni.js) per un attimo lasciano fare a pillole.js, così il contenuto non sparisce */\n"
     "  window.addEventListener('click', function (ev) { var b = ev.target && ev.target.closest && ev.target.closest('button'), c = b && b.parentElement;\n"
     "    if (c && c.matches && c.matches(FILE) && b.getAttribute('aria-pressed') !== 'true' && b.getAttribute('aria-selected') !== 'true' && !b.classList.contains('on')) window.__pilloleT = Date.now(); }, true);"),
]


def sostituisci(t, rel, vecchio, nuovo, tutte=False):
    if nuovo in t:
        return t
    n = t.count(vecchio)
    if n == 0 or (n != 1 and not tutte):
        raise SystemExit('%s: atteso «%s…», trovato %d volte: il sito non è la 6.2.4 pubblicata' % (rel, vecchio[:60], n))
    return t.replace(vecchio, nuovo)


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    base = pathlib.Path(argv[0])
    v = json.loads((base / 'versioni.json').read_text(encoding='utf-8'))['versioni'][0]['v']
    if v not in ('6.2.4', '6.5'):
        raise SystemExit('La copia deve avere la 6.2.4 pubblicata (trovata ' + v + ')')
    cambiati = 0

    def scrivi(rel, fn):
        nonlocal cambiati
        f = base / rel; t = f.read_text(encoding='utf-8'); n = fn(t, rel)
        if n != t:
            f.write_text(n, encoding='utf-8'); cambiati += 1

    def app(t, rel):
        t = sostituisci(t, rel, APP[0][0], APP[0][1], tutte=True)
        t = sostituisci(t, rel, APP[1][0], APP[1][1], tutte=True)
        t = sostituisci(t, rel, APP[2][0], APP[2][1])
        t = sostituisci(t, rel, FX[0], FX[1], tutte=True)
        return t
    for rel in ('girrr/app.html', 'stadio/girrr/app.html'):
        scrivi(rel, app)

    def pill(t, rel):
        for a, b in PILL:
            t = sostituisci(t, rel, a, b)
        return t
    scrivi('pillole.js', pill)
    for rel in ('girrr/transizioni.js', 'stadio/girrr/transizioni.js'):
        scrivi(rel, lambda t, rel: sostituisci(t, rel, FX[0], FX[1], tutte=True))
    for html in sorted(base.rglob('*.html')):
        rel = str(html.relative_to(base))
        scrivi(rel, lambda t, rel: re.sub(r'(?<=["/])transizioni\.js(\?v=\w+)?(?=["\'])', 'transizioni.js?v=' + V, re.sub(r'pillole\.js\?v=\w+', 'pillole.js?v=' + V, t)))
    print('6.5 applicata · File cambiati:', cambiati)


if __name__ == '__main__':
    main(sys.argv[1:])
