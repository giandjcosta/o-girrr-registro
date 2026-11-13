# Ramificazioni

`ramificazioni.html` è una pagina del Registro. Usa i colori e i caratteri del sito, un grafo SVG navigabile e un pannello dettagli. Si possono selezionare repository, rami e stato, cercare, ingrandire il grafo, aprire un commit e seguire i collegamenti alle PR.

`ramificazioni.py` legge **tutti i riferimenti dei rami** dei due repository mediante copie Git senza blob. Ricava da Git i genitori, il percorso di primo genitore del main, l’antenato comune e i conteggi avanti/indietro. Non inventa l’origine di un ramo: il merge-base con main è un punto di confronto, non la prova della sua creazione. Le storie indipendenti di main e gh-pages restano separate. Il grafo mostra una finestra dichiarata dei commit; il resto è indicato con linee tratteggiate.

I titoli e le descrizioni provengono, in ordine, dalle note di `ramificazioni-note.json`, dalle PR disponibili o dall’ultimo commit. La pagina indica la fonte. I colori derivano dall’identità repository/ramo e rimangono stabili. Il numero di versione viene da `versioni.json` di gh-pages del sito e da `registro-stato.json` del main del Registro.

## Aggiornamento automatico

Il workflow `ramificazioni.yml`, una volta presente sul main, controlla entrambi i repository ogni 15 minuti e agli eventi di creazione/eliminazione rami. Gli orari delle Actions possono slittare. Non modifica la cadenza settimanale della sincronizzazione Anteprima/Archivio/Changelog di Claude.

Lo snapshot viene conservato nel solo ramo tecnico `chatgpt/dati-ramificazioni`, escluso dal grafo: così un aggiornamento della mappa non genera un nuovo commit del codice, non si autoalimenta e non distribuisce il sito. La pagina mostra subito lo snapshot incluso, poi controlla la copia raw aggiornata ogni minuto. Non usa token nel browser. Se la rete fallisce conserva la copia già caricata. “Dati modificati” indica la data della modifica del contenuto, non una verifica remota che non sia documentata.

Non viene riscritto il file se il grafo è invariato. La raccolta è atomica: un errore Git non sostituisce lo snapshot valido. Se non sono disponibili le PR si usa la descrizione verificata del commit, dichiarando il ripiego.

## Riproduzione

```sh
python3 ramificazioni.py --cache /tmp/girrr-grafi
python3 prove/prova_ramificazioni.py
```

Durante la preparazione della 6.0 il workflow non viene attivato sul main. La nuova pagina e lo snapshot statico restano nel ramo di rilascio fino al deploy di Claude.
