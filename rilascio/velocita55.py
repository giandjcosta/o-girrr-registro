"""Prima apertura più veloce delle pagine 5.5 (2 novembre 2026, richiesta di Gianluca: «la pagina rimane bianca 3-4 secondi la prima volta»).

Uso: python3 rilascio/velocita55.py CARTELLA   (una copia di gh-pages, oppure ufficiale/src/sito)
Per ogni pagina 5.5 di Lega (girrr/) e Stadio (stadio/girrr/):
  - colore di sfondo subito, prima di tutto il resto (niente schermo bianco mentre arrivano caratteri e fogli di stile);
    non nella Curva, che ha il suo tema chiaro o scuro;
  - collegamento anticipato ai server dei caratteri (preconnect);
  - foglio dei caratteri di Google non bloccante: la pagina appare subito e passa a Inter/Lobster appena arrivano;
  - attesa massima di Tabellone e Campo da 3 a 1,5 secondi.
Si può rilanciare: le pagine già sistemate non cambiano.
"""
import re, sys
from pathlib import Path

PAGINE = ('index.html', 'tabellone.html', 'campo.html', 'curva.html', 'notifiche.html', 'app.html')
SFONDO = {'girrr': '#1d2a52', 'stadio/girrr': '#141d3d'}
SEGNO = '<!-- 5.5: prima apertura veloce -->'


def sistema(t, sfondo):
    if SEGNO in t:
        return t, False
    testa = SEGNO + '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    if sfondo:
        testa += f'<style>html{{background-color:{sfondo}}}</style>'
    m = re.search(r'<meta charset="[^"]*">', t)
    if m:
        t = t[:m.end()] + testa + t[m.end():]
    else:
        t = t.replace('<head>', '<head>' + testa, 1)
    # caratteri di Google senza bloccare il disegno della pagina
    def font(m):
        href = m.group(1)
        return (f'<link rel="stylesheet" href="{href}" media="print" onload="this.media=\'all\'">'
                f'<noscript><link rel="stylesheet" href="{href}"></noscript>')
    t = re.sub(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/[^"]+)">', font, t)
    t = t.replace('document.documentElement.classList.remove("v55-attesa")},3000)', 'document.documentElement.classList.remove("v55-attesa")},1500)')
    return t, True


def main(cartella):
    base = Path(cartella)
    for d, colore in SFONDO.items():
        for f in PAGINE:
            p = base / d / f
            if not p.exists():
                continue
            t, cambiata = sistema(p.read_text(encoding='utf-8'), None if f == 'curva.html' else colore)
            if cambiata:
                p.write_text(t, encoding='utf-8')
            print(('sistemata ' if cambiata else 'già a posto ') + str(p.relative_to(base)))


if __name__ == '__main__':
    main(sys.argv[1])
