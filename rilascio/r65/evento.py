#!/usr/bin/env python3
"""6.5 · Skin «Notte Tropicale» sul sito vero (Claude, 18 novembre 2026).

Copia nel sito temi/evento-loader.js e la cartella temi/notte-tropicale/ (CSS, script, foto locali, crediti) e aggiunge in
<head> di ogni pagina il caricatore, una volta sola. Il caricatore decide da solo, nel browser e in ora italiana: acceso dal
18 novembre 00:00 al 24 novembre 00:00 (fine della giornata 8), poi spento senza altri rilasci. Durante l'evento grafica unica (le pagine Stadio portano
alla stessa pagina della Lega) e la Curva resta com'è. Per provarlo prima o dopo: ?evento=notte-tropicale, ?evento=off.

Uso: python3 rilascio/r65/evento.py COPIA_GH_PAGES   (dopo rilascio/r65/applica.py)
Rieseguibile: la seconda volta «Pagine cambiate: 0».
"""
import pathlib, re, shutil, sys

R = pathlib.Path(__file__).resolve().parents[2]
FILE = ('notte-tropicale.css', 'notte-tropicale.js', 'entrata.css', 'entrata.js', 'gta6-lucia-jason-cover.webp', 'scena.svg', 'miami-tramonto.jpg', 'miami-palme.jpg', 'ocean-drive-notte.jpg', 'tutto-1.jpg', 'tutto-2.jpg', 'tutto-3.jpg', 'tutto-4.jpg', 'tutto-5.jpg', 'tutto-6.jpg', 'CREDITI.md')


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    base = pathlib.Path(argv[0])
    if not (base / 'pillole.js').is_file() or 'NOSCIVOLO' not in (base / 'pillole.js').read_text(encoding='utf-8'):
        raise SystemExit('Prima rilascio/r65/applica.py sulla copia del sito')
    (base / 'temi/notte-tropicale').mkdir(parents=True, exist_ok=True)
    shutil.copyfile(R / 'temi/evento-loader.js', base / 'temi/evento-loader.js')
    for f in FILE:
        shutil.copyfile(R / 'temi/notte-tropicale' / f, base / 'temi/notte-tropicale' / f)
    n = 0
    for p in sorted(base.rglob('*.html')):
        rel = p.relative_to(base)
        s = str(rel)
        if rel.parts[0] in ('temi', 'prova', 'riepiloghi') or s.startswith('v5') or '/v5' in s:
            continue
        t = p.read_text(encoding='utf-8')
        if 'evento-loader.js' in t:
            continue
        tag = '<script src="%stemi/evento-loader.js?v=65"></script>' % ('../' * (len(rel.parts) - 1))
        t, k = re.subn(r'<head([^>]*)>', lambda m: m.group(0) + tag, t, count=1, flags=re.I)
        if k:
            p.write_text(t, encoding='utf-8'); n += 1
    print('Skin Notte Tropicale · Pagine cambiate:', n)


if __name__ == '__main__':
    main(sys.argv[1:])
