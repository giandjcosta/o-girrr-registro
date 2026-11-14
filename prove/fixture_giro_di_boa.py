#!/usr/bin/env python3
"""Fixture sintetiche solo per le prove, mai per il Lab dei risultati reali."""
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'calcoli'))
from giro_di_boa import calcola
from prova_giro_di_boa import dati

dest=Path(sys.argv[1]);dest.mkdir(parents=True,exist_ok=True)
for n in (16,17,19,34):
    (dest/f'giornata-{n}.json').write_text(json.dumps(calcola(dati(n))))
d=json.loads((Path(__file__).resolve().parents[1]/'anteprima/pubblicata/data.json').read_text())
for g in d['cal']['lega']:
    for m in g['m']:
        if not m[4] or m[4]=='-':m[1]=71;m[2]=66;m[4]='2-1'
d.pop('votiTs',None);d.pop('calcTs',None)
(dest/'nomi-lunghi.json').write_text(json.dumps(calcola(d)))
