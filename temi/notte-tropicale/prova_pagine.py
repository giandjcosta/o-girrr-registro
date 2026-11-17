#!/usr/bin/env python3
"""QA della grafica vera Notte Tropicale sulle pagine rimanenti (ChatGPT, 17/11/2026).
Esegue Chromium/Playwright, serve HTML locali dal Registro e non scrive dati.
Per ogni sezione: 320, 390, 1440 px; nessun overflow, nessun errore nuovo,
colori rossi generici assenti fuori dalle competizioni. Screenshot JPG + report JSON.
Il test confronta gli errori console del tema con la pagina identica ?evento=off.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

SIZES = ((320, 760), (390, 844), (1440, 900))
PAGES = (
    ("totogirrr", "girrr/totogirrr.html", "&demo"),
    ("carriera", "girrr/app.html", "#carriera"),
    ("girrr-sport", "girrr/app.html", "#sport"),
    ("albo-app", "girrr/app.html", "#oro"),
    ("derby-app", "girrr/app.html", "#derby"),
    ("albo", "girrr/albo.html", ""),
    ("giornale", "girrr/giornale.html", ""),
    ("spogliatoio", "index.html", ""),
    ("squadre", "girrr/squadre.html", ""),
    ("versioni", "girrr/versioni.html", ""),
    ("notifiche", "girrr/notifiche.html", ""),
    ("derby", "girrr/derby.html", ""),
)
PAGE_READY = {
    "totogirrr": "#app",
    "carriera": "#view",
    "girrr-sport": "#view",
    "albo-app": "#view",
    "derby-app": "#view",
    "albo": "#al",
    "giornale": "#ultimo",
    "spogliatoio": "#app",
    "squadre": "#sch",
    "versioni": "#versioni",
    "notifiche": "#v53notifications",
    "derby": "#al",
}
IGNORE_ERRORS = ["ERR_ABORTED"]  # richieste cancellate da navigazione, non errori JS


def url(base: str, path: str, suffix: str, on: bool) -> str:
    name = urljoin(base, path)
    state = "notte-tropicale" if on else "off"
    if suffix.startswith("&"):
        return name + "?evento=" + state + suffix
    return name + "?evento=" + state + suffix


def check_one(browser, base, label, path, suffix, width, height, out):
    context = browser.new_context(viewport={"width": width, "height": height},
                                  is_mobile=width < 500, has_touch=width < 500,
                                  device_scale_factor=1)
    # Evita qualsiasi POST/PUT/DELETE verso database, analytics e altri servizi esterni.
    def safe_route(route):
        req = route.request
        if req.method.upper() not in ("GET", "HEAD", "OPTIONS"):
            route.abort("blockedbyclient")
        else:
            route.continue_()
    context.route("**/*", safe_route)

    def inspect(on):
        page = context.new_page()
        errors, js_errors = [], []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: js_errors.append(str(e)))
        target = url(base, path, suffix, on)
        status = "ok"
        try:
            page.goto(target, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(1450)
            try:
                page.locator(PAGE_READY[label]).first.wait_for(timeout=3500)
            except PlaywrightTimeout:
                status = "contenitore di pagina assente"
            metrics = page.evaluate("""() => {
                const r=document.documentElement, z=document.body;
                const els=[...document.querySelectorAll('.nt-obl,.nt-tab')]
                    .filter(x=>x.getBoundingClientRect().height > 0).slice(0,300);
                const rgb = (s) => {
                    const m=/rgba?\\((\\d+)[, ]+([0-9]+)[, ]+([0-9]+)/.exec(s||'');
                    return m ? [Number(m[1]),Number(m[2]),Number(m[3])] : null;
                };
                const isRed = s => {
                    const c=rgb(s);
                    return c && c[0]>135 && c[1]<108 && c[2]<112
                        && c[0]>c[1]*1.4 && c[0]>c[2]*1.35;
                };
                const reds = [];
                for(const e of els) {
                    // Escludi colori delle competizioni e indicatori sportivi: non sono decorazioni generiche.
                    if(e.closest('.sw,.comp-sw,.chips,.cup,[data-mode=coppa],.m,.match,.gh.cup')) continue;
                    const c=getComputedStyle(e),b=getComputedStyle(e,'::before');
                    for(const k of ['backgroundColor','borderLeftColor','borderTopColor']) {
                        if(isRed(c[k]) || isRed(b[k])) { reds.push({el:e.tagName+'.'+e.className,kind:k,value:c[k]}); break; }
                    }
                    if(reds.length>=8)break;
                }
                return {theme:r.getAttribute('data-event-theme'),
                  width:r.scrollWidth,client:r.clientWidth,bodyWidth:z.scrollWidth,
                  obl:document.querySelectorAll('.nt-obl').length,
                  tab:document.querySelectorAll('.nt-tab').length,
                  redDecorations:reds};
            }""")
            if on:
                shot = out / f"{label}-{width}.jpg"
                page.screenshot(path=str(shot), type="jpeg", quality=78, full_page=False, timeout=20000)
            return dict(state=status, metrics=metrics, errors=errors, js_errors=js_errors, url=target)
        except Exception as e:
            return dict(state=str(e)[:400], metrics={}, errors=errors, js_errors=js_errors, url=target)
        finally:
            page.close()

    try:
        # Prima linea di base: stessi dati, stessi servizi, evento spento.
        base_result = inspect(False)
        themed = inspect(True)
        bm = base_result.get("metrics") or {}
        mm = themed.get("metrics") or {}
        old_errors = set(base_result.get("errors", []) + base_result.get("js_errors", []))
        all_new_errors = themed.get("errors", []) + themed.get("js_errors", [])
        new_errors = [e for e in all_new_errors if e not in old_errors
                      and not any(ign in e for ign in IGNORE_ERRORS)]
        failures = []
        if themed["state"] != "ok": failures.append(themed["state"])
        if mm.get("theme") != "notte-tropicale": failures.append("tema non attivo")
        if mm.get("width", 9999) > mm.get("client", 0): failures.append("overflow laterale")
        if mm.get("redDecorations"): failures.append("rosso decorativo fuori competizioni")
        if new_errors: failures.append("errori nuovi console / JavaScript")
        if mm.get("obl", 0) + mm.get("tab", 0) == 0: failures.append("nessun elemento tematizzato")
        return {"pagina":label,"width":width,"ok":not failures,"problemi":failures,
                "misure":mm,"console_nuova":new_errors[:8],
                "console_base":list(old_errors)[:5],"url":themed["url"]}
    finally:
        context.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="http://127.0.0.1:8767/lab/integrata-62/")
    p.add_argument("--browser", default="chromium", choices=["chromium", "webkit", "firefox"])
    p.add_argument("--out", default="qa_artifacts/notte-tropicale")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as pw:
        engine = getattr(pw, a.browser)
        browser = engine.launch(headless=True)
        try:
            for label, path, suffix in PAGES:
                for w, h in SIZES:
                    r = check_one(browser, a.base, label, path, suffix, w, h, out)
                    results.append(r)
                    print(("OK" if r["ok"] else "KO"), label, w,
                          ",".join(r["problemi"]), flush=True)
            # La Curva NON deve ricevere il tema (decisione Claude/Gianluca).
            with browser.new_page() as pg:
                pg.goto(url(a.base, "girrr/curva.html", "", True),
                        wait_until="domcontentloaded", timeout=20000)
                pg.wait_for_timeout(400)
                excluded = pg.evaluate("document.documentElement.getAttribute('data-event-theme') !== 'notte-tropicale'")
                results.append({"pagina": "curva-esclusa", "width": 390,
                                "ok": excluded, "problemi": [] if excluded else ["Curva tematizzata per errore"]})
        finally:
            browser.close()
    report = {"totale":len(results), "superati":sum(x["ok"] for x in results),
              "falliti":[x for x in results if not x["ok"]],"risultati":results}
    (out / "rapporto.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Verifiche: {report['superati']}/{report['totale']}; screenshot in {out}",flush=True)
    sys.exit(0 if report["superati"] == report["totale"] else 1)

if __name__ == "__main__":
    main()
