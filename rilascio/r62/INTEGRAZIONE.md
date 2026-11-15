# Integrazione della 6.2 — decisioni e controllo

**Stato: preparazione in ramo di prova, non versione pubblicata.** Ramo `chatgpt/integrazione-62-completa`; non unire la PR #92 (bozza grafica rifiutata). Claude è già in `main` del Registro con le PR #93/#94/#95, e i cartellini sono già nei dati del sito con la PR sito #17.

## Decisioni di Gianluca (15 novembre 2026)
- **La 6.1.1 confluisce nella 6.2**; non aggiungere la 6.1.1 a `versioni.json` come rilascio fittizio. Preservare Carriera/Curva/terminologia e la correzione PC.
- **Il Giornale resta su quattro pagine**, con l'assetto, i caratteri e l'impaginazione originali. La prova a tre A4 della PR #92 è esplicitamente respinta: non usare `rilascio/r62/impagina.cjs`, il PDF o il CSS di quella bozza. Il commento autentico ed eventuali dati MVP vanno integrati nel riquadro Curva originale senza alterare il resto.
- **Lega:** rosso Campionato/azzurro Champions Cup. **Stadio:** elementi di interfaccia oro anche in Coppa, senza togliere sfondi azzurrati e rosati o evidenze di retrocessione/eliminazione. Cerchio del giocatore migliore in campo oro e stella; il colore ordinario del cerchio dello Stadio è lasciato come da disegno del Campo esistente.
- **Confronto A/B ancora da approvare:** A ultimi due sondaggi chiusi in Girrr Sport e richiamo nella Curva; B ultimi due risultati in un blocco collassabile nella Curva, senza riquadri duplicati. In entrambi i casi il voto resta nella Curva.
- **Radio:** aggiungere una sola frase prima delle due battute di chiusura integrali, nella **successiva puntata programmata**, senza nuova voce, TTS, audio aggiuntivo o rigenerazione per la chiusura MVP.
- **Scadenze per nuove aperture soltanto:** vigilia e sfida fino all'inizio, dopo partita 48 ore dai risultati pubblicati, MVP non oltre 48 ore dalla prima apertura e comunque entro il prossimo turno, post 24 ore. **Non modificare votazioni e scadenze già annunciate.** La scadenza registrata della 7ª resta il 21 novembre 2026 alle 15:00 italiane.

## Integrazione preparata sul ramo della PR #96

La copia nuova di gh-pages `98c0add` viene preparata senza scrivere nell'originale. Ordine: **6.1.1 → funzioni native → Campo di Claude → ritocchi di Claude → Giornale originale**. Due preparazioni indipendenti sono state confrontate byte per byte; gli script nativi sono anche ripetibili sulla copia. Le sorgenti di Claude non sono state riscritte.

- `nativa.py` e `sondaggi.js`: sondaggi e stato personale nelle pagine originali, compresi i post del feed; conteggi reali del medesimo voto, senza aggiungere reazioni simulate. Caricamento prima del modulo, scelta immutabile, lettura al ritorno e aggiornamento delle schede aperte. Precedenti con squadra/giornata e testo autentico. Gli stili del prodotto sono quelli esistenti.
- `editoriale.py`: aggiunta contenutistica al solo Coro/riquadro Curva del renderer originale. PDF reali della 6ª e 7ª, quattro A4, stessi livelli di adattamento e scale del renderer prima/dopo. Nessun `impagina.cjs` o PDF rifiutato.
- `backend.py`: prepara separatamente il main del sito, il catalogo nel giro MVP ordinario e l'uso del dossier nella preparazione Radio già programmata. Non esegue automazioni. Il saluto Radio resta integrale; una sola battuta e nessun TTS.
- SQL esclusivamente proposta: stessi archivi di voto delle RPC esistenti, lock e vincoli unici. Gli schemi privati hanno RLS e privilegi negati al browser; preparazione e catalogo server sono riservati al servizio. Le nuove finestre dei post partono dall'attivazione, senza chiudere retroattivamente quelli precedenti senza scadenza conservata. La 7ª MVP conserva il 21 novembre alle 15 italiane.

La **preview esportata** è `lab/integrata-62/`: pagine native, entrambe le grafiche e backend dimostrativo locale. I collaudi confermano zero richieste a Supabase e conservazione della sessione personale già presente: il Lab usa uno spazio separato. Non equivale a un collaudo del database della Lega. Le prove transazionali usano PostgreSQL 17 nativo locale, con due connessioni concorrenti; il gateway browser usa PGlite locale.

`lab/confronto-62.html` apre ora A e B nelle pagine native. La vecchia comparazione concettuale è conservata in `lab/coordinamento-62/confronto-posizioni-bozza.html`, senza essere usata come interfaccia del prodotto. Le schede di Claude in `lab/novita-6-2.html` restano presenti.

**Stato della certificazione:** vedere `QA.md` e i rapporti `prove/v62/risultati-*.json`. I risultati di run precedenti fallite non sono dichiarati superati; il controllo finale dei tre motori deve terminare prima della consegna come completa. Il sito resta alla 6.1.

## Sequenza tecnica

1. Leggere `AGENTS.md`, `STATO.md`, `REGOLE-VERSIONI.md`, `rilascio/r62/NOTE-CLAUDE.md` e questo documento.
2. Preparare una **nuova copia** di `gh-pages` tramite `python3 rilascio/r62/applica.py COPIA_GH_PAGES`. Ordine: 6.1.1, integrazione nativa, Campo e ritocchi di Claude, Giornale. I cinque passaggi devono riuscire e una seconda esecuzione su una copia nuova deve produrre lo stesso risultato.
3. Provare Chromium, WebKit e Firefox × 16 profili × Lega/Stadio; anche ospite e squadra, Coppa, tastiera, Riduci movimento, 320 px, console, PDF originale a 4 pagine. Salvare immagini PC 1920 e TV emulata Lega/Stadio.
4. Solo dopo prova del Lab e «Vai» esplicito al sito: rilasciare `gh-pages`, verificare il sito, quindi aggiornare il `main` del sito se serve. Solo dopo sincronizzare `ufficiale/src/sito/` e lo stato con hash/rollback. Ogni modifica a Supabase necessita un «Vai» specifico.
5. Preparare **un solo annuncio e un solo changelog** secondo `REGOLE-VERSIONI.md` e chiederne approvazione. Non registrare la 6.2 in `versioni.json` prima del rilascio.

**Non dichiarare completamento della 6.2 fino a integrazione e QA effettivamente superati.**

## Giornale come quello di oggi (Gianluca, 15 novembre 2026, sera)

Prevale su tutto ciò che è scritto sopra sul Giornale. Gianluca vuole il Giornale «come l’ha fatto Claude», cioè quello pubblicato oggi, non la versione rigenerata da ChatGPT: quella usciva con caratteri di ripiego (Liberation Sans al posto di Inter e Inter Display, DejaVu al posto di TeX Gyre Pagella) e cambiava gli spazi della pagina 2 e i Top/Flop su quattro colonne. Ora `applica.py` usa `rilascio/r62/giornale_mvp.py` al posto di `editoriale.py`: il generatore originale aggiunge **solo** la rubrica MVP in fondo alla pagina 2, con gli stili della pagina; se lo spazio non basta interviene il normale controllo di impaginazione (pagina 2 a scala 0,94, come già succede alle pagine 1, 3 e 4). Per generare il PDF servono i caratteri Inter, Inter Display e TeX Gyre Pagella come `serif`: senza, Chromium usa caratteri di ripiego. PDF di prova in `lab/giornale-62/g7/` (numero 7 con la rubrica) e `g6/` (numero pubblicato). «Serie A, 11ª giornata» nei Top/Flop e nella formazione c’è già nel Giornale pubblicato dal 9 ottobre: non è stato toccato.

## Rettifica successiva di Gianluca

Prevale sui riferimenti precedenti al Coro: rubrica autonoma MVP con tre candidati della giornata appena conclusa, senza premio precedente. Coro intatto. In pagina 2 si compattano gli spazi e si dispongono Top/Flop su quattro colonne per mantenere quattro A4 e gli stessi caratteri. Portieri: icone laterali, pallone con piccola X per i gol subiti. Prova mirata Chromium su telefono/PC/TV, entrambe le grafiche; tre motori ancora da certificare per questa rettifica.
