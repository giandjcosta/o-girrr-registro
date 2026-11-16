"""6.2.1: verifiche statiche su checkout temporanei, mai su produzione/Supabase."""
from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit("Uso: python3 prove/v62/check621.py COPIA-GH-PAGES COPIA-BACKEND")

site, backend = (Path(x) for x in sys.argv[1:])
R = Path(__file__).resolve().parents[2]
assert site.is_dir() and backend.is_dir()

def has(base, name, *tokens):
    t = (base / name).read_text(encoding="utf-8")
    for token in tokens:
        assert token in t, f"{base / name}: manca {token!r}"
    return t

has(site, "girrr/v55/ui.js", "getAttribute('href')", "?sezione=")
has(site, "girrr/v55/home55.js", "dayLink(n,'classifica')")
has(site, "sondaggi62.js", "hasAttribute('data-v62-sondaggi')", "data-v62-precedenti", "min-height:36px")
has(site, "pillole.js", "var FERME", ".at,.dtab,.pt-competition")
has(site, "girrr/v60/tifosi.js", "data-pt-giurie", "personaggi_totali", "ptGiurieAperte")
for area in ("girrr", "stadio/girrr"):
    has(site, f"{area}/app.html", "function sfCont()", "sfide lanciate quest", "o.replaceChild(b.cloneNode(true),a)")
    has(site, f"{area}/novita.js", "lbody", "lb.animate")
    has(site, f"{area}/derby.js", "__dline", "data-dsez", "data-dp")
    has(site, f"{area}/albo.html", "se.best.n)")
    has(R / "lab/integrata-62", f"{area}/app.html", "function sfCont()", "o.replaceChild(b.cloneNode(true),a)")
    has(R / "lab/integrata-62", f"{area}/novita.js", "lbody")
    has(R / "lab/integrata-62", f"{area}/derby.js", "__dline")
has(R / "lab/integrata-62", "sondaggi62.js", "hasAttribute('data-v62-sondaggi')", "min-height:36px")
has(R / "lab/integrata-62", "pillole.js", "var FERME")
ctx = has(backend, "calcoli/tifosi/contesto.cjs", "rules.slice(0,5)", "week.stagione==='2026/27'", "week.giornata<8")
for who in ("Nonno Cesare", "Statistico Folle", "Il Romantico del Pallone", "Tifoso Arrabbiato",
            "Telecronista Stanco", "Il Complottista", "Gufo Professionista",
            "Il Mago della Cabala", "Il Tassista", "Arbitro in Pensione", "Klaus Pünktlich"):
    assert who in ctx, f"personaggio mancante: {who}"
print("6.2.1: controlli statici, script, Lab e backend: OK")
