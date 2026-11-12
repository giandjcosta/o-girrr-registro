"""Copie di revisione: il mirror pubblicato e le sue sorgenti restano intatti."""
from pathlib import Path
import json, re
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'anteprima/pubblicata'
for skin, directory in [('lega', 'girrr'), ('stadio', 'stadio/girrr')]:
    target = OUT / skin
    target.mkdir(exist_ok=True)
    for page in ['index', 'curva', 'derby', 'app', 'giornale', 'albo']:
        html = (SOURCE / directory / (page + '.html')).read_text()
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
        html = html.replace('</body>', '<script src="'+rel+'lab/prova-tifosi/model.js"></script><script src="'+rel+'lab/prova-tifosi/prova.js"></script></body>')
        (target / (page + '.html')).write_text(html)
D = json.loads((SOURCE / 'data.json').read_text())
N = json.loads((SOURCE / 'girrr/novita-dati.js').read_text().split('=', 1)[1].rstrip(';\n'))
fixture = {'aggiornato': D['updated'], 'teams': [t['name'] for t in D['teams']], 'rounds': D['cal']['lega'],
           'rivalita': [r for r in N['riv'] if r['r'] >= 80],
           'dossier': json.loads((ROOT / 'redazione/dossier.json').read_text())}
(OUT / 'dati.json').write_text(json.dumps(fixture, ensure_ascii=False, indent=2) + '\n')
print('Prova tifosi: 12 copie native e dati locali rigenerati. Mirror invariato.')

# Stessa UI nativa; adattate soltanto le costanti dei percorsi per le URL di ramo.
ui = (SOURCE / 'girrr/v55/ui.js').read_text()
ui = ui.replace("new URL('./',document.currentScript.src).href", "new URL('girrr/v55/',PROVA_TIFOSI.mirror).href")
ui = ui.replace("'/o-girrr-registro/anteprima/pubblicata/", "PROVA_TIFOSI.mirror+'")
ui = ui.replace('src="/o-girrr-registro/anteprima/pubblicata/', 'src="\''+"+PROVA_TIFOSI.mirror+"+"'" )
(OUT / 'native-ui.js').write_text(ui)
