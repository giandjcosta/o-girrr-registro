#!/usr/bin/env python3
"""Archivio dei video della giornata per la scheda Video di Girrr Sport (Claude, 12 novembre 2026).

Scrive archivio.json accanto ai video (giornata-NN.mp4 e giornata-NN.jpg, la foto di copertina), dal più recente al primo,
come voci/archivio.json della Radio. Titoli a livello sportivo: squadre, risultati, posizioni, niente fantapunti.

Uso: python3 rilascio/video/archivio.py DATA_JSON CARTELLA_DEI_VIDEO
"""
import json
import os
import re
import sys

NOMI = {'The Blue brothers': 'The Blues Brothers'}


def nm(s):
    return NOMI.get(s, s)


def classifica(giornate, fino):
    T = {}
    for x in giornate:
        if x['n'] > fino:
            continue
        for m in x['m']:
            a, b = (int(v) for v in m[4].split('-'))
            for s, g1, g2, fp in ((m[0], a, b, m[1]), (m[3], b, a, m[2])):
                t = T.setdefault(s, {'n': s, 'pt': 0, 'fp': 0})
                t['fp'] += fp
                t['pt'] += 3 if g1 > g2 else 1 if g1 == g2 else 0
    return sorted(T.values(), key=lambda t: (-t['pt'], -t['fp']))


def titolo(D, n):
    L = D['cal']['lega']
    giocate = [x for x in L if all(m[4] and m[4] != '-' for m in x['m'])]
    C = classifica(giocate, n)
    prima = classifica(giocate, n - 1) if n > 1 else []
    capo = C[0]['n']
    g = next(x for x in L if x['n'] == n)
    m = next((m for m in g['m'] if capo in (m[0], m[3])), None)
    if m:
        a, b = (int(v) for v in m[4].split('-'))
        noi, loro = (a, b) if m[0] == capo else (b, a)
        avv = m[3] if m[0] == capo else m[0]
        if noi > loro:
            verbo = f'batte {nm(avv)}'
        elif noi == loro:
            verbo = f'pareggia con {nm(avv)}'
        else:
            verbo = f'perde con {nm(avv)}'
    else:
        verbo = 'riposa'
    era = prima and prima[0]['n'] == capo
    return f"{nm(capo)} {verbo} e {'resta' if era else 'va'} in testa"


def main(data, cartella):
    D = json.load(open(data, encoding='utf-8'))
    cup = D['cal'].get('cup', [])
    L = {x['n']: x for x in D['cal']['lega']}
    voci = []
    for f in sorted(os.listdir(cartella)):
        m = re.fullmatch(r'giornata-(\d+)\.mp4', f)
        if not m:
            continue
        n = int(m.group(1))
        sa = L[n]['sa']
        cg = [x for x in cup if x['sa'] <= sa and all(r[5] and r[5] != '-' for r in x['m'])]
        tag = f'Campionato · {n}ª giornata' + (f' · Champions Cup · {cg[-1]["n"]}ª giornata' if cg else '')
        img = f'giornata-{n:02d}.jpg'
        voci.append({'n': n, 'titolo': titolo(D, n), 'tag': tag, 'file': f,
                     'img': img if os.path.exists(os.path.join(cartella, img)) else ''})
    voci.sort(key=lambda v: -v['n'])
    out = os.path.join(cartella, 'archivio.json')
    json.dump(voci, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('scritto', out, len(voci), 'video')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
