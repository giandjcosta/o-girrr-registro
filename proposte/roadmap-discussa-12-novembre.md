# Miglioramenti e novità discussi con Gianluca · 12 novembre 2026

Questo elenco conserva la discussione. Il «vai» attuale riguarda premi, allineamento e collaudi; le nuove funzionalità qui sotto restano proposte.

## Manutenzione autorizzata

- Allineare Anteprima, Changelog e Archivio ai rilasci e mantenerli aggiornati automaticamente. È manutenzione della repo di prova: nessuna nuova versione o annuncio dell'app.
- Correggere il workflow premi senza allargare i permessi del database. I permessi service_role sono già corretti; va diagnosticata la chiave GitHub.
- Incrociare Chromium, WebKit e Firefox con 16 profili di schermo. Samsung Internet, Safari su iPhone e browser di marca richiedono verifiche separate su browser effettivi: non contare il solo user-agent come una prova.
- Migliorare gradualmente le parti comuni Lega/Stadio e il caricamento delle sezioni grandi, mantenendo diverse le grafiche. Nessuna riscrittura generale mentre Claude lavora sulla Curva.
- Valutare le vecchie PR per distinguere lavoro già integrato e lavoro residuo. Non unire alla cieca né cancellare rami.

## Decisioni e proposte da definire

1. **La settimana della tua squadra.** Un resoconto breve della redazione con risultato, movimento in classifica, promesse e prossimo avversario. Prima controllare il lavoro di Claude sulla redazione per evitare duplicazioni.
2. **Classifica dei Derby — idea accolta da Gianluca.** Bilancio dei soli Derby riconosciuti, con Re dei Derby della stagione, usando risultati conservati. Dove manca il dato: «Dato non conservato». Proposta di collocazione: riquadro espandibile nella pagina Derby esistente, insieme a Testa a testa. Mostrare sempre le gare disputate, oltre a vittorie/pareggi/sconfitte e punti. Da preparare nel Lab; nessuna autorizzazione al rilascio.
3. **Simulatore della prossima giornata — escluso da Gianluca.** Non svilupparlo né riproporlo come lavoro scelto.
4. **Squadra MVP dei tifosi — richiesta di Gianluca da definire.** «Potremmo metter la squadra MVP dei tifosi votata dai bot e dalla redazione, così ogni settimana vediamo chi sia il migliore. Possiamo votarla anche noi ma non è obbligatorio». Personaggi e redazione partecipano ogni giornata; voto degli allenatori facoltativo e distinto dai voti dei personaggi. Proposta di collocazione: Curva → Sondaggi, avviso compatto in Oggi al Girrr, risultato nel Giornale e storico nell'Annuario. Questa collocazione è una proposta di ChatGPT, non ancora una decisione di Gianluca. Nell'esempio discusso si interpreta MVP come club della giornata; l'alternativa dell'undici ideale e i pesi dei voti restano da chiarire. Nessuna votazione o pubblicazione già implementata.
5. **Promemoria del mercato scambi.** Avvisi su apertura e chiusura delle finestre, se le date sono disponibili e confermate.
6. **Accessibilità e caricamento.** Etichette e tastiera, contrasto, VoiceOver/TalkBack su dispositivi disponibili, rispetto di «Riduci movimento», caricamenti che mantengano visibile il contenuto già letto.

## Correzioni alla prima proposta di ChatGPT

- **Centro partita:** già presente nel Tabellone; non proporre un'altra pagina uguale. Eventuali collegamenti mancanti si migliorano lì.
- **Video della giornata:** lo sta facendo Claude; non aprire un secondo lavoro sullo stesso tema.
- **Notifica della formazione non consegnata:** non implementabile in modo attendibile con i dati attuali. Leghe non fornisce l'API necessaria e l'assenza di una formazione importata non prova la mancata consegna. Distinta dai promemoria generici prima della scadenza già presenti.
- **Data degli aggiornamenti:** la Home mostra già la data dei dati e il Borsino la propria data. Valutare soltanto informazioni mancanti vicino a Probabili formazioni e Infortunati nello Spogliatoio, usando orari reali della fonte/importazione, mai l'ora di apertura della pagina. Nessuna modifica approvata a queste etichette.
- **Calendario esterno e Radio offline:** già rinviati da Gianluca; non riproporli come priorità.
- **Live, inglese completo e servizio per più leghe:** restano prospettive successive, con fonti, costi e manutenzione da valutare prima.

## Verifica del lavoro precedente e racconto personale

- Le grafiche 5.5 sono già state completate da Claude e pubblicate con la 5.5: vedere STATO, «1 novembre (notte) — grafiche Lega/Stadio». Valgono le correzioni successive di Gianluca: pillole Lega tonde; più oro nello Stadio; Campionato rosso e Champions Cup azzurra. La copia corrente del Registro indica la versione 5.8.1. Non ripartire dalle vecchie regole della bozza ChatGPT.
- «La mia stagione», Testa a testa e domande personalizzate della redazione sono già presenti. Il nuovo racconto settimanale va integrato con la redazione 5.8, senza un secondo generatore concorrente. La richiesta attuale è di mostrarne un esempio, non di pubblicarlo.
- Esempio tratto dal dossier della 7ª giornata, squadra Oranje VC (11 punti, quinta, pareggio con Apo team e vittoria 2-1 sulla WOA; successiva in trasferta contro la capolista Mariana Coneja):

> **Oranje VC, quattro punti per ritrovare il passo**
>
> Dopo il pareggio con l’Apo, l’Oranje ritrova la vittoria: 2-1 alla WOA, 11 punti e quinto posto. Quattro punti nelle ultime due giornate riportano nel mirino le prime quattro, l’obiettivo fissato dalla dirigenza. Il calendario però non concede tregua: ora c’è la trasferta contro la capolista Mariana Coneja. DJ Cst Brazil sceglie la prudenza: «Una partita alla volta, con umiltà». L’umiltà è dichiarata. Adesso servono anche i punti.
