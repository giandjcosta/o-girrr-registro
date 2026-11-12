#!/usr/bin/env python3
"""Scrive curva-os.css da curva-os.src.css mettendo al posto di @@MOLLE@@ le molle calcolate da molle.py.
Uso: python3 rilascio/curva-os/costruisci.py"""
import os
import sys

qui = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, qui)
import molle  # noqa: E402

righe = []
for nome, z, k in molle.MOLLE:
    p, d = molle.simula(z, k)
    massimo = max(x for _, x in p)
    righe.append('  --%s:%s;' % (nome, molle.lineare(p, d)))
    righe.append("  --%s-durata:%dms;  /* smorzamento %.2f, rigidità %d, supera l'arrivo del %.0f%% */" % (nome, round(d * 1000), z, k, max(0, (massimo - 1) * 100)))
src = open(os.path.join(qui, 'curva-os.src.css'), encoding='utf-8').read()
assert '@@MOLLE@@' in src
open(os.path.join(qui, 'curva-os.css'), 'w', encoding='utf-8').write(src.replace('@@MOLLE@@', '\n'.join(righe)))
print('curva-os.css scritto')
