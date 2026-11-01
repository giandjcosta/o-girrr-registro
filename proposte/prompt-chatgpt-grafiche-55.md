# Prompt per ChatGPT — grafiche uguali ovunque nella 5.5 (1° novembre 2026)

Copia tutto quello che c'è sotto la riga in ChatGPT.

---

Lavori sul repository `giandjcosta/o-girrr-registro` (Lab e Anteprima della lega O Fant A Girrr). Prima di tutto leggi `AGENTS.md` fino in fondo (soprattutto le **Regole grafiche — Lega e Stadio**, la fluidità e i tre livelli di scrittura) e `STATO.md` (sezioni del 1° novembre). Parti da `main` aggiornato, lavora sul ramo `chatgpt/grafiche-lega-stadio-55`, commit che iniziano con «ChatGPT:», apri una PR verso `main` e **non unirla tu**: la controlla e la unisce Claude. Nessuna modifica al sito vero (`o-fant-a-girrr`) né al database Supabase.

**Obiettivo (decisione di Gianluca):** le due grafiche devono essere davvero diverse, e ognuna uguale dappertutto nella 5.5: pagine, menu, sottomenu, schede, pillole, riquadri e card.
- **Lega** (grafica «normale», statica): come il riquadro delle partite del Tabellone Lega — riquadro dritto, **banda laterale dritta di 8 px rossa (#d62839)**, angoli 4 px a sinistra e 14 px a destra; schede e pillole squadrate (angoli piccoli). Riferimento nel codice: `.m` in `lab/prova-tabellone-lega.html`.
- **Stadio** (grafica col corsivo Lobster): come le righe della classifica Stadio — riquadri **arrotondati (12 px)** con la **banda laterale curva** che segue l'angolo; schede e pillole tonde. Riferimento: il blocco «Grafica Stadio: classifica a righe arrotondate» in `lab/prova-tabellone-stadio.html`.
- **Colori ufficiali:** il rosso della Lega è l'accento in tutte e due le grafiche (interruttori, bande, scheda attiva); l'oro (#ffd166) solo dove è oro anche sul sito vero (giornata selezionata, schede dell'Albo nello Stadio, primo posto in classifica). Prima di cambiare un colore confrontalo con la pagina vera su https://giandjcosta.github.io/o-fant-a-girrr/girrr/ e `/stadio/girrr/`.

**Dove applicarlo (Lega e Stadio):** Home 5.5 (riquadri, «Oggi al Girrr», riepilogo, notifiche nella Home), pagina Notifiche (schede delle notifiche, filtri), Tabellone (partite, schede Classifica/Risultati/Campo della versione C, interruttore Campionato/Champions Cup, giornate, «Dentro la partita»), Campo (menu laterale, scelta delle partite, riquadri «Come arrivano alla sfida», «I numeri del confronto», «Andamento dei punti», legenda), Albo d'oro e Annuario (schede, celle dell'Annuario, Derby), Curva 5.5 (sondaggio, commenti), e nel Lab le schede della Carriera e il Totogirrr di prova. Il modo migliore: poche regole comuni in `anteprima/5.5/ui.css` per `[data-v53-skin=lega]` e `[data-v53-skin=stadio]` (e lo stesso nel Campo e nel Tabellone del Lab), non regole sparse pagina per pagina. Dopo ogni modifica al Lab: `python3 anteprima/build.py`.

**Da non toccare** (le gestisce Claude): la logica delle notifiche personali e Supabase (`rpcN`, `notifiche_stato`, `notifiche_segna_lette`, il passaggio in `anteprima/preview-guard.js`), le funzioni `vista()`, `schede()`, `tendine()`, `passaggi()` e `ospite()` in `ui.js`, le formazioni e il grafico del Campo, la banca `lab/curva-banca-ampliata.js`, i file `lab/ospite-prova-*.js`, la Curva vera e le sorgenti `ufficiale/src/sito/`. Non rimettere l'accento oro nel Tabellone Stadio (era stato tolto il 1° novembre perché il sito vero è rosso). Non aggiungere sottomenu.

**Regole da rispettare**
- Fluidità: cambi di scheda, aperture e chiusure morbide, niente di scattante, rispettando «riduci movimento».
- Maiuscole: frasi ed etichette con l'iniziale maiuscola, anche nelle legende e dopo i simboli.
- Testi: tre livelli (in Radio e Giornale niente Fantapunti salvo vittorie per pochissimi fantapunti, Cucchiaio di legno e statistiche del Giornale); mai scommesse nei post ufficiali; niente disclaimer.
- Pagine a 320 px senza scorrimento laterale e senza errori in console.

**Prove prima della PR**
- `python3 anteprima/build.py`, `python3 prove/collaudo_anteprima_52.py`, `python3 prove/prova_moviola.py`.
- `node prove/collaudo_55_browser.js chromium` (registro servito su `http://127.0.0.1:8765`): deve finire con «problemi: 0». Su GitHub il workflow `claude-collaudo-55.yml` lo ripete con WebKit.
- Foto di ogni pagina in Lega e Stadio a 320, 390, 768 e 1280 px, una accanto all'altra, da mettere nella PR: si deve vedere a colpo d'occhio che Lega è dritta e Stadio è tonda, in ogni menu e riquadro.

**Quando hai finito:** scrivi nella PR e in `STATO.md` (una sezione «ChatGPT — grafiche Lega/Stadio») cosa hai cambiato, pagina per pagina, cosa hai provato e cosa non hai potuto provare. Elenca anche le cose che, controllando, ti sembrano mancare o incoerenti tra le due grafiche, senza correggerle se sono nella lista «Da non toccare».
