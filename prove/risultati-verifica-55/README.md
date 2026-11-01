# Verifica della 5.5 di Claude — 1 novembre 2026

Base verificata: `4a0720883998b354292b1103077479a3c525058a`, presente sia su `main` del Registro sia su `claude/campo-unione-chatgpt`. Il sito pubblico O Girrr è stato soltanto letto.

- `baseline.json`: dieci percorsi Home → Tabellone → Campo, entrambe le skin a 320/390/768/1280/1440. Ventidue giocatori della quinta giornata, nomi confrontati con le formazioni pubbliche, clic funzionanti, nessun errore JS/HTTP né overflow. Prima della correzione Invio non apriva i dettagli (dieci riproduzioni).
- Screenshot `campo-claude-*.png`: vista delle formazioni di Claude a 390 e 1440, presa durante la verifica del commit di base; gli screenshot precedenti con i monogrammi non rappresentano più questo Campo.
- `percorsi-completi.json`: esiti del collaudo delle sei sezioni della 5.5.
- `statici.json`: tre controlli superati; `prova_cronache_integrate.py` fallisce perché i collegamenti post/Radio preparati da ChatGPT non sono stati integrati su questa base. Il fallimento resta visibile.

Sul ramo di revisione sono corretti il selettore ancora etichettato 5.3, il vecchio link nelle Notizie del Registro e i comandi Invio/Spazio sui giocatori. `prova_campo_contenuti.py` ora isola anche `formazioni.json` con fixture e prova 22 giocatori, Invio e Spazio; entrambe le skin PASS. Build riproducibile.

Le formazioni pubbliche esistono per G2–G5. Gianluca conferma che i dieci nomi dei Blue brothers in G4 / Serie A 8 sono corretti: la squadra aveva molti infortuni. Il controllo che nascondeva quella formazione è stato corretto: sono mostrati dieci giocatori e gli undici avversari, senza ricostruzioni o dati scritti. La prova controllata 10 + 11 si aggiunge a quella 11 + 11. La sostituzione automatica dello stesso ruolo è una stima della logica del client, non una posizione reale sul terreno.

Non verificati Safari/iPhone fisico e una futura giornata reale. Le nuove modifiche sono solo sul ramo `chatgpt/verifica-55-claude`: nessun merge, pubblicazione, audio o scrittura a Supabase.
