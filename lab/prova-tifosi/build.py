"""Copie di revisione: il mirror pubblicato e le sue sorgenti restano intatti."""
from pathlib import Path
import json, re
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'anteprima/pubblicata'
for skin, directory in [('lega', 'girrr'), ('stadio', 'stadio/girrr')]:
    target = OUT / skin
    target.mkdir(exist_ok=True)
    for page in ['index', 'curva', 'derby', 'derby-stagione', 'app', 'giornale', 'albo']:
        html = (SOURCE / directory / (('derby' if page == 'derby-stagione' else page) + '.html')).read_text()
        if page == 'derby-stagione':
            html = re.sub(r'<script src="derby\.js[^"]*"></script>', '', html)
            html = html.replace('<h1>I Derby</h1>', '<h1>Derby della stagione</h1>').replace('href="index.html">‹ O Girrr', 'href="albo.html#derby">‹ I Derby')
            html = html.replace('O Girrr · I dati arrivano dallo Spogliatoio', '2026/27 · Derby ufficiali registrati')
        # Base relativa stabile anche per il caricamento anticipato degli asset.
        base = '<base href="../../../anteprima/pubblicata/' + directory + '/">'
        head = '<head>' + base + '<script src="' + ('../../../../' if skin == 'stadio' else '../../../') + 'lab/prova-tifosi/guard.js"></script>'
        html = html.replace('<head>', head, 1)
        # Evita service worker e app installata; il resto mantiene gli asset originali.
        html = re.sub(r'<script[^>]*src="[^\"]*(?:offline\.js|assets/app\.js)[^\"]*"[^>]*></script>', '', html)
        rel = '../../../../' if skin == 'stadio' else '../../../'
        html = html.replace('src="v55/ui.js', 'src="'+rel+'lab/prova-tifosi/native-ui.js')
        html = html.replace('/o-girrr-registro/anteprima/pubblicata/', '../../' if skin == 'stadio' else '../')
        html = html.replace('</head>', '<link rel="stylesheet" href="'+rel+'lab/prova-tifosi/prova.css"></head>')
        html = html.replace('</body>', '<script src="'+rel+'lab/prova-tifosi/model.js"></script><script src="'+rel+'lab/prova-tifosi/racconti.js"></script><script src="'+rel+'lab/prova-tifosi/prova.js"></script></body>')
        (target / (page + '.html')).write_text(html)
D = json.loads((SOURCE / 'data.json').read_text())
N = json.loads((SOURCE / 'girrr/novita-dati.js').read_text().split('=', 1)[1].rstrip(';\n'))
official = json.loads((OUT / 'derby-ufficiali.json').read_text())
def pair(a, b):
    return tuple(sorted((a.casefold(), b.casefold())))
names = {pair(r['a'], r['b']): r['n'] for r in N['riv']}
accepted = {pair(r['da'], r['a']): r for r in official['sfide'] if r['stagione'] == official['stagione']}
coppie = []
for r in official['attivi']:
    k = pair(r['a'], r['b'])
    challenge = accepted.get(k)
    coppie.append({'a': r['a'], 'b': r['b'], 'n': challenge['nome'] if challenge else names.get(k, 'Derby'),
                   'dal': r['dal'], 'sfida_id': challenge['id'] if challenge else None})
fixture = {'aggiornato': D['updated'], 'teams': [t['name'] for t in D['teams']], 'rounds': D['cal']['lega'],
           'rivalita': [r for r in N['riv'] if r['r'] >= 80],
           'cupRounds': D['cal']['cup'], 'titoli': N['stag'],
           'dossier': json.loads((ROOT / 'redazione/dossier.json').read_text()),
           'derby_ufficiali': {'stagione': official['stagione'], 'verificato': official['verificato'], 'coppie': coppie}}
(OUT / 'dati.json').write_text(json.dumps(fixture, ensure_ascii=False, indent=2) + '\n')
print('Prova tifosi: 14 copie native e dati locali rigenerati. Mirror invariato.')

# Stessa UI nativa; adattate soltanto le costanti dei percorsi per le URL di ramo.
ui = (SOURCE / 'girrr/v55/ui.js').read_text()
ui = ui.replace("new URL('./',document.currentScript.src).href", "new URL('girrr/v55/',PROVA_TIFOSI.mirror).href")
ui = ui.replace("'/o-girrr-registro/anteprima/pubblicata/", "PROVA_TIFOSI.mirror+'")
ui = ui.replace('src="/o-girrr-registro/anteprima/pubblicata/', 'src="\''+"+PROVA_TIFOSI.mirror+"+"'" )
(OUT / 'native-ui.js').write_text(ui)
