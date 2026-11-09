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

### Condividi come immagine (Gianluca chiede dove e cosa sarebbe)
- **Dove:** un pulsante «Condividi» (icona di condivisione del telefono) in tre punti: sotto la tua partita nel Tabellone, sulla classifica, sulla copertina del Giornale.
- **Cosa:** un'immagine verticale pronta per WhatsApp, con la grafica scelta (Lega o Stadio): stemmi, risultato, marcatori e giornata («Mariana Coneja–Apo team 3-2 · 7ª giornata»); per la classifica le prime posizioni con la tua squadra evidenziata; per il Giornale la copertina. Si apre il menu del telefono e scegli il gruppo. Solo dati del livello sportivo, niente fantapunti.
- **Come:** l'immagine si disegna nel telefono (canvas) e si passa alla condivisione del sistema (Web Share, iPhone e Android); su PC si scarica.

### Cerca un giocatore (Gianluca: «sempre nello Spogliatoio») — in prova nel Lab
Fatto nel Lab (`lab/offline/` → Spogliatoio). Dettagli in `STATO.md`.

### La mia stagione (Gianluca chiede dove e come sarebbe)
- **Dove:** nello Spogliatoio, una scheda «La mia stagione» accanto a Statistiche; in più un riquadro in Home che compare a fine girone d'andata e a fine stagione («È pronta la tua stagione»).
- **Come:** schede a tutto schermo da scorrere col dito, una alla volta, con la grafica scelta: posizione e punti in classifica (e la migliore posizione raggiunta), vittorie, pareggi e sconfitte, la striscia più lunga, la miglior giornata (fantapunti, livello tecnico), il giocatore che ha portato più fantapunti, il colpo di mercato (Borsino), Derby vinti e persi, Champions Cup. Ultima scheda riassuntiva da condividere come immagine.
- Solo dati veri; dove mancano «Dato non conservato».

### Risultati provvisori durante la giornata (Gianluca: «difficilissimo seguire tutto mentre si gioca»)
- I voti ufficiali arrivano a fine partita (sera o giorno dopo); durante le partite esistono solo i dati «live» (gol, assist, cartellini, minuti), che però sono le parti che decidono i bonus e malus.
- Un «in diretta» onesto: durante le partite di Serie A, per ogni sfida del Girrr solo i **fatti certi dei giocatori schierati** (gol, assist, rigori, cartellini, chi è in campo), senza inventare voti né un punteggio provvisorio. Il risultato vero resta quello di Leghe a fine giornata. Si aggiorna ogni pochi minuti.
- Il problema è la fonte: serve un servizio con i dati live di Serie A affidabile e consultabile (spesso a pagamento o senza permesso di uso), e le formazioni schierate su Leghe prima della chiusura. Prima di farlo bisogna trovare la fonte; senza, niente.

## Fatte
- **Copia offline** (online il 9 novembre 2026, `gh-pages` `e06cbe2`), vedi `STATO.md`.
- **Scorciatoie dell'icona nella grafica scelta** (online il 9 novembre 2026, `gh-pages` `e06cbe2`): Tabellone, Curva, Giornale, Totogirrr. Non su iPhone.
