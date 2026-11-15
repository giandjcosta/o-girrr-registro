#!/usr/bin/env python3
"""Prepara la 6.2 in una directory NUOVA, senza modificare gh-pages o Supabase.

La 6.1.1, mai pubblicata separatamente, confluisce nella 6.2.
Uso: python3 rilascio/r62/applica.py PERCORSO_COPIA_GH_PAGES [--out DIR_NUOVA]
Non usare questa preparazione come autorizzazione alla pubblicazione.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

RADICE = Path(__file__).resolve().parents[2]
PASSI = ("rilascio/r611/applica.py", "rilascio/r62/nativa.py", "rilascio/r62/campo_coppa.py", "rilascio/r62/testi.py", "rilascio/r62/campo_portieri.py", "rilascio/r62/giornale_mvp.py")

def prepara(sorgente: Path, uscita: Path):
    sorgente = sorgente.resolve()
    uscita = uscita.resolve()
    for rel in ("versioni.json", "girrr/campo.html", "stadio/girrr/campo.html", "girrr/tabellone.html", "stadio/girrr/tabellone.html"):
        if not (sorgente / rel).is_file():
            raise FileNotFoundError(f"Copia di gh-pages incompleta: {rel}")
    if uscita == sorgente or uscita.is_relative_to(sorgente) or sorgente.is_relative_to(uscita):
        raise ValueError("La destinazione deve essere separata dalla copia originale")
    if uscita.exists():
        raise FileExistsError(f"Non sovrascrivo una directory preesistente: {uscita}")
    shutil.copytree(sorgente, uscita, ignore=shutil.ignore_patterns(".git"))
    for passo in PASSI:
        print(f"Applico {passo} sulla NUOVA copia {uscita}", flush=True)
        subprocess.run((sys.executable, str(RADICE / passo), str(uscita)), check=True)
    print(f"Preparazione completata: {uscita}")
    print("Versioni e pubblicazione non modificate; verificare differenze e browser prima di ogni rilascio.")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("copia", type=Path)
    p.add_argument("--out", type=Path, default=None)
    a = p.parse_args()
    prepara(a.copia, a.out or a.copia.with_name(a.copia.name + "-anteprima-62"))
