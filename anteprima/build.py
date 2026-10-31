"""Genera anteprima/index.html a partire dal Lab: stessa logica, ma impaginata come l'app vera (Home con riquadri, niente voti né note del laboratorio).
Si lancia con: python3 anteprima/build.py (dalla cartella del repo). Va rilanciato ogni volta che cambia lab/index.html."""
import os, pathlib, re
RIL0 = bool(os.environ.get("APP_RIL"))
R = pathlib.Path(__file__).resolve().parent.parent
s = (R / "lab" / "index.html").read_text(encoding="utf-8")
import sys; sys.path.insert(0, str(R / "rilascio"))
import livepatch
s = livepatch.applica(s, os.environ.get("APP_MODO", "prova"), os.environ.get("APP_DATI", "dati/lab-dati.json"))   # dati veri + database (in anteprima: finto, nel browser)
def sost(a, b, n=1):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b, n)
sost("<title>Laboratorio O Girrr</title>", "<title>O Girrr · Anteprima 5.3</title>")
sost('href="../favicon-64.png"', 'href="../favicon-64.png"')
sost("<h1>Laboratorio O Girrr</h1>", "<h1>O Girrr 5.3</h1>")
sost("<p>Prova ogni idea e dai un voto. Alla fine trovi il riassunto da mandare a Gianluca.</p>", "<p>Anteprima della nuova versione: così apparirà tutto quando andrà in linea.</p>")
sost('<span class="proto">Prototipo</span> <a class="back" href="../">Torna al Registro</a>', '<span class="proto">Anteprima 5.3</span> <a class="back" href="../lab/versione-5-2.html">Archivio 5.2</a>')
sost('<a class="back" href="versione-5-2.html">Archivio 5.2</a>', '')
# nascondere il materiale da laboratorio
sost("</style>", ".where,.note,.lead,.fb,.proto-only{display:none!important}.hm{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}.hm button{display:flex;flex-direction:column;gap:4px;text-align:left;padding:14px;border-radius:16px;background:linear-gradient(160deg,#17214a,#2a1c52);border:1px solid var(--line);color:#fff;min-height:96px}.hm b{font-family:var(--fd);font-size:20px;font-weight:400}.hm small{color:var(--mute);font-size:12px;font-weight:600}.hm .big{grid-column:1/-1}</style>", 1)
# nav e Home
sost(re.search(r"var TABS=\[.*?\];", s).group(0), "var TABS=[['home','Home'],['sport','Girrr Sport'],['oro','Albo d\\'oro'],['spog','Spogliatoio'],['toto','Totogirrr'],['carriera','Carriera']];")
sost("var cur='prob',", "var cur='home',")
home = r"""function vHome(){var T=[['sport','Girrr Sport','Giornale, conferenze stampa, radio e sfide lanciate','big'],['oro','Albo d\'oro','Storia, stagioni, Era dei Titani, Derby e Albo di Latta'],['spog','Spogliatoio','Il Borsino e la tua squadra'],['toto','Totogirrr','Le probabilità e le quote'],['carriera','Carriera','Obiettivi, presidente e Cassa']];
  return '<div class="hm">'+T.map(function(t){return '<button data-tab="'+t[0]+'" class="'+(t[3]||'')+'">'+(t[0]==='sport'?'<img src="'+D.img.gs+'" alt="Girrr Sport" style="height:46px;width:auto;align-self:flex-start;border-radius:6px">':'<b>'+t[1]+'</b>')+'<small>'+t[2]+'</small></button>'}).join('')+'</div>'}
function vSpog(){return vBors()}function vToto(){return vProb()}
var V={spog:vSpog,toto:vToto,home:vHome,"""
sost("var V={", home)
sost("where('Totogirrr','Sfide')+'<h2>Sfida 1 contro 1", "where('Totogirrr','Sfide 1 contro 1')+'<h2>Sfida 1 contro 1")
sost("  h+=sfidaCard();\n  var DT=", "  var DT=")
sost("(cur==='parere'?'':fbBox())", "''")
sost("S.fb[cur]", "S.fb[cur]")

# --- Ristrutturazione: tutto dentro quattro tab grandi ---
sost("['derby','I Derby'],['annuario','Annuario'],['all','Gli allenatori']", "['derby','I Derby'],['annuario','Annuario'],['latta','Albo di Latta'],['all','Gli allenatori']")
sost("  if(S.oro==='storia')h+=", "  if(S.oro==='derby')return h+vDerby();if(S.oro==='latta')return h+vAlbo();\n  if(S.oro==='storia')h+=")
s = re.sub(r"\+'<div class=\"card\"><h3>Cosa cambia in Home</h3>.*?homeMock\(\)\+'</div>'", "", s, flags=re.S)
sost("['moviola','Moviola']]", "['sfide','Sfide'],['moviola','Moviola']]")
sost("sp==='radio'?spRadio():sp==='moviola'?spMoviola():'';", "sp==='radio'?spRadio():sp==='sfide'?vSfideDerby():sp==='moviola'?spMoviola():'';")
extra = r"""
S.cr=S.cr||'ob';
var vCar0=vCar;
function vStat(){var ok=false;try{ok=JSON.parse(localStorage.getItem('fg')||'{}').team==='Oranje VC'}catch(e){}return ok?'<a class="card" href="@@STAT@@" style="display:block;margin-top:14px;padding:14px 16px;text-decoration:none;color:inherit"><b>📊 Statistiche</b><br><span style="opacity:.75;font-size:13px">Solo per te: chi entra e dove ›</span></a>':''}
function vCarr(){return '<button class="btn o" data-cr="'+(S.cr==='cassa'?'ob':'cassa')+'" style="margin-bottom:12px">'+(S.cr==='cassa'?'‹ Torna alla Carriera':'Apri la Cassa')+'</button>'+(S.cr==='cassa'?vCassa():vCar0())}
document.addEventListener('click',function(e){var b=e.target.closest('[data-cr]');if(!b)return;S.cr=b.dataset.cr;render()});
function vSfideDerby(){return where('Girrr Sport','Sfide')+'<h2>Sfide</h2><p class="lead">Sfida un rivale in conferenza stampa: la rivalità sale subito e, se lui accetta, nasce un Derby ufficiale.</p>'+sfidaHub()}
S.tt=S.tt||'prob';
function vTotoP(){return '<div class="seg" role="group" aria-label="Sezioni di Totogirrr">'+[['prob','Probabilità'],['duello','Sfide 1 contro 1']].map(function(x){return '<button data-tt="'+x[0]+'" aria-pressed="'+(S.tt===x[0])+'">'+x[1]+'</button>'}).join('')+'</div>'+(S.tt==='duello'?vSfide():vProb())}
document.addEventListener('click',function(e){var b=e.target.closest('[data-tt]');if(!b)return;S.tt=b.dataset.tt;render()});
function route(t){var M={derby:['oro','oro','derby'],albo:['oro','oro','latta'],sfide:['sport','sp','sfide'],duello:['toto','tt','duello'],borsino:['spog'],prob:['toto','tt','prob'],cassa:['carriera','cr','cassa']};
  if(M[t]){if(M[t][1])S[M[t][1]]=M[t][2];return M[t][0]}return t}
"""

if os.environ.get("APP_RIL"):   # nel sito vero Probabilità e Sfide 1 contro 1 vivono dentro Totogirrr, con il suo menu e la sua grafica
    extra += "(function(){function go(){var h=(location.hash||'').slice(1);if(h==='toto'||h==='prob'||h==='duello')location.replace('@@TOTO@@?t='+(h==='duello'?'sfide':'prob'))}go();window.addEventListener('hashchange',go)})();\n"
sost("var V={spog:vSpog,toto:vToto,home:vHome,", extra + "function vSpog(){return vBors()}function vToto(){return vTotoP()}\nvar V={duello:vSfide,spog:vSpog,toto:vToto,home:vHome,")
sost("function go(t){", "function go(t){t=route(t);if(t==='home'){location.href='@@HOME@@';return}")
sost("if(V[hh])cur=hh;", "if(V[hh])cur=route(hh);if(cur==='home'){location.replace('@@HOME@@')}")
sost("carriera:vCar,", "carriera:vCarr,")
sost("var CARSCELTA=true;", "var CARSCELTA=false;")   # Anteprima e sito vero: solo la propria squadra (in prova si cambia con ?come=Squadra)
if RIL0:   # nel sito vero i premi arrivano dal database (carriera_stato), non dal Totogirrr finto dell'anteprima
    sost("var PREMI52=true,", "var PREMI52=false,")
else:   # anteprima: Totogirrr è la pagina finta anteprima/totogirrr-52.html, con la squadra della Carriera; niente strumenti di prova a vista
    sost("function go(t){t=route(t);", "function go(t){var t0=t;if(t==='carriera')S.cr='ob';t=route(t);if(t==='toto'){location.href=toto52Url(S.cteam||ME,(location.pathname.split('/').pop()||'index.html')+'#'+cur)+(t0==='duello'?'&t=sfide':t0==='prob'?'&t=prob':'');return}")
    sost("if(cur==='home'){location.replace('@@HOME@@')}", "if(cur==='home'){location.replace('@@HOME@@')}if(cur==='toto'){location.replace(toto52Url(S.cteam||ME,'@@HOME@@'))}")
    sost("</style>", ".lvprova,[data-sst],[data-nm=\"s-prop\"],[data-nm=\"s-ok\"],[data-nm=\"s-ctr\"],[data-rx=\"nuova\"],[data-nuova]{display:none!important}</style>")
sost(".seg{display:flex;", ".seg{flex-wrap:wrap;display:flex;") if False else None

# Pagine come nel sito ufficiale: niente testata Anteprima né riga di tab; testata con scudo e titolo, link per tornare alla Home
sost('<div class="tabs" id="tabs" role="tablist" aria-label="Sezioni del prototipo"></div>', '<a class="oback" href="@@HOME@@">‹ O Girrr</a><header class="ohead"><img id="olg" alt=""><div><div class="okick">O FANT A GIRRR · 2026/27</div><h1 id="ot"></h1></div></header><div class="tabs" id="tabs" role="tablist" aria-label="Sezioni del prototipo" style="display:none"></div>')
sost("function render(){", "function render(){try{var _t=TABS.filter(function(z){return z[0]===cur})[0];$('#ot').textContent=_t?_t[1]:'';$('#olg').src=D.img.lega;document.title='O Girrr · '+(_t?_t[1]:'')}catch(e){}")
sost("</style>", ".top{display:none!important}.col{max-width:900px;padding:22px 16px 36px}.oback{display:inline-block;font-weight:800;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);text-decoration:none;margin-bottom:10px}.ohead{display:flex;align-items:center;gap:16px;margin:4px 0 18px}.ohead img{height:86px;width:auto;filter:drop-shadow(0 6px 10px rgba(0,0,0,.4))}.okick{font-weight:800;font-size:12px;letter-spacing:.3em;color:var(--gold)}.ohead h1{font-family:var(--fd);font-weight:900;font-size:clamp(34px,7vw,58px);line-height:1;margin:6px 0 0;letter-spacing:-.01em}</style>")
s_plain = s  # senza loghi nelle tab: serve alla grafica attuale
# tab più piccole con i loghi ufficiali
sost("</style>", "header.hero,header.top,.ohead{position:relative;padding-bottom:24px!important;margin-bottom:20px!important}header.hero::after,header.top::after,.ohead::after{content:'';position:absolute;left:0;right:0;bottom:0;height:10px;border-radius:2px;transform:skewX(-45deg);background:linear-gradient(90deg,#d62839 0 10%,#ffd166 10% calc(10% + 11px),#1d2a52 calc(10% + 11px) 100%);box-shadow:0 0 0 .5px rgba(251,246,236,.4),0 2px 8px rgba(0,0,0,.35)}html{background:#141d3d}.lg-leghe .go,button.go,.btn:not(.o):not(.ghost),.chips button.sel,.sq button.sel,button.sel{background:#ffd166!important;color:#1d2a52!important;border-color:#ffd166!important}.btn.o,.btn.ghost{background:rgba(255,255,255,.14)!important;color:#fbf6ec!important;border:1px solid rgba(255,255,255,.28)!important}.at button[aria-selected=true]{background:#ffd166!important;color:#1d2a52!important}.tabs button[aria-selected=true]{background:#ffd166!important;color:#1d2a52!important;border-color:transparent!important}.seg button[aria-pressed=true]{background:#ffd166!important;color:#1d2a52!important}.play,.mvbtn{background:#ffd166!important;color:#1d2a52!important;border-color:#ffd166!important}.mvbtn::before{border-left-color:#1d2a52!important}body{background:radial-gradient(900px 520px at 85% -8%,rgba(214,40,57,.26),transparent 62%),radial-gradient(1000px 640px at -10% 18%,rgba(61,147,214,.26),transparent 60%),linear-gradient(180deg,#2c3f7c,#1d2a52 45%,#141d3d)!important;background-attachment:fixed!important}body::before{display:none!important}.seg{flex-wrap:wrap}.tabs{background:none!important;backdrop-filter:none}.tabs{gap:5px;padding:6px 0}.tabs button{padding:5px 11px 5px 7px;font-size:12px;display:inline-flex;align-items:center;gap:6px}.tabs button img.gsl{width:auto;height:22px;border-radius:3px}.tabs button img{width:18px;height:18px;object-fit:contain;border-radius:4px}</style>")
sost("""'<button role="tab" data-tab="'+t[0]+'" aria-selected="'+(cur===t[0])+'">'+t[1]+'</button>'""",
     """'<button role="tab" data-tab="'+t[0]+'" aria-selected="'+(cur===t[0])+'" aria-label="'+t[1]+'">'+(t[0]==='sport'?'<img class="gsl" src="'+D.img.gs+'" alt="Girrr Sport">':(({home:1,oro:1,spog:1,carriera:1})[t[0]]?'<img src="'+D.img.lega+'" alt="">':'')+t[1])+'</button>'""")
s = s.replace('src="annuario.js"', 'src="../lab/annuario.js"')
s = s.replace('src="voci/', 'src="../lab/voci/').replace("fetch('voci/", "fetch('../lab/voci/")
RIL = bool(os.environ.get("APP_RIL"))   # rilascio: pagine per il sito vero (percorsi relativi, niente barra da anteprima)
VOCI = os.environ.get("APP_VOCI", "voci/")
MOV = os.environ.get("APP_MOV")   # nel sito vero la Moviola sta in girrr/dati/moviola.json (gh-pages), copiata dal workflow
def fin(t, stat, home):
    t = t.replace("@@STAT@@", stat).replace("@@HOME@@", home)
    if MOV:
        assert t.count("MVU='../calcoli/moviola.json'") == 1
        t = t.replace("MVU='../calcoli/moviola.json'", "MVU='" + MOV + "'")
    t = t.replace("@@TOTO@@", stat.replace("statistiche.html", "totogirrr.html"))
    if RIL:
        t = t.replace("../lab/voci/", VOCI).replace('<link rel="icon" href="../favicon-64.png">', "")
        t = re.sub(r'<link rel="icon"[^>]*favicon-64[^>]*>', "", t)
        t = re.sub(r'<span class="proto">.*?</span>( <a class="back"[^>]*>[^<]*</a>)+', "", t, count=1, flags=re.S)
        return t
    return t + '\n<script src="../ufficiale/girrr/barra.js"></script>\n'
if RIL:
    out = pathlib.Path(os.environ["APP_OUT_STADIO"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(fin(s, "statistiche.html", "index.html"), encoding="utf-8")
else:
    out = R / "anteprima" / "index.html"
    out.write_text(fin(s, "../ufficiale/nuovo/girrr/statistiche.html", "../ufficiale/nuovo/girrr/index.html"), encoding="utf-8")
print("scritto", out, len(s))
# Seconda versione: stesse funzioni, grafica attuale del sito (font Inter, sfondo a barre, tab a pillola)
skin = """<style id="skin-attuale">
:root{--fd:Inter,system-ui,sans-serif;--bg:#1d2a52}
html{background:transparent!important}
body{background:radial-gradient(1200px 700px at 80% -10%,#2c3f7c 0,#1d2a52 55%,#141d3d 100%)!important;background-attachment:fixed}
body::after{content:'';position:fixed;inset:-120px;z-index:-1;pointer-events:none;background:repeating-linear-gradient(115deg,rgba(255,255,255,.04) 0 36px,transparent 36px 72px);animation:strisce 9s linear infinite}
@keyframes strisce{to{transform:translate3d(79.45px,0,0)}}
@media (prefers-reduced-motion:reduce){body::after{animation:none}}
.top h1,h2,.derby .hd,.cov h3,.ch .vs{font-weight:900!important;letter-spacing:0}
.top h1{font-size:26px}h2{font-size:22px}
.tabs button{background:rgba(255,255,255,.1)!important;border:2px solid transparent!important;font-weight:800;opacity:.75}
.tabs button[aria-selected=true]{background:var(--red)!important;border-color:transparent!important;opacity:1}
.rac .rt,.rac h4{font-family:Inter,system-ui,sans-serif!important;font-weight:900}
.card,.derby,.cov,.hm button{background:linear-gradient(150deg,rgba(255,255,255,.12),rgba(255,255,255,.05))!important}
.seg button[aria-pressed=true]{background:var(--red)!important;color:#fff!important}
.tabs button{padding:9px 14px;font-size:13px}
</style>"""
s_plain = s_plain.replace('src="annuario.js"', 'src="../lab/annuario.js"')
s_plain = s_plain.replace('src="voci/', 'src="../lab/voci/').replace("fetch('voci/", "fetch('../lab/voci/")
a = s_plain.replace("</style>", "</style>" + skin, 1)
a = a.replace("<title>O Girrr · Anteprima 5.3</title>", "<title>O Girrr · Anteprima 5.3 (grafica attuale)</title>")
a = a.replace("family=Lobster&family=Inter", "family=Inter")
if RIL:
    pathlib.Path(os.environ["APP_OUT_LEGA"]).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.environ["APP_OUT_LEGA"]).write_text(fin(a, "statistiche.html", "index.html"), encoding="utf-8")
else:
    (R / "anteprima" / "attuale.html").write_text(fin(a, "../ufficiale/girrr/statistiche.html", "../ufficiale/girrr/index.html"), encoding="utf-8")
print("scritto attuale.html")

# Le sole build di preview aggiungono Home, Tabellone e Campo navigabili.
if not RIL:
    from navigazione import genera
    genera()
