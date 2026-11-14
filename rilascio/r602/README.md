# Giro di boa e rilascio 6.0.2

`calcoli/giro_di_boa.py` è l'unico calcolo di pagina, album e Radio. Legge risultati pubblicati, fiducia e aspettative fisse, più le due letture pubbliche MVP/Derby. Scrive il JSON del sito solo attraverso **Calcoli dopo la giornata**. Le prove e l'esempio del Lab scrivono esclusivamente copie separate.

Il bilancio comprende `finora`, `andata` dalla 17ª e `ritorno` dalla 18ª. Posizione e punti sono cumulativi fino alla data scelta; casa, trasferta e gli altri bilanci riguardano il periodo. A pari punti vale l'ordine del Tabellone (Fantapunti prima della differenza reti). La zona retrocessione è l'ultimo posto. La fascia non è conservata nelle aspettative: «Dato non conservato». I Derby sono le coppie ufficiali disponibili; cambi storici di ufficialità non conservati restano dichiarati.

Gli album sono tre PNG 1080×1350, insieme in `navigator.share({files})`, senza testo. La pagina consente squadra/campionato e tutti i periodi, anche da ospite. Il nome mostrato «The Blues Brothers» mantiene la chiave interna. Le scelte restano anche quando Carriera si ridisegna dopo le letture.

Radio: `voci-src/segmento_giro_boa.py` legge lo stesso JSON, senza ricalcolare. Segmento alla 17ª sull'andata e alla 19ª sulle prime due del ritorno. Si attiva automaticamente soltanto dalla **versione pubblicata 6.0.2**; per la preparazione testuale nel Lab c'è `--giro-di-boa`. Nessun servizio vocale nelle prove.

## Preparazione

Su copia fresca della **6.0**, applicare una volta `r601/applica.py`; per la 6.0.2 continuare con `r602/applica.py` sulla stessa copia. Il condividi.js della 6.0.1 rimane congelato. R601 include la correzione del montaggio ritardato di Cerca: rispetta le tre schede pubbliche previste, indipendentemente dal browser.

`python3 rilascio/r602/prepara_server.py COPIA_MAIN_SITO` copia il nuovo calcolo e aggiunge il passo al workflow corrente. Rifiuta ancoraggi cambiati. Le sorgenti Radio rimangono nel Registro, letto da radio-giornata.yml. La copia `server/dopo-giornata.yml` serve alla revisione.

L'ingresso manuale `solo_giro_di_boa=true` salta chiusure, post, promesse, duelli e tutte le operazioni DB. Esegue solo le due letture pubbliche MVP/Derby e salva il JSON su gh-pages. Usarlo per il primo popolamento; niente generazione manuale di dati pubblicati.

## Prove riproducibili

```sh
python3 prove/prova_giro_di_boa.py
python3 prove/server_range.py --directory CARTELLA_WEB --port 8890
MOTORE=chromium BASE=http://127.0.0.1:8890/o-fant-a-girrr/ node prove/prova_giro_di_boa_browser.js
MOTORE=webkit node prove/prova_cerca_pubblica.js
MOTORE=firefox FIREFOX_CERT_PROFILE=PROFILO_NSS node prove/prova_giro_di_boa_browser.js
VERSIONE=602 MOTORE=chromium node prove/prova_601.js
MOTORE=chromium node prove/prova_602.js
MOTORE=chromium node prove/prova_derby_schede.js
```

Firefox: creare con `certutil` un profilo NSS e importare la CA del proxy; non disattivare TLS. La prova HTTPS dell'ambiente con quel profilo ha risposto 200. WebKit può usare `WEBKIT_PATH`. La matrice contiene 16 schermi nei tre motori reali, con due grafiche. I casi futuri e lo stress dei 60 album sono **fixture dichiarate**, mai anteprime dei risultati reali.

Lab: `prove/prova_giro_di_boa_lab.js` controlla ingresso e cache. Nell'ambiente WebKit la simulazione offline restituisce un errore interno anche su un service worker minimo indipendente dal progetto; Chromium e Firefox riaprono lo specchio senza rete. Non equivale a una prova di Safari su iPhone.

Le condivisioni nei test sono simulate e i file vengono verificati per numero, MIME e contenuto. WhatsApp su iPhone, Samsung Internet, Safari/Chrome/Edge di marca e TV fisica richiedono prove sui dispositivi; l'identità Tizen emulata non certifica il browser Samsung.

## Pubblicazione e ritorno indietro

Gianluca ha autorizzato il deploy della 6.0.2 il 14 novembre, dopo le verifiche. Prima Lab, poi backend e JSON generato dal workflow, quindi 6.0.1 e 6.0.2. Usare `rilascio/versioni/aggiungi.py --tipo minore` per ciascuna, con messaggi e changelog che parlano delle novità del sito. Sincronizzare il Registro con il workflow ordinario dopo la pubblicazione.

Gli hash effettivi e i comandi di `git revert` saranno annotati in STATO.md al termine. Nessun push forzato; pull con rebase prima di ogni push.
