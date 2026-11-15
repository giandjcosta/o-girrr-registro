"""Solo contenuti nel riquadro Curva originale; nessuna modifica a CSS o impaginazione."""
import copy
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
MESI=('gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre')
def integra(testi,dossier,giornata,ora=None):
    t=copy.deepcopy(testi);ora=ora or datetime.now(timezone.utc)
    validi=[x for x in dossier.get('archivio',[]) if x.get('chiusa') and x.get('classifica') and x.get('giornata',999)<=giornata]
    gia=set(dossier.get('giornale_annunciati',[]));validi=[x for x in validi if f"{x.get('stagione')}:{x['giornata']}" not in gia]
    w=max(validi,key=lambda x:x['giornata']) if validi else dossier.get('votazione')
    if not w or not isinstance(w.get('giornata'),int) or w['giornata']>giornata:return t
    n=w['giornata'];vincitore=None
    if w.get('chiusa') and w.get('classifica'):
        vincitore=w['classifica'][0]['team'];msg=f'MVP dei tifosi della {n}ª: {vincitore}.'
    else:
        try:fine=datetime.fromisoformat(w['chiude'].replace('Z','+00:00'))
        except (KeyError,TypeError,ValueError):return t
        if fine.tzinfo is None or fine<=ora:return t
        fine=fine.astimezone(ZoneInfo('Europe/Rome'));msg=f'MVP della {n}ª: si vota in Curva fino al {fine.day} {MESI[fine.month-1]} alle {fine:%H:%M}.'
    quote=dossier.get('commento') or {}
    autentico=quote.get('post_id') is not None and quote.get('giornata')==n and quote.get('testo') and quote.get('fonte') and quote.get('pertinente') is True
    if vincitore:autentico=autentico and quote.get('squadra_riferita')==vincitore
    t['coro']={'squadra':quote['squadra'] if autentico else 'Girrr Sport','testo':msg+('\n'+quote['testo'] if autentico else '')}
    return t
