#!/usr/bin/env python3
"""6.5 · Correzioni di sistema per Lega e Stadio, senza pubblicare (ChatGPT, 18 novembre 2026).
Uso: python3 rilascio/r65/ritocchi.py COPIA_GH_PAGES_6_5
Si esegue DOPO r65/applica.py e r65/evento.py; può essere usato sul Lab già rigenerato.
Tutte le modifiche sono sostituzioni ESATTE; prima controlla tutti i file e poi scrive.
Seconda esecuzione: 0 file cambiati.
"""
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
PATCHES=json.loads((pathlib.Path(__file__).with_name('ritocchi-patches.json')).read_text(encoding='utf-8'))
def main(args):
    if len(args)!=1:raise SystemExit(__doc__)
    base=pathlib.Path(args[0])
    if not (base/'pillole.js').is_file() or 'NOSCIVOLO' not in (base/'pillole.js').read_text(encoding='utf-8'):
        raise SystemExit('Prima applicare r65/applica.py sulla copia di gh-pages')
    changed={}
    for rel,pairs in PATCHES.items():
        f=base/rel
        if not f.is_file():raise SystemExit('File mancante: '+str(f))
        t=f.read_text(encoding='utf-8')
        for a,b in pairs:
            if a==b:raise SystemExit(rel+': sostituzione identica')
            if b in t and a not in t:continue
            n=t.count(a)
            if n!=1:raise SystemExit(rel+': testo atteso '+str(n)+' volte: '+a[:85])
            t=t.replace(a,b)
        if t!=f.read_text(encoding='utf-8'):changed[f]=t
    for f,t in changed.items():f.write_text(t,encoding='utf-8')
    print('6.5 · File cambiati:',len(changed))
if __name__=='__main__':main(sys.argv[1:])
