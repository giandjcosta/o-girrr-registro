# Stato del progetto O Girrr (aggiornato 24 ottobre 2026, mattina)

Per aprire una chat nuova: incolla "Leggi STATO.md nel repo o-girrr-registro e continuiamo da lì".

## Dove vive tutto
- Sito vero: repo `giandjcosta/o-fant-a-girrr`, ramo `gh-pages` (pagine) e `main` (workflow e calcoli). Sito: https://giandjcosta.github.io/o-fant-a-girrr/
- Laboratorio e registro: repo `giandjcosta/o-girrr-registro`, ramo `main`.
- Database: Supabase, progetto `qmjqfgmvimsuxvghetgi`.

## Intenzioni 25/26 ottobre (Grok, con Gianluca) — solo prova nel registro

Deciso insieme: separazione pubblico/privato, login unico, infinite scroll Curva, lazy loading Spogliatoio, coerenza colori pulsanti. Tutto prima nel registro, poi eventuale "vai" sul sito vero.

### Mappa pubblico / privato (confermata)
**Pubblico (senza codice):** Home O Girrr; Giornale; Tabellone; Curva in sola lettura; Moviola; Conferenze in lettura; Radio Girrr; Albo e Storia; Probabilità; Carriera (visione); lista Sfide/Derby.

**Privato (serve codice squadra):** Spogliatoio completo; Borsino e scambi; Totogirrr (giocare); scrivere/reagire in Curva; scrivere Conferenze; lanciare/rispondere alle Sfide; Statistiche personali.

### Da fare (in ordine)
1. **Colori pulsanti** — Lega: tutti i primari rossi (`#d62839`); Stadio: tutti i primari giallo/oro (`#ffd166`). Secondari restano trasparenti/bianchi.
   - FATTO (25 ottobre): home Lega in `ufficiale/girrr/index.html` — "Leggi il giornale" e il pulsante dello strip passano da giallo a rosso. Stadio era già coerente via skin.
   - ANCORA: allineare le altre pagine Lega (Totogirrr, Spogliatoio, app, giornale, ecc.) se ci sono primari gialli fuori posto.
2. **Infinite scroll Curva** — caricare i post a pacchetti (es. 15–20) invece di tutta la cronologia in una volta; più fluido su mobile.
3. **Login unico** — un solo accesso con codice squadra che sblocca tutto il privato; le sezioni pubbliche restano visibili senza login.
4. **Lazy loading Spogliatoio** — caricare le schede (Borsino, Scambi, Infortunati…) solo quando si aprono, non tutto all’avvio.
5. **Fuori per ora:** notifiche push; ricerca globale (idea per dopo); menu laterale (non richiesto: si tiene la navigazione attuale dalla home).

Niente di questo va online sul sito vero senza il "vai" di Gianluca.

---

NOTA: il resto dello storico di STATO.md (Moviola, Ere, rilascio del 24–25 ottobre, ecc.) è stato temporaneamente ridotto durante un aggiornamento; va reintegrato dal commit precedente `f4f21773903d705485ad157fbe475a588799a266` se manca ancora dettaglio.
