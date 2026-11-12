"""Controlla versione unica, archivio completo e protezione della copia pubblicata."""
import hashlib
import json
from pathlib import Path
import subprocess

R = Path(__file__).resolve().parents[1]
state = json.loads((R / 'registro-stato.json').read_text())
versions = json.loads((R / 'rilascio/versioni/versioni.json').read_text())['versioni']
assert state['versione'] == versions[0]['v']
assert json.loads((R / 'anteprima/pubblicata/versioni.json').read_text())['versioni'] == versions
archive = (R / 'archivio.html').read_text()
for v in versions:
    assert 'id="v' + v['v'] + '"' in archive
wrapper = (R / 'ufficiale/index.html').read_text()
assert 'Anteprima ' + state['versione'] in wrapper and 'anteprima/pubblicata.js' in wrapper
for path in (R / 'anteprima/pubblicata').rglob('*.html'):
    text = path.read_text()
    first = text.lower().find('<script')
    assert first >= 0 and 'sola-lettura.js' in text[first:text.find('</script>', first)], path
    assert 'data-goatcounter' not in text, path
# La build ripetuta deve essere deterministica e non riportare l'ingresso alla 5.5.
paths = list((R / 'anteprima').glob('*.html')) + list((R / 'anteprima/5.5').glob('*')) + [R / 'ufficiale/index.html']
def hashes():
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
before = hashes()
subprocess.run(['python3', 'anteprima/build.py'], cwd=R, check=True)
assert before == hashes(), 'Build non riproducibile'
print('PASS versione, archivio completo, ingresso corrente, protezione HTML e build riproducibile')
