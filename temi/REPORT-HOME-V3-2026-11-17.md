# O Girrr — Miami Nights Home V3 · 17 novembre 2026

## Obiettivo
Tradurre il mockup grafico generato in una **pagina HTML/CSS/JavaScript reale** e navigabile. **Non è uno screenshot AI**. Prototipo isolato: non collegato ai dati ufficiali della lega, non pubblicato nella app e non certificato per deploy.

## File realizzati
- `temi/anteprima-home-v3.html`: Home completa con una hero fotografica, intestazione O Girrr, titolo City Nights in corsivo neon, navigazione nuova, sezione Big Match, classifica, indicatori stagione e tre schede editoriali.
- `temi/home-v3.css`: UI realmente diversa dalle skin standard (tab a pillola neon, componenti scorecard, layout mobile/desktop, dock mobile); media query 850/680/420/340 px, `prefers-reduced-motion`, focus e skip link.
- `temi/home-v3.js`: alternanza dimostrativa tramonto/notte (due foto), indicatore ARIA e fallback gradient se CDN non disponibile.
- `temi/prova_home_v3.cjs`: QA Playwright riutilizzabile, sei viewport, aria/nav, overflow, toggle, screenshot. Non ancora eseguito in browser reale.
- `temi/index.html`: link predefinito alla Home V3, vecchia V2 conservata e raggiungibile.

## Design
- Ispirazione al mockup approvato; nome grafico **Miami Nights** (identità originale O Girrr). Evita loghi, brand e illustrazioni Rockstar.
- Contrasto rosa/fucsia/viola e arancio, titoli sportivi bold in Barlow Condensed, firma corsiva Yellowtail, componenti leggibili.
- Squadre, calendario, punteggi, stagione e classifica sono dichiaratamente **sintetici**.
- CTA e tab collegano a file demo effettivamente presenti: Tabellone, Carriera e Totogirrr. Nessun login, Supabase, modifica dati o pagamenti.
- Foto remote sperimentali: Unsplash `photo-1605723517503-3cadb5818a0c`; Pexels Luis Erives `11457824`. Prima di un rilascio serve validare la resa, salvare asset ottimizzati e testare offline.

## Verifiche effettuate
Verifica statica dei sorgenti **14/14**: tutti i file trovati; import CSS/JS corretti; link esistenti; demo chiaramente segnalata; tema e skin separati; quattro tab nuove; immagini e toggle; CSS responsive e reduced motion; skip link e nomi accessibili; parentesi CSS bilanciate; link hub aggiornato.
**Non eseguiti**: Playwright, test reali Chromium/WebKit/Firefox, screenshot da browser, schermi e foto su rete reale, test touchscreen. Nessun esito QA di questi test è dichiarato.

## Stato branch
`chatgpt/theme-engine-vice-city-event` era diverged rispetto a `main` (36 commit ahead, 13 behind al controllo). Nessun merge o riallineamento automatico: integrare con cautela l'attuale 6.2.4 e le modifiche Claude. Niente modifica a `giandjcosta/o-fant-a-girrr`, a Supabase, al Lab pubblico o a servizi a pagamento.

## Collaborazione con Claude
Claude presidia il caricatore temporale `temi/evento-loader.js`, attivazione/scadenza e integrazione sulle pagine reali. ChatGPT si limita ai file V3 e design system; nessun conflitto sui suoi file. Riferimento PR #125: https://github.com/giandjcosta/o-girrr-registro/pull/125

## Prossime azioni necessarie
1. Eseguire `node temi/prova_home_v3.cjs http://127.0.0.1:8768/temi/` mentre nella root gira `python3 -m http.server 8768`, correggere eventuali problemi e raccogliere veri screenshot PC/mobile.
2. Sostituire gli asset CDN con foto originali/librerie verificate con dimensioni corrette, compressione e fallback offline.
3. Concordare con Claude il porting delle nuove tab, card e dei titoli sulle **pagine vere** nel Lab, usando il suo loader come unico attivatore.
4. Collaudare Lega/Stadio, desktop/mobile/TV, accessibilità, e chiedere approvazione esplicita prima di un eventuale deploy.
