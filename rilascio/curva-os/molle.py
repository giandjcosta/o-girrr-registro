#!/usr/bin/env python3
"""Molle della Curva per iPhone e Android (Claude, 12 novembre 2026).

iOS e Android animano con molle fisiche (rigidità e smorzamento), non con curve fisse. Nel CSS una molla si scrive
con la funzione linear(): questo script simula ogni molla e stampa le variabili da incollare in curva-os.css
(curva e durata). Uso: python3 rilascio/curva-os/molle.py

iPhone: le molle di SwiftUI, descritte con «durata percepita» e «rimbalzo» (.smooth, .snappy, .bouncy):
  rigidità = (2π / durata)², smorzamento = 1 − rimbalzo.
Android: le molle di Material 3 Expressive (rapporto di smorzamento e rigidità): «spaziali» per i movimenti,
  un po' rimbalzanti; «effetti» per colori e trasparenze, senza rimbalzo.
"""
import math

MOLLE = [
    # nome, smorzamento (rapporto), rigidità
    ('ios-morbida', 1.0, (2 * math.pi / .5) ** 2),   # .smooth: niente rimbalzo
    ('ios-scattante', .85, (2 * math.pi / .5) ** 2), # .snappy: rimbalzo 0,15
    ('ios-elastica', .7, (2 * math.pi / .5) ** 2),   # .bouncy: rimbalzo 0,3
    ('ios-veloce', .9, (2 * math.pi / .3) ** 2),     # tocchi: rapida, appena elastica
    ('m3-spaziale-veloce', .6, 800),
    ('m3-spaziale', .8, 380),
    ('m3-spaziale-lenta', .8, 200),
    ('m3-effetti-veloce', 1.0, 3800),
    ('m3-effetti', 1.0, 1600),
]


def simula(z, k, dt=.0005, soglia=.002):
    c = 2 * z * math.sqrt(k)
    x = v = t = 0.0
    punti = [(0.0, 0.0)]
    fermo = 0.0
    while t < 3:
        a = -k * (x - 1) - c * v
        v += a * dt
        x += v * dt
        t += dt
        punti.append((t, x))
        if abs(x - 1) < soglia and abs(v) < .05:
            fermo += dt
            if fermo > .03:
                break
        else:
            fermo = 0.0
    return punti, t


def lineare(punti, durata, n=40):
    out = []
    j = 0
    for i in range(n + 1):
        tt = durata * i / n
        while j < len(punti) - 1 and punti[j + 1][0] < tt:
            j += 1
        out.append(punti[j][1])
    out[-1] = 1.0
    return 'linear(' + ','.join(('%.3f' % x).rstrip('0').rstrip('.') if x not in (0, 1) else str(int(x)) for x in out) + ')'


if __name__ == '__main__':
    for nome, z, k in MOLLE:
        p, d = simula(z, k)
        massimo = max(x for _, x in p)
        print('  --%s:%s;' % (nome, lineare(p, d)))
        print('  --%s-durata:%dms;  /* smorzamento %.2f, rigidità %d, supera l\'arrivo del %.0f%% */' % (nome, round(d * 1000), z, k, max(0, (massimo - 1) * 100)))
