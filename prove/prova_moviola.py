#!/usr/bin/env python3
"""Prova con dati finti del post Moviola di Girrr Sport (passo 4). Non tocca il database né il sito: lavora in una cartella temporanea
con una copia degli script di calcoli/ (moviola.py, post_curva.py, pubblica_curva.py) e una rete finta.
Uso (dalla cartella del repo): python3 prove/prova_moviola.py      -  serve node per la Curva (ufficiale/src/sito/girrr/curva-banca.js).

Cinque giornate giocate una dopo l'altra, come nella stagione vera:
  1 quattro episodi (più un quinto che resta fuori) 2 nessun episodio            3 solo scartati (giocatore senza formazione)
  4 un episodio scritto a mano                     5 un episodio con il video (aggiunto a mano)
Dopo ogni giornata: moviola.py, post_curva.py e pubblica_curva.py (due giri). Controlla:
  - un solo post Moviola per giornata, chiave moviola:G<n>:0, con titolo, testo e verdetto del primo episodio di moviola.json;
  - nessun post per le giornate 2 e 3; nessun doppione al secondo giro;
  - ordine nella Curva: Giornale, poi Radio (5 minuti dopo), poi Moviola (10 minuti dopo); la Curva non fa più gs:mov;
  - il post rimanda alla tab Moviola (link "Apri la Moviola" in curva.html, Lega e Stadio).
"""
import datetime, importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

R = Path(__file__).resolve().parent.parent
ESITI = []
SQ = ["Apo team", "WOA", "Grodah", "The Blue brothers", "Real Madrink", "stif dc"]


def ok(cond, cosa):
    ESITI.append((bool(cond), cosa))
    print(("OK   " if cond else "NO   ") + cosa)


def node(js):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
    try:
        return json.loads(subprocess.check_output(["node", f.name]))
    finally:
        os.unlink(f.name)


def stagione(k):
    """data.json e formazioni.json finti con le giornate 1..k giocate (giornata n = Serie A n+4)."""
    P, teams, votes, F = {}, [], {}, {}
    for i, t in enumerate(SQ):
        ids = [str(100 + i * 10 + j) for j in range(6)]
        teams.append(dict(name=t, pl=[dict(id=int(x)) for x in ids]))
        for j, x in enumerate(ids):
            P[x] = dict(n=f"Giocatore{chr(65 + i)}{j}", t=["Napoli", "Inter", "Milan", "Roma", "Genoa", "Lazio"][i], r="PDDCCA"[j])
    lega, ris = [], {1: [["Apo team", 72.5, 66, "WOA", "2-0"], ["Grodah", 70, 64.5, "The Blue brothers", "1-0"], ["Real Madrink", 60, 60, "stif dc", "0-0"]],
                     2: [["Apo team", 70, 70, "WOA", "1-1"], ["Grodah", 80, 66, "The Blue brothers", "3-0"], ["Real Madrink", 61, 74, "stif dc", "0-2"]],
                     3: [["WOA", 74, 64, "Grodah", "2-0"], ["Apo team", 66, 72, "Real Madrink", "1-2"], ["The Blue brothers", 68, 68, "stif dc", "1-1"]],
                     4: [["WOA", 70, 70, "Apo team", "1-1"], ["Grodah", 75, 62, "stif dc", "2-0"], ["Real Madrink", 66, 76, "The Blue brothers", "1-3"]],
                     5: [["Apo team", 80, 64, "Grodah", "3-0"], ["WOA", 71, 66, "stif dc", "2-1"], ["The Blue brothers", 70, 70, "Real Madrink", "1-1"]]}
    for n in range(1, 7):
        sa = n + 4
        m = ris[n] if n <= k else [[a, 0, 0, b, "-"] for a, _, _, b, _ in ris[1]]
        lega.append(dict(n=n, sa=sa, m=m))
        if n <= k:
            F[str(sa)] = {t["name"]: dict(tit=[p["id"] for p in t["pl"][:4]], pan=[p["id"] for p in t["pl"][4:5]]) for t in teams}
            for x in P:   # tutti a voto 6 senza voci
                votes.setdefault(x, {})[str(sa)] = dict(v=6, f=6, b=[])
    def voce(x, n, b, eff):
        votes[x][str(n + 4)] = dict(v=6, f=6 + eff, b=[b])
    voce("101", 1, "1 rigore sbagliato", -3); voce("112", 1, "1 autogol", -2); voce("120", 1, "1 rigore parato", 3); voce("133", 1, "1 rigore sbagliato", -3); voce("114", 1, "1 rigore sbagliato", -3)
    if k >= 3:
        voce("145", 3, "1 rigore sbagliato", -3)   # 145 è in rosa ma non in formazione (solo i primi 5): scartato
    if k >= 5:
        voce("102", 5, "1 autogol", -2)
    sett = datetime.date(2026, 10, 7) + datetime.timedelta(days=7 * (k - 1))   # un mercoledì per giornata
    d = dict(teams=teams, P=P, votes=votes, cal=dict(lega=lega, date=sett.isoformat()), sa={}, ps={}, scambi=[])
    return d, F


MANUALE = [{"giornata": 4, "tipo": "altro", "giocatore": "GiocatoreC2", "squadra": "Grodah", "testo": "Gol annullato per un fuorigioco di pochi centimetri: al replay la spalla è avanti."},
           {"giornata": 5, "tipo": "autogol", "giocatore": "GiocatoreA2", "squadra": "Apo team", "video": {"url": "https://www.youtube.com/watch?v=abcdefghijk", "secondo": 95}}]


def curva(sito, d, ms, radio):
    """Post che la Curva vera (versione del rilascio) genera da sola con questi dati."""
    js = "var window=globalThis;" + (R / "ufficiale" / "src" / "sito" / sito / "curva-banca.js").read_text(encoding="utf-8") + \
         "\nCVB.RADIO=%s;var D=%s;var SQ=D.teams.map(function(t){return t.name});" % (json.dumps(radio), json.dumps(d)) + \
         "var U=D.cal.lega.filter(function(g){return g.m.some(function(m){return m[4]!=='-'})}).pop();" \
         "var P=CVB.genera(D,SQ,{cls:SQ.map(function(n){return{n:n,pt:0,fp:0}}),ult:U,next:null,cup:{}},%d);" \
         "console.log(JSON.stringify(P.map(function(p){return {k:p.k,a:p.a,ts:p.ts,tipo:p.tipo||''}})))" % ms
    return node(js)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="prova-moviola-"))
    C = tmp / "calcoli"
    C.mkdir()
    for f in ("moviola.py", "post_curva.py", "pubblica_curva.py", "nomi.json", "curva_config.json"):
        shutil.copy(R / "calcoli" / f, C / f)
    (C / "moviola-manuale.json").write_text(json.dumps(MANUALE, ensure_ascii=False), encoding="utf-8")
    (C / "eventi.json").write_text("[]", encoding="utf-8")
    os.environ.update(CURVA_MODO="auto", CURVA_URL="http://finto.invalid", CURVA_KEY="x", CURVA_TEAM="Oranje VC", CURVA_CODE="x")
    spec = importlib.util.spec_from_file_location("pubblica_finta", C / "pubblica_curva.py")
    pub = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pub)
    inviati = []   # corpi delle chiamate a curva_adm_scrivi: rete finta, niente esce davvero

    class Risposta:
        def read(self):
            return str(len(inviati)).encode()

    def urlopen(rich, timeout=None):
        assert rich.full_url.endswith("/rpc/curva_adm_scrivi"), rich.full_url
        inviati.append(json.loads(rich.data))
        return Risposta()
    pub.urllib.request.urlopen = urlopen
    post_mov = {}

    for k in range(1, 6):
        d, F = stagione(k)
        (tmp / "data.json").write_text(json.dumps(d), encoding="utf-8")
        (tmp / "formazioni.json").write_text(json.dumps(F), encoding="utf-8")
        subprocess.check_call([sys.executable, str(C / "moviola.py"), str(tmp / "data.json"), str(tmp / "formazioni.json"), str(C / "moviola.json")], stdout=subprocess.DEVNULL)
        M = json.loads((C / "moviola.json").read_text(encoding="utf-8"))
        prima = len(inviati)
        for giro in (1, 2):   # dopo la giornata e mezz'ora dopo (curva-subito): il secondo non deve pubblicare niente
            subprocess.check_call([sys.executable, str(C / "post_curva.py"), str(C / "eventi.json"), str(C / "post_curva.json"), str(C / "moviola.json"), str(tmp / "data.json")], stdout=subprocess.DEVNULL)
            sys.argv = ["pubblica_curva.py", "--vai"]
            pub.main()
            if giro == 1:
                dopo1 = len(inviati)
        nuovi = inviati[prima:]
        G = M["giornate"][str(k)]
        mov = [p for p in nuovi if p["p_body"].startswith("MOVIOLA")]
        if k in (2, 3):
            ok(not mov, f"giornata {k} ({'nessun episodio' if k == 2 else 'solo scartati: ' + str(len(G['scartati']))}): nessun post Moviola")
            continue
        e = G["episodi"][0]
        ok(len(mov) == 1 and len(inviati) == dopo1, f"giornata {k}: un solo post Moviola, nessun doppione al secondo giro ({len(G['episodi'])} episodi)")
        if not mov:
            continue
        b = mov[0]["p_body"]
        intero = e["testo"] in b
        ok(b.startswith(f"MOVIOLA · Giornata {k}\n{e['titolo']}. ") and f"Verdetto: {e['verdetto']}." in b and len(b) <= 280
           and (intero or (len(e["testo"]) > 280 - len(f"MOVIOLA · Giornata {k}\n{e['titolo']}. Verdetto: {e['verdetto']}.") and "…" in b)),
           f"giornata {k}: episodio principale con titolo, {'testo intero' if intero else 'testo accorciato (troppo lungo)'} e verdetto della tab ({len(b)} caratteri)")
        post_mov[k] = (mov[0], d, e)
    pj = json.loads((C / "pubblicati.json").read_text(encoding="utf-8"))
    ok(sorted(x for x in pj if x.startswith("moviola:")) == ["moviola:G1:0", "moviola:G4:0", "moviola:G5:0"], "chiavi moviola:G<n>:0 solo per le giornate 1, 4 e 5")
    M = json.loads((C / "moviola.json").read_text(encoding="utf-8"))
    ok(len(M["giornate"]["1"]["episodi"]) == 4 and len(M["giornate"]["1"]["automatici"]) == 5, "giornata 1: 5 episodi trovati, 4 mostrati")
    ok(M["giornate"]["4"]["episodi"][0].get("manuale") and post_mov.get(4) and "fuorigioco" in post_mov[4][0]["p_body"], "giornata 4: il post usa l'episodio scritto a mano")
    ok(any(x.get("video") for x in M["giornate"]["5"]["episodi"]) and 5 in post_mov, "giornata 5: episodio con video, post regolare")

    # ordine nella Curva vera: Giornale, Radio (+5), Moviola (+10); niente gs:mov
    for k in (4, 5):
        p, d, _ = post_mov[k]
        q = datetime.datetime.fromisoformat(p["p_quando"]).timestamp() * 1000
        for sito in ("girrr", "stadio/girrr"):
            cb = curva(sito, d, int(q + 36e5), [k])
            gio = [x["ts"] for x in cb if x["k"] == f"gior:{k}"]
            rad = [x["ts"] for x in cb if x["k"] == f"gs:radio{k}"]
            ok(gio and rad and rad[0] - gio[0] == 5 * 60000 and q - rad[0] == 5 * 60000,
               f"giornata {k} ({sito}): Giornale, Radio 5 minuti dopo, Moviola 5 minuti dopo la Radio")
            ok(not [x for x in cb if x["k"].startswith("gs:mov")], f"giornata {k} ({sito}): la Curva non fa più il vecchio post gs:mov")
    p, d, _ = post_mov[1]
    cb = curva("girrr", d, int(datetime.datetime.fromisoformat(p["p_quando"]).timestamp() * 1000 + 36e5), [])
    gio = [x["ts"] for x in cb if x["k"] == "gior:1"]
    ok(gio and datetime.datetime.fromisoformat(p["p_quando"]).timestamp() * 1000 - gio[0] == 10 * 60000, "giornata 1: Moviola 10 minuti dopo il Giornale")
    ok(all(x.get("p_quando") is None for x in inviati if not x["p_body"].startswith("MOVIOLA")), "solo la Moviola ha un orario (p_quando)")
    for sito in ("girrr", "stadio/girrr"):
        h = (R / "ufficiale" / "src" / "sito" / sito / "curva.html").read_text(encoding="utf-8")
        ok("/^MOVIOLA · Giornata /.test(p.x||'')?'<a class=\"lnk\" href=\"app.html#moviola\">Apri la Moviola ›</a>'" in h, f"curva.html ({sito}): il post rimanda alla tab Moviola")

    no = [c for v, c in ESITI if not v]
    print("\nTutto a posto." if not no else f"\n{len(no)} controlli NON passati.")
    shutil.rmtree(tmp, ignore_errors=True)
    sys.exit(1 if no else 0)


if __name__ == "__main__":
    main()
