#!/usr/bin/env python3
"""Pagina Versioni sul sito con la 5.5.1 (Claude, 9 novembre 2026). Scrive in una copia locale di gh-pages; NON fa commit né push.

Uso: python3 rilascio/versioni/rilascio551.py COPIA_GH_PAGES
Fa: versioni.js e versioni.json (senza la 5.6, che è ancora in prova) nella radice; girrr/versioni.html e
stadio/girrr/versioni.html; <script src="…/versioni.js" defer> nelle due Home (avviso delle prime 3 visite) e nelle
due Notifiche (pulsante «V5.5.1 ›» in fondo). Si può rilanciare. Alla 5.6 ci pensa rilascio56.py (versioni.json completo).
"""
import json, pathlib, shutil, subprocess, sys

QUI = pathlib.Path(__file__).resolve().parent
if len(sys.argv) < 2:
    sys.exit(__doc__)
GH = pathlib.Path(sys.argv[1])
d = json.loads((QUI / "versioni.json").read_text(encoding="utf-8"))
d["versioni"] = [x for x in d["versioni"] if x["v"] != "5.6"]
(GH / "versioni.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
shutil.copyfile(QUI / "versioni.js", GH / "versioni.js")
subprocess.run([sys.executable, str(QUI / "crea_pagine.py"), str(GH)], check=True)
for rel in ("girrr/index.html", "stadio/girrr/index.html", "girrr/notifiche.html", "stadio/girrr/notifiche.html"):
    p = GH / rel
    t = p.read_text(encoding="utf-8")
    if "versioni.js" in t:
        continue
    su = "../" * (len(pathlib.Path(rel).parts) - 1)
    k = t.lower().find("</head>")
    p.write_text(t[:k] + f'<script src="{su}versioni.js" defer></script>\n' + t[k:], encoding="utf-8")
    print("script versioni.js in", rel)
print("ultima versione sul sito:", d["versioni"][0]["v"])
