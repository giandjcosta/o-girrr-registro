"""Rubrica MVP autonoma: Curva intatta, verdetti e candidature distinti."""
import copy
from datetime import datetime,timezone

def integra(testi,dossier,giornata,ora=None):
    t=copy.deepcopy(testi);ora=ora or datetime.now(timezone.utc)
    w=dossier.get('votazione') or {}
    rubrica={'titolo':'MVP dei tifosi','verdetto':None,'giornata':None,'candidati':[]}
    if not w.get('chiusa') and w.get('giornata')==giornata and w.get('classifica'):
        rubrica['giornata']=giornata
        for c in w['classifica'][:3]:
            # Soltanto risultati registrati: nessuna giocata o prestazione individuale dedotta.
            if not all(k in c for k in ('team','gf','gs','op','away')):continue
            sede='in trasferta' if c['away'] else 'in casa'
            motivo=next((v['motivo'] for v in w.get('redazione',[]) if v.get('scelta')==c['team']),None)
            testo=motivo or (f"Colpo sul campo di {c['op']}: il {c['gf']}–{c['gs']} porta {c['team']} fra le tre candidate." if c['away'] else f"Tre gol e una vittoria combattuta contro {c['op']}: il {c['gf']}–{c['gs']} accende la corsa al premio." if c['gf']==3 else f"Il {c['gf']}–{c['gs']} {sede} contro {c['op']} vale la candidatura.")
            rubrica['candidati'].append({'squadra':c['team'],'testo':testo})
    if rubrica['candidati']:t['mvp_editoriale']=rubrica
    return t
