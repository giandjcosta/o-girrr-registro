#!/usr/bin/env python3
"""Aggiorna solo la copia locale del calendario pubblico usata per le cronache 5.3.
Non pubblica file, non contatta database e non genera audio.
"""
import json
from pathlib import Path
from urllib.request import urlopen
R=Path(__file__).resolve().parent

def riduci(d):
    if not isinstance(d.get('teams'),list) or not (d.get('cal') or {}).get('lega'):
        raise ValueError('Calendario o squadre non disponibili')
    return {'updated':d.get('updated'),'teams':[{'name':t['name']} for t in d['teams']],
            'cal':{'lega':d['cal']['lega']}}

def main():
    with urlopen('https://giandjcosta.github.io/o-fant-a-girrr/data.json',timeout=30) as r:
        d=json.load(r)
    (R/'dati/calendario-stagione.json').write_text(json.dumps(riduci(d),ensure_ascii=False,indent=2))
    print('Copia locale aggiornata. Rigenerare con python3 anteprima/build.py; nessun file pubblicato.')

if __name__=='__main__':main()
