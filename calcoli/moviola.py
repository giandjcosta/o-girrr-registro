#!/usr/bin/env python3
"""Moviola di Girrr Sport: gli episodi di ogni giornata già giocata, decisi una volta sola.

Legge data.json (calendario in "cal.lega", voti in "votes", nomi in "P", rose in "teams") e formazioni.json del sito.
Scrive moviola.json, che la tab Moviola legge così com'è (non ricalcola niente).
Uso:  python3 calcoli/moviola.py [data.json] [formazioni.json] [moviola.json] [--rigenera]

Regole (le stesse del Lab del 23 ottobre):
  - Al massimo 3 episodi per giornata, per priorità: rosso, rigore sbagliato, autogol, rigore parato,
    partita vinta per meno di 1 punto (i pareggi no).
  - Verdetto fisso per tipo: rosso → Rosso confermato; rigori e autogol → Regolare; partita sul filo → Da rivedere.
  - Testo scelto tra le varianti in modo stabile (stessa giornata, stesso tipo e stesso giocatore danno lo stesso testo).
  - La squadra del giocatore viene dalla formazione di quella giornata (titolari e panchina). Se non si ricava,
    l'episodio non esce, finisce tra gli "scartati" e lo script lo scrive nell'output.
  - Una giornata già scritta non cambia più, anche se i voti vengono corretti dopo. Con --rigenera si riscrive tutto.
Solo le giornate con tutti i risultati entrano. Non scrive nel database.
"""
import json, re, sys
from datetime import date
from pathlib import Path

QUI = Path(__file__).resolve().parent
ARG = [a for a in sys.argv[1:] if not a.startswith("--")]
RIGENERA = "--rigenera" in sys.argv
DATI = Path(ARG[0]) if len(ARG) > 0 else QUI.parent / "data.json"
FORM = Path(ARG[1]) if len(ARG) > 1 else QUI.parent / "formazioni.json"
USCITA = Path(ARG[2]) if len(ARG) > 2 else QUI / "moviola.json"

TIPI = {
    "rosso": ("Rosso diretto", "Rosso confermato", [
        "{G} lascia {S} in dieci: l'arbitro non ha dubbi e mostra il rosso. Le immagini confermano, per {A} un problema in più.",
        "Intervento in ritardo di {G} e cartellino rosso. Rivisto al rallentatore, l'episodio è netto: {S} resta in inferiorità.",
        "Espulsione per {G}: la squadra di {A} finisce la partita con un uomo in meno. Il replay dà ragione al direttore di gara."]),
    "sbagliato": ("Rigore sbagliato", "Regolare", [
        "{G} va sul dischetto e non trova la porta. Il rigore era netto, l'errore pure: sulla panchina di {A} nessuno ci crede.",
        "Rigore concesso a {S}, sul pallone va {G}. Tiro debole, l'occasione sfuma. Nessun dubbio sul fischio, tanti sull'esecuzione.",
        "Dal replay il contatto c'è: rigore giusto. Poi però {G} lo calcia male e {S} resta a bocca asciutta.",
        "Il dischetto tradisce {G}. Il fallo era evidente, il rigore anche, il gol no: dalle parti di {A} si mastica amaro."]),
    "autogol": ("Autogol", "Regolare", [
        "Cross teso in area, {G} prova a spazzare e la mette nella propria porta. Rivista l'azione, la deviazione è sua.",
        "Sfortuna per {G}: tocco decisivo nella sua porta. Nessun fallo prima, il gol è valido e {S} lo paga caro.",
        "La moviola non lascia scampo: l'ultimo tocco è di {G}. Autogol regolare, e sulla panchina di {A} cala il silenzio."]),
    "parato": ("Rigore parato", "Regolare", [
        "{G} intuisce, si allunga e para il rigore. Al replay i piedi sono sulla linea: tutto regolare, e che parata per {S}.",
        "Rigore contro {S}, ma {G} ci arriva. Nessun movimento in anticipo: la parata è buona e la panchina di {A} esulta.",
        "Dal dischetto parte il tiro, {G} lo respinge. Controllato il posizionamento: regolare. Una parata che vale come un gol."]),
    "stretta": ("Partita decisa sul filo", "Da rivedere", [
        "{C} {R} {O}: finisce {P}, decisa da un soffio. Basta un episodio per cambiare tutto, e in studio se ne parlerà a lungo.",
        "Un dettaglio separa {C} e {O}: {R} e punteggio di {P}. Festa per {AC}, rabbia per {AO}: c'è chi chiede di rivedere tutto.",
        "La più tirata della giornata: {C}–{O} {R}, con un punteggio di {P}. Partita da rivedere azione per azione."]),
}
PRIORITA = ["rosso", "sbagliato", "autogol", "parato", "stretta"]


def tipo(voce):
    if re.search(r"espuls|\brosso\b", voce, re.I): return "rosso"
    if "rigore sbagliato" in voce: return "sbagliato"
    if "autogol" in voce: return "autogol"
    if "rigore parato" in voce: return "parato"
    return None


def hash31(s):   # come mvH del Lab: h = h*31 + codice del carattere, a 32 bit
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) & 0xFFFFFFFF
    return h


def num(x):
    return (str(int(x)) if float(x) == int(x) else str(x)).replace(".", ",")


def allenatori(squadra, nomi):
    return [n.strip() for n in nomi.get(squadra, squadra).split("&")]


def giornata(G, d, form, nomi):
    sa = str(G["sa"]); V, P = d.get("votes", {}), d.get("P", {})
    F = form.get(sa) or {}
    chi = {}
    for t, f in F.items():
        for pid in (f.get("tit") or []) + (f.get("pan") or []):
            chi[str(pid)] = t
    rosa = {str(p["id"]) for t in d.get("teams", []) for p in t.get("pl", [])} | set(chi)   # i giocatori della lega
    cand, scartati = [], []
    for pid, gg in V.items():
        v = gg.get(sa)
        if not v or pid not in P or pid not in rosa:
            continue
        for voce in v.get("b") or []:
            k = tipo(voce)
            if not k:
                continue
            if pid not in chi:
                scartati.append({"tipo": k, "giocatore": P[pid]["n"], "id": pid, "motivo": "squadra non ricavabile dalla formazione"})
                continue
            cand.append({"k": k, "g": P[pid]["n"], "s": chi[pid], "id": pid})
    for m in G["m"]:
        if m[4] == "-":
            continue
        r = m[4].split("-")
        if r[0] == r[1] or abs(m[1] - m[2]) >= 1:
            continue
        cand.append({"k": "stretta", "c": m[0], "o": m[3], "r": m[4], "p": num(m[1]) + " a " + num(m[2]), "id": m[0] + m[3]})
    cand.sort(key=lambda e: (PRIORITA.index(e["k"]), (e.get("g") or e.get("c")).casefold()))
    out = []
    for e in cand[:3]:
        titolo, verdetto, varianti = TIPI[e["k"]]
        x = varianti[hash31("%d:%s:%s" % (G["n"], e["k"], e["id"])) % len(varianti)]
        if e["k"] == "stretta":
            ac, ao = allenatori(e["c"], nomi), allenatori(e["o"], nomi)
            x = x.replace("{C}", e["c"]).replace("{O}", e["o"]).replace("{R}", e["r"]).replace("{P}", e["p"])
            x = x.replace("{AC}", " e ".join(ac)).replace("{AO}", " e ".join(ao))
            out.append({"tipo": e["k"], "titolo": titolo, "verdetto": verdetto, "testo": x,
                        "casa": e["c"], "ospite": e["o"], "allenatori_casa": ac, "allenatori_ospite": ao})
        else:
            a = allenatori(e["s"], nomi)
            x = x.replace("{G}", e["g"]).replace("{S}", e["s"]).replace("{A}", " e ".join(a))
            out.append({"tipo": e["k"], "titolo": titolo, "verdetto": verdetto, "testo": x,
                        "giocatore": e["g"], "squadra": e["s"], "allenatori": a})
    return {"sa": G["sa"], "scritta": date.today().isoformat(), "episodi": out, "scartati": scartati}


def main():
    d = json.loads(DATI.read_text(encoding="utf-8"))
    form = json.loads(FORM.read_text(encoding="utf-8")) if FORM.exists() else {}
    nomi = json.loads((QUI / "nomi.json").read_text(encoding="utf-8"))
    prima = {} if RIGENERA or not USCITA.exists() else json.loads(USCITA.read_text(encoding="utf-8"))
    G = prima.get("giornate", {})
    giocate = [g for g in d["cal"]["lega"] if g["m"] and all(m[4] and m[4] != "-" for m in g["m"])]
    for g in giocate:
        n = str(g["n"])
        if n in G:
            print("Giornata %s: già scritta il %s, non cambia" % (n, G[n]["scritta"]))
            continue
        G[n] = giornata(g, d, form, nomi)
        x = G[n]
        print("Giornata %s: %d episodi%s" % (n, len(x["episodi"]), "".join("\n  - " + e["titolo"] + ": " + (e.get("giocatore") or e["casa"] + "–" + e["ospite"]) for e in x["episodi"])))
        for s in x["scartati"]:
            print("  ! SCARTATO %s di %s (giornata %s): %s" % (TIPI[s["tipo"]][0].lower(), s["giocatore"], n, s["motivo"]))
    nuovo = {"giocate": [g["n"] for g in giocate], "giornate": {k: G[k] for k in sorted(G, key=int)}}
    testo = json.dumps(nuovo, ensure_ascii=False, indent=1) + "\n"
    if USCITA.exists() and USCITA.read_text(encoding="utf-8") == testo:
        print("moviola.json invariato")
        return
    USCITA.write_text(testo, encoding="utf-8")
    print("scritto", USCITA)


if __name__ == "__main__":
    main()
