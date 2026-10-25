# Stato del progetto O Girrr (ultimi giorni — aggiornato 26 ottobre 2026)

Per aprire una chat nuova: incolla "Leggi STATO.md nel repo o-girrr-registro e continuiamo da lì".
Lo **storico completo** (dall'inizio fino al 25 ottobre) è in `STATO-storico.md` e nel commit `940d2d374df4`.

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
- Micro correzioni di testo: online in automatico, avviso dopo. Tutto il resto: serve il "vai" di Gianluca.
- Storie come un campionato vero. "Derby" con la D maiuscola. Post ufficiali mai sulle scommesse.

## Online negli ultimi giorni
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

## Carriera: obiettivi con scadenza (25 ottobre)
- Obiettivi di posizione non risultano più "Fatto" prima della scadenza. Dettaglio nello storico / lavori del 25 ottobre.
- Online sul sito vero (`gh-pages` `b75fb68`, `girrr/app.html` e `stadio/girrr/app.html`).
