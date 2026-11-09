#!/usr/bin/env python3
"""Rilascio della 5.6 (Claude, 9 novembre 2026). Mette tutta la 5.6 in una copia locale di gh-pages. NON fa commit né push.

Uso:
  python3 rilascio/rilascio56.py COPIA_GH_PAGES           prova a vuoto
  python3 rilascio/rilascio56.py COPIA_GH_PAGES --vai     scrive
  aggiungi --senza-push per lasciare fuori le notifiche sul telefono (se il database non è pronto)

Fa:
  1. copia offline e scorciatoie (rilascio/offline/applica.py: sw.js, offline.js, apri.html, manifest, offline.js nelle pagine);
  2. copia nella radice versioni.json, versioni.js, cerca.js, condividi.js e push.js;
  3. crea girrr/versioni.html e stadio/girrr/versioni.html (rilascio/versioni/crea_pagine.py);
  4. aggiunge gli script: versioni.js nelle due Home e nelle due Notifiche, cerca.js nello Spogliatoio, condividi.js in Tabellone e Giornale,
     push.js nelle due Notifiche.
Si può rilanciare: dove lo script c'è già non si aggiunge.
"""
import pathlib, shutil, subprocess, sys

QUI = pathlib.Path(__file__).resolve().parent
A = sys.argv[1:]
if not A:
    sys.exit(__doc__)
GH = pathlib.Path(A[0]); VAI = "--vai" in A; PUSH = "--senza-push" not in A
if not (GH / "data.json").exists():
    sys.exit(f"{GH} non sembra una copia di gh-pages")

subprocess.run([sys.executable, str(QUI / "offline" / "applica.py"), str(GH)] + (["--vai"] if VAI else []), check=True)

FILE = {"versioni.json": QUI / "versioni" / "versioni.json", "versioni.js": QUI / "versioni" / "versioni.js",
        "cerca.js": QUI / "cerca" / "cerca.js", "condividi.js": QUI / "condividi" / "condividi.js"}
if PUSH:
    FILE["push.js"] = QUI / "push" / "push.js"
for nome, src in FILE.items():
    if not (GH / nome).exists() or (GH / nome).read_bytes() != src.read_bytes():
        print("  copia  ", nome)
        if VAI:
            shutil.copyfile(src, GH / nome)

if VAI:
    subprocess.run([sys.executable, str(QUI / "versioni" / "crea_pagine.py"), str(GH)], check=True)
else:
    print("  pagina  girrr/versioni.html, stadio/girrr/versioni.html")

SCRIPT = [("versioni.js", ["girrr/index.html", "stadio/girrr/index.html", "girrr/notifiche.html", "stadio/girrr/notifiche.html"]),
          ("cerca.js", ["index.html"]),
          ("condividi.js", ["girrr/tabellone.html", "stadio/girrr/tabellone.html", "girrr/giornale.html", "stadio/girrr/giornale.html"])]
if PUSH:
    SCRIPT.append(("push.js", ["girrr/notifiche.html", "stadio/girrr/notifiche.html"]))
for nome, pagine in SCRIPT:
    for rel in pagine:
        p = GH / rel
        t = p.read_text(encoding="utf-8")
        if nome in t:
            continue
        su = "../" * (len(pathlib.Path(rel).parts) - 1)
        k = t.lower().find("</head>")
        print(f"  script  {nome} in {rel}")
        if VAI:
            p.write_text(t[:k] + f'<script src="{su}{nome}" defer></script>\n' + t[k:], encoding="utf-8")
print("fatto" if VAI else "prova a vuoto: aggiungi --vai per scrivere")
