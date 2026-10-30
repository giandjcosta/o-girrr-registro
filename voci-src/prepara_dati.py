#!/usr/bin/env python3
"""Prepara i dati della puntata radio dalla giornata chiusa, senza interventi a mano.

Uso:  python3 prepara_dati.py SITO EVENTI [--segna]
  SITO    cartella del ramo gh-pages del sito (data.json, girrr/dati/lab-dati.json, girrr/voci/archivio.json)
  EVENTI  calcoli/eventi.json del main del sito (conferenze, promesse, sfide e Derby dal database)
  --segna dopo la puntata riuscita: segna i Derby annunciati (girrr/voci/annunciate.json del sito)
Scrive voci-src/dati.json, conferenze.json e (se serve) svuota curva.json. Stampa  giornata=N  per GitHub Actions
(giornata= vuoto se non c'è niente da fare: giornata non chiusa, o puntata già in archivio).
"""
import json, re, sys
from pathlib import Path
QUI = Path(__file__).resolve().parent
A = [x for x in sys.argv[1:] if not x.startswith("--")]
SITO, EV = Path(A[0]), Path(A[1])
ANN = SITO / "girrr/voci/annunciate.json"   # sta nel sito, così il workflow non deve scrivere nel registro

def carica(p, d=None):
    try: return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception: return d

def chiusa(d):
    lega = d["cal"]["lega"]
    ch = [r for r in lega if r["m"] and all(m[4] and m[4] != "-" for m in r["m"])]
    return max(ch, key=lambda r: r["n"]) if ch else None

def main():
    d = carica(SITO / "data.json")
    r = chiusa(d)
    if not r: print("giornata="); return
    n, sa = r["n"], r.get("sa")
    arc = carica(SITO / "girrr/voci/archivio.json", [])
    if any(re.search(rf"Giornata {n}\b", (e.get("tag") or "") + " " + (e.get("titolo") or "")) for e in arc):
        print("giornata="); return          # già fatta
    if "--segna" in sys.argv:
        ev = carica(EV, [])
        k = {f"derby:{e['k']}" for e in ev if e.get("tipo") == "derby"}
        ANN.write_text(json.dumps(sorted(k | set(carica(ANN, []))), indent=1), encoding="utf-8")
        print(f"giornata={n}"); return
    ev = carica(EV, [])
    dati = carica(SITO / "girrr/dati/lab-dati.json")
    cp_ = [c for c in d["cal"].get("cup", []) if c.get("sa") == sa and c.get("m")]
    if cp_ and not all(m[5] and m[5] != "-" for m in cp_[-1]["m"]):
        print("giornata="); return          # la Coppa di questa giornata non è ancora chiusa: aspetto
    # Champions Cup: se ne parla solo se si è giocato nella stessa giornata di Serie A del campionato
    dati["cup"] = [c for c in d["cal"].get("cup", []) if c.get("sa") == sa and c.get("m") and all(m[5] and m[5] != "-" for m in c["m"])][-1:]
    (QUI / "dati.json").write_text(json.dumps(dati, ensure_ascii=False), encoding="utf-8")
    conf = [e for e in ev if e.get("tipo") == "conferenza" and e.get("giornata") == n]
    squadre = {}
    for e in conf:
        s = squadre.setdefault(e["team"], {"toni": []})
        s["toni"].append(e.get("tono", 1))
    for e in ev:
        if e.get("tipo") == "promessa" and e.get("giornata") == n and e.get("team") in squadre and e.get("promessa"):
            squadre[e["team"]].update({"promessa": e["promessa"], "pesa": e.get("pesa", 1), "esito": e.get("esito", "")})
    annunciate = set(carica(ANN, []))
    derby = [{"da": e["da"], "a": e["a"], "stato": "accettata", "nome": e["nome"], "annunciata": f"derby:{e['k']}" in annunciate}
             for e in ev if e.get("tipo") == "derby"]
    out = {"_come_si_usa": "Generato da prepara_dati.py (dati veri dal database del sito).", "demo": False, "giornata": n,
           "partite": [[e["team"], e.get("avversario", "")] for e in conf if e.get("avversario")],
           "squadre": squadre, "sfide_derby": derby}
    (QUI / "conferenze.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    cv = carica(QUI / "curva.json", {})
    if cv.get("giornata") != n:        # il post della Curva vale solo per la giornata per cui è stato messo
        (QUI / "curva.json").write_text(json.dumps({"_come_si_usa": "Un post vero dalla Curva per la giornata indicata in \"giornata\". Se manca o è di un'altra giornata la radio non ne parla.", "giornata": n, "post": ""}, ensure_ascii=False), encoding="utf-8")
    print(f"giornata={n}")
main()
