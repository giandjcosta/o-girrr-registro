# O Girrr · Fusione Notte Tropicale × Miami Nights V3 — 17/11/2026

## Sintesi
Questa è la **prima fusione reale nel Lab** tra il lavoro di Claude e l'art direction Home V3 di ChatGPT. Non è una nuova app standalone e non cambia il sito pubblico.

**Origine branch**: `claude/totogirrr-ui-responsive-b2pgee` al commit bloccato `9431b587c3d008a8f3e396ccf3ec9e24d7da0a1c`, copiato nel nuovo `chatgpt/miami-nights-fusione-lab`. La PR di Claude #126 non è stata unita e il suo branch non è stato modificato.

## Cosa rimane di Claude (conservato)
- `temi/evento-loader.js`: unico caricatore, in modalità SOLO MANUALE nel Lab; date 18–20 novembre, gestione preferenze sessione e spegnimento a fine finestra per la versione di rilascio, da validare prima del deploy.
- `temi/notte-tropicale/notte-tropicale.js`: navbar mobile, senza seconda navbar concorrente, barra nascosta nello Spogliatoio e quando la schedina copre il fondo.
- Fotografie reali locali (miami-palme.jpg, ocean-drive-notte.jpg, miami-tramonto.jpg) e scena SVG fallback. Crediti e licenze in `temi/notte-tropicale/CREDITI.md`.
- Titoli neon, tab Totogirrr in griglia, selettori inclinati Tabellone, base scura per leggibilità.
- Le vere Home e pagine 6.2.4 già nel Lab, Lega e Stadio.

## Cosa aggiunge ChatGPT — porting del mockup Home V3 alle pagine vere
Aggiunte nuove regole con commento `Miami Nights / fusione della UI` al fondo di due file IDENTICI:
- `temi/notte-tropicale/notte-tropicale.css` (sorgente unico che il generatore di Claude copia)
- `lab/integrata-62/temi/notte-tropicale/notte-tropicale.css` (preview aggiornata senza rigenerare né riscrivere le pagine HTML)

Interventi visivi: hero fotografica dedicata in Home, badge evento, logo e titolo sportivo XXL con firma corsiva, nuove tab principali vere `.v53-menu` in griglia, dashboard `.v53-home`, KPI originali in card neon, spotlight `.big`, riquadri risultati `.strip`, sei card editoriali fotografiche `.cards>.c`, pannelli Curva/Notifiche e dock mobile di Claude conservato.

**Nessun dato inventato** nella fusione: le pagine caricano gli stessi dati e usano gli stessi link dell'app. Ospite consigliato per prova di sola lettura (`?ospite=1`). Non abbiamo introdotto alcuna nuova scrittura dati o chiamata al database.

## Preview da verificare in browser (non certificata)
- Lega: `lab/integrata-62/girrr/index.html?ospite=1&evento=notte-tropicale`
- Stadio: `lab/integrata-62/stadio/girrr/index.html?ospite=1&evento=notte-tropicale`
- Modalità notte: aggiungere `&evento-sfondo=notte`
- Spegnere: `?evento=off` (sulla stessa cartella). Il flag tema resta nella sessione come implementato da Claude.

Usare il **branch di fusione**, non l'URL GitHub Pages pubblico del Registro (che non contiene ancora queste modifiche).

## QA effettivo
**10/10 controlli statici eseguiti:**
- CSS origine e Lab identici;
- codice Claude originario e modifiche Home V3 entrambe presenti;
- attributo tema distinto da skin;
- HTML Home Lega e Stadio presenti e loader manuale;
- tutte e 3 le fotografie locali presenti;
- CSS riduzione movimento presente;
- sintassi delle graffe/commenti/stringhe CSS bilanciata.

**Non eseguiti:** screenshot reali, Playwright, Safari/WebKit, Firefox, touchscreen, prove di switch off/on durante navigazione, accessibilità colori, layout 320/390/1280/1920. Un tentativo di verifica dell'URL RawGitHack via strumento web ha restituito URL non accessibile; ciò **non equivale** a sito non funzionante.

## Limiti e rischi
- CSS usa `!important` perché la versione 6.2.4 ha altre specificità elevate. Priorità futura: ridurre l'override dopo test e confronto con CSS originali.
- L'hero è fotografica sopra il testo; serve QA contrasto su schermi reali.
- Le card `.cards>.c` passano a griglia a 3 colonne PC e 2 telefono (1 a 365px): da verificare per elementi dinamici e contenuti molto lunghi.
- Nessun merge della PR #125/#126. Nessuna modifica a `main`, `gh-pages` del sito vero o Supabase, né strumenti a pagamento.

## Prossimo passo
Provare questa fusione in Chromium/WebKit/Firefox sui viewport richiesti, correggere le eventuali differenze tra Lega e Stadio e condividere la review con Claude PR #126. Dopo approvazione di Gianluca preparare uno script di rilascio idempotente e il rollback.
