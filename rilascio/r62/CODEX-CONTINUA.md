# Codex — completa O Girrr 6.2 senza pubblicarla
Data di consegna: 15 novembre 2026

## Ingresso
Lavora nel repository `giandjcosta/o-girrr-registro`. Il lavoro già impostato da ChatGPT è nella **PR #96**, ramo `chatgpt/integrazione-62-completa`; non partire da zero e non usare come base la PR #92 (`chatgpt/coordinamento-62`), che contiene grafica esplicitamente rifiutata.

Leggi per intero `AGENTS.md`, `STATO.md`, `REGOLE-VERSIONI.md`, `RAMIFICAZIONI.md`, `rilascio/r62/NOTE-CLAUDE.md`, `rilascio/r62/NOTE.md` nella PR #92 solo per recuperare requisiti e logica, `rilascio/r62/INTEGRAZIONE.md` e `rilascio/r62/ANNUNCIO-BOZZA.md`. Leggi anche `AGENTS.md` del sito `giandjcosta/o-fant-a-girrr`.

## Stato già confermato
- Sito vero alla **6.1**. La 6.1.1 **non** è stata pubblicata e, per decisione dell'utente, confluisce nella 6.2.
- Claude ha integrato in main del Registro le PR #93 e #94 (Campo con Campionato/Champions Cup, frecce, migliore in campo, simboli, Tabellone, Padri Fondatori). **PR #95 è unita** e documenta i cartellini in `data.json`, già presenti sul sito con PR #17 e autorizzazione dell'utente. Non rifare o cancellare questi lavori.
- Nella PR #96 esistono `rilascio/r62/applica.py` che prepara su una nuova copia di gh-pages prima 6.1.1 e poi i due script di Claude, `lab/novita-6-2.html` con le schede originali più le novità e `lab/confronto-62.html` che permette il confronto A/B in sola lettura.
- Recuperate da Work nella PR #96 le funzioni Radio/MVP e di scadenza, i test unitari e la SQL **solo proposta**. La SQL non è stata applicata.
- Le anteprime HTML del ramo sono state aperte e navigate da TinyFish. Il confronto A/B funziona, ma questo **non** certifica l'integrazione nelle pagine reali.
- Le Ramificazioni sono **già automaticamente aggiornate**: il ramo `chatgpt/integrazione-62-completa` è in `rami-dati.json` e PR #95 appare come merged in `ramificazioni-dati.json` del ramo tecnico `chatgpt/dati-ramificazioni`. Non modificare manualmente gli snapshot. La pagina deve continuare a dire «Sul sito la 6.1» finché la 6.2 non è davvero online.

## Decisioni definitive da rispettare
1. Giornale: **quattro pagine A4**, esattamente la grafica e impaginazione attuali; non usare il PDF a tre pagine né `impagina.cjs` della PR #92. Inserire, dove possibile, l'MVP e commenti autentici nel riquadro Curva originale.
2. Colori: **Lega** rosso in Campionato e azzurro in Champions Cup; **Stadio** UI tutta oro anche in Coppa, sfondi azzurri/rosati invariati, rosso di retrocessione/eliminazioni invariato. Niente oro su Albo e Derby. Per il Campo il cerchio oro è solo del migliore in campo, non di tutti i giocatori.
3. 6.1.1 dentro 6.2: grafico Carriera, testi leggibili, Curva fluida, «Campionato & Champions Cup» e «Peggiore» su una riga in PC. Mai pubblicare una 6.1.1 fittizia.
4. Conferenze › Precedenti: squadra e giornata, testo autentico quando esiste, «Dato non conservato» altrimenti.
5. Votazioni in Curva, un solo voto per squadra/persona secondo le regole già presenti; risultati chiusi limitati agli ultimi due. Fare entrambe le proposte **A** (in Girrr Sport) e **B** (nella Curva), rispettando la grafica reale e senza scegliere per l'utente. Nessun risultato proclamato prima del verdetto definitivo.
6. Scadenze **solo future**: vigilia e sfida fino al calcio d'inizio; dopo partita 48h dalla pubblicazione dei risultati; MVP entro 48h dalla prima apertura e prima del turno seguente; post 24h. Nessuna scadenza già annunciata modificata: MVP 7ª giornata 21/11/2026 alle 15:00 ora italiana.
7. Radio: **una sola frase** nella normale puntata, subito prima delle due battute di chiusura immutate. Mai produrre nuove voci, audio o puntate a pagamento solo per l'MVP.

## Da completare realmente
1. Preparare in locale una copia fresca di gh-pages e provare gli script con `python3 rilascio/r62/applica.py COPIA`. Verificare gli ancoraggi delle pagine reali, idempotenza e nessun file scritto nella copia originale.
2. Integrare votazioni, scelte personali, ultimi due risultati, Precedenti e MVP nelle **pagine originali**, Lega e Stadio, mantenendo menu, font, colori, stili, risposte alla tastiera e comportamenti esistenti. Non sostituire l'interfaccia reale con il simulatore di Work.
3. Correggere il Giornale originale su quattro pagine e provare PDF reali di più giornate; nessun taglio o duplicazione di testi, nessuna modifica di font e impaginazione rifiutata.
4. Testare il catalogo delle votazioni e la proposta SQL in isolamento, con sessioni concorrenti e casi di votazioni storiche. Non fare SQL sul progetto reale. Verificare compatibilità con vecchie RPC e autenticazione a codice; `SECURITY DEFINER` va sottoposta a revisione di sicurezza.
5. Collegare, in preparazione non pubblicata, i dati editoriali alle normali automazioni; nessun TTS o invio.
6. Collaudare 16 profili di schermo × Lega/Stadio × Chromium/WebKit/Firefox, testare ospite e squadra fittizia, Coppa, tastiera, Riduci movimento, errori console e 320 px, anche con i test delle Ramificazioni. Screenshot PC/TV e risultati salvati.
7. Aggiornare la pagina Lab 6.2 con foto PC/TV, ingresso nelle due grafiche e una preview navigabile integrata. Aggiornare `STATO.md`, `rilascio/r62/INTEGRAZIONE.md`, `ANNUNCIO-BOZZA.md`, senza inserire ancora la 6.2 in `versioni.json`.

## Stato CI al passaggio
PR #96 ha eseguito il workflow Registro run 43736049556, con gli stessi esiti per gruppi già visibili nella vecchia run 43722387690: `cornice-archivio` PASS nei tre motori, `filtri-panorama` e `browser` FAIL nei tre motori. Sono **anomalie preesistenti**, non prova che la 6.2 sia pulita. Il workflow dedicato `.github/workflows/integrazione-62-qa.yml` è stato aggiunto nella PR #96 ma non risultava ancora eseguito; attivarlo solo nella forma permessa da GitHub e leggere i risultati reali. Non presentare test non eseguiti come PASS.

## Pubblicazione e consenso
- **Nessun merge, push su gh-pages, modifica di main del sito o Supabase senza il successivo «Vai» esplicito di Gianluca**. Non usare push --force, non cancellare file, non applicare la SQL, non usare servizi a pagamento.
- Codex può continuare sul ramo `chatgpt/integrazione-62-completa` con commit `ChatGPT:` se è lui che opera come ChatGPT Codex; altrimenti usare il prefisso realmente previsto da AGENTS.
- Prima portare tutte le pagine e le prove nel Lab con autorizzazione di Gianluca; poi, **dopo un distinto «Vai, pubblica»**, seguire l'ordine `gh-pages` → QA online → eventuale `main` del sito; sincronizzare le sorgenti del Registro e annotare hash e `git revert`.
- Messaggio e changelog: **un solo messaggio della 6.2**, seguendo `REGOLE-VERSIONI.md`, con approvazione dell'utente **prima** del rilascio. Non annunciare funzioni non ancora integrate.

## Consegna
Restituisci i link precisi alla preview navigabile e alla PR, gli screenshot PC/TV Lega/Stadio, i test effettivamente riusciti/falliti e la lista dei blocchi rimasti. Non dichiarare finita la 6.2 prima della certificazione.
