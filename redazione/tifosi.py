#!/usr/bin/env python3
"""Prepara e controlla i racconti settimanali. Nessuna generazione a pagamento o scrittura al DB."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]


import sys
sys.path.insert(0,str(ROOT/'calcoli/tifosi'))
from fatti import context,deadline


def validate(edition,ctx):
    if edition.get('schema')!=1 or edition.get('stagione')!=ctx['stagione']:raise ValueError('Formato o stagione errati')
    facts={str(g['giornata']):g for g in ctx['giornate']}
    if str(ctx['ultima']) not in edition.get('giornate',{}):raise ValueError('Manca la settimana corrente: la redazione deve prepararla')
    for day,entry in edition['giornate'].items():
        if day not in facts or entry.get('firma')!=facts[day]['firma']:raise ValueError('Fatti modificati nella giornata '+day+': rigenerare il racconto')
        if not facts[day]['coppaCompleta']:raise ValueError('Risultati di Champions Cup ancora parziali')
        historic=entry.get('storicoCurato') is True and int(day)<edition.get('avvioGiornata',0)
        teams=set(entry.get('squadre',{}))
        if not teams or not teams.issubset(ctx['squadre']) or (not historic and teams!=set(ctx['squadre'])):raise ValueError('Servono i racconti di tutte le squadre')
        seen=set()
        for team,e in entry['squadre'].items():
            if not isinstance(e.get('titolo'),str) or not 8<=len(e['titolo'])<=150:raise ValueError('Titolo non valido: '+team)
            paragraphs=e.get('paragrafi',[])
            if len(paragraphs)!=3 or any(not isinstance(p,str) or not 30<=len(p)<=1800 for p in paragraphs):raise ValueError('Servono tre paragrafi: '+team)
            text=' '.join(paragraphs)
            if re.search(r'fantapunti|fantacrediti|scommess',text,re.I) or re.search(r'·\s+[a-zà-ù]',text):raise ValueError('Livello editoriale o maiuscole da correggere: '+team)
            if text in seen:raise ValueError('Racconti duplicati fra squadre')
            seen.add(text)
        jury=entry.get('redazione',[])
        candidates={c['team'] for c in facts[day]['candidati']}
        if candidates and not historic:
            if not 1<=len(jury)<=10 or len({v['autore'] for v in jury})!=len(jury):raise ValueError('Giuria redazione non valida')
            for vote in jury:
                if vote.get('scelta') not in candidates or not 15<=len(vote.get('motivo',''))<=600:raise ValueError('Preferenza redazione non valida')
    return True


def publish(edition,ctx,path):
    validate(edition,ctx)
    # Un archivio precedente non viene cancellato se la redazione invia solo la nuova settimana.
    if path.exists():
        old=json.loads(path.read_text())
        if old.get('stagione')==edition['stagione']:
            edition={**old,**edition,'giornate':{**old.get('giornate',{}),**edition['giornate']}}
            validate(edition,ctx)
    text=json.dumps(edition,ensure_ascii=False,indent=2)+'\n'
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists() or path.read_text()!=text:path.write_text(text)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('azione',choices=['prepara','controlla']);p.add_argument('--sito',type=Path,required=True);p.add_argument('--derby',type=Path,required=True);p.add_argument('--stagione',default='2026/27');p.add_argument('--file',type=Path,default=ROOT/'redazione/tifosi.json');p.add_argument('--pubblica',type=Path);args=p.parse_args()
    ctx,raw=context(args.sito,json.loads(args.derby.read_text()),args.stagione)
    if args.azione=='prepara':
        for g in ctx['giornate']:g['chiude']=deadline(raw,g['giornata'],ctx['stagione'])
        out=ROOT/'redazione/tifosi-dossier.json';out.write_text(json.dumps(ctx,ensure_ascii=False,indent=2)+'\n');print(out);return
    edition=json.loads(args.file.read_text());validate(edition,ctx)
    if args.pubblica:publish(edition,ctx,args.pubblica)
    print('Racconti, candidature, giuria e impronte verificati.')


if __name__=='__main__':main()
