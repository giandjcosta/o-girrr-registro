"""Tabellone con più dati: V, N, P, gol fatti, gol subiti e differenza reti accanto a G, Pt e Fantapunti.
Sul telefono (sotto 560 px) restano Pt, DR e Fantapunti; G, V, N, P, GF e GS compaiono da 560 px in su.
L'ordine della classifica non cambia (Pt, poi Fantapunti).

Uso:
  python3 rilascio/tabellone_dati.py SORGENTE DESTINAZIONE            # patch per il sito vero
  python3 rilascio/tabellone_dati.py SORGENTE DESTINAZIONE --lab URL  # copia di prova nel Lab: <base> verso URL, niente statistiche visite
Esempio Lab: python3 rilascio/tabellone_dati.py tabellone.html lab/prova-tabellone-lega.html --lab https://giandjcosta.github.io/o-fant-a-girrr/girrr/
"""
import sys, pathlib


def applica(s, lab_base=None):
    def sost(a, b):
        nonlocal s
        assert s.count(a) == 1, a[:70]
        s = s.replace(a, b)

    sost("sq[n]={n:n,g:0,pt:0,fp:0,gf:0,gs:0,gir:''}", "sq[n]={n:n,g:0,pt:0,fp:0,gf:0,gs:0,v:0,nn:0,p:0,gir:''}")
    sost("x[0].pt+=x[1]>x[2]?3:(x[1]===x[2]?1:0)",
         "if(x[1]>x[2]){x[0].pt+=3;x[0].v++}else if(x[1]===x[2]){x[0].pt++;x[0].nn++}else x[0].p++")
    sost("""(fp?'<tr><th></th><th>Squadra</th><th>G</th><th>Pt</th><th>Fantapunti</th></tr>':'<tr><th></th><th>Squadra</th><th>G</th><th>Pt</th></tr>')""",
         """'<tr><th></th><th>Squadra</th><th class="w">G</th><th class="w">V</th><th class="w">N</th><th class="w">P</th><th class="w">GF</th><th class="w">GS</th><th>DR</th><th>Pt</th>'+(fp?'<th>Fantapunti</th>':'')+'</tr>'""")
    sost("""<td>'+x.g+'</td><td class="pt">'+x.pt+'</td>'""",
         """<td class="w">'+x.g+'</td><td class="w">'+x.v+'</td><td class="w">'+x.nn+'</td><td class="w">'+x.p+'</td><td class="w">'+x.gf+'</td><td class="w">'+x.gs+'</td><td class="dr">'+(x.gf-x.gs>0?'+':x.gf-x.gs<0?'−':'')+Math.abs(x.gf-x.gs)+'</td><td class="pt">'+x.pt+'</td>'""")
    sost("td.fp{", "th.w,td.w{display:none}@media (min-width:560px){th.w,td.w{display:table-cell}}td.dr{font-size:.9em;font-weight:800}td.fp{")
    if lab_base:
        sost('<head>\n', '<head>\n<base href="' + lab_base + '">\n')   # prima di ospite.js, che è il primo script
        sost('<script>window.goatcounter={path:function(){return location.pathname},no_onload:/[?&]demo/.test(location.search)}</script>\n', '')
        sost('<script data-goatcounter="https://djcosta18.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n', '')
    return s


if __name__ == "__main__":
    a = sys.argv[1:]
    lab = a[a.index("--lab") + 1] if "--lab" in a else None
    src, dst = a[0], a[1]
    pathlib.Path(dst).write_text(applica(pathlib.Path(src).read_text(encoding="utf-8"), lab), encoding="utf-8")
    print("scritto", dst)
