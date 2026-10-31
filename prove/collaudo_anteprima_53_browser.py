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
 # L'ingresso storico mantiene le fixture pubbliche per prove controllate.
 # La QA completa ora verifica i menu nativi e fallisce anche su errori JS/404.
 import subprocess,sys
 subprocess.run([sys.executable,str(Path(__file__).with_name('prova_53_completa.py'))],check=True)
if __name__=="__main__":main()
