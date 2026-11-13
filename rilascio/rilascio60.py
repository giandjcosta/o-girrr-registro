#!/usr/bin/env python3
"""Rilascio della 6.0 su una copia di gh-pages (Claude, 12 novembre 2026). Non fa commit e non tocca il sito vero.

Uso: python3 rilascio/rilascio60.py CARTELLA_GH_PAGES [--lab]
  --lab: aggiunge gli agganci per le prove automatiche della Curva (window.__curvaProva). Mai sul sito vero.

Cosa mette (tutto dal registro):
  1. Curva per sistema (Liquid Glass su iPhone, Material 3 su Android), Curva ferma, Notifiche divise, pillola «Nuovi cori»,
     bozza, link ai cori, Impostazioni, nuovi personaggi: rilascio/curva-os/applica.py sulle due curva.html, più
     curva-os.js e curva-os.css (caricati dalle due curva.html) e curva-banca.js (Lega e Stadio).
  2. Scheda Video in Girrr Sport: rilascio/video/scheda/applica.py sulle due app.html; video delle giornate già giocate
     (lab/video-giornata/archivio/) in girrr/video/ con copertine e archivio.json. Dopo, li fa il workflow «Video della giornata».
  3. «Condividi la giornata»: condividi.js nella radice e caricato dalle due Home (rilascio/condividi/applica.py).
La Radio (fischi nuovi) è nel registro (voci-src/monta.py): vale dalla prima puntata dopo l'unione al main del registro.
Il workflow del video va sul main del sito (.github/workflows/video-giornata.yml, ramo claude/o-girrr-versione-6-0-mjh4ut).
versioni.json si aggiorna a parte con rilascio/versioni/aggiungi.py.
"""
import importlib.util
import os
import shutil
import sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def modulo(rel):
    spec = importlib.util.spec_from_file_location(rel.replace('/', '_'), os.path.join(R, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def leggi(p):
    return open(p, encoding='utf-8').read()


def scrivi(p, t):
    open(p, 'w', encoding='utf-8').write(t)


def main(sito, lab=False):
    cambiati = []
    # 1. Curva
    cos = modulo('rilascio/curva-os/applica.py')
    for rel in ('girrr/curva.html', 'stadio/girrr/curva.html'):
        p = '../../' if rel.startswith('stadio') else '../'
        t = cos.applica(leggi(os.path.join(sito, rel)), lab)
        if 'curva-os.js' not in t:   # stile per sistema (nel Lab lo aggiunge lo specchio, lab/offline/sw-prova.js)
            assert t.count('</head>') == 1, rel
            t = t.replace('</head>', '<script src="%scurva-os.js"></script><link rel="stylesheet" href="%scurva-os.css"></head>' % (p, p))
        scrivi(os.path.join(sito, rel), t); cambiati.append(rel)
    for src, dst in (('rilascio/curva-os/curva-os.js', 'curva-os.js'), ('rilascio/curva-os/curva-os.css', 'curva-os.css'),
                     ('rilascio/curva-os/pagine/girrr/curva-banca.js', 'girrr/curva-banca.js'),
                     ('rilascio/curva-os/pagine/stadio/girrr/curva-banca.js', 'stadio/girrr/curva-banca.js'),
                     # 3. Condividi la giornata
                     ('rilascio/condividi/condividi.js', 'condividi.js')):
        shutil.copyfile(os.path.join(R, src), os.path.join(sito, dst)); cambiati.append(dst)
    # 2. Scheda Video e video già fatti
    vid = modulo('rilascio/video/scheda/applica.py')
    for rel, base in (('girrr/app.html', "'video/'"), ('stadio/girrr/app.html', "'../../girrr/video/'")):
        scrivi(os.path.join(sito, rel), vid.applica(leggi(os.path.join(sito, rel)), base)); cambiati.append(rel)
    arch, dest = os.path.join(R, 'lab/video-giornata/archivio'), os.path.join(sito, 'girrr/video')
    os.makedirs(dest, exist_ok=True)
    for f in sorted(os.listdir(arch)):
        if f.endswith(('.mp4', '.jpg')) and not os.path.exists(os.path.join(dest, f)):
            shutil.copyfile(os.path.join(arch, f), os.path.join(dest, f)); cambiati.append('girrr/video/' + f)
    import subprocess
    subprocess.run([sys.executable, os.path.join(R, 'rilascio/video/archivio.py'), os.path.join(sito, 'data.json'), dest], check=True)
    cambiati.append('girrr/video/archivio.json')
    # 3. Home con condividi.js
    for rel, p in (('girrr/index.html', '../'), ('stadio/girrr/index.html', '../../')):
        t, tag, a = leggi(os.path.join(sito, rel)), '<script src="%scondividi.js" defer></script>' % p, '<script src="%sversioni.js" defer></script>' % p
        if tag not in t:
            assert t.count(a) == 1, rel
            scrivi(os.path.join(sito, rel), t.replace(a, a + '\n' + tag))
        cambiati.append(rel)
    # 4. Novità dei tifosi: agganci sulle pagine appena preparate, inclusa la scheda Video.
    tifosi = modulo('rilascio/tifosi60/applica.py')
    tifosi.main(sito, lab)
    print('6.0 applicata a', sito, '·', len(cambiati), 'file più il modulo tifosi')
    for c in cambiati:
        print('  ', c)


if __name__ == '__main__':
    main(sys.argv[1], '--lab' in sys.argv)
