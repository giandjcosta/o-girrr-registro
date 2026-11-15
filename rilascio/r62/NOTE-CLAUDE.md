# Proposta 6.2 · Campo con Campionato e Champions Cup (Claude, 15 novembre 2026)

Parte di Claude della 6.2. Prima certificazione nel Lab (`lab/novita-6-2.html`), poi «Vai» alla pubblicazione.

- **Interruttore Campionato / Champions Cup** nel Campo, Lega e Stadio. Prima le partite di Coppa si aprivano solo con `?coppa=1` dal Tabellone (il collegamento resta valido).
- **Passaggio morbido:** l'indicatore scorre (0,55 s); partite e schede escono in 0,16 s e rientrano in 0,34 s. **Lega:** indicatore e bande sfumano da rosso ad azzurro, con un velo che cambia solo opacità. **Stadio:** tutto resta oro anche in Coppa (regola di Gianluca, 15 novembre). «Riduci movimento»: cambio immediato.
- **Cerchio dei giocatori di casa:** nella Lega rosso in Campionato e azzurro in Coppa; nello Stadio azzurro come prima (l'oro è riservato al voto più alto). Ospite bianco.
- **Cerchio oro e stella:** solo il migliore in campo dei dati ufficiali (uno, o uno per squadra). Decisione di Gianluca, 15 novembre.
- **Simboli dei bonus e malus** come su Fantacalcio, con legenda: ⚽ gol, 🎯 rigore segnato, 👟 assist, 🧤 rigore parato, 🛡️ porta inviolata (portiere con voto e nessun gol subito), 🥅 gol subiti dal portiere, ❌ rigore sbagliato, 🔴 autogol, ↑ entrato. **Cartellini:** 🟨 ammonito e 🟥 espulso, con legenda; compaiono quando sarà unita [giandjcosta/o-fant-a-girrr#17](https://github.com/giandjcosta/o-fant-a-girrr/pull/17), che fa leggere i cartellini a `scripts/aggiorna_dati.py`. La lettura è provata sulle pagine vere delle giornate 1–11 di Serie A: zero differenze oltre ai cartellini, Moviola −0,5 e −1. Gol decisivo e assist da fermo non sono nella pagina dei voti di Fantacalcio.it. I simboli del portiere ospite stanno sopra il cerchio, così il bordo del campo non li taglia.
- **La tua partita si apre per prima:** con il codice della squadra il Campo apre la tua partita, in Campionato e in Coppa; nella fila resta al suo posto (anche ultima), con il contorno oro e «La tua partita», e la fila scorre per mostrarla.
- **Frecce:** ‹ › cambiano partita, « » cambiano giornata; le partite si scorrono e si toccano (o cliccano) come prima. Ogni cambio con una dissolvenza breve (0,15 s in uscita, 0,34 s in entrata), senza la vecchia animazione di entrata delle schede; clic ripetuti si sommano.
- Ogni competizione ricorda giornata e partita; l'indirizzo segue la scelta (`coppa=1`). Se il calendario della Coppa manca l'interruttore si nasconde.

## Altri ritocchi (`rilascio/r62/testi.py`)

- Tabellone › Dentro la partita: «= Stessa posizione» con la maiuscola e «1 posizione» al singolare (`girrr/v55/ui.js`, Lega e Stadio).
- Albo › La Storia: Padri Fondatori solo con il nome, tutti in fila, senza squadra (`novita.js`, Lega e Stadio). Il testo della Storia non cambia.
- Tabellone › Risultati: con il codice della squadra la tua partita resta al suo posto, con un leggero velo oro e la scritta «La tua partita», senza contorno (Campionato e Coppa). Da ospite nulla cambia. Albo d’oro e Derby restano senza oro (Gianluca, 15 novembre).
- Tabellone dello Stadio tutto oro, in Campionato e in Coppa (Gianluca, 15 novembre): interruttore, scheda Classifica/Risultati, giornata scelta, bande delle partite, cerchi dei gironi, podio e nome della tua squadra; testo scuro sull'oro. Sfondi azzurrati (Coppa) e rosati restano. Rosso per retrocessione ed eliminate invariato.
- Segnalato, non toccato: `girrr/v55/cronache.json` risponde 404 anche sul sito vero (il Tabellone lo chiede).

## Preparazione

Su una copia nuova di gh-pages: `python3 rilascio/r62/campo_coppa.py COPIA` e `python3 rilascio/r62/testi.py COPIA` (ui.js, novita.js, tabellone.html) (modifica `girrr/campo.html` e `stadio/girrr/campo.html`, si ferma se le pagine non sono quelle attese, rieseguirlo non cambia nulla). Pagine del Lab: `python3 rilascio/r62/campo_coppa.py --lab` → `rilascio/r62/pagine/`. Dopo il rilascio aggiornare anche `ufficiale/src/sito/` con le due pagine. Nessuna modifica a dati, workflow o database. Ritorno: `git revert` del commit di rilascio.

## Prove (Chromium reale, schermi emulati)

- 11 schermi × 2 grafiche (320 → 2560): niente scorrimento laterale, interruttore intero, nessun errore in console.
- Fluidità: PC 1920, media 17–18 ms per fotogramma durante il cambio (prima tecnica scartata: 26–34 ms); telefono 390 con CPU rallentata 4×: un solo fotogramma lento, quello del nuovo disegno mentre il contenuto è invisibile.
- Clic ripetuti veloci: vince l'ultimo, nessuno stato a metà. Andata e ritorno conservano la giornata.
- **Non provati qui:** WebKit e Firefox (non installati in questo ambiente: usare `registro-browser-qa.yml`), Safari su iPhone, Samsung Internet, TV fisiche.

## Giornale (15 novembre, sera)

- Gianluca vuole il Giornale come quello di oggi. `rilascio/r62/giornale_mvp.py` aggiunge al generatore originale solo la rubrica «MVP dei tifosi» con i tre candidati della giornata appena finita, in fondo alla pagina 2. Il Coro resta senza MVP e non cambiano caratteri, spazi o colonne.
- Prima ho rigenerato il numero 7 con il generatore originale e con i caratteri giusti: è identico al PDF pubblicato, a parte il nome «The Blues Brothers», aggiornato dopo. Poi ho aggiunto la rubrica.
- Caratteri necessari sulla macchina che genera il PDF: Inter, Inter Display e TeX Gyre Pagella come `serif`.

## Rubrica MVP (15 novembre, sera tardi)

Capolettera rosso sulla prima frase. La rubrica dice fino a quando si vota, presenta i tre candidati della giornata appena finita e, dal numero dopo, il verdetto della giornata prima. Il verdetto riporta squadra, risultato vero e motivo della redazione. Vale dal prossimo Giornale; i numeri già usciti non si rigenerano.

## Votazioni e verdetto MVP (15 novembre, sera)

Decisione di Gianluca:
- risultati chiusi in Curva e in Girrr Sport;
- voto unico condiviso, con il pulsante piccolo «Cambia il mio voto» per sondaggi e MVP;
- post del verdetto MVP del profilo Girrr Sport nella Curva, con la squadra taggata e nessun'altra notifica.

Dettagli in `INTEGRAZIONE.md`. La SQL resta una proposta: senza il «Vai» non si applica.
