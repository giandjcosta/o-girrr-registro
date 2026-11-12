"""Rigenera tutte le anteprime dopo ogni modifica al Laboratorio, così restano allineate.
python3 aggiorna.py   (dalla cartella del repo)
 - anteprima/index.html     grafica nuova (Lobster, sfondo viola-blu, tab con loghi)
 - anteprima/attuale.html   stesse funzioni, grafica attuale del sito
 - ufficiale/index.html     ingresso della copia corrente in sola lettura
Per riallineare anche i rilasci: sincronizza.py --sito CHECKOUT_GH_PAGES."""
import subprocess, pathlib
R = pathlib.Path(__file__).resolve().parent
# ufficiale/build.py è uno strumento storico di rilascio: cerca il checkout
# di Claude e ricostruisce pagine con patch 5.0. Non va eseguito sul Registro.
for s in ["anteprima/build.py"]:
    subprocess.check_call(["python3", str(R / s)], cwd=R)
import shutil
shutil.copy(R / "lab" / "girrr-sport.png", R / "anteprima" / "girrr-sport.png")
