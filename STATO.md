# Stato del progetto O Girrr (ultimi giorni — aggiornato 30 ottobre 2026)

## 30 ottobre 2026 — Tabellone con più dati (Claude, prova nel Lab)
- Richiesta di Gianluca: in classifica anche V, N, P, gol fatti, gol subiti e differenza reti. L'ordine della classifica non cambia (Pt, poi Fantapunti) e non c'è nessuna nota sullo spareggio (decisione di Gianluca).
- Sul telefono (<560 px) la classifica mostra DR, Pt e Fantapunti; da 560 px in su anche G, V, N, P, GF, GS. Vale anche per i gironi di Champions Cup (senza Fantapunti, come oggi).
- Patch unica `rilascio/tabellone_dati.py`: con `--lab` crea le copie di prova (`lab/prova-tabellone-lega.html`, `lab/prova-tabellone-stadio.html`, generate dal `tabellone.html` di `gh-pages`, con `<base>` verso il sito e senza statistiche visite); senza `--lab` è la patch per il sito vero. Link nel Lab (card «Tabellone · Più dati in classifica», solo Lab).
- Provato in Chromium a 320, 375, 768 e 1280 px, Lega e Stadio, Campionato e Champions Cup: nessuno scorrimento laterale, console pulita; controllato che V+N+P = G per ogni squadra e che i gol fatti della lega pareggino quelli subiti (84 = 84). Non provato: Safari/iPhone.
- Per il sito vero (dopo il «vai»): `python3 rilascio/tabellone_dati.py girrr/tabellone.html girrr/tabellone.html` e lo stesso per `stadio/girrr/tabellone.html` su `gh-pages`, poi copia in `ufficiale/src/sito/`.

## Carriera a tab — resoconti
Piano e prompt in `proposte/carriera-tab-piano.md`. Base: ramo `claude/review-ai-changes-test-ui9gjy`. Ognuno scrive solo nel suo paragrafo.

### Tab Panoramica e Fiducia + struttura (Claude)
- Carriera divisa in 4 tab (Panoramica, Obiettivi, Fiducia, Storia; la Cassa resta fuori, decisione di Gianluca). Selettore a pillole sotto la bolla, che va a capo a 320 px. Panoramica: arco Fiducia, «N su 4 raggiunti», Reputazione e sponsor. Fiducia: aspettativa, simulatore, nuovo grafico «Fiducia giornata per giornata» (classifica di ogni giornata giocata dal calendario del sito), Fiducia in lega. Zone vuote pronte per ChatGPT (`vCarObiettivi`) e Grok (`vCarStoria`), con versione provvisoria.
- **Solo la propria squadra** (decisione di Gianluca): nell'Anteprima e nel rilascio la Carriera mostra solo la squadra entrata col codice (`ME`), senza selettore (`CARSCELTA=false` da `build.py`). Il selettore resta nel Lab; nell'Anteprima si prova un'altra squadra con `?come=Grodah`. I non entrati vedono già «Entra con la tua squadra» (`livepatch`). Aperto: «Fiducia in lega» mostra ancora la classifica fiducia di tutti.
- Provato in Chromium a 320 e 1280 px su Lab, Lega e Stadio, tutti e 4 i tab e The Blue brothers (due allenatori): nessuno scorrimento laterale, console pulita. Test automatici superati. Non provato: Safari/iPhone.

### Tab Obiettivi (ChatGPT)
- Linea del tempo 2/6/8/10/18/26/34: giornate giocate da `gioc()`/CL, prossima evidenziata e scorrimento interno.
- Obiettivi stagionali con progressi, stati e scadenze; Champions Cup del presidente e dell'allenatore; premio sponsor con link solo se riscuotibile.
- Collaudi JavaScript su snapshot del ramo (milestone/Totogirrr e fiducia universale): PASS; verifica equivalente di `collaudo_anteprima_52.py`: PASS.
- Chromium sul componente isolato a 320/375/1280 px, Oranje VC/Grodah/The Blue brothers: 9 casi PASS, nessun overflow o errore JS; stati premio e link verificati.
- Non eseguiti `python3 anteprima/build.py` e `git diff --exit-code anteprima/` in checkout locale (DNS GitHub bloccato); blocco generato propagato nelle anteprime e confrontato.
- Non eseguito browser end-to-end delle tre pagine complete via HTTP, né Safari; serve verifica CI/QA della PR.
- **Verifica Claude (unione PR #36):** `build.py` dà un'Anteprima identica a quella committata; test JS e `collaudo_anteprima_52.py` superati. Chromium sulle pagine complete (Lab, Lega, Stadio) a 320, 375 e 1280 px con Oranje VC, Grodah e The Blue brothers (`?premi=prova`): nessuno scorrimento laterale, console pulita, link «Vai a Totogirrr» solo quando il premio è da riscuotere. A 320 px la linea del tempo scorre dentro la sua card.

### Tab Storia (Grok)
- **Non consegnato (verifica Claude):** il ramo `grok/carriera-tab-storia` contiene solo un commit su STATO.md, senza il codice di `vCarStoria`. Quel commit cancella circa 80 righe di STATO.md e mette parole inglesi nel testo («with», «for», «the»), quindi **non è stato unito**. Nel Lab resta la versione base (elenco stagioni).

## 30 ottobre 2026 — Claude: Carriera/Totogirrr 5.2 sistemati (ramo `claude/review-ai-changes-test-ui9gjy`, non ancora su `main`)
- **Revisione del lavoro ChatGPT fino a `33fdfc4`:** tutto il codice 5.2 era stato scritto a mano in `anteprima/index.html` e `attuale.html`. `python3 anteprima/build.py` lo cancellava, e i workflow restavano verdi perché rigeneravano l'Anteprima prima di provarla.
- **Ora la logica sta nel Lab** (`lab/index.html`) e l'Anteprima è rigenerata con `build.py`:
  - premi calcolati dagli **obiettivi veri** dello sponsor della squadra (50/75/100/125 crediti Totogirrr quando l'obiettivo è «Fatto»), non più dal selettore ipotetico. Tolti «Sponsor tecnico/risultati/premium», la giornata 38 irraggiungibile e il saldo finto in Carriera;
  - bolla «Premio sponsor da riscuotere» sotto il selettore della squadra, solo se c'è un premio non ancora riscosso; riquadro «Reputazione e sponsor» con la reputazione della stagione (+2 per obiettivo del presidente, +1 per quello dello sponsor) e lo stato del premio (In corso / Da riscuotere / Riscosso). La reputazione fissa a 72 è sparita;
  - con dati veri oggi hanno il premio Apo team, Grodah, WOA (50), Real Madrink e Atletico ma non troppo (75). Per provare con tutte le squadre: aggiungi `?premi=prova` all'indirizzo (es. `anteprima/attuale.html?premi=prova#carriera`).
- **`anteprima/totogirrr-52.html`:** apre la **stessa squadra della Carriera** (`?team=`) con i suoi premi. Saldo, riscatti e movimenti sono tenuti squadra per squadra (sessionStorage `ogirrr52-v2`). «Cambia squadra» passa alla squadra successiva senza azzerare niente. «‹ O GIRRR» torna alla pagina da cui sei partito (Lab, Lega o Stadio): prima `transizioni.js` lo riscriveva verso la home Stadio della copia ufficiale. Tornando in Carriera resta selezionata la stessa squadra.
- **`build.py`:** nell'Anteprima la scheda Totogirrr apre `totogirrr-52.html` (come nel sito vero, dove Probabilità e Sfide stanno dentro Totogirrr) e nasconde gli strumenti di prova. Nel rilascio (`APP_RIL`) i premi finti sono spenti (`PREMI52=false`).
- Testi di ChatGPT portati nel Lab («La fiducia dipende dai risultati…», Cassa «I valori sono modificabili dal tesoriere»). La card Lab «Spogliatoio · Lazy Loading», finita nell'Anteprima con un link rotto, ora è `proto-only`.
- **Test:** `collaudo_preview52_totogirrr_milestone.js` e `collaudo_fiducia_universale52.js` aggiornati e superati sui file pubblicati; `collaudo_anteprima_52.py`, `prova_moviola.py`, `prova_moviola_gol.py` superati. Il workflow «Anteprima Totogirrr 5.2 QA» ora **fallisce se l'Anteprima non è quella generata dal Lab**. Provato in Chromium (320 px) il giro Lab/Lega/Stadio → bolla → Totogirrr → riscatto → cambia squadra → ritorno: nessun errore in console, nessuno scorrimento laterale, nessuna chiamata a Supabase. **Non provati:** WebKit/Safari, telefono vero, `collaudo_milestone_ufficiali52.js` (vuole il checkout del sito), test browser Python (Playwright Python non installato qui).
- **Restano:** `anteprima/totogirrr.html` (vecchia copia, non più collegata) e `totogirrr-premi-5-2.html` da cancellare col «vai» di Gianluca. Il Totogirrr usa sempre la grafica Lega. Nel rilascio il riquadro «Reputazione e sponsor» mostra lo stato del premio, ma il riscatto vero dipende da `carriera_stato`/`carriera_riscatta` su Supabase. Nell'Anteprima la Cassa non è raggiungibile (`vCarr` ignora `S.cr`).
- Prossimo passo proposto: tab nella Carriera, piano in `proposte/carriera-tab-piano.md`.

## 30 ottobre 2026 — Correzione doppio clic «Restituisci» in Totogirrr (ChatGPT)
- Corrette le due versioni dell'anteprima (`anteprima/totogirrr-52.html` navigata dalle Anteprime e `anteprima/totogirrr.html` storico): blocco di rimborso per ID prestito, disabilitazione immediata di tutti i pulsanti «Restituisci» del prestito, ripristino UI solo dopo aggiornamento completo.
- Una notifica `toast` unica viene riutilizzata, con annullamento del precedente timer, impedendo la sovrapposizione e la comparsa/scomparsa immediata dovuta a doppie risposte. Un solo rendering al completamento del rimborso al posto della doppia combinazione `loadPR()`/`carica()`.
- Nel backend isolato della preview un rimborso valido detrae l'importo dal saldo, aggiorna il prestito e registra una sola uscita nella lista movimenti. Respinge importi negativi, eccessivi, ripetizioni oltre residuo e saldo insufficiente; chiude il prestito saldato.
- **Test eseguito:** due click sincroni sullo stesso pulsante `Restituisci 10` nel DOM simulato. Da saldo 346 FC/restituito 50 FC a saldo 336 FC/restituito 60 FC; una sola nuova riga movimenti e una sola notifica. Sintassi JavaScript di entrambe le pagine verificata. Non è un collaudo visuale su Safari/GitHub Pages.
- **Nessun dato reale alterato**, nessun commit o merge in produzione `o-fant-a-girrr`, nessun cambiamento Supabase. Per correggere anche il Totogirrr ufficiale serve modifica/rilascio separato con approvazione.

## 30 ottobre 2026 — Fix login Totogirrr Anteprima 5.2 (ChatGPT)
- **Corretto il bug segnalato dall'utente:** il file `anteprima/totogirrr.html` aveva ancora `gate()` e `render()` poteva mostrare «Codice squadra». Il fix precedente era nel file distinto `anteprima/totogirrr-52.html`, ma la navigazione delle due anteprime continuava ad aprire il file vecchio.
- Ora **entrambi i file** sono senza schermata codice/login; lo stato della squadra viene inizializzato prima del primo render. In `anteprima/index.html` (Stadio) e `anteprima/attuale.html` (Lega), i link Totogirrr puntano a `totogirrr-52.html?skin=...` per evitare vecchie copie in cache.
- **Test eseguiti:** esecuzione JavaScript del Totogirrr con DOM simulato, in modalità Lega e Stadio. In entrambi: squadra, saldo, intestazione SVG, partite, premio, Movimenti e «Cambia squadra» visibili; **nessun campo codice/login**. Test di sintassi JavaScript delle pagine aggiornate riuscito.
- **Supabase:** plugin collegato, progetto «Girrr» individuato; nessuna modifica effettuata al database. I file Totogirrr in anteprima non contengono più l'indirizzo Supabase di produzione.
- **Limiti:** il sito GitHub Pages non è accessibile dal browser remoto del modello: il deployment pubblico non è stato collaudato visivamente. Nessuna modifica a `o-fant-a-girrr` ufficiale.

## 30 ottobre 2026 — Anteprima Carriera/Totogirrr: squadra visitabile
- Tolta **esclusivamente la seconda card «Milestone e premi»** aggiunta in fondo alla Carriera delle due anteprime (Lega e Stadio). Restano i controlli originali «Come cambia la fiducia con il calendario» e gli obiettivi nativi. La bubble premio e il riquadro reputazione/sponsor rimangono, con importi e stato condizionale, e riutilizzano la giornata/posizione selezionata sopra.
- Totogirrr `anteprima/totogirrr.html` ora **si apre già su una squadra di esempio estratta casualmente** (scelta persistente per sessione, senza richiesta codice): saldo iniziale 346 FC, partite aperte e concluse, schedine vinte/perse, prestito attivo e richiesta in attesa, movimenti e premio sponsor riscuotibile. Nessun banner «demo», stessa grafica CSS originale ufficiale. La scelta di squadra è locale e non corrisponde a identità reali.
- **Controlli:** sintassi JS delle tre pagine verificata. Eseguito anche test isolato dei dati Totogirrr con una squadra d'esempio: 346 FC iniziali, otto partite, due schedine, riscatto +60 FC → saldo 406 FC, riscatto duplicato impedito. Nessuna chiamata RPC Supabase dal Totogirrr anteprima. Non verificato il deployment pubblico né svolto un collaudo end-to-end nel browser. Nessuna modifica al sito ufficiale `o-fant-a-girrr`.

## 30 ottobre 2026 — Correzione grafica e UI della 5.2 (ChatGPT)
- **Anteprima Totogirrr** rigenerata dal file `girrr/totogirrr.html` di `o-fant-a-girrr/gh-pages` anziché da un layout ricostruito. Verificato che il CSS incorporato è **identico byte per byte** a quello ufficiale e che il titolo SVG nativo è presente. Il logo usa il percorso dell'asset ufficiale.
- Conservati intestazione, saldo, menù, schede delle partite, schedine, prestiti, classifiche e stile ufficiale; aggiunta solo la tab `Movimenti` con entrate verdi e uscite rosse.
- **Carriera → Totogirrr**: la bubble appare per premi disponibili e sparisce dopo l'incasso. Sponsor, saldo e movimenti della prova usano lo stesso `sessionStorage` e sono isolati dalle API di produzione. Tolti il vecchio link a `totogirrr-premi-5-2.html` e il riquadro «Proposta 5.2» duplicato; nascosti i controlli riservati al Laboratorio nelle due anteprime.
- **Test eseguiti:** sintassi JavaScript di tutte e tre le pagine OK, confronto CSS Totogirrr OK, verificati staticamente link Lega/Stadio e presenza del flusso di riscossione. **Non collaudati** visivamente nel browser remoto, non verificato il deployment su GitHub Pages; il database è simulato e le operazioni reali non vengono scritte.
- **Produzione non toccata:** nessun commit in `o-fant-a-girrr`, nessun merge della release 5.2, nessuna modifica Supabase. Il Changelog pubblico segue i commit del sito ufficiale e non deve indicare questa come release.

## 30 ottobre 2026 — UI Totogirrr dedicata e rifinitura
- **30 ottobre — correzione Totogirrr:** sostituita la ricostruzione grafica arbitraria di `anteprima/totogirrr.html` con il codice HTML/CSS originale della pagina Totogirrr presente nel branch 5.2, mantenendo logo SVG del titolo, layout, ticker, tab, schedine, prestiti e stile nativo. Modalità demo forzata (mock RPC), `data.json` sostituito con elenco locale; rimossi tracker e script accessori. Aggiunta scheda Movimenti alla navigazione originale, con importi verdi/rossi. Non è stato eseguito test end-to-end browser. Il mock usa un premio sponsor di esempio e va ancora armonizzato con la simulazione Carriera; il link `#premi` della vecchia preview non punta a una tab omonima del Totogirrr originale. Niente produzione o Supabase.
- **30 ottobre — rifinitura Anteprima 5.2:** aggiunta `anteprima/totogirrr.html` con grafica dedicata derivata dal CSS del Totogirrr ufficiale, navigazione Partite/Vincite/Prestiti/Premi sponsor/Movimenti/Classifica e movimenti verdi/rossi. Le due anteprime Lega/Stadio portano al Totogirrr dedicato, mentre la bubble premi in Carriera collega direttamente ai premi. La riscossione è isolata in `sessionStorage` e aggiorna lo storico e lo stato della bubble; nessuna API Supabase viene chiamata dalla nuova pagina. Eliminati testi esplicativi della simulazione dai nuovi moduli della UI. **È una release candidate visiva con dati di esempio, non un rilascio production-ready**: browser/Pages non verificati, flussi originali completi di Totogirrr da allineare ancora con il mock. Nessuna modifica a produzione.

## 29 ottobre 2026 — Anteprima 5.2 integrata (ChatGPT)
- **29 ottobre — rifinitura UI 5.2 in anteprima:** movimenti positivi verdi e negativi rossi; bubble vetro/trasparente in Carriera mostrata soltanto con premi sponsor simulati disponibili, scompare dopo aver riscosso tutti i premi. Solo simulazione in memoria: al ricaricamento i dati demo si azzerano. Nessuna modifica al sito ufficiale o a Supabase. Verifica browser online ancora da effettuare.
- **29 ottobre — Totogirrr/Carriera in anteprima**: aggiunto link da Carriera a Totogirrr per riscuotere i premi; inserita scheda «Movimenti» dentro la navigazione Totogirrr (grafica Lega e Stadio) con storico di prova di vincite, sponsor, prestiti, rimborsi e trattenute. I riscatti demo generano una riga nello storico e incrementano soltanto il saldo simulato. Richieste di prestito ancora in attesa mostrate separatamente: non impattano il saldo. Tutto su `o-girrr-registro/anteprima/`, senza toccare produzione/Supabase. **Collaudo browser e verifica link online ancora da fare; non è uno storico persistente reale.**
- Aggiornate **solo** le pagine `anteprima/index.html` (Stadio) e `anteprima/attuale.html` (Lega) sul Registro: le sezioni esistenti restano navigabili, con nuovi riquadri 5.2 **dentro Carriera e Totogirrr**.
- Moduli di UI disponibili: milestone giornata/posizione, stato sponsor, reputazione, riscatto sponsor e saldo simulato. Tutte le operazioni nuove usano dati locali effimeri e non inviano scritture a Supabase.
- Questa è una **prima integrazione visiva simulata**, NON ancora parità funzionale con tutte le modifiche della PR di produzione 5.2: occorre allineare regole complete, premi e backend in modalità isolata, collaudare browser/telefono e verificare il deployment pubblico.
- Nessuna modifica eseguita in `o-fant-a-girrr` (produzione); niente merge della PR 5.2, niente cambi di database.
- Il prototipo isolato `anteprima/demo-5-2.html` resta materiale sperimentale e non è la preview integrata definitiva; in seguito trasferirlo nel Laboratorio.

Per aprire una chat nuova: incolla "Leggi STATO.md nel repo o-girrr-registro e continuiamo da lì".
Lo **storico del progetto**, ricostruito dalle cronologie Git e dalle note, è in [STATO-storico.md](./STATO-storico.md). La cronologia Git consultabile parte dal 7 ottobre 2026 per il sito; attività precedenti non sono documentate nei repository esaminati.

## Dove vive tutto
- Sito vero: repo `giandjcosta/o-fant-a-girrr`, ramo `gh-pages` (pagine) e `main` (workflow e calcoli). Sito: https://giandjcosta.github.io/o-fant-a-girrr/
- Laboratorio e registro: repo `giandjcosta/o-girrr-registro`, ramo `main`.
- **Lab** (prove nuove, anche “incasinato”): https://giandjcosta.github.io/o-girrr-registro/lab/ — da qui in poi le novità si provano qui.
- **Anteprima 5.1** (Lab impaginato come l’app): https://giandjcosta.github.io/o-girrr-registro/anteprima/attuale.html (Lega) e `anteprima/index.html` (Stadio).
- Database: Supabase, progetto `qmjqfgmvimsuxvghetgi`.
- Anteprima 5.2 (la 5.1 è online; archivio in `lab/versione-5-1.html`): https://giandjcosta.github.io/o-girrr-registro/anteprima/attuale.html (Lega) e `anteprima/index.html` (Stadio).
- Lab: https://giandjcosta.github.io/o-girrr-registro/lab/

## Lab vs registro vs sito vero (scelta 26 ottobre)
- **Non si uniscono** il “sito del registro” (index/aggiornamenti) e il Lab.
- Il **Lab resta il posto per provare robe nuove** (anche grezze).
- L’**Anteprima** mostra le stesse cose in forma più ordinata (due grafiche).
- Il **sito vero** riceve solo ciò che passa il “vai” di Gianluca.

## Regole di pubblicazione
- Assistenti: Claude Code, agente di VS Code, Perplexity, Aider, **Grok** (e Gianluca). Regole in `AGENTS.md`.
- Ogni modifica destinata al sito, comprese le correzioni di testo, va prima mostrata e provata nella [preview del Lab](https://giandjcosta.github.io/o-girrr-registro/lab/). Il sito vero resta invariato fino alla certificazione della prova e al «Vai» esplicito di Gianluca.
- Storie come un campionato vero. "Derby" con la D maiuscola. Post ufficiali mai sulle scommesse.

## Online negli ultimi giorni
- **26 ottobre, mattina — Giornata 4 entrata** (Serie A 8, Champions Cup 2ª): importata da Leghe con totali verificati (`gh-pages` `a15c34f`), Giornale n. 4, tabelloni lega 04 e coppa 02, riepilogo e archivio (`8cb66d4`), poi "Calcoli dopo la giornata" lanciato a mano (fiducia, probabilità, Borsino, Moviola con 3 episodi, post Curva; `gh-pages` `af6e8ff`, `main` `e4573d9`). Uscita pubblica del Giornale alle 09:42 (un'ora dopo la lettura), Coppa +5 minuti. La Blue brothers ha giocato in 10 (Cancellieri s.v.): `leghe_importa.py` blocca con meno di 11, importata con una copia locale che accetta 9–11, script del sito non toccato. Per la Real Madrink il modificatore difesa era 1 (non 1,5): totale 75 come Leghe. **Radio fatta** (workflow `voci-puntata` su ramo, 33 battute tutte Gemini, 3'37"): `voci-src/dati.json` ora è una copia di `girrr/dati/lab-dati.json` del sito (dati veri), `conferenze.json` con le due conferenze e le due sfide/Derby veri, `copione.py` gestisce il pareggio nelle promesse e i Derby ufficiali; puntata in archivio come `puntata-g04.mp3` (`gh-pages` `38e29d7`), il post della Curva nasce dall'archivio. Curva vuota (nessun post vero dato). Non ho potuto riascoltare l'audio. Resta da automatizzare: copiare `lab-dati.json` in `voci-src/dati.json` e lanciare la puntata a fine giornata.
- **25 ottobre, sera — Curva ripristinata**: un push di prova dell'infinite scroll (`99aabf9` e seguenti) aveva lasciato `girrr/curva.html` come guscio di 2 KB che caricava la pagina dal registro. Rimessa la versione completa di `b75fb68` (`gh-pages` `2489bf3`). Provata online in Chromium e WebKit, senza errori in console. L'infinite scroll resta da fare nel registro prima di un nuovo rilascio. 
- **25 ottobre, sera — Curva a 320 px**: la riga dei pulsanti sotto i post (risposta, rilancio, applausi, visite, condividi, elimina) usciva dallo schermo fino a 380 px. Ora a meno di 420 px i pulsanti si stringono e, solo in casi estremi (sotto 320 px o contatori molto lunghi), vanno a capo. Online su Lega e Stadio (`gh-pages` `a4154c4`); stesse righe in `ufficiale/src/sito/`, `ufficiale/girrr/` e `ufficiale/nuovo/girrr/`. Provata da 300 a 768 px in Chromium e WebKit: nessuno scorrimento laterale e console pulita.
- **24 ottobre — Moviola passo 4** (post in Curva e rilascio): online su sito vero.
- **25 ottobre — Ere** (racconto + descrizione): online (`gh-pages` `85a9415`).
- **25 ottobre — colori home Lega** (registro): primari giornale/strip in rosso.

## Changelog e archivio (25 ottobre)
- Il Changelog del registro sembrava fermo al 16 ottobre: la pagina leggeva da GitHub 6 pagine di commit a ogni apertura; senza accesso GitHub ne concede 60 l'ora, e se una sola falliva si vedeva la copia salvata del 16 ottobre.
- Ora legge solo le ultime 100 modifiche (una richiesta, tenuta 10 minuti nel browser) e le unisce alla copia salvata, rinfrescata fino al 25 ottobre. Le modifiche con lo stesso titolo nello stesso giorno compaiono una volta sola. Per rinfrescare la copia: `python3 changelog.py`.
- Archivio 5.1 in `lab/versione-5-1.html` (cosa ha portato la 5.1, cosa resta aperto); le schede dicono "Archivio 5.1" e "Anteprima 5.2". L'archivio 5.0 resta in `lab/versione-5.html`.
- Nota: `ufficiale/build.py` cerca il sito in `/home/claude/o-fant-a-girrr` e se non lo trova svuota `ufficiale/girrr/`: non lanciare `aggiorna.py` dove il sito sta in un'altra cartella.

## Infinite scroll Curva + Supabase (26 ottobre)
- **"vai" di Gianluca sullo SQL** ricevuto.
- File pronto: `sql/curva-feed-page.sql` — `curva_feed` con `p_limit` e `p_before` opzionali, più `has_more`. Compatibile col client attuale (senza i nuovi parametri resta limite 150).
- **Da fare da Gianluca:** incollare ed eseguire quello script nello SQL Editor di Supabase.
- **Client (HTML):** ancora da applicare il rendering a pacchetti (20 post + scroll) su `curva.html` (file molto grande; patch descritto in `ufficiale/src/sito/girrr/curva-scroll-README.md`). Si può fare anche solo lato client senza SQL; con lo SQL il carico rete scende quando i post superano il limite.

## Intenzioni aperte (Grok + Gianluca) — solo prova nel registro / Lab

### Mappa pubblico / privato (confermata)
**Pubblico:** Home O Girrr; Giornale; Tabellone; Curva lettura; Moviola; Conferenze lettura; Radio; Albo e Storia; Probabilità; Carriera visione; lista Sfide/Derby.
**Privato (codice squadra):** Spogliatoio; Borsino e scambi; Totogirrr giocare; scrivere/reagire in Curva; scrivere Conferenze; azioni Sfide; Statistiche personali.

### Da fare (in ordine)
1. Colori pulsanti — Lega rosso / Stadio oro (home Lega fatto; resto se serve).
2. Infinite scroll Curva — SQL pronto; client HTML ancora da applicare.
3. Login unico.
4. Lazy loading Spogliatoio.
5. Fuori per ora: notifiche; ricerca globale; menu laterale.

Niente di questo va sul sito vero senza altro "vai" esplicito (lo SQL feed è già autorizzato).

## Lazy Loading Spogliatoio — prova grafica Lega (ChatGPT, 26 ottobre 2026)
- Ramo `chatgpt/lab-lazy-grafica-lega`: `lab/prova-lazy-tabs-lega.html` usa grafica O Girrr (blu/rosso/vetro) e nove tab con dati simulati; il link compare in `lab/index.html`.
- **Corretta l'architettura:** la versione iniziale Grok non poteva intercettare `render` esterno alla IIFE del sito. Il modulo `lab/spogliatoio-lazy.js` ora esporta `window.spgLazyWrap`, che è installato dal codice originale attraverso un callback che legge lo stato privato. Non espone `D` globalmente. Guida puntuale in `lab/spogliatoio-lazy-README.md`.
- **Controlli svolti:** parsing JavaScript del modulo e degli script inline della demo (OK); verifiche statiche di link e nove tab (OK); simulazione con finto DOM per tab leggere/pesanti, skeleton, doppio frame, annullamento di click rapidi, login, cambio dati e controllo Statistiche (OK, con la limitazione del DOM simulato).
- **Test eseguiti da ChatGPT (26 ottobre):** test Node.js `prove/prova_spogliatoio_lazy.js` ricostruito con lo stesso codice del ramo: **PASS**, otto verifiche; Chromium headless con Playwright su **harness HTML locale equivalente** a 320/375/768/1280 px: **PASS** per skeleton, passaggio rapido tab, logout, overflow e console senza eccezioni. La navigazione diretta verso il sito GitHub Pages e il server localhost è bloccata dall'ambiente; test via `page.set_content`. Non sono test end-to-end sulla pagina pubblicata e non validano la resa visiva integrale della demo GitHub.
- **Da completare:** build `python3 anteprima/build.py` sul checkout completo; test browser **sulla pagina reale** del Lab, WebKit/Safari e iPhone a 320 px, autenticazione con codice valido, caricamento remoto del Borsino e fetch aggiornamenti `data.json`. La demo resta un ambiente con dati simulati.
- **Non online:** ramo e PR in attesa del «Vai» esplicito per `main` del Registro e pubblicazione nel Lab. `gh-pages` del sito vero invariato; niente rilascio senza certificazione e ulteriore «Vai».

## Carriera: obiettivi con scadenza (25 ottobre)
- Obiettivi di posizione non risultano più "Fatto" prima della scadenza. Dettaglio nello storico / lavori del 25 ottobre.
- Online sul sito vero (`gh-pages` `b75fb68`, `girrr/app.html` e `stadio/girrr/app.html`).

- **ChatGPT 26/10 — collaudo su copia integrale:** aggiunta `lab/prova-spogliatoio-reale.html`, copia dell'`index.html` vero con wrapper lazy inserito *prima* della IIFE e agganciato alla `render()` interna. Il collegamento è presente nella demo grafica Lega. Parsing di tutti gli script JavaScript inline superato (il seed JSON è escluso). La pagina usa il `data.json` remoto dell'originale via `<base>` e **non** è stata provata online con codice squadra vero; serve unirla al Lab soltanto dopo il «Vai» ed eseguire test end-to-end. Nessuna modifica a `gh-pages`.

- **ChatGPT 26/10 — PR #27 Curva completa:** su ramo `chatgpt/collaudo-curva-infinite` preparata `lab/prova-curva-completa-infinite.html` dal sorgente integrale della Curva, con 20 post visibili per batch, ulteriori pagine RPC da 150 post tramite `p_before`, deduplicazione e conservazione archivio al refresh. La demo originaria `lab/prova-infinite-scroll.html` collega la prova completa. Test sintassi JS positivo; test Supabase **solo lettura**: funzione `curva_feed(text,text,int,double precision)` presente, chiamate con `p_limit=2` e successiva `p_before` restituiscono due pagine ordinate. Nessun SQL modificato, nessuna produzione toccata. Richiede test UI online e «Vai» prima di `main`.

- **ChatGPT 26/10 — PR #28 Carriera:** corretta la funzione `esito` in `lab/index.html` e applicata la stessa sostituzione mirata a `anteprima/index.html` e `anteprima/attuale.html`. Senza storico della giornata interessata, l'obiettivo passa a `In attesa della classifica alla Nª`, mai `Fatto`/`Mancato` in base alla classifica corrente. Test JS di 4 casi superati. La build completa `python3 anteprima/build.py` non è stata eseguita per mancato checkout (DNS github.com bloccato); le due Anteprime sono state allineate con patch identica, ma serve rigenerarle/verificarle in checkout prima del merge. Nessuna produzione/Supabase modificata.

## 26 ottobre — ChatGPT: collaudo finale UI Carriera
- Corretta la griglia `.ob`: logo a dimensione fissa, colonna titolo elastica, stato sotto il titolo sugli schermi piccoli (≤700 px). Barra `.pbar` con sfondo e bordo visibile, riempimento percentuale. Titolo non più una parola per riga.
- Stessa CSS inserita in `lab/index.html`, `anteprima/index.html` e `anteprima/attuale.html`.
- Collaudo Chromium su layout rappresentativo a 300, 320, 375, 390, 430, 640, 768 e 1024 px: nessun overflow orizzontale, titolo leggibile, stato nei limiti, track barra distinto e riempimento al 99%; **8/8 viewport PASS**. Questo è un test del componente, non del sito completo online.
- Preparato nel repository originale, **solo ramo** `chatgpt/staging-20261026-lazy-curva-carriera`, l'integrazione Carriera + Lazy Loading Spogliatoio + Infinite Scroll Curva (Lega e Stadio). Sintassi JS inline delle cinque pagine controllata senza errori. Ingresso unico Grok non applicato: la Home vera contiene già `ospite.js`, e non va duplicato un secondo controllo d'accesso senza test d'integrazione.
- **Non ancora pubblicato su `gh-pages`**: attende verifica end-to-end sulla UI completa, build canonica `python3 anteprima/build.py` e via libera finale. Nessuna mutazione a Supabase.

## Anteprima 5.2 — proseguimento lavori (26 ottobre 2026)
- Le modifiche pubblicate oggi al sito originale (lazy loading dello Spogliatoio, infinite scroll Curva, correzione card sponsor, colori Fiducia in lega e arco multicolore) sono **parte del ciclo 5.2**; non costituiscono l'avvio della 5.3.
- Le nuove idee e rifiniture della 5.2 vanno prima nel **Lab/Anteprima 5.2**. Nessun rilascio automatico su `gh-pages` senza ulteriore decisione esplicita.
- La card sponsor in `lab/index.html`, `anteprima/index.html`, `anteprima/attuale.html` usa ora markup con badge sotto al titolo su mobile e progress bar a larghezza piena.
- La Fiducia in lega mostra barre monocolore basate sul valore (rosso→arancione→giallo→verde→turchese→blu), con track grigio e numero invariati.
- Il semicerchio Fiducia del presidente mantiene il gradiente completo, ma il cursore è ridotto da r=9 a **r=6**, riempimento **blu notte #141d3d** e bordo crema chiaro, in linea con la grafica del sito. Questa ulteriore rifinitura è **solo in Anteprima 5.2**, non ancora nel sito ufficiale.

## 26 ottobre 2026 — ChatGPT: Fiducia 5.2 e premi Carriera (solo Anteprima)
- Arco SVG progressivo troncato al valore, resto grigio, nessun pallino; numero flip ~520 ms quando cambia la squadra, con rispetto di reduced-motion. Modifiche in Lab e nelle due Anteprime.
- Fiducia: bonus di leadership tardiva max +4 e +3 aggiuntivi per capolista emergente; ipotesi 78→85 alla 34ª giornata, non bonus permanente.
- Premi presidente (+2 reputazione), sponsor (+1 reputazione e 50–125 Fantacrediti) mostrati come **simulazione non accreditata**. Per il server predisposti proposta schema SQL privato anti-duplicazione e piano in `proposte/`. Nessuna mutazione di Supabase, né di `gh-pages`.
- Controlli GitHub Actions: build Anteprima 5.2 e browser Chromium/WebKit sul cambio squadra.

## 26 ottobre 2026 — Seconda revisione Fiducia 5.2
- Eliminato il bonus riservato a capolista emergente. Ogni squadra riceve bonus **o** malus sulla fiducia in base a differenza tra posizione effettiva e posizione attesa, aumentato gradualmente con le giornate giocate e limitato a ±11 punti. Vale per Big, Emergenti e Outsider.
- Simulazione sponsor: premi 50/75/100/125 Fantacrediti secondo difficoltà, non accreditati realmente. Solo Lab e Anteprima 5.2.
