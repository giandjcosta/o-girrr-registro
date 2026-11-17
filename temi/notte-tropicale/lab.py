#!/usr/bin/env python3
"""«Notte Tropicale» nel Lab (Claude, 17 novembre 2026): aggiunge il caricatore dei temi evento a tutte le pagine di
lab/integrata-62/ (la preview della versione online) in modalità «solo a mano», e copia accanto i file del tema.
Senza ?evento=… nell'indirizzo il Lab resta identico; con ?evento=notte-tropicale il tema si accende e resta acceso per la
sessione mentre si naviga (?evento=off per spegnerlo). Rieseguibile; va rilanciato dopo ogni rilascio/rXYZ/lab.py.

Uso: python3 temi/notte-tropicale/lab.py
"""
import pathlib, re, shutil

R = pathlib.Path(__file__).resolve().parents[2]
OUT = R / 'lab/integrata-62'
TEMI = OUT / 'temi'


def main():
    (TEMI / 'notte-tropicale').mkdir(parents=True, exist_ok=True)
    shutil.copyfile(R / 'temi/evento-loader.js', TEMI / 'evento-loader.js')
    for f in ('notte-tropicale.css', 'notte-tropicale.js', 'scena.svg', 'miami-tramonto.jpg', 'miami-palme.jpg', 'ocean-drive-notte.jpg'):
        shutil.copyfile(R / 'temi/notte-tropicale' / f, TEMI / 'notte-tropicale' / f)
    n = 0
    for p in sorted(OUT.rglob('*.html')):
        rel = p.relative_to(OUT)
        if rel.parts[0] == 'temi':
            continue
        t = p.read_text(encoding='utf-8')
        if 'evento-loader.js' in t:
            continue
        prefix = '../' * (len(rel.parts) - 1)
        tag = '<script src="%stemi/evento-loader.js" data-solo-manuale></script>' % prefix
        guard = '<script src="%slab62.js"></script>' % prefix
        if guard in t:
            t = t.replace(guard, guard + tag, 1)
        else:
            t, k = re.subn(r'<head([^>]*)>', lambda m: m.group(0) + tag, t, count=1, flags=re.I)
            if not k:
                continue
        p.write_text(t, encoding='utf-8'); n += 1
    print('Notte Tropicale nel Lab · Pagine con il caricatore:', n)


if __name__ == '__main__':
    main()
