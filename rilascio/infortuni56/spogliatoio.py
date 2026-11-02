#!/usr/bin/env python3
"""Spogliatoio: infortuni e squalifiche contati bene in «Chi scambiare» e «Mercato Scambi».

Uso:
  python3 rilascio/infortuni56/spogliatoio.py SORGENTE DESTINAZIONE [--lab]

SORGENTE è lo Spogliatoio del sito (index.html della radice di gh-pages, copia in
ufficiale/src/sito/spogliatoio-index.html). Con --lab scrive la prova del Laboratorio:
stessa pagina, ma legge i dati dal sito vero e applica alle giornate 6-10 lo storico
degli indisponibili (ind_storico.json), come farà lo script aggiornato.

Cosa cambia:
- Chi scambiare: le giornate saltate per infortunio o squalifica (I) non contano più
  come «non giocata»; l'infortunio di oggi pesa secondo i giorni che mancano al rientro
  (fino a 14 giorni niente, da 60 giorni o fine stagione +30), la squalifica non pesa.
- Mercato Scambi: la quota di partite giocate si calcola sulle partite in cui il
  giocatore era disponibile, non su tutte quelle della sua squadra.
"""
import json
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent

SOST = [
    # Chi scambiare: niente peso alle giornate da indisponibile, nel calcolo e nel grafico
    ("D.rounds.filter(function(r){return log[r]}).sort(function(a,b){return b-a}).slice(0,6).forEach(function(r){var c=w[log[r]]||0;if(keep&&c>0)c=0;s+=c*k;k*=d});\n  if(coverOf(id))return Math.min(base(id),20);\n  var n=nxt(id).s,bump={I:keep?0:10,",
     "D.rounds.filter(function(r){return log[r]&&log[r]!=='I'}).sort(function(a,b){return b-a}).slice(0,6).forEach(function(r){var c=w[log[r]]||0;if(keep&&c>0)c=0;s+=c*k;k*=d});\n  if(coverOf(id))return Math.min(base(id),20);\n  var n=nxt(id).s,bump={I:keep?0:injBump(id),", 1),
    ("D.rounds.filter(function(r){return log[r]&&r<=upto})",
     "D.rounds.filter(function(r){return log[r]&&log[r]!=='I'&&r<=upto})", 1),
    # peso dell'infortunio di oggi secondo il rientro previsto
    ("function probAt(id,upto){",
     "function injBump(id){var e=injOf(id),st=nxt(id);if(/squalific/i.test((e&&e.w)||st.n||''))return 0;if(!e)return 10;var dd=/stagione/i.test((e.b||'')+' '+(e.w||''))?200:injDays(e);return dd<=14?0:dd>=60?30:Math.round((dd-14)/46*30)}\n"
     "function nI(id){var l=(D.log||{})[id]||{},k,c=0;for(k in l)if(l[k]==='I')c++;return c}\n"
     "function probAt(id,upto){", 1),
    # Mercato Scambi: partite disponibili, non tutte quelle della squadra
    ("tg=(D.sf&&D.sf[p.t]?D.sf[p.t][0]:0);",
     "tg=Math.max(0,(D.sf&&D.sf[p.t]?D.sf[p.t][0]:0)-nI(id));", 1),
    # testi
    ("la percentuale sale quando resta in panchina o è indisponibile e scende quando gioca titolare.",
     "la percentuale sale quando resta in panchina e scende quando gioca titolare. Le giornate saltate per infortunio o squalifica non contano; un infortunio lungo la fa salire.", 1),
    ("Poi sale di '+D.w.P+' punti per ogni partita non giocata e di '+D.w.I+' per ogni assenza per infortunio o squalifica, mentre scende di '+Math.abs(D.w.T)+' a ogni partita da titolare. Le giornate più recenti pesano di più.",
     "Poi sale di '+D.w.P+' punti per ogni partita passata in panchina e scende di '+Math.abs(D.w.T)+' a ogni partita da titolare. Le giornate più recenti pesano di più. Le giornate saltate per infortunio o squalifica (I) non contano. Se oggi è infortunato sale secondo il rientro previsto: niente fino a 14 giorni, poi sempre di più, fino a 30 punti da 60 giorni in su o se la stagione è finita. La squalifica non la fa salire.", 1),
]


def applica(t):
    for vecchio, nuovo, n in SOST:
        c = t.count(vecchio)
        if c != n:
            raise SystemExit(f"atteso {n} volte, trovato {c}: {vecchio[:70]}…")
        t = t.replace(vecchio, nuovo)
    return t


def lab(t):
    storico = json.loads((QUI / "ind_storico.json").read_text(encoding="utf-8"))
    ind = {g: sorted(v["I"]) for g, v in storico["giornate"].items()}
    t = t.replace("<head>", '<head>\n<base href="https://giandjcosta.github.io/o-fant-a-girrr/">\n<meta name="robots" content="noindex">', 1)
    # come farà lo script: nelle giornate con lo storico, «P» diventa «I» per chi era indisponibile
    hook = ("function labInd(X){var I=" + json.dumps(ind, separators=(",", ":")) +
            ",g,i,l;for(g in I)I[g].forEach(function(i){l=(X.log||{})[i];if(l&&l[g]==='P')l[g]='I'});return X}\n")
    vecchio = "fetch('data.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){if(j&&j.teams&&j.P&&(j.updated>=D.updated)){D=j;"
    if t.count(vecchio) != 1:
        raise SystemExit("aggancio dei dati non trovato")
    t = t.replace(vecchio, hook + vecchio.replace("{D=j;", "{D=labInd(j);"))
    t = t.replace("<body>", '<body>\n<div style="background:#ffd166;color:#141d3d;font:700 13px/1.4 system-ui,sans-serif;padding:8px 14px;text-align:center">Prova del Laboratorio: infortuni e squalifiche in «Chi scambiare» e «Mercato Scambi». Dati veri del sito.</div>', 1)
    return t


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    t = applica(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if "--lab" in sys.argv:
        t = lab(t)
    Path(sys.argv[2]).write_text(t, encoding="utf-8")
    print("scritto", sys.argv[2])


if __name__ == "__main__":
    main()
