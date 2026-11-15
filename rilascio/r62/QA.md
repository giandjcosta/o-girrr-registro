# Collaudo 6.2 — bozza pronta, non pubblicata

Base isolata: gh-pages `98c0add`. Main sito letto: `40837e6`. PR di lavoro: #96. Versione vera 6.1.

- PostgreSQL 17 nativo locale: 19 verifiche superate, due connessioni concorrenti. Compresi primo voto, compatibilità vecchie RPC, privilegi, post precedente all'attivazione, MVP senza allenatori, archivio immutabile e conferenze pubblicate.
- Cinque prove testuali Radio/Giornale/scadenze superate. Nessun client TTS eseguito. ResourceWarning preesistente in `derby.py`, senza fallimenti.
- PDF 6ª e 7ª: quattro A4, nessun cambio di font/CSS, stessi livelli e scale di adattamento della base, tutte le pagine entro il piede. `lab/giornale-62/` contiene PDF, immagini e misure.
- Anteprima esportata: Chromium e WebKit, entrambe le grafiche, 320 px, scelte condivise, Precedenti e cambio ospite/squadra; zero richieste a Supabase e sessione personale conservata.
- Ramificazioni: Chromium e WebKit nelle tre viste, autonome e nel portale, quattro profili. Filtri/Panorama Chromium su 320 px, PC e TV. Corrette aspettative dei test rimaste sul vecchio ingresso; gli snapshot automatici non sono stati modificati.
- Matrice 16 profili × Lega/Stadio × tre motori: SUPERATA nella run 43742212017 (commit 2d3f346), insieme a funzioni condivise, preview, Ramificazioni, Campo e 6.1.1. Le ripetizioni automatiche sui commit 98b90cc e 44dd624 sono ancora in corso: non sono dichiarate concluse. Il successivo ritocco del backend a fine stagione è stato verificato separatamente in isolamento, senza rete. Firefox locale non avviabile in questo container; la prova reale è affidata al runner con profilo NSS e TLS attivo.

I vecchi tentativi registrano errori effettivi: configurazione caricata dopo l'apertura dei Precedenti (corretto attendendo il caricamento), test che confrontava il primo elemento invece dell'ID del sondaggio (corretto), whitelist del collaudo 6.1.1 non aggiornata alle nuove letture (corretta), servizio di prova senza lettura avatar `curva_pimg` (corretto). Un colore WebKit letto durante la dissolvenza è ora verificato a transizione conclusa. Nessuna di queste run fallite vale come certificazione finale.

Dispositivi e schermi sono emulati, i motori sono reali. Safari su iPhone, Samsung Internet e TV fisiche non sono stati provati. Nessun risultato locale certifica Supabase reale, che resta invariato. Nessuna pubblicazione o audio.

## Consegna della bozza

Anteprime e immagini salvate nella PR #96, commit 98b90cc; testi aggiornati e prova del dopo partita finale nel commit 44dd624. Rapporto del backend in `prove/v62/risultati-backend.json`, protezione Radio già in archivio in `prove/v62/risultati-radio-cli.json`. Il browser condiviso non è controllabile per un errore AT-SPI; la navigazione della preview è stata invece verificata con Chromium e WebKit tramite il runner. Server locale sulla porta 8898. Nessuna certificazione del database reale e nessuna autorizzazione alla pubblicazione.

## Rettifica successiva: rubrica MVP e portieri

Giornale: rubrica autonoma dei tre candidati della giornata appena conclusa; Coro invariato, nessun verdetto precedente. PDF 6ª/7ª a quattro pagine con gli stessi livelli e scale di adattamento della base. In pagina 2 si compattano gli spazi e si distribuiscono Top/Flop su quattro colonne, conservando caratteri e contenuti. Cinque test testuali superati.

Portieri: pallone con piccola X e contatore, laterali al cerchio di casa e ospite. Test Chromium su 320 px/PC/TV nelle due grafiche, compreso il portiere ospite con gol subiti: simboli dentro il campo, nessuno scorrimento laterale. Queste modifiche non sono ancora certificate nei tre motori.
