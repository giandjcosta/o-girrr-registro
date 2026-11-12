#!/usr/bin/env python3
"""Video della giornata sul sito (Claude, 12 novembre 2026): lo usa il workflow «Video della giornata» del sito.

  python3 pubblica_video.py quale SITO GIORNATE_JSON [--giornata N] [--rifai]
      Scrive «giornata=N» (per $GITHUB_OUTPUT) se c'è un video da fare: l'ultima giornata di Campionato con tutti i
      risultati, già calcolata dal workflow «Calcoli dopo la giornata» (calcoli/giornate.json, «fatta»), e senza video
      in SITO/girrr/video/. Altrimenti «giornata=». Con --giornata sceglie la giornata, con --rifai la rifà anche se c'è.

  python3 pubblica_video.py metti SITO VIDEO.mp4 N
      Copia il video in SITO/girrr/video/giornata-NN.mp4, fa la copertina giornata-NN.jpg (il logo con «Nª giornata»)
      e riscrive archivio.json con archivio.py. La scheda Video di Girrr Sport (Lega e Stadio) legge da lì.
"""
import json
import os
import shutil
import subprocess
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
COPERTINA_S = 1.6   # secondo del video con il logo della lega e «Campionato · Nª giornata» fermi


def giocate(sito):
    D = json.load(open(os.path.join(sito, 'data.json'), encoding='utf-8'))
    return [r['n'] for r in D['cal']['lega'] if r['m'] and all(m[4] and m[4] != '-' for m in r['m'])]


def quale(sito, giornate_json, scelta=None, rifai=False):
    fatte = json.load(open(giornate_json, encoding='utf-8')) if os.path.exists(giornate_json) else {}
    G = giocate(sito)
    n = scelta if scelta else (max(G) if G else None)
    if not n or n not in G:
        return None
    if not scelta and not fatte.get(str(n), {}).get('fatta'):
        return None   # i calcoli della giornata non sono ancora finiti: si aspetta il giro dopo
    if not rifai and os.path.exists(os.path.join(sito, 'girrr', 'video', 'giornata-%02d.mp4' % n)):
        return None
    return n


def metti(sito, video, n):
    cart = os.path.join(sito, 'girrr', 'video')
    os.makedirs(cart, exist_ok=True)
    mp4 = os.path.join(cart, 'giornata-%02d.mp4' % n)
    shutil.copyfile(video, mp4)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(COPERTINA_S), '-i', mp4, '-frames:v', '1',
                    '-vf', 'scale=360:-2', '-q:v', '3', os.path.join(cart, 'giornata-%02d.jpg' % n)], check=True)
    subprocess.run([sys.executable, os.path.join(QUI, 'archivio.py'), os.path.join(sito, 'data.json'), cart], check=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'quale':
        g = int(a[a.index('--giornata') + 1]) if '--giornata' in a and a[a.index('--giornata') + 1] else None
        n = quale(a[1], a[2], g, '--rifai' in a)
        print('giornata=%s' % (n or ''))
    elif a[0] == 'metti':
        metti(a[1], a[2], int(a[3]))
    else:
        sys.exit(__doc__)
