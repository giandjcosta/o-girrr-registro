#!/usr/bin/env python3
"""Aggiunge una versione in cima a versioni.json (Claude, 9 novembre 2026).

Prima di ogni rilascio sul sito si chiede a Gianluca che tipo di aggiornamento è:
  correzione minore  -> terza cifra   (5.6 -> 5.6.1 -> 5.6.2)          --tipo minore
  aggiornamento medio -> seconda cifra (5.6 -> 5.7 -> 5.8)             --tipo medio
  aggiornamento grande -> prima cifra  (5.x -> 6.0 -> 7.0)             --tipo grande
Il numero si calcola da solo dall'ultima versione; con --v lo si può scrivere a mano.

Uso:
  python3 rilascio/versioni/aggiungi.py --tipo minore --titolo "Correzioni" \
      --messaggio "🔧 **O Girrr 5.6.1 è online!** …" \
      --voce "Spogliatoio: la ricerca trova anche i nomi con l'accento" [--voce "Area: testo" …] \
      [--data 2026-11-10] [--file rilascio/versioni/versioni.json] [--file COPIA_GH_PAGES/versioni.json] [--prova]
Con --prova stampa la versione senza scrivere. Le voci con lo stesso «Area:» finiscono nello stesso gruppo.
"""
import argparse, datetime, json, pathlib, re, sys

QUI = pathlib.Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument("--tipo", required=True, choices=["minore", "medio", "grande"])
p.add_argument("--titolo", required=True)
p.add_argument("--messaggio", required=True)
p.add_argument("--voce", action="append", default=[])
p.add_argument("--v")
p.add_argument("--data", default=datetime.date.today().isoformat())
p.add_argument("--file", action="append")
p.add_argument("--prova", action="store_true")
a = p.parse_args()
files = [pathlib.Path(f) for f in (a.file or [QUI / "versioni.json"])]


def prossima(ultima, tipo):
    n = [int(x) for x in re.findall(r"\d+", ultima)[:3]] + [0, 0, 0]
    if tipo == "grande":
        return f"{n[0] + 1}.0"
    if tipo == "medio":
        return f"{n[0]}.{n[1] + 1}"
    return f"{n[0]}.{n[1]}.{n[2] + 1}"


d = json.loads(files[0].read_text(encoding="utf-8"))
ultima = d["versioni"][0]["v"]
v = a.v or prossima(ultima, a.tipo)
if any(x["v"] == v for x in d["versioni"]):
    sys.exit(f"La versione {v} c'è già")
gruppi = {}
for voce in a.voce:
    area, _, testo = voce.partition(":")
    if not testo:
        area, testo = "Novità", voce
    testo = testo.strip()
    testo = testo[:1].upper() + testo[1:]  # ogni voce del changelog con la maiuscola (Gianluca)
    gruppi.setdefault(area.strip(), []).append(testo)
nuova = {"v": v, "data": a.data, "tipo": a.tipo, "titolo": a.titolo, "messaggio": a.messaggio,
         "novita": [{"area": k, "voci": x} for k, x in gruppi.items()]}
print(f"{ultima} -> {v}")
print(json.dumps(nuova, ensure_ascii=False, indent=2))
if a.prova:
    sys.exit(0)
for f in files:
    dd = json.loads(f.read_text(encoding="utf-8"))
    dd["versioni"].insert(0, nuova)
    f.write_text(json.dumps(dd, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("scritta in", f)
