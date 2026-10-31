#!/usr/bin/env python3
"""Anteprima 5.3: controlla le due grafiche su pagine reali, senza scrivere al sito."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE="http://127.0.0.1:8765/anteprima/5.3/"
NAMES=["The Blue brothers","Apo team","Grodah","WOA","Real Madrink","stif dc","Mariana Coneja","AFA SELECCION","Oranje VC","Atletico ma non troppo"]
def fixture():
 teams=[{"name":name,"pl":[{"id":100+i,"c":9+i*3}]} for i,name in enumerate(NAMES)]
 cal=[]
 for day in range(1,6):
  pairs=[]
  order=NAMES[day:]+NAMES[:day]
  for j in range(5):
   a,b=order[2*j],order[2*j+1]
   sa,sb=68+day+j*2,64+day+j
   ga=max(0,1+(sa-66)//5) if sa>=66 else 0
   gb=max(0,1+(sb-66)//5) if sb>=66 else 0
   pairs.append([a,sa if day<5 else 0,sb if day<5 else 0,b,f"{ga}-{gb}" if day<5 else "-"])
  cal.append({"n":day,"sa":day+5,"m":pairs})
 cup=[]
 for d in range(1,11):
  x=[]
  for group,group_names in [("A",NAMES[:5]),("B",NAMES[5:])]:
   for j in range(2):
    x.append([group,group_names[j],70,68,group_names[(j+2)%5],"2-1" if d<3 else "-"])
  cup.append({"n":d,"sa":d+5,"m":x})
 return {"updated":"2026-10-31","teams":teams,"P":{str(100+i):{"n":"Giocatore "+str(i),"t":"Club","r":"A"} for i in range(10)},"cal":{"lega":cal,"cup":cup},"votes":{}}
def main():
 data=fixture()
 Path("anteprima/5.3/qa-screenshot").mkdir(parents=True,exist_ok=True)
 errs=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for skin in ["lega","stadio"]:
   for width in [320,390,1280]:
    pg=browser.new_page(viewport={"width":width,"height":900})
    pg.on("pageerror", lambda exc: errs.append(str(exc)))
    def route(r):
     url=r.request.url
     if "/anteprima/5.3/ui.js" in url:
      r.fulfill(status=200,content_type="application/javascript",body=Path("anteprima/5.3/ui.js").read_text())
     elif "/anteprima/5.3/ui.css" in url:
      r.fulfill(status=200,content_type="text/css",body=Path("anteprima/5.3/ui.css").read_text())
     elif url.split("?")[0].endswith("/data.json"):
      r.fulfill(status=200,content_type="application/json",headers={"access-control-allow-origin":"*"},body=json.dumps(data))
     elif "supabase.co" in url:
      r.abort()
     else:r.continue_()
    pg.route("**/*",route)
    def visit(path):
     pg.goto(BASE+path+"-"+skin+".html",wait_until="domcontentloaded",timeout=25000)
     pg.wait_for_selector(".v53-menu a",timeout=15000)
     assert pg.locator(".v53-menu a").count()==5,(skin,path,"nav")
     assert pg.evaluate("document.documentElement.scrollWidth")<=width+2,(skin,path,"overflow",pg.evaluate("document.documentElement.scrollWidth"))
    visit("index")
    pg.locator("#v53metrics .v53-metric").first.wait_for(timeout=12000)
    assert pg.locator("#v53metrics .v53-metric").count()==3
    assert pg.locator(".cards").count()==1
    assert pg.locator("#v53nav a").count()==5
    pg.locator("#v53team").select_option(label="WOA")
    pg.locator("#v53read").click()
    pg.screenshot(path=f"anteprima/5.3/qa-screenshot/home-{skin}-{width}.png",full_page=True)
    visit("tabellone")
    assert pg.locator("#board").count()==1 and pg.locator("#tab").count()==1
    pg.locator("#v53from option").first.wait_for(state="attached",timeout=12000)
    pg.locator('#v53boardtabs button[data-view="center"]').click()
    pg.locator("#v53matchstats .score").first.wait_for()
    assert "Fantapunti" in pg.locator("#v53matchstats").inner_text()
    pg.screenshot(path=f"anteprima/5.3/qa-screenshot/tabellone-{skin}-{width}.png",full_page=True)
    visit("albo")
    assert pg.locator("#al").count()==1
    pg.locator("#v53annual details").first.wait_for(timeout=12000)
    assert pg.locator("#v53annual details").count()==5
    assert "Fantapunti" in pg.locator("#v53annual").inner_text()
    pg.screenshot(path=f"anteprima/5.3/qa-screenshot/albo-{skin}-{width}.png",full_page=True)
    visit("curva")
    assert pg.locator("#vista").count()==1 and pg.locator("#nav").count()==1
    pg.locator("#v53vote input").first.wait_for(timeout=12000)
    pg.locator('#v53vote input').first.check()
    pg.locator('#v53vote button').click()
    pg.locator("#v53message").fill("Questa partita promette spettacolo!")
    pg.locator('#v53comment button').click()
    assert "Questa partita promette spettacolo!" in pg.locator("#v53usercomments").inner_text()
    assert pg.locator("#v53dialog .v53-comment").count()>=6
    pg.screenshot(path=f"anteprima/5.3/qa-screenshot/curva-{skin}-{width}.png",full_page=True)
    visit("notifiche")
    pg.locator("#v53notifications article").first.wait_for(timeout=12000)
    pg.locator('#v53filters button[data-f="curva"]').click()
    assert "Sondaggio della Curva" in pg.locator("#v53notifications").inner_text()
    pg.locator("#v53markread").click()
    pg.screenshot(path=f"anteprima/5.3/qa-screenshot/notifiche-{skin}-{width}.png",full_page=True)
    print("PASS",skin,width,"Home, Tabellone, Albo, Curva e Notifiche; navigazione e contenuti esistenti")
    pg.close()
  browser.close()
 # The copied original Curva can throw network-only errors when Supabase is blocked;
 # do not treat them as success of 5.3, but report for manual review.
 if errs:print("BROWSER ERRORS (original/preview; check):",errs[:12])
 print("COMPLETATO: screenshot e test DOM 5.3")
if __name__=="__main__":main()
