# 6.6 «Gli scambi nell'app» · scaletta di rilascio

Preparata da Claude il 24 novembre 2026 sopra la 6.5.1 pubblicata. In prova nel Lab: `lab/novita-6-6.html` (anteprima in `lab/integrata-62/`, scambi simulati con `rilascio/r66/lab66.js`).

## Cosa c'è
1. **Scambi nell'app** (Spogliatoio › Mercato Scambi): «Effettua lo scambio» dopo «Valuta uno scambio», elenco «Richieste di scambio», conferma dell'altra squadra, della Lega (Oranje VC) o di un altro allenatore come testimone (mai chi l'ha proposto), rifiuto, annullamento. Vale la prima conferma, anche quella automatica da Leghe. File: `assets/scambi66.js` più quattro agganci in `index.html`.
2. **Database**: `sql/scambi-66.sql` (tabella `scambi`, funzioni `scambio_*`, notifiche e voce «scambi» del telefono). Prove: `sudo -u postgres python3 prove/v66/prova_scambi_sql.py` (37 prove, PostgreSQL locale).
3. **Dopo la conferma** (`main` del sito): `calcoli/scambi_app.py` nel nuovo workflow «Scambi dell'app, una volta al giorno» (`scambi-giornata.yml`, ogni mattina verso le 7:40 ora italiana; Gianluca: «una volta al giorno è ok»): rose in `data.json`, classifica delle rose, `girrr/dati/mercato.json` per il Giornale, post della Lega con Ciro (`calcoli/mercato-app.json`, letto da `post_curva.py`), notizia per la Radio (`voci-src/prepara_dati.py` e `puntata.py` del registro). Prove: `python3 prove/v66/prova_scambi_app.py COPIA_GH_PAGES` (14 prove).
4. **Notifiche**: link delle notifiche degli scambi allo Spogliatoio, filtro «Scambi», voce «Scambi» per il telefono, riquadro «Icona dell'app» (scudo o simbolo, `icona66.js`, `manifest-simbolo.webmanifest`, `assets/icone/`).
5. **Giornale**: riquadro «Mercato · Ufficiale» a pagina 3 (`scripts/pdf_giornale.py`), dal Giornale n° 9: c'è già lo scambio Blues Brothers–Real Madrink.
6. **Loghi**: `rilascio/loghi-66/applica.py` (scudi per sempre, simboli 2026 · 27), lanciato da `applica.py`.

## Ordine (ognuno con il «Vai» di Gianluca)
1. **SQL**: Gianluca incolla `sql/scambi-66.sql` nell'SQL Editor di Supabase (progetto `qmjqfgmvimsuxvghetgi`). Controllo: `select public.scambio_stato();` restituisce `{"ok": false, "scambi": []}`. Prima dell'SQL le pagine dicono «Gli scambi nell'app si attivano con la versione 6.6» e non mandano niente; il workflow non fa niente.
2. **gh-pages**: copia aggiornata, `python3 rilascio/r66/applica.py COPIA` (seconda volta: tutti «0»), versione con `rilascio/versioni/aggiungi.py` da `ANNUNCIO-BOZZA.json`, `versioni.json` nella radice, push. Controllo sul sito vero: Spogliatoio › Mercato Scambi, Notifiche Lega e Stadio, Tabellone, Giornale; console senza errori nuovi.
3. **main del sito**: `calcoli/scambi_app.py`, `calcoli/post_curva.py` (del registro, con la lettura di `mercato-app.json`), `.github/workflows/scambi-giornata.yml` da `rilascio/r66/workflow/` («Curva, post quasi subito» resta com'è: pubblica i post appena compaiono in `mercato-app.json`). Lanciare a mano «Scambi dell'app» una volta e guardare i tre passi.
4. **main del registro**: unione del ramo (`voci-src`, `calcoli`, `sql`, `rilascio/r66`, Lab).
5. Post nel gruppo con il messaggio di `ANNUNCIO-BOZZA.json`.

## Per tornare indietro
- gh-pages: `git revert` del commit della 6.6 (le pagine tornano alla 6.5.1; le richieste restano nel database ma nessuno le vede).
- main del sito: `git revert` del commit con `scambi_app.py` e il workflow.
- Database: in fondo a `sql/scambi-66.sql` (drop delle funzioni `scambio_*`, della tabella e dello schema `scambi_private`; le due funzioni delle notifiche si rimettono come prima togliendo l'ultimo «union all»).

## Limiti noti
- L'icona sulla schermata Home si fissa quando si aggiunge l'app: per cambiarla bisogna togliere l'app e aggiungerla di nuovo (su iPhone di sicuro). Lo dice il riquadro.
- «Conferma dalla notifica» apre la richiesta nello Spogliatoio, dove si conferma con un tocco: i pulsanti dentro la notifica non ci sono (su iPhone non sono supportati).
- I ruoli dello scambio li controlla la pagina e li ricontrolla il workflow sulle rose vere (se non tornano lo scambio diventa «non valido» e non si applica). Il database controlla squadre, numero di giocatori e doppioni.
- Provato con Chromium (16 schermi). Safari, Firefox e telefoni veri non provati.
