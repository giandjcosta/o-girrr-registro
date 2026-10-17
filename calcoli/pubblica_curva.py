#!/usr/bin/env python3
"""Pubblica nella Curva i post di calcoli/post_curva.json, una sola volta ciascuno.

Di default NON pubblica: stampa cosa farebbe. Per pubblicare davvero servono tre variabili d'ambiente (segreti, mai nel repo):
  CURVA_URL   indirizzo del database (come TOTO_URL)       CURVA_KEY   chiave publishable
  CURVA_TEAM  squadra amministratrice                      CURVA_CODE  codice della squadra amministratrice
e l'opzione --vai.   Uso:  python3 calcoli/pubblica_curva.py [--vai]
Usa la funzione curva_adm_scrivi del database. Tiene traccia di quanto già pubblicato in calcoli/pubblicati.json.
"""
import json, os, sys, urllib.request
from pathlib import Path

QUI = Path(__file__).resolve().parent
POST = QUI / "post_curva.json"
FATTI = QUI / "pubblicati.json"


def main():
    vai = "--vai" in sys.argv
    post = json.loads(POST.read_text(encoding="utf-8")) if POST.exists() else []
    fatti = set(json.loads(FATTI.read_text(encoding="utf-8"))) if FATTI.exists() else set()
    nuovi = [p for p in post if p["chiave"] not in fatti]
    print(len(nuovi), "post nuovi,", len(post) - len(nuovi), "già pubblicati")
    for p in nuovi:
        print(f"  [{p['h']}] {p['body'][:90].replace(chr(10), ' ')}…")
    if not vai or not nuovi:
        if nuovi: print("Prova a vuoto: aggiungi --vai per pubblicare davvero.")
        return
    url, key, team, code = (os.environ.get(k) for k in ("CURVA_URL", "CURVA_KEY", "CURVA_TEAM", "CURVA_CODE"))
    if not all((url, key, team, code)):
        sys.exit("Mancano CURVA_URL, CURVA_KEY, CURVA_TEAM o CURVA_CODE: non pubblico niente.")
    for p in nuovi:
        corpo = json.dumps(dict(p_team=team, p_code=code, p_h=p["h"], p_body=p["body"])).encode()
        rich = urllib.request.Request(f"{url}/rest/v1/rpc/curva_adm_scrivi", corpo, {"apikey": key, "Authorization": "Bearer " + key, "Content-Type": "application/json"})
        urllib.request.urlopen(rich, timeout=30).read()
        fatti.add(p["chiave"])
        FATTI.write_text(json.dumps(sorted(fatti), indent=1), encoding="utf-8")
    print("Pubblicati", len(nuovi), "post.")


if __name__ == "__main__":
    main()
