#!/usr/bin/env python3
"""Prova della redazione di Girrr Sport (Claude, 11 novembre 2026, versione 5.8): controllo dei testi e giudizi nei calcoli.
Uso: python3 prove/prova_redazione.py   (usa redazione/redazione.json e redazione/dossier.json; nessun accesso alla rete)"""
import datetime, importlib.util as u, json, subprocess, sys, tempfile
from pathlib import Path
R = Path(__file__).resolve().parent.parent
ko = 0


def ok(c, m):
    global ko
    ko += not c
    print(("PASS " if c else "FAIL ") + m)


def carica(nome, rel):
    sys.argv = ["x"]
    s = u.spec_from_file_location(nome, R / rel); x = u.module_from_spec(s); s.loader.exec_module(x); return x


r = subprocess.run([sys.executable, str(R / "redazione/controlla.py"), str(R / "redazione/redazione.json")], capture_output=True, text=True)
ok(r.returncode == 0, "controlla.py accetta la redazione dell'8ª giornata")
rs = json.loads((R / "redazione/redazione.json").read_text())
rs["domande"]["WOA"][0]["a"][0]["t"] = "Vinciamo noi · la quota è alta."
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump(rs, f, ensure_ascii=False)
r = subprocess.run([sys.executable, str(R / "redazione/controlla.py"), f.name], capture_output=True, text=True)
ok(r.returncode == 1 and "dopo «·»" in r.stdout and "parola vietata" not in r.stdout, "controlla.py blocca la minuscola dopo «·», nessuna parola vietata")
le, pc = carica("le", "calcoli/leggi_eventi.py"), carica("pc", "calcoli/post_curva.py")
ora = datetime.datetime.now(datetime.timezone.utc).isoformat()
conf = [{"team": "Apo team", "giornata": 7, "risposte": [{"a": "free", "k": 1, "t": "Ci crediamo", "w": 0}, {"a": "free", "k": 1, "t": "Partita difficile", "w": 0}, {"a": "free", "k": 1, "t": "Frase offensiva", "w": 0}]},
        {"team": "WOA", "giornata": 7, "risposte": [{"a": "free", "k": 1, "t": "Vinciamo noi", "w": 0}, {"a": 0, "k": 0, "t": "Lo centriamo", "w": 1}, {"a": 1, "k": 1, "t": "Grazie", "w": 0}], "promessa": "Lo centriamo", "pesa": 1}]
red = {"controllato": True, "aggiornato": ora, "giudizi": {"Apo team|7": {"risposte": [
    {"i": 0, "k": 1, "w": 0, "pubblicabile": True, "nota": "x"}, {"i": 1, "k": 1, "w": 0, "pubblicabile": True, "nota": "x"}, {"i": 2, "k": 2, "w": 1, "pubblicabile": False, "nota": "x"}]}}}
c2, p2, d2, att = le.applica_redazione(conf, [{"team": "Apo team", "giornata": 7, "promessa": "Frase offensiva", "pesa": 1, "esito": "s"}], [], red)
ok(att == {"C7-WOA"}, "con la redazione attiva, la conferenza non ancora giudicata aspetta")
ev = [e for e in le.eventi_conferenza(c2) if e["team"] == "Apo team"][0]
ok(ev["risposte"][2] == "…" and "Frase offensiva" not in json.dumps(pc.post(ev), ensure_ascii=False), "la frase non pubblicabile non compare nel post")
ok(p2[0]["promessa"] == "Frase non riportata" and p2[0]["pesa"] == 2, "nella promessa: «Frase non riportata», peso dal giudizio")
_, _, _, att2 = le.applica_redazione(conf, [], [], dict(red, aggiornato="2026-01-01T00:00:00+00:00"))
ok(att2 == set(), "con la redazione ferma da più di 24 ore non aspetta niente")
c3, p3, _, att3 = le.applica_redazione(conf, [], [], None)
ok(c3 == conf and att3 == set(), "senza redazione tutto come prima")
print("Tutto a posto." if not ko else f"Problemi: {ko}")
sys.exit(1 if ko else 0)
