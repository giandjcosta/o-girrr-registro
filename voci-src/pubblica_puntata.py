#!/usr/bin/env python3
"""Mette la puntata appena generata (lab/voci/puntata.mp3 e puntata.json) nel sito: puntata.mp3 e puntata.json correnti,
copia di archivio puntata-gNN.mp3 e voce in archivio.json.  Uso: python3 pubblica_puntata.py SITO LAB_VOCI N"""
import json, shutil, sys
from pathlib import Path
SITO, LAB, N = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
V = SITO / "girrr/voci"
t = json.loads((LAB / "puntata.json").read_text(encoding="utf-8"))
assert len(t) >= 20 and (LAB / "puntata.mp3").stat().st_size > 200_000, "puntata troppo corta: non pubblico"
shutil.copy(LAB / "puntata.mp3", V / "puntata.mp3")
shutil.copy(LAB / "puntata.mp3", V / f"puntata-g{N:02d}.mp3")
(V / "puntata.json").write_text(json.dumps(t, ensure_ascii=False), encoding="utf-8")
a = json.loads((V / "archivio.json").read_text(encoding="utf-8"))
a = [e for e in a if e.get("file") != f"puntata-g{N:02d}.mp3"]
a.insert(0, {"titolo": f"Radio Girrr · Giornata {N}", "tag": f"Lega Giornata {N}", "file": f"puntata-g{N:02d}.mp3", "testo": t})
(V / "archivio.json").write_text(json.dumps(a, ensure_ascii=False, indent=1), encoding="utf-8")
