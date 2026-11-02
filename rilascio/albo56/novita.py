#!/usr/bin/env python3
"""Albo d'oro (girrr/albo.html con novita.js): ritocchi chiesti da Gianluca il 2 novembre 2026.

Uso: python3 rilascio/albo56/novita.py FILE [FILE ...]   (girrr/novita.js e stadio/girrr/novita.js di gh-pages)
Modifica sul posto; se un file è già aggiornato lo lascia stare.

- Albo di Latta, nota sotto «La latta di sempre»: il 2022/23 è già contato (campionato a sei);
  tolta la frase sbagliata e la spiegazione di «Ultimo», che si capisce da sola.
- Pillole «Questa stagione / Di sempre» e delle giornate: rosse nella grafica Lega, oro nello Stadio.
- Riquadri interni della storia (.rac): nella Lega banda rossa dritta di 8 px e angoli 4/14 px;
  nello Stadio restano come sono.
"""
import sys
from pathlib import Path

SOST = [
    ("""<p class="lnt">"Metà bassa" conta le stagioni chiuse nella parte bassa della classifica, "Ultimo" quelle chiuse all\\'ultimo posto. La stagione 2022/23 non c\\'è, perché la classifica completa non si è conservata.</p>""",
     """<p class="lnt">"Metà bassa" conta le stagioni chiuse nella parte bassa della classifica. Il 2022/23 conta con le sei squadre di quel campionato.</p>"""),
    ("#latbox .lseg button[aria-pressed=true]{background:var(--hi);color:#141d3d}",
     "#latbox .lseg button[aria-pressed=true]{background:var(--hi);color:#141d3d}html.alb-lega #latbox .lseg button[aria-pressed=true]{background:#d62839;color:#fff}"
     "html.alb-lega .rac{border-left:8px solid #d62839;border-radius:4px 14px 14px 4px}"),
    ("var LAB=",
     "/* Gianluca, 2 novembre: nella Lega accento rosso e riquadri dritti, nello Stadio oro */document.documentElement.classList.toggle('alb-lega',!/stadio/i.test(location.pathname));\nvar LAB="),
]

for f in sys.argv[1:]:
    p = Path(f)
    t = p.read_text(encoding="utf-8")
    cambiato = False
    for a, b in SOST:
        if b in t:
            continue
        if t.count(a) != 1:
            raise SystemExit(f"{f}: atteso una volta, trovato {t.count(a)}: {a[:70]}…")
        t = t.replace(a, b)
        cambiato = True
    if cambiato:
        p.write_text(t, encoding="utf-8")
    print(("aggiornato " if cambiato else "già aggiornato ") + f)
