# Stato del progetto O Girrr (ultimi giorni — aggiornato 26 ottobre 2026)

Per aprire una chat nuova: incolla "Leggi STATO.md nel repo o-girrr-registro e continuiamo da lì".
Lo **storico completo** (dall'inizio fino al 25 ottobre) è in `STATO-storico.md` e nel commit `940d2d374df4`.

## Dove vive tutto
- Sito vero: repo `giandjcosta/o-fant-a-girrr`, ramo `gh-pages` (pagine) e `main` (workflow e calcoli). Sito: https://giandjcosta.github.io/o-fant-a-girrr/
- Laboratorio e registro: repo `giandjcosta/o-girrr-registro`, ramo `main`.
- Database: Supabase, progetto `qmjqfgmvimsuxvghetgi`.
- Anteprima 5.1: https://giandjcosta.github.io/o-girrr-registro/anteprima/attuale.html (Lega) e `anteprima/index.html` (Stadio).
- Lab: https://giandjcosta.github.io/o-girrr-registro/lab/

## Regole di pubblicazione
- Assistenti: Claude Code, agente di VS Code, Perplexity, Aider, **Grok** (e Gianluca). Regole in `AGENTS.md`.
- Micro correzioni di testo: online in automatico, avviso dopo. Tutto il resto: serve il "vai" di Gianluca.
- Storie come un campionato vero. "Derby" con la D maiuscola. Post ufficiali mai sulle scommesse.

## Online negli ultimi giorni
- **24 ottobre — Moviola passo 4** (post in Curva e rilascio): online su sito vero (`gh-pages` `a8ae5c0`, `main` `c505036`).
- **25 ottobre — Ere** (racconto + descrizione): online (`gh-pages` `85a9415`).
- **25 ottobre — colori home Lega** (registro): in `ufficiale/girrr/index.html` i primari "Leggi il giornale" e strip passano da giallo a rosso (coerenza Lega = rosso, Stadio = giallo/oro).

## Intenzioni 25/26 ottobre (Grok, con Gianluca) — solo prova nel registro

Deciso insieme: separazione pubblico/privato, login unico, infinite scroll Curva, lazy loading Spogliatoio, coerenza colori pulsanti. Tutto prima nel registro, poi eventuale "vai" sul sito vero.

### Mappa pubblico / privato (confermata)
**Pubblico (senza codice):** Home O Girrr; Giornale; Tabellone; Curva in sola lettura; Moviola; Conferenze in lettura; Radio Girrr; Albo e Storia; Probabilità; Carriera (visione); lista Sfide/Derby.

**Privato (serve codice squadra):** Spogliatoio completo; Borsino e scambi; Totogirrr (giocare); scrivere/reagire in Curva; scrivere Conferenze; lanciare/rispondere alle Sfide; Statistiche personali.

### Da fare (in ordine)
1. **Colori pulsanti** — Lega: primari rossi (`#d62839`); Stadio: primari giallo/oro (`#ffd166`).
   - FATTO (25 ottobre): home Lega in `ufficiale/girrr/index.html`.
   - ANCORA: altre pagine Lega se servono.
2. **Infinite scroll Curva** — post a pacchetti (15–20), più fluido su mobile. (in corso)
3. **Login unico** — un codice squadra sblocca tutto il privato.
4. **Lazy loading Spogliatoio** — schede caricate solo quando si aprono.
5. **Fuori per ora:** notifiche; ricerca globale; menu laterale.

Niente di questo va online sul sito vero senza il "vai" di Gianluca.

## Carriera: obiettivi con scadenza corretti (25 ottobre, solo Lab e Anteprima)
- Segnalato da Gianluca: "Resta nella metà alta dopo la 10ª giornata" risultava "Fatto" alla 4ª. Prima l'etichetta "Fatto" usciva appena la barra arrivava al 100%, anche per gli obiettivi di posizione (presidente: piazzamento finale; sponsor: metà alta o fuori dagli ultimi 3 dopo la 10ª, meglio dello scorso anno).
- Ora (`lab/index.html`, funzioni `esito`, `aGiornata`, `gioc`; Anteprima rigenerata): prima della scadenza un obiettivo di posizione non è mai "Fatto" (barra al massimo 99%, etichetta "In linea", "Da recuperare" o "Ora 5° · conta la 10ª"); dopo la scadenza si guarda la classifica di quella giornata e diventa "Fatto" o "Mancato". Gli obiettivi che si accumulano (giornate sopra 60/65, punteggio massimo) sono "Fatto" appena raggiunti e "Mancato" se a fine stagione non lo sono. "Almeno N vittorie nelle prime 8 giornate" conta solo le prime 8. La classifica per giornata si calcola dai risultati di `data.json` del sito (34 giornate).
- Provato: con i dati veri nessun obiettivo di posizione risulta "Fatto" (Oranje VC: "Ora 5° · conta la 10ª"); con dati di prova a 12 giornate gli obiettivi della 10ª diventano "Fatto" o "Mancato" secondo la classifica della 10ª (Chromium). WebKit con i dati veri, 320 px, console pulita.
- Non ancora sul sito vero: al rilascio va `app.html` di `girrr/` e `stadio/girrr/`.
