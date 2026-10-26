# Lazy loading Spogliatoio — Laboratorio (ChatGPT)

## Stato
La prova con **grafica Lega** si trova in `lab/prova-lazy-tabs-lega.html`, collegata da `lab/index.html`.
La demo usa dati simulati e lo stesso modulo `lab/spogliatoio-lazy.js` previsto per lo Spogliatoio. Non è una replica dei dati o dell'autenticazione reali.

## Problema della prima versione
Nel vero `o-fant-a-girrr/index.html` il codice è racchiuso in una IIFE:
`<script>(function(){ var D=...; ... function render(){...} ... })();</script>`.
Quindi uno script caricato **dopo** questa IIFE non vede `render`, `tab`, `D` e non li può intercettare. La precedente riga aggiunta prima di `assets/app.js` era inefficace.

## Nuova integrazione proposta, SOLO DOPO autorizzazione al rilascio
Non modificare `gh-pages` senza «Vai» esplicito. Preparare il nuovo file
`assets/spogliatoio-lazy.js` copiando **`lab/spogliatoio-lazy.js`** (non la vecchia versione Grok).

**Inserimento A:** in `index.html`, subito prima dello script inline che comincia
`<script>\n(function(){\nvar D=JSON.parse(document.getElementById('seed').textContent);`:

```html
<script src="assets/spogliatoio-lazy.js?v=3"></script>
```

**Inserimento B:** dentro *quella stessa IIFE*, immediatamente prima di `byHash();render();`:

```js
render = window.spgLazyWrap(render, function () {
  return {
    tab:tab, team:team, data:D, filter:filter, role:role, sortBy:sortBy,
    open:open,
    mkV:typeof mkV==='undefined'?'':mkV,
    mkT:typeof mkT==='undefined'?'':mkT,
    calComp:typeof calComp==='undefined'?'':calComp,
    calIdx:typeof calIdx==='undefined'?'':calIdx,
    authed:authed(),
    setTab:function(t){tab=t}
  };
});
```

Questa soluzione mantiene lo scope originale, la funzione `render` esistente, il seed JSON e `assets/app.js` invariati. Il wrapper diventa operativo anche durante il fetch successivo di `data.json` perché la variabile locale `render` viene riassegnata **prima** del primo `byHash();render()`.

## Cosa cambia
- Rosa e Giornata immediate.
- Scambi, Mercato, Svincolati, Sostituzioni, Borsino, Calendario e Statistiche: skeleton e costruzione dopo due `requestAnimationFrame`.
- Logout e click rapidi invalidano gli aggiornamenti in coda.
- La riassegnazione di `D` invalida la cache senza alterare `window.D`.
- Il gate originale e l'accesso a Statistiche (solo Oranje VC) sono preservati.

Non è un caricamento di dati a pacchetti: il calcolo pesante rimane sul thread principale; il doppio frame consente soltanto il primo paint dello skeleton.

## Controlli prima del rilascio
1. `node prove/prova_spogliatoio_lazy.js`.
2. Demo con grafica Lega, a 320 px e su Safari/iPhone; nessun errore in console.
3. Tab leggere/pesanti, click rapidi, logout/login, cambi filtro e dati; Statistiche solo Oranje VC.
4. Se si modifica `lab/index.html`: rigenerare `anteprima/` con `python3 anteprima/build.py`.
5. Solo dopo la certificazione e il «Vai» di Gianluca, applicare il piano al repository vero.
