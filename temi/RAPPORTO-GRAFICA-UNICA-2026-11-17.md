# 17/11/2026 — O Girrr: grafica evento UNICA, non Lega/Stadio

## Decisione di Gianluca
Durante l'evento 18–20 novembre deve esistere **una sola identità visiva** totalmente diversa dalle due grafiche permanenti. Non due interpretazioni del tema. Quando si spegne l'overlay, Lega/Stadio ritornano esattamente come prima.

## Modifiche effettive nel branch `chatgpt/miami-nights-fusione-lab`
- Aggiunto il livello finale `EVENT TAKEOVER UNICO` a `temi/notte-tropicale/notte-tropicale.css` e alla copia IDENTICA `lab/integrata-62/temi/notte-tropicale/notte-tropicale.css`.
- Token fissi evento: fucsia `#ff4bac`, tramonto `#ffb875`, ciano `#86eeff`, notte `#160b2a`; tutte le variabili `--acc`, `--hi`, `--bg`, `--v53-accent`, `--v53-title-font` del tema sovrascritte identicamente nelle due origini.
- La Home nasconde SOLO DURANTE L'EVENTO la specifica immagine logo Lega/Stadio nella testata e usa un marchio evento CSS unico, mantenendo il link Home e tutte le pagine.
- Menu, tab, card, titoli e dock del tema (base Claude + Home V3 ChatGPT) hanno la stessa identità. Dati, click, squadre, competizioni e semantica esiti non alterati.
- Loader di Claude, fotografie vere locali, script barra mobile, tab Totogirrr e componente Tabellone mantenuti.
- Aggiunto `temi/prova_ui_unica.cjs`: script QA Chromium per le DUE origini, sei viewport, valori CSS, overflow e link. **Non eseguito sul Lab**.

## Risultati realmente verificati
1. Controlli statici sul codice effettivo in GitHub: **10/10** passati (CSS sorgente=Lab, scope, token, entrambe origini, logo evento, media query, asset, motore, reduced-motion, bilanciamento CSS).
2. Un **prototipo HTML locale di sola dimostrazione**, non la Home del Lab: testato davvero con Chromium headless tramite `page.set_content`. A 320, 375, 390, 768 e 1440 px: larghezza senza overflow, nessun errore JavaScript, navigazione fra Home/Tabellone/Carriera/Totogirrr, selezione demo 1/X/2. Con il solo attributo `data-origin` che cambia Lega→Stadio, screenshot a 390px pixel-identici; è una prova di principio del prototipo, NON la certificazione delle pagine reali.
3. Screenshot PNG del prototipo e ZIP HTML locale disponibili nella conversazione ChatGPT del 17/11.

## Precisazioni sulle immagini
- Il prototipo HTML offline usa **un ritaglio della bozza illustrata** già mostrata: NON è una fotografia originale e lo screenshot non deve essere chiamato «schermata del Lab».
- Il Lab su GitHub mantiene le 3 foto vere locali già verificate da Claude, con crediti in `temi/notte-tropicale/CREDITI.md`.
- Prima di andare in produzione è indispensabile uno screenshot dal vero Lab Lega e Stadio, non quello simulato.

## QA ancora aperta
- Caricamento e resa del CSS del Lab in Chromium/WebKit/Firefox, iPhone reale e PC; effettiva identità visiva sul DOM reale, anche con eventuali `!important` di Stadio.
- Navigazione da Home a Carriera/Tabellone/Totogirrr/Curva/Giornale e ritorno; preferenze sessione `?evento=`, senza regressioni.
- Colorimetria dei significati (vittoria/sconfitta, competizioni, accessibilità); selettori semanticamente importanti non devono diventare ambigui.
- Carico/ottimizzazione immagini e font offline. `?ospite=1` utile solo per prova di sola lettura.
- Prima del rilascio: run di `temi/prova_ui_unica.cjs` da root con server locale, review Claude sulla PR #126 e consenso esplicito «Vai, pubblica».

## Link alla fusione
Lega `lab/integrata-62/girrr/index.html?ospite=1&evento=notte-tropicale` e Stadio `lab/integrata-62/stadio/girrr/index.html?ospite=1&evento=notte-tropicale` su questo branch. Devono mostrare **la stessa grafica evento**, non due skin diverse.

Nessun commit sul sito vero, nessun merge, nessuna modifica Supabase, nessun costo esterno. Il nome pubblico «City Nights» / «Notte Tropicale» resta da approvare; evitare loghi GTA/Rockstar non autorizzati.
