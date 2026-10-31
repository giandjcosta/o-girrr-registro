#!/usr/bin/env python3
"""Registra nel database i premi sponsor raggiunti (funzione carriera_registra_server).

Legge il JSON scritto da premi_giornata.js e, per ogni premio, chiama la funzione del database con la chiave
service_role. Il database accetta solo crediti 0/50/75/100/125, solo la stagione 2026/27 e non registra due volte
lo stesso premio: rifare la stessa chiamata risponde «duplicate» e non cambia niente.

Uso:
  python3 calcoli/premi/registra_premi.py premi.json DATA_JSON            # prova: stampa cosa registrerebbe, non scrive
  python3 calcoli/premi/registra_premi.py premi.json DATA_JSON --vai      # registra davvero (serve SUPABASE_SERVICE_ROLE_KEY)

La chiave non viene mai stampata. L'URL del progetto è pubblico (è già nelle pagine del sito).
"""
import json
import os
import sys
import urllib.error
import urllib.request

PROGETTO = "https://qmjqfgmvimsuxvghetgi.supabase.co"
STAGIONE = "2026/27"
CREDITI_VALIDI = (0, 50, 75, 100, 125)


def ultima_giornata_chiusa(data):
    """Ultima giornata con tutti e cinque i risultati numerici, senza buchi (stessa regola del Lab)."""
    fatta = 0
    for g in sorted(data["cal"]["lega"], key=lambda g: g["n"]):
        ok = (g["n"] == fatta + 1 and g.get("m") and len(g["m"]) == 5 and
              all(m[4] and m[4] != "-" and len(m[4].split("-")) == 2 and
                  all(x != "" and x.lstrip("-").isdigit() for x in m[4].split("-")) for m in g["m"]))
        if not ok:
            break
        fatta += 1
    return fatta


def chiave_obiettivo(obiettivo, stagione=STAGIONE):
    """«sponsor» diventa sponsor_2026_27, come nel database; «sponsor_coppa» diventa sponsor_coppa_2026_27."""
    return f"{obiettivo}_{stagione.replace('/', '_')}"


def costruisci(premi, data, oggi):
    giornata = ultima_giornata_chiusa(data)
    righe = []
    for p in premi:
        if p["credits"] not in CREDITI_VALIDI:
            raise SystemExit(f"Crediti non validi per {p['team']}: {p['credits']}")
        righe.append({
            "p_season": STAGIONE,
            "p_manager": p["manager"],
            "p_team": p["team"],
            "p_objective": chiave_obiettivo(p["objective"]),
            "p_sponsor": p["sponsor"],
            "p_kind": "sponsor",
            "p_rep": p["reputation"],
            "p_credits": p["credits"],
            "p_proof": {"source": "official_github_data_json", "as_of": oggi, "verified_through": giornata},
        })
    return righe


def registra(riga, chiave):
    corpo = json.dumps(riga).encode("utf-8")
    richiesta = urllib.request.Request(
        f"{PROGETTO}/rest/v1/rpc/carriera_registra_server", data=corpo, method="POST",
        headers={"apikey": chiave, "Authorization": f"Bearer {chiave}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(richiesta, timeout=30) as r:
            return r.read().decode("utf-8").strip('"')
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Il database ha risposto {e.code} per {riga['p_team']}: {e.read().decode('utf-8')[:300]}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        raise SystemExit(__doc__)
    premi = json.load(open(args[0], encoding="utf-8"))["premi"]
    data = json.load(open(args[1], encoding="utf-8"))
    from datetime import date
    righe = costruisci(premi, data, date.today().isoformat())

    print(f"Premi da registrare: {len(righe)} (giornata verificata: {righe[0]['p_proof']['verified_through'] if righe else '-'})")
    for r in righe:
        print(f"  {r['p_team']} · {r['p_manager']} · {r['p_objective']} · {r['p_credits']} crediti")

    if "--vai" not in sys.argv:
        print("\nPROVA: non ho scritto niente. Con --vai registro questi premi nel database.")
        return

    chiave = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not chiave:
        raise SystemExit("Manca il segreto SUPABASE_SERVICE_ROLE_KEY: niente registrazione.")
    print("\nRegistrazione:")
    for r in righe:
        esito = registra(r, chiave)
        print(f"  {r['p_team']}: {esito}")


if __name__ == "__main__":
    main()
