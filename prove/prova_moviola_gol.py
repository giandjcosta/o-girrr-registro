#!/usr/bin/env python3
"""Prova con dati finti degli episodi nuovi della Moviola: gol decisivo, assist decisivo, decisivo dalla panchina, limite di 4
episodi con al massimo 2 tra gol, assist e panchina. Lavora in una cartella temporanea con una copia di moviola.py: non tocca
il registro, il sito né il database.
Uso (dalla cartella del repo): python3 prove/prova_moviola_gol.py

Una giornata con tre partite. I punteggi fissano le soglie dei gol a 66 il primo e poi uno ogni 5 punti
(65,5 → 0, 66 → 1, 70,5 → 1, 71 → 2, 75,5 → 2, 76 → 3):
  Apo team 71 – WOA 70,5 (2-1)   Apo A0 gol, A1 entrato a partita in corso con gol, A2 assist: senza ognuno sarebbe 1-1.
                                 Apo A4 (panchina della formazione) gol: non può decidere, non esce.
                                 WOA B0 assist: senza, WOA perde lo stesso.
  Grodah 76 – The Blue brothers 65,5 (3-0)   Grodah C0 doppietta: senza vince lo stesso. C1 rigore parato: Regolare.
  Real Madrink 66 – stif dc 75,5 (1-2)       stif D0 doppietta: senza sarebbe 1-1. Real E0 rigore sbagliato: Regolare.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

R = Path(__file__).resolve().parent.parent
SQ = ["Apo team", "WOA", "Grodah", "The Blue brothers", "Real Madrink", "stif dc"]
ESITI = []


def ok(cond, cosa):
    ESITI.append(bool(cond))
    print(("OK   " if cond else "NO   ") + cosa)


def dati():
    P, teams, votes, F = {}, [], {}, {}
    for i, t in enumerate(SQ):
        ids = [str(100 + i * 10 + j) for j in range(6)]
        teams.append(dict(name=t, pl=[dict(id=int(x)) for x in ids]))
        for j, x in enumerate(ids):
            P[x] = dict(n=f"Giocatore{chr(65 + i)}{j}", t="Napoli", r="PDDCCA"[j])
            votes[x] = {"8": dict(v=6, f=6, b=[])}
    F["8"] = {t["name"]: dict(tit=[p["id"] for p in t["pl"][:4]], pan=[p["id"] for p in t["pl"][4:5]]) for t in teams}
    def voce(x, b, eff):
        votes[x]["8"] = dict(v=6, f=6 + eff, b=b)
    voce("100", ["1 gol"], 3); voce("101", ["subentrato", "1 gol"], 3); voce("102", ["1 assist"], 1); voce("104", ["1 gol"], 3)
    voce("103", ["subentrato"], 0)
    voce("110", ["1 assist"], 1)
    voce("120", ["2 gol"], 6); voce("121", ["1 rigore parato"], 3)
    voce("150", ["2 gol"], 6); voce("140", ["1 rigore sbagliato"], -3)
    lega = [dict(n=1, sa=8, m=[["Apo team", 71, 70.5, "WOA", "2-1"], ["Grodah", 76, 65.5, "The Blue brothers", "3-0"],
                               ["Real Madrink", 66, 75.5, "stif dc", "1-2"]])]
    return dict(teams=teams, P=P, votes=votes, cal=dict(lega=lega), sa={}, ps={}), F


def gira(tmp, manuale):
    C = tmp / "calcoli"
    (C / "moviola-manuale.json").write_text(json.dumps(manuale, ensure_ascii=False), encoding="utf-8")
    out = C / "moviola.json"
    if out.exists():
        out.unlink()
    subprocess.check_call([sys.executable, str(C / "moviola.py"), str(tmp / "data.json"), str(tmp / "formazioni.json"), str(out)],
                          stdout=subprocess.DEVNULL)
    return json.loads(out.read_text(encoding="utf-8"))["giornate"]["1"]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="prova-moviola-gol-"))
    (tmp / "calcoli").mkdir()
    for f in ("moviola.py", "nomi.json"):
        shutil.copy(R / "calcoli" / f, tmp / "calcoli" / f)
    d, F = dati()
    (tmp / "data.json").write_text(json.dumps(d), encoding="utf-8")
    (tmp / "formazioni.json").write_text(json.dumps(F), encoding="utf-8")

    G = gira(tmp, [])
    A = {(e["tipo"], e.get("giocatore")): e for e in G["automatici"]}
    vis = [(e["tipo"], e.get("giocatore"), e["verdetto"]) for e in G["episodi"]]
    print("   mostrati:", vis)
    ok(A.get(("gol", "GiocatoreA0"), {}).get("verdetto") == "Ha deciso la partita", "gol che cambia il risultato: Gol decisivo, Ha deciso la partita")
    ok(A.get(("panchina", "GiocatoreA1"), {}).get("titolo") == "Decisivo dalla panchina", "entrato a partita in corso e decisivo: Decisivo dalla panchina")
    ok(A.get(("assist", "GiocatoreA2"), {}).get("titolo") == "Assist decisivo", "assist che cambia il risultato: Assist decisivo")
    ok(not any(e.get("giocatore") == "GiocatoreA4" for e in G["automatici"]), "gol di chi parte dalla panchina della formazione: non esce")
    ok(not any(e.get("giocatore") in ("GiocatoreB0", "GiocatoreC0") for e in G["automatici"]), "gol e assist che non cambiano il risultato: non escono")
    dop = A.get(("gol", "GiocatoreF0"), {})
    ok(dop.get("verdetto") == "Ha deciso la partita" and "doppietta" in dop.get("testo", "") and "punt" not in dop.get("testo", ""),
       "doppietta decisiva: il testo dice doppietta e non parla di punti")
    ok(len(G["episodi"]) == 4, "al massimo 4 episodi mostrati")
    ok(sum(e["tipo"] in ("gol", "assist", "panchina") for e in G["episodi"]) == 2, "al massimo 2 tra gol, assist e panchina")
    ok(vis == [("gol", "GiocatoreF0", "Ha deciso la partita"), ("panchina", "GiocatoreA1", "Ha deciso la partita"),
               ("parato", "GiocatoreC1", "Regolare"), ("sbagliato", "GiocatoreE0", "Regolare")],
       "ordine: prima chi pesa di più (doppietta), poi panchina prima del gol a parità, poi il rigore parato (sposta un gol) e quello sbagliato (nessuno)")

    G = gira(tmp, [{"giornata": 1, "tipo": "gol", "giocatore": "GiocatoreD1", "squadra": "The Blue brothers",
                    "testo": "Gol annullato e poi convalidato dopo il controllo: al replay la posizione è buona."}])
    vis = [(e["tipo"], e.get("giocatore"), e["verdetto"]) for e in G["episodi"]]
    print("   con la voce a mano:", vis)
    ok(len(G["episodi"]) == 4 and ("gol", "GiocatoreD1", "Regolare") in vis, "voce a mano di tipo gol: entra sempre, Regolare")
    ok(sum(e["tipo"] in ("gol", "assist", "panchina") and not e.get("manuale") for e in G["episodi"]) == 2,
       "con la voce a mano restano al massimo 2 automatici tra gol, assist e panchina")

    shutil.rmtree(tmp)
    print("\nTutto a posto." if all(ESITI) else f"\n{ESITI.count(False)} controlli NON passati.")
    sys.exit(0 if all(ESITI) else 1)


if __name__ == "__main__":
    main()
