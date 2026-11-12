#!/usr/bin/env python3
"""«Condividi la giornata» nella Home (Claude, 12 novembre 2026, versione 6.0).

La Home (Lega e Stadio) carica condividi.js, che mette il pulsante «Condividi la giornata» nel riquadro del Giornale,
accanto a «Leggi il giornale». Il Giornale lo carica già (lì il pulsante va accanto a «Condividi l'ultimo numero»).

Uso: python3 rilascio/condividi/applica.py CARTELLA_DEL_SITO
Scrive rilascio/condividi/pagine/girrr/index.html e rilascio/condividi/pagine/stadio/girrr/index.html.
"""
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
ANCORA = '<script src="{p}versioni.js" defer></script>'

def main(sito):
    for rel, p in (('girrr/index.html', '../'), ('stadio/girrr/index.html', '../../')):
        s = open(os.path.join(sito, rel), encoding='utf-8').read()
        tag = '<script src="%scondividi.js" defer></script>' % p
        if tag not in s:
            a = ANCORA.format(p=p)
            assert s.count(a) == 1, (rel, 'manca il punto dove aggiungere condividi.js')
            s = s.replace(a, a + '\n' + tag)
        out = os.path.join(QUI, 'pagine', rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(s)
        print('scritto', out)

if __name__ == '__main__':
    main(sys.argv[1])
