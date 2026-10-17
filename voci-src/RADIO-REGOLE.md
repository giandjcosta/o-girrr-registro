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
