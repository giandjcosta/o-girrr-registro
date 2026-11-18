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
                    # Screenshot Gianluca: il solo ritorno è ‹ Tabellone;
                    # niente tre link intermedi, secondo ritorno o sponsor.
                    struttura=page.evaluate("""() => {
                        const back=document.querySelector('.nt-ritorno');
                        const box=document.querySelector('.nt-stat');
                        const before=box?getComputedStyle(box,'::before'):null;
                        const header=document.querySelector('.nt-numeri-header');
                        const headBefore=header?getComputedStyle(header,'::before'):null;
                        return {
                            backText:back?back.textContent.trim():'',
                            backHref:back?back.getAttribute('href'):'',
                            nav:document.querySelectorAll('.nt-numeri-nav').length,
                            backLinks:document.querySelectorAll('a.nt-ritorno').length,
                            footerLinks:document.querySelectorAll('.nt-numeri-footer a').length,
                            sponsors:document.querySelectorAll('.sp,.sponsor,.nt-slide-sponsor').length,
                            sponsorWords:document.body.textContent.indexOf('Gentilmente offerto da')>=0,
                            cardsBackground:box?getComputedStyle(box).backgroundColor:'',
                            cardSkew:before?before.transform:'',
                            cardInlay:before?before.boxShadow:'',
                            cardBeforeFill:before?before.backgroundImage:'',
                            headerSkew:headBefore?headBefore.transform:'',
                            headerInlay:headBefore?headBefore.boxShadow:''
                        };
                    }""")
                    checks["Unico ritorno in alto verso Tabellone"]=(
                        struttura["backText"]=="‹ Tabellone" and
                        struttura["backHref"]=="tabellone.html?evento=notte-tropicale" and
                        struttura["backLinks"]==1 and struttura["footerLinks"]==0)
                    checks["Tre link superflui eliminati"]=struttura["nav"]==0
                    checks["Nessuna pubblicità in Numeri"]=struttura["sponsors"]==0 and not struttura["sponsorWords"]
                    checks["Filo integrato nella sagoma obliqua"]=(
                        struttura["cardSkew"]!="none" and
                        "inset" in struttura["cardInlay"] and
                        "rgb(" in struttura["cardInlay"] and
                        struttura["headerSkew"]!="none")
                    # Controllo di ritorno anche sul link reale, non solo sull'href.
                    page.locator(".nt-ritorno").click()
                    page.wait_for_url("**/tabellone.html?evento=notte-tropicale",timeout=12000)
                    checks["Tocco sul ritorno apre Tabellone"]=page.url.endswith(
                        "tabellone.html?evento=notte-tropicale")
                    page.go_back(wait_until="domcontentloaded")
                    page.locator(".nt-stat").first.wait_for(timeout=15000)
                    if width in (320,390,1440):
                        page.screenshot(path=str(OUT/f"numeri-campionato-{width}.jpg"),type="jpeg",quality=83,full_page=True)

                    page.goto(BASE+"tabellone.html?evento=notte-tropicale",wait_until="domcontentloaded",timeout=25000)
                    page.locator(".giornata-nav .nt-numeri-link").wait_for(timeout=13000)
                    isdisplay=page.locator(".nt-numeri-link").evaluate("(e) => getComputedStyle(e).display !== 'none'")
                    checks["Tabellone Campionato mostra Numeri"]=isdisplay
                    checks["Menu Campionato porta alla pagina nuova"]=page.locator(".nt-numeri-link").get_attribute("href")=="numeri-campionato.html?evento=notte-tropicale"
                    # Stessa grafica sulle quattro voci, senza creare nuove sezioni dati.
                    menu=page.evaluate("""() => {
                      const nav=document.querySelector('.giornata-nav');
                      const el=[...nav.querySelectorAll(':scope > a:not([hidden])')];
                      return {
                        pronto:nav.classList.contains('nt-quattro-menu'),
                        nomi:el.map(x=>x.textContent.trim()),
                        link:el.map(x=>x.getAttribute('href')),
                        oltre:document.documentElement.scrollWidth-document.documentElement.clientWidth,
                        fili:el.map(x=>{
                          const cs=getComputedStyle(x,'::before');
                          return {transform:cs.transform,ombra:cs.boxShadow,
                            fondo:cs.backgroundImage};
                        }),
                        footerOriginale:document.querySelectorAll('.sp').length
                      };
                    }""")
                    checks["Quattro voci vere nella barra del Tabellone"]=menu["nomi"]==[
                        "Classifica","Risultati","Numeri del Campionato","Campo"]
                    checks["Le due voci interne conducono ai pannelli esistenti"]=(
                        menu["link"][:3]==["#tab","#board",
                            "numeri-campionato.html?evento=notte-tropicale"] and
                        menu["link"][3].startswith("campo.html"))
                    checks["Stesso stile obliquo e fili su quattro voci"]=(
                        menu["pronto"] and all(x["transform"]!="none" and
                        "inset" in x["ombra"] and
                        "gradient" in x["fondo"] for x in menu["fili"]))
                    checks["Quattro voci senza overflow"]=menu["oltre"]<=2
                    # Le prime due voci scorrono ai pannelli autentici, senza
                    # creare nuove schermate o cambiare risultati/classifiche.
                    page.locator(".giornata-nav .nt-classifica-link").click()
                    checks["Classifica apre il pannello esistente"]=(
                        page.url.endswith("#tab") and
                        page.locator("#tab").is_visible() and
                        page.locator(".nt-classifica-link").get_attribute("aria-current")=="location")
                    page.locator(".giornata-nav .nt-risultati-link").click()
                    checks["Risultati apre il pannello esistente"]=(
                        page.url.endswith("#board") and
                        page.locator("#board").is_visible() and
                        page.locator(".nt-risultati-link").get_attribute("aria-current")=="location")
                    if width in (390,1440):
                        page.screenshot(path=str(OUT/f"tabellone-quattro-voci-{width}.jpg"),
                            type="jpeg",quality=81,full_page=False)
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
