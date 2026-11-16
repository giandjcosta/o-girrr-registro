#!/usr/bin/env python3
"""6.2.3 · Preview del Lab: la 6.2.2 pubblicata più rilascio/r623/applica.py (Claude, 16 novembre 2026).

Come per la 6.2.2 (rilascio/r622/lab.py): quello che si prova nel Lab è quello che va online. Sopra si aggiungono solo le
comodità del Lab (Totogirrr dimostrativo, Spogliatoio da ospite) e la versione 6.2.3 in prova nella pagina Versioni.

Uso: python3 rilascio/r623/lab.py COPIA_GH_PAGES_CON_6_2_3   (copia di gh-pages con la 6.2.2, già passata da rilascio/r623/applica.py)
"""
import json, pathlib, shutil, subprocess, sys, tempfile

R = pathlib.Path(__file__).resolve().parents[2]
OUT = R / 'lab/integrata-62'
sys.path.insert(0, str(R / 'rilascio/r62'))
from preview import esporta  # noqa: E402

SOLO_LAB = {
    'girrr/index.html': [
        ('<a class="c" href="../index.html"><div class="ic"><img src="../assets/logo-lega.png" alt=""></div><h2>Spogliatoio</h2><p>La tua rosa, la giornata, gli scambi e il Mercato Scambi, svincolati e infortunati.</p>',
         '<a class="c" href="squadre.html"><div class="ic"><img src="../assets/logo-lega.png" alt=""></div><h2>Spogliatoio</h2><p>Modalità ospite di prova: consulta squadre, rose e dati pubblici. Scambi e mercato non sono ancora simulati.</p>'),
    ],
    'stadio/girrr/index.html': [
        ('<a class="c" href="../../index.html"><div class="ic"><img src="../../assets/logo-lega.png" alt=""></div><h2>Spogliatoio</h2><p>La tua rosa, la giornata, gli scambi e il Mercato Scambi, svincolati e infortunati.</p>',
         '<a class="c" href="squadre.html"><div class="ic"><img src="../../assets/logo-lega.png" alt=""></div><h2>Spogliatoio</h2><p>Modalità ospite di prova: consulta squadre, rose e dati pubblici. Scambi e mercato non sono ancora simulati.</p>'),
    ],
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
