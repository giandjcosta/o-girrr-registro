# Lavori in corso · O Girrr

Quaderno comune di tutti gli assistenti (Claude, ChatGPT, Grok, Copilot, Perplexity…) e di Gianluca. Regole in `REGOLE-LAVORO.md`, punto 6.
**Aggiornalo quando cominci e quando ti fermi.** Chi riprende il lavoro parte da qui, poi legge `STATO.md`.

Formato di ogni voce: **cosa** · chi · stato · dove (rami, file, PR) · prossimo passo.
Stati: `Da fare` · `In corso` · `In prova nel Lab` · `Aspetta Gianluca` · `Bloccato`.

Ultimo aggiornamento: 16 novembre 2026, Claude.

## Aspetta Gianluca
- **Rilascio 6.2.1** («Correzioni e personaggi in Curva») · Claude · `Aspetta Gianluca` · Ramo `claude/fervent-thompson-rwlwrh` del registro, script `rilascio/r621/` (`applica.py`, `bug621.py`, `backend.py`, `lab.py`), annuncio approvato in `rilascio/r621/ANNUNCIO-APPROVAZIONE.json`. Prossimo passo: con il «Vai», `applica.py` su `gh-pages`, poi `versioni.json` con `aggiungi.py`, controllo del sito vero, poi `backend.py` sul `main` del sito.
- **SQL dei personaggi che votano durante la settimana** (`sql/mvp-personaggi-621.sql`) · Claude · `Aspetta Gianluca` · Provato su PostgreSQL locale (`prove/v62/postgres_personaggi.py`, 10 prove). Prossimo passo: dopo il rilascio 6.2.1 e con il «Vai», Gianluca lo incolla nell'SQL Editor di Supabase.

## In prova nel Lab
- **Carriera sul telefono** · Claude · `In prova nel Lab` · `rilascio/r621/bug621.py` (CENTRA, ORO_SCROLL, WEEK_MORPH, PILL_FILA) e anteprima in `lab/integrata-62/`. Ogni tocco su una pillola fa partire un solo scorrimento e la fila arriva sulla voce scelta. Prima tre codici muovevano la stessa fila e un ridisegno a metà la fermava (per esempio «Promesse» si fermava a 226 invece di 279). Prossimo passo: Gianluca prova sul suo telefono.
- **Tabellone della Fiducia a ogni ingresso nella Carriera** · Claude · `In prova nel Lab` · `bug621.py` (FID_TAB, FID_INIT, FID_GATE). Riparte ogni volta che si entra nella Carriera dalla Home o da un altro menu; cambiando scheda dentro la Carriera non riparte. Prima girava al massimo una volta ogni 5 minuti.
- **Niente alone al tocco su «‹ O Girrr» e sugli altri link** · Claude · `In prova nel Lab` · `bug621.py` (TOCCO, aggiunto in `tv.js`, che è in tutte le pagine; `tv.js?v=621`).
- **Notifiche: logo e titolo come nelle altre pagine** · Claude · `In prova nel Lab` · `bug621.py` (NOTIFICHE_NEW): «‹ O Girrr» sopra, logo 104×120 su PC e 60×70 su telefono, a 16 px dal titolo, come nell'Albo.
- **Schede del Derby e Campionato/Champions Cup** · Claude · `In prova nel Lab` · `rilascio/r621/file/*/derby.js`: su PC le schede sono di nuovo al centro. La regola cercava l'ultimo elemento della fila, che ora è la linea, non un pulsante. `bug621.py` (COMP in `tifosi.js`): i due pulsanti stanno affiancati su iPhone SE (andavano a capo per 1 px); nello Stadio sono tutto oro, anche in Champions Cup.
- **Registro: barra in alto più piccola e un solo interruttore Lega/Stadio** · Claude · `In prova nel Lab` · `registro.css`, `registro.js` e `rilascio/r62/lab62.js`, che ora ha una riga di prova compatta al posto dei link blu sottolineati.

## Da fare
- **Verificare Spogliatoio e Totogirrr nella 6.2.1** (elenco di Gianluca del 16 novembre) · Nessuno ancora · `Da fare`.
- **Safari e Firefox veri, e telefoni veri** · Tutti · `Da fare` · Nell'ambiente di Claude c'è solo Chromium. I workflow di GitHub provano anche WebKit e Firefox, ma non i dispositivi veri.

## Fatto di recente
- 16 novembre 2026 · Claude · Decisioni di Gianluca: Anteprima del Registro di nuovo alla versione online (6.2) in sola lettura, la 6.2.1 resta nel Lab; Ramificazioni solo a mano (`ramificazioni.yml` con il solo «Run workflow»).
- 16 novembre 2026 · Claude · `anteprima/build.py` di nuovo funzionante dopo il nuovo menu del Lab: l'allineamento automatico del Registro era fermo dalle 11:01 (PR #115).
- 16 novembre 2026 · Claude · Archivio con i prototipi e l'anteprima storica della 5.5. «Link utili» del README aggiornati. Regole comuni in `REGOLE-LAVORO.md` e questo quaderno.
