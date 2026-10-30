# Carriera a tab: piano di lavoro (Claude, ChatGPT, Grok)

Oggi la Carriera è una pagina sola e lunga. La dividiamo in tab con lo stesso selettore a pillole già usato da Totogirrr (`.seg` + `aria-pressed`). Il selettore della squadra e la bolla del premio restano sopra i tab.

| Tab | Contenuto | Chi |
|---|---|---|
| **Panoramica** | Fiducia del presidente (arco), riassunto obiettivi (quanti Fatto / In corso), riquadro Reputazione e sponsor | Claude |
| **Obiettivi** | Obiettivi della stagione con linea del tempo delle scadenze (giornate 2, 6, 8, 10, 18, 26, 34), obiettivi di Coppa, stato del premio sponsor | ChatGPT |
| **Fiducia** | «Come nasce l'aspettativa», «Come cambia la fiducia con il calendario», «Fiducia in lega», più un grafico della fiducia giornata per giornata | Claude |
| **Storia** | Carriera dell'allenatore: stagioni passate (posizione su quante squadre), titoli, squadre allenate, grafico delle posizioni | Grok |
| **Cassa** | La Cassa della lega già esistente (`vCassa`), oggi irraggiungibile nell'Anteprima | Claude |

## Ordine
1. **Claude (passo 0, prima degli altri):** prepara in `lab/index.html` l'impalcatura dei tab con cinque funzioni separate e due **zone riservate** già pronte (vuote) per ChatGPT e Grok. Rigenera l'Anteprima, prova e unisce a `main`.
2. **ChatGPT e Grok in parallelo**, ognuno sul suo ramo partito dal `main` aggiornato, toccano **solo la propria zona**.
3. **Claude unisce** i due rami (le zone sono separate, quindi niente conflitti), rigenera, prova tutto a 320 px e aggiorna STATO.md. Poi Gianluca prova nel Lab e dà il «vai».

## Contratto delle zone (vale per tutti)
Dentro `lab/index.html` ci saranno:

```js
/* === TAB CARRIERA: OBIETTIVI (ChatGPT) === */
function vCarObiettivi(t){ return '' }
/* === FINE TAB OBIETTIVI === */

/* === TAB CARRIERA: STORIA (Grok) === */
function vCarStoria(t){ return '' }
/* === FINE TAB STORIA === */
```

- `t` è il nome della squadra selezionata. La funzione restituisce **una stringa HTML** e non tocca il DOM.
- Si scrive **solo tra i due commenti della propria zona**. Funzioni di aiuto: nella zona, con un prefisso (`ob_…` per ChatGPT, `st_…` per Grok).
- Gli eventi si agganciano con `document.addEventListener('click'|'change', …)` dentro la zona, filtrando su attributi propri (`data-ob…`, `data-st…`). Dopo un cambio di stato: `render()`.
- Stato locale in `S.ob` / `S.st` (oggetti già creati dall'impalcatura).

---

## Prompt per ChatGPT (da incollare così)

> Lavora nel repository `giandjcosta/o-girrr-registro`. Leggi prima `AGENTS.md` e `STATO.md`, poi `proposte/carriera-tab-piano.md`.
>
> **Compito:** riempi la funzione `vCarObiettivi(t)` in `lab/index.html`, tra i commenti `/* === TAB CARRIERA: OBIETTIVI (ChatGPT) === */` e `/* === FINE TAB OBIETTIVI === */`. Non modificare nient'altro nel file.
>
> **Contenuto del tab Obiettivi:**
> 1. Elenco degli obiettivi della stagione della squadra `t`: i tre del presidente e quello dello sponsor. Usa le funzioni esistenti `OB[t]`, `EXP[t]`, `vittObj(t)`, `sponsorDi(t)`, `esito(...)`, `aGiornata(n,t)`, `gioc()`, `GTOT`, con lo stesso calcolo che fa oggi `vCar()` per `e1`, `e2`, `e4`. Per ogni obiettivo: logo (sponsor) o «Pres.», titolo, barra `.pbar`, etichetta di stato (`Fatto` / `Mancato` / `In attesa della classifica alla Nª` / stato in corso).
> 2. **Linea del tempo** orizzontale delle scadenze: giornate 2, 6, 8, 10, 18, 26, 34. Pallino pieno = giornata giocata (`gioc()` o calendario `CL`), evidenziata la prossima. Sotto ogni scadenza, gli obiettivi che si decidono lì (es. vittorie entro l'8ª, sponsor alla 10ª o a fine stagione). Su 320 px deve scorrere **dentro la sua scatola** (`overflow-x:auto`), mai la pagina.
> 3. Obiettivi di Coppa: `OB[t].cp` (presidente) e `OB[t].ca` (allenatore), solo testo con stato «In corso».
> 4. Premio sponsor: riusa `premioSponsor(t)` e `premi52Riscossi(t)` (già nel file) per mostrare «In corso / Da riscuotere / Riscosso» e i crediti. **Non** creare altri premi né importi.
>
> **Regole:**
> - Ramo `chatgpt/carriera-tab-obiettivi` partito dal `main` aggiornato. Commit che iniziano con `ChatGPT:`.
> - **Non modificare a mano** `anteprima/index.html` né `anteprima/attuale.html`: dopo ogni modifica al Lab lancia `python3 anteprima/build.py` e committa i file generati. Il workflow «Anteprima Totogirrr 5.2 QA» fallisce se l'Anteprima non corrisponde al Lab.
> - Grafica: classi esistenti (`.card`, `.ob`, `.pbar`, `.tag`, `.sm`, `.mut`, `.row`), niente librerie, niente CSS globale nuovo (stili inline o con prefisso `.ob-`).
> - Testi in italiano da campionato vero, maiuscola iniziale, niente «fantacalcio» e niente disclaimer «simulazione / dati finti».
> - Niente Supabase, niente `fetch` nuovi.
> - Prove prima di consegnare: `node prove/collaudo_preview52_totogirrr_milestone.js`, `node prove/collaudo_fiducia_universale52.js`, `python3 prove/collaudo_anteprima_52.py`. Prova nel browser a 320, 375 e 1280 px su `lab/index.html#carriera`, `anteprima/attuale.html#carriera` e `anteprima/index.html#carriera`: nessuno scorrimento laterale, console senza errori.
> - Non unire a `main`: apri una Pull Request verso `main` e scrivi cosa hai provato e cosa no.

## Prompt per Grok (da incollare così)

> Lavora nel repository `giandjcosta/o-girrr-registro`. Leggi prima `AGENTS.md` e `STATO.md`, poi `proposte/carriera-tab-piano.md`.
>
> **Compito:** riempi la funzione `vCarStoria(t)` in `lab/index.html`, tra i commenti `/* === TAB CARRIERA: STORIA (Grok) === */` e `/* === FINE TAB STORIA === */`. Non modificare nient'altro nel file.
>
> **Contenuto del tab Storia (carriera dell'allenatore della squadra `t`):**
> 1. Intestazione: nome dell'allenatore (`mg(t)`; per «The Blue brothers» `mgrsOf(t)` restituisce due allenatori: mostrali entrambi), fascia attuale (`fascia(t)`) e punteggio storico (`Math.round(histScore(t))` su 100).
> 2. **Stagione per stagione** da `HIST[allenatore]`: ogni riga è `[stagione, posizione, numero squadre]`. Mostra «2024/25 · 5° su 10», con 🏆 per il 1° posto. Più recente in alto.
> 3. **Grafico SVG** delle posizioni nelle stagioni (asse verticale rovesciato: 1° in alto), inline, `viewBox` e `width:100%` così si adatta a 320 px. Colori dalle variabili esistenti (`var(--gold)`, `var(--mute)`, `var(--line)`).
> 4. Titoli: conteggio dei 1° posti in `HIST` più gli anni pre-storici in `PRE` (`[stagione, squadra, allenatore]`) dove compare l'allenatore.
> 5. Una frase di racconto generata dai dati (es. «Tre podi nelle ultime cinque stagioni, titolo nel 2025/26»), come un giornale sportivo vero.
>
> **Regole:**
> - Ramo `grok/carriera-tab-storia` partito dal `main` aggiornato. Commit che iniziano con `Grok:`.
> - **Non modificare a mano** `anteprima/index.html` né `anteprima/attuale.html`: dopo ogni modifica al Lab lancia `python3 anteprima/build.py` e committa i file generati. Il workflow «Anteprima Totogirrr 5.2 QA» fallisce se l'Anteprima non corrisponde al Lab.
> - Grafica: classi esistenti (`.card`, `.row`, `.tag`, `.sm`, `.mut`, `.num`), niente librerie, niente CSS globale nuovo (stili inline o con prefisso `.st-`).
> - Testi in italiano da campionato vero, maiuscola iniziale, niente «fantacalcio» e niente disclaimer. «Derby» con la D maiuscola se compare.
> - Niente Supabase, niente `fetch` nuovi: tutti i dati sono già nel file.
> - Prove prima di consegnare: `node prove/collaudo_preview52_totogirrr_milestone.js`, `python3 prove/collaudo_anteprima_52.py`. Prova nel browser a 320, 375 e 1280 px su `lab/index.html#carriera`, `anteprima/attuale.html#carriera` e `anteprima/index.html#carriera`, con almeno tre squadre diverse, tra cui «The Blue brothers»: nessuno scorrimento laterale, console senza errori.
> - Non unire a `main`: apri una Pull Request verso `main` e scrivi cosa hai provato e cosa no.

## Lavoro di Claude
- **Passo 0:** impalcatura tab (`S.ctab`, selettore `.seg` sotto la bolla, funzioni `vCarPanoramica`, `vCarFiducia`, `vCarCassa`, zone vuote `vCarObiettivi` e `vCarStoria`), con il contenuto attuale spostato senza cambiarne la logica. La Cassa è raggiungibile dal tab, e `route('cassa')` apre direttamente quel tab.
- **Fiducia:** aggiunge il grafico «Fiducia giornata per giornata» (da `aGiornata(n,t)` per le giornate giocate e `fidA`).
- **Unione finale:** unisce i rami ChatGPT e Grok, rigenera, prova tutto e aggiorna `STATO.md`.
