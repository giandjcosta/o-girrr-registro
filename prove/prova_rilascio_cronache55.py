#!/usr/bin/env python3
"""Collegamenti reali del pacchetto, eseguiti solo su copie senza publisher/audio."""
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R/'rilascio'))
from cronache55 import prepara
PAC = R/'rilascio/cronache55'
FIX = R/'lab/cronache-prova/prova-dda1bc9a84fd84fa'
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    for ramo in ('main', 'gh-pages'):
        shutil.copytree(PAC/ramo, root/ramo)
        subprocess.run(['git', 'apply', '--reverse', str(PAC/(ramo+'.patch'))], cwd=root/ramo, check=True)
    prima = {p:p.read_bytes() for p in root.rglob('*') if p.is_file()}
    m = prepara(root/'main', root/'gh-pages', root/'pacchetto')
    assert len(m['file']) == 11 and m['push'] is False and m['audio'] is False
    assert all(p.read_bytes()==v for p,v in prima.items())
    for ramo in ('main','gh-pages'):
        subprocess.run(['git','apply','--check',str(root/'pacchetto'/(ramo+'.patch'))],cwd=root/ramo,check=True)
        subprocess.run(['git','apply',str(root/'pacchetto'/(ramo+'.patch'))],cwd=root/ramo,check=True)
    sito = root/'gh-pages'
    (sito/'girrr/dati').mkdir(parents=True)
    shutil.copyfile(FIX/'data.json', sito/'data.json')
    snapshot = json.loads((FIX/'radio-dati.json').read_text())
    for key in ('cronache_classifica_attive','zona_classifica','cronaca_classifica'):
        snapshot.pop(key,None)
    (sito/'girrr/dati/lab-dati.json').write_text(json.dumps(snapshot))
    (root/'eventi.json').write_text('[]')
    (root/'moviola.json').write_text('{}')
    # Dipendenza già esistente sul main del sito, estranea alla patch.
    shutil.copyfile(R/'calcoli/nomi.json',root/'main/calcoli/nomi.json')
    # Si eseguono esclusivamente le righe di PREPARAZIONE estratte dai workflow.
    def comando(nome, cerca):
        testo = (root/'main/.github/workflows'/nome).read_text()
        return shlex.split(next(x.strip() for x in testo.splitlines() if cerca in x).split(' >> ')[0])
    args = comando('radio-giornata.yml','--cronache-classifica >>')
    args[1:4] = [str(R/'voci-src/prepara_dati.py'),str(sito),str(root/'eventi.json')]
    subprocess.run(args+['--uscita',str(root/'radio')],check=True,capture_output=True)
    radio = json.loads((root/'radio/dati.json').read_text())
    assert radio['cronache_classifica_attive'] and radio['zona_classifica']
    args = comando('dopo-giornata.yml','python3 code/calcoli/post_curva.py ')
    args[1:6] = [str(root/'main/calcoli/post_curva.py'),str(root/'eventi.json'),
                 str(root/'posts.json'),str(root/'moviola.json'),str(sito/'data.json')]
    subprocess.run(args,check=True,capture_output=True)
    post = json.loads((root/'posts.json').read_text())
    assert len(post)==3 and all(x['cronaca']==radio['zona_classifica']['chiave'] for x in post)
    # Il generatore preparato include la storia da solo: nessun monkeypatch/adattatore.
    shutil.copyfile(FIX/'scripts/toto_quote.py',sito/'scripts/toto_quote.py')
    codice = '''import importlib.util,json,sys
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p/'scripts'))
spec=importlib.util.spec_from_file_location('giornale',p/'scripts/pdf_giornale.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t={'classifiche':'Il commento originale.'}
h,n=g.costruisci(t)
assert t=={'classifiche':'Il commento originale.'}
(p/'giornale.html').write_text(h)
(p/'giornata.json').write_text(json.dumps(n))
'''
    for parziale in (False,True):
        if parziale:
            d=json.loads((sito/'data.json').read_text())
            prossimo=next(g for g in d['cal']['lega'] if g['n']>radio['aw'][-1]['n'])
            prossimo['m'][0][4]='2-1'
            (sito/'data.json').write_text(json.dumps(d))
        subprocess.run([sys.executable,'-c',codice,str(sito)],check=True)
        assert json.loads((sito/'giornata.json').read_text())==radio['aw'][-1]['n']
        assert (sito/'giornale.html').read_text().count(radio['zona_classifica']['testo'])==1
    # Aggiornamenti concorrenti del sito richiedono una nuova integrazione esplicita.
    (root/'main/calcoli/post_curva.py').write_text('# Modifica successiva da preservare\n')
    try:
        prepara(root/'main',root/'gh-pages',root/'altra-uscita')
    except ValueError:
        pass
    else:
        raise AssertionError('Sorgente cambiato sovrascritto senza verifica')
print('PASS rilascio: patch applicabili, chiamanti attivi, chiave comune, PDF automatico e turno parziale; nessun invio/audio')
