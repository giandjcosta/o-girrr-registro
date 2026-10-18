#!/usr/bin/env python3
"""Mette il pacchetto di rilascio nel repo della lega, in locale. NON fa push: il push lo fai (o lo dai) tu, dopo il "vai".

Uso:
  python3 rilascio/applica.py --gh-pages <cartella con gh-pages> --main <cartella con main>          prova a vuoto: elenca cosa cambierebbe
  python3 rilascio/applica.py --gh-pages ... --main ... --vai                                      copia e fa i commit in locale

Fa in ordine:
  1. copia gh-pages/ del pacchetto sopra il ramo gh-pages (pagine nuove, app.html, dati, voci);
  2. copia main/ del pacchetto sopra il ramo main (workflow nuovi e script dei calcoli);
  3. scrive la data di oggi in calcoli/curva_config.json ("rilascio"): da lì parte il periodo di approvazione dei post della Curva (14 giorni);
  4. commit in locale, uno per ramo. Non tocca mai .github/workflows/aggiorna-dati.yml.
"""
import datetime, filecmp, json, pathlib, shutil, subprocess, sys

PAC = pathlib.Path(__file__).resolve().parent / "pacchetto"
A = sys.argv[1:]
VAI = "--vai" in A
def arg(n):
    return pathlib.Path(A[A.index(n) + 1]) if n in A else sys.exit(f"Manca {n}")
GH, MAIN = arg("--gh-pages"), arg("--main")
INTOCCABILI = {".github/workflows/aggiorna-dati.yml", ".github/workflows/riepilogo.yml"}
TRAILER = "\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01GK5zscNUimtKKY8gDEaZw5"


def piano(sorg, dest):
    nuovi, cambiati = [], []
    for f in sorted(p for p in sorg.rglob("*") if p.is_file()):
        rel = f.relative_to(sorg).as_posix()
        if rel in INTOCCABILI:
            continue
        d = dest / rel
        if not d.exists():
            nuovi.append(rel)
        elif not filecmp.cmp(f, d, shallow=False):
            cambiati.append(rel)
    return nuovi, cambiati


def copia(sorg, dest, rel):
    (dest / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(sorg / rel, dest / rel)


def git(d, *a):
    subprocess.check_call(["git", "-C", str(d), *a])


def main():
    for nome, sorg, dest in (("gh-pages", PAC / "gh-pages", GH), ("main", PAC / "main", MAIN)):
        nuovi, cambiati = piano(sorg, dest)
        print(f"{nome}: {len(nuovi)} file nuovi, {len(cambiati)} cambiati")
        for r in cambiati:
            print("   cambiato:", r)
        if VAI:
            for r in nuovi + cambiati:
                copia(sorg, dest, r)
    if not VAI:
        print("Prova a vuoto: aggiungi --vai per copiare e fare i commit in locale.")
        return
    cfg = MAIN / "calcoli" / "curva_config.json"
    c = json.loads(cfg.read_text(encoding="utf-8"))
    c["rilascio"] = datetime.date.today().isoformat()
    cfg.write_text(json.dumps(c, indent=1, ensure_ascii=False), encoding="utf-8")
    git(GH, "add", "-A")
    git(GH, "commit", "-m", "5.0: pagine nuove (Girrr Sport, Spogliatoio, Totogirrr, Carriera), Derby e Sfide" + TRAILER)
    git(MAIN, "add", "-A")
    git(MAIN, "commit", "-m", "5.0: workflow dei calcoli e della coda della Curva, script dei calcoli" + TRAILER)
    print("Fatto in locale. Per pubblicare: git push origin gh-pages (cartella gh-pages) e git push origin main (cartella main).")


if __name__ == "__main__":
    main()
