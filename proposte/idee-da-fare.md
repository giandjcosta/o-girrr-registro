# Idee per O Girrr — proposte e non ancora fatte

Elenco da consultare, aggiornato da chi propone o realizza un'idea. Quando un'idea si fa, si sposta in fondo in «Fatte» con la data e il riferimento in `STATO.md`.
Nessuna di queste è approvata: ognuna aspetta il «vai» di Gianluca (e, se tocca il database, un «vai» apposta).

## In attesa

### Notifiche push (Gianluca: «crea pure», 9 novembre 2026) — in prova nel Lab
Fatte nel Lab (`lab/offline/`), aspettano la conferma della migrazione su Supabase e poi la prova sul telefono. Dettagli in `STATO.md`.

### Scarica la Radio per il treno (Claude, 9 novembre 2026; Gianluca: «per ora no»)
Un pulsante «Scarica per ascoltare offline» accanto alla puntata: salva l'mp3 (circa 1,4 MB) nella copia offline.

### Calendario delle giornate in Google Calendar (Claude, 9 novembre 2026; Gianluca: «per ora no»)
Un file `.ics` scritto dai workflow con le giornate e l'orario di consegna della formazione: si aggiunge una volta a Google Calendar (o al calendario dell'iPhone) e si aggiorna da solo, con il promemoria.

### Conto alla rovescia della formazione (Gianluca: sì, come notifica 3 ore e 1 ora prima)
Dentro le notifiche push. Resta da fare, se si vuole, il conto alla rovescia scritto anche nella Home.

### Condividi come immagine (Gianluca: «ok, puoi crearlo») — in prova nel Lab
Fatto nel Lab: `rilascio/condividi/condividi.js`. Tabellone → «Condividi»: La mia partita, Risultati della giornata, Classifica; Giornale → «Condividi l'ultimo numero». Dettagli in `STATO.md`.

### Cerca un giocatore (Gianluca: «una scheda a sé nello Spogliatoio») — in prova nel Lab
Scheda «Cerca» dopo «Rosa». Dettagli in `STATO.md`.

### La mia stagione (Gianluca: «meglio in Spogliatoio, Albo o Carriera?»)
- **Proposta di Claude: nella Carriera**, come nuova scheda «Stagione» accanto a Panoramica, Obiettivi, Fiducia, Storia e Regole. È il posto della tua storia da allenatore (si entra con il codice, ci sono già fiducia, obiettivi e posizioni giornata per giornata). Lo Spogliatoio resta per gestire la rosa; l'Albo d'oro è la storia di tutti.
- A fine stagione il riepilogo resta anche nell'**Albo d'oro**, nell'Annuario della stagione, per ogni squadra.
- **Come:** schede a tutto schermo da scorrere col dito: posizione e punti (e la migliore posizione raggiunta), vittorie, pareggi e sconfitte, la striscia più lunga, la miglior giornata (fantapunti, livello tecnico), il giocatore che ha portato più fantapunti, il colpo di mercato (Borsino), Derby, Champions Cup; ultima scheda da condividere come immagine.
- Solo dati veri; dove mancano «Dato non conservato».

### Risultati provvisori durante la giornata (Gianluca: «si potrebbe usare Fantacalcio, ma non ho un'API della loro app»)
- Fantacalcio/Leghe non ha un'API pubblica. Le strade possibili, tutte da verificare prima: (1) leggere Leghe dal browser con l'accesso di Gianluca, come già si fa per importare le giornate: funziona solo con il PC acceso e collegato, troppo fragile per il «live»; (2) un servizio di dati live di Serie A (gol, assist, cartellini, minuti), da scegliere guardando costi e condizioni d'uso.
- Anche con la fonte, durante le partite non ci sono i voti: si mostrerebbero solo i fatti certi dei giocatori schierati, senza inventare un punteggio. Il risultato vero resta quello di Leghe.

### Altre idee (Claude, 9 novembre 2026)
- **Testa a testa:** scegli due squadre e vedi i loro scontri della stagione (Campionato e Champions Cup), la classifica a confronto e, se è un Derby, la sua storia. Per le stagioni passate dove manca il dato: «Dato non conservato».
- **MVP dei tifosi:** dopo ogni giornata un sondaggio in Curva con tre candidati scelti dai dati (migliori voti della giornata); il vincitore finisce nel Giornale e nell'Annuario.
- **Promemoria del mercato scambi:** quando si apre e si chiude una finestra di mercato, avviso in Home e notifica sul telefono, con il conto alla rovescia.
- **Testo più grande:** un interruttore in Info per ingrandire i caratteri su tutte le pagine (utile su TV e per chi legge da lontano).

## Fatte
- **Copia offline** (online il 9 novembre 2026, `gh-pages` `e06cbe2`), vedi `STATO.md`.
- **Scorciatoie dell'icona nella grafica scelta** (online il 9 novembre 2026, `gh-pages` `e06cbe2`): Tabellone, Curva, Giornale, Totogirrr. Non su iPhone.
