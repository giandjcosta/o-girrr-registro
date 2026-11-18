# Transizione B · Studio delle alternative (6.5)

Claude, 18 novembre 2026. Ramo `claude/girrr-transition-effects-zpfofz`, derivato da `chatgpt/65-transizione-b-sfumata-60fps` (PR #134). **Solo anteprima nel Lab**: niente merge, niente deploy, niente Supabase, date dell'evento invariate. La copertina A non è toccata.

Pagina di confronto: `lab/transizioni-b.html` (selettore di variante e schermo, «Riprova», video a 60 fps, tabella delle misure).
Indirizzo diretto: `lab/integrata-62/girrr/index.html?evento=notte-tropicale&evento-intro=trasformazione&b=<variante>`.
Senza `b=` resta la transizione attuale di ChatGPT.

| Parametro `b=` | Alternativa | Durata |
|---|---|---|
| `nuvola` | E · Nuvola e polvere (tecnica F) | 3,0 s |
| `fumo` | C · Fumo | 3,1 s |
| `vento` | D · Polvere nel vento (tecnica F) | 3,2 s |
| `nuvola-morbida` | A · Nuvola morbida | 3,0 s |
| `nuvola-maskpos` | Solo misura: E con `mask-position` animata | 3,0 s |

Durate allungate di circa un quarto il 19 novembre (Gianluca: «leggermente più lente»); le misure e i video qui sotto sono stati fatti con le durate di prima (2,4–2,6 s). Facoltativi: `b-durata=1600…4500` (ms) e `b-leggero=1|0` per forzare la versione leggera.

## Come funziona
0. I caratteri della skin si scaricano prima della foto della nuova Home (altrimenti l'iPhone mostrava il suo corsivo di sistema). Per tutta l'entrata non c'è la barra di scorrimento: sugli schermi grandi la sua fascia scura sotto il fumo sembrava un lato dritto; torna al primo scorrimento o tocco.
1. Le texture vengono decodificate prima (al massimo 1,5 s di attesa): la maschera non arriva a effetto iniziato.
2. La vecchia Home viene fotografata come gruppo `girrr-vecchia`. Nel callback della View Transition la skin si accende e si aspetta che il tema abbia riempito la Home (`nt-cruscotto-pronto`, al massimo 1,2 s). Intanto resta ferma la foto della vecchia Home. La nuova (`girrr-nuova`) quindi non si ricompone durante l'effetto: con la transizione attuale lo script del tema girava a metà animazione.
3. La maschera (nuvola o vento) non si sposta con `mask-position`, perché si ridisegnerebbe a ogni fotogramma. Si sposta la scatola mascherata con `transform` e la pagina vecchia al contrario della stessa quantità. Polvere e fumo sono strati vuoti con una texture di sfondo, animati sul loro gruppo. Risultato: solo `transform` e `opacity`, tutto sul compositor.
4. Alla fine si tolgono strati, classi e nomi. La prova controlla che non resti nulla sopra la pagina e che il centro dello schermo sia cliccabile.
5. Senza View Transitions (Safari prima della 18, browser vecchi) tutte le varianti usano il fumo, con un velo che nasconde il cambio. Con «Riduci movimento» il cambio è immediato.
6. Versione leggera automatica sopra i 3,5 milioni di pixel fisici (TV, 4K, iPad Pro): niente granelli, nel fumo due sbuffi su quattro.

Texture in `entrata-b/`, rigenerabili con `genera_texture.py` (seme fisso): `nuvola.webp` 43 KB, `nuvola-morbida.webp` 50 KB, `vento.webp` 42 KB, `polvere.webp` 41 KB, `fumo-a.webp` 47 KB, `fumo-b.webp` 52 KB. Nessuna libreria.

## Misure (Chromium 157 headless, senza GPU)
Prova: `node prove/v65/prova_transizioni_b.js misura [--cpu 4] [--motore webkit]`. Rapporti in `lab/transizioni-b/`.

- **Telefoni (320 e 390 px):** tutte le varianti a 54–60 fps, fotogramma mediano 16,7 ms e nessun long task durante l'effetto a CPU normale. Con la CPU 4 volte più lenta restano a 53–58 fps, con al massimo un long task di 50–56 ms. L'attuale con CPU 4× ha long task da 69 a 146 ms, perché lo script del tema gira durante l'animazione; nelle nuove varianti gira prima. Il fumo è la variante più pesante sul telefono (p95 33 ms su 390 px).
- **Ridisegni (traccia CDP, 1,5 s di effetto):** con `mask-position` 721 raster (170 ms) sul telefono e 1248 (461 ms) su PC. Con la maschera spostata via transform 15 (6 ms) e 52 (24 ms). È la prova che la tecnica F va fatta così.
- **iPad, PC e TV:** qui il rendering è software, quindi conta quanti pixel si compongono. Già l'attuale scende a circa 35 fps su PC e 23 sulla TV; le varianti con maschera e strati costano circa il doppio (iPad 25–30 fps, PC e TV 14–17 fps). In software `mask-position` va meglio solo perché lì comporre costa più che ridisegnare; su un dispositivo vero il conto si rovescia (vedi i ridisegni). Su una GPU vera comporre 3–5 strati a tutto schermo è un lavoro normale, ma **va provato su dispositivi veri**, soprattutto le smart TV, che hanno GPU deboli. Per questo c'è la versione leggera.
- **Fine pulita:** in ogni caso stato `completo`, zero strati rimasti, pagina cliccabile, nessuno scorrimento laterale, nessun errore in console.
- Video: fotogrammi disegnati dal browser uno per uno a 1/60 s (animazioni ferme e spostate), codificati a 60 fps. Mostrano la resa, non la fluidità.

**Non provati:** Safari su iPhone e iPad veri, Android vero, smart TV vera. WebKit di Playwright gira nel workflow `claude-65-transizioni-b-qa.yml` (Linux, rendering software), che non sostituisce Safari.

## Raccomandazione
1. **E · Nuvola e polvere**: è la più vicina alla sensazione richiesta («si dissolve come una nuvola di polvere morbida»). Le zone spariscono in momenti diversi, il bordo è granuloso e la skin è ferma sotto. Costa poco sul telefono.
2. **C · Fumo**: la più cinematografica e la più robusta. Serve comunque come ripiego senza View Transitions, ma copre di più la Home e somiglia meno a una «disgregazione».
3. **D · Polvere nel vento**: bella e dinamica, ma ha una direzione: è il rischio maggiore di ricordare uno swipe.

A non è scartata: è E senza polvere, utile se E sembra troppo «sporca». B con particelle vere è scartata per i costi (canvas e foto della pagina) ed è assorbita da E.
