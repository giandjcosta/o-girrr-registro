#!/usr/bin/env python3
"""Rilascio della 6.0 su una copia di gh-pages (Claude, 12 novembre 2026). Non fa commit e non tocca il sito vero.

Uso: python3 rilascio/rilascio60.py CARTELLA_GH_PAGES [--lab]
  --lab: aggiunge gli agganci per le prove automatiche della Curva (window.__curvaProva). Mai sul sito vero.
     python3 rilascio/rilascio60.py CARTELLA_GH_PAGES --controlla [--lab]
  Solo controllo di una copia già preparata (lo fa anche alla fine del rilascio): pezzi presenti, niente agganci di prova
  sul sito vero, video e copertine dell'archivio esistenti, condividi.js uguale al registro.
Va eseguito una volta su una copia NUOVA di gh-pages: se la copia è già preparata si ferma prima di scrivere.

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


def gia_preparata(sito):
    """La Curva per sistema e la scheda Video lasciano segni riconoscibili: se ci sono, la copia è già stata preparata."""
    segni = []
    for rel, segno in (('girrr/curva.html', 'function cvNuovi('), ('stadio/girrr/curva.html', 'function cvNuovi('),
                       ('girrr/app.html', 'function spVideo('), ('stadio/girrr/app.html', 'function spVideo(')):
        if segno in leggi(os.path.join(sito, rel)):
            segni.append(rel)
    return segni


def controlla(sito, lab=False):
    """Controlla una copia preparata. Restituisce l'elenco dei problemi (vuoto se è tutto a posto)."""
    import json, re
    pr = []
    for rel, p in (('girrr/curva.html', '../'), ('stadio/girrr/curva.html', '../../')):
        t = leggi(os.path.join(sito, rel))
        if 'function cvNuovi(' not in t: pr.append(rel + ': manca la Curva ferma (cvNuovi)')
        if '<script src="%scurva-os.js"></script>' % p not in t: pr.append(rel + ': non carica curva-os.js')
        if ('window.__curvaProva' in t) != lab: pr.append(rel + (': agganci di prova presenti sul sito vero' if not lab else ': mancano gli agganci di prova'))
    for rel, base in (('girrr/app.html', "VB='video/'"), ('stadio/girrr/app.html', "VB='../../girrr/video/'")):
        t = leggi(os.path.join(sito, rel))
        if 'function spVideo(' not in t: pr.append(rel + ': manca la scheda Video')
        if base not in t.replace(' ', ''): pr.append(rel + ': cartella dei video sbagliata (attesa ' + base + ')')
        if 'video-giornata/archivio' in t: pr.append(rel + ': legge i video del Lab')
    for rel, p in (('girrr/index.html', '../'), ('stadio/girrr/index.html', '../../')):
        if '<script src="%scondividi.js" defer></script>' % p not in leggi(os.path.join(sito, rel)): pr.append(rel + ': non carica condividi.js')
    for f in ('curva-os.js', 'curva-os.css', 'condividi.js', 'girrr/curva-banca.js', 'stadio/girrr/curva-banca.js'):
        if not os.path.isfile(os.path.join(sito, f)): pr.append(f + ': manca')
    if os.path.isfile(os.path.join(sito, 'condividi.js')) and leggi(os.path.join(sito, 'condividi.js')) != leggi(os.path.join(R, 'rilascio/condividi/condividi.js')):
        pr.append('condividi.js diverso da quello del registro')
    cart = os.path.join(sito, 'girrr/video')
    try:
        A = json.load(open(os.path.join(cart, 'archivio.json'), encoding='utf-8'))
        if not A: pr.append('girrr/video/archivio.json: vuoto')
        for v in A:
            for k in ('file', 'img'):
                if v.get(k) and not os.path.isfile(os.path.join(cart, v[k])): pr.append('girrr/video/' + v[k] + ': manca')
    except (OSError, ValueError) as e:
        pr.append('girrr/video/archivio.json: ' + str(e))
    for d in ('girrr', 'stadio/girrr'):
        for f in ('index.html', 'app.html', 'curva.html'):
            t = leggi(os.path.join(sito, d, f))
            if t.count('<script') != t.count('</script>'): pr.append(d + '/' + f + ': tag <script> non chiusi')
            if re.search(r'https?://(localhost|127\.0\.0\.1)', t): pr.append(d + '/' + f + ': indirizzo di prova (localhost)')
    return pr


def main(sito, lab=False):
    segni = gia_preparata(sito)
    if segni:
        sys.exit('Questa copia è già preparata (' + ', '.join(segni) + '): usa una copia nuova di gh-pages. Niente è stato scritto.')
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
    pr = controlla(sito, lab)
    if pr:
        sys.exit('Controllo finale: ' + str(len(pr)) + ' problemi\n  ' + '\n  '.join(pr))
    print('Controllo finale: tutto a posto' + (' (copia di prova, con gli agganci della Curva)' if lab else ' (copia per il sito vero)'))


if __name__ == '__main__':
    if '--controlla' in sys.argv:
        pr = controlla(sys.argv[1], '--lab' in sys.argv)
        print('Controllo: ' + ('tutto a posto' if not pr else str(len(pr)) + ' problemi\n  ' + '\n  '.join(pr)))
        sys.exit(1 if pr else 0)
    main(sys.argv[1], '--lab' in sys.argv)
