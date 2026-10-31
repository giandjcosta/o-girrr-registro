#!/usr/bin/env python3
"""Test selezione notizie e silenzi: non tocca sito né database."""
import importlib.util
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "calcoli/zone_classifica.py"
spec = importlib.util.spec_from_file_location("zone_classifica", path)
z = importlib.util.module_from_spec(spec)
spec.loader.exec_module(z)

squadre = [f"Squadra {i}" for i in range(10)]
def calendario(turni, leader=0, ultima=9):
    result=[]
    for n in range(1,turni+1):
        # ogni squadra affronta un'altra; leader e ultima si affrontano.
        mm=[[squadre[0],75,65,squadre[9],"3-0"]]
        mm += [[squadre[i],70,65,squadre[9-i],"1-0"] for i in range(1,5)]
        result.append({"n":n,"m":mm})
    return {"teams":[{"name":t} for t in squadre],"cal":{"lega":result}}

d=calendario(2)
assert z.evento(d) is None  # leader 2 giornate: niente ritornello
d=calendario(3)
attese={"squadre":{squadre[9]:{"attesa":2}}}
e=z.evento(d,attese)
assert e["tipo"]=="sorpresa" and e["squadra"]==squadre[9] and e["durata"]==3
e=z.evento(d)
assert e["tipo"]=="vetta" and e["durata"]==3 and e["canale"]=="radio"
assert z.evento(calendario(4)) is None  # non ripete ogni settimana
assert z.evento(calendario(5)) is None
assert z.evento(calendario(6)) is None
assert z.evento(calendario(7))["durata"]==7
# Giornate parziali o non consecutive non producono notizie spurie
d=calendario(3)
d["cal"]["lega"][-1]["m"][2][4]="-"
assert z.evento(d) is None
# Un campionato con soltanto 1 o 2 giornate non viene raccontato come serie.
assert z.evento(calendario(1)) is None
print("PASS zone classifica: soglie, crisi favorita, cooldown e risultati completi")
