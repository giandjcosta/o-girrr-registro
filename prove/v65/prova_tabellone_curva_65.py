#!/usr/bin/env python3
"""6.5 · Collaudo mirato sulle copie Lab, senza scritture esterne.
Uso: python3 prove/v65/prova_tabellone_curva_65.py --base http://127.0.0.1:8767/lab/integrata-62/
"""
import argparse
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def main(base, out):
    out.mkdir(parents=True,exist_ok=True)
    cases=[]
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True)
        for width in (320,390,1440):
            for skin,path in (("Lega","girrr/tabellone.html"),("Stadio","stadio/girrr/tabellone.html")):
                ctx=await browser.new_context(viewport={"width":width,"height":820},device_scale_factor=1)
                page=await ctx.new_page()
                errors=[]
                page.on("pageerror",lambda e: errors.append(str(e)))
                async def route(req):
                    if req.request.method!="GET":
                        await req.abort()
                    elif not req.request.url.startswith("http://127.0.0.1:8767"):
                        await req.fulfill(status=204,body="")
                    else:
                        await req.continue_()
                await page.route("**/*",route)
                for comp in ("lega","coppa"):
                    url=base+path+"?evento=off#"+comp
                    await page.goto(url,wait_until="domcontentloaded")
                    await page.wait_for_timeout(900)
                    if comp=="coppa":
                        await page.locator(".sw [data-m=coppa]").click()
                        await page.wait_for_timeout(400)
                    assert await page.locator("#v53board").count()==1
                    closed=await page.locator("#v53board").evaluate("(el)=>el.open")
                    assert not closed,f"{skin} {width}: approfondimenti aperti all'ingresso"
                    await page.locator("#v53board summary").click()
                    assert await page.locator("#v53board").evaluate("(el)=>el.open")
                    await page.locator("#v53board summary").click()
                    assert not await page.locator("#v53board").evaluate("(el)=>el.open")
                    metrics=await page.evaluate("({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,body:document.body.scrollWidth})")
                    assert metrics["scroll"]<=metrics["client"]+1 and metrics["body"]<=metrics["client"]+1,f"{skin} {comp} {width}: overflow {metrics}"
                    assert not errors,f"{skin} {comp} {width}: {errors}"
                    await page.screenshot(path=str(out/f"tab-{skin.lower()}-{comp}-{width}.png"),full_page=True)
                    cases.append({"page":skin,"competition":comp,"width":width,"overflow":False,"pageerrors":0})
                await ctx.close()
        # Curva: due skin, tre larghezze, tema chiaro/scuro.
        for width in (320,390,1440):
            for skin,path in (("Lega","girrr/curva.html"),("Stadio","stadio/girrr/curva.html")):
                for theme in ("light","dark"):
                    ctx=await browser.new_context(viewport={"width":width,"height":820},device_scale_factor=1)
                    page=await ctx.new_page()
                    errors=[]
                    page.on("pageerror",lambda e: errors.append(str(e)))
                    async def route(req):
                        if req.request.method!="GET":await req.abort()
                        elif not req.request.url.startswith("http://127.0.0.1:8767"):await req.fulfill(status=204,body="")
                        else:await req.continue_()
                    await page.route("**/*",route)
                    await page.goto(base+path+"?evento=off",wait_until="domcontentloaded")
                    await page.wait_for_timeout(500)
                    await page.evaluate("(theme)=>document.documentElement.setAttribute('data-theme',theme)",theme)
                    metrics=await page.evaluate("({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,body:document.body.scrollWidth})")
                    assert metrics["scroll"]<=metrics["client"]+1 and metrics["body"]<=metrics["client"]+1,f"Curva {skin} {theme} {width}: overflow {metrics}"
                    assert not errors,f"Curva {skin} {theme} {width}: {errors}"
                    await page.screenshot(path=str(out/f"curva-{skin.lower()}-{theme}-{width}.png"),full_page=True)
                    cases.append({"page":"Curva "+skin,"theme":theme,"width":width,"overflow":False,"pageerrors":0})
                    await ctx.close()
        await browser.close()
    (out/"rapporto.json").write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"6.5 · Tabellone e Curva: {len(cases)} casi superati in Chromium. iPhone/Android: identità non eseguita sui dispositivi fisici.")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--base",required=True);p.add_argument("--out",default="qa_artifacts/65_tab_curva")
    x=p.parse_args();asyncio.run(main(x.base,Path(x.out)))
