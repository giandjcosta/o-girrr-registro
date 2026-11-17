# Rilascio 6.2.4 «Spogliatoio e Totogirrr più fluidi»

Preparato e pubblicato da Claude nella notte del 17 novembre 2026, con il «Vai» di Gianluca del 16 novembre («se lo risolvi all'una hai già il mio vai per aggiungerlo alla 6.2.4 e pubblicarla sul sito vero, tanto son correzioni minori»). Tipo: **correzione minore**.

## Cosa cambia (rilascio/r624/applica.py, sopra la 6.2.3 pubblicata `gh-pages` `4b0fc71`)
- **«‹ O Girrr» senza fondo** (`tv.js?v=624`): il link `.v55-return` delle pagine con la testata v55 (Versioni, Notifiche…) prendeva un riquadro grigio al passaggio del mouse e dopo il tocco (`.v55-header a:hover` di `v55/ui.css`). Ora nessun link indietro ha fondo, contorno o alone.
- **Totogirrr** (`pillole.js?v=624`): `nav .nvi` tra le file «ferme»: il colore non scivola, passa con la dissolvenza di 0,18 s della 6.2.3; resta la scheda toccata tutta in vista.
- **Spogliatoio › Calendario** (`index.html`): `calCambia()` tiene la freccia dove è stata toccata, blocca l'altezza durante il cambio e fa entrare la giornata nuova in dissolvenza dal lato della freccia.
- **Spogliatoio senza salti da allenatore** (`assets/spogliatoio-lazy.js?v=624`): il «Carico…» delle schede pesanti compariva a ogni cambio dentro la scheda (giornata, ruolo, filtro), la pagina si accorciava e il browser riportava su (misurato simulando Safari: la freccia del Calendario saltava da 200 a 824 px). Ora compare solo entrando nella scheda.
- **Lab** (`rilascio/r624/lab.py`): lo Spogliatoio accetta la squadra di prova di `lab62.js` («Squadra di prova», `?squadra=…`): si vedono tutte le 12 schede da allenatore con i dati di `data.json`, senza database. Solo nel Lab.

## Prove (Chromium; WebKit non disponibile qui, Safari simulato senza ancoraggio dello scorrimento)
- `prove/v624/prova_624.js` sul Lab: iPhone SE, Pixel 7, PC × Lega/Stadio: alone con mouse e tocco su 5 pagine, Totogirrr senza pillola fantasma, Spogliatoio da allenatore (12 schede), Calendario fermo e in dissolvenza. Tutte superate.
- `prove/v623/prova_toto623.js`: 16 schermi × Lega/Stadio, 32 casi superati.
- 63 pagine (Spogliatoio e 10 pagine × Lega/Stadio × iPhone SE, PC, TV) sulla copia e poi sul sito vero: nessun errore nuovo, nessuno scorrimento laterale, pillola «V6.2.4».
- Sul sito vero anche alone e Totogirrr (`prova_624.js` senza la parte da allenatore, che richiede un codice vero).
- Numeri dello Spogliatoio nella Lega: in tutte le schede da allenatore restano colorati solo quelli di stato (Salta, variazioni del Borsino verdi e rosse).
- Non provati: Safari e Firefox veri, telefoni veri.

## Pubblicazione
- Sito: PR #22, ramo `claude/totogirrr-ui-responsive-b2pgee` (commit `f808740`, 33 file), merge su `gh-pages` **`6276dc6`**. Il `main` del sito non cambia.
- Per tornare indietro: «Revert» della PR #22 del sito, oppure `git revert -m 1 6276dc6` su `gh-pages`.
- `ufficiale/src/sito/` allineato a `gh-pages` `6276dc6` (23 file sorgente).
