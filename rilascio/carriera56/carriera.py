#!/usr/bin/env python3
"""Carriera: loghi degli sponsor, niente riquadri vuoti, arco della fiducia animato ogni 5 minuti.

Uso: python3 rilascio/carriera56/carriera.py FILE [FILE ...]
FILE: lab/index.html (poi rigenerare l'Anteprima) oppure, al rilascio, girrr/app.html e
stadio/girrr/app.html di gh-pages. Modifica i file sul posto; se un file è già aggiornato lo lascia stare.

- Panoramica → Reputazione e sponsor: il logo di ogni sponsor accanto al suo obiettivo
  (stessi loghi di «Obiettivi», logo generico per chi non ne ha uno).
- Riquadri che entrano in dissolvenza: durante l'entrata niente sfocatura dello sfondo
  (backdrop-filter). Con sfocatura e dissolvenza insieme Chrome a volte disegnava solo lo
  sfondo sfocato e non il contenuto: il riquadro vuoto in Regole.
- Fiducia del presidente: se sono passati almeno 5 minuti dall'ultima volta, l'arco si
  colora da 0 al valore e il numero scorre come un tabellone, molto veloce. Con «riduci
  movimento» niente animazione.
- Reputazione da 0 a 100% (Gianluca, 2 novembre): si parte da 50; la posizione aggiunge o
  toglie un po' (+20 il primo, poi sempre meno fino a −20 l'ultimo); ogni obiettivo del
  presidente +10 se raggiunto e −10 se mancato, fino a fine stagione; ogni obiettivo di
  sponsor +1 o −1 per sempre (i malus li registra il workflow dei premi: malus52()).
"""
import sys
from pathlib import Path

SOST = [
    # 1. loghi degli sponsor in Reputazione e sponsor
    ("""+'<div class="row" style="padding:9px 0;border-top:1px solid var(--line);margin-top:8px;gap:6px 10px;flex-wrap:wrap"><span class="grow" style="min-width:60%"><b>'+esc(ps.sponsor)""",
     """+'<div class="row" style="padding:9px 0;border-top:1px solid var(--line);margin-top:8px;gap:6px 10px;flex-wrap:wrap"><img class="sp-logo" src="'+esc(SPIMG[ps.sponsor]||D.img.sp2)+'" alt="'+esc(ps.sponsor)+'"><span class="grow" style="flex:1 1 150px;min-width:0"><b>'+esc(ps.sponsor)"""),
    ("""+'<div class="row" style="padding:9px 0;border-top:1px solid var(--line);gap:6px 10px;flex-wrap:wrap"><span class="grow" style="min-width:60%"><b>'+esc(pc.sponsor)""",
     """+'<div class="row" style="padding:9px 0;border-top:1px solid var(--line);gap:6px 10px;flex-wrap:wrap"><img class="sp-logo" src="'+esc(SPIMG[pc.sponsor]||D.img.sp2)+'" alt="'+esc(pc.sponsor)+'"><span class="grow" style="flex:1 1 150px;min-width:0"><b>'+esc(pc.sponsor)"""),
    # 2. niente sfocatura durante l'entrata + stile dei loghi + scatto del numero
    ("st.textContent='@keyframes fxin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}.fx-in{animation:fxin .62s cubic-bezier(.22,.61,.36,1) both;animation-delay:calc(var(--fxd,0)*70ms)}",
     "st.textContent='@keyframes fxin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}.fx-in{animation:fxin .62s cubic-bezier(.22,.61,.36,1) both;animation-delay:calc(var(--fxd,0)*70ms);-webkit-backdrop-filter:none!important;backdrop-filter:none!important}"),
    (".trust-visual .trust-number.trust-flip{animation:trust-score-flip .52s ease-out both}",
     ".trust-visual .trust-number.trust-flip{animation:trust-score-flip .52s ease-out both}\n"
     ".trust-visual .trust-number.trust-tick{animation:trust-score-tick .08s ease-out}@keyframes trust-score-tick{0%{opacity:.45;transform:rotateX(-75deg)}to{opacity:1;transform:none}}\n"
     ".sp-logo{width:53px;height:35px;object-fit:contain;flex:0 0 53px;border-radius:6px}\n"
     "@media(prefers-reduced-motion:reduce){.trust-visual .trust-number.trust-tick{animation:none}}"),
    # 3. arco animato al massimo una volta ogni 5 minuti
    ("function animaFiducia(t,v){\n  var el=document.querySelector('#view .trust-visual');if(!el)return;\n  var path=el.querySelector('.trust-fill'),number=el.querySelector('.trust-number'),reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;\n  var previous=TRUSTANIM.value==null?v:TRUSTANIM.value;\n  TRUSTANIM.team=t;var id=++TRUSTANIM.token,from=previous,start=performance.now(),duration=reduce?0:520;\n  var card=el.querySelector('svg');card.setAttribute('aria-label','Fiducia del presidente '+v+' su 100');\n  if(from!==v&&!reduce){number.classList.remove('trust-flip');void number.getBoundingClientRect();number.classList.add('trust-flip')}\n  function frame(now){\n    if(id!==TRUSTANIM.token)return;\n    var x=duration?Math.min(1,(now-start)/duration):1, ease=1-Math.pow(1-x,3),cur=from+(v-from)*ease;\n    TRUSTANIM.value=cur;path.setAttribute('stroke-dasharray',cur.toFixed(3)+' 100');\n    number.textContent=String(Math.round(cur));\n    if(x<1)requestAnimationFrame(frame);else{TRUSTANIM.value=v;number.textContent=String(v);path.setAttribute('stroke-dasharray',v+' 100')}\n  }requestAnimationFrame(frame);\n}\n",
     "function animaFiducia(t,v){\n  var el=document.querySelector('#view .trust-visual');if(!el)return;\n  var path=el.querySelector('.trust-fill'),number=el.querySelector('.trust-number'),reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;\n  /* Gianluca: l'arco che si colora da zero e il numero che scorre come un tabellone, non a ogni ingresso ma al massimo ogni 5 minuti */\n  var G=TRUSTANIM.giro,giro=false,ora=Date.now(),ult=0;\n  if(G&&G.team===t&&G.v===v)giro=true;   /* la pagina si è ridisegnata durante il giro: si continua da dove era */\n  else if(!reduce){try{ult=+localStorage.getItem('orr_fid_anim')||0}catch(e){}\n    if(ora-ult>=300000){giro=true;G=TRUSTANIM.giro={team:t,v:v,start:null,duration:Math.max(700,Math.min(1500,v*18))};try{localStorage.setItem('orr_fid_anim',String(ora))}catch(e){}}}\n  var previous=giro?0:TRUSTANIM.value==null?v:TRUSTANIM.value,shown=null;\n  if(!giro)TRUSTANIM.giro=null;\n  TRUSTANIM.team=t;var id=++TRUSTANIM.token,from=previous,start=performance.now(),duration=reduce?0:520;\n  var card=el.querySelector('svg');card.setAttribute('aria-label','Fiducia del presidente '+v+' su 100');\n  if(from!==v&&!reduce&&!giro){number.classList.remove('trust-flip');void number.getBoundingClientRect();number.classList.add('trust-flip')}\n  function show(cur){TRUSTANIM.value=cur;path.setAttribute('stroke-dasharray',cur.toFixed(3)+' 100');var r=Math.round(cur);\n    if(r!==shown){shown=r;number.textContent=String(r);if(giro&&r!==v){number.classList.remove('trust-tick');void number.getBoundingClientRect();number.classList.add('trust-tick')}}}\n  function frame(now){\n    if(id!==TRUSTANIM.token)return;\n    if(giro){var nascosta=document.documentElement.classList.contains('v55-attesa')||document.hidden;   /* si parte quando la pagina si vede */\n      if(nascosta||G.start==null){if(!nascosta)G.start=now;show(0);requestAnimationFrame(frame);return}\n      start=G.start;duration=G.duration}\n    var x=duration?Math.min(1,(now-start)/duration):1, ease=1-Math.pow(1-x,3),cur=from+(v-from)*ease;\n    show(cur);\n    if(x<1)requestAnimationFrame(frame);else{TRUSTANIM.value=v;TRUSTANIM.giro=null;number.textContent=String(v);path.setAttribute('stroke-dasharray',v+' 100')}\n  }if(giro)show(G.start==null?0:TRUSTANIM.value||0);   /* niente lampo del numero finale quando la pagina si ridisegna */\n  requestAnimationFrame(frame);\n}\n"),
    # 4. reputazione da 0 a 100
    ("function vCarRiassunto(t,C){",
     "/* Gianluca, 2 novembre: reputazione da 0 a 100. Partenza 50; posizione da +20 (primo) a −20 (ultimo); obiettivi del presidente ±10 fino a fine stagione; sponsor ±1 per sempre. Ognuno con i suoi obiettivi */\n"
     "function repCalcolo(t,o){var r=row(t),n=Math.max(2,D.teams.length),pp=Math.round(20-(r.pos-1)*40/(n-1)),pr=0,sp=0;o.forEach(function(x){var v=x[4]==='Fatto'?1:x[4]==='Mancato'?-1:0;if(x[0])pr+=10*v;else sp+=v});return {pos:r.pos,pp:pp,pr:pr,sp:sp,tot:Math.max(0,Math.min(100,50+pp+pr+sp))}}\n"
     "function repBlocco(t,o){var q=repCalcolo(t,o),sg=function(n){return n>0?'+'+n:n<0?'−'+Math.abs(n):'0'};\n"
     "  return '<p style=\"font-weight:800;margin-top:8px\">Reputazione: <span class=\"num\">'+q.tot+'%</span></p><div class=\"pbar\" role=\"progressbar\" aria-label=\"Reputazione\" aria-valuemin=\"0\" aria-valuemax=\"100\" aria-valuenow=\"'+q.tot+'\" style=\"margin:6px 0 8px\"><i style=\"width:'+q.tot+'%\"></i></div>'\n"
     "   +'<p class=\"sm mut\">Partenza 50 · Posizione (ora '+q.pos+'°) '+sg(q.pp)+' · Obiettivi del presidente '+sg(q.pr)+' · Sponsor '+sg(q.sp)+'</p>'}\n"
     "function vCarRiassunto(t,C){"),
    ("""+'<p style="font-weight:800;margin-top:8px">'+(repDB!=null?'Reputazione certificata: <span class="num">+'+repDB+'</span>':'Reputazione della stagione: <span class="num">+'+(bonusPres+bonusSponsor)+'</span>')+'</p>'""",
     """+repBlocco(t,o)"""),
    ("'La reputazione sale di 2 per ogni obiettivo del presidente raggiunto e di 1 per ogni obiettivo di sponsor.','La reputazione resta anche la stagione dopo: chi arriva da una buona annata parte con più credito.'",
     "'La reputazione va da 0 a 100%: si parte da 50.','La posizione in classifica aggiunge o toglie un po\\' di reputazione: +20 al primo posto, poi un po\\' meno a ogni posizione, fino a −20 all\\'ultimo. Durante la stagione conta la posizione di oggi.','Ogni obiettivo del presidente raggiunto vale +10, ogni obiettivo mancato −10, fino alla fine della stagione. Ognuno ha i suoi obiettivi, secondo la fascia e dove lo aspetta il presidente.','Ogni obiettivo di sponsor vale +1 se raggiunto e −1 se mancato, e resta anche nelle stagioni dopo.','Con tutti gli obiettivi del presidente e il primo posto la reputazione arriva al 100%.'"),
    # 5. malus degli sponsor: li registra il workflow dei premi; nella pagina «Mancato», non «Da riscuotere»
    ("/* Sito vero (PREMI52=false): i premi li registra il server;",
     "function malus52(){var m={};D.teams.forEach(function(x){var s=sponsorDi(x),e=esito(x,s.pct,s.stato,s.dl||GTOT,s.ok),c=sponsorCoppa(x),l=[];if(e[1]==='Mancato')l.push({obiettivo:'sponsor',sponsor:s.nome});if(c.stato==='Mancato')l.push({obiettivo:'sponsor_coppa',sponsor:c.nome});m[x]=l});return m}   /* obiettivi di sponsor mancati: −1 di reputazione per sempre, senza crediti */\n"
     "/* Sito vero (PREMI52=false): i premi li registra il server;"),
    ("if(e)return e.stato==='claimed'?{lab:'Riscosso',ok:false,riscosso:true}",
     "if(e)return e.stato==='malus'?{lab:'Mancato',ok:false,riscosso:false}:e.stato==='claimed'?{lab:'Riscosso',ok:false,riscosso:true}"),
]


def applica(t):
    cambiato = False
    for a, b in SOST:
        if b in t:
            continue   # già applicata
        if t.count(a) != 1:
            raise SystemExit(f"atteso una volta, trovato {t.count(a)}: {a[:80]}…")
        t = t.replace(a, b)
        cambiato = True
    return t, cambiato


for f in sys.argv[1:]:
    p = Path(f)
    t, cambiato = applica(p.read_text(encoding="utf-8"))
    if cambiato:
        p.write_text(t, encoding="utf-8")
    print(("aggiornato " if cambiato else "già aggiornato ") + f)
