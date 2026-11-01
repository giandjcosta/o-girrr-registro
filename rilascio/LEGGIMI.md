# Preparazione delle cronache 5.5

Le cronache sono già abilitate nelle copie del futuro rilascio contenute in
`rilascio/cronache55/`: chiamante Curva, chiamante Radio e costruzione del PDF.
Non occorre tornare a sviluppare quei collegamenti dopo l'approvazione.
Il sito principale continua a usare i suoi file attuali fino al «Vai» di Gianluca.

`python3 rilascio/cronache55.py COPIA_MAIN_AGGIORNATA COPIA_GH_PAGES_AGGIORNATA USCITA_SEPARATA`
prepara undici file e due patch, senza applicarli, fare commit/push o eseguire
workflow e generatori vocali. Le copie qui consegnate derivano dai sorgenti
pubblici letti il 1 novembre. Il manifest contiene gli hash prima/dopo.
Se il post della Curva o i collegamenti attesi nei sorgenti sono cambiati,
la preparazione si ferma: integrare gli aggiornamenti, senza sovrascriverli.

- `main.patch`: aggiunge il flag ai preparatori chiamati da `dopo-giornata.yml`
  e `radio-giornata.yml` e include i moduli delle cronache. Nessuna modifica
  a `curva-subito.yml`: queste storie nascono dalla chiusura della giornata.
- `gh-pages.patch`: il normale `costruisci` del Giornale integra il trafiletto
  prima dell'impaginazione; le giornate parziali restano escluse. Include i
  tre moduli di supporto accanto al generatore. Non cambia `aggiorna-dati.yml`.
- La Radio usa i sorgenti già integrati nel Registro. Il flag nel futuro workflow
  la attiverà al rilascio, preservando fino ad allora il comportamento ufficiale.

Prova: `python3 prove/prova_rilascio_cronache55.py`. Applica le patch soltanto
a copie temporanee, estrae ed esegue le sole righe di preparazione e verifica
la chiave comune dei testi; il PDF include da solo la notizia anche con una
gara finita nel turno successivo. Nessun publisher, audio o database invocato.

Le due patch vanno incluse nel rilascio complessivo della 5.5 e ricontrollate sulle
versioni aggiornate del sito **prima del push autorizzato**. Il pacchetto storico
5.0 descritto sotto non è il comando di costruzione della 5.5 e non va eseguito
per questa preparazione (richiama `ufficiale/build.py`).

# Rilascio storico della 5.0

Tutto si prepara qui, senza toccare il sito vero.

1. `python3 aggiorna.py` e `python3 rilascio/pacchetto.py` costruiscono `rilascio/pacchetto/` (non è nel repo: si rifà ogni volta).
   - `gh-pages/`: pagine della Lega e dello Stadio, `app.html` (Girrr Sport, Spogliatoio, Totogirrr, Carriera), dati di partenza e le voci della radio (circa 8 MB).
   - `main/`: i workflow `dopo-giornata.yml` e `curva-coda.yml` e gli script `calcoli/`.
2. `python3 rilascio/applica.py --gh-pages <cartella gh-pages> --main <cartella main>` mostra cosa cambierebbe. Con `--vai` copia e fa i commit in locale, senza push.
3. Dopo il "vai" di Gianluca: push dei due rami. Non si tocca `aggiorna-dati.yml`.

Segreti da avere in GitHub (Settings, Secrets): `CURVA_URL`, `CURVA_KEY`, `CURVA_TEAM`, `CURVA_CODE`.

Dopo ogni giornata: Actions, "Calcoli dopo la giornata", Run workflow. Nei primi 14 giorni i post della Curva restano in coda: "Curva, coda di approvazione" per vedere l'elenco, approvare o scartare.
In `app.html` la modalità è "reale": database vero, squadra scelta al login. Nel sito di prova (anteprima) il database è finto.
