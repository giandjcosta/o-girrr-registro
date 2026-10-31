#!/usr/bin/env python3
"""Pipeline preparatoria locale: post/commenti, testo Radio e adattatore PDF.

Nessun publisher, rete, database o generatore audio invocato.
"""
import importlib.util
import json
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
R=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(R/'calcoli'))
from giornale_classifica import integra
from zone_classifica import evento
spec=importlib.util.spec_from_file_location('zone_test',R/'prove/prova_zone_classifica.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
d=t.calendario(3);att={}
e=evento(d,att);assert e
originale={'classifiche':'Il commento della redazione.'}
out=integra(originale,d,att)
assert originale=={'classifiche':'Il commento della redazione.'}
assert out['classifiche'].count(e['testo'])==1
assert integra(out,d,att)==out
assert integra(originale,t.calendario(1))==originale
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);cal=root/'calcoli';cal.mkdir()
    for nome in ('post_curva.py','zone_classifica.py','nomi.json'):
        shutil.copy(R/'calcoli'/nome,cal/nome)
    (cal/'aspettative.json').write_text(json.dumps(att))
    (root/'eventi.json').write_text('[]');(root/'moviola.json').write_text('{}');(root/'data.json').write_text(json.dumps(d))
    args=[sys.executable,str(cal/'post_curva.py'),str(root/'eventi.json'),str(root/'post.json'),str(root/'moviola.json'),str(root/'data.json')]
    subprocess.run(args,check=True)
    posts=json.loads((root/'post.json').read_text());assert len(posts)==3
    assert [p['h'] for p in posts]==['girrr_sport','giornale_girrr','giornale_girrr']
    assert posts[2]['re']==posts[0]['chiave'] and posts[2]['re_h']=='girrr_sport'
    assert all(len(p['body'])<=280 for p in posts)
    subprocess.run(args,check=True);assert json.loads((root/'post.json').read_text())==posts
    (root/'data.json').write_text(json.dumps(t.calendario(2)))
    subprocess.run(args,check=True);assert json.loads((root/'post.json').read_text())==[]
# Il copione resta testo e include una sola volta la storia principale.
sys.path.insert(0,str(R/'voci-src'))
spec=importlib.util.spec_from_file_location('copione',R/'voci-src/copione.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
radio=json.loads((R/'voci-src/dati.json').read_text());radio['zona_classifica']=e
for seed in (0,1,7,13):
    battute=c.build(radio,random.Random(seed),[])
    testi=[x[1] for x in battute]
    assert testi.count(e['testo'])==1
    saluto=next(i for i,x in enumerate(battute) if x[0]=='S' and 'restituisco la linea' in x[1])
    assert not any(x[0]=='S' for x in battute[saluto+1:]),'Giulia parla dopo il saluto'
    assert not any('punti sul secondo!' in x or 'punti sul quarto:' in x for x in testi)
print('PASS pipeline preparatoria: GS + profilo Giornale + commento con parent, idempotenza, PDF e copione (4 semi), nessun audio')
# Preparazione Radio dalla chiusura: niente giornate saltate o snapshot dei calcoli vecchio.
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);v=root/'voci-src';v.mkdir();cal=root/'calcoli';cal.mkdir()
    for f in ('zone_classifica.py','aspettative.json'):shutil.copy(R/'calcoli'/f,cal/f)
    shutil.copy(R/'voci-src/prepara_dati.py',v/'prepara_dati.py')
    site=root/'site';(site/'girrr/dati').mkdir(parents=True);(site/'girrr/voci').mkdir()
    dati=t.calendario(3)
    for g in dati['cal']['lega']:g['sa']=g['n']+4
    (site/'data.json').write_text(json.dumps(dati));(root/'eventi.json').write_text('[]')
    snapshot={'aw':[{'n':3}],'cup':[]}
    (site/'girrr/dati/lab-dati.json').write_text(json.dumps(snapshot))
    args=[sys.executable,str(v/'prepara_dati.py'),str(site),str(root/'eventi.json')]
    ret=subprocess.check_output(args,text=True);assert 'giornata=3' in ret
    pronto=json.loads((v/'dati.json').read_text());assert pronto['zona_classifica']['giornata']==3
    assert pronto['zona_classifica']==pronto['cronaca_classifica']
    # Chiusura della Coppa nello stesso turno necessaria; nessun file nuova giornata scritto.
    dati['cal']['cup']=[{'n':1,'sa':7,'m':[['A','Squadra 0',0,0,'Squadra 1','-']]}]
    (site/'data.json').write_text(json.dumps(dati));assert 'giornata=\n' in subprocess.check_output(args,text=True)
    dati['cal']['cup']=[];dati['cal']['lega'][1]['m'][0][4]='-'
    (site/'data.json').write_text(json.dumps(dati));assert 'giornata=\n' in subprocess.check_output(args,text=True)
    # Una puntata in archivio non viene preparata di nuovo.
    dati=t.calendario(3);(site/'data.json').write_text(json.dumps(dati))
    (site/'girrr/voci/archivio.json').write_text('[{"tag":"Giornata 3"}]')
    assert 'giornata=\n' in subprocess.check_output(args,text=True)
print('PASS prepara_dati: calcoli allineati, cronaca comune, attesa Coppa, giornata parziale, archivio')
