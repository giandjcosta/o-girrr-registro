"""Solo copione testuale da una copia del sito: nessun generatore vocale."""
from pathlib import Path
import argparse,json,random,sys,tempfile
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r/'voci-src'))
import copione,prepara_dati
p=argparse.ArgumentParser();p.add_argument('sito',type=Path);a=p.parse_args();out=r/'lab/coordinamento-62'
with tempfile.TemporaryDirectory() as td:
    w=Path(td);eventi=a.sito/'calcoli/eventi.json'
    if not eventi.exists():
        eventi=w/'eventi.json';eventi.write_text('[]')
    prepara_dati.main([str(a.sito),str(eventi),'--uscita',str(w/'radio'),'--rifai','--cronache-classifica'])
    d=json.loads((w/'radio/dati.json').read_text());conf=json.loads((w/'radio/conferenze.json').read_text());curva=json.loads((w/'radio/curva.json').read_text())
nomi=json.loads((r/'voci-src/nomi.json').read_text());n=d['aw'][-1]['n'];regole=json.loads((r/'voci-src/regole.json').read_text())
base=copione.build(d,random.Random(n),{},nomi,conf,curva,regole)
d['mvp_tifosi']=json.loads((out/'mvp-reale.json').read_text())['votazione'];dopo=copione.build(d,random.Random(n),{},nomi,conf,curva,regole)
aggiunta=dopo[-3];assert dopo[:-3]+dopo[-2:]==base
(out/'radio-copione.txt').write_text(f'RADIO 6.2 · SOLO TESTO · {n}ª giornata · Nessun audio generato\n\nCONFRONTO PRIMA\n'+'\n'.join(nomi.get(k,k)+': '+t for k,t,_ in base[-3:])+'\n\nCONFRONTO DOPO\n'+nomi[aggiunta[0]]+': [UNICA BATTUTA AGGIUNTA] '+aggiunta[1]+'\n'+'\n'.join(nomi.get(k,k)+': '+t for k,t,_ in dopo[-2:])+'\n\nCOPIONE COMPLETO DI PROVA\n'+'\n\n'.join(nomi.get(k,k)+': '+('[AGGIUNTA] ' if i==len(dopo)-3 else '')+t for i,(k,t,_) in enumerate(dopo))+'\n')
print('Copione pronto',len(base),len(dopo),'battute, giornata',n)
