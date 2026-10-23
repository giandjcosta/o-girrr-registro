#!/usr/bin/env python3
"""Costruisce il pacchetto di rilascio della 5.0 in rilascio/pacchetto/ (non tocca nessun sito).

  gh-pages/   pagine del sito vero: Lega (girrr/) e Stadio (stadio/girrr/), con la app delle novità (app.html), dati e voci della radio
  main/       workflow di GitHub Actions e script dei calcoli (cartella calcoli/)

Uso:  python3 rilascio/pacchetto.py
Poi: python3 rilascio/applica.py <repo della lega> (prova a vuoto) e, solo dopo il tuo "vai", con --vai.
"""
import json, os, pathlib, shutil, subprocess, sys, tempfile

R = pathlib.Path(__file__).resolve().parent.parent
PAC = R / "rilascio" / "pacchetto"
GH, MAIN = PAC / "gh-pages", PAC / "main"


def esegui(env, *cmd):
    subprocess.check_call([sys.executable, *cmd], cwd=R, env=dict(os.environ, **env))


def main():
    shutil.rmtree(PAC, ignore_errors=True)
    esegui({"RILASCIO": "1"}, "ufficiale/build.py")
    tmp = pathlib.Path(tempfile.mkdtemp())
    lega, stadio = GH / "girrr" / "app.html", GH / "stadio" / "girrr" / "app.html"
    base = {"APP_MODO": "reale", "APP_RIL": "1"}
    esegui(dict(base, APP_DATI="dati/lab-dati.json", APP_VOCI="voci/", APP_OUT_LEGA=str(lega), APP_OUT_STADIO=str(tmp / "x.html")), "anteprima/build.py")
    esegui(dict(base, APP_DATI="../../girrr/dati/lab-dati.json", APP_VOCI="../../girrr/voci/", APP_OUT_LEGA=str(tmp / "y.html"), APP_OUT_STADIO=str(stadio)), "anteprima/build.py")
    # dati di partenza (il workflow "Calcoli dopo la giornata" li rinnova)
    shutil.copytree(R / "anteprima" / "dati", GH / "girrr" / "dati")
    # voci della radio: solo i file che la app usa davvero
    V = R / "lab" / "voci"
    usati = {"archivio.json", "elenco.json", "elenco2.json", "puntata.json", "puntata.mp3", "radio-it.mp3", "radio-en.mp3"}
    def cerca(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in ("file", "audio", "src") and isinstance(v, str):
                    usati.add(v)
                cerca(v)
        elif isinstance(x, list):
            for i in x:
                cerca(i)
    for n in ("elenco.json", "elenco2.json", "puntata.json"):
        if (V / n).exists():
            cerca(json.loads((V / n).read_text(encoding="utf-8")))
    for f in sorted(usati):
        if (V / f).is_file():
            (GH / "girrr" / "voci" / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(V / f, GH / "girrr" / "voci" / f)
    shutil.copy(R / "lab" / "girrr-sport.png", GH / "girrr" / "girrr-sport.png")
    # main: workflow e calcoli (senza i file di stato, che nascono dal lavoro)
    (MAIN / ".github" / "workflows").mkdir(parents=True)
    for y in (R / "rilascio" / "workflow").glob("*.yml"):
        shutil.copy(y, MAIN / ".github" / "workflows" / y.name)
    (MAIN / "calcoli").mkdir()
    stato = {"eventi.json", "post_curva.json", "coda_curva.json", "pubblicati.json", "conferenze.json", "moviola.json"}
    for f in (R / "calcoli").iterdir():
        if f.is_file() and f.name not in stato and f.suffix in (".py", ".json", ".md"):
            shutil.copy(f, MAIN / "calcoli" / f.name)
    (MAIN / "calcoli" / "conferenze.json").write_text("[]", encoding="utf-8")
    # sfondo su un livello fisso a parte in tutte le pagine (Safari non rispetta background-attachment:fixed)
    sys.path.insert(0, str(R / "rilascio"))
    import sfondo
    for cartella in (GH / "girrr", GH / "stadio" / "girrr"):
        for f in sorted(cartella.glob("*.html")):
            t, k = sfondo.applica(f.read_text(encoding="utf-8"))
            if k:
                f.write_text(t, encoding="utf-8")
                print(f"sfondo fisso: {f.relative_to(GH)} ({k} regole)")
    n = sum(1 for _ in PAC.rglob("*") if _.is_file())
    mb = sum(f.stat().st_size for f in PAC.rglob("*") if f.is_file()) / 1e6
    print(f"Pacchetto pronto: {n} file, {mb:.1f} MB in {PAC}")


if __name__ == "__main__":
    main()
