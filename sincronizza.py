#!/usr/bin/env python3
"""Allinea il Registro al checkout gh-pages del sito, senza toccare Lab o rami altrui.

python3 sincronizza.py --sito /percorso/checkout-gh-pages
Genera la copia in sola lettura, versione, archivio e ingressi. Non pubblica da solo.
"""
import argparse
from datetime import date
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urljoin, urlsplit, unquote

ROOT = Path(__file__).resolve().parent
LIVE = 'https://giandjcosta.github.io/o-fant-a-girrr/'
MIRROR = '/o-girrr-registro/anteprima/pubblicata/'

def scrivi(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')

def pagina(titolo, body):
    return ('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex"><link rel="stylesheet" href="stile.css"><link rel="stylesheet" href="archivio.css">'
            '<style>*{box-sizing:border-box}body{margin:0;padding:20px;font-family:Inter,system-ui,sans-serif;color:#fbf6ec;background:#1d2a52}main{max-width:900px;margin:auto}nav{display:flex;flex-wrap:wrap;gap:16px}a{color:#ffd166}article{margin:18px 0;padding:18px;border:1px solid #7888a8;border-radius:12px}h1{font-size:clamp(26px,6vw,42px)}h2{overflow-wrap:anywhere}li{margin:8px 0}</style>'
            '<script src="registro-ingresso.js" data-sezione="archivio" defer></script><title>' + html.escape(titolo) + ' · O Girrr</title><main><nav><a href="./">Changelog</a><a href="aggiornamenti.html">Aggiornamenti</a><a href="ufficiale/">Anteprima</a><a href="archivio.html">Archivio</a><a href="lab/">Laboratorio</a></nav>' + body + '</main></html>\n')

def genera_archivio(versions):
    """Schede delle versioni; la prima aperta, lo storico consultabile senza JS."""
    latest = versions[0]
    months = ('gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre')
    cards = []
    for index, version in enumerate(versions):
        number = html.escape(version['v'])
        raw_date = version.get('data') or 'Dato non conservato'
        try:
            day = date.fromisoformat(raw_date)
            when = f'<time datetime="{day.isoformat()}">{day.day} {months[day.month - 1]} {day.year}</time>'
        except (ValueError, TypeError):
            when = '<span>' + html.escape(str(raw_date)) + '</span>'
        areas = version.get('novita', [])
        details = ''.join('<section class="release-area"><h3>' + html.escape(area['area']) + '</h3><ul>' + ''.join('<li>' + html.escape(text) + '</li>' for text in area['voci']) + '</ul></section>' for area in areas)
        if not details:
            details = '<p>I dettagli di questa versione non sono conservati.</p>'
        cards.append('<article class="release-card' + (' release-latest' if index == 0 else '') + '" id="v' + number + '"><details' + (' open' if index == 0 else '') + '><summary><span class="release-version">' + number + '</span><span class="release-heading"><strong>' + html.escape(version.get('titolo', 'Versione ' + version['v'])) + '</strong><span class="release-meta">' + when + (' · ' + str(len(areas)) + ' aree aggiornate' if areas else '') + '</span></span>' + ('<span class="release-live">Ultima versione</span>' if index == 0 else '') + '<span class="release-chevron" aria-hidden="true">⌄</span></summary><div class="release-content"><h2 class="sr-only">Novità della ' + number + '</h2>' + details + '</div></details></article>')
    body = '<header class="archive-heading"><div><p class="archive-kicker">La storia di O Girrr</p><h1>Archivio delle versioni</h1><p>Apri una versione per ritrovare le novità, divise per area.</p></div><div class="archive-current"><span>Ultima versione online</span><strong>' + html.escape(latest['v']) + '</strong></div></header>'
    body += '<div class="release-list">' + ''.join(cards) + '</div>'
    body += '<section class="archive-prototypes"><h2>Prototipi storici</h2><p>Le prove delle versioni precedenti rimangono consultabili nel Laboratorio.</p><div>' + ''.join('<a href="lab/' + name + '">' + html.escape(name.replace('versione-', '').replace('.html', '').replace('-', '.')) + '<span aria-hidden="true"> ↗</span></a>' for name in ('versione-5.html', 'versione-5-1.html', 'versione-5-2.html', 'versione-5-3.html')) + '</div></section>'
    return pagina('Archivio', body)

def collega_pagine_registro(text, source, site):
    """I vecchi link al Lab vanno al Registro, non a pagine mancanti nel mirror."""
    canonical = {'ufficiale/', 'ufficiale/index.html', 'archivio.html', 'aggiornamenti.html'}
    origin = urlsplit(LIVE)
    registry = MIRROR.removesuffix('anteprima/pubblicata/')
    def fix(match):
        href = html.unescape(match[3])
        if any(c in href for c in ('+', '{', '}', '$')):
            return match[0]
        target = urlsplit(urljoin(LIVE + source.relative_to(site).as_posix(), href))
        if target.netloc != origin.netloc or not target.path.startswith(origin.path):
            return match[0]
        relative = unquote(target.path.removeprefix(origin.path))
        published = (site / relative).resolve()
        if published.is_relative_to(site) and (published.is_file() or (published / 'index.html').is_file()):
            return match[0]
        local = relative.removeprefix('stadio/')
        candidates = [local]
        if local.startswith('girrr/'):
            candidates.append('lab/' + local.removeprefix('girrr/'))
        for candidate in candidates:
            path = (ROOT / candidate).resolve()
            if not path.is_relative_to(ROOT):
                continue
            if candidate in canonical or path.is_file() or (path / 'index.html').is_file():
                url = registry + candidate + ('?' + target.query if target.query else '') + ('#' + target.fragment if target.fragment else '')
                return match[1] + match[2] + html.escape(url, quote=True) + match[2]
        return match[0]
    return re.sub(r'(<a\b[^>]*?\bhref=)(["\x27])([^"\x27]+)\2', fix, text, flags=re.I)

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
            if src.suffix == '.html':
                text = collega_pagine_registro(text, src, site)
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
    scrivi(ROOT / 'archivio.html', genera_archivio(versions))
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
    text = re.sub(r'Versione online sul sito vero:.*?(?=\n\n)', 'Versione online sul sito vero: **' + latest['v'] + '**. Anteprima corrente: copia in sola lettura della stessa versione; i prototipi restano nel Laboratorio. Allineamento automatico dopo le modifiche al Lab e sincronizzazione ogni 7 giorni, subito se esce una versione nuova (gli orari GitHub possono slittare).', text, flags=re.S)
    scrivi(readme, text)
    print('Registro allineato alla ' + latest['v'] + ' · Sito ' + sha[:7] + ' · ' + str(len(files)) + ' file in sola lettura')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sito', required=True, type=Path)
    sincronizza(p.parse_args().sito.resolve())
