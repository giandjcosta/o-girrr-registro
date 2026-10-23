# Stato del progetto O Girrr (aggiornato 23 ottobre 2026)

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

## Note
- Il workflow Curva salva lo stato in `calcoli/pubblicati.json` su `main`; l'opzione `solo_segna` segna i post attuali come già usciti senza inviarli.
- Le storie degli allenatori stanno in `ufficiale/src/storie.json`.
- Le chiavi dei post sono `tipo:k:indice` (es. `conferenza:C3-Apo team:0`): ogni post esce una sola volta.
