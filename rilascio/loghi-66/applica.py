#!/usr/bin/env python3
"""Loghi della 6.6 (Gianluca, 24 novembre 2026): scudi per sempre, simboli col pallone per la stagione.

- Scudo della Lega «SINCE 2020 · 21» (assets/loghi/scudo-lega.png): Home, Albo d'oro, Derby, Rivalità, Versioni, Notifiche
  e i pulsanti che riportano alla Home. Scudo della Champions Cup «SINCE 2025 · 26» (scudo-coppa.png) pronto per Albo e record della Coppa.
- Simbolo di stagione col pallone e «2026 · 27» (stagione-campionato.png, stagione-coppa.png in azzurro): Tabellone, Campo,
  Squadre, Statistiche, Totogirrr, Giornale; in Tabellone e Campo cambia con l'interruttore Campionato/Champions Cup.
Uso: python3 rilascio/loghi-66/applica.py CARTELLA_GH_PAGES   (idempotente: la seconda volta «File cambiati: 0»)
"""
import shutil, sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
L, C = "logo-lega-o-fant-a-girrr.png", "logo-cup-champions-cup.png"
URL = "https://giandjcosta.github.io/o-fant-a-girrr/assets/loghi/"
PER_SEMPRE = ["index", "albo", "derby", "rivalita", "versioni", "notifiche"]
STAGIONE = ["tabellone", "squadre", "statistiche", "giornale"]


def cambia(f, coppie):
    s = f.read_text(encoding="utf-8"); o = s
    for a, b, n in coppie:
        s = s.replace(a, b) if n is None else s.replace(a, b, n)
    if s != o:
        f.write_text(s, encoding="utf-8"); return 1
    return 0


def applica(sito):
    (sito / "assets/loghi").mkdir(parents=True, exist_ok=True)
    for x in (QUI / "assets").iterdir():
        shutil.copyfile(x, sito / "assets/loghi" / x.name)
    n = 0
    for d in ("girrr", "stadio/girrr"):
        for p in PER_SEMPRE:
            n += cambia(sito / d / (p + ".html"), [("loghi/" + L, "loghi/scudo-lega.png", None)])
        for p in STAGIONE:
            n += cambia(sito / d / (p + ".html"), [("loghi/" + L, "loghi/stagione-campionato.png", None), ("loghi/" + C, "loghi/stagione-coppa.png", None)])
        # Campo: il logo nella barra laterale riporta alla Home (scudo); titolo e cambio Campionato/Coppa sono di stagione
        n += cambia(sito / d / "campo.html", [(URL + L, URL + "scudo-lega.png", 1), (URL + L, URL + "stagione-campionato.png", None), (URL + C, URL + "stagione-coppa.png", None)])
        # Totogirrr: piccolo logo all'ingresso
        n += cambia(sito / d / "totogirrr.html", [("assets/logo-lega.png", "assets/loghi/stagione-campionato.png", None)])
    # pulsanti che riportano alla Home (barra 5.5)
    for f in ("girrr/v55/ui.js", "girrr/v55/destinazioni55.js"):
        n += cambia(sito / f, [(URL + L, URL + "scudo-lega.png", None)])
    print("File cambiati:", n)


if __name__ == "__main__":
    applica(Path(sys.argv[1]))
