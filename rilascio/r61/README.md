# Preparazione della 6.1

Regole e contenuti: [BILANCI-STAGIONE.md](../../BILANCI-STAGIONE.md).

Su una copia fresca della 6.0.1 pubblicata:

```sh
python3 rilascio/r61/applica.py COPIA
```

Non riapplicare r601. Il wrapper usa il pacchetto storico r602, comprendente condivisione, Carriera e bilanci collegati. Non modifica versioni.json e non pubblica. Il backend è preparato da r602/prepara_server.py, nella PR sito #13 in bozza.

La versione scelta da Gianluca è 6.1: al rilascio autorizzato usare `aggiungi.py --tipo medio`, senza registrare una versione 6.0.2 mai pubblicata. Nessun push su gh-pages/main del sito o avvio del workflow dati prima della certificazione del Lab e del Vai.
