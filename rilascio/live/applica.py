#!/usr/bin/env python3
"""Home: il pallino «Live» di Girrr Sport lampeggia solo durante le partite (Claude, 12 novembre 2026). Prototipo per il Lab.

Segnalazione di Gianluca: «volevo che il pallino lampeggiasse quando ci fossero le partite in Live, ma ora non c'è nessuna
partita e il pallino sta lampeggiando ancora». Nella Home (Lega e Stadio) il pallino sopra il logo di Girrr Sport (riquadro
Tabellone, .rec) aveva l'animazione sempre accesa.
Ora lampeggia solo con la classe .diretta, che uno script mette quando una partita di Serie A è in corso: da 1 minuto prima
del calcio d'inizio a 115 minuti dopo, con gli orari di data.json (campi sa e fx, giornate vicine a nx). Si ricontrolla ogni
minuto. Fuori dalle partite il pallino resta acceso ma fermo. Con «riduci movimento» non lampeggia mai (come prima).
Con ?live nell'indirizzo lampeggia sempre (solo per provarlo).

Uso: python3 rilascio/live/applica.py CARTELLA_DEL_SITO
Scrive rilascio/live/pagine/girrr/index.html e rilascio/live/pagine/stadio/girrr/index.html.
"""
import os
import sys

CODICE = r'''<script>
/* Claude, 12 novembre 2026: il pallino «Live» di Girrr Sport lampeggia solo mentre c'è una partita di Serie A (rilascio/live/applica.py) */
(function(){
 var url=(location.pathname.indexOf('/stadio/')>=0?'../../':'../')+'data.json',ORE=[];
 function roma(y,mo,d,h,mi){var g=Date.UTC(y,mo-1,d,h,mi)-36e5;for(var i=0;i<2;i++){var p={};new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Rome',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(new Date(g)).forEach(function(x){p[x.type]=+x.value});
  g+=Date.UTC(y,mo-1,d,h,mi)-Date.UTC(p.year,p.month-1,p.day,p.hour,p.minute)}return g}
 function orari(D){var out=[],ora=new Date(),n=+D.nx||+D.round||0;[n-1,n,n+1].forEach(function(k){[(D.sa||{})[k],(D.fx||{})[k]].forEach(function(L){(L||[]).forEach(function(m){var x=/(\d{1,2})\/(\d{1,2})\s+(\d{1,2}):(\d{2})/.exec(m[2]||'');if(!x)return;
   var mo=+x[2],y=ora.getFullYear();if(mo<ora.getMonth()+1-6)y++;else if(mo>ora.getMonth()+1+6)y--;out.push(roma(y,mo,+x[1],+x[3],+x[4]))})})});return out}
 function guarda(){var t=Date.now(),su=/[?&]live\b/.test(location.search)||ORE.some(function(k){return t>=k-6e4&&t<=k+115*6e4});
  [].forEach.call(document.querySelectorAll('.rec'),function(e){e.classList.toggle('diretta',su)})}
 fetch(url,{cache:'no-store'}).then(function(r){return r.json()}).then(function(D){ORE=orari(D);guarda();setInterval(guarda,6e4)}).catch(function(){guarda()});
})();
</script>'''

SOSTITUZIONI = [
    ("background:var(--dot);animation:recp 2.6s ease-in-out infinite}",
     "background:var(--dot)}.rec.diretta::after{animation:recp 2.6s ease-in-out infinite}"),
]


def applica(t):
    for a, b in SOSTITUZIONI:
        n = t.count(a)
        assert n == 1, 'trovato %d volte: %s' % (n, a[:60])
        t = t.replace(a, b)
    assert t.count('</body>') == 1
    return t.replace('</body>', CODICE + '</body>')


if __name__ == '__main__':
    sito = sys.argv[1]
    qui = os.path.dirname(os.path.abspath(__file__))
    for rel in ('girrr/index.html', 'stadio/girrr/index.html'):
        t = open(os.path.join(sito, rel), encoding='utf-8').read()
        out = os.path.join(qui, 'pagine', rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(applica(t))
        print('scritto', out)
