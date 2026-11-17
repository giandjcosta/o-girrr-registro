# Coordinamento UI + infrastruttura — ChatGPT ↔ Claude (17 novembre 2026)

Stato: **solo sperimentale** · Nessun merge/deploy · Commento di coordinamento pubblicato in PR #125.
PR: https://github.com/giandjcosta/o-girrr-registro/pull/125

## Evidenza visionata
- Claude: `temi/evento-loader.js`, `temi/prova_evento.js` (14 casi superati secondo suo rapporto), `temi/CONSIGLI-CLAUDE.md` (24 combinazioni Chromium dichiarate superate), `temi/notte-tropicale/notte-tropicale.css`, `temi/notte-tropicale/lab.py` e `scena.svg` nella sua PR.
- ChatGPT: quattro schermate demo + hub, `temi/theme-engine.js`, fotografie Unsplash/Pexels e titolo decorativo neon.
- Claude ha rilevato i controlli demo fissi sovrapposti su iPhone SE. Correzione applicata dalla nostra parte: `temi/anteprima-home.html` commit `898b83ddd8540309fe08f10784fe522b611e042a`. Ora controlli nel flusso con ARIA; **correzione non ancora verificata nel browser**.
- La PR #125 include differenze molto ampie provenienti dai nuovi commit di `main` del Registro (versione 6.2.4), dunque non unirla prima del riallineamento e della review dei soli file in `temi/`.

## Divisione per evitare conflitti
- Claude: caricatore temporale, integrazione nel vero Lab, allineamento alla 6.2.4, test e rollback; NON editare le demo ChatGPT e il loro design.
- ChatGPT: asset fotografici con licenze verificate, tipografia, art direction, stile dei pannelli e dei dati, mockup responsive; NON editare `tv.js`, `rilascio/r624/`, `lab/integrata-62/` o la grafica `notte-tropicale` di Claude senza accordo.
- In produzione un **solo controller di attivazione**. Il loader di Claude è candidato principale. Non eseguire insieme l'attivazione automatica di `theme-engine.js` e quella di `evento-loader.js`.
- Le due grafiche permanenti restano distinte: Lega rossa/azzurra e Stadio oro secondo AGENTS.md, con colori di stati rispettati. L'evento è un overlay reversibile.
- Le foto devono essere pacchettizzate o avere un fallback affidabile prima del rilascio e la grafica deve essere leggibile offline. Sfondi originali stilizzati possono diventare fallback, non sostituire la direzione fotografica richiesta.
- Titoli decorativi in corsivo neon; statistiche e risultati in font sportivo bold leggibile.

## Gate
Solo `chatgpt/theme-engine-vice-city-event` per ChatGPT; nulla su sito vero `o-fant-a-girrr` né Supabase. Preview reale desktop/mobile e test, decisione sul nome pubblico, nuovo «Vai, pubblica». Le prove di Claude sono **dichiarazioni nel suo rapporto**, non test ripetuti da ChatGPT.

## Prossimi passi
1. Preparare prototipo fotografico sul foglio evento integrabile nei selettori reali (senza sovrascrivere gli asset di Claude).
2. Riprendere dal sito aggiornato 6.2.4 e preparare demo Lega/Stadio nel Lab.
3. Rivedere il caricatore una volta isolati i suoi file dalla PR #125, con priorità scadenza e offline.
4. Fare review incrociata e annotare i bug verificati; non dichiarare collaudi passati senza esecuzione.
