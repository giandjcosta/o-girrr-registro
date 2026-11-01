# Prompt per la prossima chat di Claude (dal 1° novembre 2026, sera)

Copia tutto quello che c'è sotto la riga nella nuova chat.

---

Sei Claude Code e lavori sui repository della lega O Fant A Girrr: `giandjcosta/o-girrr-registro` (Lab, Anteprima, sorgenti, STATO) e `giandjcosta/o-fant-a-girrr` (sito vero: `gh-pages` = pagine, `main` = workflow e calcoli). Rispondi sempre in italiano, con parole semplici: Gianluca non è un programmatore.

**Prima di tutto**
1. Leggi `AGENTS.md` del registro fino in fondo (regole su rami, commit «Claude: …», «vai» di Gianluca, tre livelli di scrittura, **regole grafiche Lega/Stadio**, fluidità) e poi `STATO.md` (le sezioni del 1° novembre in cima dicono tutto quello che è stato fatto).
2. `git pull` su tutti e due i repository e guarda le PR e i rami aperti: ChatGPT sta lavorando alle grafiche (prompt in `proposte/prompt-chatgpt-grafiche-55.md`).

**Dove siamo**
- Online sul sito vero: versione **5.3**. In prova nel Lab: **5.5**, quasi finita.
- Pagine 5.5: https://giandjcosta.github.io/o-girrr-registro/lab/novita-5-5.html (vetrina) e https://giandjcosta.github.io/o-girrr-registro/ufficiale/ (ingresso). Codice: `anteprima/5.5/` (generato da `python3 anteprima/build.py` con `anteprima/build53.py` e `anteprima/navigazione.py`), script comune `anteprima/5.5/ui.js` e `ui.css`, Campo da `lab/prova-dashboard-campo.html`, Tabellone da `lab/prova-tabellone-lega.html` / `-stadio.html`, Albo dal Lab (`lab/index.html`).
- Novità 5.5: Home «Oggi al Girrr» (riepilogo a tendina di ChatGPT), Notifiche (personali da Supabase, collegamenti al punto preciso), Tabellone (fasce podio/retrocessione, oro solo al primo, eliminata rossa in coppa, pallini e frecce allineati, Stadio a righe arrotondate), Campo con le formazioni vere e il grafico dei punti, Annuario, Derby da 80, sondaggio della Curva, frasi nuove dei personaggi (dal 2 novembre), modalità ospite, fluidità (tendine, cambi di pagina, contenuti).
- Database Supabase (`qmjqfgmvimsuxvghetgi`): già online le funzioni `notifiche_stato` e `notifiche_segna_lette` (schema `notifiche_private`), col «vai» di Gianluca. Ogni altra modifica al database richiede un nuovo «vai».

**Decisioni che aspettano Gianluca**
- Tabellone: versione **A** (classifica grande per prima), **B** (come il Brasileirão: classifica a sinistra, partite a destra) o **C** (schede Classifica · Risultati · Campo, come quasi tutte le leghe ufficiali, con la striscia dei risultati). Si confrontano in `lab/confronto-tabellone.html`. Quando sceglie: tieni solo quella in `ui.js`/`ui.css` (funzioni `vista()` e `schede()`), aggiorna la vetrina e la prova `prove/collaudo_55_browser.js`.
- Storie della classifica automatiche (post di Girrr Sport/Giornale in Curva, trafiletto nel Giornale, Radio): pronte sul ramo vecchio di ChatGPT, non attive. Vanno riviste con la regola dei tre livelli e con il suo «vai».
- Derby a 80 nel database (`derby_aggiorna()` usa ancora 70): migrazione preparata, serve il «vai».

**Il tuo lavoro (dividilo con ChatGPT come scritto sotto)**
1. **Controllare e unire il lavoro di ChatGPT sulle grafiche** (PR con prefisso `chatgpt/`): leggere il diff, verificare che non tocchi le parti indicate come vietate nel suo prompt, rigenerare l'Anteprima, lanciare le prove, guardare le foto Lega e Stadio a 320, 390, 768 e 1280 px, confrontare i colori con il sito vero (vedi lo script di confronto usato il 1° novembre: interruttore, bande, giornata selezionata, schede). Unire su un ramo `claude/…` e poi su `main` del registro. Non unire nulla che rompa le regole grafiche o le notifiche.
2. **Preparare il rilascio 5.5 sul sito vero** (solo dopo la scelta del Tabellone e il «vai» di Gianluca). Le pagine 5.5 oggi sono copie di prova con `<base>` verso il sito e la protezione `preview-guard.js`: vanno portate nelle pagine vere di `gh-pages` (Lega `girrr/` e Stadio `stadio/girrr/`: `index.html`, `tabellone.html`, `curva.html`, `app.html` per Albo/Annuario/Carriera, pagine nuove `campo.html` e `notifiche.html`), con `ui.js`/`ui.css` serviti dal sito, senza la protezione dell'Anteprima e senza le scritte «Anteprima». Aggiornare anche `rilascio/tabellone_dati.py` e le sorgenti `ufficiale/src/sito/` (devono restare uguali a `gh-pages`). Insieme alla 5.5 vanno pubblicati, già pronti:
   - riquadri della Home in modalità ospite: `lab/ospite-prova-lega.js` → `girrr/ospite.js`, `lab/ospite-prova-stadio.js` → `stadio/girrr/ospite.js`;
   - post automatici delle squadre che contano anche risposte e rilanci: stessa riga di `anteprima/sorgenti/53/curva-*.html` in `girrr/curva.html` e `stadio/girrr/curva.html` (cerca `S.posts.forEach(function(p){(tm[p.team]`);
   - banca dei personaggi ampliata: `lab/curva-banca-ampliata.js` → `girrr/curva-banca.js` (e la copia in `ufficiale/src/sito/girrr/curva-banca.js`).
   Ordine: prima `gh-pages`, poi controlla il sito vero (pagine aperte, console senza errori nuovi, Lega e Stadio, telefono e PC, WebKit tramite il workflow), solo dopo `main`. Annota gli hash e come tornare indietro (`git revert`). Gianluca ha autorizzato i push su `gh-pages` ma vuole **tutto insieme con la 5.5**. Se il controllo di sicurezza della sessione blocca il push, fermati e spiegalo.
3. **Dopo il rilascio**: aggiornare STATO.md, la vetrina (o un archivio `lab/versione-5-5.html` come per la 5.3) e la numerazione della prossima versione (chiedere a Gianluca il numero).

**Come provare**
- `python3 anteprima/build.py` (deve rigenerare l'Anteprima uguale a quella salvata), `python3 prove/collaudo_anteprima_52.py`, `python3 prove/prova_moviola.py`, `python3 prove/prova_moviola_gol.py`.
- `node prove/collaudo_55_browser.js chromium` con il registro servito su `http://127.0.0.1:8765` (`python3 -m http.server 8765` dalla cartella del registro). WebKit (Safari) qui non c'è e non va installato: gira su GitHub nel workflow `.github/workflows/claude-collaudo-55.yml` a ogni modifica di `anteprima/` o `lab/`.
- Chromium è già installato (`require('playwright')`, `NODE_PATH=$(npm root -g)`), non lanciare `playwright install`.
- Mai lanciare `voci-src/prova_*.py` (servizi a pagamento).

**Cose che può fare solo Gianluca (ricordagliele se servono)**
- Segreti nel repository del sito: `GEMINI_API_KEY` (Radio automatica) e `SUPABASE_SERVICE_ROLE_KEY` (premi automatici).
- Profili social della Lega (Gmail della Lega, Pagina Facebook, Instagram professionale): le immagini sono pronte in `social/` (`node social/genera.js` le rifà con la classifica nuova). Quando avrà la chiave di Instagram, si prepara la pubblicazione automatica dopo ogni giornata (mai scommesse nei post ufficiali).
- Cancellare il ramo `grok/carriera-tab-storia` (danneggiato) e chiudere la PR #35 (superata).
- Provare su un iPhone vero.

Quando hai finito ogni pezzo: di' cosa hai cambiato, cosa hai provato e cosa non hai potuto provare, e aggiorna `STATO.md`.
