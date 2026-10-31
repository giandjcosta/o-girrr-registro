# O Girrr 5.3 — integrazione per la revisione di Gianluca

## Provenienza e confini

Ramo `chatgpt/completamento-53-campo`, creato dalla PR #41 (`03a2a9f`). Integra il lavoro della #42 e del ramo `chatgpt/lavori-31-ottobre` con una normale unione **locale sul nuovo ramo**, risolvendo i conflitti nei sorgenti e rigenerando gli output. La [PR #43](https://github.com/giandjcosta/o-girrr-registro/pull/43), bozza non unita, punta a `chatgpt/anteprima-53-integrata`. Nessuna modifica ai rami degli altri, nessun force-push, nessuna unione di PR. La #39 resta `dirty`; #41 e #42 restano aperte.

Il riferimento Campo è **l'immagine allegata da Gianluca**, poi verificata nella [pagina originale indicata dall'utente](https://sg-wc2026.com/2026-world-cup-x-platform-data-modules-guide). La [prima illustrazione dell'articolo](https://sg-wc2026.com/uploads/2026-04-09/150428-2026-world-cup-x-platform-data-modules-g-img-1.webp), vista integralmente, è la stessa dello screenshot: cockpit blu, campo verde con porte in alto e in basso, navigazione laterale, strumenti e KPI. È un'illustrazione nell'articolo; non è stata verificata una dashboard interattiva di quel sito. Il Campo riprende questa disposizione con componenti propri e dati della Lega. Nessun asset di terzi copiato nell'app. La grafica resta da approvare manualmente; i test non costituiscono approvazione estetica.

Nessuna modifica al repository pubblicato `o-fant-a-girrr`, alle sue Actions, al database o alla pubblicazione. Nessun audio. Le sole risorse remote lette sono dati e file pubblici/documentazione; i controlli del database sono locali.

## Percorsi e link

Base delle prove:
`https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/completamento-53-campo/anteprima/5.3/`

- Selettore: `index.html`.
- Home: `index-lega.html`, `index-stadio.html`.
- Tabellone: `tabellone-lega.html`, `tabellone-stadio.html`.
- Campo: `campo-lega.html`, `campo-stadio.html`.
- Curva: `curva-lega.html`, `curva-stadio.html`.
- Albo/Annuario: `albo-lega.html`, `albo-stadio.html`.
- Notifiche: `notifiche-lega.html`, `notifiche-stadio.html`.

Anche l'ingresso abituale **Registro → Anteprima 5.3** (`ufficiale/`) apre queste pagine. La cornice conserva la posizione durante il cambio skin e migra gli indirizzi delle vecchie Home memorizzati dal browser. Le card native della Home aprono Tabellone, Albo e Curva; Notifiche ha il proprio collegamento contestuale. Campo, Centro partita e confronto giornate stanno nel Tabellone. **Eliminata la seconda barra a cinque sezioni** della vecchia prova. Il menu originale della Curva funziona.

La prova diretta della CDN era bloccata da HTTP 403 nell'ambiente: **accessibilità pubblica e cache raw.githack non certificate**. I percorsi browser certificati sono serviti via HTTP locale. Nessun aggiramento del blocco. I link di GitHub e le immagini nel repository offrono una consegna verificabile anche senza CDN.

## Integrato e verificato

- **Home:** «Oggi al Girrr» compatto con selezione squadra, risultato, prossimo avversario e posizione; tutte le card e sezioni originali conservate. Una cronaca rilevante può emergere tra le notizie.
- **Tabellone:** Campionato e Champions Cup, giornate, risultati, gruppi e accesso a quarti/semifinali/finale, forma, frecce affiancate, grafico della posizione, media/max/min, prossimo turno, Derby e Regole. Colori solo su fasce laterali e numeri delle posizioni; DR/Pt chiari e Fantapunti/intestazioni azzurri dopo il confronto con il Tabellone originale. Posizioni più piccole e distanziate dalle barre; legenda senza posizioni; velatura e nome oro della squadra scelta ripristinati. Le giornate incomplete non vengono trattate come chiuse. Risultato, Fantapunti e punti assegnati nel turno sono distinti nel Centro partita.
- **Campo:** layout a tre colonne oltre alla sidebar su desktop; campo centrale, strumenti a sinistra, KPI a destra, grafici in basso. Tablet a due colonne e telefono verticale. Solo risultati e metriche del calendario; anelli = vittorie / gare complete. Due grafici cumulativi con la stessa scala. Giorno, partita e skin nell'URL; ritorno alla giornata scelta.
- **Albo:** tutte le sezioni del Lab riutilizzate nella build 5.3, singola fila scorrevole, tab attiva conservata durante il cambio skin. Annuario espandibile per stagione, record storici non conservati espliciti, campione/podio/ultimo non assegnati durante la stagione. Calcolo condiviso in `lab/annuario.js`: niente seconda logica dei record. Pareggi esclusi dalle vittorie; marcatori definiti come gol dei giocatori in rosa nelle giornate di Serie A associate, senza inventare una corrispondenza fra quei gol e il risultato della Lega. Costi in fantacrediti e punteggi in Fantapunti.
- **Curva:** personaggi originali e banca CVB conservati, variazioni sui risultati, tono distinto e una cronaca di classifica quando significativa. Sondaggio commentabile e voto modificabile, senza duplicare il conteggio votando due volte. Menu nativo Esplora/Home funzionante. I contenuti di prova sono identificati come locali.
- **Notifiche:** pagina dedicata, filtri e stato letto locale; eventi derivati dai dati pubblici e dal sondaggio di prova. Nessun errore delle automazioni mostrato agli allenatori.
- **Cronache:** priorità e cooldown, crisi delle favorite, permanenze, sorpassi, podio, risalite e movimenti ampi su tre turni. Chiave con stagione e prove delle posizioni iniziali/finali. Preparazione GS/profilo Giornale/commento/Radio/PDF nel Registro. Nessun invio.

## Cosa è locale o sperimentale

Il sondaggio, i commenti inseriti dall'utente e lo stato letto delle notifiche vivono **solo in localStorage sul dispositivo**. Non sono condivisi tra allenatori. Nessuna push, autenticazione o servizio di recapito implementato. Il feed reale degli utenti della Curva non viene interrogato in questa prova: si preservano grafica e personaggi, non si simula di avere caricato le attività del database.

`anteprima/preview-guard.js` intercetta le richieste ai domini Supabase prima degli script originali: risposte locali vuote per le RPC di lettura previste; altre operazioni rispondono localmente 403; XHR e beacon bloccati. Il test con un oggetto `Request` di scrittura verifica **zero richieste al dominio del database**. Non è una sostituzione della sicurezza server e non va distribuito come backend.

`anteprima/5.3/cronache.json` proviene dalla logica Python condivisa e da una copia pubblica ridotta del calendario, non da fatti inventati. Il client confronta la firma di tutte le giornate complete: quando i dati sono diversi, non mostra vecchie cronache come nuove. Per aggiornare la copia locale:

```bash
python3 anteprima/aggiorna_snapshot53.py
python3 anteprima/build.py
```

Questi comandi non pubblicano nulla. Prima del rilascio servirà collegare un aggiornamento approvato alla chiusura della giornata. Anche il PDF richiede che il processo approvato passi i testi arricchiti dall'adattatore al generatore originale; il PDF locale di prova è nei risultati della #42.

Le vecchie pagine `lab/prova-*` rimangono prototipi di confronto. Non sono più necessarie per arrivare alle funzioni dall'Anteprima. Le prove #40 restano un archivio di idee, non un riferimento grafico.

## Build e QA

`python3 anteprima/build.py` genera le due app, la cornice e le pagine `anteprima/5.3/` con `build53.py`. I sorgenti fermi della #41 per Home/Curva/Notifiche sono in `anteprima/sorgenti/53/`; Tabellone e Albo usano i sorgenti completi già mantenuti nel Lab. I tag base remoti sono rimossi; l'Albo usa una base locale controllata. Nessun link rimanda al ramo precedente per caricare il JS/CSS della 5.3.

**Superati localmente:**

- Build riproducibile, collaudi Anteprima, milestone/premi, fiducia universale e Moviola.
- Test zone e cronache integrate: turni parziali/saltati, priorità, cooldown, chiavi, commenti, attesa Coppa, snapshot Radio disallineato, archivio e quattro semi del copione testuale.
- PDF costruito con il generatore originale letto in sola lettura: cronaca nella seconda pagina, tutte e quattro le pagine nei margini.
- Annuario controllato con fixture: stagione non conclusa, turno parziale, buco nel calendario e pareggi.
- **5.3 completa, dieci combinazioni:** entrambe le skin a 320/390/768/1280/1440 px. Click reali Home → Tabellone/Centro partita/confronto/Coppa → Campo → Tabellone → Home → Albo/Annuario → Home → Curva/voto/commento → Notifiche. Nessun overflow, errore JS, errore console o risposta 404 nei percorsi provati; zero richieste al database.
- Ingresso abituale dal Registro, vecchia URL memorizzata e cambio skin nella cornice: cinque viewport, Tabellone/Campo/Albo, selezione mantenuta e riapertura.
- Percorsi della precedente integrazione e prove isolate a 320/768/1280 rieseguiti. Quarti, semifinali e finale aperti anche in una prova dedicata; menu originale Curva Esplora/Home collaudato.

**Problemi storici distinti:** la QA Fiducia `41228042480` era fallita sul lavoro precedente: cercava il vecchio blocco «Premi Carriera in simulazione» e il selettore squadra rimosso nelle Anteprime personali. Non è stata modificata la UI per soddisfare questi selettori obsoleti; il test resta da riallineare. Il precedente YAML non valido della milestone è già corretto nel lavoro integrato. Le run precedenti verdi non vengono attribuite all'ultimo commit.

**Non verificati:** Safari/iPhone fisico, accesso pubblico via CDN, account veri, caricamento del feed reale Curva, push, sincronizzazione multiutente, giornata futura reale e distribuzione in produzione. Nessuna di queste funzioni è dichiarata pronta.

Screenshot PC/telefono e rapporti: `prove/risultati-53-completa/`. Tutti gli screenshot delle altre larghezze sono prodotti dalla QA nei relativi artefatti.

CI nuova, primo tentativo (`41234940046`): importazione anticipata e inutilizzata di Playwright dal modulo fixture, prima del passo di installazione. Dipendenza rimossa. La run successiva `41235097625` supera build, collaudi dati, dieci percorsi precedenti e cinque ingressi dal Registro; si ferma nell'Annuario Stadio a 768 px perché legge il testo appena apparse le stagioni storiche, prima del caricamento del calendario corrente. Il test ora attende esplicitamente «Da assegnare», mantenendo la verifica del risultato. Rieseguite tutte le dieci combinazioni locali con esito PASS. Nuova run CI da verificare separatamente.


Revisione grafica del Tabellone dopo gli screenshot di Gianluca: dieci verifiche specifiche di colori, dimensioni, spaziatura, selezione squadra e navigazione superate. Screenshot aggiornati e rapporto in `prove/risultati-tabellone-feedback/`; le immagini di classifica nella precedente galleria documentano la versione prima di questo feedback.
