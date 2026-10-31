#!/usr/bin/env python3
"""Prove visuali 320 / 768 / 1280 per Tabellone, Campo e Albo. Nessuna scrittura al sito."""
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = "http://127.0.0.1:8765"
OUT = Path("qa_artifacts")
OUT.mkdir(exist_ok=True)

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=["--no-sandbox"])
    for w in (320,768,1280):
        ctx=browser.new_context(viewport={"width":w,"height":850},device_scale_factor=1)
        ctx.route(re.compile(r"https?://[^/]+\.supabase\.co/.*"),
                  lambda r:r.fulfill(status=200,content_type="application/json",body='{"voti":[],"sfide":[]}'))
        for pth,short in [
            ("/lab/prova-tabellone-lega.html","tabellone-lega"),
            ("/lab/prova-tabellone-stadio.html","tabellone-stadio"),
            ("/lab/prova-dashboard-campo.html?skin=lega","campo-lega"),
            ("/lab/prova-dashboard-campo.html?skin=stadio","campo-stadio"),
            ("/lab/index.html#oro","albo")
        ]:
            p=ctx.new_page()
            errs=[]
            p.on("pageerror",lambda e:errs.append("JS: "+str(e)))
            p.on("console",lambda m:errs.append("Console: "+m.text) if m.type=="error" else None)
            p.goto(ROOT+pth,wait_until="domcontentloaded",timeout=35000)
            if short.startswith("tabellone"):
                p.locator("#tab table").first.wait_for(timeout=25000)
                p.locator("#tab .numpos").first.wait_for(timeout=10000)
                px=p.locator("#tab th").nth(1).evaluate("(e)=>parseFloat(getComputedStyle(e).fontSize)")
                assert px>=12, (short,w,"intestazione piccola",px)
                pos=p.locator("#tab tbody tr").first
                assert "zona-1" in pos.get_attribute("class"), (short,w,"campione non colorato")
            if short.startswith("campo"):
                p.locator("#matches .gamebtn").first.wait_for(timeout=25000)
                assert p.locator(".pitch svg").count()==1
                p.locator("#next").click()
                assert "Giornata" in p.locator("#roundtitle").inner_text()
                p.locator("#matches button").last.click()
                assert p.locator(".match-head .club").count()==2
            if short=="albo":
                p.locator(".oro-scroll button[data-oro='annuario']").click()
                p.wait_for_timeout(500)
                assert p.locator(".oro-scroll button[aria-pressed=true]").get_attribute("data-oro")=="annuario"
                assert p.locator(".oro-scroll").evaluate("(e)=>getComputedStyle(e).overflowX")=="auto"
            p.wait_for_timeout(600)
            extent=p.evaluate("({inner:innerWidth, scroll:document.documentElement.scrollWidth})")
            assert extent["scroll"]<=extent["inner"]+1,(short,w,"overflow",extent)
            assert not errs,(short,w,errs)
            p.screenshot(path=str(OUT/f"{short}-{w}.png"),full_page=True)
            print("PASS UI",short,w,extent,"console pulita")
            p.close()
        ctx.close()
    browser.close()
