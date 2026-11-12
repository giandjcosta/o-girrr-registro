# Miglioramenti e novità discussi con Gianluca · 12 novembre 2026

Questo elenco conserva la discussione. Il «vai» attuale riguarda premi, allineamento e collaudi; le nuove funzionalità qui sotto restano proposte.

## Manutenzione autorizzata

- Allineare Anteprima, Changelog e Archivio ai rilasci e mantenerli aggiornati automaticamente. È manutenzione della repo di prova: nessuna nuova versione o annuncio dell'app.
- Correggere il workflow premi senza allargare i permessi del database. I permessi service_role sono già corretti; va diagnosticata la chiave GitHub.
- Incrociare Chromium, WebKit e Firefox con 16 profili di schermo. Samsung Internet, Safari su iPhone e browser di marca richiedono verifiche separate su browser effettivi: non contare il solo user-agent come una prova.
- Migliorare gradualmente le parti comuni Lega/Stadio e il caricamento delle sezioni grandi, mantenendo diverse le grafiche. Nessuna riscrittura generale mentre Claude lavora sulla Curva.
- Valutare le vecchie PR per distinguere lavoro già integrato e lavoro residuo. Non unire alla cieca né cancellare rami.

## Proposte da scegliere

1. **La settimana della tua squadra.** Un resoconto breve della redazione con risultato, movimento in classifica, promesse e prossimo avversario. Prima controllare il lavoro di Claude sulla redazione per evitare duplicazioni.
2. **Classifica dei Derby.** Bilancio degli scontri fra rivali e Re dei Derby della stagione, usando soltanto risultati conservati. Dove manca il dato: «Dato non conservato».
3. **Simulatore della prossima giornata.** Scegliere risultati ipotetici e vedere come cambierebbe la classifica. Applicare gli spareggi effettivamente documentati; nessuna scrittura sui risultati ufficiali.
4. **MVP dei tifosi.** Sondaggio con candidati scelti dai dati, con collegamento al Giornale e all'Annuario. Valutare insieme ai sondaggi già esistenti.
5. **Promemoria del mercato scambi.** Avvisi su apertura e chiusura delle finestre, se le date sono disponibili e confermate.
6. **Accessibilità e caricamento.** Etichette e tastiera, contrasto, VoiceOver/TalkBack su dispositivi disponibili, rispetto di «Riduci movimento», caricamenti che mantengano visibile il contenuto già letto.

## Correzioni alla prima proposta di ChatGPT

- **Centro partita:** già presente nel Tabellone; non proporre un'altra pagina uguale. Eventuali collegamenti mancanti si migliorano lì.
- **Video della giornata:** lo sta facendo Claude; non aprire un secondo lavoro sullo stesso tema.
- **Notifica della formazione non consegnata:** non implementabile in modo attendibile con i dati attuali. Leghe non fornisce l'API necessaria e l'assenza di una formazione importata non prova la mancata consegna. Distinta dai promemoria generici prima della scadenza già presenti.
- **Data degli aggiornamenti:** la Home mostra già la data dei dati e il Borsino la propria data. Valutare soltanto informazioni mancanti vicino a Probabili formazioni e Infortunati nello Spogliatoio, usando orari reali della fonte/importazione, mai l'ora di apertura della pagina. Nessuna modifica approvata a queste etichette.
- **Calendario esterno e Radio offline:** già rinviati da Gianluca; non riproporli come priorità.
- **Live, inglese completo e servizio per più leghe:** restano prospettive successive, con fonti, costi e manutenzione da valutare prima.
