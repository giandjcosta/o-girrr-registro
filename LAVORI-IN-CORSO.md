# Lavori in corso · O Girrr

Quaderno comune di tutti gli assistenti (Claude, ChatGPT, Grok, Copilot, Perplexity…) e di Gianluca. Regole in `REGOLE-LAVORO.md`, punto 6.
**Aggiornalo quando cominci e quando ti fermi.** Chi riprende il lavoro parte da qui, poi legge `STATO.md`.

Formato di ogni voce: **cosa** · chi · stato · dove (rami, file, PR) · prossimo passo.
Stati: `Da fare` · `In corso` · `In prova nel Lab` · `Aspetta Gianluca` · `Bloccato`.

Ultimo aggiornamento: 16 novembre 2026, Claude.

## In corso · 18 novembre 2026 · ChatGPT
- **6.5 · Edizione speciale Radio, Video e Curva** · ChatGPT · `In prova nel Lab` · ramo `chatgpt/65-edizione-speciale`, PR verso `main` ancora senza merge. Radio: la battuta su Miami/forme della giornata si aggiunge **solo** se la puntata riguarda la giornata 8, dopo la fine delle partite. Video Remotion: grafica Notte Tropicale **solo** su giornata 8, con `SKIN=notte-tropicale` per la prova esplicita della 7 e `SKIN=off` per la regressione. Curva: post dei soli personaggi in date prestabilite 18–23/11, spariscono automaticamente il 24/11 alle 00:00 (ora italiana); banca sorgente e copie Lab sincronizzate. **Non eseguire** prove con Gemini, non pubblicare puntate né video e non unire la PR senza «Vai» esplicito. Da fare: prove di rendering reale Remotion, screenshot e controllo della puntata 8 quando i dati saranno disponibili; aggiornare la data finale dell'evento anche nel caricatore 6.5 di Claude.

## Aspetta Gianluca
- **Tema evento temporaneo (18–20 novembre)** · ChatGPT con Claude · `In corso` · ramo `chatgpt/theme-engine-vice-city-event` del registro. Claude rivede alle 4:30 e propone. Consigli di Claude: un solo caricatore in tv.js con finestra di date in ora italiana (si spegne da solo anche nella copia offline), ?evento=on/off per provarlo, nome e grafica originali (niente «Vice City», logo o caratteri Rockstar), niente animazioni continue sopra i contenuti, Lega/Stadio riconoscibili. Serve il «Vai, pubblica» di Gianluca prima del 18.
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
