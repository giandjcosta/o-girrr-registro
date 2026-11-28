#!/usr/bin/env python3
"""Home: la partita da guardare, la classifica breve e i numeri della stagione nella grafica normale (Claude, 28 novembre 2026).
Novità della skin Notte Tropicale portate nella Home di Lega e Stadio, sotto «Oggi al Girrr» (decisioni di Gianluca del 24 e 28 novembre).

- girrr/home-cruscotto.js (da rilascio/r67/home-cruscotto.js);
- lo script incluso nella Home della Lega e in quella dello Stadio, dopo quello della settimana dei tifosi.
Uso: python3 rilascio/r67/applica.py CARTELLA_GH_PAGES   (idempotente: la seconda volta «File cambiati: 0»)
"""
import pathlib
import shutil
import sys

QUI = pathlib.Path(__file__).resolve().parent
PAGINE = {'girrr/index.html': ('<script src="v60/tifosi.js?v=622"></script>', 'home-cruscotto.js'),
          'stadio/girrr/index.html': ('<script src="../../girrr/v60/tifosi.js?v=622"></script>', '../../girrr/home-cruscotto.js')}


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    sito = pathlib.Path(argv[0]).resolve()
    cambiati = set()
    d = sito / 'girrr/home-cruscotto.js'
    if not d.exists() or d.read_bytes() != (QUI / 'home-cruscotto.js').read_bytes():
        shutil.copyfile(QUI / 'home-cruscotto.js', d); cambiati.add(str(d))
    for rel, (ancora, src) in PAGINE.items():
        f = sito / rel; t = f.read_text(encoding='utf-8')
        if 'home-cruscotto.js' in t:
            continue
        if t.count(ancora) != 1:
            raise SystemExit(rel + ': script della settimana dei tifosi non trovato una volta sola')
        t = t.replace(ancora, ancora + '\n<script src="' + src + '?v=67"></script>', 1)
        f.write_text(t, encoding='utf-8'); cambiati.add(str(f))
    print('File cambiati:', len(cambiati))


if __name__ == '__main__':
    main(sys.argv[1:])
