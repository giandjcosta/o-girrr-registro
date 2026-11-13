#!/usr/bin/env python3
"""Snapshot dei due grafi Git. Nessun deploy, nessuna chiave nel JSON pubblico."""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parent
TECHNICAL = 'chatgpt/dati-ramificazioni'
REPOS = [('sito', 'giandjcosta/o-fant-a-girrr'), ('registro', 'giandjcosta/o-girrr-registro')]


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True, stderr=subprocess.PIPE).strip()


def commits(repo, ref, limit=40, first_parent=False):
    raw = git(repo, 'log', *(['--first-parent'] if first_parent else []), f'-{limit}', '--format=%H%x00%P%x00%cI%x00%aN%x00%s', ref)
    return [dict(zip(('sha', 'parents', 'date', 'author', 'title'), line.split('\0', 4))) for line in raw.splitlines() if line]


def clone(slug, directory):
    if not directory.exists():
        subprocess.run(['git', 'clone', '--bare', '--filter=blob:none', f'https://github.com/{slug}.git', str(directory)], check=True)
    else:
        subprocess.run(['git', '-C', str(directory), 'fetch', '--prune', '--filter=blob:none', 'origin', '+refs/heads/*:refs/heads/*'], check=True)
    return directory


def pull_requests(slug):
    """Metadati facoltativi; la provenienza della descrizione è sempre dichiarata."""
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'O-Girrr-Ramificazioni'}
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    url = f'https://api.github.com/repos/{slug}/pulls?state=all&sort=updated&direction=desc&per_page=100'
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=40) as response:
        return json.load(response)


def color(key):
    hue = int(hashlib.sha256(key.encode()).hexdigest()[:8], 16) % 36000 / 100
    return f'hsl({hue} 78% 68%)'


def collect(repo, key, slug, prs=None, notes=None, limit=40):
    notes = notes or {}
    refs = git(repo, 'for-each-ref', '--format=%(refname:short)%09%(objectname)', 'refs/heads').splitlines()
    refs = dict(line.split('\t') for line in refs if line)
    if 'main' not in refs:
        raise ValueError(f'{slug}: ramo main assente')
    prs_by_branch = {}
    for pr in prs or []:
        branch = pr['head']['ref']
        if branch not in prs_by_branch or pr['state'] == 'open':
            prs_by_branch[branch] = pr
    nodes, branches = {}, []
    for name, head in sorted(refs.items(), key=lambda item: (item[0] != 'main', item[0])):
        if name == TECHNICAL:
            continue
        history = commits(repo, name, limit)
        for c in history:
            c['parents'] = c['parents'].split()
            nodes[c['sha']] = c
        behind, ahead = map(int, git(repo, 'rev-list', '--left-right', '--count', f'main...{name}').split())
        try:
            base = git(repo, 'merge-base', 'main', name)
        except subprocess.CalledProcessError:
            base = None  # main e gh-pages possono avere storie indipendenti.
        if base and base not in nodes:
            c = commits(repo, base, 1)[0]
            c['parents'] = c['parents'].split()
            nodes[base] = c
        pr = prs_by_branch.get(name)
        note = notes.get(slug + ':' + name, {})
        branches.append({
            'name': name, 'head': head, 'base': base, 'ahead': ahead, 'behind': behind,
            'state': 'principale' if name == 'main' else 'pubblicato' if key == 'sito' and name == 'gh-pages' else 'integrato' if ahead == 0 and behind else 'allineato' if ahead == behind == 0 else 'in-lavoro',
            'color': '#ff6375' if key == 'sito' and name == 'main' else '#ffd166' if name == 'main' else color(slug + ':' + name),
            'title': note.get('title') or (pr or {}).get('title') or history[0]['title'],
            'description': note.get('description') or ('Pull request: ' + pr['title'] if pr else 'Ultimo commit: ' + history[0]['title']),
            'descriptionSource': 'Nota di progetto' if note else 'Pull request' if pr else 'Commit Git',
            'commits': [c['sha'] for c in history],
            'pr': {'number': pr['number'], 'url': pr['html_url'], 'state': 'merged' if pr.get('merged_at') else pr['state'], 'base': pr['base']['ref']} if pr else None,
        })
    for c in commits(repo, 'main', limit, first_parent=True):
        c['parents'] = c['parents'].split()
        nodes[c['sha']] = c
    order = git(repo, 'rev-list', '--topo-order', '--all').splitlines()
    trunk = git(repo, 'rev-list', '--first-parent', f'--max-count={limit}', 'main').splitlines()
    version, version_ref = None, 'gh-pages' if key == 'sito' else 'main'
    try:
        path = 'versioni.json' if key == 'sito' else 'registro-stato.json'
        v = json.loads(git(repo, 'show', version_ref + ':' + path))
        version = v['versioni'][0]['v'] if key == 'sito' else v['versione']
    except (subprocess.CalledProcessError, ValueError, KeyError, IndexError):
        pass
    return {'id': key, 'name': slug, 'url': f'https://github.com/{slug}', 'main': refs['main'], 'trunk': trunk,
            'publishedRef': version_ref, 'publishedSha': refs.get(version_ref), 'version': version,
            'branches': branches, 'nodes': nodes, 'order': [sha for sha in order if sha in nodes], 'limit': limit,
            'prMetadata': 'Disponibili' if prs is not None else 'Non disponibili: descrizioni dai commit'}


def save(path, repos):
    core = {'schema': 1, 'repositories': repos, 'technicalBranchExcluded': TECHNICAL}
    fingerprint = hashlib.sha256(json.dumps(core, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    if path.exists() and json.loads(path.read_text()).get('fingerprint') == fingerprint:
        return False
    core.update(fingerprint=fingerprint, updated=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'))
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False, encoding='utf-8') as f:
        json.dump(core, f, ensure_ascii=False, separators=(',', ':'))
        f.write('\n')
        temporary = Path(f.name)
    temporary.replace(path)
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache', type=Path, default=ROOT / '.rami-cache')
    p.add_argument('--output', type=Path, default=ROOT / 'ramificazioni-dati.json')
    p.add_argument('--sito', type=Path)
    p.add_argument('--registro', type=Path)
    p.add_argument('--senza-pr', action='store_true')
    args = p.parse_args()
    notes = json.loads((ROOT / 'ramificazioni-note.json').read_text())

    def one(item):
        key, slug = item
        repo = getattr(args, key) or clone(slug, args.cache / (key + '.git'))
        prs = None
        if not args.senza_pr:
            try:
                prs = pull_requests(slug)
            except Exception:
                print(slug + ': PR non disponibili; uso i metadati Git verificati.')
        return collect(repo, key, slug, prs, notes)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        repos = list(pool.map(one, REPOS))
    print('Snapshot aggiornato.' if save(args.output, repos) else 'Rami invariati; nessun file riscritto.')


if __name__ == '__main__':
    main()
