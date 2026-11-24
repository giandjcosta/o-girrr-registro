#!/usr/bin/env python3
"""Forza della rosa nella pagina Squadre (Lega e Stadio): classifica delle rose dalla fotografia del server.

Regola di Gianluca (24 novembre 2026): «3ª rosa su 10» si aggiorna sul server dopo ogni giornata di Campionato
o dopo uno scambio (calcoli/forza_rose.py → girrr/dati/forza-rose.json); la forza della rosa al completo
(tutti sani, quella della Carriera) resta ferma e si legge sotto, «Al completo: 94 su 100».
Senza fotografia la scheda resta com'è oggi (calcolo nella pagina).

Uso: python3 rilascio/forza-rose/applica.py CARTELLA_GH_PAGES   (idempotente: la seconda volta «File cambiati: 0»)
"""
import sys
from pathlib import Path

PAGINE = {"girrr/squadre.html": "dati/forza-rose.json", "stadio/girrr/squadre.html": "../../girrr/dati/forza-rose.json"}

VECCHIO_CARTA = """  var hf='<div class="card"><h3>Forza della rosa</h3>'+(fi>=0?'<div class="sub" style="margin:0">'+(fi+1)+'ª su '+fs.length+' per fantavoti attesi dei migliori undici</div><div class="bar"><i style="width:'+Math.round(25+75*(fs[fi].f-mn)/Math.max(0.01,mx-mn))+'%"></i></div>':'<div class="vuoto">Dati non disponibili.</div>')+'</div>';"""

NUOVO_CARTA = """  var hf='<div class="card"><h3>Forza della rosa</h3>'+(fi>=0?'<div class="sub" style="margin:0">'+(fi+1)+'ª su '+fs.length+' per fantavoti attesi dei migliori undici</div><div class="bar"><i style="width:'+Math.round(25+75*(fs[fi].f-mn)/Math.max(0.01,mx-mn))+'%"></i></div>':'<div class="vuoto">Dati non disponibili.</div>')+'</div>';
  /* forza-rose: classifica delle rose dalla fotografia del server (dopo ogni giornata o scambio); sotto la forza al completo, ferma */
  var frc=FR&&FR.classifica||[],fr=frc.filter(function(x){return x.squadra===sel})[0];
  if(fr){var fmx=frc[0].valore,fmn=frc[frc.length-1].valore;
    hf='<div class="card"><h3>Forza della rosa</h3><div class="sub" style="margin:0"><b>'+fr.pos+'ª rosa su '+frc.length+'</b> · Dopo la '+FR.giornata+'ª giornata</div>'
      +'<div class="bar"><i style="width:'+Math.round(25+75*(fr.valore-fmn)/Math.max(0.01,fmx-fmn))+'%"></i></div>'
      +(fr.completa?'<div class="sub" style="margin:8px 0 0">Al completo: <b>'+fr.completa+'</b> su 100</div>':'')+'</div>'}"""

VECCHIO_FETCH = "  chips();render();document.getElementById('foot').textContent='Dati aggiornati al '+(D.cal.date||'');"


def nuovo_fetch(percorso):
    return VECCHIO_FETCH + "\n  /* forza-rose */fetch('" + percorso + "',{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(f){if(f&&f.classifica){FR=f;render()}}).catch(function(){});"


def applica(sito):
    cambiati = 0
    for rel, percorso in PAGINE.items():
        f = sito / rel
        s = f.read_text(encoding="utf-8")
        if "/* forza-rose" in s:
            continue
        assert s.count(VECCHIO_CARTA) == 1, rel + ": scheda Forza della rosa non trovata"
        assert s.count(VECCHIO_FETCH) == 1, rel + ": caricamento dei dati non trovato"
        s = s.replace(VECCHIO_CARTA, NUOVO_CARTA).replace(VECCHIO_FETCH, nuovo_fetch(percorso))
        s = s.replace("var MOD=[", "var FR=null;/* forza-rose */\nvar MOD=[", 1)
        f.write_text(s, encoding="utf-8")
        cambiati += 1
    print("File cambiati:", cambiati)


if __name__ == "__main__":
    applica(Path(sys.argv[1]))
