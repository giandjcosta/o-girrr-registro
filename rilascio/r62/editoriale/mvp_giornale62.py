"""Rubrica MVP dei tifosi nel Giornale (ChatGPT; ritoccata da Claude il 15 novembre 2026 su richiesta di Gianluca).

- Candidati: i tre della giornata appena finita, con il motivo della redazione o il risultato vero.
- Quando si vota: data e ora di chiusura della votazione aperta, così si sa quando esce l'MVP.
- Verdetto: l'MVP già votato della giornata precedente (la votazione si chiude prima del Giornale successivo),
  con il risultato vero e il motivo della redazione. Niente prestazioni inventate.
Il Coro della Curva non viene toccato.
"""
import copy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]


def nome(t):
    return (t or "").replace("The Blue brothers", "The Blues Brothers")


def quando(iso):
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(ZoneInfo("Europe/Rome"))
    except (AttributeError, TypeError, ValueError):
        return None
    return f"{GIORNI[d.weekday()]} {d.day} {MESI[d.month - 1]} alle {d.hour:02d}:{d.minute:02d}"


def motivo(w, c):
    m = next((v.get("motivo") for v in w.get("redazione", []) if v.get("scelta") == c.get("team") and v.get("motivo")), None)
    if m:
        return m
    if not all(k in c for k in ("gf", "gs", "op", "away")):
        return None
    if c["away"]:
        return f"Colpo sul campo di {nome(c['op'])}: il {c['gf']}–{c['gs']} porta {nome(c['team'])} fra le tre candidate."
    if c["gf"] == 3:
        return f"Tre gol e una vittoria combattuta contro {nome(c['op'])}: il {c['gf']}–{c['gs']} accende la corsa al premio."
    return f"Il {c['gf']}–{c['gs']} in casa contro {nome(c['op'])} vale la candidatura."


def integra(testi, dossier, giornata, ora=None):
    t = copy.deepcopy(testi)
    rubrica = {"titolo": "MVP dei tifosi", "verdetto": None, "giornata": None, "candidati": [], "chiude": None}
    w = (dossier or {}).get("votazione") or {}
    if not w.get("chiusa") and w.get("giornata") == giornata and w.get("classifica"):
        rubrica["giornata"] = giornata
        q = quando(w.get("chiude"))
        rubrica["chiude"] = f"Si vota in Curva fino a {q}" if q else None   # frase intera: il Giornale mette la maiuscola a inizio testo
        for c in w["classifica"][:3]:
            testo = motivo(w, c)
            if c.get("team") and testo:
                rubrica["candidati"].append({"squadra": nome(c["team"]), "testo": testo})
    # Verdetto dell'MVP già votato: solo la giornata precedente, solo se chiuso con una classifica vera.
    for a in sorted((dossier or {}).get("archivio") or [], key=lambda x: x.get("giornata", 0), reverse=True):
        if a.get("chiusa") and a.get("classifica") and a.get("giornata") == giornata - 1:
            v = a["classifica"][0]
            if v.get("team"):
                rubrica["verdetto"] = {"giornata": a["giornata"], "squadra": nome(v["team"]), "testo": motivo(a, v)}
            break
    if rubrica["candidati"] or rubrica["verdetto"]:
        t["mvp_editoriale"] = rubrica
    return t
