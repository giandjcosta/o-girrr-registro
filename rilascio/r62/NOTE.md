# Proposta 6.2 · Campo con Campionato e Champions Cup (Claude, 15 novembre 2026)

Parte di Claude della 6.2. Prima certificazione nel Lab (`lab/novita-6-2.html`), poi «Vai» alla pubblicazione.

- **Interruttore Campionato / Champions Cup** nel Campo, Lega e Stadio. Prima le partite di Coppa si aprivano solo con `?coppa=1` dal Tabellone (il collegamento resta valido).
- **Passaggio morbido:** l'indicatore scorre da rosso ad azzurro (0,55 s); partite e schede escono in 0,16 s e rientrano in 0,34 s; le bande delle schede sfumano (rosso → azzurro nella Lega, oro → azzurro nello Stadio) con un velo che cambia solo opacità, senza ridisegnare le schede. «Riduci movimento»: cambio immediato.
- **Cerchio dei giocatori di casa:** rosso in Campionato, azzurro in Coppa; ospite bianco.
- **Cerchio oro:** il voto più alto della partita tra le due squadre (a pari voto, tutti quelli col voto più alto). La stella ★ resta il «migliore in campo» dei dati ufficiali. Legenda aggiornata.
- **La tua partita per prima:** con il codice della squadra la tua partita è aperta e al primo posto della fila, con il contorno oro già esistente.
- Ogni competizione ricorda giornata e partita; l'indirizzo segue la scelta (`coppa=1`). Se il calendario della Coppa manca l'interruttore si nasconde.

## Preparazione

Su una copia nuova di gh-pages: `python3 rilascio/r62/campo_coppa.py COPIA` (modifica `girrr/campo.html` e `stadio/girrr/campo.html`, si ferma se le pagine non sono quelle attese, rieseguirlo non cambia nulla). Pagine del Lab: `python3 rilascio/r62/campo_coppa.py --lab` → `rilascio/r62/pagine/`. Dopo il rilascio aggiornare anche `ufficiale/src/sito/` con le due pagine. Nessuna modifica a dati, workflow o database. Ritorno: `git revert` del commit di rilascio.

## Prove (Chromium reale, schermi emulati)

- 11 schermi × 2 grafiche (320 → 2560): niente scorrimento laterale, interruttore intero, nessun errore in console.
- Fluidità: PC 1920, media 17–18 ms per fotogramma durante il cambio (prima tecnica scartata: 26–34 ms); telefono 390 con CPU rallentata 4×: un solo fotogramma lento, quello del nuovo disegno mentre il contenuto è invisibile.
- Clic ripetuti veloci: vince l'ultimo, nessuno stato a metà. Andata e ritorno conservano la giornata.
- **Non provati qui:** WebKit e Firefox (non installati in questo ambiente: usare `registro-browser-qa.yml`), Safari su iPhone, Samsung Internet, TV fisiche.
