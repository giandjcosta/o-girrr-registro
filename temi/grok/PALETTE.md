# Notte tropicale · Colori e caratteri di riferimento

17 novembre 2026 · Grok · solo nel registro di prova. Non è integrato nel Lab, non è sul sito vero, non aspetta un numero di versione.

Gianluca ha chiesto i colori e i caratteri del marchio del capitolo VI, e la lettura delle sue sfumature. Qui c'è quella lettura, tradotta in campioni che O Girrr può usare senza copiare il logo e senza portare nel progetto un carattere commerciale.

## Cosa è ufficiale e cosa no

Rockstar non ha pubblicato una guida con i codici colore. I numeri di questa pagina sono **campioni** letti da una ricostruzione pubblica del marchio del 2023 (un SVG su Wikimedia Commons, non un file uscito da Rockstar). Servono a capire la luce del tramonto. Non sono un marchio nostro e non vanno ridisegnati come il numero VI.

## Due versioni del marchio

### 2023 · Trailer del 5 dicembre

- La scritta della serie resta bianca, con il contorno pesante di sempre.
- Il numero è un **disegno**, non una riga di testo: dentro ci sono le palme in controluce.
- Il riempimento è una sfumatura **verticale**: blu in alto, magenta al centro, arancio in basso.
- Anche il **contorno** del numero era sfumato: oro e rosa in alto, viola scuro in basso.

### 2026 · 18 giugno, copertina e preordini

- L'interno non cambia: palme e la stessa fascia di tramonto.
- Il contorno del numero diventa **bianco pieno**. Sul nero si legge meglio. La sfumatura del contorno del 2023 non si usa più.
- Il numero è più grande e sta **dietro** la scritta, che diventa più piccola.
- Questa descrizione viene dai resoconti pubblici del 18–20 giugno 2026. Il file ufficiale del 2026 non è stato ricampionato qui: il bianco del contorno nuovo è `#FFFFFF`.

## Sfumatura del riempimento

Direzione: dall'alto in basso, lineare. Niente sfumatura radiale. Il blu è il cielo, il magenta è la fascia di neon, l'arancio è il sole basso.

Due campioni dello stesso passaggio, letti su due forme diverse del file. Il primo è quello da usare come riferimento.

| Punto | Campione A · da usare | Campione B |
|---|---|---|
| Alto · 0% | `#2B60DA` | `#2E49BF` |
| Centro | `#FF4CB9` a metà | `#C045B6` al 49% |
| Basso · 100% | `#E6953E` | `#DF7B4D` |

In CSS, il campione A:

```css
linear-gradient(to bottom, #2B60DA 0%, #FF4CB9 50%, #E6953E 100%)
```

Il campione B è più smorzato, utile se il magenta pieno stanca su un riquadro di testo:

```css
linear-gradient(to bottom, #2E49BF 0%, #C045B6 49%, #DF7B4D 100%)
```

## Sfumatura del contorno del 2023

Sempre verticale, dall'alto in basso. Nel 2026 questo contorno è sostituito da un filo bianco.

| Punto | Colore |
|---|---|
| 0% · alto | `#FFBC24` |
| 29% | `#FF49B9` |
| 75% | `#BC0082` |
| 94% | `#8B0179` |
| 100% · basso | `#6D016D` |

## Viola di profondità

Dietro le palme il cielo non è il blu acceso del riempimento. È un viola notte, da `#350054` a `#6D016D`. È il colore giusto per il fondo di una scheda, non per un titolo.

## Come li useremmo noi

Il brief già aperto da ChatGPT (`temi/VICE-CITY-BRIEF.md`, ramo `chatgpt/theme-engine-vice-city-event`) ha una palette più morbida. Non la sostituisco. La accosto, così si vede lo scarto.

| Ruolo | Campione del marchio | Già scelto nel brief |
|---|---|---|
| Cielo | `#2B60DA` | turchese `#67D6CF` |
| Neon | `#FF4CB9` | rosa `#FF91BB` e `#EE6599` |
| Sole | `#E6953E` | pesca `#FFB878` |
| Notte | `#350054` | indaco `#25214A` |
| Testo sul fondo scuro | `#FFF4ED` | `#FFF4ED` |
| Filo del 2026 | `#FFFFFF` | bordo rosa trasparente |

Regole che restano, da `AGENTS.md`:

- La **Lega** tiene il rosso `#D62839` e la Champions Cup azzurra.
- Lo **Stadio** tiene l'oro `#FFD166`, anche in Champions Cup.
- La Notte tropicale, se si accende, è un velo sopra. Spento, le due grafiche tornano com'erano.
- Niente animazione continua sopra i risultati. `prefers-reduced-motion` va rispettato.
- Nome e disegno originali. Niente logo, niente caratteri del marchio, niente scritta «Vice City» nella grafica che vedono i giocatori.

I token pronti da copiare sono in `palette.css`. Non c'è una pagina e non c'è un'app: non sono collegati al Lab. ChatGPT e Claude stanno già sul tema, e non sovrappongo il loro lavoro.

## Caratteri

### Quelli del marchio

- La scritta della serie, da GTA III in poi, è **Pricedown** di Ray Larabie (Typodermic): nero, bianco, contorno. Rockstar non ha pubblicato l'elenco dei caratteri di questo capitolo. Il nero si scarica gratis per usarlo sul proprio computer. Il file non si può copiare in un repository né nel sito: lo vieta la licenza desktop di Typodermic del 17 agosto 2026. Istruzioni per Claude in `CARATTERI.md`.
- Il numero **non è un font**. È un disegno con le palme. Alcuni siti parlano di un carattere «Art Deco» per quel numero: Rockstar non lo ha confermato, e nel marchio quelle due lettere non sono testo. Non lo usiamo.

### Quelli che richiamano il gioco e si possono usare

- Nello **Stadio** il corsivo da insegna c'è già: Lobster. Resta quello.
- I titoli della Notte tropicale usano il carattere già della pagina, **riempito** con la sfumatura verticale. Nessun font nuovo da scaricare, e la pagina funziona anche offline.
- Un sans nero da manifesto (per esempio Bebas Neue, licenza OFL) ricorda solo il peso, non la forma storta di Pricedown. Non è caricato in questa prova.

## Cosa non c'è in questa cartella

Niente logo, niente file di font a pagamento, niente modifica a `tv.js` o al sito, niente Supabase. Per andare online serve il «Vai» di Gianluca, e prima la prova nel Lab insieme al tema già aperto.
