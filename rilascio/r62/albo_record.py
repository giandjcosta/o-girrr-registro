#!/usr/bin/env python3
"""6.2 · Albo d'oro › Record (Claude, 15 novembre 2026, richiesta di Gianluca).

- Copia albo62.js nella radice del sito e lo collega ad albo.html (Lega e Stadio): «MVP del campionato» (squadra con più
  MVP dei tifosi) e «La partita più seguita» (sondaggi delle partite, voti di allenatori, redazione e personaggi).
- Archivio MVP della 6.0: sotto la vincitrice il motivo della redazione che ha scelto proprio lei (prima: il primo voto
  della redazione, anche se riguardava un'altra squadra).
Uso: python3 rilascio/r62/albo_record.py COPIA_DI_GH_PAGES   (rieseguito non cambia nulla)
"""
import pathlib, sys

QUI = pathlib.Path(__file__).resolve().parent
TAG = {"girrr/albo.html": '<script src="../albo62.js?v=62-1" defer></script>', "stadio/girrr/albo.html": '<script src="../../albo62.js?v=62-1" defer></script>'}
MOT_OLD = "E(w.redazione?.[0]?.motivo||'Verdetto della redazione e dei tifosi.')"
MOT_NEW = "E((w.redazione||[]).find(v=>v.scelta===winner.team)?.motivo||'Verdetto della redazione e dei tifosi.')"


def main(base):
    (base / "albo62.js").write_text((QUI / "albo62.js").read_text(encoding="utf-8"), encoding="utf-8")
    for rel, tag in TAG.items():
        p = base / rel
        s = p.read_text(encoding="utf-8")
        if "albo62.js" not in s:
            if s.count("</head>") != 1:
                raise SystemExit(f"{rel}: pagina diversa da quella attesa")
            p.write_text(s.replace("</head>", tag + "</head>"), encoding="utf-8")
    p = base / "girrr/v60/tifosi.js"
    s = p.read_text(encoding="utf-8")
    if MOT_NEW not in s:
        if s.count(MOT_OLD) != 1:
            raise SystemExit("tifosi.js diverso da quello atteso (archivio MVP)")
        p.write_text(s.replace(MOT_OLD, MOT_NEW), encoding="utf-8")
    print("Albo › Record 6.2 pronto in", base)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(pathlib.Path(sys.argv[1]).resolve())
