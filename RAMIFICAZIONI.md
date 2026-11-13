# Ramificazioni

`ramificazioni.html` è una pagina del Registro, collegata ai suoi menu. La panoramica occupa tutta la larghezza e mostra **tutti i rami già selezionati**, senza scorrimento orizzontale o riquadri da trascinare. Le schede sono disposte su due colonne ampie sui monitor e su una colonna sui telefoni e tablet. La pagina scorre verticalmente.

Ogni scheda confronta l’antenato comune con main e la punta del ramo. Le linee puntinate rappresentano il percorso compresso fra i due, **non un collegamento diretto fra commit**; le distanze sono uniformi e non codificano tempo o numero di modifiche. Se la punta è già contenuta in main, è indicato; se le storie sono indipendenti, i punti rimangono scollegati. Non viene inventata l’origine di un ramo.

«Seleziona tutti» è disponibile sia per entrambi i repository sia per ciascuno. «Solo main», le scelte singole, ricerca e filtro per stato permettono di ridurre la vista. Se sono selezionati tutti i rami, quelli nuovi ricevuti dal feed entrano automaticamente. I comandi A−/A+ ingrandiscono il testo senza allargare il grafo oltre la pagina; «Adatta alla pagina» ripristina la dimensione iniziale.

I colori visivi provengono da una palette con variazioni di tonalità, luminosità e saturazione, assegnata per distanza percettiva e con contrasto rispetto allo sfondo. Ogni ramo ha anche un simbolo e un codice stabile ricavato dal suo nome: la distinzione non dipende soltanto dal colore. L’assegnazione è conservata nel browser, nel solo spazio `og:ramificazioni:colori-v3`; nuovi rami non cambiano i colori già visti. Nessuna modifica alla sessione della lega.

Toccando una scheda si aprono i dettagli nella stessa mappa: titolo, descrizione e fonte, commit avanti/indietro, antenato, PR e collegamenti GitHub. La storia espandibile mostra fino a 24 commit conservati. Le linee continue fra commit consecutivi appaiono solo se il secondo è un genitore reale del primo; per ciascuno sono indicati anche gli altri genitori.

`ramificazioni.py` legge tutti i riferimenti dei due repository mediante copie Git senza blob, ricava genitori, percorso di primo genitore del main, antenati comuni e conteggi avanti/indietro. Titoli e descrizioni provengono dalle note di progetto, dalle PR disponibili o dall’ultimo commit, con fonte dichiarata. La versione pubblicata viene da `versioni.json` di gh-pages del sito; la versione dell’Anteprima da `registro-stato.json` del main del Registro.

## Aggiornamento automatico

Il workflow `ramificazioni.yml`, una volta presente sul main, controlla entrambi i repository ogni 15 minuti, dopo modifiche al raccoglitore sul main e su avvio manuale. Anche creazioni e cancellazioni dei rami vengono rilevate nel controllo successivo. Gli orari delle Actions possono slittare. Non modifica la cadenza settimanale della sincronizzazione Anteprima/Archivio/Changelog di Claude.

Lo snapshot viene conservato nel solo ramo tecnico `chatgpt/dati-ramificazioni`, escluso dal grafo: così un aggiornamento della mappa non genera un nuovo commit del codice, non si autoalimenta e non distribuisce il sito. La pagina mostra subito lo snapshot incluso, poi controlla la copia raw aggiornata ogni minuto. Non usa token nel browser. Se la rete fallisce conserva la copia già caricata. Una copia remota più vecchia non sostituisce una fotografia locale più recente. “Dati modificati” indica la data della modifica del contenuto, non una verifica remota che non sia documentata.

Non viene riscritto il file se il grafo è invariato. La raccolta è atomica: un errore Git non sostituisce lo snapshot valido. Se non sono disponibili le PR si usa la descrizione verificata del commit, dichiarando il ripiego.

## Riproduzione

```sh
python3 ramificazioni.py --cache /tmp/girrr-grafi
python3 prove/prova_ramificazioni.py
```

Durante la preparazione della 6.0 il workflow non viene attivato sul main. La nuova pagina e lo snapshot statico restano nel ramo di rilascio fino al deploy di Claude.
