#!/usr/bin/env python3
"""Risultati completi, scelte editoriali, priorità e assenza di duplicazioni."""
import copy
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'calcoli'))
import zone_classifica as z
squadre=[f'Squadra {i}' for i in range(10)]
def calendario(turni):
    return {'teams':[{'name':t} for t in squadre], 'cal':{'lega':[{'n':n,'m':[[squadre[i],80-i,65-i,squadre[9-i],'3-0' if i==0 else '1-0'] for i in range(5)]} for n in range(1,turni+1)]}}
assert z.evento(calendario(1)) is None
assert z.evento(calendario(2)) is None
# Ultima reale è Squadra 5: tutte le perdenti hanno zero punti, decide il totale.
att={'squadre':{'Squadra 5':{'attesa':2}}}
e=z.evento(calendario(2),att)
assert e['tipo']=='sorpresa' and e['durata']==2
es=z.eventi(calendario(14),att)
assert len({e['giornata'] for e in es})==len(es)
assert len({e['chiave'] for e in es})==len(es)
crisi=[e['giornata'] for e in es if e['tipo']=='sorpresa']
assert all(b-a>=4 for a,b in zip(crisi,crisi[1:]))
assert all(e['canali']==['radio','girrr_sport','giornale','commenti','pdf'] for e in es)
assert any(e['tipo']=='vetta' for e in es), 'La vetta resta eleggibile dopo un’altra notizia'
for modifica in ('parziale','salto','duplicato','mancante'):
    d=calendario(3)
    if modifica=='parziale':d['cal']['lega'][2]['m'][0][4]='-'
    if modifica=='salto':d['cal']['lega'][2]['n']=4
    if modifica=='duplicato':d['cal']['lega'][2]['m'][1][0]=squadre[0]
    if modifica=='mancante':d['cal']['lega'][2]['m'].pop()
    assert len(z.storia(d))==2,modifica
# Scenari editoriali definiti da posizioni e distacchi; il motore di classifica è provato sopra.
def storia_ordini(ordini):
    return [{'giornata':i+1,'posizioni':{t:j+1 for j,t in enumerate(o)},'classifica':[{'t':t,'pt':20-j,'pos':j+1} for j,t in enumerate(o)]} for i,o in enumerate(ordini)]
base=squadre[:]
def verifica(ordini,tipo,asp=None):
    with patch.object(z,'storia',return_value=storia_ordini(ordini)):
        e=z.evento({},asp)
        assert e and e['tipo']==tipo,(tipo,e)
verifica([base]*3+[base[1:2]+base[:1]+base[2:]],'sorpasso')
r=base[:];r[-1],r[-2]=r[-2],r[-1]
verifica([base]*3+[r],'risalita')
r=base[:];r[2],r[4]=r[4],r[2]
verifica([base]*3+[r],'ingresso_podio')
# Rivelazione realmente definita da aspettative verificate, senza euristiche sui nomi.
with patch.object(z,'storia',return_value=storia_ordini([base]*3)):
    e=z.evento({}, {'squadre':{squadre[1]:{'attesa':7}}})
    assert e['tipo']=='rivelazione'
print('PASS cronache: giornate complete, crisi, rivelazione, sorpasso, risalita, podio, cooldown, chiavi e canali')
seconda=base[:];seconda[2],seconda[3]=seconda[3],seconda[2]
quarta=base[:];quarta[1],quarta[3]=quarta[3],quarta[1]
verifica([base,seconda,base,quarta],'uscita_podio')
hist=storia_ordini([base]*4)
hist[2]['classifica'][0]['pt']=25
with patch.object(z,'storia',return_value=hist):
    assert z.evento({})['tipo']=='lotta_scudetto'
print('PASS uscita dal podio e riapertura lotta scudetto')
