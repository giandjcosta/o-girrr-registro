"""Agganci aggiuntivi sulle pagine correnti. Nessuna copia HTML della preview viene pubblicata."""
import importlib.util
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[2]
FILES=('index.html','app.html','curva.html','derby.html','albo.html')


def main(site,lab=False):
    site=Path(site)
    # Verifica prima di scrivere: la redazione deve corrispondere ai risultati da rilasciare.
    spec=importlib.util.spec_from_file_location('redazione_tifosi',ROOT/'redazione/tifosi.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    derby=json.loads((ROOT/'lab/prova-tifosi/dati.json').read_text())['derby_ufficiali']
    edition=json.loads((ROOT/'redazione/tifosi.json').read_text())
    ctx,_=m.context(site,derby,edition['stagione']);m.validate(edition,ctx)
    for folder in ['girrr','stadio/girrr']:
        for f in FILES:
            p=site/folder/f
            if not p.is_file() or p.read_text().count('</head>')!=1 or p.read_text().count('</body>')!=1:raise ValueError('Pagina da verificare prima del rilascio: '+str(p))
    target=site/'girrr/v60';target.mkdir(parents=True,exist_ok=True)
    for name in ['model.js','tifosi.js','tifosi.css']:shutil.copy2(ROOT/'rilascio/tifosi60'/name,target/name)
    (target/'tifosi-config.json').write_text(json.dumps({'stagione':edition['stagione'],'url':'https://qmjqfgmvimsuxvghetgi.supabase.co','publishableKey':'sb_publishable_qPhimkrF4iUvIad7JPoH8A_i-eOqG7n'},indent=2)+'\n')
    m.publish(edition,ctx,site/'girrr/dati/tifosi-settimane.json')
    for folder in ['girrr','stadio/girrr']:
        prefix='../../girrr/v60/' if folder.startswith('stadio') else 'v60/'
        for f in FILES:
            p=site/folder/f;s=p.read_text()
            if 'data-girrr-tifosi' not in s:
                s=s.replace('</head>','<link rel="stylesheet" href="'+prefix+'tifosi.css" data-girrr-tifosi></head>')
                s=s.replace('</body>','<script src="'+prefix+'model.js"></script><script src="'+prefix+'tifosi.js"></script></body>')
                p.write_text(s)
    print('MVP, Derby e racconti applicati alla copia di rilascio:',site)
