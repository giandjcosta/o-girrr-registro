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
