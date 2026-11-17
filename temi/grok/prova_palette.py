#!/usr/bin/env python3
"""Controlla che i campioni della Notte tropicale restino allineati. 17 novembre 2026 (Grok)."""
from pathlib import Path

qui = Path(__file__).resolve().parent
css = (qui / "palette.css").read_text(encoding="utf-8")
html = (qui / "index.html").read_text(encoding="utf-8")
md = (qui / "PALETTE.md").read_text(encoding="utf-8")
attesi = ["#2b60da", "#ff4cb9", "#e6953e", "#ffffff", "#350054", "#ffbc24", "#6d016d"]
mancano = [c for c in attesi if c not in css.lower()]
if mancano:
    raise SystemExit("Nel CSS mancano: " + ", ".join(mancano))
if "http://" in html or "https://" in html:
    raise SystemExit("La pagina non deve caricare nulla da fuori")
if "VI" in html or "Pricedown" in html:
    raise SystemExit("La pagina visibile non deve citare il marchio o il suo carattere")
for c in ("#2B60DA", "#FF4CB9", "#E6953E", "#FFBC24", "#FFFFFF"):
    if c not in md:
        raise SystemExit("Nella nota manca " + c)
print("palette ok")
