"""Segmento editoriale: legge esclusivamente la scheda del calcolo condiviso.

Nessuna rete, nessun servizio vocale, nessuna classifica ricalcolata.
"""


def nome(t):
    return 'The Blues Brothers' if t == 'The Blue brothers' else t


def segmento(dati, giornata):
    if giornata not in (17, 19) or not dati:
        return []
    if dati.get('ultima_pubblicata') != giornata:
        raise ValueError('Giro di boa non allineato alla puntata')
    chiave = 'andata' if giornata == 17 else 'ritorno'
    p = dati.get('periodi', {}).get(chiave)
    if not p:
        raise ValueError('Periodo del Giro di boa non disponibile')
    c = p['campionato']
    out = [('B', 'Giro di boa! Il bilancio del girone d’andata.' if giornata == 17 else
            'Giro di boa, il ritorno. Facciamo il punto sulle prime due giornate del girone di ritorno.', 'urlo')]
    if c.get('campione_inverno'):
        out.append(('G', f"Il campione d’inverno è {nome(c['campione_inverno'])}.", None))
    out.append(('B', f"Nel periodo si sono giocate {c['partite']} partite, con {c['gol']} gol. "
                f"Miglior attacco: {', '.join(map(nome,c['miglior_attacco']))}. "
                f"Miglior difesa: {', '.join(map(nome,c['miglior_difesa']))}.", None))
    for i, r in enumerate(p['classifica']):
        s = p['squadre'][r['squadra']];b = s['bilancio'];f = s['dirigenza'];cp = s['coppa'];de = s['derby'];pr = s['promesse'];mv = s['mvp']
        frasi = [f"{nome(s['squadra'])}: posizione {s['posizione']}, {s['punti_classifica']} punti in classifica, a {s['distacco_vetta']} dalla vetta.",
                 f"Nel periodo, {b['vittorie']} vittorie, {b['pareggi']} pareggi e {b['sconfitte']} sconfitte; {b['gol_fatti']} gol fatti e {b['gol_subiti']} subiti.",
                 f"In casa {s['casa']['punti']} punti, in trasferta {s['trasferta']['punti']}."]
        frasi.append(f"È ultima, a {s['distacco_penultimo']} punti dal penultimo posto." if s['in_zona_retrocessione'] else f"Il margine sull’ultimo posto è di {s['margine_ultimo_posto']} punti.")
        if f['attesa'] is not None:
            frasi.append(f"Il presidente si aspettava il posto {f['attesa']}: {f['giudizio'].lower()}.")
        if f['fiducia'] is not None:frasi.append(f"Fiducia: {f['fiducia']} su cento.")
        if s['serie']['imbattibilita']['partite']:
            z=s['serie']['imbattibilita'];frasi.append(f"La serie più lunga senza sconfitte è di {z['partite']} partite, dalla giornata {z['dalla']} alla {z['alla']}.")
        if de['disponibile']:frasi.append(f"Nei Derby del registro disponibile: {de['vittorie']} vittorie, {de['pareggi']} pareggi, {de['sconfitte']} sconfitte.")
        else:frasi.append('Derby: Dato non conservato.')
        frasi.append(f"Champions Cup: {cp['qualificazione']}.")
        if pr['disponibile']:frasi.append(f"Promesse: {pr['mantenute']} mantenute, {pr['pari']} pari, {pr['tradite']} tradite.")
        else:frasi.append('Promesse: Dato non conservato.')
        frasi.append(f"MVP dei tifosi ricevuti: {mv['ricevuti']}." if mv['disponibile'] else 'MVP dei tifosi: Dato non conservato.')
        # Unica eccezione tecnica di questo segmento: vittoria strettissima vera.
        vittorie = [x for x in s['sul_filo'] if x['esito']=='V']
        if vittorie:
            x=vittorie[0];scarto=x['scarto_fantapunti']
            frasi.append(f"Alla giornata {x['giornata']} ha battuto {nome(x['avversario'])} {x['gol_fatti']} a {x['gol_subiti']}, con appena {str(scarto).replace('.',',')} Fantapunti di differenza.")
        out.append(('G' if i%2==0 else 'B', ' '.join(frasi), None))
    return out
