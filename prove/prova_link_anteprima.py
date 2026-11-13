"""I collegamenti ereditati dal Lab puntano al Registro, senza cambiare le pagine reali."""
from pathlib import Path
import tempfile
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import sincronizza

with tempfile.TemporaryDirectory() as folder:
    root=Path(folder)/'registro';site=Path(folder)/'sito'
    (root/'lab').mkdir(parents=True);(site/'girrr').mkdir(parents=True)
    (root/'lab/prova.html').write_text('Prototipo')
    (site/'girrr/tabellone.html').write_text('Pagina pubblicata')
    source=site/'girrr/app.html'
    original='''<a href="../ufficiale/">Anteprima</a><a href="prova.html?skin=lega&amp;team=1#storia">Prova</a><a href="tabellone.html#lega">Tabellone</a><a href="mancante.html">Sconosciuta</a><a href="https://example.com/ufficiale/">Esterno</a>'''
    with patch.object(sincronizza,'ROOT',root):
        result=sincronizza.collega_pagine_registro(original,source,site)
        assert 'href="/o-girrr-registro/ufficiale/"' in result
        assert 'href="/o-girrr-registro/lab/prova.html?skin=lega&amp;team=1#storia"' in result
        assert 'href="tabellone.html#lega"' in result
        assert 'href="mancante.html"' in result
        assert 'href="https://example.com/ufficiale/"' in result
        assert sincronizza.collega_pagine_registro(result,source,site)==result
print('PASS link al Registro, query e hash, pagine reali preservate, destinazioni sconosciute non inventate e idempotenza')
