#!/usr/bin/env python3
"""ChatGPT · 17/11/2026 · Home Notte Tropicale: controllo dei difetti segnalati da Gianluca.
Non modifica i dati: intercetta tutte le richieste HTTP non GET e verifica la Home reale
del Lab usando Chromium. Acquisisce screenshot del layout e della fila a fine scorrimento.
Comando: python3 temi/notte-tropicale/prova_home_schede.py
(prima avviare python3 -m http.server 8767 dalla radice del Registro).
"""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get("NT_HOME_URL", "http://127.0.0.1:8767/lab/integrata-62/girrr/index.html")
OUT = Path(os.environ.get("NT_QA_OUT", "qa_artifacts/notte-tropicale"))
OUT.mkdir(parents=True, exist_ok=True)

JS = """() => {
 const root=document.documentElement;
 const titolo=document.getElementById('nt-tutto-titolo');
 const fila=document.querySelector('.wrap > .cards');
 const s=sel=>document.querySelector(sel);
 const vis=e=>e&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;
 const tituloOrdine=()=>({
   titolo:getComputedStyle(titolo).order,
   fila:getComputedStyle(fila).order
 });
 const ct=[...document.querySelectorAll('#strip > .st')].filter(vis)
   .map(e=>{const v=e.querySelector('.vai');return {label:v?.textContent.trim()||'',top:e.getBoundingClientRect().top,
      bottom:v?.getBoundingClientRect().bottom||0}});
 return {
  tema:root.getAttribute('data-event-theme'),integrata:root.classList.contains('nt-rail-integrata'),
  titolo:!!titolo,fuoriDallaFila:!!(titolo&&fila&&!fila.contains(titolo)),
  ordine:!!(titolo&&fila&&titolo.nextElementSibling===fila),
  titoloVisivamenteSopra:!!(titolo&&fila&&
    titolo.getBoundingClientRect().bottom<=fila.getBoundingClientRect().top+2&&
    fila.getBoundingClientRect().top-titolo.getBoundingClientRect().bottom<65),
  ordineCSS:tituloOrdine(),
  carte:fila?.querySelectorAll(':scope > .c').length||0,
  altre:fila?.querySelectorAll(':scope > .nt-slide').length||0,
  curva:!!(s('#cvw')&&fila?.contains(s('#cvw'))),
  notifiche:!!(s('.mini .mn[href="notifiche.html"]')&&fila?.contains(s('.mini .mn[href="notifiche.html"]'))),
  statistiche:!!(s('.mini .mn[href="statistiche.html"]')&&fila?.contains(s('.mini .mn[href="statistiche.html"]'))),
  sponsor:!!(s('.sp')&&fila?.contains(s('.sp'))),
  titoliInPagina:[...document.querySelectorAll('#nt-tutto-titolo')].length,
  overflow:root.scrollWidth-root.clientWidth,client:root.clientWidth,scroll:fila?.scrollWidth||0,
  scrollPort:fila?.clientWidth||0,ct:ct
 };
}"""


def run():
    result=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        try:
            for width,height in ((320,750),(390,844),(768,960),(1440,900)):
                context=browser.new_context(viewport={"width":width,"height":height},
                                            has_touch=width<600,is_mobile=width<600,
                                            device_scale_factor=1)
                context.route("**/*", lambda route: route.continue_() if route.request.method in ("GET","HEAD","OPTIONS") else route.abort("blockedbyclient"))
                page=context.new_page()
                errors=[]
                page.on("pageerror",lambda e:errors.append(str(e)))
                try:
                    page.goto(BASE+"?evento=notte-tropicale",wait_until="domcontentloaded",timeout=20000)
                    page.locator("#nt-tutto-titolo").wait_for(timeout=12000)
                    page.wait_for_timeout(3100)  # completa i dati read-only e la classifica
                    measure=page.evaluate(JS)
                    problems=[]
                    for key in ("integrata","titolo","fuoriDallaFila","ordine","titoloVisivamenteSopra","curva","notifiche","statistiche","sponsor"):
                        if not measure.get(key):problems.append("manca "+key)
                    if measure.get("carte")!=6:problems.append("schede originali non sono sei")
                    if measure.get("altre")!=4:problems.append("schede aggiunte non sono quattro")
                    if measure.get("titoliInPagina")!=1:problems.append("titolo duplicato")
                    if measure.get("overflow",100)>0:problems.append("overflow documento")
                    if measure.get("tema")!="notte-tropicale":problems.append("tema disattivato")
                    ct=measure.get("ct") or []
                    results=[x for x in ct if "RISULTATI" in x["label"].upper()]
                    groups=[x for x in ct if "GIRONI" in x["label"].upper()]
                    if not results or not groups:problems.append("azioni competizioni assenti")
                    if results and groups and abs(results[0]["top"]-groups[0]["top"])<8:
                        if abs(results[0]["bottom"]-groups[0]["bottom"])>3:
                            problems.append("azioni non allineate: delta "+str(round(abs(results[0]["bottom"]-groups[0]["bottom"]),2)))
                    # Verifica scroll reale: solo la fila deve muoversi, non il suo titolo.
                    if width<900:
                        before=page.evaluate("""() => {let c=document.querySelector('.wrap>.cards'),
                           h=document.getElementById('nt-tutto-titolo');return {left:h.getBoundingClientRect().left,
                           rail:c.scrollLeft,scrollMax:c.scrollWidth-c.clientWidth}}""")
                        page.evaluate("""() => {let c=document.querySelector('.wrap>.cards'); c.scrollLeft=c.scrollWidth}""")
                        page.wait_for_timeout(280)
                        after=page.evaluate("""() => {let c=document.querySelector('.wrap>.cards'),
                           h=document.getElementById('nt-tutto-titolo');return {left:h.getBoundingClientRect().left,
                           rail:c.scrollLeft}}""")
                        if before["scrollMax"]<10 or abs(after["rail"]-before["rail"])<10:
                            problems.append("la fila non scorre")
                        if abs(after["left"]-before["left"])>1:
                            problems.append("titolo si muove orizzontalmente")
                        # Foto della coda della fila, con il titolo visibile anche sul telefono.
                        page.evaluate("""() => {
                           const h=document.getElementById('nt-tutto-titolo');
                           window.scrollTo(0,Math.max(0,h.getBoundingClientRect().top+scrollY-95))
                        }""")
                        page.wait_for_timeout(120)
                        page.screenshot(path=str(OUT/f"home-{width}-fila-finale.jpg"),type="jpeg",quality=82)
                    # Screenshot di pagina reale, non immagine sintetica.
                    page.evaluate("window.scrollTo(0,0)")
                    page.screenshot(path=str(OUT/f"home-{width}-intera.jpg"),type="jpeg",quality=81,full_page=True)
                    if errors:problems.extend(["errore JS "+x[:160] for x in errors[:2]])
                    row={"larghezza":width,"ok":not problems,"problemi":problems,"metriche":measure}
                    result.append(row)
                    print(("OK" if row["ok"] else "KO"),width,problems,flush=True)
                except Exception as exc:
                    result.append({"larghezza":width,"ok":False,"problemi":[str(exc)[:400]]})
                    print("KO",width,str(exc)[:200],flush=True)
                finally:
                    context.close()
        finally:
            browser.close()
    report={"superati":sum(1 for x in result if x["ok"]),"totale":len(result),"casi":result}
    (OUT/"rapporto-home.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Home: ",report["superati"],"/",report["totale"],flush=True)
    if report["superati"]!=report["totale"]:raise SystemExit(1)

if __name__=="__main__":run()
