# Infinite scroll Curva (in corso)

Intenzione: mostrare 20 post alla volta e caricarne altri 20 allo scroll.

Il patch completo è pronto in locale (`curva_patched.html`) ma il file `curva.html` è molto grande (~155 KB).

Modifiche previste in `ufficiale/src/sito/girrr/curva.html` (e copie Stadio):
1. Variabile `FEED_SHOW=20`
2. Home: `feed(L.slice(0,FEED_SHOW))` + indicatore `#piu-feed`
3. Listener scroll che aumenta `FEED_SHOW` di 20 e chiama `renderFermo()`
4. Reset `FEED_SHOW=20` al cambio filtro e al refresh home

Niente modifiche al database (niente "vai" SQL).
