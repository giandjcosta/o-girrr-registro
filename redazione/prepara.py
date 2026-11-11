#!/usr/bin/env python3
"""Redazione di Girrr Sport · Dossier delle squadre (Claude, 11 novembre 2026, versione 5.8).

Prepara per ogni squadra i fatti veri che servono alla redazione (Claude in una sessione programmata, vedi ISTRUZIONI.md)
per scrivere le domande della conferenza stampa e giudicare le risposte scritte a mano. Solo letture: sito pubblico e
funzioni pubbliche del database (le stesse della Curva). Non scrive niente nel database né sul sito.

Uso:  python3 redazione/prepara.py [uscita.json]          (predefinito: redazione/dossier.json)
      opzioni: --sito URL_O_CARTELLA (predefinito il sito vero), --giornata N (predefinita la prossima da giocare)
I risultati contano solo quando la giornata è pubblicata sul sito (un'ora dopo voti e calcolo, come le pagine).
"""
import datetime, json, re, sys, urllib.request
from pathlib import Path

QUI = Path(__file__).resolve().parent
REG = QUI.parent
DB, KEY = "https://qmjqfgmvimsuxvghetgi.supabase.co", "sb_publishable_qPhimkrF4iUvIad7JPoH8A_i-eOqG7n"
ARG = sys.argv[1:]


def opz(nome, predef=None):
    return ARG[ARG.index(nome) + 1] if nome in ARG else predef


USCITA = Path(next((a for i, a in enumerate(ARG) if not a.startswith("--") and (i == 0 or not ARG[i - 1].startswith("--"))), QUI / "dossier.json"))
SITO = opz("--sito", "https://giandjcosta.github.io/o-fant-a-girrr/")
MOSTRA = {"The Blue brothers": "The Blues Brothers"}   # nomi come si leggono sul sito (nomi.js)
TONI = ["Sicuro", "Umile", "Provocatorio"]


def leggi(rel):
    if SITO.startswith("http"):
        return urllib.request.urlopen(SITO.rstrip("/") + "/" + rel, timeout=30).read().decode("utf-8")
    return (Path(SITO) / rel).read_text(encoding="utf-8")


def rpc(nome, corpo=None):
    r = urllib.request.Request(f"{DB}/rest/v1/rpc/{nome}", json.dumps(corpo or {}).encode(),
                               {"apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(r, timeout=30).read())
    except Exception as e:
        print(f"{nome}: non disponibile ({e})")
        return None


def gol(s):
    m = re.match(r"^(\d+)\s*-\s*(\d+)$", s or "")
    return (int(m.group(1)), int(m.group(2))) if m else None


def main():
    D = json.loads(leggi("data.json"))
    try:
        F = json.loads(leggi("girrr/dati/fiducia.json"))
    except Exception:
        F = {}
    try:
        nov = leggi("girrr/novita-dati.js")
        RIV = json.loads(nov[nov.index("{"):nov.rindex("}") + 1]).get("riv", [])
    except Exception:
        RIV = []
    ASP = json.loads((REG / "calcoli" / "aspettative.json").read_text(encoding="utf-8"))
    MGR = json.loads((REG / "calcoli" / "nomi.json").read_text(encoding="utf-8"))
    conf = rpc("conf_pubbliche") or []
    prom = rpc("conf_promesse") or []
    dopo = rpc("conf_dopo_pubbliche") or []
    derby = rpc("derby_stato", {"p_team": None, "p_code": None}) or {}

    ora = datetime.datetime.now(datetime.timezone.utc).timestamp()

    def pubblicata(g):
        v, c = (D.get("votiTs") or {}).get(str(g["sa"])), (D.get("calcTs") or {}).get(str(g["sa"]))
        if not v and not c:
            return True
        t = max(datetime.datetime.fromisoformat(x.replace("Z", "+00:00")).timestamp() for x in (v, c) if x)
        return ora >= t + 3600

    lega = D["cal"]["lega"]
    giocate = [g for g in lega if g["m"] and all(gol(m[4]) for m in g["m"]) and pubblicata(g)]
    ultima = giocate[-1]["n"] if giocate else 0
    G = int(opz("--giornata", 0)) or next((g["n"] for g in lega if g["n"] > ultima), ultima)
    prossima = next((g for g in lega if g["n"] == G), None)

    # classifica dopo l'ultima giornata pubblicata (punti, differenza reti, gol fatti; a pari tutto i fantapunti, come Leghe)
    T = {t["name"]: dict(t=t["name"], g=0, v=0, n=0, p=0, gf=0, gs=0, pt=0, fp=0.0, forma=[]) for t in D["teams"]}
    for g in giocate:
        for m in g["m"]:
            r = gol(m[4])
            for sq, a, b, fp, avv in ((m[0], r[0], r[1], m[1], m[3]), (m[3], r[1], r[0], m[2], m[0])):
                s = T[sq]; s["g"] += 1; s["gf"] += a; s["gs"] += b; s["fp"] += float(fp or 0)
                e = "V" if a > b else "N" if a == b else "P"
                s["v" if e == "V" else "n" if e == "N" else "p"] += 1; s["pt"] += 3 if e == "V" else 1 if e == "N" else 0
                s["forma"].append(f"{e} {a}-{b} contro {MOSTRA.get(avv, avv)} ({g['n']}ª)")
    cl = sorted(T.values(), key=lambda s: (-s["pt"], -(s["gf"] - s["gs"]), -s["gf"], -s["fp"]))
    for i, s in enumerate(cl):
        s["pos"] = i + 1

    def chiave(a, b):
        return "|".join(sorted([a.lower(), b.lower()]))
    derby_nomi = {chiave(o["a"], o["b"]): o.get("n") or "Derby" for o in RIV if o.get("r", 0) >= 80}
    for s in derby.get("sfide", []):
        if s.get("stato") == "accettata" and s.get("nome_ok"):
            derby_nomi[chiave(s["da"], s["a"])] = s.get("nome") or "Derby"

    squadre = {}
    for t in T:
        s = T[t]
        m = next((x for x in (prossima or {}).get("m", []) if t in (x[0], x[3])), None)
        avv = (m[3] if m[0] == t else m[0]) if m else None
        a = ASP["squadre"].get(t, {})
        f = (F.get("squadre") or {}).get(t, {})
        miei = sorted([p for p in prom if p["team"] == t], key=lambda p: p["giornata"])
        ultima_conf = max([c for c in conf if c["team"] == t], key=lambda c: c["giornata"], default=None)
        squadre[t] = dict(
            squadra=MOSTRA.get(t, t), allenatore=MGR.get(t, t), giornata=G,
            partita=f"{MOSTRA.get(m[0], m[0])} - {MOSTRA.get(m[3], m[3])}" if m else None,
            in_casa=bool(m and m[0] == t), avversario=MOSTRA.get(avv, avv) if avv else None,
            derby=derby_nomi.get(chiave(t, avv)) if avv else None,
            classifica=dict(posizione=s["pos"], punti=s["pt"], giocate=s["g"], vittorie=s["v"], pareggi=s["n"], sconfitte=s["p"], gol_fatti=s["gf"], gol_subiti=s["gs"]),
            avversario_classifica=(lambda o: dict(posizione=o["pos"], punti=o["pt"]))(T[avv]) if avv else None,
            ultime=s["forma"][-5:],
            obiettivo_presidente=a.get("obiettivo"), posizione_attesa=a.get("attesa"), obiettivo_coppa=a.get("coppa"),
            fiducia=f.get("fiducia"),
            promesse=[dict(giornata=p["giornata"], promessa=p["promessa"], esito={"v": "mantenuta", "p": "pareggio", "s": "tradita"}.get(p.get("esito"), "in attesa")) for p in miei][-4:],
            ultima_conferenza=dict(giornata=ultima_conf["giornata"], risposte=[r.get("t") for r in ultima_conf.get("risposte") or []]) if ultima_conf else None,
            silenzi=[g["n"] for g in giocate if not any(c["team"] == t and c["giornata"] == g["n"] for c in conf)][-3:],
        )

    # risposte scritte a mano da giudicare (conferenze della vigilia e del dopo partita delle ultime due giornate)
    da_giudicare = []
    for c in conf:
        if c["giornata"] >= G - 1:
            for i, r in enumerate(c.get("risposte") or []):
                if r.get("a") == "free" and r.get("t"):
                    da_giudicare.append(dict(tipo="vigilia", chiave=f"{c['team']}|{c['giornata']}", squadra=c["team"], giornata=c["giornata"], domanda=i, risposta=r["t"], tono_automatico=TONI[int(r.get("k", 1))], promessa_automatica=bool(r.get("w"))))
    for c in dopo:
        r = c.get("risposta") or {}
        if c["giornata"] >= G - 1 and r.get("a") == "free" and r.get("t"):
            da_giudicare.append(dict(tipo="dopo", chiave=f"{c['team']}|{c['giornata']}|dopo", squadra=c["team"], giornata=c["giornata"], risposta=r["t"]))

    out = dict(aggiornato=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), giornata=G,
               ultima_giocata=ultima, squadre=squadre, da_giudicare=da_giudicare)
    USCITA.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Dossier scritto: {USCITA} · giornata {G} · {len(squadre)} squadre · {len(da_giudicare)} risposte da giudicare")


if __name__ == "__main__":
    main()
