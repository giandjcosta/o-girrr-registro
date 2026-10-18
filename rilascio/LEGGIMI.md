# Rilascio della 5.0

Tutto si prepara qui, senza toccare il sito vero.

1. `python3 aggiorna.py` e `python3 rilascio/pacchetto.py` costruiscono `rilascio/pacchetto/` (non è nel repo: si rifà ogni volta).
   - `gh-pages/`: pagine della Lega e dello Stadio, `app.html` (Girrr Sport, Spogliatoio, Totogirrr, Carriera), dati di partenza e le voci della radio (circa 8 MB).
   - `main/`: i workflow `dopo-giornata.yml` e `curva-coda.yml` e gli script `calcoli/`.
2. `python3 rilascio/applica.py --gh-pages <cartella gh-pages> --main <cartella main>` mostra cosa cambierebbe. Con `--vai` copia e fa i commit in locale, senza push.
3. Dopo il "vai" di Gianluca: push dei due rami. Non si tocca `aggiorna-dati.yml`.

Segreti da avere in GitHub (Settings, Secrets): `CURVA_URL`, `CURVA_KEY`, `CURVA_TEAM`, `CURVA_CODE`.

Dopo ogni giornata: Actions, "Calcoli dopo la giornata", Run workflow. Nei primi 14 giorni i post della Curva restano in coda: "Curva, coda di approvazione" per vedere l'elenco, approvare o scartare.
In `app.html` la modalità è "reale": database vero, squadra scelta al login. Nel sito di prova (anteprima) il database è finto.
