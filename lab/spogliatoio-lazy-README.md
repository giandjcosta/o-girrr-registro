# Lazy loading Spogliatoio

## Già così nel sito vero
- Tab: si disegna **solo la tab attiva** (`vRosa`, `vDay`, …).
- **Borsino**: `borsino.json` si scarica al primo ingresso in tab.
- **Statistiche**: API GoatCounter al primo ingresso.

## Cosa aggiunge `spogliatoio-lazy.js`
Sulle tab pesanti (Scambi, Mercato, Svincolati, Sostituzioni, Borsino, Calendario, Statistiche):
1. click → aggiorna tab + skeleton «Carico…»
2. al frame successivo → `render` completo

Così l’interfaccia non “si blocca” mentre calcola liste lunghe.

## Prova nel Lab
https://giandjcosta.github.io/o-girrr-registro/lab/prova-lazy-tabs.html

## Applicare allo Spogliatoio vero (`index.html`)
Subito **dopo** lo `</script>` principale (quello con `function render`), **prima** di `assets/app.js`:

```html
<script src="girrr/spogliatoio-lazy.js?v=1"></script>
```

(oppure il path relativo giusto se il file sta in `assets/`).

Copiare `lab/spogliatoio-lazy.js` in `o-fant-a-girrr` (es. `assets/spogliatoio-lazy.js` o `girrr/spogliatoio-lazy.js`).

Solo dopo prova in Lab/Anteprima e «vai» di Gianluca.
