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

## Piano preliminare di attivazione (NON autorizzato)

1. Acquisire una copia verificata delle definizioni RPC/trigger esistenti, privilegi, conteggi dei voti e finestre; verificare i valori reali prima di ogni modifica.
2. In una finestra controllata, applicare **prima** `sql/votazioni-62-proposta.sql`, quindi `sql/finestre-62-proposta.sql`. Sono ancora bozze e richiedono un «Vai» specifico per Supabase.
3. Il catalogo deve essere pronto **prima** di pubblicare le pagine: `catalogo62.py` rifiuta normalmente di scrivere finché il numero è 6.1. Per il solo intervento di rilascio già autorizzato, utilizzare la **copia separata del backend del sito** preparata da `rilascio/r62/backend.py`, che include `calcoli/catalogo62.py`, e invocarla come `python3 COPIA_BACKEND/calcoli/catalogo62.py COPIA_GH_PAGES --vai --prima-del-rilascio`. Il flag anticipato funziona solo se `versioni.json` della copia di gh-pages è ancora alla 6.1; senza `--vai` non può operare. Non utilizzare questo comando prima dell'autorizzazione SQL di Gianluca. Non usare lo script originale nella cartella Registro: il suo percorso di import è progettato per la copia del backend.
4. Verificare con le RPC di sola lettura che il catalogo sia completo, che le preferenze precedenti siano immutate, che le conferenze siano ancora operative, e che la scadenza MVP della **7ª, 21 novembre 2026 ore 15:00 Europe/Rome**, sia invariata. Solo dopo le verifiche pubblicare le pagine 6.2 e aggiornare `versioni.json`, seguendo la procedura ufficiale e registrando SHA e rollback.

**Interruzione del vecchio voto «Quale sfida seguire»:** la funzione `sondaggio_vota` ora mantiene un percorso 6.1 se il catalogo non è ancora pronto; il downtime applicativo atteso per questo caso è **0 minuti se SQL e permessi sono corretti**. Non è una misura: non si possono quantificare i tempi reali di migrazione o degli eventuali errori da test locale. La nuova UI richiede comunque il catalogo e le RPC verificate prima di essere visibile. Non confondere la continuità della vecchia RPC con la disponibilità della 6.2.

**Limite dello schema delle conferenze:** le tabelle storiche `conf_risposta` / `conf_dopo` non dichiarano la stagione. Il trigger usa la stagione esplicita solo se la colonna esiste; in mancanza usa l'anno sportivo corrente (confine a luglio, fuso Roma). Non può distinguere in modo certo un inserimento retroattivo fuori stagione senza un campo stagione: per i backfill storici serve uno schema esplicitamente stagionalizzato o una procedura di importazione dedicata. Se non esiste una finestra corrispondente, il nuovo trigger lascia in vigore il comportamento precedente. Prima dell'applicazione reale verificare i casi storico/attuale sulla struttura effettiva.

**Stagione futura dei sondaggi delle sfide:** `sondaggio_private.voti` è indicizzata solo da (giornata, team): la prossima stagione riuserebbe le stesse chiavi. Proposta separata, NON inclusa nella 6.2: introdurre una chiave `(stagione, giornata, team)`, migrare tutti i voti esistenti alla stagione verificata, mantenere la vecchia RPC come adattatore alla stagione corrente fino all'aggiornamento dei client. Non riattribuire stagioni per ipotesi.
