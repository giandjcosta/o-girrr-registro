#!/usr/bin/env python3
"""17/11/2026: controlli statici gratuiti delle demo Vice City, senza rete."""
from pathlib import Path
from html.parser import HTMLParser

HERE = Path(__file__).resolve().parent
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            assert a["id"] not in self.ids, f"ID duplicato: {a['id']}"
            self.ids.add(a["id"])
        if tag in ("a", "link", "script") and (a.get("href") or a.get("src")):
            self.links.append(a.get("href") or a.get("src"))

def check(name):
    html = (HERE / name).read_text(encoding="utf-8")
    p = Links()
    p.feed(html)
    assert 'name="viewport"' in html, name
    assert 'data-event-theme="vice-city"' in html, name
    assert 'data-skin="girrr"' in html, name
    assert 'prefers-reduced-motion' in html, name
    assert "Supabase" in html or "SUPABASE" in html, name
    for link in p.links:
        if link.startswith(("http:", "https:", "#", "data:")):
            continue
        local = link.split("?", 1)[0].split("#", 1)[0]
        assert (HERE / local).is_file(), f"{name}: collegamento mancante {local}"
    print(f"OK statico: {name}, {len(p.links)} riferimenti")
check("anteprima-home.html")
check("anteprima-tabellone.html")
check("anteprima-carriera.html")
check("anteprima-totogirrr.html")
hub = Links()
hub.feed((HERE / "index.html").read_text(encoding="utf-8"))
for link in hub.links:
    if link.startswith(("http:", "https:", "#", "data:")):
        continue
    assert (HERE / link.split("?", 1)[0].split("#", 1)[0]).is_file(), f"Hub: collegamento mancante {link}"
print(f"OK statico: index.html, {len(hub.links)} riferimenti")
print("NOTA: non sostituisce prove reali Chromium/WebKit/Firefox o touch.")
