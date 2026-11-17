# Miami Nights · PROVA GRAFICA REALE sul Lab 6.2.4

**17 novembre 2026 · Branch di prova `chatgpt/miami-ux-claude-base` · Non pubblicato.**

Questa NON è una serie di screenshot AI. Sono le otto pagine originali del Lab 6.2.4 (Home, Tabellone, Carriera, Totogirrr, Lega e Stadio), con due file di tema aggiunti ai veri documenti:
- `temi/miami-ui.css` (regole grafiche per header, tab, pillole, card, score, schedine e mobile).
- `temi/miami-nav.js` (barra di navigazione evento nativa tra pagine vere).
- `temi/applica-miami-lab.py` (script idempotente per rigenerare le otto copie del Lab dal loro HTML originale dopo aggiornamenti di Claude).

## Aprire
- **Lega (Home)**: `https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/miami-ux-claude-base/lab/integrata-62/girrr/index.html`
- **Stadio (Home)**: `https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/miami-ux-claude-base/lab/integrata-62/stadio/girrr/index.html`
- Nav all'inizio delle pagine: Home, Tabellone, Carriera, Totogirrr.
- Una cornice di confronto alternativa è in `temi/miami-prova.html`, ma **i due link sopra sono diretti e non usano iframe**.

## Provenienza e isolamento
- Branch derivato dal commit Claude `98f1b16` (PR #126), che include il Lab 6.2.4.
- Il lavoro su `temi/notte-tropicale/`, `temi/evento-loader.js` e le altre modifiche Claude resta intatto.
- Le modifiche a `lab/integrata-62/` esistono solo nel branch ChatGPT, non nel Lab pubblico, non nel repo del sito, non in Supabase.
- Nessun merge, nessun deploy, nessun costo esterno.
- Il CSS porta foto remote con fallback gradiente: prima del rilascio bisogna incorporare asset/fallback offline e verificare le licenze.
- Dati e componenti sono quelli delle pagine originali del Lab (possono essere in stato demo/ospite, non inventati per immagini).

## Verifiche reali fatte
- Ho verificato via API GitHub l'esistenza e il contenuto delle otto pagine, presenza di un solo link CSS e un solo script JS per pagina, e la correttezza dei percorsi relativi (Lega vs Stadio).
- Ho effettuato parsing sintattico JS di `miami-nav.js` e dello script della cornice: esito positivo.
- **Test browser reale NON eseguito da questa sessione.** I test automatici `temi/prova_miami_diretto.cjs` (24 combinazioni: 2 skin × 4 sezioni × 320/390/1440) e `temi/prova_miami_browser.cjs` sono predisposti per Playwright Chromium in ambiente con clone e browser. Non dichiararli superati senza esecuzione.

## Da completare
- QA visivo e funzionale Chromium, Firefox, WebKit e su telefono vero; evitare overflow, errori console e incompatibilità.
- Le immagini remote e l'eventuale interferenza di CSS generati dinamicamente richiedono verifica in browser.
- Dopo approvazione estetica: integrare la variante approvata nel generatore della versione corrente, con il loader di Claude come unico controller evento.
- Per ogni rilascio: nuova autorizzazione esplicita «Vai, pubblica».
