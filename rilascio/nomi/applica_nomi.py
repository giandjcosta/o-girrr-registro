#!/usr/bin/env python3
"""Nome mostrato «The Blues Brothers» (Claude, 9 novembre 2026, decisione di Gianluca). Scrive in una copia di gh-pages; NON fa commit né push.

La chiave interna della squadra resta «The Blue brothers» (codici di accesso, database, data.json, calcoli). Cambia ciò che si legge:
  1. nomi.js nella radice e <script src="…/nomi.js"></script> subito dopo <head> in tutte le pagine (sito, immagini disegnate, condivisioni);
  2. scripts/pdf_settimana.py: esc() scrive il nome nuovo, quindi Giornale in PDF e immagini del Tabellone (tabellone.py, pdf_giornale.py);
  3. scripts/leghe_importa.py: su Leghe il nome è già «The Blues Brothers»; l'import lo riporta alla chiave interna, così non si blocca.
Uso: python3 rilascio/nomi/applica_nomi.py COPIA_GH_PAGES [--vai]      Si può rilanciare.
"""
import pathlib, shutil, sys

QUI = pathlib.Path(__file__).resolve().parent
A = sys.argv[1:]
if not A:
    sys.exit(__doc__)
GH = pathlib.Path(A[0]); VAI = "--vai" in A
cambi = []

if not (GH / "nomi.js").exists() or (GH / "nomi.js").read_bytes() != (QUI / "nomi.js").read_bytes():
    cambi.append("copia nomi.js")
    if VAI:
        shutil.copyfile(QUI / "nomi.js", GH / "nomi.js")

pagine = [GH / "index.html", GH / "riepilogo.html"] + sorted((GH / "girrr").glob("*.html")) + sorted((GH / "stadio" / "girrr").glob("*.html"))
for p in pagine:
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8")
    if "nomi.js" in t:
        continue
    i = t.lower().find("<head")
    j = t.find(">", i) + 1 if i >= 0 else -1
    if j <= 0:
        print("  senza <head>, saltata:", p.relative_to(GH)); continue
    su = "../" * (len(p.relative_to(GH).parts) - 1)
    cambi.append(f"script nomi.js in {p.relative_to(GH)}")
    if VAI:
        p.write_text(t[:j] + f'\n<script src="{su}nomi.js"></script>' + t[j:], encoding="utf-8")

ps = GH / "scripts" / "pdf_settimana.py"
t = ps.read_text(encoding="utf-8")
ESC_A = "def esc(x):\n    return html.escape(str(x))\n"
ESC_B = ('# Nomi mostrati (Claude, 9 novembre 2026): la chiave resta «The Blue brothers», nei PDF e nelle immagini si legge il nome ufficiale.\n'
         'NOMI_MOSTRATI = {"Blue brothers": "Blues Brothers", "Blue Brothers": "Blues Brothers", "BLUE BROTHERS": "BLUES BROTHERS"}\n\n\n'
         'def nome_mostrato(x):\n    s = str(x)\n    for a, b in NOMI_MOSTRATI.items():\n        s = s.replace(a, b)\n    return s\n\n\n'
         'def esc(x):\n    return html.escape(nome_mostrato(x))\n')
if "NOMI_MOSTRATI" not in t:
    if t.count(ESC_A) != 1:
        sys.exit("pdf_settimana.py: esc() è cambiata, controlla a mano")
    cambi.append("scripts/pdf_settimana.py: esc() con il nome mostrato")
    if VAI:
        ps.write_text(t.replace(ESC_A, ESC_B), encoding="utf-8")

li = GH / "scripts" / "leghe_importa.py"
t = li.read_text(encoding="utf-8")
IMP_A = '    L = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))\n'
IMP_B = (IMP_A + '    # Nomi su Leghe diversi dalla chiave del sito (Claude, 9 novembre 2026): si riportano alla chiave interna\n'
         '    DA_LEGHE = {"The Blues Brothers": "The Blue brothers"}\n'
         '    for parte in ("lega", "coppa"):\n'
         '        for m in L.get(parte) or []:\n'
         '            for lato in ("A", "B"):\n'
         '                if isinstance(m.get(lato), dict) and m[lato].get("s") in DA_LEGHE:\n'
         '                    m[lato]["s"] = DA_LEGHE[m[lato]["s"]]\n')
if "DA_LEGHE" not in t:
    if t.count(IMP_A) != 1:
        sys.exit("leghe_importa.py: la lettura è cambiata, controlla a mano")
    cambi.append("scripts/leghe_importa.py: «The Blues Brothers» di Leghe → chiave interna")
    if VAI:
        li.write_text(t.replace(IMP_A, IMP_B), encoding="utf-8")

for c in cambi:
    print("  " + c)
print(f"{len(cambi)} cambiamenti" + ("" if VAI else " (prova a vuoto: aggiungi --vai per scriverli)"))
