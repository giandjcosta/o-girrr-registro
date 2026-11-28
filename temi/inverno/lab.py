#!/usr/bin/env python3
"""Skin «Inverno» nel Lab (Claude, 28 novembre 2026): copia caricatore, foglio di stile, script e scene in lab/integrata-62/temi/
e mette il caricatore «solo a mano» nelle pagine (lo stesso passo di temi/notte-tropicale/lab.py). Senza ?evento=… il Lab resta
identico; con ?evento=inverno la skin si accende (e resta accesa per la sessione); ?evento-sfondo=natale|capodanno|wonderland|premium
cambia atmosfera. Rieseguibile; va rilanciato dopo ogni rilascio/rXYZ/lab.py.

Uso: python3 temi/inverno/lab.py
"""
import importlib.util, pathlib, shutil

R = pathlib.Path(__file__).resolve().parents[2]
DEST = R / 'lab/integrata-62/temi/inverno'
FILE = ('inverno.css', 'inverno.js', 'inverno-premium.svg', 'inverno-natale.svg', 'inverno-capodanno.svg', 'inverno-wonderland.svg')


def main():
    spec = importlib.util.spec_from_file_location('nt_lab', R / 'temi/notte-tropicale/lab.py')
    nt = importlib.util.module_from_spec(spec); spec.loader.exec_module(nt)
    nt.main()   # caricatore aggiornato e inserito in tutte le pagine
    DEST.mkdir(parents=True, exist_ok=True)
    for f in FILE:
        shutil.copyfile(R / 'temi/inverno' / f, DEST / f)
    (DEST / 'foto').mkdir(exist_ok=True)
    for f in (R / 'temi/inverno/foto').iterdir():
        shutil.copyfile(f, DEST / 'foto' / f.name)
    print('Inverno nel Lab · File copiati:', len(FILE))


if __name__ == '__main__':
    main()
