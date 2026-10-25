# Stato del progetto O Girrr (aggiornato 25 ottobre 2026, sera)

Per aprire una chat nuova: incolla "Leggi STATO.md nel repo o-girrr-registro e continuiamo da lì".

**Nota:** lo storico dettagliato (Moviola passi 1–4, Ere, rilascio 24–25 ottobre) è nel commit `940d2d374df4`. Qui restano dove vive tutto, le regole e le intenzioni attuali.

## Dove vive tutto
- Sito vero: repo `giandjcosta/o-fant-a-girrr`, ramo `gh-pages` (pagine) e `main` (workflow e calcoli). Sito: https://giandjcosta.github.io/o-fant-a-girrr/
- Laboratorio e registro: repo `giandjcosta/o-girrr-registro`, ramo `main`.
- Database: Supabase, progetto `qmjqfgmvimsuxvghetgi`.
- Anteprima 5.1: https://giandjcosta.github.io/o-girrr-registro/anteprima/attuale.html (Lega) e `anteprima/index.html` (Stadio).

## Regole di pubblicazione
- Micro correzioni di testo: online in automatico, avviso dopo. Tutto il resto: serve il "vai" di Gianluca.
- Storie come un campionato vero. "Derby" con la D maiuscola. Post ufficiali mai sulle scommesse.

## Online di recente
- Moviola passo 4 + post in Curva (24 ottobre).
- Ere con racconto e descrizione (25 ottobre, gh-pages `85a9415`).

## Intenzioni 25/26 ottobre (Grok, con Gianluca) — solo prova nel registro

Deciso insieme: separazione pubblico/privato, login unico, infinite scroll Curva, lazy loading Spogliatoio, coerenza colori pulsanti. Tutto prima nel registro, poi eventuale "vai" sul sito vero.

### Mappa pubblico / privato (confermata)
**Pubblico (senza codice):** Home O Girrr; Giornale; Tabellone; Curva in sola lettura; Moviola; Conferenze in lettura; Radio Girrr; Albo e Storia; Probabilità; Carriera (visione); lista Sfide/Derby.

**Privato (serve codice squadra):** Spogliatoio completo; Borsino e scambi; Totogirrr (giocare); scrivere/reagire in Curva; scrivere Conferenze; lanciare/rispondere alle Sfide; Statistiche personali.

### Da fare (in ordine)
1. **Colori pulsanti** — Lega: tutti i primari rossi (`#d62839`); Stadio: tutti i primari giallo/oro (`#ffd166`).
   - FATTO (25 ottobre): home Lega in `ufficiale/girrr/index.html` — "Leggi il giornale" e strip in rosso.
   - ANCORA: allineare le altre pagine Lega se servono.
2. **Infinite scroll Curva** — post a pacchetti (15–20), più fluido su mobile. (prossimo)
3. **Login unico** — un codice squadra sblocca tutto il privato.
4. **Lazy loading Spogliatoio** — schede caricate solo quando si aprono.
5. **Fuori per ora:** notifiche; ricerca globale; menu laterale.

Niente di questo va online sul sito vero senza il "vai" di Gianluca.
