#!/usr/bin/env python3
"""Prepara soltanto copie e patch locali per il futuro rilascio delle cronache.

Non applica file a checkout, non esegue workflow, publisher, build del sito o voci.
Le sorgenti MAIN e GH_PAGES sono copie aggiornate lette dal sito ufficiale.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parent.parent
BASE_POST = 'bb6a18c74c1dbc827a2215aacedce7fcd4d26bd7'
MODULI = ('zone_classifica.py', 'aspettative.json', 'giornale_classifica.py')
DOPO = '.github/workflows/dopo-giornata.yml'
RADIO = '.github/workflows/radio-giornata.yml'
PDF = 'scripts/pdf_giornale.py'
SETTIMANA = 'scripts/pdf_settimana.py'


def sostituisci(testo, prima, dopo):
    if dopo in testo:
        return testo
    if testo.count(prima) != 1:
        raise ValueError('Sorgente cambiato: controllare il collegamento '+prima[:100])
    return testo.replace(prima, dopo)


def blob(contenuto):
    return hashlib.sha1(b'blob '+str(len(contenuto)).encode()+b'\0'+contenuto).hexdigest()


def prepara(main, gh, uscita):
    main, gh, uscita = (Path(p).resolve() for p in (main, gh, uscita))
    for sorgente in (main, gh):
        if uscita == sorgente or sorgente in uscita.parents or uscita in sorgente.parents:
            raise ValueError('Uscita e sorgenti devono essere cartelle separate')
    marker = uscita/'.cronache55-pacchetto.json'
    if uscita.exists() and any(uscita.iterdir()) and not marker.exists():
        raise ValueError('Uscita non vuota ed estranea al pacchetto cronache')
    post = (main/'calcoli/post_curva.py').read_bytes()
    if blob(post) not in (BASE_POST, blob((R/'calcoli/post_curva.py').read_bytes())):
        raise ValueError('post_curva.py del sito è cambiato: integrare prima le sue novità nel Registro')
    # Anche moduli eventualmente già installati non vengono sovrascritti alla cieca.
    for nome in MODULI:
        for esistente in (main/'calcoli'/nome, gh/'scripts'/nome):
            if esistente.exists() and esistente.read_bytes() != (R/'calcoli'/nome).read_bytes():
                raise ValueError('Modulo del sito diverso: '+str(esistente))
    sorgenti = {('main', DOPO):(main/DOPO).read_text(),
                ('main', RADIO):(main/RADIO).read_text(),
                ('main', 'calcoli/post_curva.py'):post.decode(),
                ('gh-pages', PDF):(gh/PDF).read_text(),
                ('gh-pages', SETTIMANA):(gh/SETTIMANA).read_text()}
    nuovi = dict(sorgenti)
    comando = 'python3 code/calcoli/post_curva.py code/calcoli/eventi.json code/calcoli/post_curva.json code/calcoli/moviola.json site/data.json'
    nuovi['main', DOPO] = sostituisci(nuovi['main', DOPO], comando+'\n', comando+' --cronache-classifica\n')
    comando = 'python3 reg/voci-src/prepara_dati.py site code/calcoli/eventi.json'
    for coda in (' >> "$GITHUB_OUTPUT"', ' --segna > /dev/null'):
        nuovi['main', RADIO] = sostituisci(nuovi['main', RADIO], comando+coda,
                                          comando+' --cronache-classifica'+coda)
    nuovi['main', 'calcoli/post_curva.py'] = (R/'calcoli/post_curva.py').read_text()
    prima = 'def costruisci(t, tema="classico"):\n    t = maiuscole(t)'
    dopo = ('def costruisci(t, tema="classico"):\n'
            '    # Cronache 5.5: arricchisce una copia prima della normale impaginazione.\n'
            '    from giornale_classifica import integra\n'
            '    attese = json.loads(Path(__file__).with_name("aspettative.json").read_text(encoding="utf-8"))\n'
            '    t = integra(t, D, attese)\n    t = maiuscole(t)')
    nuovi['gh-pages', PDF] = sostituisci(nuovi['gh-pages', PDF], prima, dopo)
    prima = 'def giocata(g):\n    return any(m[-1] != "-" for m in g["m"])'
    dopo = '''def giocata(g):
    # Cronache 5.5: medesima giornata interamente chiusa di Curva e Radio.
    from zone_classifica import _giornate, RIS
    chiuse = _giornate(D)
    if any(g is x for x in D['cal']['lega']):
        return any(g is x for x in chiuse)
    sa = chiuse[-1].get('sa') if chiuse else None
    return bool(sa is not None and g.get('sa') is not None and g['sa'] <= sa
                and g.get('m') and all(RIS.fullmatch(str(m[-1])) for m in g['m']))'''
    nuovi['gh-pages', SETTIMANA] = sostituisci(nuovi['gh-pages', SETTIMANA], prima, dopo)
    for nome in MODULI:
        for ramo, cartella in (('main', 'calcoli'), ('gh-pages', 'scripts')):
            nuovi[ramo, cartella+'/'+nome] = (R/'calcoli'/nome).read_text()
    manifest = {'modalita':'preparazione_locale', 'applicato':False, 'push':False,
                'invii':False, 'audio':False, 'file':[]}
    uscita.mkdir(parents=True, exist_ok=True)
    for (ramo, percorso), testo in nuovi.items():
        dest = uscita/ramo/percorso
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(testo, encoding='utf-8')
        prima = sorgenti.get((ramo, percorso), '')
        manifest['file'].append({'ramo':ramo, 'percorso':percorso,
            'prima_sha256':hashlib.sha256(prima.encode()).hexdigest() if prima else None,
            'dopo_sha256':hashlib.sha256(testo.encode()).hexdigest()})
    for ramo in ('main', 'gh-pages'):
        patch = ''
        for (r,p),t in nuovi.items():
            if r != ramo:
                continue
            righe = list(difflib.unified_diff(sorgenti.get((r,p), '').splitlines(True), t.splitlines(True),
                         fromfile='a/'+p if (r,p) in sorgenti else '/dev/null', tofile='b/'+p))
            if righe:
                patch += 'diff --git a/'+p+' b/'+p+'\n'
                patch += ''.join(x if x.endswith('\n') else x+'\n\\ No newline at end of file\n' for x in righe)
        (uscita/(ramo+'.patch')).write_text(patch, encoding='utf-8')
    marker.write_text(json.dumps({'tipo':'cronache55-preparazione'},indent=2)+'\n')
    (uscita/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    return manifest


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('main', type=Path)
    p.add_argument('gh_pages', type=Path)
    p.add_argument('uscita', type=Path)
    a = p.parse_args()
    m = prepara(a.main, a.gh_pages, a.uscita)
    print('Preparati', len(m['file']), 'file locali. Nessuna applicazione, push, pubblicazione o generazione audio.')
