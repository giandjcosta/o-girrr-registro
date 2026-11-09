# Idee per O Girrr — proposte e non ancora fatte

Elenco da consultare, aggiornato da chi propone o realizza un'idea. Quando un'idea si fa, si sposta in fondo in «Fatte» con la data e il riferimento in `STATO.md`.
Nessuna di queste è approvata: ognuna aspetta il «vai» di Gianluca (e, se tocca il database, un «vai» apposta).

## In attesa

### Scarica la Radio per il treno (Claude, 9 novembre 2026; Gianluca: «per ora no»)
Un pulsante «Scarica per ascoltare offline» accanto alla puntata: salva l'mp3 (circa 1,4 MB) nella copia offline.

### Calendario delle giornate in Google Calendar (Claude, 9 novembre 2026; Gianluca: «per ora no»)
Un file `.ics` scritto dai workflow con le giornate e l'orario di consegna della formazione: si aggiunge una volta a Google Calendar (o al calendario dell'iPhone) e si aggiorna da solo, con il promemoria.

### Conto alla rovescia della formazione scritto in Home
La notifica 3 ore e 1 ora prima è online con la 5.6. Resta da fare, se si vuole, il conto alla rovescia scritto anche nella Home.

### Risultati provvisori durante la giornata (Gianluca: «si potrebbe usare Fantacalcio, ma non ho un'API della loro app»)
- Fantacalcio/Leghe non ha un'API pubblica. Le strade possibili, tutte da verificare prima: (1) leggere Leghe dal browser con l'accesso di Gianluca, come già si fa per importare le giornate: funziona solo con il PC acceso e collegato, troppo fragile per il «live»; (2) un servizio di dati live di Serie A (gol, assist, cartellini, minuti), da scegliere guardando costi e condizioni d'uso.
- Anche con la fonte, durante le partite non ci sono i voti: si mostrerebbero solo i fatti certi dei giocatori schierati, senza inventare un punteggio. Il risultato vero resta quello di Leghe.

### Versione in inglese (Gianluca, 9 novembre 2026: «per potenziali interessati, ma nessuno la chiede ora») — in attesa
- **Non è una 5.6.1:** sarebbe almeno un aggiornamento medio (5.7).
- **Interfaccia** (menu, pulsanti, titoli, schede, legende, avvisi, notifiche): migliaia di frasi in più di 15 pagine, ognuna doppia (Lega e Stadio); Carriera, Curva e Spogliatoio sono file molto grandi. Servono un interruttore IT/EN e un dizionario: diverse sessioni di lavoro e molte prove.
- **Contenuti scritti ogni giornata** (Giornale, Radio, Curva e personaggi, cronache, Moviola, storie dell'Albo): tradurli vuol dire cambiare i workflow e generare ogni testo due volte, con lavoro e costi in più ogni settimana.
- **Restano uguali:** nomi di squadre, giocatori e allenatori, numeri e risultati.
- **Proposta:** a fasi. Prima l'interfaccia con l'interruttore IT/EN (Giornale, Radio e Curva restano in italiano); i contenuti dopo, solo se servono.

### Altre idee (Claude, 9 novembre 2026)
- **Testa a testa:** scegli due squadre e vedi i loro scontri della stagione (Campionato e Champions Cup), la classifica a confronto e, se è un Derby, la sua storia. Per le stagioni passate dove manca il dato: «Dato non conservato».
- **MVP dei tifosi:** dopo ogni giornata un sondaggio in Curva con tre candidati scelti dai dati (migliori voti della giornata); il vincitore finisce nel Giornale e nell'Annuario.
- **Promemoria del mercato scambi:** quando si apre e si chiude una finestra di mercato, avviso in Home e notifica sul telefono, con il conto alla rovescia.
- **Testo più grande:** un interruttore in Info per ingrandire i caratteri su tutte le pagine (utile su TV e per chi legge da lontano).

## Fatte
- **Copia offline** (online il 9 novembre 2026, `gh-pages` `e06cbe2`), vedi `STATO.md`.
- **Scorciatoie dell'icona nella grafica scelta** (online il 9 novembre 2026, `gh-pages` `e06cbe2`): Tabellone, Curva, Giornale, Totogirrr. Non su iPhone.
- **5.6** (online il 9 novembre 2026, `gh-pages` `caa13c6`): notifiche sul telefono (con la formazione 3 ore e 1 ora prima), Cerca un giocatore (scheda dello Spogliatoio), Condividi come immagine, La mia stagione (Carriera), pagina Versioni.
