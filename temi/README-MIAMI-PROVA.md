# Miami Nights · Prova grafica REALE su O Girrr 6.2.4 (17 novembre 2026)

**Non un mockup.** `temi/miami-prova.html` carica via iframe same-origin le pagine vere di `lab/integrata-62/` (Lega e Stadio) e aggiunge un CSS di redesign: `temi/miami-ui.css`. Non duplica i dati e non costruisce pagine fake.

## Origine e collaborazione
- Branch `chatgpt/miami-ux-claude-base` nato dal commit `98f1b16` di Claude (`claude/totogirrr-ui-responsive-b2pgee`, PR #126).
- La grafica originale di Claude (`temi/notte-tropicale/`) e il suo caricatore eventi (`temi/evento-loader.js`) **restano intatti**. Questo è un esperimento alternativo iniettabile, non la versione da rilasciare.
- Non si modificano `lab/integrata-62/`, `rilascio/r624/`, `tv.js`, il sito vero o Supabase.

## Come aprirlo
- Compila il link RawGitHack del commit sul branch:
  `https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/miami-ux-claude-base/temi/miami-prova.html`
- Toolbar: **Lega/Stadio**, **Telefono/Schermo**; dentro le pagine tab **Home/Tabellone/Carriera/Totogirrr**.
- Le quattro sezioni sono quelle reali del Lab 6.2.4; i contenuti seguono il loro stato demo/ospite, **non sono i dati inventati degli screenshot**.
- Può essere aperto su telefono; scegliere `Schermo` per la larghezza naturale, `Telefono` per simulare 390 px su PC.

## Modifiche effettivamente implementate
- Navbar distinta: 4 tab glossy con stato attivo e integrazione nei documenti reali.
- Header evento Miami Nights e titoli sportivi condensati.
- Home: hero fotografico, card, sezione Oggi al Girrr, KPI e menu di accesso trasformati.
- Tabellone: switch Campionato/Champions Cup, selettori giornata, board partite e punteggi ridisegnati.
- Carriera: tab, schede, pannelli e titoli con nuova gerarchia visuale.
- Totogirrr: la sua nav dinamica, schede, pulsanti 1/X/2 e selezione rifatti in CSS.
- Responsive fino a 320 px e preferenza `prefers-reduced-motion`.
- Le varianti Lega/Stadio e i colori di stato esistenti non sono sostituiti con logica nuova.

## Limiti e QA
- Static check fatto: i sette file reali esistono nel branch, il JS dell'anteprima è sintatticamente valido, CSS e sorgenti principali sono presenti; il test non garantisce resa in browser.
- `temi/prova_miami_browser.cjs` prevede 24 casi (2 skin × 4 sezioni × 3 viewport), con Playwright/Chromium; **non è stato eseguito**, perché qui non è disponibile Playwright con clone locale e accesso al repository. Non dichiarare il test verde.
- Le fotografie sono URL esterni Unsplash/Pexels con fallback a gradienti. La disponibilità runtime dei CDN, il caching/offline e le prestazioni restano da verificare.
- Le pagine del Lab possono mostrare dati in modalità demo/ospite e contenere interazioni: usare solo per prova visiva e non immettere dati personali/operazioni reali.
- La prova potrebbe non caricarsi se il visualizzatore statico blocca l'iframe; in quel caso l'integrazione in `lab/integrata-62/` con script idempotente è il prossimo passo, non aggirare i blocchi del browser.
- **Nessun merge/deploy**, nessuna modifica permanente. Prima di qualunque rilascio serve prova nel Lab pubblico, regressione WebKit/Firefox, controllo delle immagini, approvazione e «Vai, pubblica» di Gianluca.
