#!/usr/bin/env python3
"""Albo d'oro (girrr/albo.html e stadio/girrr/albo.html): punti non conservati scritti per esteso.

Uso: python3 rilascio/albo56/punti.py FILE [FILE ...]   (modifica sul posto, rilanciabile)
- Classifica di una stagione senza nessun punto (2022/23): niente colonna di trattini, sotto la
  tabella «Punti finali: dato non conservato.».
- Scheda dell'allenatore, «Il percorso»: «Dato non conservato» al posto del trattino.
(Regola della lega: dove mancano dati storici si scrive «Dato non conservato».)
"""
import sys
from pathlib import Path

SOST = [
    ("""else{body='<table><tr><th>#</th><th style="text-align:left">Squadra</th><th>Punti</th></tr>'
      +e.t.map(function(r,i){return '<tr><td>'+(i+1)+'°</td><td style="text-align:left;font-weight:700">'+esc(r[0])+'<small>'+esc(alS(r[1]))+'</small></td><td>'+(r[2]!=null?r[2]:'–')+'</td></tr>'}).join('')+'</table>'}""",
     """else{var np=e.t.every(function(r){return r[2]==null});   /* Gianluca, 2 novembre: punti non conservati scritti per esteso, non una colonna di trattini */
      body='<table><tr><th>#</th><th style="text-align:left">Squadra</th>'+(np?'':'<th>Punti</th>')+'</tr>'
      +e.t.map(function(r,i){return '<tr><td>'+(i+1)+'°</td><td style="text-align:left;font-weight:700">'+esc(r[0])+'<small>'+esc(alS(r[1]))+'</small></td>'+(np?'':'<td>'+(r[2]!=null?r[2]:'Dato non conservato')+'</td>')+'</tr>'}).join('')+'</table>'+(np?'<div class="nota">Punti finali: dato non conservato.</div>':'')}"""),
    ("""<td>'+(r.pt!=null?r.pt:'–')+'</td></tr>'}).join('')+'</table>';""",
     """<td>'+(r.pt!=null?r.pt:'<small style="display:block;font-weight:600;opacity:.8;line-height:1.2">Dato non conservato</small>')+'</td></tr>'}).join('')+'</table>';"""),
]

for f in sys.argv[1:]:
    p = Path(f)
    t = p.read_text(encoding="utf-8")
    cambiato = False
    for a, b in SOST:
        if b in t:
            continue
        if t.count(a) != 1:
            raise SystemExit(f"{f}: atteso una volta, trovato {t.count(a)}: {a[:70]}…")
        t = t.replace(a, b)
        cambiato = True
    if cambiato:
        p.write_text(t, encoding="utf-8")
    print(("aggiornato " if cambiato else "già aggiornato ") + f)
