"""Soli testi; nessun client DB, TTS o archivio modificato."""
from datetime import datetime, timezone

def frase(stato, annunciati=(), ora=None, giornata_puntata=None):
    if not stato: return None
    n, stagione = stato.get('giornata'), stato.get('stagione')
    if not isinstance(n, int) or not 1 <= n <= 60 or not stagione: return None
    if giornata_puntata is not None and n > giornata_puntata: return None
    chiave = f'{stagione}:{n}'
    if stato.get('chiusa') and stato.get('risultato'):
        if chiave in annunciati: return None
        squadra = stato['risultato'][0].get('team')
        if not squadra or not isinstance(squadra, str): return None
        squadra = squadra.replace('The Blue brothers', 'The Blues Brothers')
        return f'{squadra} è l’MVP dei tifosi della {n}ª giornata.'
    if stato.get('chiusa'): return None
    try: fine = datetime.fromisoformat(stato['chiude'].replace('Z', '+00:00'))
    except (KeyError, TypeError, ValueError): return None
    if fine.tzinfo is None or (ora or datetime.now(timezone.utc)) >= fine: return None
    return f'Per l’MVP della {n}ª si vota ancora in Curva.'


def scegli(stato, annunciati=()):
    """Un verdetto definitivo non annunciato ha precedenza sul voto aperto."""
    archivio = [x for x in stato.get('archivio', []) if x.get('chiusa') and x.get('classifica')]
    for x in sorted(archivio, key=lambda x: x['giornata'], reverse=True):
        if f"{x['stagione']}:{x['giornata']}" not in annunciati:
            return {**x, 'risultato': x['classifica']}
    x = stato.get('votazione')
    if x and not x.get('chiusa'): return x
    return None
