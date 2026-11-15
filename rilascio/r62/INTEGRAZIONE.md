# Integrazione della 6.2 — decisioni e controllo

**Stato: preparazione in ramo di prova, non versione pubblicata.** Ramo `chatgpt/integrazione-62-completa`; non unire la PR #92 (bozza grafica rifiutata). Claude è già in `main` del Registro con le PR #93/#94/#95, e i cartellini sono già nei dati del sito con la PR sito #17.

## Decisioni di Gianluca (15 novembre 2026)
- **La 6.1.1 confluisce nella 6.2**; non aggiungere la 6.1.1 a `versioni.json` come rilascio fittizio. Preservare Carriera/Curva/terminologia e la correzione PC.
- **Il Giornale resta su quattro pagine**, con l'assetto, i caratteri e l'impaginazione originali. La prova a tre A4 della PR #92 è esplicitamente respinta: non usare `rilascio/r62/impagina.cjs`, il PDF o il CSS di quella bozza. Il commento autentico ed eventuali dati MVP vanno integrati nel riquadro Curva originale senza alterare il resto.
- **Lega:** rosso Campionato/azzurro Champions Cup. **Stadio:** elementi di interfaccia oro anche in Coppa, senza togliere sfondi azzurrati e rosati o evidenze di retrocessione/eliminazione. Cerchio del giocatore migliore in campo oro e stella; il colore ordinario del cerchio dello Stadio è lasciato come da disegno del Campo esistente.
- **Confronto A/B ancora da approvare:** A ultimi due sondaggi chiusi in Girrr Sport e richiamo nella Curva; B ultimi due risultati in un blocco collassabile nella Curva, senza riquadri duplicati. In entrambi i casi il voto resta nella Curva.
- **Radio:** aggiungere una sola frase prima delle due battute di chiusura integrali, nella **successiva puntata programmata**, senza nuova voce, TTS, audio aggiuntivo o rigenerazione per la chiusura MVP.
- **Scadenze per nuove aperture soltanto:** vigilia e sfida fino all'inizio, dopo partita 48 ore dai risultati pubblicati, MVP non oltre 48 ore dalla prima apertura e comunque entro il prossimo turno, post 24 ore. **Non modificare votazioni e scadenze già annunciate.** La scadenza registrata della 7ª resta il 21 novembre 2026 alle 15:00 italiane.

## Cosa esiste e cosa manca

**Già nella parte di Claude del Lab:** Campo con Coppa, navigazione tra partite/giornate, cambio fluido, tua partita, migliore in campo, cartellini, ritocchi del Tabellone e Padri Fondatori. Vedere `rilascio/r62/NOTE-CLAUDE.md`.

**Pronto come codice isolato in questa integrazione:** `calcoli/finestre62.py`, `voci-src/mvp_editoriale62.py`, `voci-src/copione.py` e `voci-src/prepara_dati.py` (nuovo segmento solo con `--mvp-tifosi`), `prove/v62/testi.py` e la **proposta NON applicata** `sql/votazioni-62-proposta.sql`. Sono stati recuperati dal lavoro Work senza importare la grafica rifiutata.

**Da completare prima di un rilascio:** integrazione di votazioni, Precedenti, MVP e risultati nelle pagine reali Lega/Stadio conservando menu e grafica; mappatura reale degli ID di sfide/post, compatibilità con voti preesistenti e controlli sull'autenticazione a codice; test con PostgreSQL di più sessioni; aggiornamento del Giornale originale a quattro pagine e del dossier editoriale; eventuale collegamento dei metadati alle automazioni. Nessuna modifica al DB senza autorizzazione separata.

La pagina `lab/confronto-62.html` confronta le posizioni A/B **solo come struttura visiva**, senza transazioni e senza dichiarare che sia la pagina di produzione. La pagina `lab/novita-6-2.html` mantiene tutte le schede di Claude e integra i riferimenti alle altre aree. La 6.1.1 continua a essere consultabile da `lab/novita-6-1-1.html`.

## Sequenza tecnica

1. Leggere `AGENTS.md`, `STATO.md`, `REGOLE-VERSIONI.md`, `rilascio/r62/NOTE-CLAUDE.md` e questo documento.
2. Preparare una **nuova copia** di `gh-pages` tramite `python3 rilascio/r62/applica.py COPIA_GH_PAGES`. Ordine: 6.1.1, Campo di Claude, ritocchi di Claude. I tre passaggi devono riuscire e una seconda esecuzione su una copia nuova deve produrre lo stesso risultato.
3. Provare Chromium, WebKit e Firefox × 16 profili × Lega/Stadio; anche ospite e squadra, Coppa, tastiera, Riduci movimento, 320 px, console, PDF originale a 4 pagine. Salvare immagini PC 1920 e TV emulata Lega/Stadio.
4. Solo dopo prova del Lab e «Vai» esplicito al sito: rilasciare `gh-pages`, verificare il sito, quindi aggiornare il `main` del sito se serve. Solo dopo sincronizzare `ufficiale/src/sito/` e lo stato con hash/rollback. Ogni modifica a Supabase necessita un «Vai» specifico.
5. Preparare **un solo annuncio e un solo changelog** secondo `REGOLE-VERSIONI.md` e chiederne approvazione. Non registrare la 6.2 in `versioni.json` prima del rilascio.

**Non dichiarare completamento della 6.2 fino a integrazione e QA effettivamente superati.**
