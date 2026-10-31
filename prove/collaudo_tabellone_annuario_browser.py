#!/usr/bin/env python3
"""Collaudo di Tabellone (Lega/Stadio) e Annuario (Lab), senza scritture remote."""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8765"
CLUB = ["The Blue brothers", "Apo team", "Mariana Coneja", "stif dc",
        "Real Madrink", "Atletico ma non troppo", "Oranje VC", "AFA SELECCION", "Grodah", "WOA"]


def dati():
    def gol(p):
        return max(0, 1 + int((p - 66) // 5)) if p >= 66 else 0
    teams = [{"name": name, "pl": [{"id": 100 + i, "c": i * 3 + 10}]} for i, name in enumerate(CLUB)]
    P = {str(100 + i): {"n": "Giocatore " + str(i), "r": "A", "t": "Club",
                        "q": 1, "f": i * 3 + 10} for i in range(10)}
    lega = []
    for n in range(1, 9):
        order = CLUB[n % 10:] + CLUB[:n % 10]
        matches = []
        for j in range(5):
            a, b = order[2*j], order[2*j+1]
            x = 63 + ((n * 9 + j * 5) % 28)
            y = 63 + ((n * 4 + j * 11) % 28)
            matches.append([a, x if n <= 5 else 0, y if n <= 5 else 0,
                            b, f"{gol(x)}-{gol(y)}" if n <= 5 else "-"])
        lega.append({"n": n, "sa": n+4, "m": matches})
    cup = []
    for n in range(1, 11):
        m, rests = [], []
        for gr, noms in [("A", CLUB[:5]), ("B", CLUB[5:])]:
            order = noms[n % 5:] + noms[:n % 5]
            rests.append([gr, order[4]])
            for j in range(2):
                a, b = order[j*2], order[j*2+1]
                x, y = 67 + j*7 + n, 69 + j*4 + n
                m.append([gr, a, x if n <= 2 else 0, y if n <= 2 else 0,
                          b, f"{gol(x)}-{gol(y)}" if n <= 2 else "-"])
        cup.append({"n": n, "sa": n+4, "m": m, "rest": rests})
    return {"updated": "2026-10-31", "teams": teams, "P": P,
            "ps": {str(100+i): {"g": i % 4, "as": i % 3} for i in range(10)},
            "cal": {"lega": lega, "cup": cup}, "lock": {}}


def main():
    fixture = dati()
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for width in (320, 1280):
            for skin in ("lega", "stadio"):
                page = browser.new_page(viewport={"width": width, "height": 800})
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.route("**/data.json*", lambda route: route.fulfill(status=200, content_type="application/json", body=json.dumps(fixture)))
                page.route("**/novita-dati.js*", lambda route: route.fulfill(status=200, content_type="text/javascript", body="window.NOV={riv:[]};"))
                for name in ("ospite.js", "pub.js", "transizioni.js"):
                    page.route(f"**/{name}*", lambda route: route.fulfill(status=200, content_type="text/javascript", body=""))
                page.route("**/rest/v1/rpc/derby_stato", lambda route: route.fulfill(status=200, content_type="application/json", body='{"voti":[],"nomi":[]}'))
                page.goto(f"{BASE}/lab/prova-tabellone-{skin}.html", wait_until="domcontentloaded")
                page.locator(".panel table").first.wait_for(timeout=15000)
                page.wait_for_timeout(550)
                assert page.locator(".formadots").count() == 10, (skin, width, "Forma")
                assert page.locator(".zoneleg").count() == 1, (skin, width, "Zone")
                assert page.locator(".turnoprossimo").count() == 1, (skin, width, "Prossima")
                assert page.locator(".movpos").count() > 0, (skin, width, "Freccia")
                media_display = page.locator("td.med").first.evaluate("(e) => getComputedStyle(e).display")
                assert (media_display != "none") == (width >= 560), (skin, width, "Media")
                page.locator(".clubgraph").first.click()
                page.locator(".grafpos svg").wait_for(timeout=10000)
                assert page.locator(".grafpos polyline").count() == 1
                page.wait_for_timeout(350)
                scroll = page.evaluate("document.documentElement.scrollWidth")
                assert scroll <= width + 1, (skin, width, "overflow", scroll)
                page.get_by_role("tab", name="Champions Cup").click()
                page.locator(".panel table").first.wait_for()
                page.wait_for_timeout(350)
                assert page.locator(".zoneleg").count() == 0, (skin, width, "Zone solo Lega")
                scroll = page.evaluate("document.documentElement.scrollWidth")
                assert scroll <= width + 1, (skin, width, "overflow Coppa", scroll)
                print(f"PASS tabellone {skin} {width}px")
                page.close()
            page = browser.new_page(viewport={"width": width, "height": 800})
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.route("**/data.json*", lambda route: route.fulfill(status=200, content_type="application/json", body=json.dumps(fixture)))
            page.goto(f"{BASE}/lab/index.html", wait_until="domcontentloaded")
            page.locator('[data-tab="oro"]').first.click()
            page.locator('[data-oro="annuario"]').first.click()
            page.locator(".ann-anno").first.wait_for(timeout=10000)
            page.wait_for_timeout(450)
            assert page.get_by_text("Giocatore più pagato").count() >= 1
            assert page.get_by_text("Dato non conservato").count() >= 1
            scroll = page.evaluate("document.documentElement.scrollWidth")
            assert scroll <= width + 1, ("annuario", width, "overflow", scroll)
            print(f"PASS annuario {width}px")
            page.close()
        browser.close()
    assert not errors, "Errori Javascript: " + "; ".join(errors[:10])
    print("PASS nessun errore JavaScript nuovo")


if __name__ == "__main__":
    main()
