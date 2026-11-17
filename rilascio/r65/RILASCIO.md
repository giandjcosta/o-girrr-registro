# Rilascio 6.5

Preparato da Claude il 17 novembre 2026. Numero scelto da Gianluca: **6.5** al posto di 6.2.5, «visto il grande cambiamento di grafica, anche se temporaneo». Tipo: **medio** (`aggiungi.py --v 6.5`).

## Cosa contiene
1. **Fluidità** (`rilascio/r65/applica.py`, sopra la 6.2.4 pubblicata):
   - Carriera, Girrr Sport e le altre schede di `app.html`: altezza ferma durante il cambio di scheda, poi accorciamento morbido (prima la pagina tornava su).
   - Il contenuto non sparisce più per un attimo: dopo un tocco su una pillola partivano due animazioni d'entrata (quella di `app.html`/`transizioni.js`, da trasparente, e quella di `pillole.js`); ora solo quella delle pillole, con un rimbalzo morbido di 0,56 s. Totogirrr invariato.
   - Pillole della Carriera e dell'Albo d'oro che scivolano come le altre.
   - Conferenze stampa senza errore se il codice della squadra non è riconosciuto.
2. **Skin Notte Tropicale** (`rilascio/r65/evento.py`): copia `temi/evento-loader.js` e `temi/notte-tropicale/` nel sito e aggiunge il caricatore alle pagine. Si accende da sola dal 18 novembre 00:00 al 24 novembre 00:00, cioè fino alla fine della giornata 8 (ora italiana), poi si spegne senza altri rilasci. Grafica unica, Curva esclusa.
3. **Curva**: i messaggi sui risultati non dicono più «vince» per un pareggio (vincitore dai gol, coppa letta con il suo schema).

## Prove fatte (Chromium)
- `prove/v65/prova_fluidita_65.js`: sito vero 6.2.4 e Lab 6.5 a confronto su iPhone 13. Sul sito vero il contenuto arrivava a opacità 0 e la Carriera saltava di 160 px; nel Lab opacità minima 0,6 e nessun salto.
- `prove/v65/prova_schermi_65.js`: 11 schermi (iPhone SE, iPhone 13, Pixel 7, Galaxy S9+, iPad verticale e orizzontale, Galaxy Tab, PC 1280 e 1920, monitor 2560, TV) × 8 pagine × con e senza tema: 176 controlli, nessun errore nuovo, nessuno scorrimento laterale.
- Non provati: Safari/WebKit e Firefox veri, telefoni veri.

## Ancora aperto
- Tabellino della Carriera sul telefono: in attesa della foto di Gianluca.
- Pagina delle novità `lab/novita-6-5.html` e messaggio definitivo (`ANNUNCIO-BOZZA.json`), dopo il nome dell'evento.

## Pubblicazione (con il «Vai» di Gianluca)
1. Copia di `gh-pages` del sito, `python3 rilascio/r65/applica.py COPIA` e poi `python3 rilascio/r65/evento.py COPIA` (seconda esecuzione di entrambi: nessun file cambiato). Provato il 18 novembre sulla copia di `gh-pages`: 36 controlli, skin accesa per data, Curva esclusa, Stadio → Lega, nessun errore.
2. `versioni.json` con `aggiungi.py --tipo medio --v 6.5` e il testo di `ANNUNCIO-BOZZA.json`.
3. PR verso `gh-pages` del sito, controllo sul sito vero, poi `STATO.md`. Per tornare indietro: «Revert» della PR.
