# Collaudo della preparazione 6.0 di ChatGPT

La copia completa unisce il rilascio di Claude fino a `3b85b41` e gli agganci di MVP, Derby e racconti. La base pubblicata è gh-pages `b0c5f45`; viene copiata, mai modificata. Non è stato eseguito un deploy né collegato il database della lega.

## Cosa viene verificato

- Modelli: giornate complete/parziali, incontri di Campionato e Coppa della stessa settimana, candidature, punti Derby, cronologia e firme dei fatti.
- Redazione: dieci racconti distinti nella settimana iniziale, episodi storici curati dell’Oranje, rifiuto dei testi mancanti o riferiti a risultati modificati, scadenza dal calendario reale e niente votazioni retroattive.
- Database: SQL eseguita due volte sullo stesso Postgres 17 locale reale, RLS e accessi diretti negati, amministrazione riservata al servizio, autenticazione della squadra, voto/cambio/ritiro, percentuali normalizzate, scadenza durante una transazione, chiusura senza allenatori e archivio immutabile. Contenitore di prova rimosso dopo il collaudo. Nessuna migrazione applicata a Supabase.
- Dipendenze server: helper della chiave incluso e identico al Registro; nuove chiavi server solo in `apikey`, vecchi JWT solo se `service_role` e del progetto corretto. Blocco prima della versione 6.0 verificato senza chiamate di rete.
- Git: veri repository temporanei con ramo principale, ramo unito, ramo non unito e gh-pages orfano. Versione nuova rilevata, snapshot invariato non riscritto, ramo tecnico escluso e nessuna origine inventata.
- Rilascio: applicazione completa senza `--lab` su copia fresca, agganci di prova assenti. Seconda applicazione del solo modulo tifosi identica byte per byte; sette video e cinque elementi di Condividi di Claude conservati.

## Browser

`prova_integrazione60_browser.py` attraversa nove pagine in ciascuna grafica (Home, MVP, Carriera, Derby, Curva, archivio, Video, Giornale e Tabellone) e Ramificazioni: **19 visite per profilo, 304 per motore, 912 per matrice completa**. Anche le richieste di lettura Supabase sono simulate: nessuna scrittura reale può uscire dal collaudo.

Sedici profili: iPhone 320, SE, 15 Pro e Pro Max; Galaxy S8, Pixel 7 e Galaxy S9+; iPad Mini, iPad orizzontale e Pro 11; Galaxy Tab S4 verticale e orizzontale; PC 1280, 1920 e 2560; Smart TV 1920×1080 a densità doppia. La verifica TV aggiuntiva ha completato 57 visite e nove percorsi interattivi nei tre motori, con zero problemi. Per la TV viene usata anche l’identità Tizen, verificando che il sito attivi davvero `tv-grande`. È un’identità emulata, non Samsung Internet su un dispositivo.

Si controllano errori JS/HTTP e scorrimento laterale, stile della Curva per sistema, presenza dei sette video, apertura di Condividi con cinque elementi e azioni visibili. Nei percorsi interattivi: voto/cambio/ritiro/persistenza ed errore senza voto fittizio, ritorno a Video, menu della Carriera, separazione Campionato/Coppa nei Derby e identità originale conservata. Per la mappa: filtri, selezione ramo, dettagli, tastiera, zoom, errore della copia remota e nuova versione senza ricaricare la pagina.

**Esito conclusivo: 912/912 visite, zero problemi**, più 57/57 verifiche TV e nove percorsi interattivi, zero problemi. Esecuzione [43339506523](https://github.com/giandjcosta/o-girrr-registro/actions/runs/43339506523), commit funzionale `da72bd4`; i tre motori e il job SQL sono tutti riusciti. JSON conservato in `prove/risultati-integrazione60.json`.

Esiti e collegamenti alle esecuzioni sono riportati nel [ticket di consegna #57](https://github.com/giandjcosta/o-girrr-registro/issues/57), insieme ai merge. Rapporti locali in `qa_artifacts/integrazione60-finale/` e `qa_artifacts/integrazione60-tv/`; la CI conserva JSON e foto negli artefatti per motore. Foto PC e TV salvate per entrambe le grafiche.

La copia autonoma `consegna/ramificazioni.html` è generata da `esporta_ramificazioni.py`: circa 710 KB, dati e codice incorporati, nessun server necessario. Verificata senza rete in Chromium, WebKit e Firefox, a 320 e 1920 px, con due grafi, filtro repository, apertura del commit e nessuna fuoriuscita laterale. È una consegna di revisione, non il file da distribuire su Pages.

## Correzioni del collaudo e limiti

Le prime esecuzioni hanno individuato problemi nel test: prefisso GitHub Pages mancante, intercettazione involontaria degli URL `blob:` di WebKit e intestazioni CORS mancanti nelle RPC simulate. Il router ora usa il percorso vero, intercetta solo URL HTTP locali e riproduce le intestazioni dell’API. Le esecuzioni precedenti restano consultabili; non sono state corrette retroattivamente né dichiarate tutte riuscite.

La prima raccolta Ramificazioni, scattata alla creazione del ramo, cercava il raccoglitore sul main dove non è ancora presente. Non ha scritto dati. Tolti gli eventi di creazione/eliminazione: il workflow opera soltanto dal main dopo il rilascio, ogni 15 minuti, su modifica del raccoglitore o su avvio manuale. Nuovi rami e versioni sono rilevati nel controllo successivo.

Samsung Internet, Safari su dispositivi e Chrome/Edge di marca non sono disponibili qui. I motori sono eseguiti realmente; schermi e identità sono emulati. La validità dei segreti server, gli advisors Supabase e le RPC sul progetto live vanno verificati dopo l’applicazione autorizzata dello schema e prima della pubblicazione. Non risultano collaudati da questa attività.

Lo script completo di Claude va applicato una volta su una copia fresca: la sua patch Curva non è idempotente. Il nuovo modulo tifosi è invece idempotente. Non distribuire la vecchia copia HTML della prova al posto delle pagine correnti.
