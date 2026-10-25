# Infinite scroll Curva — applicato (26 ottobre 2026)

## Comportamento
- In home si mostrano **20 cori** alla volta.
- Scorrendo fino a «Scorri per altri cori…» se ne caricano altri 20 (`renderFermo` mantiene la posizione).
- Cambio filtro o refresh home: si riparte da 20.
- Versione cache: `cv-ver=20261026a`.

## File da aggiornare (stesso patch)
- `ufficiale/src/sito/girrr/curva.html` (Lega)
- `ufficiale/src/sito/stadio/girrr/curva.html` (Stadio)
- Sito vero (`o-fant-a-girrr` gh-pages): `girrr/curva.html` e `stadio/girrr/curva.html`

## SQL (già online)
- `sql/curva-feed-page.sql` + `sql/curva-feed-page-fix.sql` eseguiti su Supabase.

## Nota tecnica
Il file HTML è ~155 KB: se il push automatico del file intero fallisce, applicare le 5 sostituzioni elencate in `curva-infinite.patch`.
