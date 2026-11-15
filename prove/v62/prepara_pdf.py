"""Solo preparazione locale; non esegue il main originale, TTS o workflow."""
import json,shutil,sys,importlib.util
from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('sito',type=Path);a=p.parse_args()
r=Path(__file__).resolve().parents[2];site=a.sito.resolve();w=r/'qa_artifacts/pdf62';w.mkdir(parents=True,exist_ok=True)
for d in ['scripts','assets/loghi','formazioni','riepiloghi']:
 if (site/d).exists():shutil.copytree(site/d,w/d,dirs_exist_ok=True)
shutil.copyfile(site/'data.json',w/'data.json');sys.path.insert(0,str(w/'scripts'))
spec=importlib.util.spec_from_file_location('giornale',w/'scripts/pdf_giornale.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t=json.loads((site/'testi.json').read_text());m=json.loads((r/'lab/coordinamento-62/mvp-reale.json').read_text())['votazione']
# Soltanto voto aperto reale, giornata e scadenza annunciata conservate.
from datetime import datetime
from zoneinfo import ZoneInfo
fine=datetime.fromisoformat(m['chiude']).astimezone(ZoneInfo('Europe/Rome'))
commento=json.loads((r/'lab/coordinamento-62/commento-reale.json').read_text());t['coro']['squadra']=commento['squadra'];t['coro']['testo']=f'MVP della {m["giornata"]}ª: si vota in Curva fino al {fine.day} novembre alle {fine:%H:%M}.\n'+commento['testo']
h,n=g.costruisci(t);(w/'originale.html').write_text(h)
print(w,n)
