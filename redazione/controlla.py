#!/usr/bin/env python3
"""Redazione di Girrr Sport · Controllo di quello che ha scritto la redazione (Claude, 11 novembre 2026, versione 5.8).

Prima di pubblicare, controlla redazione.json (scritto da Claude seguendo ISTRUZIONI.md) contro il dossier e le regole
della lega. Se c'è anche un solo errore non pubblica niente e li elenca tutti.

Uso:  python3 redazione/controlla.py [redazione/redazione.json] [--dossier redazione/dossier.json] [--pubblica DESTINAZIONE]
Con --pubblica scrive il file controllato nella destinazione (nel Lab: lab/redazione/redazione.json; sul sito, con il «vai»
di Gianluca: girrr/dati/redazione.json di gh-pages).
"""
import json, re, sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
ARG = sys.argv[1:]


def opz(nome, predef=None):
    return ARG[ARG.index(nome) + 1] if nome in ARG else predef


FILE = Path(next((a for i, a in enumerate(ARG) if not a.startswith("--") and (i == 0 or not ARG[i - 1].startswith("--"))), QUI / "redazione.json"))
DOSSIER = Path(opz("--dossier", QUI / "dossier.json"))
DEST = opz("--pubblica")

VIETATE = re.compile(r"fantapunt|scommess|\bquot[ae]\b|puntat[ae]\b|schedin|bookmaker|totogirrr", re.I)
errori = []


def err(dove, msg):
    errori.append(f"{dove}: {msg}")


def testo(dove, t, minimo, massimo):
    if not isinstance(t, str) or not (minimo <= len(t.strip()) <= massimo):
        return err(dove, f"testo tra {minimo} e {massimo} caratteri ({len(t) if isinstance(t, str) else '—'}): {t!r}")
    t = t.strip()
    if VIETATE.search(t):
        err(dove, f"parola vietata (scommesse o Fantapunti): {t!r}")
    if not t[0].isupper() and not t[0] in "«\"'0123456789":
        err(dove, f"deve cominciare con la maiuscola: {t!r}")
    for m in re.finditer(r"·\s+(\S)", t):
        if m.group(1).islower():
            err(dove, f"dopo «·» ci vuole la maiuscola: {t!r}")
    for m in re.finditer(r"[.!?]\s+([a-zà-ù])", t):
        err(dove, f"frase che comincia con la minuscola ({m.group(0)!r}): {t!r}")
    if re.search(r"Blue brothers|Blue Brothers", t):
        err(dove, "il nome giusto è «The Blues Brothers»")


def main():
    R = json.loads(FILE.read_text(encoding="utf-8"))
    D = json.loads(DOSSIER.read_text(encoding="utf-8"))
    if R.get("giornata") != D["giornata"]:
        err("giornata", f"{R.get('giornata')} invece di {D['giornata']} (quella del dossier)")
    dom = R.get("domande") or {}
    for t in D["squadre"]:
        Q = dom.get(t)
        if not isinstance(Q, list) or len(Q) != 3:
            err(t, "servono esattamente 3 domande")
            continue
        for i, q in enumerate(Q):
            dove = f"{t} · domanda {i + 1}"
            testo(dove, q.get("q"), 20, 220)
            A = q.get("a") or []
            if len(A) != 3 or sorted(a.get("k") for a in A) != [0, 1, 2]:
                err(dove, "servono 3 risposte, una per tono (k 0 Sicuro, 1 Umile, 2 Provocatorio)")
                continue
            for a in A:
                testo(f"{dove} · risposta k{a.get('k')}", a.get("t"), 5, 80)
                if a.get("w") not in (0, 1):
                    err(dove, "w deve essere 0 o 1 (1 = è una promessa)")
                if a.get("k") == 1 and a.get("w") == 1:
                    err(dove, "la risposta umile non può essere una promessa")
    for t in dom:
        if t not in D["squadre"]:
            err(t, "squadra che non è nel dossier (usare la chiave interna, per esempio «The Blue brothers»)")
    chiavi = {x["chiave"]: x for x in D.get("da_giudicare", [])}
    for k, g in (R.get("giudizi") or {}).items():
        if not any(c.startswith(k) or k == c for c in chiavi):
            err(f"giudizio {k}", "nessuna risposta da giudicare con questa chiave nel dossier")
            continue
        for r in g.get("risposte", []):
            if r.get("k") not in (0, 1, 2) or r.get("w") not in (0, 1) or not isinstance(r.get("pubblicabile"), bool):
                err(f"giudizio {k}", "ogni risposta: k 0-2, w 0/1, pubblicabile vero o falso")
            testo(f"giudizio {k} · nota", r.get("nota", ""), 5, 160)
        if g.get("domanda_dopo"):
            testo(f"giudizio {k} · domanda successiva", g["domanda_dopo"], 20, 220)
    for c in chiavi:
        base = c
        if not any(base == k for k in (R.get("giudizi") or {})):
            err(f"giudizio {c}", "risposta scritta a mano non giudicata")
    if errori:
        print("NON PUBBLICATO. Da correggere:")
        for e in errori:
            print(" -", e)
        sys.exit(1)
    R["controllato"] = True
    print(f"Tutto a posto: {len(dom)} squadre, {len(R.get('giudizi') or {})} giudizi.")
    if DEST:
        Path(DEST).parent.mkdir(parents=True, exist_ok=True)
        Path(DEST).write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
        print("Pubblicato in", DEST)


if __name__ == "__main__":
    main()
