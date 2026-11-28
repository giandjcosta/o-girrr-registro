#!/usr/bin/env python3
"""Skin «Inverno» (Claude, 28 novembre 2026): disegna le quattro scene di sfondo (SVG originali, niente foto né marchi).
Stadio di notte con i fari, neve, abeti ai lati; cambiano cielo e dettagli: premium (navy, ghiaccio, stelle oro),
natale (abeti con le luci, nastri berry), capodanno (fuochi d'artificio oro e lavanda, 2027), wonderland (aurora, ghiaccio).
Uso: python3 temi/inverno/scena.py  → scrive inverno-<atmosfera>.svg accanto a questo file."""
import math, pathlib, random

QUI = pathlib.Path(__file__).resolve().parent
W, H = 1600, 1000

ATM = {
    'premium':    dict(cielo=('#070d1f', '#111b38', '#1d2d55', '#304779'), stelle='#d6b66f', neve='#edf5fc', fari='#eaf3fc', abete='#0e1a33', luci=None),
    'natale':     dict(cielo=('#06101a', '#0f1f33', '#17234a', '#1f3b4d'), stelle='#d5b66e', neve='#f5f0e7', fari='#fff3d6', abete='#103a2c', luci=('#d52c43', '#d5b66e', '#f5f0e7')),
    'capodanno':  dict(cielo=('#070a17', '#101629', '#221f45', '#302d59'), stelle='#d8b96e', neve='#f3e9d5', fari='#f3e9d5', abete='#141530', luci=None),
    'wonderland': dict(cielo=('#0d2340', '#1b3f6b', '#3c6f9e', '#8fc1e3'), stelle='#ffffff', neve='#ffffff', fari='#ffffff', abete='#1e4466', luci=None),
}


def abete(x, base, h, col, neve, luci, rnd):
    w = h * .42; s = []
    for i in range(4):   # quattro piani di rami, dal basso
        y0 = base - h * (.12 + i * .2); y1 = y0 - h * .38; ww = w * (1 - i * .2)
        s.append('<path d="M%.0f %.0fL%.0f %.0fL%.0f %.0fZ" fill="%s"/>' % (x - ww / 2, y0, x, y1, x + ww / 2, y0, col))
        s.append('<path d="M%.0f %.0fQ%.0f %.0f %.0f %.0fL%.0f %.0fZ" fill="%s" opacity=".9"/>' % (x - ww * .3, y1 + h * .2, x, y1 + h * .12, x + ww * .3, y1 + h * .2, x, y1, neve))
    s.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>' % (x - h * .03, base - h * .12, h * .06, h * .12, '#0b1222'))
    if luci:
        for _ in range(int(h / 14)):
            t = rnd.random(); yy = base - h * .14 - t * h * .7; half = w * (1 - t) * .42
            s.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s"/>' % (x + rnd.uniform(-half, half), yy, rnd.uniform(2.2, 3.6), rnd.choice(luci)))
        s.append('<path d="M%.0f %.0fl6 13 14 2-10 10 3 14-13-7-13 7 3-14-10-10 14-2z" fill="%s"/>' % (x, base - h * 1.02 - 13, '#d5b66e'))
    return ''.join(s)


def scena(nome, a):
    rnd = random.Random(2027)
    c = a['cielo']
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMax slice">' % (W, H),
         '<defs><linearGradient id="c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset=".45" stop-color="%s"/><stop offset=".75" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % c,
         '<radialGradient id="f" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="%s" stop-opacity=".95"/><stop offset=".25" stop-color="%s" stop-opacity=".35"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (a['fari'], a['fari'], a['fari']),
         '<linearGradient id="n" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="#9ccbea"/></linearGradient>' % a['neve'],
         '<linearGradient id="a" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7fffd4" stop-opacity="0"/><stop offset=".3" stop-color="#7fffd4" stop-opacity=".35"/><stop offset=".6" stop-color="#9ccbea" stop-opacity=".45"/><stop offset="1" stop-color="#b6a6ff" stop-opacity="0"/></linearGradient></defs>',
         '<rect width="%d" height="%d" fill="url(#c)"/>' % (W, H)]
    for _ in range(120):   # stelle
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * .55), rnd.choice((0.8, 1, 1.2, 1.6, 2.2))
        s.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>' % (x, y, r, a['stelle'] if r > 1.5 else a['neve'], rnd.uniform(.35, .95)))
    for _ in range(9):     # stelle grandi a quattro punte
        x, y, r = rnd.uniform(60, W - 60), rnd.uniform(30, H * .4), rnd.uniform(6, 13)
        s.append('<path d="M%.0f %.0fQ%.1f %.1f %.0f %.0fQ%.1f %.1f %.0f %.0fQ%.1f %.1f %.0f %.0fQ%.1f %.1f %.0f %.0fZ" fill="%s" opacity=".9"/>' % (
            x, y - r, x + r * .15, y - r * .15, x + r, y, x + r * .15, y + r * .15, x, y + r, x - r * .15, y + r * .15, x - r, y, x - r * .15, y - r * .15, x, y - r, a['stelle']))
    if nome == 'wonderland':
        s.append('<path d="M0 260C300 140 520 330 820 210S1300 120 1600 240V330C1300 220 1100 330 820 300S300 250 0 360Z" fill="url(#a)"/>')
        s.append('<path d="M0 180C340 80 600 250 900 140S1350 60 1600 160V210C1350 130 1100 230 900 200S320 160 0 240Z" fill="url(#a)" opacity=".6"/>')
    if nome == 'premium' or nome == 'natale':   # luna
        s.append('<circle cx="1300" cy="170" r="54" fill="%s" opacity=".92"/><circle cx="1324" cy="156" r="50" fill="%s"/>' % (a['neve'], c[0]))
    if nome == 'capodanno':   # fuochi d'artificio
        for (x, y, r, col) in ((330, 210, 120, '#d8b96e'), (1240, 170, 140, '#7968b7'), (820, 120, 90, '#f3e9d5'), (1480, 340, 70, '#d8b96e'), (120, 380, 60, '#7968b7')):
            for k in range(22):
                an = k / 22 * math.tau; x1, y1 = x + math.cos(an) * r * .25, y + math.sin(an) * r * .25; x2, y2 = x + math.cos(an) * r, y + math.sin(an) * r
                s.append('<path d="M%.0f %.0fL%.0f %.0f" stroke="%s" stroke-width="3" stroke-linecap="round" opacity=".85"/>' % (x1, y1, x2, y2, col))
                s.append('<circle cx="%.0f" cy="%.0f" r="3.5" fill="%s"/>' % (x2, y2, col))
        s.append('<text x="800" y="420" text-anchor="middle" font-family="Georgia,serif" font-size="150" font-weight="700" fill="none" stroke="#d8b96e" stroke-width="2.5" opacity=".55" letter-spacing="18">2027</text>')
    # colline innevate lontane
    s.append('<path d="M0 690C220 640 420 660 640 630S1080 610 1300 640 1500 660 1600 650V1000H0Z" fill="%s" opacity=".22"/>' % a['neve'])
    # stadio: tribune ovali con i fari
    s.append('<g transform="translate(800 705)">')
    s.append('<ellipse rx="430" ry="118" fill="#0b1324"/><ellipse rx="430" ry="118" fill="none" stroke="%s" stroke-opacity=".5" stroke-width="3"/>' % a['fari'])
    s.append('<ellipse cy="-30" rx="380" ry="80" fill="#162545"/>')
    for k in range(60):   # luci delle tribune
        an = math.pi + k / 59 * math.pi
        s.append('<circle cx="%.0f" cy="%.0f" r="2.4" fill="%s" opacity=".75"/>' % (math.cos(an) * 405, math.sin(an) * 100 - 10, a['fari']))
    s.append('<ellipse cy="-18" rx="300" ry="52" fill="url(#n)" opacity=".95"/>')   # campo innevato
    s.append('<ellipse cy="-18" rx="300" ry="52" fill="none" stroke="#ffffff" stroke-opacity=".5" stroke-width="2"/><path d="M0 -70V34" stroke="#ffffff" stroke-opacity=".45" stroke-width="2"/><ellipse cy="-18" rx="44" ry="14" fill="none" stroke="#ffffff" stroke-opacity=".45" stroke-width="2"/>')
    for fx in (-470, 470):   # torri dei fari
        s.append('<path d="M%d 40V-250" stroke="#0b1324" stroke-width="10"/><rect x="%d" y="-290" width="80" height="40" rx="6" fill="%s"/>' % (fx, fx - 40, a['fari']))
        s.append('<ellipse cx="%d" cy="-270" rx="190" ry="150" fill="url(#f)"/>' % fx)
    s.append('</g>')
    # neve in primo piano
    s.append('<path d="M0 820C260 770 520 800 800 790S1340 760 1600 800V1000H0Z" fill="url(#n)"/>')
    s.append('<path d="M0 880C300 850 560 900 820 880S1340 860 1600 890V1000H0Z" fill="%s" opacity=".9"/>' % a['neve'])
    # abeti ai lati
    for x, base, h in ((60, 900, 360), (190, 880, 270), (300, 860, 190), (1540, 900, 380), (1410, 885, 280), (1300, 865, 200)):
        s.append(abete(x, base, h, a['abete'], a['neve'], a['luci'], rnd))
    if nome == 'natale':   # festone di luci in alto
        s.append('<path d="M0 40Q200 120 400 40T800 40T1200 40T1600 40" fill="none" stroke="#103a2c" stroke-width="4"/>')
        for k in range(33):
            x = k * 50; y = 40 + 40 * abs(math.sin(math.pi * x / 400))
            s.append('<circle cx="%d" cy="%.0f" r="7" fill="%s"/>' % (x, y + 6, ('#d52c43', '#d5b66e', '#f5f0e7')[k % 3]))
    s.append('</svg>')
    (QUI / ('inverno-%s.svg' % nome)).write_text(''.join(s), encoding='utf-8')


if __name__ == '__main__':
    for k, v in ATM.items():
        scena(k, v)
    print('Scene scritte:', ', '.join(ATM))
