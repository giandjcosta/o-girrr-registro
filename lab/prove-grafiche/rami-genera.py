# Claude, 13 novembre 2026: albero dei rami per lab/prove-grafiche/rami-alternative.html. Uso: python3 rami-genera.py USCITA.json (con i due repository clonati accanto)
# Albero dei rami da Git: per ogni ramo, il ramo da cui è nato (il punto di separazione più recente), data, autore, stato.
import subprocess, json, sys, time
def g(repo, *a): return subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True).stdout.strip()
def albero(repo, nome, escludi=('chatgpt/dati-ramificazioni',)):
    refs = [r for r in g(repo, 'for-each-ref', '--format=%(refname:short)', 'refs/remotes/origin').split('\n') if r and r != 'origin/HEAD' and not r.endswith(escludi)]
    names = [r[len('origin/'):] for r in refs]
    head = {n: g(repo, 'rev-parse', 'origin/' + n) for n in names}
    ts = lambda sha: int(g(repo, 'show', '-s', '--format=%ct', sha))
    info = {}
    for n in names:
        h = head[n]; d, a, s = g(repo, 'show', '-s', '--format=%ct%x1f%an%x1f%s', h).split('\x1f')
        info[n] = {'nome': n, 'punta': h[:7], 'data': int(d), 'titolo': s[:110], 'autore': (s.split(':')[0] if ':' in s[:20] else a)}
    tronco = 'main' if 'main' in names else names[0]
    # nascita: il commit più vecchio del ramo che non è nel tronco (se non ce n'è, il punto di separazione)
    for n in names:
        if n in (tronco, 'gh-pages'): info[n]['b'] = 0; continue
        prim = g(repo, 'rev-list', '--reverse', 'origin/%s..origin/%s' % (tronco, n)).split('\n')[0]
        info[n]['b'] = ts(prim) if prim else ts(g(repo, 'merge-base', 'origin/' + n, 'origin/' + tronco) or head[n])
    radici = [x for x in (tronco, 'gh-pages') if x in names]
    for n in names:
        if n in radici: info[n].update(padre=None, nascita=None, avanti=0, indietro=0, stato='principale'); continue
        best = None
        for p in names:
            if p == n or (p not in radici and (info[p]['b'], p) >= (info[n]['b'], n)): continue   # il padre è nato prima
            mb = g(repo, 'merge-base', 'origin/' + n, 'origin/' + p)
            if not mb or mb == head[n]: continue          # ramo già contenuto in p: p non è il padre
            t = ts(mb)
            # a parità di punto preferisci main, poi il ramo con la punta più vecchia (nato prima)
            key = (t, p in radici, -info[p]['data'])
            if best is None or key > best[0]: best = (key, p, mb)
        if best is None:
            mb = g(repo, 'merge-base', 'origin/' + n, 'origin/' + tronco)
            best = ((0,), tronco, mb)
        p, mb = best[1], best[2]
        dentro = any(subprocess.run(['git', '-C', repo, 'merge-base', '--is-ancestor', head[n], 'origin/' + t]).returncode == 0 for t in radici)
        av = int(g(repo, 'rev-list', '--count', 'origin/%s..origin/%s' % (p, n)) or 0)
        info[n].update(padre=p, nascita=mb[:7] if mb else None, dataNascita=ts(mb) if mb else None, avanti=av,
                       stato='unito' if dentro else ('attivo' if time.time() - info[n]['data'] < 7 * 86400 else 'fermo'))
    return {'repo': nome, 'tronco': tronco, 'radici': radici, 'rami': sorted(info.values(), key=lambda r: r['data'])}
out = [albero('/home/user/o-fant-a-girrr', 'o-fant-a-girrr'), albero('/home/user/o-girrr-registro', 'o-girrr-registro')]
for r in out:
    for b in r['rami']: b.pop('b', None)
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
for r in out:
    figli = {}
    for b in r['rami']:
        figli.setdefault(b['padre'], []).append(b['nome'])
    sub = [b['nome'] + ' ← ' + b['padre'] for b in r['rami'] if b['padre'] not in (None, r['tronco'])]
    print(r['repo'], len(r['rami']), 'rami;', sum(b['stato'] == 'attivo' for b in r['rami']), 'in corso;', len(sub), 'sotto-rami')
    print('  ', '\n   '.join(sub[:12]))
