#!/usr/bin/env python3
"""Pacchetto 6.1 sulla copia della 6.0.1 pubblicata. Non pubblica e non modifica il database."""
import importlib.util
from pathlib import Path
import sys
p=Path(__file__).resolve().parents[1]/'r602/applica.py'
s=importlib.util.spec_from_file_location('pacchetto_bilanci',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
if __name__=='__main__':m.main(sys.argv[1])
