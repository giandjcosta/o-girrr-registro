#!/usr/bin/env python3
"""Moviola di Girrr Sport: sceglie e giudica gli episodi di ogni giornata e li scrive in moviola.json (lo legge la tab Moviola del Lab).

Legge data.json (voti con le voci `b`, calendario con punteggi e risultati) e formazioni.json (titolari e panchina di ogni giornata).
Per ogni episodio (rosso, rigore sbagliato, autogol, rigore parato) toglie il suo effetto dal punteggio della squadra e guarda
se l'esito (vittoria, pareggio, sconfitta) cambierebbe. Il valore di ogni voce e le soglie dei gol si ricavano dai dati, niente numeri a mano.
Verdetto: rosso → Rosso confermato; ha cambiato l'esito → Ha deciso la partita; partita decisa per meno di 1 punto → Da rivedere; altrimenti Regolare.
Ordine (al massimo 3): prima quelli che hanno deciso, poi per peso sul risultato, poi rosso, rigore sbagliato, autogol, rigore parato, partita sul filo.
Le giornate già scritte in moviola.json restano come sono: si scrivono solo le giornate nuove, oppure tutte con --rigenera
(o solo alcune con --rigenera 2,3).
Uso: python3 calcoli/moviola.py [data.json] [formazioni.json] [uscita.json] [--rigenera [N,M]]
"""
import json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

QUI = Path(__file__).resolve().parent
ARG, RIGENERA = [], None   # RIGENERA: None solo giornate nuove, True tutte, insieme di numeri solo quelle
_a = sys.argv[1:]
while _a:
    x = _a.pop(0)
    if x == "--rigenera":
        RIGENERA = {int(n) for n in _a.pop(0).split(",")} if _a and re.fullmatch(r"\d+(,\d+)*", _a[0]) else True
    else:
        ARG.append(x)
DATI = Path(ARG[0]) if len(ARG) > 0 else QUI.parent / "data.json"
FORM = Path(ARG[1]) if len(ARG) > 1 else QUI.parent / "formazioni.json"
USCITA = Path(ARG[2]) if len(ARG) > 2 else QUI.parent / "lab" / "moviola.json"

MGR = json.loads((QUI / "nomi.json").read_text(encoding="utf-8"))
PRIO = {"rosso": 0, "sbagliato": 1, "autogol": 2, "parato": 3, "stretta": 4}

MVT = {
 "rosso": {"t": "Rosso diretto", "x": [
  "{G} lascia {S} in dieci: l'arbitro non ha dubbi e mostra il rosso. Le immagini confermano, per {A} un problema in più.",
  "Intervento in ritardo di {G} e cartellino rosso. Rivisto al rallentatore, l'episodio è netto: {S} resta in inferiorità.",
  "Espulsione per {G}: la squadra di {A} finisce la partita con un uomo in meno. Il replay dà ragione al direttore di gara."]},
 "sbagliato": {"t": "Rigore sbagliato", "x": [
  "{G} va sul dischetto e non trova la porta. Il rigore era netto, l'errore pure: sulla panchina di {A} nessuno ci crede.",
  "Rigore concesso a {S}, sul pallone va {G}. Tiro debole, l'occasione sfuma. Nessun dubbio sul fischio, tanti sull'esecuzione.",
  "Dal replay il contatto c'è: rigore giusto. Poi però {G} lo calcia male e {S} resta a bocca asciutta.",
  "Il dischetto tradisce {G}. Il fallo era evidente, il rigore anche, il gol no: dalle parti di {A} si mastica amaro."]},
 "autogol": {"t": "Autogol", "x": [
  "Cross teso in area, {G} prova a spazzare e la mette nella propria porta. Rivista l'azione, la deviazione è sua.",
  "Sfortuna per {G}: tocco decisivo nella sua porta. Nessun fallo prima, il gol è valido e {S} lo paga caro.",
  "La moviola non lascia scampo: l'ultimo tocco è di {G}. Autogol regolare, e sulla panchina di {A} cala il silenzio."]},
 "parato": {"t": "Rigore parato", "x": [
  "{G} intuisce, si allunga e para il rigore. Al replay i piedi sono sulla linea: tutto regolare, e che parata per {S}.",
  "Rigore contro {S}, ma {G} ci arriva. Nessun movimento in anticipo: la parata è buona e la panchina di {A} esulta.",
  "Dal dischetto parte il tiro, {G} lo respinge. Controllato il posizionamento: regolare. Una parata che vale come un gol."]},
 "stretta": {"t": "Partita decisa sul filo", "x": [
  "{C} {R} {O}: finisce {P}, decisa da un soffio. Basta un episodio per cambiare tutto, e in studio se ne parlerà a lungo.",
  "Un dettaglio separa {C} e {O}: {R} e punteggio di {P}. Festa per {AC}, rabbia per {AO}: c'è chi chiede di rivedere tutto.",
  "La più tirata della giornata: {C}–{O} {R}, con un punteggio di {P}. Partita da rivedere azione per azione."]}}

# Verdetto "Ha deciso la partita": {M} è la partita col risultato, {E} cosa sarebbe successo a {S} senza l'episodio
DECISO = {
 "rosso": [
  "Il rosso a {G} cambia la partita: {S} resta in dieci e la gara gira. Finisce {M}, e con undici uomini fino alla fine {S} {E}.",
  "Espulsione netta per {G}, e da lì è un'altra partita: {M}. Per {A} è un rosso che costa il risultato.",
  "Il replay conferma il rosso a {G}, ed è l'episodio chiave di {M}. Senza quell'espulsione {S} {E}: sulla panchina di {A} lo sanno bene."],
 "sbagliato": [
  "{G} va sul dischetto e sbaglia: è l'episodio che decide {M}. Con quel pallone in rete {S} {E}, e sulla panchina di {A} resta solo il rimpianto.",
  "Il rigore era netto, l'esecuzione no. {G} si fa ipnotizzare e {S} paga tutto: finisce {M}. Con quel gol {S} {E}.",
  "Dal replay nessun dubbio sul fischio, ma il risultato lo cambia l'errore di {G}: {M}. Per {A} è il rigore che pesa di più in classifica.",
  "Partita decisa da undici metri. {G} calcia, il pallone non entra e {M} prende un'altra strada: dalle parti di {AO} si brinda, per {A} è una notte lunga."],
 "autogol": [
  "Un tocco sfortunato e la partita prende un'altra strada: l'autogol di {G} decide {M}. Senza quella deviazione {S} {E}.",
  "La moviola conferma: ultimo tocco di {G}, gol valido e risultato cambiato. Finisce {M}, e sulla panchina di {A} si riguarda il replay in silenzio.",
  "Il pallone carambola su {G} e finisce in rete: è il gol che decide {M}. Per {A} una beffa che pesa in classifica, perché senza quell'autogol {S} {E}."],
 "parato": [
  "{G} para il rigore e si prende la copertina: {M}. Senza quella parata {S} {E}, e sulla panchina di {A} lo sanno bene.",
  "Il rigore che decide la partita è quello che non entra. {G} vola, respinge e consegna il risultato a {S}: finisce {M}.",
  "Piedi sulla linea, tuffo giusto, pallone fuori: al replay la parata di {G} è regolare ed è quella che decide {M}. Per {A} vale quanto un gol.",
  "Dal dischetto parte il tiro, {G} lo respinge e cambia la giornata di {S}. Finisce {M}: senza quella parata {S} {E}, invece è festa per {A}."]}
CONTRO = {1: "avrebbe vinto", 0: "avrebbe pareggiato", -1: "avrebbe perso"}


def h(s):   # lo stesso hash del Lab: stessa giornata e stesso giocatore danno sempre lo stesso testo
    x = 0
    for ch in s:
        x = (x * 31 + ord(ch)) & 0xFFFFFFFF
    return x


def pick(a, k):
    return a[h(k) % len(a)]


def allenatori(t):
    return "Leanzino e Mario" if t == "The Blue brothers" else MGR.get(t, t)


def voci(v):
    """Le voci di `b` come {voce: quante}; "gol subiti" e "gol subito" sono la stessa voce."""
    c = defaultdict(int)
    for b in v.get("b") or []:
        m = re.match(r"(\d+) (.*)", b)
        n, k = (int(m.group(1)), m.group(2)) if m else (1, b)
        k = "gol subito" if k == "gol subiti" else k
        c[k] += n
    return c


def tipo(voce):
    if re.search(r"espuls|\brosso\b", voce, re.I):
        return "rosso"
    return {"rigore sbagliato": "sbagliato", "autogol": "autogol", "rigore parato": "parato"}.get(voce)


def valori_voci(votes):
    """Quanto vale ogni voce sul fantavoto, ricavato da fantavoto meno voto. Si parte dalle righe con una sola voce sconosciuta
    e si prende il valore più frequente (i gialli non sono tra le voci e tolgono mezzo punto a qualche riga: a parità vince il più alto)."""
    righe = []
    for vs in votes.values():
        for v in vs.values():
            if v.get("v") is None or v.get("f") is None:
                continue
            righe.append((voci(v), v["f"] - v["v"]))
    def stima(k, noto):   # il valore di k dalle righe dove tutte le altre voci sono già note
        cc = Counter(round((r - sum(noto[j] * n for j, n in c.items() if j != k)) / c[k] * 2) / 2
                     for c, r in righe if k in c and all(j in noto for j in c if j != k))
        return max(cc, key=lambda x: (cc[x], x)) if cc else None
    noto, tutte = {"senza voto": 0.0}, {k for c, _ in righe for k in c}
    while True:   # prima le voci che si ricavano da sole, poi quelle che dipendono da loro
        nuove = {k: stima(k, noto) for k in tutte - set(noto)}
        nuove = {k: x for k, x in nuove.items() if x is not None}
        if not nuove:
            break
        noto.update(nuove)
    return {k: (stima(k, noto) if k != "senza voto" else 0.0) for k in noto}   # ultimo giro con tutte le altre note


def gol(p, base, passo):
    return 0 if p < base else int((p - base) // passo) + 1


def soglie(lega):
    """Soglia del primo gol e punti per ogni gol in più, ricavati dai risultati giocati: la coppia (a mezzo punto) che li spiega tutti.
    Se ce ne sono più di una si sceglie quella con i numeri più tondi; se nessuna li spiega, None (e nessun episodio "decide")."""
    gi = [(p, int(g)) for x in lega for m in x["m"] if m[4] and m[4] != "-"
          for p, g in ((m[1], m[4].split("-")[0]), (m[2], m[4].split("-")[1]))]
    ok = []
    for b2 in range(100, 181):
        for s2 in range(2, 21):
            b, s = b2 / 2, s2 / 2
            if all(gol(p, b, s) == g for p, g in gi):
                ok.append((b % 1 != 0, s % 1 != 0, b, s))
    return min(ok)[2:] if ok else None


def ris(r):   # "2-2" con il trattino che non va a capo
    return r.replace("-", "\u2011")


def esito(a, b):
    return (a > b) - (a < b)


def in_campo(sa, F, V):
    """Chi gioca per chi in quella giornata e se il suo voto conta: titolare con voto, oppure panchinaro che entra al posto
    di un titolare del suo ruolo senza voto (in ordine di panchina). Senza formazione: squadra dalla rosa, conta sconosciuto (None)."""
    out = {}
    if F is None:
        return None
    for t, x in F.items():
        manca = Counter()
        for i in x.get("tit") or []:
            v = (V.get(str(i)) or {}).get(sa)
            gioca = bool(v) and v.get("v") is not None
            out[str(i)] = (t, gioca)
            if not gioca:
                manca[RUOLO.get(str(i), "?")] += 1
        for i in x.get("pan") or []:
            v = (V.get(str(i)) or {}).get(sa)
            r = RUOLO.get(str(i), "?")
            entra = bool(v) and v.get("v") is not None and manca[r] > 0
            if entra:
                manca[r] -= 1
            out[str(i)] = (t, entra)
    return out


def episodi(G, d, F, val, sg):
    sa = str(G["sa"])
    V, P = d.get("votes") or {}, d.get("P") or {}
    chi = in_campo(sa, F, V)
    if chi is None:
        chi = {str(p["id"]): (t["name"], None) for t in d.get("teams") or [] for p in t.get("pl") or []}
    partite = [m for m in G["m"] if m[4] and m[4] != "-"]
    def partita(t):
        for m in partite:
            if t in (m[0], m[3]):
                return m
    ep = []
    for pid, (sq, conta) in chi.items():
        v = (V.get(pid) or {}).get(sa)
        if not v or pid not in P:
            continue
        for voce, n in voci(v).items():
            k = tipo(voce)
            if not k:
                continue
            e = dict(k=k, g=P[pid]["n"], s=sq, id=pid, deciso=False, peso=0.0, gol=0)
            m = partita(sq)
            if m:
                casa = m[0] == sq
                mio, suo = (m[1], m[2]) if casa else (m[2], m[1])
                gm, gs = map(int, m[4].split("-")) if casa else map(int, m[4].split("-")[::-1])
                e.update(o=m[3] if casa else m[0], m=m, sul_filo=gm != gs and abs(m[1] - m[2]) < 1)
                eff = val.get(voce)
                if conta and eff and sg:
                    senza = gol(mio - eff * n, *sg)
                    e["peso"] = abs(eff * n)
                    e["gol"] = abs(gm - senza)
                    if esito(senza, gs) != esito(gm, gs):
                        e.update(deciso=True, contro=esito(senza, gs))
            ep.append(e)
    for m in partite:
        r = m[4].split("-")
        if r[0] != r[1] and abs(m[1] - m[2]) < 1:
            ep.append(dict(k="stretta", c=m[0], o=m[3], r=m[4], id=m[0] + m[3], deciso=False, peso=0.0, gol=0, sul_filo=True,
                           p=f"{m[1]:g} a {m[2]:g}".replace(".", ",")))
    ep.sort(key=lambda e: (not e["deciso"], -e["gol"], -e["peso"], PRIO[e["k"]], e.get("g") or e.get("c")))
    out = []
    for e in ep[:3]:
        k, chiave = e["k"], f"{G['n']}:{e['k']}:{e['id']}"
        if k == "rosso":
            ver = "Rosso confermato"
        elif e["deciso"]:
            ver = "Ha deciso la partita"
        elif e.get("sul_filo"):
            ver = "Da rivedere"
        else:
            ver = "Regolare"
        x = pick(DECISO[k], chiave) if e["deciso"] else pick(MVT[k]["x"], chiave)
        m = e.get("m")
        rep = {"G": e.get("g", ""), "S": e.get("s", ""), "A": allenatori(e["s"]) if e.get("s") else "",
               "C": e.get("c", ""), "O": e.get("o", ""), "R": ris(e.get("r", "")), "P": e.get("p", ""),
               "AC": allenatori(e["c"]) if e.get("c") else "", "AO": allenatori(e["o"]) if e.get("o") else "",
               "M": f"{m[0]}–{m[3]} {ris(m[4])}" if m else "", "E": CONTRO.get(e.get("contro"), "")}
        x = re.sub(r"\{(\w+)\}", lambda z: rep[z.group(1)], x)
        r = {"k": k, "t": MVT[k]["t"], "v": ver, "x": x}
        for c in ("g", "s", "c", "o"):
            if e.get(c):
                r[c] = e[c]
        out.append(r)
    return out


def main():
    global RUOLO
    d = json.loads(DATI.read_text(encoding="utf-8"))
    form = json.loads(FORM.read_text(encoding="utf-8")) if FORM.exists() else {}
    RUOLO = {k: p.get("r", "?") for k, p in (d.get("P") or {}).items()}
    lega = (d.get("cal") or {}).get("lega") or []
    val = valori_voci(d.get("votes") or {})
    sg = soglie(lega)
    old = json.loads(USCITA.read_text(encoding="utf-8")) if USCITA.exists() else {}
    gg = dict(old.get("giornate") or {})
    nuove = []
    for G in lega:
        if not any(m[4] and m[4] != "-" for m in G["m"]):
            continue
        n = str(G["n"])
        if n in gg and not (RIGENERA is True or (isinstance(RIGENERA, set) and G["n"] in RIGENERA)):
            continue
        gg[n] = {"sa": G["sa"], "episodi": episodi(G, d, form.get(str(G["sa"])), val, sg)}
        nuove.append(n)
    out = {"aggiornato": d.get("updated"), "giornate": dict(sorted(gg.items(), key=lambda z: int(z[0])))}
    USCITA.parent.mkdir(parents=True, exist_ok=True)
    USCITA.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("valori:", {k: val[k] for k in ("rigore sbagliato", "autogol", "rigore parato") if k in val}, "soglie:", sg)
    print("giornate scritte:", ", ".join(nuove) if nuove else f"nessuna (quelle già in {USCITA.name} restano come sono)")
    for n in nuove:
        for e in gg[n]["episodi"]:
            print(f"  G{n} {e['t']}: {e.get('g') or e.get('c')} → {e['v']}")


RUOLO = {}
if __name__ == "__main__":
    main()
