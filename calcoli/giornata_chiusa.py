#!/usr/bin/env python3
"""Dice se è il momento di fare i calcoli dopo una giornata.

Una giornata è chiusa quando tutte le sue partite di campionato hanno il risultato in data.json. La prima volta che la vede chiusa
lo segna in calcoli/giornate.json; dopo ATTESA_ORE ore (default 3) dice di eseguire. Dopo i calcoli la giornata si segna come fatta
(--fatta N, vale per tutte le giornate fino a N) e non si ripete.
Uso:  python3 calcoli/giornata_chiusa.py data.json            stampa esegui=true|false e giornata=N (per GitHub Actions)
      python3 calcoli/giornata_chiusa.py data.json --fatta N  segna la giornata N come elaborata
"""
import datetime, json, os, sys
from pathlib import Path

STATO = Path(__file__).resolve().parent / "giornate.json"
ATTESA_ORE = float(os.environ.get("ATTESA_ORE", "3"))
A = [x for x in sys.argv[1:] if not x.startswith("--")]


def adesso():
    return datetime.datetime.now(datetime.timezone.utc)


def main():
    stato = json.loads(STATO.read_text(encoding="utf-8")) if STATO.exists() else {}
    if "--fatta" in sys.argv:
        n = int(sys.argv[sys.argv.index("--fatta") + 1])
        for k in range(1, n + 1):   # i calcoli guardano tutta la stagione: tutte le giornate fino a N sono fatte
            stato.setdefault(str(k), {}).setdefault("fatta", adesso().isoformat())
        STATO.write_text(json.dumps(stato, indent=1), encoding="utf-8")
        return
    lega = json.loads(Path(A[0]).read_text(encoding="utf-8"))["cal"]["lega"]
    chiuse = [r["n"] for r in lega if r["m"] and all(m[4] and m[4] != "-" for m in r["m"])]
    esegui, giornata = False, ""
    for n in sorted(chiuse):
        s = stato.setdefault(str(n), {})
        if s.get("fatta"):
            continue
        if "visto" not in s:
            s["visto"] = adesso().isoformat()
            print(f"Giornata {n}: chiusa, la segno. Calcoli tra {ATTESA_ORE:g} ore.", file=sys.stderr)
        elif adesso() - datetime.datetime.fromisoformat(s["visto"]) >= datetime.timedelta(hours=ATTESA_ORE):
            esegui, giornata = True, str(n)
            break
    STATO.write_text(json.dumps(stato, indent=1), encoding="utf-8")
    print(f"esegui={'true' if esegui else 'false'}")
    print(f"giornata={giornata}")


if __name__ == "__main__":
    main()
