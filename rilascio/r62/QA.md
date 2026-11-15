# Collaudo 6.2 — stato in corso, non pubblicata

Base isolata: gh-pages `98c0add`. Main sito letto: `40837e6`. PR di lavoro: #96. Versione vera 6.1.

- PostgreSQL 17 nativo locale: 19 verifiche superate, due connessioni concorrenti. Compresi primo voto, compatibilità vecchie RPC, privilegi, post precedente all'attivazione, MVP senza allenatori, archivio immutabile e conferenze pubblicate.
- Cinque prove testuali Radio/Giornale/scadenze superate. Nessun client TTS eseguito. ResourceWarning preesistente in `derby.py`, senza fallimenti.
- PDF 6ª e 7ª: quattro A4, nessun cambio di font/CSS, stessi livelli e scale di adattamento della base, tutte le pagine entro il piede. `lab/giornale-62/` contiene PDF, immagini e misure.
- Anteprima esportata: Chromium e WebKit, entrambe le grafiche, 320 px, scelte condivise, Precedenti e cambio ospite/squadra; zero richieste a Supabase e sessione personale conservata.
- Ramificazioni: Chromium e WebKit nelle tre viste, autonome e nel portale, quattro profili. Filtri/Panorama Chromium su 320 px, PC e TV. Corrette aspettative dei test rimaste sul vecchio ingresso; gli snapshot automatici non sono stati modificati.
- Matrice finale 16 profili × Lega/Stadio × tre motori: IN CORSO su GitHub Actions, da verificare a conclusione. Firefox locale non avviabile in questo container; la prova reale è affidata al runner con profilo NSS e TLS attivo.

I vecchi tentativi registrano errori effettivi: configurazione caricata dopo l'apertura dei Precedenti (corretto attendendo il caricamento), test che confrontava il primo elemento invece dell'ID del sondaggio (corretto), whitelist del collaudo 6.1.1 non aggiornata alle nuove letture (corretta), servizio di prova senza lettura avatar `curva_pimg` (corretto). Un colore WebKit letto durante la dissolvenza è ora verificato a transizione conclusa. Nessuna di queste run fallite vale come certificazione finale.

Dispositivi e schermi sono emulati, i motori sono reali. Safari su iPhone, Samsung Internet e TV fisiche non sono stati provati. Nessun risultato locale certifica Supabase reale, che resta invariato. Nessuna pubblicazione o audio.
