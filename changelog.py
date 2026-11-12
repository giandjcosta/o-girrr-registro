"""Aggiorna lo storico completo dei commit pubblicati, anche oltre le ultime 100 modifiche."""
import json
import os
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parent
NOISE = re.compile(r'^(risultati reali|aggiorna |riavvia|ripristina|rimuove cache|prova rete|merge|initial commit|tolgo la pagina novit|novità 4.5|sql prestiti)', re.I)

def aggiorna():
    out, page = [], 1
    while True:
        url = f'https://api.github.com/repos/giandjcosta/o-fant-a-girrr/commits?sha=gh-pages&per_page=100&page={page}'
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'O-Girrr-Registro'}
        if os.environ.get('GITHUB_TOKEN'):
            headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
            commits = json.load(response)
        out += [[c['commit']['committer']['date'], c['commit']['message'].split('\n')[0]] for c in commits]
        if len(commits) < 100:
            break
        page += 1
    out = [x for x in out if not NOISE.search(x[1])]
    if not out:
        raise ValueError('Storico vuoto: conservata la copia precedente')
    path = ROOT / 'index.html'
    text, count = re.subn(r'var SNAP=\[.*?\]\],AREE=', lambda m: 'var SNAP=' + json.dumps(out, ensure_ascii=False) + ',AREE=', path.read_text(), count=1, flags=re.S)
    if count != 1:
        raise ValueError('Snapshot non trovato: nessun file modificato')
    path.write_text(text)
    print(len(out), 'modifiche conservate, ultima:', out[0][0])

if __name__ == '__main__':
    aggiorna()
