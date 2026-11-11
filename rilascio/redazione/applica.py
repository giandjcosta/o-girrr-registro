#!/usr/bin/env python3
"""5.8 · Redazione di Girrr Sport nella Conferenza (Claude, 11 novembre 2026).

girrr/app.html e stadio/girrr/app.html: le domande della conferenza arrivano dalla redazione (girrr/dati/redazione.json,
letto da conferenze.js) quando ci sono per la squadra e la giornata; altrimenti restano quelle di sempre. Sotto il titolo,
«Domande della redazione di Girrr Sport».

Uso:  python3 rilascio/redazione/applica.py COPIA_GH_PAGES          scrive nella copia (rilascio)
      python3 rilascio/redazione/applica.py COPIA --lab             scrive in rilascio/redazione/pagine/ (prova nel Lab)
Va applicato dopo rilascio/conferenze/applica.py (5.7). Si può rilanciare.
"""
import pathlib, sys

QUI = pathlib.Path(__file__).resolve().parent
A = sys.argv[1:]
if not A:
    sys.exit(__doc__)
GH = pathlib.Path(A[0]); OUT = QUI / "pagine" if "--lab" in A else GH
SEGNO = "Claude, redazione 5.8"


def sost(t, rel, a, b):
    if t.count(a) != 1:
        sys.exit(f"{rel}: non trovo il punto da cambiare: {a[:70]!r}")
    return t.replace(a, b)


for rel in ("girrr/app.html", "stadio/girrr/app.html"):
    t = (GH / rel).read_text(encoding="utf-8")
    if SEGNO not in t:
        if "Claude, conferenze 10/11" not in t:
            sys.exit(f"{rel}: prima va applicata la 5.7 (rilascio/conferenze/applica.py)")
        t = sost(t, rel, "function confQs(t){var r=row(t),",
                 "/* " + SEGNO + ": domande della redazione di Girrr Sport, se ci sono per questa squadra e giornata */\n"
                 "function confSalvate(){var G=D.cal[0]&&D.cal[0].n,c=DBS.conf.filter(function(x){return x.giornata===G})[0];return c&&Array.isArray(c.risposte)?c.risposte:null}\n"
                 "function confQs(t){var RQ=window.GirrrRedazioneQs&&window.GirrrRedazioneQs(t,D.cal[0]&&D.cal[0].n,confSalvate(),!confSalvate()&&S.cf.a.some(function(x){return x!==undefined&&x!==null}));if(RQ)return RQ;\n var r=row(t),")
        t = sost(t, rel, "h+='<div class=\"card\"><h3>Vigilia di '+esc(t)+' - '+esc(o)+'</h3>';",
                 "h+='<div class=\"card\"><h3>Vigilia di '+esc(t)+' - '+esc(o)+'</h3>'+(Q[0]&&Q[0].red?'<p class=\"sm mut\" style=\"margin:2px 0 8px\">Domande della redazione di Girrr Sport, scritte per la tua squadra.</p>':'');")
    d = OUT / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    d.write_text(t, encoding="utf-8")
    print("scritta", d)
