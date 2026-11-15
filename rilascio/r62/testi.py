#!/usr/bin/env python3
"""6.2 · Due ritocchi chiesti da Gianluca (Claude, 15 novembre 2026).

- Tabellone › Dentro la partita (girrr/v55/ui.js, usato da Lega e Stadio): «= Stessa posizione» con la maiuscola
  dopo il simbolo, e «1 posizione» al singolare (prima «↑ 1 posizioni»).
- Albo › La Storia (girrr/novita.js e stadio/girrr/novita.js): i Padri Fondatori solo con il nome, tutti in fila,
  senza la squadra di oggi. Il testo della Storia non cambia.

Uso come campo_coppa.py:  python3 rilascio/r62/testi.py COPIA_DI_GH_PAGES   oppure   --lab
"""
import pathlib
import sys

QUI = pathlib.Path(__file__).resolve().parent
REG = QUI.parent.parent

POS_OLD = "(d>0?'↑ '+d+' posizioni':d<0?'↓ '+(-d)+' posizioni':'= stessa posizione')"
POS_NEW = "(d>0?'↑ '+d+(d===1?' posizione':' posizioni'):d<0?'↓ '+(-d)+(d===-1?' posizione':' posizioni'):'= Stessa posizione')"
PF_OLD = "STORIA.f.map(function(x){return '<div><b>'+esc(x[0])+'</b><small>'+esc(x[1])+'</small></div>'})"
PF_NEW = "STORIA.f.map(function(x){return '<div><b>'+esc(x[0])+'</b></div>'})"
CSS_OLD = ".sto-f{display:grid;grid-template-columns:repeat(auto-fill,minmax(105px,1fr));gap:8px;margin:10px 0 14px}"
CSS_NEW = ".sto-f{display:grid;grid-template-columns:repeat(auto-fit,minmax(92px,1fr));gap:8px;margin:10px 0 14px}.sto-f div{text-align:center}"
LAVORI = {
    'girrr/v55/ui.js': [(POS_OLD, POS_NEW)],
    'girrr/novita.js': [(PF_OLD, PF_NEW), (CSS_OLD, CSS_NEW)],
    'stadio/girrr/novita.js': [(PF_OLD, PF_NEW), (CSS_OLD, CSS_NEW)],
}


def applica(t, nome, coppie):
    for vecchio, nuovo in coppie:
        if nuovo in t:
            continue
        if t.count(vecchio) != 1:
            raise SystemExit('%s: atteso una volta «%s…», trovato %d volte' % (nome, vecchio[:50], t.count(vecchio)))
        t = t.replace(vecchio, nuovo)
    return t


def main(argv):
    if argv == ['--lab']:
        coppie = [(REG / 'ufficiale/src/sito' / p, QUI / 'pagine' / p, p) for p in LAVORI]
    elif len(argv) == 1:
        coppie = [(pathlib.Path(argv[0]) / p, pathlib.Path(argv[0]) / p, p) for p in LAVORI]
    else:
        raise SystemExit(__doc__)
    uscite = [(dst, applica(src.read_text(encoding='utf-8'), str(src), LAVORI[p])) for src, dst, p in coppie]
    for dst, t in uscite:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(t, encoding='utf-8')
        print('Scritto', dst)


if __name__ == '__main__':
    main(sys.argv[1:])
