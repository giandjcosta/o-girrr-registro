"""Prepara il Giornale nativo; i suoi font, CSS e quattro sezioni sono invariati."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def prepara(base):
    p=base/'scripts/pdf_giornale.py';s=p.read_text()
    marker='    # Cronache 5.5: arricchisce una copia prima della normale impaginazione.'
    if 'from mvp_giornale62 import integra as integra_mvp' not in s:
        if s.count(marker)!=1:raise ValueError('Generatore PDF diverso dalla base certificata')
        s=s.replace(marker,"    from mvp_giornale62 import integra as integra_mvp\n    dossier = ROOT / 'girrr/dati/mvp-editoriale.json'\n    if dossier.exists():\n        ultima = max((x['n'] for x in D['cal']['lega'] if giocata(x)), default=0)\n        t = integra_mvp(t, json.loads(dossier.read_text()), ultima)\n"+marker)
    p.write_text(s);(base/'scripts/mvp_giornale62.py').write_text((R/'rilascio/r62/editoriale/mvp_giornale62.py').read_text())
if __name__=='__main__':
    import sys
    prepara(Path(sys.argv[1]).resolve())
