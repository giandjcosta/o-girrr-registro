#!/usr/bin/env python3
"""Copia offline (Claude, 9 novembre 2026): la mette in una copia locale del ramo gh-pages del sito. NON fa commit né push.

Uso:
  python3 rilascio/offline/applica.py COPIA_GH_PAGES            prova a vuoto: elenca cosa cambierebbe
  python3 rilascio/offline/applica.py COPIA_GH_PAGES --vai      scrive i file

Fa:
  1. copia sw.js e offline.js nella radice del sito (accanto a index.html e data.json);
  2. aggiunge <script src="…/offline.js" defer></script> prima di </head> in ogni pagina di Lega e Stadio,
     nello Spogliatoio (index.html) e in riepilogo.html, con il percorso relativo giusto.
Si può rilanciare: le pagine che hanno già offline.js non si toccano.
Dopo il rilascio copiare le pagine cambiate anche in ufficiale/src/sito/ (Lega in girrr/, Stadio in stadio/girrr/).
Per tornare indietro: git revert del commit su gh-pages (le copie salvate sui telefoni restano ma non fanno danni;
per toglierle del tutto si pubblica un sw.js che si cancella da solo, vedi STATO.md).
"""
import pathlib, shutil, sys

QUI = pathlib.Path(__file__).resolve().parent
A = sys.argv[1:]
if not A:
    sys.exit(__doc__)
GH = pathlib.Path(A[0])
VAI = "--vai" in A
if not (GH / "data.json").exists() or not (GH / "girrr").is_dir():
    sys.exit(f"{GH} non sembra una copia di gh-pages (manca data.json o girrr/)")

pagine = [GH / "index.html", GH / "riepilogo.html"] + sorted((GH / "girrr").glob("*.html")) + sorted((GH / "stadio" / "girrr").glob("*.html"))
cambi = []
for f in ("sw.js", "offline.js"):
    if not (GH / f).exists() or (GH / f).read_bytes() != (QUI / f).read_bytes():
        cambi.append(("copia", GH / f))
        if VAI:
            shutil.copyfile(QUI / f, GH / f)
for p in pagine:
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8")
    if "offline.js" in t:
        continue
    i = t.lower().find("</head>")
    if i < 0:
        print("  senza </head>, saltata:", p.relative_to(GH))
        continue
    rel = "../" * (len(p.relative_to(GH).parts) - 1)
    tag = f'<script src="{rel}offline.js" defer></script>'
    cambi.append(("pagina", p))
    if VAI:
        p.write_text(t[:i] + tag + "\n" + t[i:], encoding="utf-8")

for tipo, p in cambi:
    print(f"  {tipo:7} {p.relative_to(GH)}")
print(f"{len(cambi)} cambiamenti" + ("" if VAI else " (prova a vuoto: aggiungi --vai per scriverli)"))
