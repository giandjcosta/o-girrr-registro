#!/usr/bin/env python3
"""6.6 · Icona dell'app a scelta, scudo o simbolo (Claude, 24 novembre 2026, decisione di Gianluca).

- assets/icone/: le icone dello scudo (per sempre) e del simbolo con il pallone, nelle misure per iPhone, Android e PC.
- manifest.webmanifest usa lo scudo (scelta di base); manifest-simbolo.webmanifest è uguale ma con il simbolo.
- icona66.js nella radice, incluso in ogni pagina subito dopo l'apple-touch-icon: imposta l'icona secondo la scelta e,
  nella pagina Notifiche, mostra il riquadro «Icona dell'app».
Le vecchie icone (assets/icon-*.png, apple-touch-icon.png) restano dove sono: le usa chi ha già l'app sulla schermata Home.

Uso: python3 rilascio/r66/icona.py CARTELLA_GH_PAGES   (idempotente: la seconda volta «File cambiati: 0»)
"""
import json
import pathlib
import shutil
import sys

QUI = pathlib.Path(__file__).resolve().parent


def scrivi(f, testo, cambiati):
    if not f.exists() or f.read_text(encoding='utf-8') != testo:
        f.write_text(testo, encoding='utf-8'); cambiati.add(str(f))


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    sito = pathlib.Path(argv[0]).resolve()
    cambiati = set()
    (sito / 'assets/icone').mkdir(exist_ok=True)
    for p in sorted((QUI / 'icone').glob('*.png')):
        d = sito / 'assets/icone' / p.name
        if not d.exists() or d.read_bytes() != p.read_bytes():
            shutil.copyfile(p, d); cambiati.add(str(d))
    js = sito / 'icona66.js'
    if not js.exists() or js.read_bytes() != (QUI / 'icona66.js').read_bytes():
        shutil.copyfile(QUI / 'icona66.js', js); cambiati.add(str(js))
    # manifest: icone dello scudo come scelta di base, e la copia con il simbolo
    m = json.loads((sito / 'manifest.webmanifest').read_text(encoding='utf-8'))
    def icone(k):
        return [{"src": f"assets/icone/{k}-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                {"src": f"assets/icone/{k}-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                {"src": f"assets/icone/{k}-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]
    for k, nome in (('scudo', 'manifest.webmanifest'), ('simbolo', 'manifest-simbolo.webmanifest')):
        x = dict(m, icons=icone(k))
        x['shortcuts'] = [dict(s, icons=[{"src": f"assets/icone/{k}-192.png", "sizes": "192x192", "type": "image/png"}]) for s in m.get('shortcuts', [])]
        testo = json.dumps(x, ensure_ascii=False, indent=2) + '\n'
        scrivi(sito / nome, testo, cambiati)
    # in ogni pagina con l'apple-touch-icon: lo script subito dopo, e apple-touch-icon e favicon nuovi
    pagine = [sito / 'index.html'] + sorted((sito / 'girrr').glob('*.html')) + sorted((sito / 'stadio/girrr').glob('*.html'))
    for p in pagine:
        t = p.read_text(encoding='utf-8')
        pre = '../../' if '/stadio/girrr/' in str(p) else '../' if p.parent.name == 'girrr' else ''
        vecchio = f'<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">'
        if 'icona66.js' in t:
            continue
        nuovo = f'<link rel="apple-touch-icon" href="{pre}assets/icone/scudo-180.png"><script src="{pre}icona66.js?v=66"></script>'
        if vecchio in t:
            t = t.replace(vecchio, nuovo, 1)
        else:   # pagine senza icone (Albo, Campo, Curva, Notifiche, Versioni): si aggiungono prima della fine di <head>
            extra = ('' if 'rel="manifest"' in t else f'<link rel="manifest" href="{pre}manifest.webmanifest">') + nuovo
            if t.count('</head>') != 1:
                raise SystemExit(f'{p}: </head> non trovato una volta sola')
            t = t.replace('</head>', extra + '</head>', 1)
        t = t.replace(f'<link rel="icon" type="image/png" href="{pre}assets/favicon-64.png">', f'<link rel="icon" type="image/png" href="{pre}assets/icone/scudo-64.png">', 1)
        p.write_text(t, encoding='utf-8'); cambiati.add(str(p))
    print('Icona dell\'app: file cambiati:', len(cambiati))


if __name__ == '__main__':
    main(sys.argv[1:])
