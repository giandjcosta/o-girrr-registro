# Stato del progetto O Girrr (ultimi giorni — aggiornato 26 ottobre 2026)

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
