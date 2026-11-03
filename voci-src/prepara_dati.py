#!/usr/bin/env python3
"""Prepara i dati della puntata radio dalla giornata chiusa, senza interventi a mano.

Uso:  python3 prepara_dati.py SITO EVENTI [--segna]
Prova testi: aggiungere --cronache-classifica --uscita DIRECTORY_SEPARATA.
Senza il primo flag il comportamento della Radio esistente resta invariato.
  SITO    cartella del ramo gh-pages del sito (data.json, girrr/dati/lab-dati.json, girrr/voci/archivio.json)
  EVENTI  calcoli/eventi.json del main del sito (conferenze, promesse, sfide e Derby dal database)
  --rifai rifà la puntata di una giornata già in archivio (opzione «rifai» del workflow)
  --segna dopo la puntata riuscita: segna i Derby annunciati (girrr/voci/annunciate.json del sito)
Scrive voci-src/dati.json, conferenze.json e (se serve) svuota curva.json. Stampa  giornata=N  per GitHub Actions
(giornata= vuoto se non c'è niente da fare: giornata non chiusa, o puntata già in archivio).
"""
import argparse, json, re, sys
from pathlib import Path
QUI = Path(__file__).resolve().parent

def carica(p, d=None):
    try: return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception: return d

def chiusa(d, cronache=False):
    if cronache:
        sys.path.insert(0, str(QUI.parent / "calcoli"))
        from zone_classifica import _giornate
        ch = _giornate(d)
        return ch[-1] if ch else None
    lega = d["cal"]["lega"]
    ch = [r for r in lega if r["m"] and all(m[4] and m[4] != "-" for m in r["m"])]
    return max(ch, key=lambda r: r["n"]) if ch else None

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('sito', type=Path)
    p.add_argument('eventi', type=Path)
    p.add_argument('--segna', action='store_true')
    p.add_argument('--rifai', action='store_true', help="rifà la puntata anche se la giornata è già in archivio (la nuova sostituisce la vecchia)")
    p.add_argument('--cronache-classifica', action='store_true', help='Attiva esplicitamente le nuove cronache')
    p.add_argument('--uscita', type=Path, help='Directory separata per la preparazione di prova')
    args = p.parse_args(argv)
    SITO, EV = args.sito, args.eventi
    ANN = SITO / "girrr/voci/annunciate.json"
    dest = args.uscita or QUI
    if args.uscita and args.segna:
        p.error('La preparazione in una directory separata non segna dati nel sito')
    d = carica(SITO / "data.json")
    r = chiusa(d, args.cronache_classifica)
    if not r: print("giornata="); return
    n, sa = r["n"], r.get("sa")
    if args.segna:
        ev = carica(EV, [])
        k = {f"derby:{e['k']}" for e in ev if e.get("tipo") == "derby"}
        ANN.write_text(json.dumps(sorted(k | set(carica(ANN, []))), indent=1), encoding="utf-8")
        print(f"giornata={n}"); return
    arc = carica(SITO / "girrr/voci/archivio.json", [])
    if not args.rifai and any(re.search(rf"Giornata {n}\b", (e.get("tag") or "") + " " + (e.get("titolo") or "")) for e in arc):
        print("giornata="); return          # già fatta
    ev = carica(EV, [])
    dati = carica(SITO / "girrr/dati/lab-dati.json")
    if args.cronache_classifica and (not dati or not dati.get('aw') or dati['aw'][-1].get('n') != n):
        print('Dati dei calcoli non allineati alla giornata chiusa.')
        print('giornata='); return
    cp_ = [c for c in d["cal"].get("cup", []) if c.get("sa") == sa and c.get("m")]
    if cp_ and not all(m[5] and m[5] != "-" for m in cp_[-1]["m"]):
        print("giornata="); return          # la Coppa di questa giornata non è ancora chiusa: aspetto
    # Champions Cup: se ne parla solo se si è giocato nella stessa giornata di Serie A del campionato
    # i risultati della giornata, partita per partita: [casa, punteggio casa, punteggio trasferta, trasferta, "gol-gol"]
    dati["partite"] = r["m"]
    dati["cup"] = [c for c in d["cal"].get("cup", []) if c.get("sa") == sa and c.get("m") and all(m[5] and m[5] != "-" for m in c["m"])][-1:]
    if args.cronache_classifica:
        sys.path.insert(0, str(QUI.parent / 'calcoli'))
        from zone_classifica import evento
        att = carica(QUI.parent / 'calcoli/aspettative.json')
        if not att or not att.get('squadre'):
            raise RuntimeError('Aspettative pre-stagione non disponibili')
        dati['cronache_classifica_attive'] = True
        dati['zona_classifica'] = evento(d, att)
        dati['cronaca_classifica'] = dati['zona_classifica']
    else:
        # Il workflow pubblico non passa il flag: nessuna attivazione implicita
        # nemmeno se un vecchio snapshot contenesse i campi della prova.
        for key in ('cronache_classifica_attive', 'zona_classifica', 'cronaca_classifica'):
            dati.pop(key, None)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "dati.json").write_text(json.dumps(dati, ensure_ascii=False), encoding="utf-8")
    conf = [e for e in ev if e.get("tipo") == "conferenza" and e.get("giornata") == n]
    squadre = {}
    for e in conf:
        s = squadre.setdefault(e["team"], {"toni": []})
        s["toni"].append(e.get("tono", 1))
    for e in ev:
        if e.get("tipo") == "promessa" and e.get("giornata") == n and e.get("team") in squadre and e.get("promessa"):
            squadre[e["team"]].update({"promessa": e["promessa"], "pesa": e.get("pesa", 1), "esito": e.get("esito", "")})
    annunciate = set(carica(ANN, []))
    derby = [{"da": e["da"], "a": e["a"], "stato": "accettata", "nome": e["nome"], "annunciata": f"derby:{e['k']}" in annunciate}
             for e in ev if e.get("tipo") == "derby"]
    out = {"_come_si_usa": "Generato da prepara_dati.py (dati veri dal database del sito).", "demo": False, "giornata": n,
           "partite": [[e["team"], e.get("avversario", "")] for e in conf if e.get("avversario")],
           "squadre": squadre, "sfide_derby": derby}
    (dest / "conferenze.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    cv = carica(QUI / "curva.json", {})
    if cv.get("giornata") != n:        # il post della Curva vale solo per la giornata per cui è stato messo
        (dest / "curva.json").write_text(json.dumps({"_come_si_usa": "Un post vero dalla Curva per la giornata indicata in \"giornata\". Se manca o è di un'altra giornata la radio non ne parla.", "giornata": n, "post": "", "caso": ""}, ensure_ascii=False), encoding="utf-8")
    elif args.uscita:
        (dest / "curva.json").write_text(json.dumps(cv, ensure_ascii=False), encoding='utf-8')
    print(f"giornata={n}")
if __name__ == '__main__':
    main()
