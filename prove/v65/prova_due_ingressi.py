#!/usr/bin/env python3
"""Notte Tropicale 6.5: confronta due animazioni sul Lab, niente produzione."""
import asyncio, io, json, os
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.async_api import async_playwright

OUT=Path("qa_artifacts/65-ingressi")
OUT.mkdir(parents=True, exist_ok=True)
BASE="http://127.0.0.1:8767/lab/integrata-62/girrr/index.html"
MODES=("copertina","trasformazione")

async def capture(pw,mode,width,height,device):
    browser=await pw.chromium.launch(headless=True)
    context=await browser.new_context(viewport={"width":width,"height":height},
                                      device_scale_factor=1,reduced_motion="no-preference")
    page=await context.new_page()
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    async def route(route):
        req=route.request
        if req.method not in ("GET","HEAD"):
            await route.abort()
        elif not req.url.startswith("http://127.0.0.1:8767/"):
            await route.fulfill(status=204,body="")
        else:
            await route.continue_()
    await page.route("**/*",route)
    url=BASE+"?evento=notte-tropicale&evento-intro="+mode
    await page.goto(url,wait_until="domcontentloaded",timeout=30000)
    frames=[];states=[];interval=260
    for i in range(19):
        picture=await page.screenshot(full_page=False,animations="allow")
        im=Image.open(io.BytesIO(picture)).convert("RGB")
        size=(390,844) if device=="mobile" else (960,600)
        im.thumbnail(size,Image.Resampling.LANCZOS)
        frames.append(im)
        states.append(await page.evaluate("({state:document.documentElement.getAttribute('data-intro-state'),theme:document.documentElement.getAttribute('data-event-theme'),mode:document.documentElement.getAttribute('data-intro-preview'),vt:!!document.startViewTransition})"))
        await page.wait_for_timeout(interval)
    await page.screenshot(path=str(OUT/f"{mode}-{device}-final.png"),full_page=True)
    target=OUT/f"{mode}-{device}.gif"
    frames[0].save(target,save_all=True,append_images=frames[1:],loop=0,
                   duration=[interval]*(len(frames)-1)+[900],optimize=True)
    result={"variant":mode,"device":device,"width":width,"height":height,
            "finalState":states[-1],"states":states,"pageErrors":errors[:8],
            "gif":str(target),"screenshot":f"{mode}-{device}-final.png"}
    await context.close()
    await browser.close()
    return result,frames

async def main():
    results={}; animations={}
    async with async_playwright() as pw:
        for mode in MODES:
            for device,w,h in [("mobile",390,844),("pc",1440,900)]:
                report,frames=await capture(pw,mode,w,h,device)
                results[mode+"-"+device]=report
                animations[mode+"-"+device]=frames
                print(mode,device,report["finalState"],"errors",report["pageErrors"])
        # Confronto animato fianco a fianco: iPhone a sx Copertina, a dx Trasformazione.
        left=animations["copertina-mobile"];right=animations["trasformazione-mobile"]
        composed=[]
        for a,b in zip(left,right):
            out=Image.new("RGB",(a.width+b.width+12,max(a.height,b.height)+38),"#170c33")
            out.paste(a,(0,38));out.paste(b,(a.width+12,38))
            d=ImageDraw.Draw(out)
            d.text((12,11),"A  COPERTINA",fill="#ffb2cf")
            d.text((a.width+24,11),"B  TRASFORMAZIONE",fill="#8aeafa")
            composed.append(out)
        composed[0].save(OUT/"confronto-due-ingressi.gif",save_all=True,
                        append_images=composed[1:],loop=0,duration=[260]*18+[900],
                        optimize=True)
    (OUT/"rapporto.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    problems=[]
    for name,r in results.items():
        if r["pageErrors"] or r["finalState"]["state"]!="completo" or
           r["finalState"]["theme"]!="notte-tropicale":
            problems.append(name)
        states=[x["state"] for x in r["states"]]
        if r["variant"]=="copertina" and "uscita" not in states:
            problems.append(name+"-uscita")
        if r["variant"]=="trasformazione" and "transizione" not in states:
            problems.append(name+"-transizione")
    print("PROBLEMI:",problems)
    if problems:raise SystemExit(1)

if __name__=="__main__":
    asyncio.run(main())
