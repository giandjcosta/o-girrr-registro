# Proposta 6.1.1

Numero scelto da Gianluca il 14 novembre. Prima certificazione nel Lab, poi «Vai» alla pubblicazione.

- Carriera → Stagione: assi, posizioni per giornata, punto selezionabile e selettore accessibile. Dettagli bianchi da 15 px, didascalie da 14 px, lettura selezionata da 16 px. Linea azzurra e selezione oro; Lega e Stadio conservano le proprie bande.
- Curva: modello riutilizzato durante la navigazione, aggiornato normalmente dopo letture e azioni, e comunque dopo un minuto. Un solo controllo per fotogramma, notificato dal render; niente osservatore sull'intero documento né lettura forzata della larghezza della radice. Una transizione di 160 ms sul feed, indicatore a 180 ms, bozza ferma e «Riduci movimento» anche se cambia mentre la pagina è aperta. iPhone/Android conservano i propri stili; animazione comune su PC/TV.
- Bilanci: «Campionato & Champions Cup», già mostrato nel Lab.

## Preparazione

Su una **copia nuova della 6.1 pubblicata**, `python3 rilascio/r611/applica.py COPIA`. Lo script prepara tutti gli output prima di scrivere e conserva MVP, moduli e dati delle pagine di partenza. Non copiare le pagine del Lab sul sito: includono agganci di prova. Le sorgenti in `ufficiale/src/sito/` restano quelle pubblicate.

Il rilascio effettivo richiede ancora certificazione e «Vai»: aggiungere la versione minore con `rilascio/versioni/aggiungi.py`, collaudare la copia, pubblicare le pagine e verificare online. Nessuna modifica del backend o del database prevista. Ripristino con `git revert` del futuro commit di rilascio.

## Messaggio proposto per il gruppo

⚽ O Girrr 6.1.1! In Carriera la posizione in classifica si legge giornata per giornata: scegli un punto e ritrovi il piazzamento di quel turno. Nella Curva passare da una scheda all’altra è più rapido e fluido, dal telefono al PC. Buona giornata a tutti!

## Prove

`MOTORE=chromium|webkit|firefox node prove/prova_611.js` con le copie del sito servite in locale. In ambiente con proxy, Firefox usa il profilo NSS indicato da `FIREFOX_CERT_PROFILE`; nessuna disattivazione di TLS. Il database è simulato e le scritture sono bloccate nella pagina.

16 schermi × due grafiche per motore; controlli di posizione/giornata, selezione da tastiera, prima giornata e 34 giornate con 14 squadre, assenza di scorrimento laterale/errori, riuso e aggiornamento del modello, bozze e nodi conservati, cambi rapidi, animazione unica, notifiche e «Riduci movimento». Schermi e identità sono emulati. Safari su iPhone, Samsung Internet e TV fisici restano da provare.
