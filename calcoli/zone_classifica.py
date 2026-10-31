"""Lettura della storia di classifica per Curva, Giornale e Radio.
Solo dati delle giornate COMPLETE, nessuna chiamata di rete o scrittura.
Eventi selettivi: 3 giornate consecutive, poi ogni 4; sorpresa negativa
di una favorita soltanto se l'ultima posizione è già confermata.
"""
import re

RIS = re.compile(r"^\d+-\d+$")

def _squadre(d):
    a = d.get("teams") or []
    return sorted({x["name"] if isinstance(x, dict) else x for x in a})

def _giornate(d):
    calendario = sorted((d.get("cal") or {}).get("lega") or [], key=lambda g: g["n"])
    validi, prossimo = [], 1
    for g in calendario:
        if g.get("n") != prossimo:
            break
        mm = g.get("m") or []
        if not mm or not all(RIS.fullmatch(str(x[4])) for x in mm):
            break
        validi.append(g)
        prossimo += 1
    return validi

def storia(d):
    """Per ogni giornata: classifica e posizioni (ordine Pt, totale, DR, GF)."""
    squadre = _squadre(d)
    if len(squadre) < 2:
        return []
    tab = {t: {"t": t, "pt": 0, "fp": 0.0, "gf": 0, "gs": 0} for t in squadre}
    out = []
    for g in _giornate(d):
        for m in g["m"]:
            casa, pc, pf, ospite, ris = m
            if casa not in tab or ospite not in tab:
                return out
            a, b = map(int, ris.split("-"))
            for t, gol, presi, totale in ((casa, a, b, pc), (ospite, b, a, pf)):
                x = tab[t]
                x["pt"] += 3 if gol > presi else 1 if gol == presi else 0
                x["gf"] += gol
                x["gs"] += presi
                x["fp"] += float(totale)
        ordine = sorted(tab.values(), key=lambda x: (-x["pt"], -x["fp"], -(x["gf"]-x["gs"]), -x["gf"], x["t"]))
        out.append({"giornata": g["n"], "posizioni": {x["t"]: i+1 for i, x in enumerate(ordine)},
                    "classifica": [dict(x, pos=i+1) for i, x in enumerate(ordine)]})
    return out

def evento(d, aspettative=None):
    """Ritorna al massimo una storia significativa nell'ultima giornata.
    Nessun titolo/podio/ultimo ogni settimana, canale editoriale alternato.
    """
    hist = storia(d)
    if len(hist) < 2:
        return None
    latest = hist[-1]
    n = latest["giornata"]
    pos = latest["posizioni"]
    expected = (aspettative or {}).get("squadre") or {}
    streak = {}
    for team, posto in pos.items():
        def durata(test):
            a=0
            for x in reversed(hist):
                if test(x["posizioni"][team]):
                    a += 1
                else:
                    break
            return a
        streak[team] = {
            "vetta": durata(lambda p: p == 1),
            "podio": durata(lambda p: p <= 3),
            "ultimo": durata(lambda p: p == len(pos)),
        }
    candidati = []
    for team in sorted(pos):
        ss = streak[team]
        attesa = expected.get(team, {}).get("attesa")
        big = isinstance(attesa, (int, float)) and attesa <= 3
        ultimo = pos[team] == len(pos)
        if big and ultimo and ss["ultimo"] >= 2 and (ss["ultimo"] == 2 or (ss["ultimo"]-2)%4 == 0):
            testo = (f"Clamoroso in fondo alla classifica: {team}, attesa tra le prime {int(attesa)}, "
                     f"è ultima da {ss['ultimo']} giornate. La squadra deve reagire.")
            candidati.append((100, "sorpresa", team, ss["ultimo"], testo))
        if ss["vetta"] >= 3 and (ss["vetta"]-3)%4 == 0:
            testo = (f"{team} resta al comando da {ss['vetta']} giornate consecutive. "
                     + ("Non è più soltanto una buona partenza: ora è continuità." if ss["vetta"] == 3 else "La capolista difende la vetta e allunga la sua storia."))
            candidati.append((85, "vetta", team, ss["vetta"], testo))
        if ultimo and ss["ultimo"] >= 3 and (ss["ultimo"]-3)%4 == 0:
            testo = (f"{team} è ancora all'ultimo posto dopo {ss['ultimo']} giornate consecutive. "
                     "La zona retrocessione è diventata un problema serio.")
            candidati.append((78, "retrocessione", team, ss["ultimo"], testo))
        if pos[team] in (2, 3) and ss["podio"] >= 3 and (ss["podio"]-3)%4 == 0:
            testo = (f"{team} è sul podio da {ss['podio']} giornate consecutive. "
                     "La corsa ai primi posti ha trovato una protagonista stabile.")
            candidati.append((65, "podio", team, ss["podio"], testo))
    if not candidati:
        return None
    # Ruota il tema dominante ogni quattro giornate: la vetta non soffoca
    # per tutta la stagione chi resta in fondo o chi lotta per il podio.
    preferito = ("vetta", "retrocessione", "podio")[((n-3)//4)%3]
    candidati.sort(key=lambda z: (-(z[0] + (55 if z[1]==preferito else 0)), z[2]))
    prior, tipo, team, durata_, testo = candidati[0]
    # Una storia può essere proposta in una sola sede per giornata;
    # il Giornale qui è il profilo ufficiale della Curva, non il PDF.
    canale = ("radio", "curva", "giornale")[n % 3]
    titoli = {"sorpresa": "CRISI IMPREVISTA", "vetta": "LA VETTA DURA",
              "retrocessione": "ZONA RETROCESSIONE", "podio": "PODIO CONQUISTATO"}
    return {"chiave": f"zona:G{n}:{tipo}:{team}", "giornata": n,
            "squadra": team, "tipo": tipo, "durata": durata_, "posizione": pos[team],
            "titolo": titoli[tipo], "testo": testo, "canale": canale}
