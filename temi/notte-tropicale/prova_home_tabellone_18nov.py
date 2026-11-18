#!/usr/bin/env python3
"""ChatGPT · 18 novembre 2026.
QA vero delle correzioni richieste: persistenza del riepilogo Home,
distanza Curva, link «Numeri del Campionato» nel Tabellone.
Chromium/Playwright, solo GET; nessuna scrittura ai servizi reali.
Avvio dalla root: python3 -m http.server 8767
Poi: python3 temi/notte-tropicale/prova_home_tabellone_18nov.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import sys

ROOT = "http://127.0.0.1:8767/lab/integrata-62/girrr/"
OUT = Path("qa_artifacts/notte-tropicale")
OUT.mkdir(parents=True, exist_ok=True)

def check(browser, width, height):
    ctx = browser.new_context(
        viewport={"width": width, "height": height},
        is_mobile=width <= 390, has_touch=width <= 390,
        device_scale_factor=1)
    ctx.route("**/*", lambda r: r.continue_()
        if r.request.method in ("GET", "HEAD", "OPTIONS")
        else r.abort("blockedbyclient"))
    page = ctx.new_page()
    issues, errors = [], []
    page.on("pageerror", lambda e: errors.append(str(e)))
    try:
        # Stato iniziale: rimuovi solo la preferenza locale nella sessione di test.
        page.goto(ROOT + "index.html?evento=notte-tropicale",
                  wait_until="domcontentloaded", timeout=20000)
        page.evaluate("localStorage.removeItem('og:53:home-open')")
        page.reload(wait_until="domcontentloaded")
        page.locator("#v55dashboard").wait_for(timeout=18000)
        page.wait_for_timeout(300)
        dash = page.locator("#v55dashboard")
        if dash.evaluate("(e)=>e.open"):
            issues.append("Prima visita: riepilogo non chiuso")
        summary = page.locator("#v55dashboard > summary")
        summary.click()
        if not dash.evaluate("(e)=>e.open"):
            issues.append("Il riepilogo non si apre al tocco")
        page.wait_for_timeout(450)
        page.reload(wait_until="domcontentloaded")
        page.locator("#v55dashboard").wait_for(timeout=18000)
        if not page.locator("#v55dashboard").evaluate("(e)=>e.open"):
            issues.append("Stato aperto non ricordato")
        page.locator("#v55dashboard > summary").click()
        page.wait_for_timeout(450)
        page.reload(wait_until="domcontentloaded")
        page.locator("#v55dashboard").wait_for(timeout=18000)
        if page.locator("#v55dashboard").evaluate("(e)=>e.open"):
            issues.append("Stato chiuso non ricordato")

        page.locator("#cvw.nt-slide-curva").wait_for(timeout=15000)
        curve = page.evaluate("""() => {
          const row=document.querySelector('.wrap>.cards');
          const curve=document.querySelector('#cvw.nt-slide-curva');
          const before=curve && curve.previousElementSibling;
          if(!row || !curve || !before)return {found:false};
          curve.scrollIntoView({block:'nearest',inline:'center'});
          const css=getComputedStyle(curve);
          const rect=curve.getBoundingClientRect(),prev=before.getBoundingClientRect();
          return {found:true,inside:row.contains(curve),
                  margin:parseFloat(css.marginInlineStart),
                  gap:rect.left-prev.right,
                  scrollWidth:document.documentElement.scrollWidth,
                  clientWidth:document.documentElement.clientWidth};
        }""")
        if not curve.get("found") or not curve.get("inside"):
            issues.append("Curva non è nella fila delle schede")
        if curve.get("margin", 0) < 15:
            issues.append("Distanza aggiuntiva Curva inferiore a 15px")
        if curve.get("scrollWidth", 99999) > curve.get("clientWidth", 0)+2:
            issues.append("Overflow orizzontale Home")
        link=page.locator(".nt-stagione").get_attribute("href")
        if link!="numeri-campionato.html?evento=notte-tropicale":
            issues.append("Stagione non conduce alla pagina separata")
        page.screenshot(path=str(OUT/f"home-persistenza-curva-{width}.jpg"),
                        type="jpeg", quality=76, full_page=False)

        # Pagina del Tabellone: deve esistere nel menu alto, non solo nei contenuti.
        page.goto(ROOT + "tabellone.html?evento=notte-tropicale",
                  wait_until="domcontentloaded", timeout=20000)
        page.locator(".giornata-nav .nt-numeri-link").wait_for(timeout=15000)
        top=page.locator(".giornata-nav .nt-numeri-link")
        if not top.is_visible():
            issues.append("Link Numeri non visibile nella barra alta")
        if top.get_attribute("href")!="numeri-campionato.html?evento=notte-tropicale":
            issues.append("Link Numeri non porta alla pagina separata")
        if top.count()!=1:
            issues.append("Link Numeri duplicato")
        page.screenshot(path=str(OUT/f"tabellone-numeri-link-{width}.jpg"),
                        type="jpeg", quality=77, full_page=False)
        top.click()
        page.wait_for_url("**/numeri-campionato.html?evento=notte-tropicale",timeout=14000)
        page.locator(".nt-stat").first.wait_for(timeout=14000)
        if not page.locator("body.nt-numeri-pagina").count():
            issues.append("Navigazione non apre la pagina separata")
        if page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 2"):
            issues.append("Overflow orizzontale Numeri")
        page.locator(".nt-ritorno").click()
        page.wait_for_url("**/tabellone.html?evento=notte-tropicale",timeout=14000)
        if errors:
            issues.append("Errori JavaScript: "+" | ".join(errors[:2]))
        return {"width":width,"ok":not issues,"issues":issues,"curva":curve}
    except Exception as e:
        issues.append(str(e)[:380])
        return {"width":width,"ok":False,"issues":issues}
    finally:
        ctx.close()

def main():
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        try:
            results=[check(browser,w,h) for w,h in [(320,740),(390,844),(1440,900)]]
        finally:
            browser.close()
    (OUT/"rapporto-home-tabellone-18nov.json").write_text(
        json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    for r in results:
        print("OK" if r["ok"] else "KO",r["width"],r["issues"],flush=True)
    sys.exit(0 if all(r["ok"] for r in results) else 1)

if __name__=="__main__":
    main()
