# Idee per O Girrr — proposte e non ancora fatte

Elenco da consultare, aggiornato da chi propone o realizza un'idea. Quando un'idea si fa, si sposta in fondo in «Fatte» con la data e il riferimento in `STATO.md`.
Nessuna di queste è approvata: ognuna aspetta il «vai» di Gianluca (e, se tocca il database, un «vai» apposta).

## In attesa

### Notifiche push vere (proposta da Claude, 9 novembre 2026, da decidere)
Le notifiche arrivano sul telefono anche con O Girrr chiuso, come quelle di WhatsApp.
- **Come funzionerebbe:** nella pagina Notifiche un pulsante «Avvisami sul telefono». Il telefono chiede il permesso; se dici sì, crea un «indirizzo» di consegna solo suo, che si salva su Supabase insieme alla squadra. Quando succede qualcosa (Giornale uscito, risultati della giornata, risposta in Curva, sfida nel Derby), una funzione su Supabase o un workflow manda il messaggio a quell'indirizzo, firmato con una chiave segreta. Il service worker della copia offline (`sw.js`) lo riceve e mostra la notifica; toccandola si apre la pagina giusta (le destinazioni ci sono già, `destinazioni55.js`).
- **Si appoggia a quello che c'è:** le notifiche personali su Supabase (`notifiche_stato`) esistono già; la push sarebbe la stessa notifica, spedita anche al telefono. Ognuno sceglie quali ricevere.
- **Telefoni:** Android sì, anche dal browser. iPhone solo con O Girrr aggiunto alla schermata Home (iOS 16.4 o successivo). PC sì.
- **Costi:** zero; i servizi di consegna di Google, Apple e Mozilla sono gratuiti.
- **Serve:** una tabella e una funzione su Supabase (il «vai» per il database), due chiavi segrete nei segreti del progetto (mai nel codice), il pulsante nella pagina Notifiche. Prova nel Lab prima.

### Scarica la Radio per il treno (Claude, 9 novembre 2026; Gianluca: «per ora no»)
Un pulsante «Scarica per ascoltare offline» accanto alla puntata: salva l'mp3 (circa 1,4 MB) nella copia offline.

### Calendario delle giornate in Google Calendar (Claude, 9 novembre 2026; Gianluca: «per ora no»)
Un file `.ics` scritto dai workflow con le giornate e l'orario di consegna della formazione: si aggiunge una volta a Google Calendar (o al calendario dell'iPhone) e si aggiorna da solo, con il promemoria.

### Conto alla rovescia della formazione (Claude, 9 novembre 2026)
In Home «Mancano 3 h 20 min alla consegna della formazione», rosso nell'ultima ora. Con le notifiche push, anche un avviso due ore prima a chi non ha ancora schierato (se il dato è disponibile da Leghe).

### Condividi come immagine (Claude, 9 novembre 2026)
Un pulsante «Condividi» sul risultato della tua partita, sul Tabellone e sulla copertina del Giornale, che apre la condivisione del telefono (WhatsApp del gruppo) con un'immagine pronta. Le immagini del Tabellone le generano già i workflow (`riepiloghi/tabellone-*.png`).

### Cerca un giocatore (Claude, 9 novembre 2026)
Una casella di ricerca: scrivi «Pulisic» e vedi chi lo ha in rosa, voti e fantavoti della stagione, episodi della Moviola, andamento nel Borsino. I dati ci sono già (`data.json`, `formazioni.json`, `girrr/dati/`).

### La mia stagione (Claude, 9 novembre 2026)
A fine girone e a fine stagione un riepilogo a schede da scorrere per ogni squadra: miglior giornata, giocatore che ha portato più fantapunti, Derby vinti, posizione più alta. Livello tecnico per i numeri, editoriale per i testi.

### Risultati provvisori durante la giornata (Claude, 9 novembre 2026, fonte da verificare)
Mentre si gioca la Serie A, punteggio provvisorio delle partite del Girrr. Prima bisogna capire se esiste una fonte affidabile dei voti in diretta: senza, non si fa.

## Fatte
- **Copia offline** (9 novembre 2026): prova nel Lab `lab/offline/`, vedi `STATO.md`.
- **Scorciatoie dell'icona** (9 novembre 2026): Tabellone, Curva, Giornale, Totogirrr; prova nel Lab, vedi `STATO.md`.
