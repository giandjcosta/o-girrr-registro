"""Totogirrr: scheda Movimenti, tra Prestiti e Regole.
Mette in una sola lista, dalla più recente, le entrate e le uscite della squadra: puntate e vincite delle schedine
(da toto_stato) e i movimenti del database (da toto_pr_stato: trattenute del banco, prestiti, rimborsi, rimborso Derby,
premio sponsor). Solo lettura: non cambia niente nel database. Il riquadro Movimenti dentro Prestiti resta com'è.

Uso:
  python3 rilascio/toto_movimenti.py SORGENTE DESTINAZIONE            # patch per il sito vero
  python3 rilascio/toto_movimenti.py SORGENTE DESTINAZIONE --lab URL  # copia di prova nel Lab: <base> verso URL, niente statistiche visite
Esempio Lab: python3 rilascio/toto_movimenti.py totogirrr.html lab/prova-totogirrr-lega.html --lab https://giandjcosta.github.io/o-fant-a-girrr/girrr/
"""
import sys, pathlib


VMOV = r"""var NOMIMOV={banco:'Trattenuta del banco',cashback_derby:'Rimborso Derby',premio_sponsor:'Premio sponsor',prestito:'Prestito',restituzione:'Restituzione prestito',sussidio:'Prestito del banco'};
function vMovimenti(){
  if(!PR){if(!PRL)loadPR();return '<div class="card">Carico i movimenti…</div>'}
  var m=[],en=0,us=0;
  (PR.movimenti||[]).forEach(function(x){var t=String(x.tipo||'');m.push({n:String(x.nota||'').replace(/ · [a-z]+_[a-z0-9_]+$/,'')||NOMIMOV[t]||(t.charAt(0).toUpperCase()+t.slice(1)).replace(/_/g,' '),i:Number(x.importo)||0,d:x.creato})});
  (S.schedine||[]).forEach(function(x){m.push({n:'Schedina n° '+x.id+' · Puntata',i:-Number(x.puntata),d:x.creata});if(x.stato==='vinta'&&Number(x.vincita)>0)m.push({n:'Schedina n° '+x.id+' · Vincita',i:Number(x.vincita),d:x.creata})});
  m.forEach(function(x,k){x.k=k;if(x.i>=0)en+=x.i;else us-=x.i});
  m.sort(function(a,b){return (new Date(b.d||0)-new Date(a.d||0))||(b.k-a.k)});
  var h='<div class="card"><b>Movimenti</b><p style="font-size:12px;color:var(--sub);margin:6px 0">Tutte le entrate e le uscite della tua squadra, dalla più recente: schedine, vincite, prestiti, rimborsi, trattenute del banco e premi sponsor.</p>';
  if(m.length)h+='<div class="mv"><span>Entrate</span><b class="p">+'+f2(en)+'</b></div><div class="mv"><span>Uscite</span><b class="m">−'+f2(us)+'</b></div>';
  h+='</div><div class="card">'+(m.length?m.map(function(x){return '<div class="mv"><span>'+esc(x.n)+'<small style="display:block;color:var(--sub);font-size:11px">'+quando(x.d)+'</small></span><b class="'+(x.i>=0?'p':'m')+'">'+(x.i>=0?'+':'−')+f2(Math.abs(x.i))+'</b></div>'}).join(''):'<div class="vuoto">Ancora nessun movimento.</div>')+'</div>';
  if(PR.err)h+='<p style="font-size:12px;color:var(--sub);margin:6px 2px">Prestiti e premi non si sono caricati: qui vedi solo le schedine.</p>';
  return h;
}
function vPrestiti(){"""


def applica(s, lab_base=None):
    def sost(a, b):
        nonlocal s
        assert s.count(a) == 1, a[:70]
        s = s.replace(a, b)

    sost("['prestiti','Prestiti'],['regole','Regole']", "['prestiti','Prestiti'],['movimenti','Movimenti'],['regole','Regole']")
    sost("tab==='prestiti'?vPrestiti():", "tab==='prestiti'?vPrestiti():tab==='movimenti'?vMovimenti():")
    sost("if(tab==='prestiti')loadPR();", "if(tab==='prestiti'||tab==='movimenti')loadPR();")
    sost("var _qi=/[?&]t=(prob|sfide)/", "var _qi=/[?&]t=(prob|sfide|movimenti)/")
    sost("function vPrestiti(){", VMOV)
    if lab_base:
        sost('<head>\n', '<head>\n<base href="' + lab_base + '">\n')
        sost('<script>window.goatcounter={path:function(){return location.pathname},no_onload:/[?&]demo/.test(location.search)}</script>\n', '')
        sost('<script data-goatcounter="https://djcosta18.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n', '')
    return s


if __name__ == "__main__":
    a = sys.argv[1:]
    src, dst = a[0], a[1]
    lab = a[a.index("--lab") + 1] if "--lab" in a else None
    pathlib.Path(dst).write_text(applica(pathlib.Path(src).read_text(encoding="utf-8"), lab), encoding="utf-8")
