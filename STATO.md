# Stato del progetto O Girrr (ultimi giorni — aggiornato 30 ottobre 2026)

## 30 ottobre 2026 — Tabellone con più dati (Claude, prova nel Lab)
- Richiesta di Gianluca: in classifica anche V, N, P, gol fatti, gol subiti e differenza reti. L'ordine della classifica non cambia (Pt, poi Fantapunti) e non c'è nessuna nota sullo spareggio (decisione di Gianluca).
- Sul telefono (<560 px) la classifica mostra DR, Pt e Fantapunti; da 560 px in su anche G, V, N, P, GF, GS. Vale anche per i gironi di Champions Cup (senza Fantapunti, come oggi).
- Patch unica `rilascio/tabellone_dati.py`: con `--lab` crea le copie di prova (`lab/prova-tabellone-lega.html`, `lab/prova-tabellone-stadio.html`, generate dal `tabellone.html` di `gh-pages`, con `<base>` verso il sito e senza statistiche visite); senza `--lab` è la patch per il sito vero. Link nel Lab (card «Tabellone · Più dati in classifica», solo Lab).
- Provato in Chromium a 320, 375, 768 e 1280 px, Lega e Stadio, Campionato e Champions Cup: nessuno scorrimento laterale, console pulita; controllato che V+N+P = G per ogni squadra e che i gol fatti della lega pareggino quelli subiti (84 = 84). Non provato: Safari/iPhone.
- Per il sito vero (dopo il «vai»): `python3 rilascio/tabellone_dati.py girrr/tabellone.html girrr/tabellone.html` e lo stesso per `stadio/girrr/tabellone.html` su `gh-pages`, poi copia in `ufficiale/src/sito/`.

## Carriera a tab — resoconti
Piano e prompt in `proposte/carriera-tab-piano.md`. Base: ramo `claude/review-ai-changes-test-ui9gjy`. Ognuno scrive solo nel suo paragrafo.

### Tab Panoramica e Fiducia + struttura (Claude)
- Carriera divisa in 4 tab (Panoramica, Obiettivi, Fiducia, Storia; la Cassa resta fuori, decisione di Gianluca). Selettore a pillole sotto la bolla, che va a capo a 320 px. Panoramica: arco Fiducia, «N su 4 raggiunti», Reputazione e sponsor. Fiducia: aspettativa, simulatore, nuovo grafico «Fiducia giornata per giornata» (classifica di ogni giornata giocata dal calendario del sito), Fiducia in lega. Zone vuote pronte per ChatGPT (`vCarObiettivi`) e Grok (`vCarStoria`), con versione provvisoria.
- **Solo la propria squadra** (decisione di Gianluca): nell'Anteprima e nel rilascio la Carriera mostra solo la squadra entrata col codice (`ME`), senza selettore (`CARSCELTA=false` da `build.py`). Il selettore resta nel Lab; nell'Anteprima si prova un'altra squadra con `?come=Grodah`. I non entrati vedono già «Entra con la tua squadra» (`livepatch`). Aperto: «Fiducia in lega» mostra ancora la classifica fiducia di tutti.
- Provato in Chromium a 320 e 1280 px su Lab, Lega e Stadio, tutti e 4 i tab e The Blue brothers (due allenatori): nessuno scorrimento laterale, console pulita. Test automatici superati. Non provato: Safari/iPhone.

### Tab Obiettivi (ChatGPT)
- Obiettivi stagionali con progressi, stati e scadenze; Champions Cup del presidente e dell'allenatore; premio sponsor con link solo se riscuotibile.
- Collaudi JavaScript su snapshot del ramo (milestone/Totogirrr e fiducia universale): PASS; verifica equivalente di `collaudo_anteprima_52.py`: PASS.
- Chromium sul componente isolato a 320/375/1280 px, Oranje VC/Grodah/The Blue brothers: 9 casi PASS, nessun overflow o errore JS; stati premio e link verificati.
- Non eseguiti `python3 anteprima/build.py` e `git diff --exit-code anteprima/` in checkout locale (DNS GitHub bloccato); blocco generato propagato nelle anteprime e confrontato.
- Non eseguito browser end-to-end delle tre pagine complete via HTTP, né Safari; serve verifica CI/QA della PR.
- **Verifica Claude (unione PR #36):** `build.py` dà un'Anteprima identica a quella committata; test JS e `collaudo_anteprima_52.py` superati. Chromium sulle pagine complete (Lab, Lega, Stadio) a 320, 375 e 1280 px con Oranje VC, Grodah e The Blue brothers (`?premi=prova`): nessuno scorrimento laterale, console pulita, link «Vai a Totogirrr» solo quando il premio è da riscuotere. A 320 px la linea del tempo scorre dentro la sua card.

### Tab Storia (Grok)
- Riscritta `vCarStoria(t)` in lab/index.html: card intestazione (nome, fascia, Storia N/100, stagioni/titoli/podi), grafico SVG posizioni (asse rovesciato, 🏆 sul 1°, linea e etichette), elenco stagioni con medaglie, Albo (HIST + PRE case-insensitive), racconto generato dai dati. Supporto dual-manager (The Blue brothers). «Prima stagione in lega» se manca HIST.
- Prove: node prove/collaudo_preview52_totogirrr_milestone.js e python3 prove/collaudo_anteprima_52.py OK; build.py eseguito. Browser desktop su lab (tutte le squadre via selettore, Blue brothers entrambi): nessun errore console, contenuto completo, no overflow laterale a ~765 px.
- Non provato: Safari/iPhone e collaudo visuale a 320/375 px; anteprima Lega/Stadio solo via build.
