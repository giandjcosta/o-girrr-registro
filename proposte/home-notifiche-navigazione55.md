# ChatGPT: Home, notifiche e riferimenti grafici — 1 novembre 2026

La nuova Home è integrata nelle pagine vere Lega/Stadio della 5.5, al posto
delle tre sottoschede di Oggi al Girrr. I riferimenti di Gianluca guidano la
composizione, conservando colori, caratteri, menu e sezioni della Lega.

| Riferimento | Dove si trova nella 5.5 | Dati e comportamento |
| --- | --- | --- |
| Avvisi immediati | Inizio di Oggi al Girrr e contatore nella barra | Due avvisi apribili e numero totale; il centro notifiche mostra il resto. |
| Forma recente FotMob | Home → Le ultime cinque | Risultato dal punto di vista della squadra, avversario, giornata e link al Tabellone. |
| Mini classifica | Home → Intorno a te | Tre righe intorno alla squadra selezionata, Pt e DR; nessun nome troncato. |
| Prossimi avversari | Home → Le prossime tre sfide | Casa/trasferta e posizione attuale. Non viene inventato un indice di difficoltà. |
| Posizioni stagionali | Home → La storia dei tuoi allenatori | Dati MGR/HIST già conservati nel Lab. Stagioni mancanti interrompono la linea; 2026/27 è provvisoria. |
| Rendimento allenatori | Home → Il rendimento degli allenatori | Percentuale vittorie = V/G; punti a partita = Pt/G, solo campionato corrente. |
| Competizioni Football Manager | Home → Le competizioni | Campionato e Champions Cup reali; link al Tabellone e alla fase della Coppa. |
| Campo tattico | Tabellone → Campo, già integrato | Formazioni registrate per ruolo, conservate con il lavoro di Claude. Nessun editor tattico, possesso o movimento inventato. |
| Logo e scritta distinti | Barra delle sei sezioni 5.5 | Scudo → Home della skin attiva; scritta → pagina precedente. Un link diretto ha come ripiego Home, oppure Tabellone dal Campo. |

L'andamento delle giornate e quello delle stagioni sono due grafici diversi.
Per il secondo, il numero di squadre dei tornei passati è conservato nei dettagli
dei punti; la posizione non viene trasformata in una percentuale. Non vengono
dedotte vittorie o medie dei campionati passati dalle sole posizioni finali.
I due allenatori di The Blue brothers mantengono storie separate e condividono
il bilancio del club nella stagione corrente.

`allenatori.json` è generato da `MGR` e `HIST` del Lab: nessun secondo archivio
aggiornato a mano. `home55.js` costruisce il componente da dati pubblici;
`ui.js` conserva la selezione squadra, collega gli avvisi e gestisce la barra.
Il cambio di skin dalla barra conserva query, giornata, partita e scheda Albo.
Anche il Lab e i vecchi URL `anteprima/home-*.html` aprono la stessa Home 5.5;
le copie storiche delle Home restano nei template. Un test segue entrambi gli
ingressi e verifica il riepilogo nuovo. Corretto così il percorso che visitava
ancora la vecchia Home e il vecchio Albo. La cornice salva l’URL corrente
al ricaricamento anche quando immagini/font non hanno ancora emesso load,
evitando di riaprire la pagina precedente. Le schede dell’Albo hanno area di
tocco di almeno 44 px su telefono/tablet; su desktop restano compatte.

## Notifiche e confini

Le notifiche personali riusano `notifiche_stato` e `notifiche_segna_lette`, già
implementate da Claude. Nessuna modifica a SQL, autorizzazioni o funzioni del
database. Il caricamento legge soltanto; lo stato letto cambia solo al clic
esplicito su Segna lette. Il pulsante aspetta la prima risposta personale.
Un cambio squadra invalida la risposta precedente e non invia le credenziali
dell'allenatore alla squadra selezionata. I link a prestiti, movimenti e sfide
restano nelle pagine di prova. Il codice d'ingresso non finisce nelle URL.

Preservata anche la modalità ospite di Claude (`29d0e0b`): nelle due skin
a 390/1440 px, anche con credenziali salvate, Home e centro notifiche non
invocano RPC personali. Il cambio pagina mantiene la modalità ospite.

Le RPC sono state **simulate nei test**, con risposte coerenti al contratto
esistente. Nessuna chiamata di scrittura reale, post o audio durante il lavoro.
Non si dichiarano push o nuove automazioni backend.

Per il logo è mantenuto lo scudo O Girrr già presente. È stato chiesto se
Gianluca intende invece uno stemma della squadra selezionata: tali immagini
non risultano nei dati delle squadre esaminati e non sono state inventate.

## Verifiche e limiti

- PASS locale: Home nelle due skin a 320/390/768/1280/1440; avviso → Tabellone,
  scritta → pagina precedente, Campo → logo → Home. Numeri dei grafici e delle
  tabelle confrontati con il calendario; squadra cambiata, RPC rifiutata e
  marcatura letture solo su clic. Nessun overflow, errore JS o 404 nei percorsi.
- PASS locale: percorso completo con Tabellone/Coppa/Campo/Albo/Curva/Notifiche,
  le dieci combinazioni; Campo con 22 e con 10 + 11 giocatori, tastiera e Curva
  chiara/scura. Build riproducibile, collaudi statici/milestone/fiducia/Annuario
  e preparazione rilascio cronache.
- PASS GitHub sul codice `0ff2caf`: [integrazione completa, cronache e PDF](https://github.com/giandjcosta/o-girrr-registro/actions/runs/41324996777) e [collaudo Claude Chromium + WebKit](https://github.com/giandjcosta/o-girrr-registro/actions/runs/41324992391), oltre a QA Anteprima 5.2, milestone Totogirrr e Fiducia universale. Il commit successivo aggiorna solo documentazione e rapporti.
- **FALLIMENTO distinto e già noto:** [Fiducia 5.2 Browser QA](https://github.com/giandjcosta/o-girrr-registro/actions/runs/41324992405), indicatore di reputazione e `#riscatta-sponsor` mancanti nel Lab e nelle vecchie app. Verificati i log dell’ultima esecuzione: sono gli stessi errori, non una regressione della Home. Nessun workflow disattivato.
- Incorporate le modifiche concorrenti di Claude fino a `29d0e0b`: menu, banca personaggi, ospite e interazioni della Curva. Safari su iPhone fisico e accesso con credenziali reali non verificati.
- Verifica remota raw.githack non completata: HTTP 403 dal runtime. Per la consegna si usano i link GitHub Pages del Registro.

Screenshot e rapporti: `prove/risultati-home-notifiche55/`.
PR: https://github.com/giandjcosta/o-girrr-registro/pull/48.
Per il rilascio sul sito vanno portati i componenti Home/barra nelle sorgenti
definitive e adattati i link della preview; il build 5.5 non pubblica questi
file nel sito ufficiale. La pubblicazione su `o-fant-a-girrr` resta in attesa
del Via di Gianluca.

## Aggiunta richiesta da Gianluca: tendina e propria squadra

Oggi al Girrr è un unico pannello richiudibile; le notifiche restano fuori
dalla tendina. Da chiuso resta un riepilogo con nome, posizione e punti.
Il browser ricorda la scelta, condivisa fra Lega e Stadio.

Il Registro conserva il selettore di tutte le squadre per la prova, etichettato
«Squadra in prova». Sul percorso del sito reale il selettore offre solo la
squadra d’accesso, ignorando il club selezionato prima nella prova. Senza
accesso il riepilogo personale invita a entrare e non sceglie un club al posto
dell’utente. `?riepilogo=personale` simula questo comportamento nel Registro.
La distinzione dipende dalla pagina visitata, non dall'URL del JavaScript.
La modalità personale ignora qualunque tentativo di cambiare il selettore.

La logica è provata su percorsi locali che rappresentano il futuro sito:
nessun file o database di produzione è stato cambiato. Le autorizzazioni
delle notifiche rimangono nelle RPC già esistenti; calendario e classifica
sono informazioni pubbliche della Lega.

La nuova tendina e la modalità personale sono nella [PR #49](https://github.com/giandjcosta/o-girrr-registro/pull/49). Sul codice `2b41ddf`: [suite completa PASS](https://github.com/giandjcosta/o-girrr-registro/actions/runs/41326855787), [Chromium e WebKit PASS](https://github.com/giandjcosta/o-girrr-registro/actions/runs/41326818415). Anche le tre QA statiche PASS; [Fiducia 5.2 Browser QA resta rosso](https://github.com/giandjcosta/o-girrr-registro/actions/runs/41326818416) per i problemi precedenti. La modalità personale nella Home vera del Registro è stata verificata nelle due skin con credenziali simulate, una scelta precedente diversa e ricarica della tendina chiusa. Nessuna scrittura reale.
