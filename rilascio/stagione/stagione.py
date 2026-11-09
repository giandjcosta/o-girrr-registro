#!/usr/bin/env python3
"""Carriera · La mia stagione (Claude, 9 novembre 2026): aggiunge la scheda «Stagione» alla Carriera di app.html (Lega e Stadio).

Uso:
  python3 rilascio/stagione/stagione.py COPIA_GH_PAGES            scrive le due app.html nella copia (rilascio)
  python3 rilascio/stagione/stagione.py COPIA_GH_PAGES --lab      le scrive in rilascio/stagione/pagine/ (prova nel Lab)
Cambia tre punti: la scheda nella barra della Carriera (dopo Panoramica), il contenuto (window.GirrrStagione) e lo script stagione.js.
Si può rilanciare: se la scheda c'è già non cambia niente. stagione.js va copiato nella radice del sito (lo fa rilascio56.py).
"""
import pathlib, sys

QUI = pathlib.Path(__file__).resolve().parent
A = sys.argv[1:]
if not A:
    sys.exit(__doc__)
GH = pathlib.Path(A[0])
OUT = QUI / "pagine" if "--lab" in A else GH
TAB_A = "[['pan','Panoramica'],"
TAB_B = "[['pan','Panoramica'],['stag','Stagione'],"
DIS_A = "else if(S.ctab==='reg')h+=vCarRegole(t);"
DIS_B = DIS_A + "\n   else if(S.ctab==='stag')h+=(window.GirrrStagione?window.GirrrStagione(t):'');"
for rel, su in (("girrr/app.html", "../"), ("stadio/girrr/app.html", "../../")):
    t = (GH / rel).read_text(encoding="utf-8")
    if "['stag','Stagione']" not in t:
        if t.count(TAB_A) != 1 or t.count(DIS_A) != 1:
            sys.exit(f"{rel}: la Carriera è cambiata, controlla a mano")
        t = t.replace(TAB_A, TAB_B).replace(DIS_A, DIS_B)
        k = t.lower().find("</head>")
        t = t[:k] + f'<script src="{su}stagione.js" defer></script>\n' + t[k:]
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(t, encoding="utf-8")
    print("scritta", dest)
