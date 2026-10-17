"""Anteprima del sito ufficiale con le novità della 5.0.
Copia le pagine vere di O Girrr (repo o-fant-a-girrr, ramo gh-pages) con il loro stile e il loro font, punta dati e immagini al sito vero
e aggiunge: sezioni nuove nell'Albo d'oro, pagina Derby, riquadro in Home, post nuovi nella Curva.
Non scrive niente nel database e non tocca il sito vero. Si lancia con: python3 ufficiale/build.py (dalla cartella del repo)."""
import pathlib, re, json, subprocess, shutil, sys
R = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path("/home/claude/o-fant-a-girrr/girrr")
OUT = R / "ufficiale" / "girrr"
LIVE = "https://giandjcosta.github.io/o-fant-a-girrr/"
lab = (R / "lab" / "index.html").read_text(encoding="utf-8")

# 1) dati dal Laboratorio, valutati con node
def estrai(nome, fine):
    i = lab.index("var " + nome + "=") + len("var " + nome + "=")
    j = lab.index(fine, i)
    return lab[i:j]
js = "var RIV=%s;\nvar PRE=%s;\nvar LEG=%s;\nvar STAG=%s;\nconsole.log(JSON.stringify({riv:RIV,pre:PRE,leg:LEG,stag:STAG}));" % (estrai("RIV", ";\nS.vote="), estrai("PRE", ";\nvar LEG"), estrai("LEG", ";\nvar OROSEZ"), estrai("STAG", ";\nS.oro="))
(R / "ufficiale" / "_x.js").write_text(js, encoding="utf-8")
dati = json.loads(subprocess.check_output(["node", str(R / "ufficiale" / "_x.js")]))
(R / "ufficiale" / "_x.js").unlink()
vt = re.search(r"S\.vote=S\.vote\|\|\{\};S\.pend=S\.pend\|\|\{\};\[(.*?)\]\.forEach", lab, re.S).group(1)
dati.update(json.loads((R / "ufficiale" / "src" / "storie.json").read_text(encoding="utf-8")))
dati["rilascio"] = "2026-10-17"   # data in cui la 5.0 va in linea: il bollino Novità dura 15 giorni da qui
dati["voti"] = re.findall(r"'([^']+\|[^']+)'", vt)

# 2) copia delle pagine vere con i percorsi verso il sito vero
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for f in SRC.iterdir():
    if f.suffix not in (".html", ".js"): continue
    t = f.read_text(encoding="utf-8")
    t = re.sub(r"([\"'])\.\./", lambda m: m.group(1) + LIVE, t)
    t = "\n".join(l for l in t.split("\n") if "goatcounter" not in l)   # niente conteggi sulle aperture di prova
    (OUT / f.name).write_text(t, encoding="utf-8")

def patch(nome, a, b, n=1):
    p = OUT / nome; t = p.read_text(encoding="utf-8")
    assert a in t, (nome, a[:70])
    p.write_text(t.replace(a, b, n), encoding="utf-8")


# Carosello squadre: gira all'infinito e il chip scelto si centra sempre (anche da telefono, tablet e PC)
sq = (OUT / "squadre.html").read_text(encoding="utf-8")
a0 = sq.index("function centra(liscio){"); a1 = sq.index("fetch('" + LIVE + "data.json'", a0)
sq = sq[:a0] + """function centra(liscio){
  var ch=document.getElementById('chips'),n=D.teams.length,i=D.teams.map(function(t){return t.name}).indexOf(sel),base=ch.children[0].offsetLeft,best=null,bd=1e9;
  for(var k=0;k<3;k++){var b=ch.children[k*n+i];if(!b)continue;var x=b.offsetLeft-base-(ch.clientWidth-b.offsetWidth)/2,d=Math.abs(x-ch.scrollLeft);if(d<bd){bd=d;best=x}}
  if(best===null)return;
  if(liscio)ch.scrollTo({left:best,behavior:'smooth'});else ch.scrollLeft=best;
}
""" + sq[a1:]
old = "sel=b.dataset.t;try{history.replaceState(null,'','#'+encodeURIComponent(sel))}catch(x){}render()});"
assert old in sq
sq = sq.replace(old, "sel=b.dataset.t;try{history.replaceState(null,'','#'+encodeURIComponent(sel))}catch(x){}render();centra(true)});", 1)
old2 = "tmr=setTimeout(function(){"
assert old2 in sq
sq = sq.replace("ch.scrollLeft+=W;else if(ch.scrollLeft>W*1.5)ch.scrollLeft-=W},90)", "ch.scrollLeft+=W;else if(ch.scrollLeft>W*1.5)ch.scrollLeft-=W},120)", 1)
(OUT / "squadre.html").write_text(sq, encoding="utf-8")

# 3) Home: riquadro I derby
# 4) Albo: sezioni nuove
patch("albo.html", "</head>", '<script src="novita.js"></script>\n</head>')
patch("albo.html", "document.getElementById('al').innerHTML=stato()+allenatori()+storico()+recs();", "document.getElementById('al').innerHTML=window.ALBOTABS?ALBOTABS(D,{stato:stato(),allenatori:allenatori(),storico:storico(),recs:recs()}):stato()+allenatori()+storico()+recs();")
patch("albo.html", "function titoli(name){return STORICO.filter(function(e){return can(e.v[1])===name}).length}", "function titoli(name){return STORICO.filter(function(e){return can(e.v[1])===name}).length+(window.NOV&&NOV.pre?NOV.pre.filter(function(x){return x[2]===name}).length:0)}")
patch("albo.html", "var exl=Object.keys(ex).sort(", "if(window.NOV&&NOV.pre)NOV.pre.forEach(function(x){if(x[2]&&!CFG[can(x[2])])ex[can(x[2])]=1});var exl=Object.keys(ex).sort(")
patch("albo.html", "<b>'+f[2]+' - '+f[6]+'</b><small>'+pt(f[3])+' - '+pt(f[7])+'</small>", "<b>'+f[2]+' - '+f[6]+'</b>")
patch("albo.html", "Le stagioni passate", "L\\'Era Contemporanea · Le stagioni")
# 5) Curva: post nuovi dentro il feed
patch("curva.html", "</head>", '<script src="novita-curva.js"></script>\n</head>')
patch("curva.html", "function costruisci(){", "function costruisci(){if(window.ANT_POSTS)S.adm=(S.adm||[]).filter(function(u){return !u.ant}).concat(window.ANT_POSTS());")
patch("curva.html", "T(S1,230,230,'800 36px '+F,'#fff','center',330);T(S2,W-230,230,'800 36px '+F,'#fff','center',330);T(n(0,3)+' - '+n(1,3),W/2,260,'900 120px '+F,'#ffd166','center');", "T(S1,165,215,'800 34px '+F,'#fff','center',255);T(S2,W-165,215,'800 34px '+F,'#fff','center',255);T(n(0,3)+' - '+n(1,3),W/2,262,'900 92px '+F,'#ffd166','center');")
# 6) Pagina Derby: stessa grafica dell'Albo
alb = (OUT / "albo.html").read_text(encoding="utf-8")
a0 = alb.index("<script>\n(function(){\nvar D=null;"); a1 = alb.index("</script>\n<script src=\"" + LIVE + "assets/app.js\">")
der = alb[:a0] + '<script src="derby.js"></script>\n' + alb[a1 + len("</script>\n"):]
der = der.replace("<h1>Albo d'oro</h1>", "<h1>I Derby</h1>").replace("<title>Albo d'oro", "<title>I derby").replace('<div class="vuoto">Carico i record…</div>', '<div class="vuoto">Carico i Derby…</div>')
der = der.replace("<script src=\"novita.js\"></script>\n", "")
(OUT / "derby.html").write_text(der.replace('<script src="derby.js">', '<script>window.PAGINA="derby"</script>\n<script src="derby.js">', 1), encoding="utf-8")
_riv = der.replace("<h1>I Derby</h1>", "<h1>Le rivalità</h1>").replace("<title>I derby", "<title>Le rivalità").replace("Carico i Derby…", "Carico le rivalità…").replace('<script src="derby.js">', '<script>window.PAGINA="rivalita"</script>\n<script src="derby.js">', 1)
(OUT / "rivalita.html").write_text(_riv, encoding="utf-8")


_s = (OUT / "storia.js").read_text(encoding="utf-8")
for _a, _b in [("ser è l\\'unico che in cinque stagioni non ha mai cambiato né squadra né nome: la WOA", "ser è l\\'unico che dal 2021 non ha mai cambiato né squadra né nome: la WOA"),
    ("apo è l\\'unico ad aver vinto due titoli, e di fila: 2021/22 e 2022/23 con il Wakanda", "apo ha tre titoli, più di chiunque altro: il 2017/18 e poi 2021/22 e 2022/23 di fila con il Wakanda"),
    ("in cinque stagioni di campionato nessuno si è confermato campione tranne apo", "nella storia della lega solo apo si è confermato campione: 2021/22 e 2022/23"),
    ("'Il Wakanda di apo ha vinto", "'Mario ha vinto il primo campionato della storia della lega, nel 2016/17, con Mertens',\n 'Urba ha vinto il titolo 2018/19 e ha lasciato la lega da campione',\n 'Il Wakanda di apo ha vinto")]:
    assert _a in _s, _a[:40]
    _s = _s.replace(_a, _b)
(OUT / "storia.js").write_text(_s, encoding="utf-8")
# 7) dati e script nuovi
(OUT / "novita-dati.js").write_text("window.NOV=" + json.dumps(dati, ensure_ascii=False) + ";", encoding="utf-8")
for n in ["novita.js", "derby.js", "novita-curva.js", "novita-badge.js", "transizioni.js", "barra.js"]:
    sorg = (R / "ufficiale" / "src" / n).read_text(encoding="utf-8")
    sorg = sorg.replace("'../data.json'", "'" + LIVE + "data.json'")
    (OUT / n).write_text(sorg, encoding="utf-8")
for f in ["index.html", "albo.html", "derby.html", "rivalita.html", "curva.html", "squadre.html"]:
    p = OUT / f; t = p.read_text(encoding="utf-8")
    p.write_text(t.replace("</head>", '<script src="novita-dati.js"></script>\n</head>', 1), encoding="utf-8")
for p in OUT.glob("*.html"):
    _t = p.read_text(encoding="utf-8")
    for _a, _b in [("· i dati arrivano", "· I dati arrivano"), ("' · ex'", "' · Ex'"), ("· giornata '+g.sa", "· Giornata '+g.sa"), ("· si completa", "· Si completa"), ("· quota <b>", "· Quota <b>"), ("· risultati in arrivo", "· Risultati in arrivo"), ("' · con foto'", "' · Con foto'")]:
        _t = _t.replace(_a, _b)
    p.write_text(_t, encoding="utf-8")
for p in OUT.glob("*.html"):
    _t = p.read_text(encoding="utf-8")
    if "transizioni.js" not in _t:
        p.write_text(_t.replace("</head>", '<script src="transizioni.js"></script>\n<script src="barra.js"></script>\n</head>', 1), encoding="utf-8")
(R / "ufficiale" / "index.html").write_text((R / "ufficiale" / "src" / "confronto.html").read_text(encoding="utf-8"), encoding="utf-8")
print("scritto", OUT, len(list(OUT.iterdir())), "file")

for f in ["index.html", "albo.html", "derby.html"]:
    patch(f, '<script src="novita-dati.js"></script>', '<script src="novita-dati.js"></script>\n<script src="novita-badge.js"></script>')
# 8) Home: riquadri per le novità che vivono nel Laboratorio (stesse funzioni, aprono l'anteprima con la grafica giusta)
NUOVE = [("sfide","🥊","Sfide","Dentro Girrr Sport: lanci una sfida"),("borsino","📈","Borsino","Dentro lo Spogliatoio: chi sale e chi scende"),("prob","🎯","Probabilità","Dentro Totogirrr: quanto è probabile il titolo")]
def tiles(href):
    return "".join('<a class="mn" href="%s#%s"><div class="mi">%s</div><div><b>%s</b><span>%s</span></div></a>' % (href, k, e, n, d) for k, e, n, d in NUOVE)
shutil.copy(R / "lab" / "girrr-sport.png", OUT / "girrr-sport.png")
from PIL import Image as _I
_a = _I.open(R / "lab" / "immagini" / "albo-alloro-foto.png"); _a.thumbnail((360, 360)); _a.save(OUT / "albo-alloro.png")
_m = _I.open(R / "lab" / "immagini" / "carriera-lavagna-lega.png"); _m.thumbnail((700, 700)); _m.save(OUT / "carriera-microfoni.png")
ix = (OUT / "index.html").read_text(encoding="utf-8")
assert '<a class="mn" id="mst"' in ix
# La card Giornale diventa Girrr Sport (logo della TV), come nel Laboratorio; il Live resta solo al Tabellone
m = re.search(r'<a class="c" href="giornale.html">.*?</a>', ix, re.S)
assert m
card = '<a class="c" href="../../anteprima/attuale.html#sport"><div class="ic"><img src="girrr-sport.png" alt="Girrr Sport" style="height:54px;width:auto;border-radius:8px"></div><h2>Girrr Sport<span class="nt-nv">NOVITÀ</span></h2><p>La TV, il giornale e la radio della lega: tutto quello che si legge, si ascolta e si guarda.</p><div class="go">ENTRA ›</div></a>'
ix = ix.replace(m.group(0), card, 1).replace('<a href="giornale.html">Leggi il giornale ›</a>', '<a href="giornale.html">Leggi il giornale ›</a>', 1)
LOGO = LIVE + "assets/logo-lega.png"
import time as _t
extra_cards = ('<a class="c" href="albo.html"><div class="ic"><img src="albo-alloro.png?v=@@V@@" alt="" style="height:72px;width:auto;margin-top:-6px"></div><h2>Albo d\'oro<span class="nt-nv">NOVITÀ</span></h2><p>Storia della Lega, Era dei Titani, stagioni, Derby e record.</p><div class="go">ENTRA ›</div></a>'
               '<a class="c" href="../../anteprima/attuale.html#carriera"><div class="ic"><img src="carriera-microfoni.png?v=@@V@@" alt="" style="height:72px;width:auto;margin-top:-6px"></div><h2>Carriera<span class="nt-nv">NOVITÀ</span></h2><p>Obiettivi, fiducia del presidente e conferenza stampa di ogni allenatore.</p><div class="go">ENTRA ›</div></a>')
extra_cards = extra_cards.replace('@@V@@', str(int(_t.time())))
i0 = ix.index('<section class="cards">'); i1 = ix.index('</section>', i0)
ix = ix[:i1] + extra_cards + ix[i1:]
ix = re.sub(r'<section class="mini">.*?</section>\s*<script>try\{var f=JSON.parse\(localStorage.getItem\("fg"\).*?</script>', '', ix, count=1, flags=re.S)
assert 'class="mini"' not in ix
_stat = '<section class="mini" style="margin-top:14px"><a class="mn" id="mst" href="statistiche.html"><div class="mi">📊</div><div><b>Statistiche</b><span>Solo per te: chi entra e dove</span></div></a></section>\n  '
ix = ix.replace('<div class="sp">', _stat + '<div class="sp">', 1)
assert 'id="mst"' in ix
ix = ix.replace("</head>", "<style>.cards{grid-template-columns:repeat(3,1fr)!important}@media(max-width:820px){.cards{grid-template-columns:1fr 1fr!important}}@media(max-width:480px){.cards{grid-template-columns:1fr!important}}</style>\n</head>", 1)
(OUT / "index.html").write_text(ix, encoding="utf-8")
# Tabellone: Le squadre diventano una sezione del Tabellone
patch("tabellone.html", '<div class="sw" role="tablist">', '<a class="sqb" href="squadre.html"><span>🛡️</span><b>Le squadre</b><i>Rosa, risultati e forma di ognuno ›</i></a>\n  <div class="sw" role="tablist">')
patch("tabellone.html", "</head>", "<style>.sqb{display:flex;align-items:center;gap:10px;margin:14px 0 0;max-width:440px;padding:11px 16px;border-radius:16px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.16);color:inherit;text-decoration:none}.sqb span{font-size:20px}.sqb b{font-weight:800}.sqb i{font-style:normal;font-size:12px;opacity:.75;margin-left:auto}</style>\n</head>")
_v = str(int(_t.time()))
for _f in OUT.glob("*.html"):
    _x = _f.read_text(encoding="utf-8")
    _x = re.sub(r'src="((?:novita|derby)[\w-]*\.js)"', lambda m: 'src="%s?v=%s"' % (m.group(1), _v), _x)
    _f.write_text(_x, encoding="utf-8")
SKIN = """.mn b,.tt,.tt>span{font-family:Lobster,'Brush Script MT',cursive!important;font-weight:400!important;letter-spacing:0!important}.mn b{font-size:21px!important;line-height:1.15}.tt{font-size:25px!important}.tt small{font-family:Inter,system-ui,sans-serif!important;font-size:12px!important}.at button[aria-selected=true]{background:#ffd166!important;color:#1d2a52!important}.tabs button[aria-selected=true]{background:#ffd166!important;color:#1d2a52!important;border-color:transparent!important}.seg button[aria-pressed=true]{background:#ffd166!important;color:#1d2a52!important}header.hero,header.top,.ohead{position:relative;padding-bottom:24px!important;margin-bottom:20px!important}header.hero::after,header.top::after,.ohead::after{content:'';position:absolute;left:0;right:0;bottom:0;height:10px;border-radius:2px;transform:skewX(-45deg);background:linear-gradient(90deg,#d62839 0 10%,#ffd166 10% calc(10% + 11px),#1d2a52 calc(10% + 11px) 100%);box-shadow:0 0 0 .5px rgba(251,246,236,.4),0 2px 8px rgba(0,0,0,.35)}
html{background:#141d3d}
body{background:radial-gradient(900px 520px at 85% -8%,rgba(214,40,57,.26),transparent 62%),radial-gradient(1000px 640px at -10% 18%,rgba(61,147,214,.26),transparent 60%),linear-gradient(180deg,#2c3f7c,#1d2a52 45%,#141d3d)!important;background-attachment:fixed!important}
body::before{display:none!important}
h1,h2,.nome,.sh-nome,.hh{font-family:Lobster,'Brush Script MT',cursive!important;font-weight:400!important;text-transform:none!important;letter-spacing:0!important}
h1{font-size:clamp(30px,6vw,48px)!important}
.cards{grid-template-columns:1fr 1fr!important;gap:10px!important}.c{min-height:0!important;padding:12px!important}.c .ic{height:64px!important;margin-bottom:8px!important}.c .ic img[src*="albo-alloro"],.c .ic img[src*="carriera-micro"]{height:62px!important;margin-top:0!important}.c .ic img{max-width:100%}.c h2{font-size:19px!important}.c p{display:none!important}.c .go{font-size:11px!important;margin-top:6px}.card,.c,.mn,.lg-leghe{background:linear-gradient(150deg,rgba(255,255,255,.12),rgba(255,255,255,.05))!important}"""
N = R / "ufficiale" / "nuovo" / "girrr"
if N.parent.exists(): shutil.rmtree(N.parent)
shutil.copytree(OUT, N)
for f in N.glob("*.html"):
    x = f.read_text(encoding="utf-8").replace("../../anteprima/attuale.html", "../../../anteprima/index.html")
    if f.name != "curva.html":
        x = x.replace("</head>", '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lobster&display=swap">\n<style id="skin-nuova">' + SKIN + "</style>\n</head>", 1)
    else:
        x = x.replace("</head>", '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lobster&display=swap">\n<style id="skin-nuova">.bar .tt,.bar .tt>span,h2{font-family:Lobster,\'Brush Script MT\',cursive!important;font-weight:400!important;letter-spacing:0!important}.bar .tt{font-size:25px!important}.bar .tt small{font-family:Inter,system-ui,sans-serif!important;font-size:12px!important;font-weight:500!important}</style>\n</head>', 1)
    f.write_text(x, encoding="utf-8")
(N.parent / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=girrr/index.html"><a href="girrr/index.html">Apri l\'anteprima</a>', encoding="utf-8")
print("scritto anche la versione nuova")
