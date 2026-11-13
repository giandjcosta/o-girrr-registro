"""Copia di revisione autonoma della mappa; non è il file da pubblicare sul sito."""
import argparse
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(output, data_path=ROOT / 'ramificazioni-dati.json'):
    text = (ROOT / 'ramificazioni.html').read_text()
    text = text.replace('<head>', '<head><base href="https://giandjcosta.github.io/o-girrr-registro/">')
    for name in ['stile.css', 'ramificazioni.css']:
        text = text.replace(f'<link rel="stylesheet" href="{name}">', '<style>' + (ROOT / name).read_text() + '</style>')
    logo = base64.b64encode((ROOT / 'logo-lega.png').read_bytes()).decode()
    text = text.replace('src="logo-lega.png"', 'src="data:image/png;base64,' + logo + '"')
    text = text.replace('<h2>Due repository.', '<p>Anteprima locale · La pagina del Registro sarà disponibile al rilascio.</p><h2>Due repository.')
    js = (ROOT / 'ramificazioni.js').read_text()
    js = js.replace("new URL('./',document.currentScript.src)", "new URL('https://giandjcosta.github.io/o-girrr-registro/')")
    data = json.dumps(json.loads(data_path.read_text()), ensure_ascii=True).replace('</', '<\\/')
    js = js.replace('let data,busy=false;', 'let data=' + data + ',busy=false;')
    js = js.replace('});load();setInterval(', '});draw();load();setInterval(')
    assert 'draw();load();setInterval(' in js
    text = text.replace('<script src="ramificazioni.js" defer></script>', '')
    text = text.replace('</body>', '<script>' + js.replace('</script', '<\\/script') + '</script></body>')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text)
    print(output, '·', output.stat().st_size, 'byte')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output', type=Path, nargs='?', default=ROOT / 'consegna/ramificazioni.html')
    p.add_argument('--dati', type=Path, default=ROOT / 'ramificazioni-dati.json')
    args = p.parse_args()
    main(args.output, args.dati)
