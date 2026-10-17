"""Rigenera tutte le anteprime dopo ogni modifica al Laboratorio, così restano allineate.
python3 aggiorna.py   (dalla cartella del repo)
 - anteprima/index.html     grafica nuova (Lobster, sfondo viola-blu, tab con loghi)
 - anteprima/attuale.html   stesse funzioni, grafica attuale del sito
 - ufficiale/girrr/         pagine vere del sito (Albo, Derby, Curva) con le novità"""
import subprocess, pathlib
R = pathlib.Path(__file__).resolve().parent
for s in ["anteprima/build.py", "ufficiale/build.py"]:
    subprocess.check_call(["python3", str(R / s)], cwd=R)
import shutil
shutil.copy(R / "lab" / "girrr-sport.png", R / "anteprima" / "girrr-sport.png")
