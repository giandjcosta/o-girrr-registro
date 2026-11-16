#!/usr/bin/env python3
"""6.2.2 · Migliorie sopra la 6.2.1 pubblicata (Claude, 16 novembre 2026; Gianluca: «la 6.2.1 la miglioriamo con la 6.2.2»).

- Carriera sul telefono: un solo scorrimento per tocco, la fila arriva sulla voce scelta (prima tre scorrimenti insieme e un
  ridisegno a metà la fermavano prima o la facevano saltare).
- Tabellone della Fiducia: riparte a ogni ingresso nella Carriera (dalla Home o da un altro menu), non cambiando scheda.
- Schede del Derby al centro su PC; sul telefono la scheda toccata si vede tutta.
- Classifica dei Derby: Campionato e Champions Cup affiancati anche su iPhone SE; nella grafica Stadio tutto oro.
- Notifiche: «‹ O Girrr» sopra, logo grande a fianco del titolo, come nelle altre pagine.
- Niente alone del browser al tocco su «‹ O Girrr» e sugli altri link.

Le sostituzioni (testo della 6.2.1 → testo della 6.2.2) sono in sostituzioni.json: lo script si ferma se il sito non è più
quello della 6.2.1 pubblicata (gh-pages 19653ba). Rieseguibile.

Uso: python3 rilascio/r622/applica.py COPIA_GH_PAGES_6_2_1
"""
import json, pathlib, re, sys

QUI = pathlib.Path(__file__).resolve().parent
S = json.loads((QUI / 'sostituzioni.json').read_text(encoding='utf-8'))
APP = ['ORO', 'WEEK', 'CENTRA', 'FID_TAB', 'FID_INIT', 'FID_GATE']
LAVORI = {
    'girrr/app.html': APP, 'stadio/girrr/app.html': APP,
    'pillole.js': ['PILL'],
    'girrr/notifiche.html': ['NOT'], 'stadio/girrr/notifiche.html': ['NOT'],
}
DERBY = ('.dtab button:last-child{margin-right:auto}', '.dtab button:last-of-type{margin-right:auto}')  # l'ultimo figlio è la linea (.dline)
CODA = {'girrr/v60/tifosi.js': 'COMP', 'tv.js': 'TOCCO'}  # [marca, testo] aggiunti in fondo una volta sola


def sostituisci(t, rel, vecchio, nuovo):
    if nuovo in t:
        return t
    if t.count(vecchio) != 1:
        raise SystemExit('%s: atteso una volta «%s…», trovato %d volte: il sito non è la 6.2.1 pubblicata' % (rel, vecchio[:60], t.count(vecchio)))
    return t.replace(vecchio, nuovo)


def versioni(t):
    t = t.replace('pillole.js?v=621"', 'pillole.js?v=622"')
    t = t.replace('derby.js?v=621', 'derby.js?v=622')
    t = t.replace('v60/tifosi.js?v=621', 'v60/tifosi.js?v=622')
    t = re.sub(r'([\"/])tv\.js(?=[\"\'])', r'\1tv.js?v=622', t)
    return t


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    base = pathlib.Path(argv[0])
    v = json.loads((base / 'versioni.json').read_text(encoding='utf-8'))['versioni'][0]['v']
    if v not in ('6.2.1', '6.2.2'):
        raise SystemExit('La copia deve avere la 6.2.1 pubblicata (trovata ' + v + ')')
    for rel, chiavi in LAVORI.items():
        f = base / rel; t = f.read_text(encoding='utf-8')
        for k in chiavi:
            t = sostituisci(t, rel, *S[k])
        f.write_text(t, encoding='utf-8')
    for rel in ('girrr/derby.js', 'stadio/girrr/derby.js'):
        f = base / rel; f.write_text(sostituisci(f.read_text(encoding='utf-8'), rel, *DERBY), encoding='utf-8')
    for rel, k in CODA.items():
        f = base / rel; t = f.read_text(encoding='utf-8'); marca, testo = S[k]
        if marca not in t:
            f.write_text(t.rstrip('\n') + '\n' + testo + '\n', encoding='utf-8')
    cambiate = 0
    for html in sorted(base.rglob('*.html')):
        t = html.read_text(encoding='utf-8'); n = versioni(t)
        if n != t:
            html.write_text(n, encoding='utf-8'); cambiate += 1
    print('6.2.2 applicata · Pagine con i file nuovi:', cambiate)


if __name__ == '__main__':
    main(sys.argv[1:])
