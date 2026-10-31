#!/usr/bin/env python3
"""Prova Lab nuova esperienza: browser, mobile, interazioni locali, dati pubblici intercettati."""
import json
from playwright.sync_api import sync_playwright
BASE="http://127.0.0.1:8765"
NAMES=["The Blue brothers","Apo team","Grodah","WOA","Real Madrink","stif dc","Mariana Coneja","AFA SELECCION","Oranje VC","Atletico ma non troppo"]
def fixture():
    teams=[{"name":name,"pl":[{"id":101+i,"c":10+i*8}]} for i,name in enumerate(NAMES)]
    PP={str(101+i):{"n":"Giocatore "+str(i),"r":"A","t":"Club"} for i in range(10)}
    cal=[]
    for k in range(1,7):
        pairs=[]
        order=NAMES[k:]+NAMES[:k]
        for j in range(5):
            a,b=order[2*j],order[2*j+1]
            v,w=67+(k*3+j*2)%19,65+(k*2+j)%17
            ga=max(0,1+int((v-66)//5)) if v>=66 else 0
            gb=max(0,1+int((w-66)//5)) if w>=66 else 0
            pairs.append([a,v if k<6 else 0,w if k<6 else 0,b,f"{ga}-{gb}" if k<6 else "-"])
        cal.append({"n":k,"sa":k+4,"m":pairs})
    cup=[]
    for k in range(1,11):
        m=[]
        for gr,ls in (("A",NAMES[:5]),("B",NAMES[5:])):
            seq=ls[k%5:]+ls[:k%5]
            for j in range(2):
                a,b=seq[j*2],seq[j*2+1]
                m.append([gr,a,72 if k<=2 else 0,69 if k<=2 else 0,b,"2-1" if k<=2 else "-"])
        cup.append({"n":k,"sa":k+4,"m":m})
    forms={}
    for k in range(1,6):
        forms[str(k+4)]={name:{"tit":[101+i],"pan":[]} for i,name in enumerate(NAMES)}
    return (
        {"updated":"2026-10-31","teams":teams,"P":PP,"votes":{str(101+i):{str(k+4):{"f":7+i/10} for k in range(1,6)} for i in range(10)},"cal":{"lega":cal,"cup":cup}},
        forms,{"fid":{name:70+i for i,name in enumerate(NAMES)}}
    )
def main():
    data,forms,lab=fixture()
    errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for skin in ("lega","stadio"):
            for width in (320,1280):
                page=browser.new_page(viewport={"width":width,"height":820})
                page.on("pageerror",lambda e:errors.append(str(e)))
                def route(r):
                    path=r.request.url
                    if path.endswith("/data.json"):
                        body=data
                    elif path.endswith("/formazioni.json"):
                        body=forms
                    elif path.endswith("/lab-dati.json"):
                        body=lab
                    else:
                        r.continue_()
                        return
                    r.fulfill(status=200,content_type="application/json",headers={"access-control-allow-origin":"*"},body=json.dumps(body))
                page.route("**/*",route)
                page.goto(f"{BASE}/lab/prova-esperienza-{skin}.html",wait_until="domcontentloaded")
                page.get_by_text("Prossimo avversario",exact=True).wait_for(timeout=10000)
                assert "Oggi al Girrr" in page.locator("#content").inner_text()
                assert "Verifica in corso" in page.locator("#content").inner_text()
                assert page.evaluate("document.documentElement.scrollWidth")<=width+1,(skin,width,"home overflow",page.evaluate("document.documentElement.scrollWidth"))
                page.get_by_role("button",name="Notifiche").click()
                page.get_by_text("Come apparirebbe una notifica push").wait_for()
                page.locator("[data-push]").click()
                page.get_by_role("button",name="Sondaggio").click()
                page.locator('input[name="voto"]').first.check()
                page.get_by_role("button",name="Esprimi preferenza").click()
                page.locator("#commentText").fill("La partita sarà interessante.")
                page.get_by_role("button",name="Pubblica").click()
                assert "La partita sarà interessante." in page.locator("#content").inner_text()
                page.get_by_role("button",name="La Curva").click()
                assert page.get_by_text("Il Cronista",exact=False).count()>0
                page.get_by_role("button",name="Centro partita").click()
                assert page.get_by_text("Le formazioni della Lega").count()>0
                page.get_by_role("button",name="Tabellone").click()
                assert page.get_by_text("Confronta due giornate").count()>0
                assert page.get_by_text("Champions Cup · Fase finale").count()>0
                page.locator("#fromRound").select_option("2")
                page.get_by_role("button",name="Annuario").click()
                assert page.get_by_text("La stagione, in numeri").count()>0
                assert page.evaluate("document.documentElement.scrollWidth")<=width+1,(skin,width,"annual overflow",page.evaluate("document.documentElement.scrollWidth"))
                print("PASS",skin,width,"px: Home, Notifiche, Sondaggio, Curva, Partita, Tabellone, Annuario")
                page.close()
        browser.close()
    assert not errors,"Nuovi errori JavaScript: "+", ".join(errors[:8])
    print("PASS nessun errore JavaScript")
if __name__=="__main__":
    main()
