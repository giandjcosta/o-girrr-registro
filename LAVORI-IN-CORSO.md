# Lavori in corso · O Girrr

Quaderno comune di tutti gli assistenti (Claude, ChatGPT, Grok, Copilot, Perplexity…) e di Gianluca. Regole in `REGOLE-LAVORO.md`, punto 6.
**Aggiornalo quando cominci e quando ti fermi.** Chi riprende il lavoro parte da qui, poi legge `STATO.md`.

Formato di ogni voce: **cosa** · chi · stato · dove (rami, file, PR) · prossimo passo.
Stati: `Da fare` · `In corso` · `In prova nel Lab` · `Aspetta Gianluca` · `Bloccato`.

Ultimo aggiornamento: 16 novembre 2026, Claude.

## In prova nel ramo di fusione — ChatGPT, 17 novembre 2026
- **Tema evento Notte Tropicale × Miami Nights V3** · ChatGPT (grafica) + base Claude (motore) · `In prova nel Lab` solo sul branch `chatgpt/miami-nights-fusione-lab`, derivato dal branch Claude al commit `9431b587`. Aggiornati esclusivamente CSS evento e copia Lab con nuovi header, tab, card, KPI, big match e pannelli fotografici sulle pagine vere. Controlli statici 10/10; browser reale NON verificato. Dettagli in `temi/FUSIONE-MIAMI-NIGHTS-RAPPORTO.md`. Prossimo passo: visual QA Lega/Stadio 320–2560 px, test clic/touch e review di Claude; non pubblicare senza «Vai, pubblica».

## Aspetta Gianluca
- **Tema evento temporaneo (18–20 novembre)** · ChatGPT e Claude · `In corso`. ChatGPT: demo a sé in `temi/` sul ramo `chatgpt/theme-engine-vice-city-event`. Claude: caricatore con le date `temi/evento-loader.js` (prova `temi/prova_evento.js`) e proposta «Notte Tropicale» sopra le pagine vere (`temi/notte-tropicale/`: scena originale, griglia neon, schede scure; variante con foto vera CC0 `?evento-sfondo=foto`, crediti in `temi/notte-tropicale/CREDITI.md`, titoli in Kaushan Script; nel Lab solo a mano con `?evento=notte-tropicale`, aggiunta da `temi/notte-tropicale/lab.py`, da rilanciare dopo ogni `rilascio/rXYZ/lab.py`). Serve il «Vai, pubblica» di Gianluca prima del 18; nome definitivo da scegliere (non «Vice City»). Divisione proposta da ChatGPT il 17 novembre (commento sulla PR #125), da confermare da Gianluca: **Claude** integrazione tecnica (`temi/evento-loader.js`, date, `?evento=`, copia offline, inserimento nelle pagine vere, prove Lega/Stadio e browser); **ChatGPT** direzione artistica (foto, titoli al neon, card e tabellone dal riferimento rosa/viola) solo in `temi/` del suo ramo. Il caricatore di Claude è l'unico che accende il tema nelle pagine vere; `theme-engine.js` resta una demo. CSS finale scelto da Gianluca dopo la prova in Lega e Stadio.
- **SQL dei personaggi che votano durante la settimana** (`sql/mvp-personaggi-621.sql`) · Claude · `Aspetta Gianluca` · Provato su PostgreSQL locale (`prove/v62/postgres_personaggi.py`, 10 prove). La 6.2.1 è online: Gianluca lo incolla nell'SQL Editor di Supabase prima dell'apertura della votazione della 8ª giornata.

## Online con la 6.2.2 (16 novembre, `gh-pages` `64a243b`)
- **Carriera sul telefono** · Claude · `In prova nel Lab` · `rilascio/r622/` e anteprima in `lab/integrata-62/`. Ogni tocco su una pillola fa partire un solo scorrimento e la fila arriva sulla voce scelta. Prima tre codici muovevano la stessa fila e un ridisegno a metà la fermava (per esempio «Promesse» si fermava a 226 invece di 279). Prossimo passo: Gianluca prova sul suo telefono.
- **Tabellone della Fiducia a ogni ingresso nella Carriera** · Claude · `In prova nel Lab` · `rilascio/r622/`. Riparte ogni volta che si entra nella Carriera dalla Home o da un altro menu; cambiando scheda dentro la Carriera non riparte. Prima girava al massimo una volta ogni 5 minuti.
- **Niente alone al tocco su «‹ O Girrr» e sugli altri link** · Claude · `In prova nel Lab` · `rilascio/r622/`.
- **Notifiche: logo e titolo come nelle altre pagine** · Claude · `In prova nel Lab` · `rilascio/r622/`: «‹ O Girrr» sopra, logo 104×120 su PC e 60×70 su telefono, a 16 px dal titolo, come nell'Albo.
- **Schede del Derby e Campionato/Champions Cup** · Claude · `In prova nel Lab` · `rilascio/r622/`: su PC le schede sono di nuovo al centro. La regola cercava l'ultimo elemento della fila, che ora è la linea, non un pulsante. `rilascio/r622/` (aggiunta in `tifosi.js`): i due pulsanti stanno affiancati su iPhone SE (andavano a capo per 1 px); nello Stadio sono tutto oro, anche in Champions Cup.
- **Registro: barra in alto più piccola e un solo interruttore Lega/Stadio** · Claude · `In prova nel Lab` · `registro.css`, `registro.js` e `rilascio/r62/lab62.js`, che ora ha una riga di prova compatta al posto dei link blu sottolineati.

## Da fare
- **Verificare Spogliatoio e Totogirrr nella 6.2.1** (elenco di Gianluca del 16 novembre) · Nessuno ancora · `Da fare`.
- **Safari e Firefox veri, e telefoni veri** · Tutti · `Da fare` · Nell'ambiente di Claude c'è solo Chromium. I workflow di GitHub provano anche WebKit e Firefox, ma non i dispositivi veri.

## Fatto di recente
- 17 novembre 2026 · Claude · **6.2.4 online** (con il «Vai» di Gianluca): `gh-pages` `6276dc6` (PR #22 del sito), 63 pagine controllate sul sito vero. Per tornare indietro: «Revert» della PR #22.
- 16 novembre 2026 · Gianluca e Claude · **6.2.3 online**: `gh-pages` `4b0fc71` (PR #21 del sito, unita da Gianluca), 63 pagine controllate sul sito vero. Per tornare indietro: «Revert» della PR #21.
- 16 novembre 2026 · Gianluca · **First Pull Request made by me**: una riga nel quaderno, commit e merge dal browser
- 16 novembre 2026 · Claude · **6.2.2 online**: `gh-pages` `64a243b` («Carriera e Derby più fluidi»).
- 16 novembre 2026 · Claude · **6.2.1 online**: `gh-pages` `19653ba`, `main` del sito `4074b62`, provata sul sito vero (60 pagine).
- 16 novembre 2026 · Claude · Decisioni di Gianluca: Anteprima del Registro di nuovo alla versione online (6.2) in sola lettura, la 6.2.1 resta nel Lab; Ramificazioni solo a mano (`ramificazioni.yml` con il solo «Run workflow»).
- 16 novembre 2026 · Claude · `anteprima/build.py` di nuovo funzionante dopo il nuovo menu del Lab: l'allineamento automatico del Registro era fermo dalle 11:01 (PR #115).
- 16 novembre 2026 · Claude · Archivio con i prototipi e l'anteprima storica della 5.5. «Link utili» del README aggiornati. Regole comuni in `REGOLE-LAVORO.md` e questo quaderno.
