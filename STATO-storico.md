# O Girrr — cronologia del progetto

Riepilogo dei cambiamenti principali ricostruito dalla cronologia Git dei repository `o-fant-a-girrr` e `o-girrr-registro`, dal Registro automatico e dalle note di progetto. Lo [STATO.md](./STATO.md) resta l'overview operativo: contiene lo stato recente, le prove in corso e le decisioni aperte.

## Copertura e fonti

- La cronologia Git disponibile per il sito comincia il **7 ottobre 2026** (`o-fant-a-girrr`, commit iniziale `0811813`); quella del Registro comincia il **13 ottobre 2026** (`o-girrr-registro`, commit iniziale `93a1e96`). Nei repository e nelle note consultati non ho trovato commit che documentino attività di settembre. Se il lavoro era già iniziato a fine settembre, quei passaggi non sono ricostruibili da questa cronologia e andranno integrati da eventuali archivi o copie precedenti.
- Il [Registro / Changelog](https://giandjcosta.github.io/o-girrr-registro/) mostra le modifiche pubbliche del repository del sito, giorno per giorno. La pagina [Aggiornamenti](https://giandjcosta.github.io/o-girrr-registro/aggiornamenti.html) è invece dedicata alle esecuzioni automatiche e ai dati aggiornati.
- Questo documento raggruppa le modifiche per tappe e non ripete ogni commit automatico di voti, statistiche, risultati e riepiloghi. Per le note operative più dettagliate fino al 25 ottobre resta consultabile anche la [copia storica dello STATO al commit 940d2d3](https://github.com/giandjcosta/o-girrr-registro/blob/940d2d374df403507576bed7c47283b010c56f00/STATO.md).
- Le etichette **ONLINE**, **IN PROVA** e **DECISO** distinguono rispettivamente ciò che è stato pubblicato, ciò che è rimasto nel Laboratorio/Anteprima e le decisioni ancora da implementare. Un commit nel Registro non implica da solo che la modifica sia sul sito vero.

## 7–12 ottobre · Nascita del sito e prime sezioni

- **7 ottobre — avvio del repository del sito.** Prima versione della Home e dei dati della Lega; si aggiungono la scheda Lega con classifica e risultati e il riepilogo della giornata, anche in una pagina condivisibile.
- **8–12 ottobre — Spogliatoio.** Crescono le viste della rosa, le statistiche delle squadre e dei giocatori, il calendario di Classic League e Champions Cup, le probabili formazioni e i suggerimenti di mercato. Si lavora su leggibilità, stili grafici, moduli, selezione delle partite e resa su telefono; vengono aggiunti dati storici e informazioni sugli infortuni.
- **Giornale e stagione.** Si aggiungono pagelle, risultati e collegamenti ai numeri del Giornale; i premi dipendono dai gol e i pareggi non hanno un vincitore.
- **Curva.** Il feed si popola con i cori delle squadre, i profili ufficiali della Lega e della coppa, Girrr Sport e Ciro Trattativa. Arrivano commenti, reazioni, seguiti, notifiche, condivisione e schede con risultati, mercato e contenuti delle squadre. Si introducono personalità e frequenze diverse per i personaggi, senza duplicare le risposte.
- **Albo d'oro.** Si crea lo storico delle stagioni disponibili e si arricchiscono le schede degli allenatori con nomi precedenti, percorsi, storie, ambizioni e scontri diretti.

## 13–16 ottobre · Automazioni, contenuti e Registro

- **13 ottobre — avvio del Registro.** Nasce la repository `o-girrr-registro` come archivio delle modifiche, laboratorio delle novità e punto di preparazione dell'Anteprima. Il sito e il Registro restano repository distinti.
- Si consolida la pubblicazione automatica di risultati, statistiche, quote e riepiloghi. Il Totogirrr aggiorna le quote e considera rose, infortuni e squalifiche; sono aggiunte le previsioni sulle formazioni.
- La Curva acquisisce più profili e contenuti: Girrr Sport rilancia notizie e cori, Ciro tratta il mercato, le squadre si seguono e interagiscono, i commenti e le notifiche diventano persistenti. Vengono aggiunti il profilo Totogirrr e i primi contenuti della Champions Cup.
- **13–15 ottobre — Giornale e Albo.** Il Giornale riceve pagelle con panchina e rimpianti; le storie degli allenatori diventano più narrative e vengono corrette con i dati storici disponibili.
- **14–15 ottobre — Totogirrr e mercato.** Sono affinate le card delle partite in evidenza, la distinzione fra competizioni e la considerazione degli infortuni. In Curva vengono pubblicate rubriche come FC27 Ratings e notizie di mercato; la condivisione e la barra mobile sono corrette per iOS.
- **16 ottobre — Laboratorio e grafica.** Il Laboratorio diventa la destinazione per provare nuove idee prima del sito vero. Lo Spogliatoio aggiunge lo stile O Girrr, memorizza la scelta grafica e migliora la leggibilità della rosa. Partono anche le prove delle voci e dei copioni della Radio Girrr.

## 17–18 ottobre · Anteprima 5.0 e funzioni di Lega

- **17 ottobre — preparazione della 5.0.** Si definiscono e si provano il selettore Lega/Stadio, le nuove schede, le transizioni, le etichette e l'impaginazione. Le Ere dell'Albo diventano apribili; Stagioni, Derby e Rivalità ricevono pannelli e contenuti dedicati.
- Le Sfide della Lega distinguono le rivalità/Derby dalle sfide 1 contro 1 del Totogirrr. Si aggiungono proposta e accettazione, scadenza, nome del Derby concordato e frasi basate sui dati. Nel Totogirrr arrivano le schede Probabilità e Sfida 1 contro 1.
- Si introducono Carriera con fasce e sponsor, Albo di Latta, storie degli allenatori dal 2016/17 e ulteriori contenuti della Radio.
- **18 ottobre — rilascio 5.0 sul sito.** Vanno online Girrr Sport, Spogliatoio, Totogirrr e Carriera, insieme a Derby, Sfide e modifiche all'Albo. Le schede del Totogirrr smettono di ridisegnare testata e schedina quando non serve; il cambio scheda non provoca più il flash bianco. Il selettore Lega/Stadio riceve una transizione.
- Si collegano le Sfide e i dati al database; partono i calcoli dopo la giornata e il workflow della Curva. Le frasi inserite quando si lancia una sfida vengono conservate per i post; si aggiungono le Conferenze pre-partita. Lo sfondo fisso viene spostato su un livello separato per evitare differenze tra pagine lunghe e corte, in particolare su Safari.

## 19–22 ottobre · Dati, importazione e affidabilità

- Si importa la giornata 3 e si aggiorna il Giornale. L'importazione legge il modificatore difesa per entrambe le squadre e attende il cambio di pagina invece di affidarsi a un ritardo fisso.
- Si aggiungono controlli giornalieri che segnalano workflow falliti, aggiornamenti fermi o giornate concluse ma non importate.
- La Radio viene aggiornata con dati reali; i file di prova non vengono lasciati nei contenuti ufficiali.
- Il Borsino viene aggiunto allo Spogliatoio. Vengono corretti i dati o le etichette dei Derby secondo le decisioni del progetto.
- La Curva passa a post più tempestivi e si perfezionano dati, collegamenti e comportamento delle pagine.

## 23–24 ottobre · Moviola, correzioni e racconto

- **Moviola, prima nel Lab.** Si introduce una scheda per gli episodi di giornata con priorità, verdetti e testi riproducibili. La logica viene poi spostata in `calcoli/moviola.py` con un unico file `moviola.json`; gli episodi già scritti restano stabili, gli episodi non ricostruibili vengono segnalati e non confusi con una giornata senza episodi.
- Si aggiungono episodi manuali e video; in seguito gol, assist e cambi decisivi. Il numero di episodi è limitato e i test coprono giornate complete, dati mancanti e casi di prova.
- **24 ottobre — Moviola online.** La Moviola entra in Girrr Sport e nei post della Curva. Il rilascio riguarda sia Lega sia Stadio; i workflow salvano e aggiornano i dati necessari.
- La Home mostra lo stato di caricamento, un errore con possibilità di riprovare e la data dei dati. È corretto il percorso dell'archivio Radio nella Curva dello Stadio, che prima causava un 404.
- La card dell'allenatore viene aggiunta alle pagine delle squadre. Il selettore Lega/Stadio viene reso nitido; lo sfondo e le strisce diagonali sono corretti per mantenere l'identità di entrambe le grafiche.
- Si scrive la storia del Derby dell'Emma e si corregge la stagione del primo titolo di apo nel Derby con DJ Cst Brazil.
- Inizia la bozza della storia della Lega: collocazione nell'Albo, Padri Fondatori, origini del nome e distinzione tra la scheda della Storia e le tre Ere.

## 25 ottobre · Anteprima 5.1 e aggiornamenti successivi

- **Totogirrr a 320 px.** Si correggono le etichette che causavano lo scorrimento orizzontale e si verifica il comportamento delle schede su schermi stretti.
- **5.1 online (`gh-pages` `eb886da`).** L'Albo riceve la scheda La Storia; le Ere hanno titoli con punto mediano; Derby e sfide di classifica sono riportati in Tabellone e Totogirrr. Un errore per cui un'etichetta sovrascriveva i punteggi del Tabellone viene individuato e corretto prima del rilascio.
- **Storia e descrizioni delle Ere.** La bozza mantiene il racconto esistente, i titoli e le date, aggiungendo testi brevi. Viene ripristinata l'apertura fluida delle card. Le diverse formulazioni restano nella preview finché non vengono approvate.
- **Soglia Derby.** In prova, la soglia per riconoscere un Derby senza sfida accettata viene portata a 80 e le etichette di classifica vengono provate sul Tabellone e sul Totogirrr; gli interventi non pubblicati restano distinti dal rilascio 5.1.
- **2019/20 e 2020/21.** Le due righe «Non assegnato» vengono spostate dall'Era dei Titani al Grande Silenzio. Online su Lega e Stadio con `gh-pages` `2815139`.
- **Carriera — solo Lab/Anteprima.** Gli obiettivi legati a una giornata di scadenza non risultano più completati in anticipo: sono valutati alla giornata indicata; gli obiettivi cumulativi restano aggiornati al raggiungimento.
- Si definiscono come intenzioni, non come funzioni pubblicate, la separazione tra aree pubbliche e private, un login unico, caricamento differito dello Spogliatoio, colori coerenti tra Lega e Stadio e caricamento progressivo della Curva. Il codice del sito vero non va considerato aggiornato finché non compare un rilascio verificato.

## Procedura di prova e pubblicazione (dal 25 ottobre 2026)

- Da questa data le novità destinate al sito devono essere mostrate e provate prima nel [Laboratorio](https://giandjcosta.github.io/o-girrr-registro/lab/). Il link a un branch Git o a un file isolato non sostituisce la preview navigabile in `/lab`.
- La preview serve a raccogliere la certificazione di Gianluca. Prima del suo «Vai» non si porta la novità nel sito vero; dopo il via si rilascia sui rami del sito appropriati e si registra il commit qui e nello STATO corrente.
- Fanno eccezione i documenti di progetto e gli strumenti che non modificano il comportamento del sito: possono essere aggiornati direttamente nel Registro, senza un prototipo grafico.

## Registro e aggiornamento futuro

Il Registro automatico è la changelog puntuale dei commit pubblici. Questo file ne è la lettura storica raggruppata per tema: aggiungere una nuova tappa quando una funzione o un rilascio significativo cambia lo stato del progetto, lasciando a `STATO.md` l'overview operativo e le attività aperte.
