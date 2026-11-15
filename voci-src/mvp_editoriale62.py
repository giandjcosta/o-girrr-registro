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


# ---------- Claude, 15 novembre 2026 (Gianluca): due battute brevi in stile radiofonico (poco audio, poca spesa) ----------
# 1) commento sulla squadra MVP della scorsa giornata, con Campionato e Champions Cup insieme (solo risultati veri);
# 2) «Sono aperte le votazioni…» con le tre candidate della giornata appena terminata. Nessun audio in più: sono
#    righe della normale puntata, prima della chiusura integrale. Mai Fantapunti.

def _nome(t):
    return (t or '').replace('The Blue brothers', 'The Blues Brothers')


def partite(D, team, giornata):
    """Partite della squadra nella giornata: Campionato e, se c'è, Champions Cup della stessa giornata di Serie A."""
    out, sa = [], None
    for g in (D or {}).get('cal', {}).get('lega', []):
        if g.get('n') == giornata:
            sa = g.get('sa')
            for m in g.get('m', []):
                if team in (m[0], m[3]) and m[4] not in ('-', '', None) and '-' in str(m[4]):
                    a, b = (int(x) for x in m[4].split('-'))
                    casa = m[0] == team
                    out.append({'comp': 'Campionato', 'opp': m[3] if casa else m[0], 'gf': a if casa else b, 'gs': b if casa else a, 'casa': casa})
    for g in (D or {}).get('cal', {}).get('cup', []):
        if sa is not None and g.get('sa') == sa:
            for m in g.get('m', []):
                if team in (m[1], m[4]) and m[5] not in ('-', '', None) and '-' in str(m[5]):
                    a, b = (int(x) for x in m[5].split('-'))
                    casa = m[1] == team
                    out.append({'comp': 'Champions Cup', 'opp': m[4] if casa else m[1], 'gf': a if casa else b, 'gs': b if casa else a, 'casa': casa})
    return out


def storie(D, *voci):
    """{'squadra|giornata': [partite]} per le squadre citate, da mettere nei dati della puntata."""
    return {f'{t}|{g}': partite(D, t, g) for t, g in voci if t and g}


def _racconta(p):
    o = _nome(p['opp'])
    if p['gf'] > p['gs']:
        return f"il {p['gf']} a {p['gs']} " + ('su ' if p['casa'] else 'sul campo di ') + o
    if p['gf'] == p['gs']:
        return f"il {p['gf']} pari con {o}"
    return f"il {p['gf']} a {p['gs']} contro {o}"


def battute(verdetto, aperta, racconti=None, annunciati=(), giornata_puntata=None, ora=None):
    """Le righe (personaggio, testo, stile) della puntata: al massimo due, prima della chiusura."""
    out, racconti = [], racconti or {}
    v = verdetto if verdetto and verdetto.get('chiusa') and verdetto.get('risultato') else None
    if v and (giornata_puntata is None or v.get('giornata', 99) <= giornata_puntata) and f"{v.get('stagione')}:{v.get('giornata')}" not in annunciati:
        team, g = v['risultato'][0].get('team'), v.get('giornata')
        if team and isinstance(g, int):
            pp = racconti.get(f'{team}|{g}') or []
            vinte = [p for p in pp if p['gf'] > p['gs']]
            T = _nome(team)
            T = T[:1].upper() + T[1:]
            if len(pp) == 2 and len(vinte) == 2 and pp[0]['opp'] == pp[1]['opp']:   # stessa avversaria due volte
                testo = f"Strepitosa {T}, squadra MVP della {g}ª: batte due volte {_nome(pp[0]['opp'])}, in Campionato e in Champions Cup!"
            elif len(pp) == 2 and len(vinte) == 2:
                testo = f"Strepitosa {T}, squadra MVP della {g}ª: due vittorie e {pp[0]['gf'] + pp[1]['gf']} gol tra Campionato e Champions Cup!"
            elif vinte:
                testo = f"Applausi per {T}, squadra MVP della {g}ª: decisivo {_racconta(vinte[0])}!"
            else:
                testo = f"{T} è la squadra MVP della {g}ª giornata!"
            out.append(('G', testo, None))
    a = aperta if aperta and not aperta.get('chiusa') and aperta.get('classifica') else None
    if a and (giornata_puntata is None or a.get('giornata', 99) <= giornata_puntata):
        try:
            fine = datetime.fromisoformat(a['chiude'].replace('Z', '+00:00'))
        except (KeyError, TypeError, ValueError):
            fine = None
        if fine and fine.tzinfo and (ora or datetime.now(timezone.utc)) < fine:
            nomi = [_nome(c.get('team')) for c in a['classifica'][:3] if c.get('team')]
            if len(nomi) >= 2:
                elenco = ', '.join(nomi[:-1]) + ' e ' + nomi[-1]
                out.append(('B', f"Votazioni aperte per l’MVP della {a['giornata']}ª: in corsa {elenco}. Si vota in Curva e in Girrr Sport!", 'urlo'))
    return out
