# Lavori in corso · O Girrr

Quaderno comune di tutti gli assistenti (Claude, ChatGPT, Grok, Copilot, Perplexity…) e di Gianluca. Regole in `REGOLE-LAVORO.md`, punto 6.
**Aggiornalo quando cominci e quando ti fermi.** Chi riprende il lavoro parte da qui, poi legge `STATO.md`.

Formato di ogni voce: **cosa** · chi · stato · dove (rami, file, PR) · prossimo passo.
Stati: `Da fare` · `In corso` · `In prova nel Lab` · `Aspetta Gianluca` · `Bloccato`.

Ultimo aggiornamento: 16 novembre 2026, Claude.

## Aspetta Gianluca
- **6.3 «Il Totogirrr su ogni schermo»** · Claude · `Aspetta Gianluca` · ramo `claude/totogirrr-ui-responsive-b2pgee` del registro, `rilascio/r63/` (applica.py sopra la 6.2.2 online, lab.py, ANNUNCIO-BOZZA.json), `lab/novita-6-3.html`, `prove/v63/prova_toto63.js`. Schede del Totogirrr (scheda toccata tutta in vista, tocco breve, più trasparenti, non restano in alto), colonne su tablet/PC/TV, titolo a 320 px, Giro di boa senza «6.1». Prossimo passo: Gianluca prova nel Lab (dopo il merge del ramo), dice quale sfondo del Totogirrr ricorda e approva il messaggio; con il «Vai», `r63/applica.py` su `gh-pages` e `aggiungi.py --tipo medio`.
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
- 16 novembre 2026 · Claude · **6.2.2 online**: `gh-pages` `64a243b` («Carriera e Derby più fluidi»).
- 16 novembre 2026 · Claude · **6.2.1 online**: `gh-pages` `19653ba`, `main` del sito `4074b62`, provata sul sito vero (60 pagine).
- 16 novembre 2026 · Claude · Decisioni di Gianluca: Anteprima del Registro di nuovo alla versione online (6.2) in sola lettura, la 6.2.1 resta nel Lab; Ramificazioni solo a mano (`ramificazioni.yml` con il solo «Run workflow»).
- 16 novembre 2026 · Claude · `anteprima/build.py` di nuovo funzionante dopo il nuovo menu del Lab: l'allineamento automatico del Registro era fermo dalle 11:01 (PR #115).
- 16 novembre 2026 · Claude · Archivio con i prototipi e l'anteprima storica della 5.5. «Link utili» del README aggiornati. Regole comuni in `REGOLE-LAVORO.md` e questo quaderno.
