# Stato del progetto O Girrr (aggiornato 23 ottobre 2026, sera)

Per aprire una chat nuova: incolla "Leggi STATO.md nel repo o-girrr-registro e continuiamo da lì".

## Dove vive tutto
- Sito vero: repo `giandjcosta/o-fant-a-girrr`, ramo `gh-pages` (pagine) e `main` (workflow e calcoli). Sito: https://giandjcosta.github.io/o-fant-a-girrr/
- Laboratorio e registro: repo `giandjcosta/o-girrr-registro`, ramo `main`.
- Database: Supabase, progetto `qmjqfgmvimsuxvghetgi`.
- Build: `export SORGENTE_GIRRR=/tmp/orig/girrr` (worktree del commit 1e2506f del repo del sito: `git fetch --depth=30 origin gh-pages` e poi `git worktree add /tmp/orig 1e2506f`), poi `python3 aggiorna.py`, `python3 rilascio/pacchetto.py`, `python3 rilascio/applica.py --gh-pages /home/claude/o-fant-a-girrr --main /tmp/wm [--vai]`, push `origin HEAD:gh-pages` e `origin HEAD:main` (prima `git fetch` e `rebase`: la Curva scrive su `main` ogni mezz'ora).
- ATTENZIONE prima di applicare: il `main` online può avere file più nuovi di quelli del registro (era successo con `curva-subito.yml`, `pubblica_curva.py`, `post_curva.py`, `leggi_eventi.py`). Guardare sempre il diff di `main` nella prova a vuoto e, se ci sono file che non ho toccato, copiarli prima dal sito vero nel registro (`calcoli/`, `rilascio/workflow/`). Ora sono allineati.

## Regole di pubblicazione
- Micro correzioni di testo: online in automatico, avviso dopo. Tutto il resto: serve il "vai" di Gianluca.
- Niente disclaimer "notizia inventata" o "dati finti". Storie come un campionato vero (giocatori, gol, squadre, allenatori), niente riferimenti a fantacalcio, crediti, fantapunti o fantamedia, salvo punteggi. "Derby" sempre con la D maiuscola. Titoli ed etichette con la maiuscola iniziale. Post ufficiali mai sulle scommesse.

## Fatto e online (18 ottobre)
5.0 completa; Carriera con tre fasce e sette sponsor; Albo di Latta e Derby nell'Albo; storie di tutti gli allenatori dal 2016/17; logo della Lega in Curva porta alla Home della Lega; tab deselezionata torna neutra subito; Curva con workflow "post quasi subito" ogni mezz'ora (ora senza coda: `giorni_coda` a 0); quote Derby di Totogirrr accese (+15% per esito, +10% sulla schedina con un Derby, cashback 20%).
Sera del 18 ottobre, con il "vai" di Gianluca:
- L'app manda `p_testo` con la frase vera al lancio della sfida (`rilascio/live.js`).
- `derby_stato` restituisce `frase_testo` (`sql/5-stato-frase.sql`); `leggi_eventi.py` lo passa come `testo`; `post_curva.py` lo usa nell'Intervista speciale di qualsiasi coppia (la tabella FRASI a mano resta solo per le sfide vecchie senza testo, solo Oranje VC–Apo). Frase troppo lunga: si accorcia con i puntini.
- Post "Conferenza pre partita · Giornata X" su Girrr Sport: uno per squadra, solo per l'ultima giornata che ha conferenze, con la risposta libera, la promessa e le altre risposte nei 280 caratteri. Legge la nuova funzione `conf_pubbliche()` (`sql/6-conf-pubbliche.sql`: tutte le conferenze con le risposte; `conf_promesse` resta com'era, solo promesse, per `fiducia.py`).
- Totogirrr: il cambio scheda non fa più sparire e riapparire la pagina (tolta l'animazione `ANIM` al click sulle schede; resta all'apertura). Patch in `ufficiale/build.py`.
- Database: `4-pulizia.sql` applicato (una sola `derby_sfida_lancia`, con `p_testo`).
- Totogirrr: il cambio scheda riscrive solo il contenuto (`render()` salta testata, logo, ticker e schedina se non cambiano). Verificato in un DOM simulato e in Chromium.
- Sfondo: il gradiente non sta più su `body` con `background-attachment:fixed` (Safari lo stirava sull'altezza della pagina e cambiava colore tra pagine corte e lunghe) ma su `html::before` fisso, in tutte le pagine di Lega e Stadio. Lo fa `rilascio/sfondo.py`, chiamato da `pacchetto.py`. Non provato su Safari da me: Gianluca deve controllare.
- Verificati da Gianluca: iPhone, unificazione statistiche di Riccardo e Nobile, "Calcoli dopo la giornata" lanciato.

## Da fare
0. FATTO il 21 ottobre: tab Borsino nello Spogliatoio vero (index.html del sito, legge girrr/dati/borsino.json) e tolto il tag Derby dalle liste dei Derby. Prima era: il Borsino nello Spogliatoio. Gianluca si aspettava di trovarlo lì e non c'è (il Borsino c'è nei calcoli, `calcoli/borsino.py`, e nella app come scheda `vBors`): capire se manca nel menu dello Spogliatoio o se è solo nascosto, e deciderlo con lui.
1. Derby "The Continental" (Oranje VC–Apo): Apo deve ancora confermare il nome nell'app (`nome_ok` falso). Appena conferma, il post "Nasce un Derby" parte da solo al giro successivo della Curva.
2. Controllare il primo giro della Curva dopo le novità: l'Intervista speciale con il testo vero (alla prossima sfida lanciata) e il post Conferenza di Apo.
3. Aperto: decidere se aggiungere il post della sfida anche sul profilo della squadra (per ora solo Girrr Sport).
4. Se serve, provare il cambio tab di Totogirrr anche su Firefox e PWA.

## Aggiornamenti del 21 ottobre (sera)
- Giornata 3 (Serie A 7) importata da Leghe, Giornale n°3 e tabellone online. `scripts/leghe_estrai.js` (sito, gh-pages): ora legge il modificatore difesa di entrambe le squadre (`md` di B prima restava vuoto) e aspetta il cambio di pagina invece di 1,8 s fissi a partita.
- Nuovo workflow `controllo-fallimenti.yml` (+ `calcoli/controllo_fallimenti.py`, copiati in `rilascio/workflow/` e `calcoli/`): ogni giorno alle 07:50 apre una Issue nel repo del sito (notifica GitHub) se un workflow è fallito nelle ultime 26 ore, se "Aggiorna statistiche e voti" non gira da 2 giorni o se una giornata finita non è stata importata. Se è tutto a posto chiude la Issue. Le schedule di Claude che falliscono per "limite di utilizzo raggiunto" non si vedono dalle Actions: si notano da questi dati fermi.
- Radio: `voci-src/dati.json` aggiornato alla giornata 3 con i dati veri di `lab-dati.json`; `conferenze.json` e `mercato.json` svuotati (erano di prova), `curva.json` vuoto (niente post questa settimana, la radio non ne parla). Puntata lanciata dal workflow "Puntata di prova della Radio" con solo Gemini.
- Tolto il tag Derby dalle liste dei Derby (anche nelle sorgenti del Registro) e Borsino come tab dello Spogliatoio.

## Aggiornamenti del 23 ottobre: Moviola (solo Lab, in prova)
- Tab "Moviola" di Girrr Sport attiva nel Lab (`lab/index.html`, funzioni `spMoviola`, `mvEpisodi`, testi in `MVT`) e nelle due grafiche dell'Anteprima (`anteprima/build.py` aggiornato: etichetta "Moviola" e routing; `index.html` e `attuale.html` rigenerati). `ufficiale/` non toccata, niente online sul sito vero: serve il "vai".
- Dati: legge `data.json` (voti `votes[id][sa].b`, gli stessi del post Moviola di `curva-banca.js`) e `formazioni.json` dal sito, come il Giornale legge le copertine. Squadra del giocatore: dalla formazione di quella giornata se c'è in `formazioni.json`, altrimenti dalla rosa attuale.
- Al massimo 3 episodi per giornata, per priorità: rosso, rigore sbagliato, autogol, rigore parato, partita vinta per meno di 1 punto (i pareggi no). Verdetto fisso per tipo: rosso → Rosso confermato; rigore sbagliato, autogol, rigore parato → Regolare; partita sul filo → Da rivedere. 3 o 4 varianti di testo per tipo, scelte in modo stabile (stessa giornata e stesso giocatore danno sempre lo stesso testo). Giornata senza episodi: "Giornata tranquilla, nessun episodio". Selettore della giornata con tutte le giornate giocate.
- Cartellini rossi: NON ci sono nei dati. Le voci di `b` sono solo gol, assist, gol subiti, rigori (segnati, sbagliati, parati), autogol, subentrato, senza voto, migliore in campo. Il codice è pronto: se compare una voce con "espulso" o "rosso" entra da sola come primo episodio. Volendo si potrebbero dedurre da fantavoto meno voto (5 casi con -1 non spiegato), ma è una stima: da decidere con Gianluca.
- La tab deselezionata di Girrr Sport torna neutra subito (`#view .seg button[data-sp][aria-pressed=false]{transition:none}`).
- Provato in Chromium su iPhone SE, iPhone 13, PC 1366 e TV 1920: niente scroll orizzontale né testi fuori dalle card, selettore a 16px (niente zoom su iPhone). Provati anche con dati finti il rosso, la partita sul filo e la giornata tranquilla. Non provato su Safari vero.

## Moviola passo 1: una sola fonte (ramo `moviola-json`, solo prova)
- Nuovo `calcoli/moviola.py`: da `data.json` e `formazioni.json` del sito scrive `calcoli/moviola.json` con gli episodi di ogni giornata con tutti i risultati. Stesse regole del 23 ottobre (massimo 3, stesse priorità, stessi verdetti, stessi testi scelti nello stesso modo stabile: per le giornate 2 e 3 escono identici a prima).
- Una giornata scritta non cambia più, anche se i voti vengono corretti (`--rigenera` riscrive tutto). Il file si riscrive solo se cambia qualcosa.
- La squadra del giocatore si prende solo dalla formazione di quella giornata (titolari e panchina). Se non si ricava, l'episodio non esce, va in `scartati` e lo script stampa "! SCARTATO ...". Contano solo i giocatori della lega (in una rosa o in una formazione).
- `formazioni.json` tiene solo le ultime giornate di Serie A (oggi la 6 e la 7). Per questo la giornata 1 (Serie A 5) è scritta senza episodi, con 2 scartati (rigore sbagliato di Yeboah J. e rigore parato di Mandas). La tab mostra "Episodi della giornata 1 non disponibili", non "Giornata tranquilla".
- La tab del Lab non ricalcola più niente: legge `../calcoli/moviola.json`. Messaggi: "Carico gli episodi…" mentre carica; "La Moviola non si è caricata" se il file non arriva; "non ancora pronti" se manca la giornata; "Giornata tranquilla, nessun episodio" solo se la giornata è scritta senza episodi e senza scartati.
- Workflow `rilascio/workflow/dopo-giornata.yml`: nuovo passo "Moviola di Girrr Sport" dopo "Dati per le pagine nuove". `moviola.json` viene salvato su `main` dal passo finale insieme agli altri `calcoli/*.json`. Il workflow è solo nella copia del registro: nel sito vero arriva con il "vai".
- Da fare: il Lab legge la copia del registro, che oggi si aggiorna solo lanciando lo script a mano. Al rilascio va deciso dove la legge il sito vero, perché `main` del sito non è pubblicato su Pages: o il workflow la copia in `site/girrr/dati/`, o la pagina la legge da `main`. Il post Moviola della Curva (`curva-banca.js`) calcola ancora per conto suo: si allinea nel passo 5.
- Test: Chromium su iPhone SE, iPhone 13, PC e TV, nel Lab e nelle due Anteprime, con i dati veri e con dati finti (rosso, partita sul filo, giornata tranquilla, giornata mancante, file non trovato, caricamento lento). Tutto a posto. WebKit/Safari non provato: in questo ambiente non c'è e non si può scaricare. Il riquadro "Cosa cambia in Home", che c'è solo nel Lab e c'era già prima, esce di 22 px su iPhone SE (320 px).

## Moviola passo 2: verdetti calcolati (ramo `moviola-verdetti`, unito con `moviola-json`, solo prova)
- Base: la logica del passo 2 in `calcoli/moviola.py`; dal passo 1 restano il file unico `calcoli/moviola.json` (formato con `giocate`, `giornate`, `episodi`, `scartati`), gli scartati segnalati, il "già scritta, non cambia", la riscrittura solo se cambia qualcosa e il passo nel workflow `dopo-giornata.yml`. `lab/moviola.json` non c'è più: Lab, Anteprima Stadio (`index.html`) e Lega (`attuale.html`) leggono `../calcoli/moviola.json`.
- Ha deciso la partita: toglie l'effetto dell'episodio dal punteggio della squadra, ricalcola i gol e guarda se l'esito (vittoria, pareggio, sconfitta) cambia. Valori dai dati, niente numeri a mano: ogni voce vale la differenza fantavoto meno voto più frequente (oggi rigore sbagliato −3, autogol −2, rigore parato +3; a parità vince il valore più alto perché i gialli, che non sono tra le voci, tolgono mezzo punto); soglie dei gol dai risultati giocati (oggi 66 il primo gol, poi uno ogni 5 punti).
- Solo per i titolari con voto nella formazione di quella giornata. Chi parte dalla panchina non può "decidere" (sapere se è entrato sarebbe una stima): resta Regolare, o Da rivedere se la partita è sul filo, e non pesa nell'ordine.
- Verdetti: rosso → Rosso confermato (sempre; se ha deciso lo dice il testo); ha cambiato l'esito → Ha deciso la partita; partita vinta per meno di 1 punto → Da rivedere; il resto → Regolare. La partita sul filo non ha un effetto da togliere: non "decide" mai.
- Ordine dei 3: prima chi ha deciso, poi per peso sul risultato (gol spostati, poi punti dell'effetto), poi rosso, rigore sbagliato, autogol, rigore parato, partita sul filo.
- Testi "Ha deciso la partita": 3 o 4 varianti per rosso, rigore sbagliato, autogol e rigore parato, con allenatori e risultato della partita (mai punti o crediti). Il risultato usa un trattino che non va a capo. Colore: viola chiaro su fondo viola tenue. Ogni card ha a sinistra una barretta del colore del suo verdetto (viola Ha deciso la partita, verde Regolare, oro Da rivedere, rosa Rosso confermato), sopra l'ombra normale della card; viste in Stadio e Lega.
- `--rigenera` riscrive tutto, `--rigenera 2,3` solo quelle giornate; senza, le giornate già scritte non cambiano.
- Giornata 2 riscritta con le regole nuove (`--rigenera 2`, con `data.json` e `formazioni.json` di `gh-pages` del sito, commit 53cef58): l'autogol di Vasquez (Real Madrink, titolare) ora è "Ha deciso la partita" (senza, Real Madrink avrebbe vinto invece del 2-2). Giornate 1 e 3 lasciate come le aveva scritte il passo 1 (identiche).
- Provato con dati finti: rosso decisivo, partita sul filo (Da rivedere), titolare che decide (Ha deciso la partita), panchinaro nella stessa situazione (Regolare), giornata senza formazione (scartati). Playwright su Chromium, iPhone SE, iPhone 13, PC 1366 e TV 1920, in Lab, Stadio e Lega: tutto a posto. WebKit non si scarica in questo ambiente (rete bloccata verso `cdn.playwright.dev`).
- Da fare: Safari vero; dove legge il file il sito vero al rilascio (vedi passo 1); `ufficiale/` non toccata, niente online.


## Moviola passo 3: voci a mano e video (ramo `claude/moviola-manuale-step-3-7qapus`, rifatto da `main` dopo i passi 1 e 2, solo prova)
- Tutto dentro `calcoli/moviola.py` di main, un solo output: `calcoli/moviola.json`. Campi esistenti invariati; nuovi: per giornata `automatici` (tutti gli episodi trovati, senza taglio a 3), per episodio `id`, `squadra_reale`, `avversario_reale`, `in_casa`, `data_partita`, `video`, `manuale`. `episodi` è quello da mostrare: si rifà a ogni giro dagli automatici più le voci a mano, quindi le voci a mano valgono anche sulle giornate già scritte e dopo `--rigenera`. Le giornate scritte prima (1, 2, 3) prendono come automatici i loro episodi di allora: testi e verdetti identici a main, `--rigenera` dà gli stessi episodi.
- `calcoli/moviola-manuale.json` (oggi vuoto, esempio nel LEGGIMI): voce uguale a un automatico (giornata, giocatore, tipo) → aggiunge solo i campi mancanti; altrimenti episodio nuovo (rosso → Rosso confermato, altro → Da rivedere, testo facoltativo dai modelli); `nascondi` toglie un automatico e il posto va al successivo. Le voci a mano entrano sempre e scalzano gli automatici meno importanti. Solo link `https://`; secondo di partenza come `t=` su YouTube.
- Card: pulsante "Guarda il momento" (nuova scheda, `rel=noopener`) solo se c'è il video, in Lab, Stadio e Lega. Niente video incorporati.
- `moviola-video.html` nella radice (non collegata): per episodio titolo, giocatore, giornata, squadra reale, partita e data, ricerca YouTube già compilata, riga pronta da copiare.
- Dati: squadra reale = club di oggi in `P[id].t` (non quello della giornata); avversario e data da `fx`/`sa` di `data.json`, che coprono solo la Serie A dalla giornata 6 in poi (la giornata 1 della lega, Serie A 5, non ha avversario); si salvano la prima volta e non si perdono. Mancano rossi, minuto, risultato reale.
- Workflow `dopo-giornata.yml`: il passo Moviola c'era già; aggiunto il trigger `push` su `main` solo per `calcoli/moviola-manuale.json` (in quel caso fa solo la Moviola, niente Curva né altri calcoli) e `moviola-video.html` nel commit finale. Nessun cron nuovo.
- Provato con voci finte (rosso nuovo con video, video su un automatico, link http scartato, nascondi, altro con testo, episodio a mano su una giornata con soli scartati) con Playwright su Chromium: iPhone SE 320 e 375, iPhone 13, PC 1366, TV 1920, in Lab, Stadio, Lega e pagina dei video. Tutto a posto. WebKit non scaricabile qui.

## Note
- Il workflow Curva salva lo stato in `calcoli/pubblicati.json` su `main`; l'opzione `solo_segna` segna i post attuali come già usciti senza inviarli.
- Le storie degli allenatori stanno in `ufficiale/src/storie.json`.
- Le chiavi dei post sono `tipo:k:indice` (es. `conferenza:C3-Apo team:0`): ogni post esce una sola volta.
