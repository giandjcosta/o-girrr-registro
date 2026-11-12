# Idee per O Girrr — proposte e non ancora fatte

Elenco da consultare, aggiornato da chi propone o realizza un'idea. Quando un'idea si fa, si sposta in fondo in «Fatte» con la data e il riferimento in `STATO.md`.
Nessuna di queste è approvata: ognuna aspetta il «vai» di Gianluca (e, se tocca il database, un «vai» apposta).

## In attesa

### 5.8 · Claude in redazione (decisione di Gianluca, 11 novembre 2026: «questa novità la mettiamo per la 5.8»)
- **Niente API a pagamento** (Gianluca: «pago già un abbonamento per Claude, non voglio pagare altri soldi»): l'abbonamento non copre le chiamate da un sito, quindi Claude non risponde in diretta dentro le pagine. Lavora invece **dietro le quinte** con una sessione programmata di Claude Code (compresa nell'abbonamento, usa i suoi limiti di utilizzo) che legge dati e database, scrive i contenuti e li pubblica sul sito come file.
- **Prima parte:** domande della conferenza su misura per ogni squadra, preparate prima di ogni giornata dalla situazione vera (classifica, Derby, promesse); giudizio delle risposte scritte a mano (tono, promessa) e domanda successiva del giornalista, qualche volta al giorno.
- **Poi:** risposte di Ciro Trattativa e Girrr Sport ai cori, cronache delle partite, riassunto della settimana per ogni allenatore, commento del Giro di boa.
- **Regole per Claude:** dati veri, «Dato non conservato» dove mancano, niente scommesse nei post ufficiali, niente Fantapunti in Radio e Giornale (con le eccezioni di `AGENTS.md`), maiuscola dopo «·».
- **In diretta, solo se servirà:** Gemini con il livello gratuito (chiave già usata per la Radio), con limiti giornalieri e ritorno alle frasi fisse quando finiscono.


### Scarica la Radio per il treno (Claude, 9 novembre 2026; Gianluca: «per ora no»)
Un pulsante «Scarica per ascoltare offline» accanto alla puntata: salva l'mp3 (circa 1,4 MB) nella copia offline.

### Calendario delle giornate in Google Calendar (Claude, 9 novembre 2026; Gianluca: «per ora no»)
Un file `.ics` scritto dai workflow con le giornate e l'orario di consegna della formazione: si aggiunge una volta a Google Calendar (o al calendario dell'iPhone) e si aggiorna da solo, con il promemoria.

### Conto alla rovescia della formazione scritto in Home
La notifica 3 ore e 1 ora prima è online con la 5.6. Resta da fare, se si vuole, il conto alla rovescia scritto anche nella Home.

### Risultati provvisori durante la giornata (Gianluca: «si potrebbe usare Fantacalcio, ma non ho un'API della loro app»)
- Fantacalcio/Leghe non ha un'API pubblica. Le strade possibili, tutte da verificare prima: (1) leggere Leghe dal browser con l'accesso di Gianluca, come già si fa per importare le giornate: funziona solo con il PC acceso e collegato, troppo fragile per il «live»; (2) un servizio di dati live di Serie A (gol, assist, cartellini, minuti), da scegliere guardando costi e condizioni d'uso.
- Anche con la fonte, durante le partite non ci sono i voti: si mostrerebbero solo i fatti certi dei giocatori schierati, senza inventare un punteggio. Il risultato vero resta quello di Leghe.

### Versione in inglese (Gianluca, 9 novembre 2026: «per potenziali interessati, ma nessuno la chiede ora») — in attesa
- **Non è una 5.6.1:** sarebbe almeno un aggiornamento medio (5.7).
- **Interfaccia** (menu, pulsanti, titoli, schede, legende, avvisi, notifiche): migliaia di frasi in più di 15 pagine, ognuna doppia (Lega e Stadio); Carriera, Curva e Spogliatoio sono file molto grandi. Servono un interruttore IT/EN e un dizionario: diverse sessioni di lavoro e molte prove.
- **Contenuti scritti ogni giornata** (Giornale, Radio, Curva e personaggi, cronache, Moviola, storie dell'Albo): tradurli vuol dire cambiare i workflow e generare ogni testo due volte, con lavoro e costi in più ogni settimana.
- **Restano uguali:** nomi di squadre, giocatori e allenatori, numeri e risultati.
- **Proposta:** a fasi. Prima l'interfaccia con l'interruttore IT/EN (Giornale, Radio e Curva restano in italiano); i contenuti dopo, solo se servono.

### Altre idee (Claude, 9 novembre 2026)
- **Testa a testa:** scegli due squadre e vedi i loro scontri della stagione (Campionato e Champions Cup), la classifica a confronto e, se è un Derby, la sua storia. Per le stagioni passate dove manca il dato: «Dato non conservato».
- **MVP dei tifosi:** dopo ogni giornata un sondaggio in Curva con tre candidati scelti dai dati (migliori voti della giornata); il vincitore finisce nel Giornale e nell'Annuario.
- **Promemoria del mercato scambi:** quando si apre e si chiude una finestra di mercato, avviso in Home e notifica sul telefono, con il conto alla rovescia.
- **Testo più grande:** un interruttore in Info per ingrandire i caratteri su tutte le pagine (utile su TV e per chi legge da lontano).

### Nuove idee (Claude, 10 novembre 2026)
- **Menzioni sul telefono:** pronte nel Lab (interruttore «Menzioni»), aspettano il «vai» sul database (`rilascio/menzioni/menzioni.sql`).
- **Sala stampa:** fatta nel Lab dentro la Conferenza, sotto la tua (decisione di Gianluca), con «Silenzio stampa».
- **Conferenza del dopo partita:** fatta nel Lab sotto la conferenza stampa; aspetta il «vai» sul database (`rilascio/conferenze/dopo.sql`).
- **Diretta in salotto (TV):** prova grafica nel Lab (`lab/prove-grafiche/salotto.html`), da decidere.
- **Classifica dei Derby:** punti fatti solo negli scontri tra rivali, con il re dei Derby della stagione (dove manca il dato: «Dato non conservato»). Gianluca: «si potrebbe fare potenzialmente».
- **Giro di boa:** prova grafica nel Lab (`lab/prove-grafiche/giro-di-boa.html`), da decidere; si sbloccherebbe alla 17ª giornata.

### Novità proposte per l'app (Claude, 12 novembre 2026, su richiesta di Gianluca)
Nessuna è fatta, tranne il video della giornata, che è una prova nel Lab. Tra parentesi: cosa serve.
- **Video**
  - *Video della giornata* (prova nel Lab: `lab/video-giornata/`, esempio `giornata-7.mp4`): 16 secondi in verticale per storie e stato di WhatsApp, fatti dai dati veri (risultati, podio, prossima giornata). Passo dopo: «Condividi → Video» nel Tabellone, registrato dal telefono stesso (MediaRecorder: MP4 su iPhone, WebM o MP4 su Android), senza servizi a pagamento.
  - *La classifica che si muove*: le barre delle 10 squadre che corrono giornata per giornata fino a oggi (dati già in `data.json`).
  - *La Radio in video*: la puntata della Radio con i titoli che scorrono e l'onda della voce, da mandare su WhatsApp (ffmpeg nel workflow, gratis).
  - *Il mio girone d'andata animato*: la pagella del Giro di boa che si compone pezzo per pezzo.
- **Funzionalità** (Gianluca, 12 novembre: «le aggiungerei tutte»): pillola «Nuovi cori», bozza del coro e link a ogni coro **in prova nel Lab** (vedi `STATO.md`, 12 novembre (5)). **Promemoria della formazione: scartato** (Gianluca, 12 novembre: «niente promemoria per le formazioni, lasciamolo fuori»; il sito non sa chi ha schierato).
- **Grafica e UI:** Curva con lo stile del sistema (in prova); sagome grigie mentre carica al posto di «Carico…»; colori della propria squadra nell'app (come Material You); tema scuro automatico la sera su tutto il sito.
- **Collegamenti:** anteprima con immagine quando mandi un link della lega su WhatsApp (Open Graph); codice QR per entrare con la propria squadra su un telefono nuovo; calendario delle giornate (idea già sopra); tasto per aprire Leghe Fantacalcio sulla formazione.
- **Interattività:** reazioni ai cori oltre all'applauso (database, «vai» apposta); «allenatore della settimana» votato dai tifosi; quiz sulla storia della lega; vibrazione leggera all'applauso su Android (su iPhone Safari non la permette).
- **Statistiche:** la stagione in Curva di ogni squadra (cori, applausi ricevuti, coro più applaudito); andamento della posizione giornata per giornata per tutte; partite vinte e perse per pochi fantapunti (livello tecnico).
- **Compatibilità:** prove automatiche con WebKit (il motore di Safari) per ogni novità, ora possibili; iPhone con iOS 16 o più vecchi (molle sostituite da curve classiche, da provare); Samsung Internet e Firefox su Android; VoiceOver e TalkBack (etichette dei pulsanti, contrasto).

## Fatte
- **Online con la 5.7** (11 novembre 2026, vedi `STATO.md`): Sala stampa, conferenza del dopo partita, menzioni sul telefono; tag delle squadre nei post della conferenza, conferenza bloccata dopo la pubblicazione, tono nella fiducia, conferenza dell'avversario con «Rispondi in Curva», scheda Promesse della Carriera, **Testa a testa** (pagina Derby) e **testo più grande** (solo sulle smart TV, senza interruttore: decisione di Gianluca).
- **Copia offline** (online il 9 novembre 2026, `gh-pages` `e06cbe2`), vedi `STATO.md`.
- **Scorciatoie dell'icona nella grafica scelta** (online il 9 novembre 2026, `gh-pages` `e06cbe2`): Tabellone, Curva, Giornale, Totogirrr. Non su iPhone.
- **5.6** (online il 9 novembre 2026, `gh-pages` `caa13c6`): notifiche sul telefono (con la formazione 3 ore e 1 ora prima), Cerca un giocatore (scheda dello Spogliatoio), Condividi come immagine, La mia stagione (Carriera), pagina Versioni.
