# Revisione della proposta SQL 6.2

Revisione statica e prove su PostgreSQL 17 locale, non una verifica del progetto Supabase reale. Proposte **non applicate**: `sql/votazioni-62-proposta.sql`, poi `sql/finestre-62-proposta.sql`.

- Le funzioni esposte non accettano SQL dinamico. Le `SECURITY DEFINER` fissano `search_path=''` e qualificano tabelle e funzioni applicative.
- Le letture anonime restituiscono aggregati e metadati pubblici. La preferenza personale richiede `curva_chk(team, code)`, secondo l'autenticazione già adottata dalla Lega; nessun nuovo affidamento su localStorage o `auth.uid()`.
- Schema e tabelle privati con RLS, accessi diretti revocati ad anon/authenticated. Catalogo di servizio, apertura e registrazione delle finestre eseguibili soltanto dal servizio. I privilegi delle funzioni preesistenti vengono conservati.
- Il voto prende il lock della votazione prima di decidere; controlla nuovamente l'orologio dopo l'attesa. Vincoli unici e primo voto immutabile valgono anche per i vecchi ingressi. I voti continuano a stare nelle tabelle originarie.
- Il catalogo non importa o cancella voti. Per le aperture storiche sconosciute resta null; non viene inventata una data. Per i post precedenti all'attivazione senza scadenza conservata non viene introdotta una chiusura retroattiva. La stagione usa la mezzanotte di Roma.
- La scadenza MVP già annunciata resta fissa; le giurie e la chiusura originale restano in uso anche senza voti degli allenatori. L'archivio conserva il risultato definitivo.
- Le conferenze pubblicate non possono cambiare testo; le automazioni possono continuare ad aggiornare gli altri campi di esito.

Prove effettive: `prove/v62/postgres.py` e `prove/v62/risultati-postgres.json`: 19 verifiche, due connessioni concorrenti, accessi con ruolo anon e credenziali errate. La prova PGlite dei browser è complementare e non sostituisce la contesa nativa.

## Attivazione soltanto dopo autorizzazione

Prima di una qualunque scrittura reale servono il Vai esplicito e la revisione del piano insieme alle altre pagine. Confrontare definizioni e privilegi reali con le dipendenze, acquisire le definizioni precedenti delle funzioni e uno snapshot dei metadati interessati. Non includere chiavi nei file o nei log.

Dopo l'eventuale applicazione autorizzata, inizializzare e confrontare il catalogo su una copia di rilascio alla 6.2 **prima di attivare i nuovi moduli**: `catalogo62.py COPIA --vai` resta qui solo un comando di piano. Verificare che nessuna preferenza precedente sia cambiata, che sfide e post puntino agli ID originali e che la 7ª conservi il 21 novembre alle 15:00 italiane. La copia del Giornale legge lo stesso dossier; la Radio conserva il suo normale controllo «puntata già uscita».

Il ritorno del frontend si farà con `git revert` del commit effettivamente pubblicato, ancora inesistente. Il ritorno delle funzioni SQL richiederà ripristinare le definizioni precedenti acquisite, senza eliminare voti, cataloghi o verdetti. Nessun rollback remoto viene eseguito durante questi collaudi.
