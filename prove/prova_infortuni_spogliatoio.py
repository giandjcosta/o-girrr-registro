#!/usr/bin/env python3
"""Prova: infortuni e squalifiche nello Spogliatoio (Chi scambiare, Mercato Scambi).

1. Script dei dati (rilascio/infortuni56/aggiorna_dati.py): foto degli indisponibili
   solo prima del calcio d'inizio, «I» al posto di «P» per chi era fuori, anche sulle
   giornate già scritte; chi era disponibile resta «P».
2. Pagina: con i dati veri del sito (data.json di gh-pages dalla copia ../o-fant-a-girrr)
   Lautaro Martinez ha I nelle giornate 7-10 e passa da «Osserva» a «Tieni»; Chi scambiare
   e Mercato Scambi si aprono senza errori a 320 px.

Uso: python3 prove/prova_infortuni_spogliatoio.py
"""
import datetime as dt
import functools
import http.server
import importlib.util
import json
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
CART = RADICE / "rilascio" / "infortuni56"
SORG = RADICE / "ufficiale" / "src" / "sito" / "spogliatoio-index.html"
SITO = RADICE.parent / "o-fant-a-girrr"
errori = []


def ok(cond, msg):
    print(("OK   " if cond else "NO   ") + msg)
    if not cond:
        errori.append(msg)


def prova_script():
    spec = importlib.util.spec_from_file_location("agg", CART / "aggiorna_dati.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "scripts").mkdir()
        (tmp / "scripts" / "ind_storico.json").write_text((CART / "ind_storico.json").read_text())
        m.ROOT = tmp
        D = {"round": 11, "nx": 11, "fx": {"11": [["Inter", "Milan", "sab 07/11 18:00"]]},
             "st": {"1": {"s": "I", "n": "Infortunato"}, "2": {"s": "T"}, "3": {"s": "I", "n": "Squalificato"}}}
        prima = dt.datetime(2026, 11, 7, 16, 0, tzinfo=dt.timezone.utc)
        ind = m.aggiorna_indisponibili(D, prima)
        ok(ind.get("11") == ["1", "3"], "foto della giornata 11 prima del calcio d'inizio")
        ok("2764" in ind.get("10", []), "storico caricato (Lautaro fuori in G10)")
        D["st"]["2"] = {"s": "I"}
        m.aggiorna_indisponibili(D, prima + dt.timedelta(hours=3))
        ok(D["ind"]["11"] == ["1", "3"], "dopo il calcio d'inizio la foto non cambia")

        # giro completo di main() con pagine finte
        D = {"round": 2, "nx": 2, "fx": {}, "st": {}, "fa": [], "ps": {},
             "P": {"10": {"n": "A", "t": "Inter", "r": "A"}, "11": {"n": "B", "t": "Inter", "r": "A"},
                   "12": {"n": "C", "t": "Inter", "r": "A"}, "13": {"n": "D", "t": "Inter", "r": "C"}},
             "teams": [{"name": "X", "pl": [{"id": 10}, {"id": 11}, {"id": 12}, {"id": 13}]}],
             "log": {"11": {"1": "P"}}, "ind": {"1": ["11", "12"]}}
        (tmp / "data.json").write_text(json.dumps(D))
        m.leggi_statistiche = lambda h: {str(i): {"pg": 1} for i in range(400)}
        m.leggi_voti = lambda h: {"10": {"v": 6, "f": 6, "b": [], "sub": False}} if h == "1" else {}
        m.scarica = lambda url, c=None, n=None: "1" if url.endswith("/1") else "x"
        m.main()
        log = json.loads((tmp / "data.json").read_text())["log"]
        ok(log["10"]["1"] == "T", "chi ha giocato resta T")
        ok(log["11"]["1"] == "I", "P già scritto diventa I se era fuori")
        ok(log["12"]["1"] == "I", "giornata nuova: I per chi era fuori")
        ok(log["13"]["1"] == "P", "chi era disponibile e non ha giocato resta P")


def prova_pagina():
    try:
        dati = subprocess.run(["git", "-C", str(SITO), "show", "origin/gh-pages:data.json"],
                              capture_output=True, text=True, check=True).stdout
    except Exception:  # noqa: BLE001
        print("SALTO la prova della pagina: manca la copia ../o-fant-a-girrr con gh-pages")
        return
    D = json.loads(dati)
    storico = json.loads((CART / "ind_storico.json").read_text())["giornate"]
    for g, v in storico.items():
        for i in v["I"]:
            if D["log"].get(i, {}).get(g) == "P":
                D["log"][i][g] = "I"

    def hsh(s):
        h = 2166136261
        for ch in s:
            h ^= ord(ch)
            h = (h * 16777619) & 0xFFFFFFFF
        n, out = h, ""
        while True:
            n, r = divmod(n, 36)
            out = "0123456789abcdefghijklmnopqrstuvwxyz"[r] + out
            if not n:
                return out
    D["lock"]["Oranje VC"] = hsh("Oranje VC|PROVA")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for nome, extra in (("prima", []), ("dopo", [])):
            d = tmp / nome
            d.mkdir()
            (d / "data.json").write_text(json.dumps(D, ensure_ascii=False))
            (d / "assets").mkdir()
            for a in ("spogliatoio-lazy.js", "app.js"):
                (d / "assets" / a).write_text(subprocess.run(["git", "-C", str(SITO), "show", "origin/gh-pages:assets/" + a],
                                                             capture_output=True, text=True).stdout)
            if nome == "prima":
                (d / "index.html").write_text(SORG.read_text())
            else:
                subprocess.run([sys.executable, str(CART / "spogliatoio.py"), str(SORG), str(d / "index.html")], check=True, capture_output=True)
        http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(tmp)))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        porta = srv.server_address[1]
        js = r"""
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const out={};
for(const nome of ['prima','dopo']){const p=await b.newPage({viewport:{width:320,height:700}});const err=[];
p.on('pageerror',e=>err.push(String(e)));
await p.route(/goatcounter|zgo\.at|fonts\.g/,r=>r.abort());
await p.goto('http://127.0.0.1:PORTA/'+nome+'/index.html#PROVA');await p.waitForTimeout(1200);
await p.click('#tabs button[data-t=swap]');await p.waitForTimeout(1500);
const r=await p.evaluate(()=>{const a=[...document.querySelectorAll('article.card')].find(x=>/Martinez L\./.test(x.textContent));if(!a)return null;
return {pr:a.querySelector('.ring text').getAttribute('aria-label')||a.querySelector('svg.ring').getAttribute('aria-label'),v:a.querySelector('.verdict').textContent,chips:[...a.querySelectorAll('.chip')].map(c=>c.textContent).join('')}});
const largo1=await p.evaluate(()=>document.documentElement.scrollWidth);
await p.click('#tabs button[data-t=mkt]');await p.waitForTimeout(2500);
const mkt=await p.evaluate(()=>document.getElementById('app').textContent.length);
const largo2=await p.evaluate(()=>document.documentElement.scrollWidth);
out[nome]={r,err,mkt,largo:Math.max(largo1,largo2)};await p.close()}
console.log(JSON.stringify(out));await b.close()})();
""".replace("PORTA", str(porta))
        res = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd=str(tmp))
        srv.shutdown()
        if res.returncode:
            ok(False, "browser: " + res.stderr[-400:])
            return
        out = json.loads(res.stdout.strip().splitlines()[-1])
        print("     prima:", out["prima"]["r"])
        print("     dopo: ", out["dopo"]["r"])
        a, b = out["prima"]["r"], out["dopo"]["r"]
        ok(bool(a and b), "Lautaro Martinez presente in Chi scambiare (Oranje VC)")
        if a and b:
            ok(b["chips"].endswith("IIII"), "giornate 7-10 segnate I")
            ok(b["v"] == "Tieni", "Lautaro: «Tieni» dopo la correzione (prima «%s»)" % a["v"])
        for nome in ("prima", "dopo"):
            ok(not out[nome]["err"], f"{nome}: nessun errore in console {out[nome]['err'][:2]}")
            ok(out[nome]["largo"] <= 320, f"{nome}: niente scorrimento laterale a 320 px ({out[nome]['largo']})")
            ok(out[nome]["mkt"] > 200, f"{nome}: Mercato Scambi disegnato")


prova_script()
prova_pagina()
print("PASS" if not errori else f"FALLITA: {len(errori)} controlli")
sys.exit(1 if errori else 0)
