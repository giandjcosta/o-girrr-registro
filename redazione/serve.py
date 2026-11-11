#!/usr/bin/env python3
"""Redazione di Girrr Sport · C'è lavoro da fare? (Claude, 11 novembre 2026, versione 5.8; Gianluca: «una volta dopo la partita
appena fatta e prima della successiva va bene, massimo due»).

Al massimo due giri di redazione per giornata:
  dopo     - quando l'ultima giornata è pubblicata sul sito (un'ora dopo voti e calcolo): si giudicano le risposte scritte a mano
             della vigilia appena giocata e si preparano le domande della giornata successiva;
  vigilia  - nelle 36 ore prima della prima partita di Serie A della giornata successiva (data.json, sa): si giudicano le risposte
             scritte a mano arrivate nel frattempo (conferenze della vigilia e del dopo partita).
Il giro fatto si segna in redazione/stato.json (lo scrive questo script con --fatto). Senza lavoro risponde «niente» ed esce con 3:
la sessione programmata si chiude subito, quasi senza consumare.

Uso:  python3 redazione/serve.py                 dice cosa fare (dopo, vigilia o niente)
      python3 redazione/serve.py --fatto dopo    segna il giro come fatto (dopo averlo pubblicato)
"""
import datetime, json, re, sys, urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

QUI = Path(__file__).resolve().parent
STATO = QUI / "stato.json"
SITO = "https://giandjcosta.github.io/o-fant-a-girrr/data.json"
ROMA = ZoneInfo("Europe/Rome")
ORE_VIGILIA = 36


def gol(s):
    return re.match(r"^\d+\s*-\s*\d+$", s or "")


def situazione(D, ora):
    def pubblicata(g):
        v, c = (D.get("votiTs") or {}).get(str(g["sa"])), (D.get("calcTs") or {}).get(str(g["sa"]))
        ts = [datetime.datetime.fromisoformat(x.replace("Z", "+00:00")) for x in (v, c) if x]
        return not ts or ora >= max(ts) + datetime.timedelta(hours=1)
    lega = D["cal"]["lega"]
    giocate = [g for g in lega if g["m"] and all(gol(m[4]) for m in g["m"]) and pubblicata(g)]
    ultima = giocate[-1]["n"] if giocate else 0
    prossima = next((g for g in lega if g["n"] > ultima), None)
    inizio = None
    if prossima:
        orari = []
        for m in (D.get("sa") or {}).get(str(prossima["sa"]), []):   # calendario di Serie A: [casa, trasferta, «21/11 15:00»]
            try:   # «21/11 15:00», ora italiana; l'anno è quello della stagione
                gm, hm = m[2].split()
                dd, mm = map(int, gm.split("/")); hh, mi = map(int, hm.split(":"))
                anno = ora.year + (1 if mm < ora.month - 6 else 0) - (1 if mm > ora.month + 6 else 0)
                orari.append(datetime.datetime(anno, mm, dd, hh, mi, tzinfo=ROMA))
            except Exception:
                pass
        inizio = min(orari) if orari else None
    return ultima, prossima["n"] if prossima else None, inizio


def main():
    stato = json.loads(STATO.read_text(encoding="utf-8")) if STATO.exists() else {"dopo": 0, "vigilia": 0}
    if "--fatto" in sys.argv:
        giro = sys.argv[sys.argv.index("--fatto") + 1]
        D = json.loads(urllib.request.urlopen(SITO, timeout=30).read())
        ultima, prossima, _ = situazione(D, datetime.datetime.now(datetime.timezone.utc))
        stato[giro] = ultima if giro == "dopo" else prossima
        stato["aggiornato"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        STATO.write_text(json.dumps(stato, ensure_ascii=False, indent=1), encoding="utf-8")
        print("Segnato:", giro, stato[giro])
        return
    D = json.loads(urllib.request.urlopen(SITO, timeout=30).read())
    ora = datetime.datetime.now(datetime.timezone.utc)
    ultima, prossima, inizio = situazione(D, ora)
    if ultima > stato.get("dopo", 0):
        print(json.dumps(dict(lavoro="dopo", giornata_giocata=ultima, prossima=prossima), ensure_ascii=False))
        return
    if prossima and inizio and stato.get("vigilia", 0) < prossima and ora >= inizio - datetime.timedelta(hours=ORE_VIGILIA) and ora < inizio:
        print(json.dumps(dict(lavoro="vigilia", prossima=prossima, inizio=inizio.isoformat()), ensure_ascii=False))
        return
    print(json.dumps(dict(lavoro="niente", ultima=ultima, prossima=prossima, inizio=inizio.isoformat() if inizio else None), ensure_ascii=False))
    sys.exit(3)


if __name__ == "__main__":
    main()
