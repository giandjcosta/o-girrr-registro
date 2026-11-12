#!/usr/bin/env python3
"""Mette un brano vero sotto il video della giornata, tagliato sulla durata del video (Claude, 12 novembre 2026).

Il video non dura sempre uguale (la scena «Da non perdere» a volte manca), il brano è più lungo. Lo script tiene l'inizio
del brano e attacca il suo finale vero (gli ultimi CODA secondi), così la musica parte e finisce come l'ha pensata chi
l'ha fatta. Il punto del taglio è scelto dove il ritmo delle due parti combacia (confronto degli attacchi dei colpi),
con una dissolvenza di 80 ms: non si sente lo stacco. Il video non viene ricodificato.

Brani usati per la prova: «O Fant a Girrr (1)» e «(2)», fatti da Gianluca con MakeBestMusic.

Suoni sopra la musica (fischio, folla…): --suono FILE:DA:A@QUANDO:VOLUME, per esempio --suono fischio.mp3:0.9:3@0:1.0
(prende il pezzo DA-A secondi del file, lo porta a volume pieno per VOLUME e lo mette a QUANDO secondi del video; con
QUANDO negativo conta dalla fine del video). Con un suono sopra, la musica si abbassa un poco per lasciarlo sentire.

--inizio S fa partire il brano da S secondi (per far cadere una «esplosione» del brano su un momento del video), --fine S
lo ferma a S secondi (per togliere il silenzio finale e far cadere il colpo finale sulla chiusura del video).
--dopo FILE:INIZIO:FINE@QUANDO passa a un secondo brano a QUANDO secondi del video (per esempio dalla base calma da TV
del Campionato a quella epica della Coppa): il primo sfuma nel mezzo secondo prima, il secondo parte da INIZIO secondi
del suo brano (scelto in modo che la sua «esplosione» cada a QUANDO), si ferma a FINE e il suo finale vero chiude il video.
--effetti scene.json mette gli effetti grafici (cartella suoni/) a tempo con le scene, calcolati fotogramma per fotogramma
dalla stessa scaletta del video (vedi EFFETTI qui sotto). Ogni effetto ha il suo volume rispetto al volume medio della
musica (in dB, negativo = più basso della musica); solo i suoni importanti (loghi, fischi, boato) abbassano un poco la musica.

Uso: python3 rilascio/video/monta_musica.py BRANO.mp3 VIDEO_MUTO.mp4 VIDEO_CON_MUSICA.mp4 [--coda SECONDI] [--suono …]
"""
import argparse
import json
import os
import subprocess
import tempfile
import wave

import numpy as np

SR = 48000
HOP = 480  # 10 ms


def carica(f):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, '<i2').astype(np.float32).reshape(-1, 2) / 32768


def durata(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                                capture_output=True, text=True, check=True).stdout)


def attacchi(x):  # quanto cresce il volume ogni 10 ms: i colpi di batteria
    m = x.mean(1)
    n = len(m) // HOP
    e = np.log1p(1000 * (m[:n * HOP].reshape(n, HOP) ** 2).sum(1))
    o = np.maximum(0, np.diff(e, prepend=e[0]))
    return o - o.mean()


SUONI = __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'suoni')
# nome: (file, da, a = pezzo utile del file in secondi, picco = dove cade il colpo dentro il pezzo, dB rispetto alla musica, abbassa la musica)
EFFETTI = {
    'logo-lega': ('logo-lega.mp3', 0.0, 0.9, 0.10, -3, True),
    'fischio':   ('fischio-inizio.mp3', 0.9, 3.0, 0.3, -4, True),
    'whoosh':    ('whoosh.mp3', 0.0, 0.5, 0.25, -12, False),
    'pop':       ('pop.mp3', 0.0, 0.15, 0.0, -15, False),
    'cascata':   ('cascata.mp3', 0.0, 1.2, 0.0, -10, False),
    'podio':     ('podio.mp3', 0.25, 1.2, 0.9, -10, False),
    'boato':     ('boato.mp3', 0.0, 3.0, 0.1, -7, True),
    'ultimo':    ('ultimo.mp3', 0.0, 0.7, 0.0, -9, False),
    'logo-coppa': ('logo-coppa.mp3', 0.0, 1.0, 0.33, -2, True),
    'derby':     ('derby.mp3', 0.0, 3.3, 0.0, -6, True),
    'triplice':  ('triplice-fischio.mp3', 0.0, 2.2, 0.0, 0, True),
    'stadio':    ('stadio.mp3', 0.0, 30.0, 0.0, -24, False),
}


def scaletta(S):
    """Elenco (effetto, secondo del video in cui cade il colpo) dalla scaletta delle scene (scene.json di render.mjs).
    Gli istanti sono quelli di src/index.jsx: le partite entrano a 14 + 9·i fotogrammi, le righe della classifica a 8 + 3·i,
    i gradini del podio arrivano entro 1,2 s, la tendina copre il cambio di scena."""
    fps, ini, t = S['fps'], {}, 0.0
    for k, d in S['scene']:
        ini[k] = t
        t += d / fps
    E = [('logo-lega', 0.25), ('fischio', 1.2)]
    for k, _ in S['scene'][1:]:
        if k == 'introCoppa':
            E.append(('logo-coppa', ini[k]))
        elif k != 'fine':
            E.append(('whoosh', ini[k]))
    for k, n in (('lega', S.get('m', 5)), ('coppa', S.get('mc', 4))):
        E += [('pop', ini[k] + (14 + 9 * i + 3) / fps) for i in range(n)]
    E += [('podio', ini['podio'] + 0.95), ('boato', ini['podio'] + 1.05)]
    ncl = S.get('cl', 10)
    E += [('cascata', ini['classifica'] + 8 / fps), ('ultimo', ini['classifica'] + (8 + 3 * (ncl - 1) + 4) / fps)]
    if 'prossime' in ini and S.get('derby'):
        E.append(('derby', ini['prossime'] + 0.9))
    E.append(('triplice', ini['fine'] + 0.15))
    E.append(('stadio', 0.0))
    return E


def mescola(y, cues, lungo):
    musica = np.sqrt(np.mean(y ** 2)) + 1e-9
    g = np.ones(len(y), np.float32)
    agg = np.zeros_like(y)
    cache = {}
    for nome, quando in cues:
        f, da, a, picco, db, abbassa = EFFETTI[nome]
        if nome not in cache:
            z = carica(os.path.join(SUONI, f))[int(da * SR):int(a * SR)].copy()
            att = np.sqrt((z ** 2).mean(1))
            rms = np.sqrt(np.mean(att[att > att.max() * 0.1] ** 2))   # volume della parte che suona davvero
            z *= musica * 10 ** (db / 20) / (rms + 1e-9)
            n = min(len(z) // 4, int(0.15 * SR))
            z[-n:] *= np.linspace(1, 0, n)[:, None]
            cache[nome] = z
        z = cache[nome]
        if nome == 'stadio':  # brusio sotto tutto il video, ripetuto se serve, con entrata e uscita morbide
            z = np.tile(z, (int(np.ceil(len(y) / len(z))), 1))[:len(y)].copy()
            n = int(1.0 * SR)
            z[:n] *= np.linspace(0, 1, n)[:, None]
            z[-n:] *= np.linspace(1, 0, n)[:, None]
        i = int((quando - picco) * SR)
        j = min(len(y), i + len(z))
        if i < 0:
            z, i = z[-i:], 0
        agg[i:j] += z[:j - i]
        if abbassa:
            g[i:j] = np.minimum(g[i:j], 0.6)
    g = np.convolve(g, np.ones(4800) / 4800, 'same')   # la musica scende e risale in 0,1 s
    print('effetti: %d (%s)' % (len(cues), ', '.join(sorted(set(c[0] for c in cues)))))
    return y * g[:, None] + agg


def monta(x, lungo, coda):
    tot = len(x) / SR
    if tot <= lungo:
        return x
    o = attacchi(x)
    a0, b0 = lungo - coda, tot - coda  # taglio ideale: inizio [0, a], finale [b, fine]
    fin = 200  # confronto su 2 s prima e dopo il taglio
    meglio, ab = -1e9, (a0, b0)
    for da in range(-60, 61, 1):       # sposto il taglio fino a 0,6 s...
        for db in range(-25, 26, 1):   # ...e il finale fino a 0,25 s (la durata cambia al massimo di 0,25 s)
            a, b = int(a0 * 100) + da, int(b0 * 100) + da + db
            if a - fin < 0 or b + fin > len(o):
                continue
            s = np.dot(o[a - fin:a + fin], o[b - fin:b + fin])
            if s > meglio:
                meglio, ab = s, (a / 100, b / 100)
    a, b = int(ab[0] * SR), int(ab[1] * SR)
    xf = int(0.08 * SR)
    f = np.linspace(0, 1, xf)[:, None]
    out = np.concatenate([x[:a - xf], x[a - xf:a] * (1 - f) + x[b - xf:b] * f, x[b:]])
    print('taglio a %.2f s, riprende da %.2f s del brano (finale di %.1f s)' % (ab[0], ab[1], tot - ab[1]))
    return out


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('brano')
    p.add_argument('video')
    p.add_argument('uscita')
    p.add_argument('--coda', type=float, default=8.0, help='secondi del finale vero del brano da tenere')
    p.add_argument('--inizio', type=float, default=0.0, help='secondi del brano da cui partire')
    p.add_argument('--fine', type=float, default=0.0, help='secondi del brano a cui fermarsi (0 = fino alla fine)')
    p.add_argument('--dopo', default='', help='FILE:INIZIO:FINE@QUANDO')
    p.add_argument('--effetti', default='', help='scene.json di render.mjs: effetti grafici a tempo')
    p.add_argument('--suono', action='append', default=[], help='FILE:DA:A@QUANDO:VOLUME')
    A = p.parse_args()
    lungo = durata(A.video)
    x = carica(A.brano)
    x = x[int(A.inizio * SR):int(A.fine * SR) if A.fine else len(x)].copy()
    if A.fine:
        x[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))[:, None]
    if A.dopo:
        sorg, q = A.dopo.rsplit('@', 1)
        f2, i2, f2fine = sorg.rsplit(':', 2)
        q, xf = float(q), 0.5
        z = carica(f2)[int(float(i2) * SR):int(float(f2fine) * SR)].copy()
        z[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))[:, None]
        z = monta(z, lungo - q + xf, A.coda)
        k, n = int((q - xf) * SR), int(xf * SR)
        y = x[:k + n].copy()
        if len(y) < k + n:
            y = np.concatenate([y, np.zeros((k + n - len(y), 2), np.float32)])
        y[k:] *= np.linspace(1, 0, n)[:, None]
        z[:n] *= np.linspace(0, 1, n)[:, None]
        y = np.concatenate([y[:k], y[k:] + z[:n], z[n:]])
        print('secondo brano', f2, 'da %.2f s del video' % (q - xf))
    else:
        y = monta(x, lungo, A.coda)
    y = y[:int(lungo * SR)]
    if len(y) < lungo * SR:
        y = np.concatenate([y, np.zeros((int(lungo * SR) - len(y), 2), np.float32)])
    y[:int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))[:, None]
    for s in A.suono:
        sorg, dove = s.rsplit('@', 1)
        f, da, a = sorg.rsplit(':', 2)
        quando, vol = (float(v) for v in dove.split(':'))
        z = carica(f)[int(float(da) * SR):int(float(a) * SR)]
        z = z / (np.abs(z).max() + 1e-9) * 0.9 * vol
        k = int(0.25 * len(z))  # sfuma l'ultimo quarto
        z[-k:] *= np.linspace(1, 0, k)[:, None]
        i = int((quando if quando >= 0 else lungo + quando) * SR)
        j = min(len(y), i + len(z))
        g = np.ones(len(y), np.float32)  # la musica scende di circa 5 dB sotto il suono
        g[i:j] = 0.55
        g = np.convolve(g, np.ones(2400) / 2400, 'same')
        y = y * g[:, None]
        y[i:j] += z[:j - i]
        print('suono', f, 'a %.2f s' % (i / SR))
    if A.effetti:
        y = mescola(y, scaletta(json.load(open(A.effetti))), lungo)
    y = np.tanh(y * 1.1) / np.tanh(1.1) * 0.95
    with tempfile.NamedTemporaryFile(suffix='.wav') as t:
        w = wave.open(t.name, 'wb')
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype('<i2').tobytes())
        w.close()
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', A.video, '-i', t.name, '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', A.uscita], check=True)
    print('scritto', A.uscita, '%.1f s' % lungo)
