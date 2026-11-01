#!/usr/bin/env python3
"""La Radio attuale, letta dal Registro, non cambia senza attivazione esplicita."""
import copy
import hashlib
import importlib.util
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R/'voci-src'))
spec = importlib.util.spec_from_file_location('copione', R/'voci-src/copione.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
fixture = json.loads((R/'prove/fixture-radio-compatibilita.json').read_text())
for seed, digest in enumerate(fixture['sha256_copioni']):
    d = copy.deepcopy(fixture['dati'])
    # Anche un campo aggiunto per errore non attiva la novità senza il flag.
    d['zona_classifica'] = {'testo':'TEST DA NON TRASMETTERE', 'canali':['radio']}
    b = c.build(d, random.Random(seed), [])
    assert hashlib.sha256(json.dumps(b, ensure_ascii=False).encode()).hexdigest() == digest, seed
print('PASS Radio attuale: 32 copioni identici alla versione precedente, attivazione esplicita richiesta')

sys.path.insert(0, str(R/'prove'))
from prova_zone_classifica import calendario
sys.path.insert(0, str(R/'calcoli'))
from zone_classifica import evento
with tempfile.TemporaryDirectory() as tmp:
    t = Path(tmp)
    (t/'eventi.json').write_text('[]')
    (t/'moviola.json').write_text('{}')
    (t/'data.json').write_text(json.dumps(calendario(3)))
    args = [sys.executable, str(R/'calcoli/post_curva.py'), str(t/'eventi.json'),
            str(t/'post.json'), str(t/'moviola.json'), str(t/'data.json')]
    subprocess.run(args, check=True, capture_output=True)
    assert json.loads((t/'post.json').read_text()) == []
    subprocess.run(args+['--cronache-classifica'], check=True, capture_output=True)
    assert len(json.loads((t/'post.json').read_text())) == 3
    e = evento(calendario(3), json.loads((R/'calcoli/aspettative.json').read_text()))
    e = dict(e, tema=e['tipo'], tipo='zona_classifica', k=e['chiave'])
    (t/'eventi.json').write_text(json.dumps([e,e]))
    subprocess.run(args, check=True, capture_output=True)
    assert json.loads((t/'post.json').read_text()) == []
    subprocess.run(args+['--cronache-classifica'], check=True, capture_output=True)
    assert len(json.loads((t/'post.json').read_text())) == 3
    site = t/'sito'
    (site/'girrr/dati').mkdir(parents=True)
    (site/'data.json').write_text((t/'data.json').read_text())
    snapshot = {'aw':[{'n':3}], 'cup':[], 'cronache_classifica_attive':True,
                'zona_classifica':{'testo':'STORIA DELLA PROVA'}}
    (site/'girrr/dati/lab-dati.json').write_text(json.dumps(snapshot))
    subprocess.run([sys.executable, str(R/'voci-src/prepara_dati.py'), str(site),
        str(t/'eventi.json'), '--uscita', str(t/'radio')], check=True, capture_output=True)
    pronto = json.loads((t/'radio/dati.json').read_text())
    assert 'cronache_classifica_attive' not in pronto and 'zona_classifica' not in pronto
print('PASS Curva: i nuovi testi sono preparati soltanto con il flag esplicito')
print('PASS prepara_dati pubblico: nessuna attivazione da un vecchio snapshot')
