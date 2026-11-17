# Rilascio 6.2.3 «Il Totogirrr su ogni schermo»

Preparato da Claude il 16 novembre 2026. Tipo: **correzione minore** (decisione di Gianluca: «per una correzione così piccola 6.2.3 è più adeguato»).

## Dove sta
- Script: `rilascio/r623/applica.py` (sopra la 6.2.2 pubblicata, `gh-pages` `64a243b`), Lab con `rilascio/r623/lab.py`, annuncio in `rilascio/r623/ANNUNCIO-BOZZA.json`, novità in `lab/novita-6-2-3.html`, prove in `prove/v623/`.
- Ramo di pubblicazione nel sito: `giandjcosta/o-fant-a-girrr`, ramo `claude/totogirrr-ui-responsive-b2pgee`, commit `082bd22` (37 file, base `gh-pages` `27c68c0`). Contiene `applica.py` già applicato e `versioni.json` con la 6.2.3.
- Il `main` del sito (calcoli e workflow) non cambia con la 6.2.3.
- Controllo fatto sulla copia esatta del ramo: 63 pagine (Spogliatoio e 10 pagine × Lega/Stadio × iPhone SE, PC 1280, TV), nessun errore nuovo, nessuno scorrimento laterale, pillola «V6.2.3». Solo Chromium: Safari e Firefox veri e telefoni veri non provati.

## Pubblicazione (la fa Gianluca)
1. PR nel sito: https://github.com/giandjcosta/o-fant-a-girrr/compare/gh-pages...claude/totogirrr-ui-responsive-b2pgee — base **`gh-pages`**, titolo `Gianluca: pubblicazione 6.2.3 «Il Totogirrr su ogni schermo»`.
2. In «Files changed» leggere `versioni.json` (messaggio e changelog). Se si cambia il messaggio, controllare che il JSON resti valido.
3. «Merge pull request» → «Confirm merge»: online in circa un minuto.
4. Se il sito ha problemi: pulsante «Revert» nella pagina della PR, poi unire la PR di ritorno.

## Dopo la pubblicazione
1. Sito vero: aprire https://giandjcosta.github.io/o-fant-a-girrr/girrr/ e `stadio/girrr/` (pillola «V6.2.3» in fondo alla Home), Totogirrr, Spogliatoio (`/o-fant-a-girrr/`), Carriera › Giro di boa, Curva, Girrr Sport › Video › Condividi; console senza errori nuovi. L'avviso «ViewTransition opt-in disabled» nel passaggio Home → Spogliatoio c'era già nella 6.2.2.
2. Registro: allineare `ufficiale/src/sito/` ai file cambiati su `gh-pages` (stesso elenco dei 37 file, esclusi quelli scritti dai workflow), segnare in `STATO.md` l'hash del merge su `gh-pages` e come tornare indietro (`git revert -m 1 <merge>` su `gh-pages`, oppure «Revert» della PR), spostare la 6.2.3 in «Fatto di recente» di `LAVORI-IN-CORSO.md`. L'allineamento automatico del Registro (`sincronizza-registro.yml`) porta Anteprima, Changelog e Archivio alla 6.2.3 da solo; si può lanciare a mano da Actions › Run workflow.

## Prompt per ChatGPT (se Claude non è disponibile)

Copia tutto il blocco qui sotto in ChatGPT.

```
Sei l'assistente di Gianluca per il progetto O Fant A Girrr (repository GitHub giandjcosta/o-fant-a-girrr = sito della lega, giandjcosta/o-girrr-registro = laboratorio e registro). Rispondi in italiano semplice, un passo alla volta, e aspetta che Gianluca ti dica «fatto» prima del passo successivo. Gianluca lavora dal browser (GitHub web, spesso dal telefono): niente terminale.

Regole del progetto da rispettare (sono in AGENTS.md e REGOLE-LAVORO.md del registro):
- Ogni ramo comincia con il nome di chi lo crea (gianluca/…, chatgpt/…), ogni commit e titolo di PR con «Nome: » (due punti attaccati al nome). Messaggi in italiano.
- Mai push forzati, mai cancellare rami di altri. Il sito vero cambia solo con il merge di Gianluca. Niente modifiche al database Supabase.
- I file scritti dai workflow (data.json, formazioni.json, toto-quote.json, riepiloghi/, girrr/dati/) non si toccano a mano.

Situazione: la versione 6.2.3 «Il Totogirrr su ogni schermo» è pronta. Claude ha preparato nel sito il ramo claude/totogirrr-ui-responsive-b2pgee (commit 082bd22, 37 file, con versioni.json già aggiornato). Tutti i dettagli sono in rilascio/r623/RILASCIO.md del registro: leggilo prima di cominciare.

Guida Gianluca in questi passi:
1. Aprire la PR di pubblicazione: https://github.com/giandjcosta/o-fant-a-girrr/compare/gh-pages...claude/totogirrr-ui-responsive-b2pgee — verificare che la base sia gh-pages (non main). Titolo: «Gianluca: pubblicazione 6.2.3 «Il Totogirrr su ogni schermo»».
2. Controllare in «Files changed» versioni.json: messaggio per il gruppo e changelog (regole di scrittura in REGOLE-VERSIONI.md del registro: niente Fantapunti né scommesse nel messaggio, dopo «·» sempre la maiuscola). Se Gianluca cambia il testo, fagli verificare che il JSON resti valido (virgolette e virgole).
3. Merge della PR («Merge pull request» → «Confirm merge»). Non cancellare il ramo finché il Registro non è allineato.
4. Controllo sul sito vero dopo 1-2 minuti: https://giandjcosta.github.io/o-fant-a-girrr/girrr/ e /stadio/girrr/ (pillola «V6.2.3» in fondo alla Home, a sinistra «Esci» se si è entrati), Totogirrr, Spogliatoio, Carriera › Giro di boa (senza «6.1 · Bilancio della stagione»), Curva, Girrr Sport › Video › Condividi. Chiedi a Gianluca cosa vede; se qualcosa è rotto, «Revert» nella pagina della PR e merge della PR di ritorno.
5. Nel registro, con una PR di Gianluca su un ramo gianluca/…: aggiornare STATO.md (in cima: 6.2.3 online, hash del merge su gh-pages, come tornare indietro) e LAVORI-IN-CORSO.md (6.2.3 in «Fatto di recente»). Se hai accesso al codice, allinea anche ufficiale/src/sito/ ai file cambiati su gh-pages; altrimenti lascialo scritto in LAVORI-IN-CORSO.md come «Da fare» per Claude.
6. Lanciare a mano l'allineamento del Registro: registro › Actions › «ChatGPT - Allineamento automatico del Registro» › Run workflow.
Alla fine riassumi a Gianluca cosa è stato fatto, cosa è stato controllato e cosa resta da fare.
```
