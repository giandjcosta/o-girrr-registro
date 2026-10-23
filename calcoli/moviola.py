#!/usr/bin/env python3
"""Moviola di Girrr Sport: gli episodi di ogni giornata giocata, uguali a quelli della tab Moviola dell'app.

Legge:  data.json del sito (voti votes[id][sa].b, calendario cal.lega, rose teams) e, se c'è, formazioni.json (chi era in campo)
Scrive: calcoli/moviola.json  -  poi post_curva.py ne fa il post "Moviola" di Girrr Sport (solo l'episodio principale, il primo)
Uso:    python3 calcoli/moviola.py data.json [formazioni.json] [uscita.json]

Stessa logica della tab (lab/index.html, funzione mvEpisodi): al massimo 3 episodi per giornata, per priorità
rosso, rigore sbagliato, autogol, rigore parato, partita vinta per meno di 1 punto (i pareggi no). Verdetto fisso per tipo.
Testo scelto in modo stabile tra le varianti: stessa giornata e stesso giocatore danno sempre lo stesso testo.
Se si cambiano i testi qui, vanno cambiati anche in MVT del Lab (e viceversa): la prova prove/prova_moviola.py controlla che siano uguali.
Formato di moviola.json:
  {"giornate": [{"n": 4, "sa": 8, "pub": 1792500000000, "episodi": [{"tipo": "sbagliato", "t": "Rigore sbagliato", "v": "Regolare", "x": "...",
                 "g": "Giocatore", "s": "Squadra", "c": "", "o": ""}]}]}      (giornata senza episodi: "episodi": [])
"""
import json, re, sys, unicodedata
from pathlib import Path

QUI = Path(__file__).resolve().parent
NOMI = json.loads((QUI / "nomi.json").read_text(encoding="utf-8"))

TESTI = {
 'rosso': dict(t='Rosso diretto', v='Rosso confermato', x=[
  "{G} lascia {S} in dieci: l'arbitro non ha dubbi e mostra il rosso. Le immagini confermano, per {A} un problema in più.",
  "Intervento in ritardo di {G} e cartellino rosso. Rivisto al rallentatore, l'episodio è netto: {S} resta in inferiorità.",
  "Espulsione per {G}: la squadra di {A} finisce la partita con un uomo in meno. Il replay dà ragione al direttore di gara.",
 ]),
 'sbagliato': dict(t='Rigore sbagliato', v='Regolare', x=[
  "{G} va sul dischetto e non trova la porta. Il rigore era netto, l'errore pure: sulla panchina di {A} nessuno ci crede.",
  "Rigore concesso a {S}, sul pallone va {G}. Tiro debole, l'occasione sfuma. Nessun dubbio sul fischio, tanti sull'esecuzione.",
  "Dal replay il contatto c'è: rigore giusto. Poi però {G} lo calcia male e {S} resta a bocca asciutta.",
  "Il dischetto tradisce {G}. Il fallo era evidente, il rigore anche, il gol no: dalle parti di {A} si mastica amaro.",
 ]),
 'autogol': dict(t='Autogol', v='Regolare', x=[
  "Cross teso in area, {G} prova a spazzare e la mette nella propria porta. Rivista l'azione, la deviazione è sua.",
  "Sfortuna per {G}: tocco decisivo nella sua porta. Nessun fallo prima, il gol è valido e {S} lo paga caro.",
  "La moviola non lascia scampo: l'ultimo tocco è di {G}. Autogol regolare, e sulla panchina di {A} cala il silenzio.",
 ]),
 'parato': dict(t='Rigore parato', v='Regolare', x=[
  "{G} intuisce, si allunga e para il rigore. Al replay i piedi sono sulla linea: tutto regolare, e che parata per {S}.",
  "Rigore contro {S}, ma {G} ci arriva. Nessun movimento in anticipo: la parata è buona e la panchina di {A} esulta.",
  "Dal dischetto parte il tiro, {G} lo respinge. Controllato il posizionamento: regolare. Una parata che vale come un gol.",
 ]),
 'stretta': dict(t='Partita decisa sul filo', v='Da rivedere', x=[
  "{C} {R} {O}: finisce {P}, decisa da un soffio. Basta un episodio per cambiare tutto, e in studio se ne parlerà a lungo.",
  "Un dettaglio separa {C} e {O}: {R} e punteggio di {P}. Festa per {AC}, rabbia per {AO}: c'è chi chiede di rivedere tutto.",
  "La più tirata della giornata: {C}–{O} {R}, con un punteggio di {P}. Partita da rivedere azione per azione.",
 ]),
}
PRIORITA = {"rosso": 0, "sbagliato": 1, "autogol": 2, "parato": 3, "stretta": 4}


def h(s):
    """Stesso hash della tab (mvH): somma *31 sui caratteri UTF-16, a 32 bit."""
    x = 0
    b = s.encode("utf-16-le")
    for i in range(0, len(b), 2):
        x = (x * 31 + int.from_bytes(b[i:i + 2], "little")) & 0xFFFFFFFF
    return x


def allenatori(t):
    return NOMI.get(t, t).replace(" & ", " e ")


def num(v):
    """Numero scritto come in JavaScript (72 e non 72.0), con la virgola."""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).replace(".", ",")


def ordine(s):
    """Ordine alfabetico come localeCompare: senza accenti e maiuscole, a parità prima le minuscole."""
    base = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return (base.casefold(), s.swapcase())


def tipo(b):
    if re.search(r"espuls|\brosso\b", b, re.I):
        return "rosso"
    for k, r in (("sbagliato", "rigore sbagliato"), ("autogol", "autogol"), ("parato", "rigore parato")):
        if r in b:
            return k
    return None


def giocate(D):
    return [g for g in (D.get("cal") or {}).get("lega") or [] if any(m[4] != "-" for m in g["m"])]


def episodi(D, F, G):
    sa = str(G["sa"])
    V, P, FS = D.get("votes") or {}, D.get("P") or {}, (F or {}).get(sa)
    chi = {}
    for t in D.get("teams") or []:
        ids = (FS[t["name"]].get("tit") or []) + (FS[t["name"]].get("pan") or []) if FS and FS.get(t["name"]) else [p["id"] for p in t.get("pl") or []]
        for i in ids:
            chi[str(i)] = t["name"]
    ep = []
    for i in sorted(chi, key=lambda k: (0, int(k), "") if k.isdigit() else (1, 0, k)):   # ordine delle chiavi come in JavaScript
        v = (V.get(i) or {}).get(sa)
        if not v or i not in P:
            continue
        for b in v.get("b") or []:
            k = tipo(b)
            if k:
                ep.append(dict(k=k, g=P[i]["n"], s=chi[i], id=i))
    for m in G["m"]:
        if m[4] == "-":
            continue
        r = m[4].split("-")
        if r[0] == r[1] or abs(m[1] - m[2]) >= 1:
            continue
        ep.append(dict(k="stretta", c=m[0], o=m[3], r=m[4], p=num(m[1]) + " a " + num(m[2]), id=m[0] + m[3]))
    ep.sort(key=lambda e: (PRIORITA[e["k"]], ordine(e.get("g") or e.get("c"))))
    out = []
    for e in ep[:3]:
        T = TESTI[e["k"]]
        x = T["x"][h(f"{G['n']}:{e['k']}:{e['id']}") % len(T["x"])]
        s, c, o = e.get("s", ""), e.get("c", ""), e.get("o", "")
        for a, b in (("{G}", e.get("g", "")), ("{S}", s), ("{A}", allenatori(s) if s else ""), ("{C}", c), ("{O}", o), ("{R}", e.get("r", "")),
                     ("{P}", e.get("p", "")), ("{AC}", allenatori(c) if c else ""), ("{AO}", allenatori(o) if o else "")):
            x = x.replace(a, b)
        out.append(dict(tipo=e["k"], t=T["t"], v=T["v"], x=x, g=e.get("g", ""), s=s, c=c, o=o))
    return out


def calcola(D, F=None):
    return dict(giornate=[dict(n=G["n"], sa=G["sa"], pub=G.get("_pub"), episodi=episodi(D, F, G)) for G in giocate(D)])


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit("Uso: python3 calcoli/moviola.py data.json [formazioni.json] [uscita.json]")
    D = json.loads(Path(a[0]).read_text(encoding="utf-8"))
    fz = Path(a[1]) if len(a) > 1 else None
    F = json.loads(fz.read_text(encoding="utf-8")) if fz and fz.exists() else {}
    uscita = Path(a[2]) if len(a) > 2 else QUI / "moviola.json"
    M = calcola(D, F)
    uscita.write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")
    print("moviola.json scritto:", len(M["giornate"]), "giornate,", sum(len(g["episodi"]) for g in M["giornate"]), "episodi")


if __name__ == "__main__":
    main()
