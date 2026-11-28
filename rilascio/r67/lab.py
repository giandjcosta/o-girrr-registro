#!/usr/bin/env python3
"""Prossima versione (6.7, da confermare) · Preview del Lab: il sito pubblicato (6.6) più rilascio/r67/applica.py (Claude, 28 novembre 2026). Fatto come la 6.6.

Quello che si prova nel Lab è quello che va online. Sopra si aggiungono solo le comodità del Lab (come nella 6.5) e:
- rilascio/r66/lab66.js nello Spogliatoio, subito dopo lab62.js: gli scambi sono simulati nella memoria del browser
  (nel Lab il database vero non si tocca); c'è già una richiesta di esempio tra due
  altre squadre, per provare la conferma come testimone. ?scambi=vuoto riparte da zero;
- la versione in prova nella pagina Versioni (rilascio/r67/ANNUNCIO-BOZZA.json).

Uso: python3 rilascio/r67/lab.py COPIA_GH_PAGES   (copia di gh-pages con la 6.6, già passata da rilascio/r67/applica.py)
"""
import json, pathlib, re, shutil, subprocess, sys, tempfile

R = pathlib.Path(__file__).resolve().parents[2]
OUT = R / 'lab/integrata-62'
sys.path.insert(0, str(R / 'rilascio/r62'))
from preview import esporta  # noqa: E402

VIDEO = 'https://giandjcosta.github.io/o-fant-a-girrr/girrr/video/'   # 6.2.3: nella preview i video (20 MB) non sono copiati; si leggono dal sito vero, stesso indirizzo
SOLO_LAB = {
    'girrr/app.html': [("VB='video/'", "VB='" + VIDEO + "'")],
    'stadio/girrr/app.html': [("VB='../../girrr/video/'", "VB='" + VIDEO + "'")],
    # 6.2.3 (Gianluca: «come faccio a testare se sono link separati»): niente più dirottamento della scheda Spogliatoio
    # su squadre.html: lo Spogliatoio del Lab è integrata-62/index.html, come nel sito vero, e ci portano tutti i link.
    'girrr/index.html': [], 'stadio/girrr/index.html': [],   # restano qui per il link al Totogirrr con ?demo
    'girrr/totogirrr.html': [("var DEMO=/[?&]demo\\b/.test(location.search);", "var DEMO=true; /* Anteprima isolata: accesso ospite sempre con dati fittizi. */")],
    'stadio/girrr/totogirrr.html': [("var DEMO=/[?&]demo\\b/.test(location.search);", "var DEMO=true; /* Anteprima isolata: accesso ospite sempre con dati fittizi. */")],
}


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    sito = pathlib.Path(argv[0]).resolve()
    if not (sito / 'girrr/home-cruscotto.js').exists():
        raise SystemExit('La copia non è passata da rilascio/r67/applica.py')
    esporta(sito, OUT)
    # 6.2.3: lo Spogliatoio (index.html del sito) entra nel Lab come spogliatoio.html, con la stessa protezione delle altre
    # pagine (lab62.js per primo: niente database vero) e i caratteri locali, per provare sfondi e cambio di stile.
    s = (sito / 'index.html').read_text(encoding='utf-8')
    s = re.sub(r'<head([^>]*)>', lambda m: m.group(0) + '<script src="lab62.js"></script>', s, count=1, flags=re.I)
    s = re.sub(r'https://fonts.googleapis.com/css2[^"<>]*', 'font/originali.css', s)
    primo = re.search(r'<script\b[^>]*>', s, re.I)
    # 6.2.4: nel Lab lo Spogliatoio accetta anche il codice di prova di lab62.js («Squadra di prova», ?squadra=…), così si
    # vedono tutte le schede da allenatore con i dati di data.json. Solo nel Lab: nel sito vero il controllo resta l'impronta.
    PROVA = ("hsh(team+'|'+(LS.code||''))===D.lock[team]", "(LS.code==='codice-solo-del-test'||hsh(team+'|'+(LS.code||''))===D.lock[team])")
    if PROVA[1] not in s:
        if s.count(PROVA[0]) != 1:
            raise SystemExit('Spogliatoio del Lab: controllo del codice diverso da quello atteso')
        s = s.replace(PROVA[0], PROVA[1])
    if 'data-spogliatoio623' not in s or not primo or 'lab62.js' not in primo.group(0):
        raise SystemExit('Spogliatoio del Lab: protezione o modifiche 6.2.3 mancanti')
    # 6.6: file nuovi nella radice (icona dell'app) e la seconda entrata della skin, che l'esportazione non copia
    for rel in ('icona66.js', 'manifest-simbolo.webmanifest'):
        shutil.copyfile(sito / rel, OUT / rel)
    if (sito / 'temi/notte-tropicale/entrata-b').is_dir():
        shutil.copytree(sito / 'temi/notte-tropicale/entrata-b', OUT / 'temi/notte-tropicale/entrata-b', dirs_exist_ok=True)
    # 6.6: i loghi nuovi non sono ancora sul sito vero: dove le pagine li chiamano con l'indirizzo assoluto, nel Lab si prendono dal Lab
    NUOVI = ('scudo-lega.png', 'scudo-coppa.png', 'stagione-campionato.png', 'stagione-coppa.png')
    for f in list(OUT.rglob('*.js')) + list(OUT.rglob('*.html')):
        t = f.read_text(encoding='utf-8', errors='ignore')
        if 'o-fant-a-girrr/assets/loghi/' not in t:
            continue
        n = t
        for x in NUOVI:
            n = n.replace('https://giandjcosta.github.io/o-fant-a-girrr/assets/loghi/' + x, 'https://giandjcosta.github.io/o-girrr-registro/lab/integrata-62/assets/loghi/' + x)
        if n != t:
            f.write_text(n, encoding='utf-8')
    # 6.6: scambi simulati nel Lab, subito dopo la protezione lab62.js
    s = s.replace('<script src="lab62.js"></script>', '<script src="lab62.js"></script><script src="lab66.js"></script>', 1)
    shutil.copyfile(R / 'rilascio/r66/lab66.js', OUT / 'lab66.js')
    (OUT / 'index.html').write_text(s, encoding='utf-8')         # come nel sito: ../index.html porta allo Spogliatoio
    (OUT / 'spogliatoio.html').write_text(s, encoding='utf-8')   # indirizzo già usato nelle novità della 6.2.3
    for rel, coppie in SOLO_LAB.items():
        f = OUT / rel; t = f.read_text(encoding='utf-8')
        for a, b in coppie:
            if b in t:
                continue
            if a not in t:
                raise SystemExit('Pagina del Lab diversa da quella attesa: ' + rel)
            t = t.replace(a, b)
        t = t.replace('href="totogirrr.html"', 'href="totogirrr.html?demo"')
        f.write_text(t, encoding='utf-8')
    # Versione in prova: la pillola in basso a destra della Home e la pagina Versioni dicono 6.6
    d = json.loads((R / 'rilascio/r67/ANNUNCIO-BOZZA.json').read_text(encoding='utf-8'))
    with tempfile.TemporaryDirectory() as tmp:
        v = pathlib.Path(tmp) / 'versioni.json'
        shutil.copyfile(sito / 'versioni.json', v)
        a = [sys.executable, str(R / 'rilascio/versioni/aggiungi.py'), '--tipo', d['tipo'], '--v', d['v'], '--titolo', d['titolo'],
             '--messaggio', d['messaggio'], '--file', str(v)]
        for x in d['voci']:
            a += ['--voce', x]
        subprocess.run(a, check=True, capture_output=True)
        shutil.copyfile(v, OUT / 'versioni.json')
    print('Preview del Lab rigenerata in', OUT)


if __name__ == '__main__':
    main(sys.argv[1:])
