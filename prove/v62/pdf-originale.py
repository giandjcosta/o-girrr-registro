"""PDF su copie isolate di giornate reali, confronto con renderer originale a quattro pagine."""
import argparse,copy,importlib.util,json,os,shutil,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];p=argparse.ArgumentParser();p.add_argument('sito',type=Path);a=p.parse_args()
OUT=R/'qa_artifacts/pdf62-originale';OUT.mkdir(parents=True,exist_ok=True)
for n in (6,7):
    w=OUT/('g'+str(n));w.mkdir(exist_ok=True)
    for rel in ('scripts','assets/loghi','riepiloghi','girrr/dati'):
        shutil.copytree(a.sito/rel,w/rel,dirs_exist_ok=True)
    d=json.loads((a.sito/'data.json').read_text())
    # Conserva solo i risultati fino alla giornata selezionata, senza riscrivere il sorgente.
    sa=next(g['sa'] for g in d['cal']['lega'] if g['n']==n)
    for g in d['cal']['lega']:
        if g['n']>n:
            for m in g['m']:m[1]=m[2]=None;m[4]='-'
    for g in d['cal']['cup']:
        if g['sa']>sa:
            for m in g['m']:m[2]=m[3]=None;m[5]='-'
    (w/'data.json').write_text(json.dumps(d))
    scheda=a.sito/'riepiloghi'/f'settimana-{n:02}.json'
    testi=json.loads(scheda.read_text()) if scheda.exists() else json.loads((a.sito/'testi.json').read_text())
    # Le schede contengono i testi originali dello stesso numero.
    if 'testi' in testi:testi=testi['testi']
    if 'apertura' not in testi:testi=json.loads((a.sito/'testi.json').read_text())
    (w/'testi.json').write_text(json.dumps(testi,ensure_ascii=False))
    dossier=json.loads((R/'prove/v62/fixture/mvp-reale.json').read_text())
    dossier['commento']=json.loads((R/'prove/v62/fixture/commento.json').read_text())
    if n==6:dossier={'votazione':None,'archivio':[]}
    (w/'girrr/dati/mvp-editoriale.json').write_text(json.dumps(dossier,ensure_ascii=False))
    subprocess.run([sys.executable,str(R/'prove/v62/render-originale.py'),str(w)],check=True)
