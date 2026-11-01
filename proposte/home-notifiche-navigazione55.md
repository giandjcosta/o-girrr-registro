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
- PASS GitHub sul codice `8543d6a`: collaudo 5.5 di Claude con Chromium e WebKit,
  [run 41322147988](https://github.com/giandjcosta/o-girrr-registro/actions/runs/41322147988).
  Aggiornati solo i due controlli Home, che ora verificano il componente unico
  e i link delle notifiche; il controllo dei menu aggiunto poi da Claude è conservato.
- **FALLIMENTO distinto e già noto:** Fiducia 5.2 Browser QA,
  [run 41322147931](https://github.com/giandjcosta/o-girrr-registro/actions/runs/41322147931),
  cerca il vecchio indicatore di reputazione e `#riscatta-sponsor` nel Lab e nelle
  vecchie app. Il Lab su cui fallisce non è stato modificato da questa Home.
  Non sono stati ripristinati componenti superati né disattivato il workflow.
- La base del Registro è stata aggiornata durante il lavoro a `adbada2`:
  conservati sfondo pieno/Inter dei menu, controlli e banca personaggi di Claude
  (nuove frasi attive dal 2 novembre). La nuova CI
  sull'ultimo codice va letta nella PR #48. Safari su iPhone fisico e login con
  credenziali reali non verificati.

Screenshot e rapporti: `prove/risultati-home-notifiche55/`.
PR: https://github.com/giandjcosta/o-girrr-registro/pull/48.
Per il rilascio sul sito vanno portati i componenti Home/barra nelle sorgenti
definitive e adattati i link della preview; il build 5.5 non pubblica questi
file nel sito ufficiale. La pubblicazione su `o-fant-a-girrr` resta in attesa
del Via di Gianluca.
