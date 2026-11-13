# Integrazione ChatGPT per il rilascio 6.0 di Claude

Gianluca ha visto e approvato la prova. Il 13 novembre ha autorizzato preparazione e merge, **senza pubblicazione**. La 6.0 verrà pubblicata da Claude. Coordinamento tracciato in https://github.com/giandjcosta/o-girrr-registro/issues/57.

- Registro: [PR #58](https://github.com/giandjcosta/o-girrr-registro/pull/58), verso il ramo 6.0 di Claude.
- Server: [PR #9](https://github.com/giandjcosta/o-fant-a-girrr/pull/9), **già unita** al ramo 6.0, merge `19b8ec2027106b0e40d655b54c56b57a68de674c`.
- Nessuno di questi merge distribuisce Pages. Il messaggio finale nel ticket contiene stato del Registro ed esiti del collaudo.

## Contenuti

- Squadra MVP dei tifosi in Girrr Sport, richiamo Home, voto anche in Curva, archivio dei verdetti in Albo/Record. Redazione e personaggi partecipano sempre. Gli allenatori possono votare, cambiare e ritirare il voto; un solo voto per squadra, verificato con il codice della Curva. Pesi 40/40/20 con voti umani, 50/50 senza.
- Classifica dei Derby con punti 3/1 e giocate/V/N/P, Campionato e Champions Cup separati, registro ufficiale aggiornato. Nessuna ammissione ricostruita da un indice di rivalità.
- Settimana personale in Oggi al Girrr e archivio in Carriera. Dieci racconti della settimana iniziale, sei episodi storici dell’Oranje già curati, niente premi retroattivi. Il resto si aggiorna nella redazione già programmata: `redazione/ISTRUZIONI.md` e `LA-MIA-SETTIMANA.md`.
- Pagina Ramificazioni nel Registro, con i due grafi reali, colori, PR, commit, dettagli e aggiornamento automatico: `RAMIFICAZIONI.md`.

## Pacchetto di rilascio

`rilascio/rilascio60.py` conserva tutti i passaggi di Claude e, alla fine, richiama `rilascio/tifosi60/applica.py`. L’aggancio lavora sulle pagine appena preparate: **non copiare i quattordici HTML della vecchia prova sul sito**. Il modulo aggiunge CSS/JS a Home, app, Curva, Derby e Albo nelle due grafiche. Video, Radio, condivisione e Curva per sistema rimangono quelli di Claude.

Integrati anche i Tabelloni ufficiali di «Condividi la giornata» dell’ultimo ramo di Claude (`3b85b41`): il pacchetto conserva i suoi cinque elementi.

Il modulo tifosi è idempotente. Lo script complessivo di Claude va eseguito **una volta su una copia fresca di gh-pages**: la seconda applicazione della patch Curva incontra le sue assert originarie. Non usarlo due volte sulla stessa directory.

Il ramo server contiene `calcoli/tifosi/` e `.github/workflows/tifosi-giornata.yml`. La logica del modello è identica a quella distribuita al browser. Si riusa la chiave server già prevista dai premi, tramite il suo controllo del tipo/progetto (copia identica di `calcoli/premi/registra_premi.py` inclusa anche nel pacchetto server); nessun nuovo segreto viene esposto al client. La nuova automazione rifiuta l’attivazione finché sul sito non è pubblicata la 6.0.

## Ordine per Claude al deploy

1. Aggiornare entrambi i rami 6.0 e leggere i riferimenti delle PR e i collaudi riportati nel ticket #57. Le PR #55/#56 descrivono fasi precedenti: non unirle sopra questa integrazione.
2. Preparare e verificare la nuova SQL `sql/mvp-tifosi-60.sql`. **Non è stata eseguita sul database della lega.** Seguire il requisito di autorizzazione Supabase in AGENTS.md prima dell’applicazione. Lo schema privato aggiunge solo il nuovo premio; nessun credito o reputazione modificati.
3. Aggiornare la redazione al risultato corrente se nel frattempo è stata giocata un’altra giornata. `tifosi.py controlla` blocca il rilascio con firme obsolete o storie mancanti. La scadenza deriva dal primo incontro vero del turno successivo, con fuso di Roma. In caso di ultima giornata senza calendario serve una scadenza editoriale esplicita.
4. Su **copia fresca locale** di gh-pages eseguire `python3 rilascio/rilascio60.py CARTELLA --lab` per le prove; per il sito eseguirlo senza `--lab`, così gli agganci di collaudo Curva non entrano in produzione. Verificare percorsi e assenza di errori con la suite nuova e quella di Claude.
5. Aggiornare la voce 6.0 in `versioni.json` con la procedura ordinaria, includendo anche MVP/Derby/settimana. Il messaggio non è stato pubblicato né aggiunto alla cronologia corrente da questo lavoro.
6. Pubblicare gh-pages con il proprio via al rilascio, verificare il sito vero e solo dopo integrare il ramo server sul main, come da AGENTS.md. Il workflow tifosi aprirà l’ultima votazione disponibile soltanto se la scadenza è futura; chiude quelle scadute anche senza voti umani, senza assegnazioni retroattive.
7. Integrare il main del Registro quando si vuole rendere pubblici la nuova pagina e i contenuti del Lab. Il suo main **pubblica automaticamente**. Dopo quel passaggio lanciare `ramificazioni.yml` una prima volta; i controlli periodici aggiornano anche i cambi della repo del sito. Non è una nuova versione dell’app.

## Verifiche e limiti

Schema provato due volte sullo stesso Postgres 17 locale: autenticazione, tabelle private/RLS, privilegi minimi, voto/cambio/ritiro, normalizzazione, scadenza durante una transazione, chiusura senza allenatori, archivio e lettura dei Derby. Nessun collegamento al DB di produzione.

La prova approvata era già passata su tre motori e sedici profili. La preparazione di rilascio ha una suite dedicata per il modulo applicato insieme ai cambi di Claude e per Ramificazioni. I rapporti e gli esiti finali saranno riportati nel ticket. I test delle richieste Supabase nel browser usano risposte simulate; il protocollo SQL viene verificato nel database locale reale.

Samsung Internet, Safari su dispositivi e Chrome/Edge di marca richiedono prove separate: non sono sostituiti dagli user-agent emulati. Dopo l’applicazione autorizzata dello schema, eseguire anche i controlli/advisors Supabase e le letture effettive delle RPC prima del rilascio; non sono dichiarati eseguiti sul progetto live.
