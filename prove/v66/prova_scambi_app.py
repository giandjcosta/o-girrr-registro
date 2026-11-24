"""Claude, 24 novembre 2026: prove di calcoli/scambi_app.py (scambi nell'app, 6.6) senza database (--prova) e senza toccare il sito.
Uso: python3 prove/v66/prova_scambi_app.py CARTELLA_GH_PAGES   (legge solo data.json, lavora su una copia)"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
R = Path(__file__).resolve().parents[2]
SITO = Path(sys.argv[1])
ok = []
def check(l, x):
    if not x: raise SystemExit('FALLITA: ' + l)
    ok.append(l); print('ok ·', l)
with tempfile.TemporaryDirectory() as t:
    t = Path(t); (t / 'site').mkdir(); shutil.copyfile(SITO / 'data.json', t / 'site/data.json')
    D = json.loads((t / 'site/data.json').read_text())
    sq = {x['name']: x for x in D['teams']}
    def primo(team, r, salta=()):
        return next(str(p['id']) for p in sq[team]['pl'] if D['P'][str(p['id'])]['r'] == r and str(p['id']) not in salta)
    o_c, o_a = primo('Oranje VC', 'C'), primo('Oranje VC', 'A')
    r_c, r_a = primo('Real Madrink', 'C'), primo('Real Madrink', 'A')
    a_d, b_d = primo('Apo team', 'D'), primo('The Blue brothers', 'D')
    stato = {'scambi': [
        {'id': 5, 'da': 'Oranje VC', 'a': 'Real Madrink', 'dai': [o_c, o_a], 'ricevi': [r_c, r_a], 'nomi': {}, 'stato': 'confermato', 'conferma': 'testimone', 'confermato_da': 'Apo team', 'chiuso': '2026-11-24T18:00:00Z', 'applicato': None},
        {'id': 6, 'da': 'Apo team', 'a': 'The Blue brothers', 'dai': [a_d], 'ricevi': [b_d], 'nomi': {}, 'stato': 'attesa'},
        {'id': 7, 'da': 'Apo team', 'a': 'The Blue brothers', 'dai': [o_c], 'ricevi': [b_d], 'nomi': {}, 'stato': 'confermato', 'chiuso': '2026-11-24T18:00:00Z'},
        {'id': 8, 'da': 'Oranje VC', 'a': 'Real Madrink', 'dai': [primo('Oranje VC', 'P')], 'ricevi': [primo('Real Madrink', 'A', (r_a,))], 'nomi': {}, 'stato': 'confermato', 'chiuso': '2026-11-24T18:00:00Z'},
    ]}
    (t / 'stato.json').write_text(json.dumps(stato))
    run = lambda *a: subprocess.run([sys.executable, str(R / 'calcoli/scambi_app.py'), str(t / 'site'), '--prova', str(t / 'stato.json'), '--uscita', str(t / 'mercato-app.json'), *a], capture_output=True, text=True)
    p = run(); print(p.stdout.strip()); assert p.returncode == 0, p.stderr
    D2 = json.loads((t / 'site/data.json').read_text()); w = {str(x['id']): tm['name'] for tm in D2['teams'] for x in tm['pl']}
    check('Scambio confermato applicato alle rose (2 per 2)', w[o_c] == 'Real Madrink' and w[o_a] == 'Real Madrink' and w[r_c] == 'Oranje VC' and w[r_a] == 'Oranje VC')
    check('Rose sempre di 25 giocatori', all(len(tm['pl']) == len(sq[tm['name']]['pl']) for tm in D2['teams']))
    costo = {str(x['id']): x['c'] for x in D['teams'][0]['pl'] + [y for tm in D['teams'] for y in tm['pl']]}
    check('Il costo del giocatore resta il suo', all(x['c'] == costo[str(x['id'])] for tm in D2['teams'] for x in tm['pl']))
    check('Lo scambio in attesa non tocca le rose', w[a_d] == 'Apo team' and w[b_d] == 'The Blue brothers')
    M = json.loads((t / 'mercato-app.json').read_text())
    e = M['scambi'][0]
    check('Un solo scambio scritto (gli altri non validi o in attesa)', [x['id'] for x in M['scambi']] == [5])
    check('Post della Lega e commento di Ciro', e['post'][0][0] == 'lega_ofantagirrr' and e['post'][0][1].startswith('MERCATO · Ufficiale\nOranje VC e Real Madrink chiudono uno scambio') and e['post'][1][0] == 'ciro_trattativa' and '2 per 2' in e['post'][1][1])
    check('Post entro 280 caratteri', all(len(b) <= 280 for _, b in e['post']))
    SM = json.loads((t / 'site/girrr/dati/mercato.json').read_text())
    check('Riquadro Mercato del Giornale: scambio nel sito con la giornata', [x['id'] for x in SM['scambi']] == [5] and SM['scambi'][0]['dopo_giornata'] == e['giornata'])
    check('Notizia per la Radio della giornata dopo', e['radio']['giornata'] == e['giornata'] + 1 and e['radio']['testo'].startswith('scambio tra Oranje VC e Real Madrink'))
    check('Scambio 7 non valido (giocatore non più in rosa) e 8 non valido (ruoli diversi)', 'Scambio 7 non valido' in p.stdout and 'Scambio 8 non valido: I ruoli' in p.stdout)
    p2 = run(); D3 = (t / 'site/data.json').read_text()
    check('Seconda volta: niente di nuovo', 'ufficiale' not in p2.stdout and D3 == (t / 'site/data.json').read_text() and len(json.loads((t / 'mercato-app.json').read_text())['scambi']) == 1)
    # push fallito: il sito torna com'era, lo scambio è già in mercato-app.json ma non ancora segnato
    shutil.copyfile(SITO / 'data.json', t / 'site/data.json')
    p3 = run(); D4 = json.loads((t / 'site/data.json').read_text()); w = {str(x['id']): tm['name'] for tm in D4['teams'] for x in tm['pl']}
    check('Dopo un push fallito le rose si rimettono a posto, senza un secondo post', w[o_c] == 'Real Madrink' and 'rimesse a posto' in p3.stdout and len(json.loads((t / 'mercato-app.json').read_text())['scambi']) == 1)
    # conferma automatica: rose già scambiate da Leghe
    stato['scambi'][1]['dai'], stato['scambi'][1]['ricevi'] = [b_d], [a_d]   # Apo «dà» un giocatore che è già dei Blues: rose già scambiate
    (t / 'stato.json').write_text(json.dumps(stato))
    p4 = run()
    check('Conferma automatica quando le rose da Leghe sono già scambiate (senza --vai non scrive nel database)', 'conferma automatica' in p4.stdout)
    # post_curva legge mercato-app.json
    pc = (R / 'calcoli/post_curva.py').read_text()
    check('post_curva.py legge anche mercato-app.json', 'mercato-app.json' in pc)
print('\nTutte le %d prove superate.' % len(ok))
