"""Ingresso corrente; le pagine sperimentali della 5.5 restano consultabili."""
import json
import hashlib

def genera_cornice(root):
    state = root / 'registro-stato.json'
    if not state.exists():
        return
    version = json.loads(state.read_text())['versione']
    historic = (root / 'anteprima/sorgenti/involucro.html').read_text()
    (root / 'anteprima/storica55.html').write_text(historic)
    wrapper = historic.replace('Anteprima 5.5', 'Anteprima ' + version)
    script = root / 'anteprima/pubblicata.js'
    revision = hashlib.sha256(script.read_bytes()).hexdigest()[:12] if script.exists() else 'locale'
    wrapper = wrapper.replace('../anteprima/involucro.js?v=55h', '../anteprima/pubblicata.js?v=' + revision)
    wrapper = wrapper.replace('</nav><label', '<span style="font-size:11px;color:#bfe3ff;white-space:nowrap">Sola lettura</span></nav><label')
    wrapper = wrapper.replace('title="Anteprima"', 'title="Anteprima ' + version + ' · Sola lettura"')
    wrapper = wrapper.replace('</head>', '<script src="../registro-ingresso.js" data-sezione="anteprima" defer></script></head>')
    (root / 'ufficiale/index.html').write_text(wrapper)
