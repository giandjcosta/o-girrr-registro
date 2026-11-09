#!/usr/bin/env python3
"""Pagina Versioni (Claude, 9 novembre 2026): crea girrr/versioni.html e stadio/girrr/versioni.html partendo dalle
notifiche.html della copia di gh-pages, così hanno la stessa testata, la stessa barra e la stessa grafica di Lega e Stadio.

Uso:
  python3 rilascio/versioni/crea_pagine.py COPIA_GH_PAGES                 scrive le due pagine nella copia (rilascio)
  python3 rilascio/versioni/crea_pagine.py COPIA_GH_PAGES --lab           le scrive in rilascio/versioni/pagine/ (prova nel Lab)
Il contenuto lo disegna versioni.js leggendo versioni.json: per una versione nuova basta aggiornare versioni.json
(rilascio/versioni/aggiungi.py), non le pagine.
"""
import pathlib, re, sys

QUI = pathlib.Path(__file__).resolve().parent
A = sys.argv[1:]
if not A:
    sys.exit(__doc__)
GH = pathlib.Path(A[0])
OUT = QUI / "pagine" if "--lab" in A else GH

for rel, su in (("girrr", "../"), ("stadio/girrr", "../../")):
    t = (GH / rel / "notifiche.html").read_text(encoding="utf-8")
    t = re.sub(r"<title>[^<]*</title>", "<title>Versioni · O Girrr</title>", t, count=1)
    t = t.replace('data-v53="notifications"', 'data-v53="versioni"', 1)
    t = re.sub(r"<h1>Notifiche</h1>", "<h1>Versioni</h1>", t, count=1)
    t = re.sub(r'<div class="tag">[^<]*</div>', '<div class="tag">Tutta la storia di O Girrr, versione per versione.</div>', t, count=1)
    i, j = t.find("<main"), t.find("</main>")
    if i < 0 or j < 0:
        sys.exit(f"{rel}/notifiche.html: manca <main>")
    t = t[:i] + '<main class="v53"><div id="versioni" style="margin-top:12px"></div>' + t[j:]
    t = re.sub(r'<script src="[./]*push\.js" defer></script>\n?', "", t)
    if "versioni.js" not in t:
        k = t.lower().find("</head>")
        t = t[:k] + f'<script src="{su}versioni.js" defer></script>\n' + t[k:]
    dest = OUT / rel / "versioni.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(t, encoding="utf-8")
    print("scritta", dest)
