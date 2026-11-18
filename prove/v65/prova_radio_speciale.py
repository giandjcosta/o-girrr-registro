#!/usr/bin/env python3
"""Collaudo puramente testuale della Radio 6.5: NON genera voci o audio."""
import copy
import json
import pathlib
import random
import sys

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "voci-src"))
from copione import build  # noqa: E402

D = json.loads((R / "voci-src/dati.json").read_text(encoding="utf-8"))
N = json.loads((R / "voci-src/nomi.json").read_text(encoding="utf-8"))
M = json.loads((R / "voci-src/mercato.json").read_text(encoding="utf-8"))
frase = "C'è chi ha passato la notte tra le palme e i neon di Miami"


def copione_di_prova(n):
    """L'unica modifica alla copia del campione è il numero; NON sono dati reali della giornata 8."""
    dati = copy.deepcopy(D)
    dati["aw"][-1]["n"] = n
    return build(dati, random.Random(20261118), M, N, {}, {}, {})


sette = copione_di_prova(7)
otto = copione_di_prova(8)
assert not any(frase in testo for _, testo, _ in sette), "La puntata 7 non deve contenere la battuta"
assert sum(frase in testo for _, testo, _ in otto) == 1, "Una sola battuta nella puntata 8"
print("Radio 6.5: giornata 7 senza omaggio; giornata 8 con una sola battuta. Test con campione storico, NON con risultati reali della giornata 8.")
print("\nApertura simulata giornata 8 (solo per controllo testuale):")
for voce, testo, _ in otto[:6]:
    print(f"{N.get(voce, voce)}: {testo}")
