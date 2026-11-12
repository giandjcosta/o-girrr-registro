"""Un nuovo rilascio aggiorna tutti gli ingressi senza modificare il Laboratorio."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO))
spec = importlib.util.spec_from_file_location('sync_registro', REPO / 'sincronizza.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

with tempfile.TemporaryDirectory() as tmp:
    root, site = Path(tmp) / 'registro', Path(tmp) / 'sito'
    (root / 'anteprima/sorgenti').mkdir(parents=True)
    (root / 'anteprima/sorgenti/involucro.html').write_text((REPO / 'anteprima/sorgenti/involucro.html').read_text())
    (root / 'README.md').write_text('Versione online sul sito vero: **5.3**.\n\nPrototipi da conservare.\n')
    (root / 'lab').mkdir()
    (root / 'lab/index.html').write_text('Lavoro sperimentale di un altro autore')
    for n in ('index.html', 'aggiornamenti.html'):
        (root / n).write_text('<a href="ufficiale/">Anteprima 5.5</a><a href="lab/versione-5-3.html">Archivio 5.3</a>')
    site.mkdir()
    def git(*args): subprocess.run(['git','-C',str(site),*args],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    git('init');git('config','user.name','Prova');git('config','user.email','prova@example.invalid')
    (site / 'index.html').write_text('<!doctype html><head><script>window.originale=true</script></head>')
    versions=[]
    with patch.object(sync,'ROOT',root):
        for v in ('5.8.1','5.9'):
            versions.insert(0,{'v':v,'data':'2026-11-12','titolo':'Rilascio di prova','novita':[]})
            (site / 'versioni.json').write_text(json.dumps({'versioni':versions}))
            git('add','.');git('commit','-m','Prova '+v)
            sync.sincronizza(site)
            assert json.loads((root / 'registro-stato.json').read_text())['versione']==v
            assert 'Anteprima '+v in (root / 'ufficiale/index.html').read_text()
            assert 'Anteprima '+v in (root / 'index.html').read_text()
            assert '**'+v+'**' in (root / 'README.md').read_text()
            before={p.relative_to(root):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            sync.sincronizza(site)
            assert before=={p.relative_to(root):p.read_bytes() for p in root.rglob('*') if p.is_file()},'Seconda esecuzione modifica il risultato'
        assert all('id="v'+v+'"' in (root / 'archivio.html').read_text() for v in ('5.8.1','5.9'))
        assert (root / 'lab/index.html').read_text()=='Lavoro sperimentale di un altro autore'
print('PASS nuovo rilascio, storico conservato, Lab intatto e sincronizzazione idempotente')
