# Miami Nights — variante grafica unica sperimentale · 17/11/2026

## Obiettivo
**Due lavori paralleli, non due varianti Lega/Stadio.** 
1. **Claude**: il suo tema `Notte Tropicale`, loader e Lab restano intatti nel suo branch e nella PR #126.
2. **ChatGPT**: una proposta alternativa `Miami Nights`, su un ramo a parte **derivato esattamente dal commit Claude `98f1b16a9f131ecabf3d46581dad0f20e2fc9530`**. Nessun merge o deploy.

La grafica Miami Nights è **una sola**: non si può alternare Lega/Stadio e il selettore vecchio è nascosto nel solo prototipo. Le pagine Stadio del nostro branch sono state ripristinate byte-per-byte al commit Claude, senza hook Miami. L'eventuale integrazione definitiva potrà essere: tema Claude, tema ChatGPT, oppure fusione selettiva dopo confronto.

## Prova vera
- Apertura diretta HTML su vera Home Lab: 
  `https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/miami-ux-claude-base/lab/integrata-62/girrr/index.html?evento=off`
- Dentro la pagina, navigazione **Home / Tabellone / Carriera / Totogirrr** e funzioni originali Lab 6.2.4.
- Cornice alternativa, con soltanto Telefono/Schermo: `temi/miami-prova.html`.
- La versione originale Claude è confrontabile a `https://raw.githack.com/giandjcosta/o-girrr-registro/98f1b16a9f131ecabf3d46581dad0f20e2fc9530/lab/integrata-62/girrr/index.html?evento=notte-tropicale`.

## Come è implementata
- `temi/miami-ui.css`: nuova direzione UI: tab, chips, score, schedine, pannelli e header rinnovati.
- `temi/miami-nav.js`: navigazione evento autonoma sulle pagine vere del Lab.
- CSS/JS collegati **soltanto alle 4 pagine canoniche girrr** del nostro branch, con `data-miami-ui`, senza cambiare gli altri script/app.
- `temi/applica-miami-lab.py`: riapplica in modo idempotente i due hook dopo eventuale rigenerazione del Lab.
- Dal lavoro di Claude riprendiamo la base HTML/JS 6.2.4 e le fotografie **locali** `lab/integrata-62/temi/notte-tropicale/miami-palme.jpg` e `ocean-drive-notte.jpg` (licenze in `temi/notte-tropicale/CREDITI.md`).
- **Grok come moodboard**, non come licenza: palette ispirazionale cobalto `#3B63D6`, magenta `#FF2B90`, arancione `#E6953E`; font OFL **Bebas Neue**, **League Gothic** e corsivo **Yellowtail**. Niente font custom GTAArtDeco o loghi GTA/Rockstar.

## Verifica e limiti
- GitHub: verifica statica dei file e dei link CSS/JS, parsing di script JS.
- `temi/prova_miami_diretto.cjs`: test Chromium predisposto su 12 combinazioni (4 pagine × 320/390/1440 px), **non ancora eseguito**.
- `temi/prova_miami_browser.cjs`: test della cornice, 12 combinazioni, **non ancora eseguito**.
- Non verificata l'apertura diretta tramite visualizzatore e il browser mobile; immagini e font possono richiedere fallback nel rilascio.
- Il nuovo tema **non è online nel Lab pubblico**, non fa parte dell'app di produzione; nessuna modifica al repo `o-fant-a-girrr` o a Supabase, nessun servizio a pagamento.

## Da fare dopo la valutazione
QA reale Chromium/WebKit/Firefox e su telefono; risolvere overflow e doppie navigazioni se emergono; scegliere con Gianluca quali elementi conservare; integrare eventualmente nel loader di Claude come **una sola esperienza evento**, dopo nuovo «Vai, pubblica».
