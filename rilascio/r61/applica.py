#!/usr/bin/env python3
"""Pacchetto 6.1 sulla copia della 6.0.1 pubblicata. Non pubblica e non modifica il database."""
import importlib.util
from pathlib import Path
import re
import sys
p=Path(__file__).resolve().parents[1]/'r602/applica.py'
s=importlib.util.spec_from_file_location('pacchetto_bilanci',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)


def aggiorna_riferimenti(copia):
    # Home, Tabellone e Spogliatoio devono scaricare i moduli nuovi anche dopo la 6.0.1.
    pattern=r'''(<script\b[^>]*\bsrc=["'])([^"']*/)?((?:condividi|cerca)\.js)(?:\?[^"']*)?(["'])'''
    for pagina in Path(copia).rglob('*.html'):
        prima=pagina.read_text(encoding='utf-8')
        dopo=re.sub(pattern,lambda a:a[1]+(a[2] or '')+a[3]+'?v=61-periodi1'+a[4],prima)
        if dopo!=prima:
            pagina.write_text(dopo,encoding='utf-8')
            print('Aggiornato riferimento:',pagina.relative_to(copia))


if __name__=='__main__':
    m.main(sys.argv[1])
    aggiorna_riferimenti(sys.argv[1])
