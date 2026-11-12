#!/usr/bin/env python3
"""Allinea il Registro al checkout gh-pages del sito, senza toccare Lab o rami altrui.

python3 sincronizza.py --sito /percorso/checkout-gh-pages
Genera la copia in sola lettura, versione, archivio e ingressi. Non pubblica da solo.
"""
import argparse
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
LIVE = 'https://giandjcosta.github.io/o-fant-a-girrr/'
MIRROR = '/o-girrr-registro/anteprima/pubblicata/'

def scrivi(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')

def pagina(titolo, body):
    return ('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex"><link rel="stylesheet" href="stile.css">'
            '<style>*{box-sizing:border-box}body{margin:0;padding:20px;font-family:Inter,system-ui,sans-serif;color:#fbf6ec;background:#1d2a52}main{max-width:900px;margin:auto}nav{display:flex;flex-wrap:wrap;gap:16px}a{color:#ffd166}article{margin:18px 0;padding:18px;border:1px solid #7888a8;border-radius:12px}h1{font-size:clamp(26px,6vw,42px)}h2{overflow-wrap:anywhere}li{margin:8px 0}</style>'
            '<title>' + html.escape(titolo) + ' · O Girrr</title><main><nav><a href="./">Changelog</a><a href="aggiornamenti.html">Aggiornamenti</a><a href="ufficiale/">Anteprima</a><a href="archivio.html">Archivio</a><a href="lab/">Laboratorio</a></nav>' + body + '</main></html>\n')

def sincronizza(site):
    versions_text = (site / 'versioni.json').read_text(encoding='utf-8')
    versions = json.loads(versions_text)['versioni']
    latest = versions[0]
    if not re.fullmatch(r'\d+(?:\.\d+){1,2}', latest['v']):
        raise ValueError('Numero di versione non valido')
    sha = subprocess.check_output(['git', '-C', str(site), 'rev-parse', 'HEAD'], text=True).strip()
    # Solo file pubblicati; niente workflow, SQL o strumenti di amministrazione.
    files = subprocess.check_output(['git', '-C', str(site), 'ls-files', '-z'], text=True).split('\0')
    files = [f for f in files if f and (f.split('/')[0] in {'assets', 'girrr', 'stadio', 'riepiloghi'} or
             ('/' not in f and Path(f).suffix in {'.html', '.js', '.css', '.json', '.png', '.webmanifest'}))]
    dest = ROOT / 'anteprima/pubblicata'
    expected = set(files)
    for name in files:
        src, out = site / name, dest / name
        if src.is_symlink():
            raise ValueError('Link simbolico non ammesso nella copia pubblicata')
        out.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in {'.html', '.js', '.css', '.json', '.webmanifest'}:
            text = src.read_text(encoding='utf-8')
            if src.suffix != '.json':
                text = text.replace(LIVE, MIRROR)
            if src.suffix == '.html':
                guard = os.path.relpath(ROOT / 'anteprima/sola-lettura.js', out.parent)
                tag = '<script src="' + guard + '"></script>'
                if re.search(r'<head\b', text, flags=re.I):
                    text = re.sub(r'(<head\b[^>]*>)', lambda m: m[0] + tag, text, count=1, flags=re.I)
                else:
                    text = re.sub(r'(<!doctype[^>]*>)', lambda m: m[0] + tag, text, count=1, flags=re.I) if '<!doctype' in text.lower() else tag + text
                text = re.sub(r'<script\b[^>]*\bdata-goatcounter[^>]*>.*?</script>', '', text, flags=re.S)
            scrivi(out, text)
        elif not out.exists() or src.read_bytes() != out.read_bytes():
            shutil.copyfile(src, out)
    # Pulizia limitata esclusivamente alla cartella generata, mai sorgenti o Lab.
    for out in dest.rglob('*'):
        if out.is_file() and out.relative_to(dest).as_posix() not in expected:
            out.unlink()
    for target in ('rilascio/versioni/versioni.json', 'ufficiale/src/sito/versioni.json'):
        scrivi(ROOT / target, versions_text)
    state = {'versione': latest['v'], 'data': latest['data'], 'commit_sito': sha,
             'fonte': 'giandjcosta/o-fant-a-girrr@gh-pages', 'anteprima': 'anteprima/pubblicata/girrr/index.html'}
    scrivi(ROOT / 'registro-stato.json', json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    entries = []
    for v in versions:
        details = ''.join('<h3>' + html.escape(a['area']) + '</h3><ul>' + ''.join('<li>' + html.escape(t) + '</li>' for t in a['voci']) + '</ul>' for a in v.get('novita', []))
        entries.append('<article id="v' + html.escape(v['v']) + '"><h2>' + html.escape(v['v'] + ' · ' + v.get('titolo', '')) + '</h2><p>' + html.escape(v.get('data', 'Dato non conservato')) + '</p>' + details + '</article>')
    body = '<h1>Archivio delle versioni</h1><p>Ultima versione online: <b>' + latest['v'] + '</b>. Le schede si aggiornano dai rilasci del sito; i prototipi del Laboratorio restano separati.</p>' + ''.join(entries)
    body += '<h2>Prototipi storici conservati</h2><p>' + ' · '.join('<a href="lab/' + n + '">' + html.escape(n.replace('versione-', '').replace('.html', '')) + '</a>' for n in ('versione-5.html', 'versione-5-1.html', 'versione-5-2.html', 'versione-5-3.html')) + '</p>'
    scrivi(ROOT / 'archivio.html', pagina('Archivio', body))
    from anteprima.cornice_pubblicata import genera_cornice
    genera_cornice(ROOT)
    for name in ('index.html', 'aggiornamenti.html'):
        path = ROOT / name
        text = path.read_text(encoding='utf-8')
        text = re.sub(r'(href="ufficiale/">)Anteprima[^<]*', r'\1Anteprima ' + latest['v'], text)
        text = re.sub(r'href="(?:lab/versione-[^"]+|archivio\.html)">Archivio[^<]*', 'href="archivio.html">Archivio', text)
        scrivi(path, text)
    readme = ROOT / 'README.md'
    text = readme.read_text()
    text = re.sub(r'Versione online sul sito vero:.*?(?=\n\n)', 'Versione online sul sito vero: **' + latest['v'] + '**. Anteprima corrente: copia in sola lettura della stessa versione; i prototipi restano nel Laboratorio. Allineamento automatico dopo le modifiche al Lab e controllo dei rilasci ogni 30 minuti (gli orari GitHub possono slittare).', text, flags=re.S)
    scrivi(readme, text)
    print('Registro allineato alla ' + latest['v'] + ' · Sito ' + sha[:7] + ' · ' + str(len(files)) + ' file in sola lettura')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sito', required=True, type=Path)
    sincronizza(p.parse_args().sito.resolve())
