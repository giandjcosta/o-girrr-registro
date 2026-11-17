#!/usr/bin/env python3
"""ChatGPT, 17/11/2026 · Prova dei Numeri del Campionato e delle sei foto nel Lab.
Chromium, HTTP locale 8767, solo GET; niente scritture a Supabase.
Foto, statistiche e link controllati sul DOM reale. Screenshot della Home e della pagina.
"""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8767/lab/integrata-62/girrr/"
OUT = Path("qa_artifacts/notte-tropicale")
OUT.mkdir(parents=True, exist_ok=True)
SIZES = ((320,760),(390,844),(768,960),(1440,900))
PHOTOS = [
    "photo-1670349218709-1c246063c319",
    "photo-1759171053149-d5cce4261405",
    "photo-1767397194546-c51509f4a715",
    "photo-1700085626695-6532f02cc961",
    "photo-1637203727770-3fff478fb1ef",
    "photo-1770237710424-7ffa780f68d1",
]

def main():
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        try:
            for width,height in SIZES:
                ctx=browser.new_context(viewport={"width":width,"height":height},
                    has_touch=width<600,is_mobile=width<600,device_scale_factor=1)
                # Evita ogni POST o PUT verso servizi reali.
                ctx.route("**/*",lambda route: route.continue_() if route.request.method in ("GET","HEAD","OPTIONS")
                          else route.abort("blockedbyclient"))
                page=ctx.new_page()
                try:
                    checks={}
                    page.goto(BASE+"index.html?evento=notte-tropicale",wait_until="domcontentloaded",timeout=25000)
                    page.locator(".nt-stagione").wait_for(timeout=15000)
                    page.wait_for_timeout(500)
                    home=page.evaluate("""() => {
                      const e=document.querySelector('.nt-stagione');
                      const cards=[...document.querySelectorAll('.wrap>.cards>.c')];
                      return {href:e.getAttribute('href'),theme:document.documentElement.getAttribute('data-event-theme'),
                        images:cards.map(c=>getComputedStyle(c).backgroundImage),
                        overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth};
                    }""")
                    checks["Home mostra Stagione link corretto"]=home["href"]=="numeri-campionato.html?evento=notte-tropicale"
                    checks["Home senza overflow"]=home["overflow"]<=1
                    checks["Sei foto distinte abbinate nell'ordine"]=len(home["images"])>=6 and all(
                        PHOTOS[i] in home["images"][i] for i in range(6))
                    if width in (390,1440):
                        page.screenshot(path=str(OUT/f"home-foto-sei-{width}.jpg"),type="jpeg",quality=82,full_page=True)

                    page.locator(".nt-stagione").click()
                    page.wait_for_url("**/numeri-campionato.html?evento=notte-tropicale",timeout=15000)
                    page.locator(".nt-stat").first.wait_for(timeout=15000)
                    detail=page.evaluate("""() => ({
                      title:document.querySelector('.nt-numeri h2')?.textContent,
                      cards:document.querySelectorAll('.nt-stat').length,
                      big:document.querySelectorAll('.nt-stat-grande').length,
                      theme:document.documentElement.getAttribute('data-event-theme'),
                      overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,
                      page:document.querySelector('.nt-numeri-meta')?.innerText,
                      stats:(typeof statsCampionato==='function'&&typeof renderStats==='function'),
                      empty:document.querySelector('#nt-numeri-contenuto')?.getAttribute('aria-busy')
                    })""")
                    checks["Nuova pagina raggiungibile dalla Home"]=page.url.endswith("numeri-campionato.html?evento=notte-tropicale")
                    checks["Statistiche calcolate su dati reali"]=detail["cards"]==14 and detail["big"]==4 and detail["stats"] and detail["empty"]=="false"
                    checks["Titolo Numeri del Campionato"]=detail["title"]=="Numeri del Campionato"
                    checks["Pagina statistiche senza overflow"]=detail["overflow"]<=1
                    checks["Tema attivo nella pagina"]=detail["theme"]=="notte-tropicale"
                    if width in (320,390,1440):
                        page.screenshot(path=str(OUT/f"numeri-campionato-{width}.jpg"),type="jpeg",quality=83,full_page=True)

                    page.goto(BASE+"tabellone.html?evento=notte-tropicale",wait_until="domcontentloaded",timeout=25000)
                    page.locator(".giornata-nav .nt-numeri-link").wait_for(timeout=13000)
                    isdisplay=page.locator(".nt-numeri-link").evaluate("(e) => getComputedStyle(e).display !== 'none'")
                    checks["Tabellone Campionato mostra Numeri"]=isdisplay
                    checks["Menu Campionato porta alla pagina nuova"]=page.locator(".nt-numeri-link").get_attribute("href")=="numeri-campionato.html?evento=notte-tropicale"
                    page.evaluate("document.body.setAttribute('data-mode','coppa')")
                    hidden=page.locator(".nt-numeri-link").evaluate("(e) => getComputedStyle(e).display === 'none'")
                    checks["Champions Cup non mostra Numeri Campionato"]=hidden
                    row={"width":width,"ok":all(checks.values()),"checks":checks,"detail":detail}
                    results.append(row)
                    print(("OK" if row["ok"] else "KO"),width,
                          [n for n,good in checks.items() if not good],flush=True)
                except Exception as e:
                    results.append({"width":width,"ok":False,"error":str(e)[:450]})
                    print("KO",width,str(e)[:200],flush=True)
                finally:
                    ctx.close()
        finally:
            browser.close()
    report={"passed":sum(int(x["ok"]) for x in results),"total":len(results),"rows":results}
    (OUT/"rapporto-numeri-foto.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Numeri e Foto:",report["passed"],"/",report["total"])
    return 0 if report["passed"]==report["total"] else 1
if __name__=="__main__":
    sys.exit(main())
