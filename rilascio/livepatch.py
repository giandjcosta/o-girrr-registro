"""Collega le pagine nuove (Laboratorio) ai dati veri e al database.
applica(s, modo, dati_url) -> testo della pagina.
  modo 'prova'  : finto database nel browser (localStorage), strumenti di prova visibili, senza login si entra come Oranje VC
  modo 'reale'  : funzioni vere del database (derby_*, conf_salva), squadra scelta al login (localStorage 'fg')
"""
import pathlib, re
QUI = pathlib.Path(__file__).resolve().parent


def applica(s, modo, dati_url):
    prova = modo == "prova"

    def sost(a, b):
        nonlocal s
        assert a in s, a[:70]
        s = s.replace(a, b, 1)

    # dati di oggi, se il file c'è (altrimenti resta la fotografia incorporata)
    sost("D.img.gs='girrr-sport.png?v=20261016s';",
         "D.img.gs='girrr-sport.png?v=20261016s';(function(){try{var x=new XMLHttpRequest();x.open('GET','" + dati_url + "?'+Date.now(),false);x.send();if(x.status===200){var j=JSON.parse(x.responseText);for(var k in j){var v=j[k];if(v==null||(Array.isArray(v)&&!v.length)||(typeof v==='object'&&!Array.isArray(v)&&!Object.keys(v).length))continue;D[k]=v}}}catch(e){}})();")
    # squadra scelta al login
    sost("var ME='Oranje VC';",
         "var LVQ=new URLSearchParams(location.search),FG={};try{FG=JSON.parse(localStorage.getItem('fg')||'{}')}catch(e){}\n"
         "var ME=(" + ("LVQ.get('come')||" if prova else "") + "FG.team||" + ("'Oranje VC'" if prova else "''") + "),CODE=FG.code||'',GUEST=D.teams.indexOf(ME)<0;if(GUEST)ME='Oranje VC';\n"
         "if(D.rosters&&D.rosters[ME])D.ros=D.rosters[ME];")
    sost("</style>", ".nmin,.cfree{-webkit-appearance:none;appearance:none;width:100%;box-sizing:border-box;min-height:50px;padding:13px 18px;font:inherit;font-size:16px;font-weight:600;color:#fff;background:rgba(255,255,255,.14);-webkit-backdrop-filter:blur(18px) saturate(160%);backdrop-filter:blur(18px) saturate(160%);border:1px solid rgba(255,255,255,.32);border-radius:16px;box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 4px 14px rgba(0,0,0,.2);outline:none;transition:border-color .15s,background .15s}.nmin::placeholder,.cfree::placeholder{color:rgba(255,255,255,.6);font-weight:500}.nmin:focus,.cfree:focus{border-color:#ffd166;background:rgba(255,255,255,.2)}.nmin{flex:1 1 100%!important;min-width:0!important}</style>")
    # niente voti finti: i Derby nascono dai dati veri
    s2 = re.sub(r"S\.vote=S\.vote\|\|\{\};S\.pend=S\.pend\|\|\{\};\[.*?\]\.forEach\(function\(p\)\{var x=p\.split\('\|'\);S\.vote\[rvKey\(x\[0\],x\[1\]\)\]=true\}\);",
                "S.vote=S.vote||{};S.pend=S.pend||{};", s, flags=re.S)
    assert s2 != s, "voti finti"
    s = s2
    # Derby: ufficiale se votato dai più o nato da una sfida accettata; veto dei più lo spegne; altrimenti conta la rivalità storica
    sost("der=any?inten>=50:o.r>=50,", "der=S.veto&&S.veto[k]?false:(S.vote[k]?true:o.r>=50),")
    # frasi della sfida dal punto di vista di chi sfida
    sost("SFPAIR[rvKey(ME,'Apo team')]=", "SFPAIR[rvKey('Oranje VC','Apo team')]=")
    sost("function sfF(t){var p=SFPAIR[rvKey(ME,t)];", "function sfF(t,fr){fr=fr||ME;var p=fr==='Oranje VC'?SFPAIR[rvKey(fr,t)]:null;")
    # fiducia: se c'è il calcolo completo (con le promesse) vale quello
    sost("function fid(t){var r=row(t);", "function fid(t){if(D.fid&&D.fid[t]!=null)return Math.round(D.fid[t]);var r=row(t);")
    # voto sul Derby: dal database
    sost("""'<button class="tag '+(S.vote[rvKey(o.a,o.b)]?'o':'')+'" data-vote="'+esc(rvKey(o.a,o.b))+'" aria-pressed="'+(!!S.vote[rvKey(o.a,o.b)])+'" style="margin-top:8px">Lo sento come Derby</button>""",
         """(GUEST?'<p class="sm mut" style="margin-top:8px">Entra con il tuo codice squadra per dire se lo senti come Derby.</p>':'<button class="tag '+(S.mine[rvKey(o.a,o.b)]?'o':'')+'" data-lvote="'+esc(rvKey(o.a,o.b))+'" aria-pressed="'+(!!S.mine[rvKey(o.a,o.b)])+'" style="margin-top:8px">Lo sento come Derby</button>')+'""")
    sost("I primi voti sono quelli degli amici, gli altri sono di prova.", "I voti sono quelli degli amici della lega.")
    # conferenza: pubblicazione e dopo-partita dal database
    sost("if(b.id==='cpub'&&!b.disabled){S.cf.pub=true;render();var c=$('.post');if(c&&c.scrollIntoView)c.scrollIntoView({block:'center',behavior:'smooth'});return}",
         "if(b.id==='cpub'&&!b.disabled){lvConfPubblica();return}")
    m = re.search(r"    var pw=ch\.filter\(function\(c\)\{return c\.w\}\)\.length;\n    h\+='<div class=\"card\"><h3>Dopo la partita.*?\n    h\+='</div>'\}\n", s, flags=re.S)
    assert m, "dopo la partita"
    s = s.replace(m.group(0), "    h+=lvDopo(t,ch,ch.filter(function(c){return c.w}).length)}\n", 1)
    # radio: la sfida e l'esito vengono dal database
    sost("if(S.cf.pub&&S.cf.esito&&ch.every(function(c){return c})){var prom=ch.filter(function(c){return c.w})[0],win=S.cf.esito==='v';",
         "if(S.cf.pub&&S.cf.esito&&ch.every(function(c){return c})){var prom=ch.filter(function(c){return c.w})[0],win=S.cf.esito==='v';")
    # pagine personali: senza login un invito a entrare
    for f in ("vConf", "vBors", "vCar"):
        sost("function %s(){" % f, "function %sL(){" % f)
    live = (QUI / "live.js").read_text(encoding="utf-8").replace("@@MODE@@", modo)
    gate = ("function lvGate(t){return '<div class=\"card\"><h3>Entra con la tua squadra</h3><p class=\"sm\">'+t+' è personale: serve il codice della tua squadra. Entra dalla pagina principale del sito e torna qui.</p></div>'}\n"
            "function vConf(){return GUEST?lvGate('La conferenza stampa'):vConfL()}function vBors(){return GUEST?lvGate('Il Borsino della tua squadra'):vBorsL()}function vCar(){return GUEST?lvGate('La Carriera'):vCarL()}\n")
    live = live.replace("/* ---------- Sfide ---------- */", gate + "/* ---------- Sfide ---------- */", 1)
    # esito della conferenza e ultima sfida per la radio
    live = live.replace("  var G=D.cal[0]&&D.cal[0].n,row=DBS.conf.filter(function(c){return c.giornata===G})[0];\n  if(row&&!S.cfok",
        "  var lastS=DBS.sfide.filter(function(x){return x.da===ME})[0];S.lancio.ok=null;S.lancio.stato=null;\n  if(lastS&&(lastS.stato==='rifiutata'||lastS.stato==='scaduta'||(lastS.stato==='accettata'&&lastS.nome_ok))){S.lancio.ok={r:lastS.a,f:lastS.frase};S.lancio.stato=lastS.stato}\n  var G=D.cal[0]&&D.cal[0].n,row=DBS.conf.filter(function(c){return c.giornata===G})[0];S.cf.esito=row&&row.esito?(row.esito==='v'?'v':'p'):null;\n  if(row&&!S.cfok", 1)
    live = live.replace("var fid0=fid;function fid(t){return (D.fid&&D.fid[t]!=null)?Math.round(D.fid[t]):fid0(t)}\n", "")
    sost("var hh=(location.hash||'').slice(1);if(hh==='conf'", live + "\nvar hh=(location.hash||'').slice(1);if(hh==='conf'")
    return s
