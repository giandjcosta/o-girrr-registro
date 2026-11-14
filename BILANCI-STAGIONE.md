# Bilanci della stagione · Regole della 6.1

Richieste di Gianluca del 14 novembre 2026. La versione pubblicata è **6.1**; la 6.0.2 era una bozza, non un rilascio. Online resta la versione indicata da `registro-stato.json`. Pubblicare il Lab non pubblica il sito della lega.

- **Periodo:** «Fino ad ora» è la scelta iniziale. Le tappe sono cumulative dalla 1ª giornata: inizio (1), ogni cinque giornate (5, 10, 15, 20, 25, 30), metà (17) e fine (34). Si sbloccano solo con risultati completi e pubblicati, rispettando l’attesa di un’ora dei risultati. Una giornata incompleta blocca anche le successive. Le tappe passate restano disponibili. Il ritorno, separato, resta disponibile dalla 18ª.
- **Competizione:** Campionato rosso; Champions Cup azzurra; entrambe con i due colori. Le tappe seguono le giornate del Campionato; la Coppa comprende i risultati pubblicati fino alla stessa giornata di Serie A. Nessuna somma di punti né classifica unica: i punti del Campionato e dei gironi della Coppa restano separati. Nella fase a eliminazione i risultati non danno punti di classifica.
- **Ambito:** una squadra oppure la situazione generale. Ogni numero, grafico, risultato, primato e commento segue ambito, periodo e competizione. I primati riportano il numero dei gol del risultato; chi non ha giocato è escluso dai primati. I Fantapunti hanno sempre l’unità esplicita nella sezione tecnica.
- **Redazione:** bilanci fattuali generati dallo stesso calcolo. Per la lega raccontano capolista e distacco reale, gruppi ravvicinati e coda; per la Coppa gironi, qualificazione o risultati della fase finale; per una squadra il suo percorso. Le citazioni settimanali firmate restano conservate separatamente, senza essere presentate come un commento all’intero periodo.
- **Curva:** soltanto parole realmente pubblicate, con autore, data e collegamento al contesto conservato nel JSON. Un post va selezionato per periodo, competizione e squadra o tema generale. Non basta il nome dell’autore. I commenti ambigui fra le due competizioni vengono esclusi; se manca una voce pertinente compare **Dato non conservato**. Nella vista mista si possono affiancare due voci distinte, ciascuna con la propria competizione.
- **Immagini:** due immagini per una competizione; tre per entrambe (Campionato, Coppa, bilancio e voci). Si condividono insieme come soli file PNG, senza testo o collegamenti aggiunti.
- **Aggiornamento:** `calcoli/giro_di_boa.py` è l’unico calcolo per pagina, immagini e segmento Radio. Il workflow «Calcoli dopo la giornata» aggiorna `girrr/dati/giro-di-boa.json`; quei dati sul sito li scrive soltanto il workflow. Il Lab ha un campione separato e dichiarato. La Radio usa i periodi `andata` alla 17ª e `ritorno` alla 19ª e resta inattiva fino al rilascio della 6.1.

## Preparazione, senza pubblicazione

Su una copia fresca della **6.0.1** pubblicata: `python3 rilascio/r61/applica.py COPIA`. Non riapplicare la 6.0.1. Il wrapper riusa il pacchetto interno storico `r602`, mantenendo i vecchi collegamenti come reindirizzamenti. Il pacchetto non cambia `versioni.json` e non pubblica.

Il server si prepara con `python3 rilascio/r602/prepara_server.py COPIA_MAIN`. Ramo del sito `chatgpt/giro-boa-calcoli-602`, PR #13 in bozza: nessun merge o avvio del workflow senza il Vai al rilascio. Al futuro rilascio il numero si calcola con `rilascio/versioni/aggiungi.py --tipo medio`: dalla 6.0.1 alla 6.1, senza una 6.0.2 fittizia.

## Collaudi

`prove/prova_giro_di_boa.py` verifica risultati, soglie di sblocco, tappe stabili, Coppa, commenti pertinenti e Radio senza servizi vocali. `prove/prova_giro_di_boa_filtri_61.js` incrocia sedici schermi e le due grafiche nei tre motori, con album e controlli dei periodi futuri. Le altre prove del bilancio, grafica, Carriera e Radio restano nel workflow `giro-boa-602-qa.yml`.

Schermi e identità sono emulati; i motori Chromium, WebKit e Firefox sono reali. WhatsApp, Safari/iPhone, Samsung Internet e televisori fisici richiedono verifica sui dispositivi: nessuna condivisione verso persone viene eseguita dalle prove.
