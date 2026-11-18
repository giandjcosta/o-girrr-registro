#!/usr/bin/env python3
"""6.5 (Gianluca, 18 novembre) · schermate browser reale: iPhone, iPad, PC, Smart TV.
Solo lettura e locale, senza Supabase o browser a pagamento.
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

BASE="http://127.0.0.1:8767/lab/integrata-62/"
OUT=Path("qa_artifacts/65-layout")
OUT.mkdir(parents=True,exist_ok=True)

async def main():
    report=[]
    async with async_playwright() as pw:
      browser=await pw.chromium.launch(headless=True)
      configs=[
       ("iphone-se",320,700),("iphone",390,844),("ipad",1024,1366),
       ("pc",1440,900),("smart-tv",1920,1080),("tv-4k-css",2560,1440)
      ]
      for name,width,height in configs:
       context=await browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1,reduced_motion="reduce")
       page=await context.new_page()
       errors=[]
       page.on("pageerror",lambda e: errors.append(str(e)))
       async def route(req):
           if req.request.method not in ("GET","HEAD"):await req.abort()
           elif not req.request.url.startswith("http://127.0.0.1:8767/"):
               await req.fulfill(status=204,body="")
           else:await req.continue_()
       await page.route("**/*",route)
       url=BASE+"girrr/tabellone.html?evento=notte-tropicale#lega"
       await page.goto(url,wait_until="domcontentloaded")
       await page.wait_for_timeout(1100)
       nav=page.locator(".giornata-nav.v55-schede")
       count=await nav.locator(":scope > button, :scope > a").count()
       boxes=await nav.locator(":scope > button, :scope > a").evaluate_all(
          "(els)=>els.map(e=>{const r=e.getBoundingClientRect();return {t:e.textContent.trim(),x:r.x,y:r.y,w:r.width,h:r.height,scroll:e.scrollWidth,client:e.clientWidth}})")
       no_wrap=count==4 and len(boxes)==4 and max(x["y"] for x in boxes)-min(x["y"] for x in boxes)<3
       overall=await page.evaluate("({html:document.documentElement.scrollWidth,body:document.body.scrollWidth,client:document.documentElement.clientWidth,mode:document.body.dataset.mode,theme:document.documentElement.getAttribute('data-event-theme')})")
       await page.screenshot(path=str(OUT/f"tabellone-{name}-{width}.png"),full_page=True,animations="disabled")
       entry={"screen":name,"width":width,"navCount":count,"nav":boxes,"sameRow":no_wrap,"metrics":overall,"pageErrors":errors[:5]}
       # Gianluca, 18/11: su telefoni la fila deve davvero scorrere orizzontalmente.
       # Non basta che le tab siano allineate; tutte e quattro devono essere raggiungibili.
       if width<=600:
           nav_scroll=await nav.evaluate("""el=>{
               const s=getComputedStyle(el),max=el.scrollWidth-el.clientWidth;
               el.scrollLeft=max;
               return {scrollWidth:el.scrollWidth,clientWidth:el.clientWidth,
                       maxScroll:max,actualScroll:el.scrollLeft,overflowX:s.overflowX,
                       flexWrap:s.flexWrap};
           }""")
           entry["navScroll"]=nav_scroll
           await page.screenshot(path=str(OUT/f"tabellone-{name}-{width}-scroll-finale.png"),
                                 full_page=True,animations="disabled")
           await nav.evaluate("(el)=>el.scrollLeft=0")
       # Tocchi funzionali: non serve un browser remoto o dati reali
       if name in ("iphone-se","iphone","ipad"):
           try:
               await nav.locator('button[data-sez="risultati"]').click()
               entry["risultati"]=await page.evaluate("location.search+'|'+document.querySelector('.grid>section').hidden")
               await nav.locator('button[data-sez="classifica"]').click()
               entry["classifica"]=await page.evaluate("location.search+'|'+document.querySelector('.grid>aside.panel').hidden")
               await nav.locator('a[data-v65-numeri]').click()
               await page.wait_for_timeout(700)
               entry["numeri"]={"url":page.url,"exists":await page.locator("#v65numeri").count(),"visible":await page.locator("#v65numeri").is_visible()}
           except Exception as e:
               entry["interactionError"]=str(e)
       report.append(entry)
       print(json.dumps(entry,ensure_ascii=False)[:1300])
       # La Home appartiene allo stesso tema, ma Curva è un riquadro indipendente.
       if name in ("iphone","ipad","pc","smart-tv"):
           await page.goto(BASE+"girrr/index.html?evento=notte-tropicale",wait_until="domcontentloaded")
           await page.wait_for_timeout(1150)
           home=await page.evaluate("""() => {
             const cards=document.querySelector('.wrap>.cards'),curva=document.querySelector('#cvw');
             const rv=curva?.getBoundingClientRect(), rc=cards?.getBoundingClientRect();
             return {curvaInCards:!!cards?.contains(curva),curvaSotto:!!rv&&!!rc&&rv.top>=rc.bottom-2,
               miniOutside:Array.from(document.querySelectorAll('.wrap>.mini')).length,cardCount:cards?.querySelectorAll(':scope>.c').length,
               overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth};
           }""")
           await page.screenshot(path=str(OUT/f"home-{name}-{width}.png"),full_page=True,animations="disabled")
           report.append({"screen":"home-"+name,**home})
       await context.close()
      await browser.close()
    (OUT/"rapporto.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    problems=[r for r in report if r.get("sameRow") is False or r.get("navCount",4)!=4 or
      (r.get("metrics",{}).get("html",0)>r.get("metrics",{}).get("client",0)+1) or
      r.get("pageErrors") or r.get("interactionError") or r.get("curvaInCards") is True or r.get("curvaSotto") is False or
      (r.get("width",999)>0 and r.get("width",999)<=600 and
       (r.get("navScroll",{}).get("maxScroll",0)<40 or
        r.get("navScroll",{}).get("actualScroll",0)<30 or
        r.get("navScroll",{}).get("overflowX") not in ("auto","scroll") or
        r.get("navScroll",{}).get("flexWrap")!="nowrap"))]
    print("Problemi rilevati:",len(problems))
    for p in problems:print("ATTENZIONE",json.dumps(p,ensure_ascii=False)[:2000])
    if problems:raise SystemExit(1)

if __name__=="__main__":
    asyncio.run(main())
