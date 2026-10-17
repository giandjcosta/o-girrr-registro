# Radio O Girrr: regole decise da Gianluca (da rispettare sempre)

Voci Gemini: Beppe Rovesciata = Charon, Luigi Fischietti = Orus, Giulia Cronaca = Aoede, Ciro Trattativa = Fenrir.
Il secondo commentatore si chiama Luigi Fischietti (non Steve Offside, non Sandro Fuorigioco).

Motori, in ordine: Gemini Pro (gemini-3.8-flash-tts) -> Gemini Lite -> Chirp -> edge-tts (ordine deciso da Gianluca).
Le puntate automatiche usano SOLO_GEMINI=1: se Gemini non risponde per tutte le battute NON si pubblica nulla e resta la puntata precedente.
Limite Gemini: 100 richieste al giorno PER MODELLO (una puntata ne usa circa 32). Non fare più di una puntata di prova al giorno. Non rilanciare in serie: i tentativi si esauriscono.

Testo e toni:
- Niente parentesi o etichette tra [ ]: vengono lette ad alta voce. Il tono deve venire dal senso della frase e dalla scrittura (maiuscole e "!!!" per l'urlo da gol, "Ahahahahah" per la risata, "Ma... davvero?! No!" per lo stupore, puntini per il sospiro).
- "Girrr" si pronuncia "Girr" (due r), altrimenti si mangiano la r.
- Parole che si possono leggere in due modi vanno con l'accento giusto (tabella ACC in puntata.py): Rovesciàta, guardàti, ancòra, sùbito, ecc.
- Tra una voce e l'altra niente rumori: ogni battuta è rifinita (rifinisci in gtrim.py) e le code di rumore di Gemini sono tagliate (taglia_coda).

Montaggio (monta.py): la canzone entra 2 secondi prima del punto scelto, a volume basso, e sale fino al volume pieno nel secondo in cui prima partiva; stesso effetto in chiusura.
Resta da fare: esultanza del pubblico nel mix.

La radio esce automaticamente a fine giornata, quando sarà collegata ai dati veri del Giornale (oggi usa voci-src/dati.json, uno scatto fisso).

## Dati della puntata (deciso da Gianluca il 17 ottobre)
Si usano SOLO dati veri della lega: ultima giornata (re, flop, mazzata), classifica, probabilità, calendario, Champions Cup, notizie di mercato (mercato.json).
Restano scritti a mano e vanno bene: storie dei manager, posizione dell'anno scorso, aspettativa del presidente. I derby li decide lui (o si trova un modo oggettivo / si chiede agli amici).
Niente Totogirrr, niente cassa, niente frasi inventate sulla Curva.
Conferenze stampa: se qualcuno le fa (conferenze.json) la radio fa un riepilogo mischiato dei toni (sicuro / umile / provocatorio) e lo confronta con la partita: parole mantenute, parole forti per niente, umile ma ha dimostrato di valere, ha dichiarato guerra e ha perso. Se non ci sono, la parte salta.
Curva: una volta a settimana, prima di far uscire la radio, chiedere a Gianluca se c'è un post vero (curva.json). Se è vuoto la radio non ne parla.
Attenzione: conferenze.json e mercato.json oggi sono dati di prova (demo: true).

## Derby e rivalità (deciso il 17 ottobre)
Rivalità dalla storia (derby.py + storico.json dall'Albo d'oro), da 0 a 100: stagioni insieme, stagioni insieme nelle prime 4, peso dei podi (titolo 3, secondo 2, terzo 1, vale il più basso dei due) e anzianità (il più basso dei due).
Derby = voti degli amici di Gianluca (regole.json, "derby_amici"): pesano il 60%, la storia il 40%. Derby se l'intensità arriva a 50. Con la lista vuota decide solo la storia: derby se la rivalità storica arriva a 60 su 100, così un derby ha sempre rivalità alta.
Un derby ha sempre rivalità alta: rivalità finale = storia + 60% del voto degli amici, minimo 70 se il voto è almeno 50. Sopra 70 la radio aggiunge "Una rivalità storica!".
AFA SELECCION = Maria (mappa dell'app). Squadre con due allenatori (The Blue brothers) = media dei punteggi delle coppie di allenatori.
