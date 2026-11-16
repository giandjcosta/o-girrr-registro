#!/usr/bin/env python3
"""6.2.3 · Preview del Lab: la 6.2.2 pubblicata più rilascio/r623/applica.py (Claude, 16 novembre 2026).

Come per la 6.2.2 (rilascio/r622/lab.py): quello che si prova nel Lab è quello che va online. Sopra si aggiungono solo le
comodità del Lab (Totogirrr dimostrativo, Spogliatoio come nel sito in integrata-62/index.html) e la versione 6.2.3
in prova nella pagina Versioni.

Uso: python3 rilascio/r623/lab.py COPIA_GH_PAGES_CON_6_2_3   (copia di gh-pages con la 6.2.2, già passata da rilascio/r623/applica.py)
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
    if 'data-toto623' not in (sito / 'girrr/totogirrr.html').read_text(encoding='utf-8'):
        raise SystemExit('La copia non è passata da rilascio/r623/applica.py')
    esporta(sito, OUT)
    # 6.2.3: lo Spogliatoio (index.html del sito) entra nel Lab come spogliatoio.html, con la stessa protezione delle altre
    # pagine (lab62.js per primo: niente database vero) e i caratteri locali, per provare sfondi e cambio di stile.
    s = (sito / 'index.html').read_text(encoding='utf-8')
    s = re.sub(r'<head([^>]*)>', lambda m: m.group(0) + '<script src="lab62.js"></script>', s, count=1, flags=re.I)
    s = re.sub(r'https://fonts.googleapis.com/css2[^"<>]*', 'font/originali.css', s)
    primo = re.search(r'<script\b[^>]*>', s, re.I)
    if 'data-spogliatoio623' not in s or not primo or 'lab62.js' not in primo.group(0):
        raise SystemExit('Spogliatoio del Lab: protezione o modifiche 6.2.3 mancanti')
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
    # Versione in prova: la pillola in basso a destra della Home e la pagina Versioni dicono 6.2.3
    d = json.loads((R / 'rilascio/r623/ANNUNCIO-BOZZA.json').read_text(encoding='utf-8'))
    with tempfile.TemporaryDirectory() as tmp:
        v = pathlib.Path(tmp) / 'versioni.json'
        shutil.copyfile(sito / 'versioni.json', v)
        a = [sys.executable, str(R / 'rilascio/versioni/aggiungi.py'), '--tipo', d['tipo'], '--titolo', d['titolo'],
             '--messaggio', d['messaggio'], '--file', str(v)]
        for x in d['voci']:
            a += ['--voce', x]
        subprocess.run(a, check=True, capture_output=True)
        shutil.copyfile(v, OUT / 'versioni.json')
    print('Preview del Lab rigenerata in', OUT)


if __name__ == '__main__':
    main(sys.argv[1:])
