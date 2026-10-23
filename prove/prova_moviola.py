#!/usr/bin/env python3
"""Prova con dati finti del post Moviola di Girrr Sport (passo 4). Non tocca il database né il sito: lavora in una cartella temporanea.
Uso (dalla cartella del repo): python3 prove/prova_moviola.py      -  serve node per confrontare con la tab del Lab e con la Curva.

Controlla:
 1. calcoli/moviola.py dà gli stessi episodi, testi e verdetti della tab Moviola del Lab (mvEpisodi in lab/index.html);
 2. il post esce con l'episodio principale (il primo), verdetto, link alla tab e chiave moviola:G<n>:0;
 3. ordine: Giornale, poi Radio, poi Moviola, pochi minuti l'uno dall'altro (e il Giornale nella Curva esce proprio a _pub);
 4. nessun doppione: due giri di pubblicazione, il secondo non pubblica niente; e la Curva non fa più il vecchio post gs:mov;
 5. giornata senza episodi: nessun post.
"""
import datetime, importlib, json, os, subprocess, sys, tempfile
from pathlib import Path

R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / "calcoli"))
import moviola

PUB = 1792854000000   # 24 ottobre 2026, 17:00 ora di Roma: pubblicazione della giornata 3
ESITI = []


def ok(cond, cosa):
    ESITI.append((bool(cond), cosa))
    print(("OK   " if cond else "NO   ") + cosa)


def dati_finti():
    sq = ["Apo team", "WOA", "Grodah", "The Blue brothers", "Real Madrink", "stif dc"]
    P, teams, votes = {}, [], {}
    for i, t in enumerate(sq):
        ids = [str(100 + i * 10 + j) for j in range(4)]
        teams.append(dict(name=t, pl=[dict(id=int(x)) for x in ids]))
        for j, x in enumerate(ids):
            P[x] = dict(n=f"Giocatore{chr(65 + i)}{j} {'É' if j == 3 else 'Z'}.", t="Club", r="PDCA"[j])
    def b(x, sa, f, *ev):
        votes.setdefault(x, {})[str(sa)] = dict(f=f, b=list(ev))
    # giornata 1 (Serie A 5): tanti episodi, ne restano 3; giornata 2 (Serie A 6): niente; giornata 3 (Serie A 7): l'ultima
    b("101", 5, 4.5, "1 rigore sbagliato"); b("112", 5, 5, "1 autogol"); b("120", 5, 9, "1 rigore parato"); b("133", 5, 3, "1 rigore sbagliato")
    b("101", 6, 6.5, "1 gol"); b("112", 6, 6, "1 assist")
    b("143", 7, 4, "1 autogol"); b("150", 7, 9.5, "1 rigore parato"); b("102", 7, 7, "2 gol")
    lega = [dict(n=1, sa=5, _pub=PUB - 14 * 864e5, m=[["Apo team", 72.5, 66, "WOA", "2-0"], ["Grodah", 70, 69.5, "The Blue brothers", "1-0"], ["Real Madrink", 60, 60, "stif dc", "0-0"]]),
            dict(n=2, sa=6, _pub=PUB - 7 * 864e5, m=[["Apo team", 70, 70, "WOA", "1-1"], ["Grodah", 80, 66, "The Blue brothers", "3-0"], ["Real Madrink", 61, 74, "stif dc", "0-2"]]),
            dict(n=3, sa=7, _pub=PUB, m=[["WOA", 74, 73.5, "Grodah", "2-1"], ["Apo team", 66, 72, "Real Madrink", "0-1"], ["The Blue brothers", 68, 68, "stif dc", "1-1"]]),
            dict(n=4, sa=8, m=[["WOA", 0, 0, "Apo team", "-"], ["Grodah", 0, 0, "stif dc", "-"], ["Real Madrink", 0, 0, "The Blue brothers", "-"]])]
    F = {"7": {"stif dc": dict(tit=[150, 151], pan=[152, 153]), "Real Madrink": dict(tit=[140, 141, 142, 143], pan=[])}}
    return dict(teams=teams, P=P, votes=votes, cal=dict(lega=lega, date="2026-10-20"), sa={}, ps={}, scambi=[]), F


def lab_episodi(D, F):
    """Episodi calcolati dal codice vero della tab (lab/index.html), con node."""
    lab = (R / "lab" / "index.html").read_text(encoding="utf-8")
    pezzo = lab[lab.index("var MV=null,MVF={};"):lab.index("function spMoviola(){")]
    mgr = lab[lab.index("MGR={"):lab.index("function mg(t){return MGR[t]||t}") + len("function mg(t){return MGR[t]||t}")]
    mgrs = lab[lab.index("function mgrsOf(t)"):lab.index("\n", lab.index("function mgrsOf(t)"))]
    js = "var " + mgr + "\n" + mgrs + "\n" + pezzo + "\nMV=" + json.dumps(D) + ";MVF=" + json.dumps(F) + \
         ";console.log(JSON.stringify(mvGiocate().map(function(G){return {n:G.n,episodi:mvEpisodi(G)}})))"
    return node(js)


def curva_banca(D, ms):
    """Post che la Curva (curva-banca.js, versione del ramo) genera da sola con questi dati."""
    js = "var window=globalThis;" + (R / "ufficiale" / "girrr" / "curva-banca.js").read_text(encoding="utf-8") + \
         "\nvar D=" + json.dumps(D) + ";var SQ=D.teams.map(function(t){return t.name});" \
         "var P=window.CVB.genera(D,SQ,{cls:SQ.map(function(n){return{n:n,pt:0,fp:0}}),ult:D.cal.lega[2],next:null,cup:{}},%d);" \
         "console.log(JSON.stringify(P.map(function(p){return {k:p.k,a:p.a,ts:p.ts}})))" % ms
    return node(js)


def node(js):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
    try:
        return json.loads(subprocess.check_output(["node", f.name]))
    finally:
        os.unlink(f.name)


def main():
    D, F = dati_finti()
    M = moviola.calcola(D, F)
    L = lab_episodi(D, F)
    mio = [dict(n=g["n"], episodi=[{k: e[k] for k in ("t", "v", "x", "g", "s", "c", "o")} for e in g["episodi"]]) for g in M["giornate"]]
    lab = [dict(n=g["n"], episodi=[{k: (e.get(k) or "") for k in ("t", "v", "x", "g", "s", "c", "o")} for e in g["episodi"]]) for g in L]
    ok(mio == lab, "1. stessi episodi, testi e verdetti della tab Moviola del Lab (3 giornate)")
    ok([len(g["episodi"]) for g in M["giornate"]] == [3, 0, 3], "1. al massimo 3 episodi; la giornata 2 è tranquilla")

    tmp = Path(tempfile.mkdtemp(prefix="prova-moviola-"))
    ev = tmp / "eventi.json"
    ev.write_text(json.dumps([dict(tipo="conferenza", k="C3-Apo team", team="Apo team", giornata=3, libera="Vinciamo noi", promessa="", risposte=[])]), encoding="utf-8")
    mv = tmp / "moviola.json"
    mv.write_text(json.dumps(M, ensure_ascii=False), encoding="utf-8")

    def post_curva():
        subprocess.check_call([sys.executable, str(R / "calcoli" / "post_curva.py"), str(ev), str(tmp / "post_curva.json"), str(mv)], stdout=subprocess.DEVNULL)
        return json.loads((tmp / "post_curva.json").read_text(encoding="utf-8"))

    out = post_curva()
    mov = [p for p in out if p["chiave"].startswith("moviola:")]
    ok(len(mov) == 1 and mov[0]["chiave"] == "moviola:G3:0" and mov[0]["h"] == "girrr_sport", "2. un solo post Moviola, di Girrr Sport, chiave moviola:G3:0 (solo l'ultima giornata)")
    e0 = M["giornate"][-1]["episodi"][0]
    ok(mov and e0["t"] in mov[0]["body"] and e0["x"] in mov[0]["body"] and f"Verdetto: {e0['v']}." in mov[0]["body"] and len(mov[0]["body"]) <= 280,
       "2. il post ha l'episodio principale con lo stesso testo e verdetto della tab: " + (mov[0]["body"].replace("\n", " / ") if mov else ""))
    curva = (R / "ufficiale" / "girrr" / "curva.html").read_text(encoding="utf-8")
    ok(mov and mov[0]["body"].startswith("MOVIOLA · Giornata ") and "Apri la Moviola ›" in curva and "#moviola\">Apri la Moviola" in curva,
       "2. nella Curva il post rimanda alla tab Moviola (Apri la Moviola ›)")

    pc = importlib.import_module("post_curva")
    q = datetime.datetime.fromisoformat(mov[0]["quando"]).timestamp() * 1000 if mov else 0
    ok(pc.SCALETTA["giornale"] < pc.SCALETTA["radio"] < pc.SCALETTA["moviola"] <= 15 and q == PUB + pc.SCALETTA["moviola"] * 60000,
       "3. ordine Giornale (+%d min), Radio (+%d), Moviola (+%d): la Moviola esce a %s" % (pc.SCALETTA["giornale"], pc.SCALETTA["radio"], pc.SCALETTA["moviola"], mov[0].get("quando") if mov else "-"))
    cb = curva_banca(D, PUB + 3 * 36e5)
    gio = [p for p in cb if p["k"] == "gior:3"]
    ok(gio and gio[0]["ts"] == PUB and gio[0]["ts"] < q, "3. il post del Giornale nella Curva esce a _pub, prima della Moviola")
    ok(not [p for p in cb if p["k"].startswith("gs:mov")], "4. la Curva non genera più il vecchio post gs:mov (niente doppio post per lo stesso episodio)")

    # due giri di pubblicazione (in modo AUTO, con l'invio finto): il secondo non trova niente di nuovo
    os.environ["CURVA_MODO"] = "auto"
    pub = importlib.import_module("pubblica_curva")
    pub.POST, pub.FATTI, pub.CODA, pub.CONF = (tmp / n for n in ("post_curva.json", "pubblicati.json", "coda_curva.json", "curva_config.json"))
    inviati = []   # corpi delle chiamate a curva_adm_scrivi: la rete è finta, niente esce davvero
    os.environ.update(CURVA_URL="http://finto.invalid", CURVA_KEY="x", CURVA_TEAM="Oranje VC", CURVA_CODE="x")
    class Finta:
        def read(self):
            return b"1"
    def urlopen(rich, timeout=None):
        assert rich.full_url.endswith("/rpc/curva_adm_scrivi")
        inviati.append(json.loads(rich.data))
        return Finta()
    pub.urllib.request.urlopen = urlopen
    sys.argv = ["pubblica_curva.py", "--vai"]
    pub.main()
    primo = len(inviati)
    post_curva()          # il giro dopo rifà gli stessi post (come il workflow ogni mezz'ora)
    pub.main()
    ok(primo == 2 and len(inviati) == 2, "4. primo giro: %d post (conferenza e Moviola); secondo giro: %d nuovi" % (primo, len(inviati) - primo))
    ok(len({p["chiave"] for p in out}) == len(out), "4. chiavi tutte diverse nel formato tipo:k:indice")
    ok(mov and [p.get("p_quando") for p in inviati if p["p_body"].startswith("MOVIOLA")] == [mov[0]["quando"]]
       and [p.get("p_quando") for p in inviati if not p["p_body"].startswith("MOVIOLA")] == [None], "3. l'orario arriva a curva_adm_scrivi come p_quando (solo per la Moviola)")

    # giornata senza episodi (l'ultima è la 2, tranquilla) e moviola.json assente: nessun post Moviola
    M2 = dict(giornate=M["giornate"][:2])
    mv.write_text(json.dumps(M2, ensure_ascii=False), encoding="utf-8")
    ok(not [p for p in post_curva() if p["chiave"].startswith("moviola:")], "5. giornata senza episodi: nessun post Moviola")
    mv.unlink()
    ok(not [p for p in post_curva() if p["chiave"].startswith("moviola:")], "5. senza moviola.json: nessun post Moviola")

    no = [c for v, c in ESITI if not v]
    print("\nTutto a posto." if not no else f"\n{len(no)} controlli NON passati.")
    sys.exit(1 if no else 0)


if __name__ == "__main__":
    main()
