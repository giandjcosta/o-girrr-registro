# Regole comuni di lavoro · O Girrr

Valgono per tutti: Claude, ChatGPT, Grok, Copilot, Perplexity, Aider, VS Code e Gianluca (decisione di Gianluca, 16 novembre 2026).
Ognuno può usare i suoi metodi: per esempio ChatGPT è molto bravo nella grafica e nel front end. Queste sono le **basi comuni**, perché chi riprende il lavoro di un altro trovi tutto in ordine.
Le regole di progetto restano in `AGENTS.md` (contenuti, grafiche Lega e Stadio, versioni, «Vai» di Gianluca). Questo file dice **come** si lavora.

## 0. Prima di toccare qualcosa
1. Leggi `AGENTS.md`, `STATO.md` e **`LAVORI-IN-CORSO.md`**. Se qualcuno ha lasciato un lavoro a metà, riparti da lì e non rifarlo da capo.
2. `git pull` su tutti e due i repository. Guarda Pull Request e rami aperti.
3. Scrivi in `LAVORI-IN-CORSO.md` cosa stai per fare (vedi il punto 6), così se la chat si interrompe chi arriva dopo lo sa.

## 1. Scrivere il codice
- **Una fonte sola.** Una correzione destinata al sito va nello script del rilascio (`rilascio/rXYZ/…`). Il Lab si rigenera da lì (per la 6.2.1: `rilascio/r621/applica.py` poi `rilascio/r621/lab.py`). Mai correggere a mano solo la copia nel Lab e solo il rilascio: le due versioni si separano e quello che si prova non è quello che va online.
- **Sostituzioni che si fermano se il file è cambiato.** Gli script di rilascio cercano il testo esatto da sostituire e si fermano se non lo trovano (oppure confrontano l'impronta sha256 in `ORIGINALI.json`). Non togliere questi controlli: sono quelli che evitano di pubblicare sopra una modifica di un altro.
- **Rieseguibili.** Lanciare due volte uno script di rilascio deve dare lo stesso risultato (alla seconda volta: «0 file cambiati»).
- **Lega e Stadio insieme.** Quasi ogni modifica va nelle due copie (`girrr/` e `stadio/girrr/`). Attenzione ai percorsi relativi.
- **Versione nell'indirizzo dei file.** Se cambi un `.js` o un `.css`, cambia anche il `?v=` nelle pagine che lo caricano, altrimenti i telefoni tengono quello vecchio.
- **Un solo responsabile per ogni movimento.** Uno scorrimento, un'animazione o un ridisegno deve avere un solo codice che lo comanda. Nella Carriera la fila delle pillole era mossa da tre codici insieme e sul telefono si fermava a metà.
- **Animazioni.** Sempre fluide e sempre con `prefers-reduced-motion`. Al tocco niente alone del browser: `-webkit-tap-highlight-color:transparent`, con un segnale proprio, per esempio `:active{opacity:.7}`.
- **Commenti nel codice** in italiano, con data e motivo («6.2.1 (Gianluca): …»). Sono il diario di chi arriva dopo.
- **Niente segreti** nel codice. Le chiavi «publishable» di Supabase già presenti sono pubbliche per scelta.

## 2. Provare
- **Sempre nel browser vero, non solo leggendo il codice.** Playwright con Chromium: `require('playwright')` funziona da qualsiasi cartella nell'ambiente di Claude. Su GitHub i workflow provano Chromium, WebKit e Firefox.
- **Telefono = tocco vero.** Su telefono usa `page.touchscreen.tap(x, y)` su un punto **visibile** dell'elemento. `locator.tap()` e `click()` prima fanno scorrere la pagina fino all'elemento: nascondono proprio i difetti di posizione e di scorrimento.
- **Misura, non indovinare.** Per le animazioni registra la posizione fotogramma per fotogramma (`requestAnimationFrame`) e intercetta chi muove cosa (`scrollTo`, `scrollLeft`, `scrollIntoView`). Così si vede subito se due codici si contendono lo stesso movimento.
- **Schermi:** 320 px (iPhone SE) senza scorrimento laterale, telefono grande, tablet, PC 1280 e 1920, monitor 2560 e TV (`prove/prova_schermi_56.js`). A Gianluca le foto su PC e TV.
- **Console senza errori nuovi.** Se un errore c'era già, confrontalo con la versione pubblicata e dillo.
- **Controlli di GitHub** (Gianluca, 16 novembre 2026): sulle PR partono da soli solo quelli della versione in corso e del Registro (`integrazione-62-qa`, `registro-browser-qa`). I collaudi delle versioni passate restano nei file e si lanciano a mano (Actions › Run workflow) quando serve. Una versione nuova aggiunge il suo controllo e rende «solo a mano» quello vecchio.
- **Prove automatiche del registro** (`prove/`): lancia quelle di quello che hai toccato. Non lanciare `voci-src/prova_*.py`, che usano servizi a pagamento.
- **Database:** le prove SQL solo su PostgreSQL locale (`prove/v62/postgres_*.py`), mai su Supabase.
- **Di' sempre cosa hai provato davvero e cosa no**: per esempio «Safari su iPhone non disponibile qui» oppure «solo Chromium». Cambiare user-agent non vale come prova di un altro browser.

## 3. Rilasciare (deploy)
1. **Prima la prova nel Lab** (`https://giandjcosta.github.io/o-girrr-registro/lab/`), poi la certificazione e il **«Vai» esplicito di Gianluca**. Senza «Vai» non va online niente.
2. **Chiedi a Gianluca che tipo di versione è**: correzione minore, aggiornamento medio o aggiornamento grande. Poi scrivi messaggio e changelog seguendo `REGOLE-VERSIONI.md` e aggiungili con `rilascio/versioni/aggiungi.py`.
3. **Ordine fisso:** prima `gh-pages` del sito, poi la controlli sul sito vero (pagina aperta, console pulita), solo dopo `main` del sito e del registro. `git pull --rebase` prima di ogni push: i workflow scrivono ogni pochi minuti.
4. **Annota gli hash** dei commit e come tornare indietro (`git revert <hash>` sul ramo giusto) in `STATO.md` e nella cartella del rilascio (`rilascio/rXYZ/RILASCIO.md`).
5. **SQL:** solo con il «Vai». Gianluca lo applica dall'SQL Editor di Supabase (la conferma dello strumento di Claude spesso non gli arriva). Prepara sempre anche le funzioni di prima, per tornare indietro.
6. **Unire una Pull Request** solo quando i controlli di GitHub sono finiti e verdi. Se un controllo era rosso già prima, spiegalo nella PR invece di ignorarlo.
7. Dopo il rilascio: allinea `ufficiale/src/sito/` con `gh-pages` e aggiorna `STATO.md` e `LAVORI-IN-CORSO.md`.

## 4. Cercare un guasto (troubleshooting)
1. **Riproducilo** nel browser, con la stessa grafica (Lega o Stadio), lo stesso schermo e lo stesso modo di toccare di Gianluca.
2. **Pubblicato o in prova?** Confronta il sito vero, il Lab e la copia locale. Spesso il guasto è solo in una delle tre.
3. **Guarda la storia:** `git log -S"testo" -- file` dice chi ha introdotto una riga e perché.
4. **Un controllo di GitHub rosso:** leggi il log (`get_job_logs`) e verifica se era rosso anche su `main` prima della tua modifica. «Instabile» non è una causa.
5. **Cache:** se il sito vero «non cambia», di solito manca il `?v=` nuovo oppure il service worker (`offline.js`) tiene la copia di prima.
6. **Workflow che scrivono da soli** (Curva, voti, calcoli, Ramificazioni, Allineamento del Registro): non modificare a mano i file che generano. Correggi lo script che li genera e rilancia il workflow.
7. **Se un controllo di sicurezza ti blocca, fermati e spiegalo.** Non aggirarlo.

## 5. Scrivere per Gianluca
- In italiano, semplice. Cosa è cambiato, cosa hai provato, cosa no, cosa serve da lui (un «Vai», una scelta).
- Le domande vanno fatte una volta sola e chiare, con le opzioni e la tua raccomandazione.

## 6. Passaggio di consegne
- `LAVORI-IN-CORSO.md` è il quaderno comune: ogni voce dice **cosa**, **chi**, **stato**, **dove** (rami, file, PR) e **prossimo passo**.
- Aggiornalo **quando cominci** e **quando ti fermi**, anche se ti fermi a metà: soprattutto se ti fermi a metà.
- Quando una voce è finita e pubblicata, spostala in «Fatto di recente». Dopo una settimana la cronologia vive in `STATO.md` e `STATO-storico.md`.
