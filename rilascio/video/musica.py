#!/usr/bin/env python3
"""Musica di sottofondo del video della giornata (Claude, 12 novembre 2026).

Musica originale, generata qui con numpy: nessun servizio a pagamento, nessun brano di altri, nessun diritto da chiedere.
Va a tempo con le scene del video (scene.json scritto da remotion/render.mjs):
- apertura col logo della lega: colpo e accordo, poi sale verso i risultati;
- Campionato: ritmo da sigla sportiva (cassa dritta, basso, accordi) in La minore;
- podio: rullo di tamburo mentre salgono i gradini e piatto quando arrivano;
- Champions Cup: stacco, colpo sul logo della coppa, stesso ritmo ma un tono più su e con l'arpeggio di campanelle;
- «Da non perdere» (se c'è): torna il tema del Campionato;
- «Tutto su O Girrr»: accordo finale maggiore che sfuma.
Un fruscio accompagna ogni tendina tra le scene.

Uso: python3 rilascio/video/musica.py scene.json VIDEO_MUTO.mp4 VIDEO_CON_MUSICA.mp4
"""
import json
import subprocess
import sys
import tempfile
import wave

import numpy as np

SR = 44100
BPM = 124
BEAT = 60 / BPM
rng = np.random.default_rng(7)


def nota(n):  # numero MIDI -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n, a, d):  # attacco e decadimento esponenziale
    t = np.arange(n) / SR
    e = np.exp(-t / d)
    k = max(1, int(a * SR))
    e[:k] *= np.linspace(0, 1, k)
    return e


def sega(f, n, arm=8, stonato=0.0):  # dente di sega «morbido» (poche armoniche)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for h in range(1, arm + 1):
        s += np.sin(2 * np.pi * f * h * (1 + stonato) * t) / h
    return s


def passa_basso(x, a):  # filtro a un polo, a tra 0 e 1 (più basso = più cupo)
    y = np.empty_like(x)
    p = 0.0
    for i, v in enumerate(x):
        p += a * (v - p)
        y[i] = p
    return y


def cassa(forte=1.0, lunga=0.32, f0=150, f1=45):
    n = int(lunga * 1.4 * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.035)
    return forte * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, lunga / 2.5)


def rullante(forte=1.0):
    n = int(0.22 * SR)
    r = np.diff(rng.standard_normal(n + 1)) * 0.5 * env(n, 0.001, 0.05)
    t = np.arange(n) / SR
    return forte * (r + 0.5 * np.sin(2 * np.pi * 190 * t) * env(n, 0.001, 0.03))


def charleston(forte=1.0):
    n = int(0.06 * SR)
    r = np.diff(np.diff(rng.standard_normal(n + 2))) * 0.25
    return forte * r * env(n, 0.0005, 0.015)


def piatto(forte=1.0, lungo=1.8):
    n = int(lungo * SR)
    r = np.diff(np.diff(rng.standard_normal(n + 2))) * 0.22
    return forte * r * env(n, 0.002, lungo / 4)


def colpo(forte=1.0):  # impatto: cassa profonda, rumore e piatto
    a = cassa(1.0, 1.1, 120, 32)
    b = passa_basso(rng.standard_normal(int(0.5 * SR)), 0.08) * env(int(0.5 * SR), 0.001, 0.12) * 0.9
    c = piatto(0.8, 2.2)
    out = np.zeros(max(len(a), len(b), len(c)))
    out[:len(a)] += a
    out[:len(b)] += b
    out[:len(c)] += c
    return forte * out


def fruscio(lungo=0.55):  # sale e si ferma sul cambio di scena
    n = int(lungo * SR)
    x = rng.standard_normal(n)
    y = np.empty(n)
    p = 0.0
    for i in range(n):
        a = 0.02 + 0.5 * (i / n) ** 2
        p += a * (x[i] - p)
        y[i] = p
    return y * np.linspace(0, 1, n) ** 2 * 0.55


def accordo(note, durata, forte=0.12, attacco=0.25, arm=7):
    n = int(durata * SR)
    s = np.zeros(n)
    for m in note:
        for st in (-0.003, 0.003):
            s += sega(nota(m), n, arm, st)
    s = passa_basso(s, 0.18)
    e = np.minimum(1, np.arange(n) / (attacco * SR)) * np.minimum(1, (n - np.arange(n)) / (0.08 * SR))
    return forte * s * e / len(note)


def campanella(m, forte=0.1):
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * nota(m) * t) + 0.3 * np.sin(2 * np.pi * nota(m) * 2.01 * t)
    return forte * s * env(n, 0.002, 0.12)


def metti(buf, x, t):
    i = int(t * SR)
    if i >= len(buf) or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    k = min(len(x), len(buf) - i)
    buf[i:i + k] += x[:k]


# accordi (fondamentale del basso, note dell'accordo): La minore i-VI-III-VII; la Coppa un tono sopra (Si minore)
LEGA = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]
COPPA = [(47, [59, 62, 66]), (43, [59, 62, 67]), (50, [57, 62, 66]), (45, [57, 61, 64])]


def base(buf, da, a, prog, coppa=False, densa=True):
    """Ritmo della sigla da da ad a (secondi), battute allineate a da."""
    batt = 4 * BEAT
    i = 0
    t = da
    while t < a - 0.05:
        rad, acc = prog[i % len(prog)]
        lb = min(batt, a - t)
        metti(buf, accordo(acc, lb, 0.10 if densa else 0.13), t)
        for b in range(4):
            tb = t + b * BEAT
            if tb >= a - 0.02:
                break
            metti(buf, cassa(0.9), tb)
            metti(buf, charleston(0.5), tb + BEAT / 2)
            if densa and b in (1, 3):
                metti(buf, rullante(0.45), tb)
            for c in range(2):  # basso a crome che «pompa» con la cassa
                tc = tb + c * BEAT / 2
                n = int(BEAT / 2 * SR * 0.9)
                bs = sega(nota(rad + (12 if c == 1 and b == 3 else 0)), n, 6) * env(n, 0.004, 0.16) * 0.22
                metti(buf, bs, tc)
            if coppa:
                arp = acc + [acc[0] + 12]
                for s in range(4):
                    metti(buf, campanella(arp[(b * 4 + s) % 4] + 12, 0.06), tb + s * BEAT / 4)
        t += batt
        i += 1


def componi(scene, fps):
    ini, t = {}, 0.0
    for k, d in scene:
        ini[k] = (t, t + d / fps)
        t += d / fps
    tot = t + 0.2
    buf = np.zeros(int(tot * SR) + SR * 3)
    # apertura: colpo sul logo, accordo che regge e sale verso i risultati
    a0, a1 = ini['introLega']
    metti(buf, colpo(0.9), 0.05)
    metti(buf, accordo(LEGA[0][1] + [45], a1 - 0.1, 0.16, 0.05), 0.05)
    # Campionato: dai risultati alla classifica
    fine_lega = ini['classifica'][1]
    base(buf, a1, fine_lega, LEGA)
    # podio: rullo mentre salgono i gradini, piatto all'arrivo
    p0 = ini['podio'][0]
    k = 0
    while k < 28:
        tt = p0 + 0.05 + k * (0.9 / 28) + (k / 28) ** 2 * 0.2
        metti(buf, rullante(0.18 + 0.4 * k / 28), tt)
        k += 1
    metti(buf, piatto(0.9, 2.0), p0 + 1.2)
    # Coppa: stacco, colpo sul logo della coppa, poi lo stesso ritmo un tono sopra con le campanelle
    c0, c1 = ini['introCoppa']
    metti(buf, colpo(0.95), c0)
    metti(buf, accordo(COPPA[0][1] + [47], c1 - c0, 0.15, 0.05), c0)
    for s in range(8):
        metti(buf, campanella(COPPA[0][1][s % 3] + 24, 0.05), c0 + 0.6 + s * BEAT / 2)
    fine_coppa = ini['gironi'][1]
    base(buf, c1, fine_coppa, COPPA, coppa=True)
    # Da non perdere (se c'è): torna il Campionato, un po' più leggero
    if 'prossime' in ini:
        q0, q1 = ini['prossime']
        base(buf, q0, q1, LEGA, densa=False)
    # fine: accordo maggiore (La maggiore) che sfuma
    f0, f1 = ini['fine']
    metti(buf, colpo(1.0), f0)
    metti(buf, accordo([57, 61, 64, 69, 45], f1 - f0 + 2.5, 0.2, 0.02), f0)
    # fruscio prima di ogni tendina (le tendine coprono i cambi di scena)
    for k, d in scene[1:]:
        s0 = ini[k][0]
        fr = fruscio()
        metti(buf, fr, s0 - len(fr) / SR)
    buf = buf[:int(tot * SR)]
    buf /= np.max(np.abs(buf)) + 1e-9
    buf = np.tanh(buf * 1.6) / np.tanh(1.6) * 0.89  # limitatore morbido
    n = len(buf)
    buf[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))
    buf[:int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))
    return buf


if __name__ == '__main__':
    S = json.load(open(sys.argv[1]))
    audio = componi(S['scene'], S['fps'])
    with tempfile.NamedTemporaryFile(suffix='.wav') as f:
        w = wave.open(f.name, 'wb')
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((audio * 32767).astype('<i2').tobytes())
        w.close()
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', sys.argv[2], '-i', f.name, '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', sys.argv[3]], check=True)
    print('scritto', sys.argv[3], round(len(audio) / SR, 1), 's')
