#!/usr/bin/env python3
"""Prova offline del pacchetto: ripetibilità, attesa e protezione degli input."""
import json
import sys
import tempfile
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R/'calcoli'))
sys.path.insert(0, str(R/'prove'))
from prepara_cronache import prepara
from prova_zone_classifica import calendario

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    sito = root/'sito'
    (sito/'girrr/dati').mkdir(parents=True)
    snapshot = json.loads((R/'prove/fixture-radio-compatibilita.json').read_text())['dati']
    snapshot['aw'][-1]['n'] = 3
    (sito/'data.json').write_text(json.dumps(calendario(3)))
    (sito/'girrr/dati/lab-dati.json').write_text(json.dumps(snapshot))
    ev, testi = root/'eventi.json', root/'testi.json'
    ev.write_text('[]'); testi.write_text('{"classifiche":"Il commento originale."}')
    iniziali = {p:p.read_bytes() for p in sito.rglob('*.json')}
    prima = prepara(sito, ev, testi, root/'uscita')
    nomi = ['manifest.json', 'post-curva.json', 'radio-copione.txt', 'testi-giornale.json']
    contenuti = {n:(prima/n).read_bytes() for n in nomi}
    seconda = prepara(sito, ev, testi, root/'uscita')
    assert prima == seconda and contenuti == {n:(seconda/n).read_bytes() for n in nomi}
    assert len(json.loads((prima/'post-curva.json').read_text())) == 3
    assert all(p.read_bytes()==v for p,v in iniziali.items())
    # Un calcolo vecchio ferma tutto il pacchetto, senza riutilizzare i post precedenti.
    snapshot['aw'][-1]['n'] = 2
    (sito/'girrr/dati/lab-dati.json').write_text(json.dumps(snapshot))
    attesa = prepara(sito, ev, testi, root/'uscita')
    assert attesa != prima
    assert json.loads((attesa/'manifest.json').read_text())['stato'] == 'in_attesa'
    assert not (attesa/'post-curva.json').exists()
    # G2 completa ma senza storia: nessun post aggiunto, copione comunque valido.
    (sito/'data.json').write_text(json.dumps(calendario(2)))
    quiete = prepara(sito, ev, testi, root/'uscita')
    assert json.loads((quiete/'post-curva.json').read_text()) == []
    assert json.loads((quiete/'testi-giornale.json').read_text()) == json.loads(testi.read_text())
    estranea = root/'estranea'; estranea.mkdir(); (estranea/'da-preservare.txt').write_text('Intatto')
    for destinazione in (sito/'output', estranea):
        try:
            prepara(sito, ev, testi, destinazione)
        except ValueError:
            pass
        else:
            raise AssertionError('Destinazione non sicura accettata')
    assert (estranea/'da-preservare.txt').read_text() == 'Intatto'
print('PASS pacchetto: idempotenza, input intatti, attesa, nessuna notizia, destinazioni protette')
