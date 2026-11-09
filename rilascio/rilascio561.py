#!/usr/bin/env python3
"""Rilascio della 5.6.1 (Claude, 9 novembre 2026). Scrive in una copia locale di gh-pages; NON fa commit né push.

Uso: python3 rilascio/rilascio561.py COPIA_GH_PAGES [--vai]
Fa: versioni.js (passaggio fluido Messaggio/Changelog, pillola della versione nella Home sopra gli sponsor),
versioni.json con la 5.6.1, notifiche-lette.js nella radice e nelle due pagine Notifiche (lette rimpicciolite).
Si può rilanciare.
"""
import pathlib, shutil, sys

QUI = pathlib.Path(__file__).resolve().parent
A = sys.argv[1:]
if not A:
    sys.exit(__doc__)
GH = pathlib.Path(A[0]); VAI = "--vai" in A
FILE = {"versioni.js": QUI / "versioni" / "versioni.js", "versioni.json": QUI / "versioni" / "versioni.json",
        "notifiche-lette.js": QUI / "notifiche" / "notifiche-lette.js"}
for nome, src in FILE.items():
    if not (GH / nome).exists() or (GH / nome).read_bytes() != src.read_bytes():
        print("  copia  ", nome)
        if VAI:
            shutil.copyfile(src, GH / nome)
for rel in ("girrr/notifiche.html", "stadio/girrr/notifiche.html"):
    p = GH / rel
    t = p.read_text(encoding="utf-8")
    if "notifiche-lette.js" in t:
        continue
    su = "../" * (len(pathlib.Path(rel).parts) - 1)
    k = t.lower().find("</head>")
    print("  script  notifiche-lette.js in", rel)
    if VAI:
        p.write_text(t[:k] + f'<script src="{su}notifiche-lette.js" defer></script>\n' + t[k:], encoding="utf-8")
print("fatto" if VAI else "prova a vuoto: aggiungi --vai per scrivere")
