#!/usr/bin/env python3
"""Texture della transizione B (studio 6.5, Claude, 18 novembre 2026). Rieseguibile, risultato identico (seme fisso).

Rumore frattale fatto con la FFT: è periodico, quindi le maschere si ripetono senza cuciture (mask-repeat).
- nuvola.webp       E · Nuvola e polvere: maschera alfa 1:3, la dissoluzione scende dall'alto, bordi nuvolosi con grana di polvere.
- nuvola-morbida.webp  A · Nuvola morbida: come sopra, senza grana.
- vento.webp        D · Polvere nel vento: maschera alfa 3:1, scie orizzontali, da sinistra a destra.
- polvere.webp      granelli luminosi (RGBA), decorazione che accompagna il fronte.
- fumo-a.webp, fumo-b.webp  C · Fumo: sbuffi morbidi (RGBA) lilla e rosa.
Uso: python3 temi/notte-tropicale/entrata-b/genera_texture.py
"""
import pathlib
import numpy as np
from PIL import Image

D = pathlib.Path(__file__).resolve().parent
rng = np.random.default_rng(65)


def fbm(h, w, beta=2.2, aniso=(1.0, 1.0), lo=2.0):
    """Rumore 1/f^beta periodico, normalizzato 0..1. aniso allunga le strutture (scie)."""
    fy = np.fft.fftfreq(h)[:, None] * h / aniso[0]
    fx = np.fft.fftfreq(w)[None, :] * w / aniso[1]
    f = np.sqrt(fx * fx + fy * fy)
    f[0, 0] = 1
    amp = 1 / f ** (beta / 2)
    amp[f < lo] *= (f[f < lo] / lo) ** 2  # niente macchie grandi quanto tutta la texture
    amp[0, 0] = 0
    ph = np.exp(2j * np.pi * rng.random((h, w)))
    n = np.real(np.fft.ifft2(amp * ph))
    return (n - n.min()) / (n.max() - n.min())


def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def salva_alfa(alpha, nome, q=82):
    a = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    rgba = np.dstack([np.full_like(a, 255)] * 3 + [a])
    Image.fromarray(rgba, 'RGBA').save(D / nome, 'WEBP', quality=q, method=6)


def maschera_sweep(lungo, corto, verticale, grana, aniso, nome, soft=0.07, amp=0.75):
    """Texture lunga 3 volte: un terzo pieno (pagina visibile), il terzo centrale con il fronte irregolare, un terzo vuoto."""
    h, w = (lungo, corto) if verticale else (corto, lungo)
    n = fbm(h, w, beta=3.0, aniso=aniso, lo=1.0)
    fine = fbm(h, w, beta=1.0, lo=1.0)  # grana di polvere
    pos = (np.arange(lungo) / (lungo - 1))
    ramp = np.clip((pos - 0.20) / 0.60, 0, 1)  # 0 in alto/sinistra (dissolto), 1 in basso/destra (pagina)
    ramp = ramp[:, None] if verticale else ramp[None, :]
    f = ramp + amp * (n - 0.5) * 2 * np.minimum(1, 4 * ramp * (1 - ramp) + .15)
    if grana:
        f = f + 0.16 * (fine - 0.5) * 2
    alpha = smooth(0.5 - soft, 0.5 + soft, f)
    # estremi garantiti: nessun granello sopravvive fuori dal terzo centrale
    m = np.clip((pos - 0.06) / 0.06, 0, 1) * np.clip((0.94 - pos) / 0.06, 0, 1)
    m = m[:, None] if verticale else m[None, :]
    full = (pos > 0.5).astype(float)
    full = full[:, None] if verticale else full[None, :]
    alpha = alpha * m + full * (1 - m)
    salva_alfa(alpha, nome)


def polvere(size=512, n=900):
    img = np.zeros((size, size, 4))
    yy, xx = np.mgrid[0:size, 0:size]
    cols = np.array([[255, 236, 248], [255, 190, 225], [170, 240, 255], [255, 214, 160]]) / 255
    for _ in range(n):
        x, y = rng.random(2) * size
        r = rng.choice([0.6, 0.9, 1.3, 2.0], p=[.45, .3, .18, .07])
        a = rng.uniform(.35, 1)
        c = cols[rng.integers(len(cols))]
        x0, x1, y0, y1 = int(x - 6), int(x + 7), int(y - 6), int(y + 7)
        for dy in range(y0, y1):
            for dx in range(x0, x1):
                d2 = (dx - x) ** 2 + (dy - y) ** 2
                g = a * np.exp(-d2 / (2 * r * r))
                if g < .01:
                    continue
                py, px = dy % size, dx % size
                old = img[py, px, 3]
                na = old + g * (1 - old)
                img[py, px, :3] = (img[py, px, :3] * old + c * g * (1 - old)) / max(na, 1e-6)
                img[py, px, 3] = na
    Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8), 'RGBA').save(D / 'polvere.webp', 'WEBP', quality=85, method=6)


def fumo(nome, colore, size=384, seme_lo=1.0):
    n = fbm(size, size, beta=3.2, lo=seme_lo)
    n2 = fbm(size, size, beta=2.4, lo=2)
    yy, xx = np.mgrid[0:size, 0:size] / (size - 1) - 0.5
    r = np.sqrt(xx ** 2 + yy ** 2) * 2
    fall = smooth(1.0, 0.25, r)
    a = smooth(0.25, 0.8, n * 0.75 + n2 * 0.25) * fall
    a = np.clip(a * 1.15, 0, 0.9)
    c = np.array(colore) / 255
    tint = (c[None, None, :] * (0.82 + 0.18 * n[..., None]))
    rgba = np.dstack([tint, a[..., None]])
    Image.fromarray((np.clip(rgba, 0, 1) * 255).astype(np.uint8), 'RGBA').save(D / nome, 'WEBP', quality=72, method=6)


if __name__ == '__main__':
    maschera_sweep(1152, 384, True, True, (1.0, 1.0), 'nuvola.webp', soft=0.09, amp=0.75)
    maschera_sweep(1152, 384, True, False, (1.0, 1.0), 'nuvola-morbida.webp', soft=0.16, amp=0.75)
    maschera_sweep(1152, 384, False, True, (1.0, 14.0), 'vento.webp', soft=0.06, amp=0.6)
    if not (D / 'polvere.webp').exists():
        polvere()
    fumo('fumo-a.webp', (242, 228, 255))
    fumo('fumo-b.webp', (255, 214, 236), seme_lo=2.5)
    for p in sorted(D.glob('*.webp')):
        print(p.name, p.stat().st_size // 1024, 'KB')
