"""Genera anteprima/index.html a partire dal Lab: stessa logica, ma impaginata come l'app vera (Home con riquadri, niente voti né note del laboratorio).
Si lancia con: python3 anteprima/build.py (dalla cartella del repo). Va rilanciato ogni volta che cambia lab/index.html."""
import pathlib, re
R = pathlib.Path(__file__).resolve().parent.parent
s = (R / "lab" / "index.html").read_text(encoding="utf-8")
def sost(a, b, n=1):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b, n)
sost("<title>Laboratorio O Girrr</title>", "<title>O Girrr · Anteprima 5.0</title>")
sost('href="../favicon-64.png"', 'href="../favicon-64.png"')
sost("<h1>Laboratorio O Girrr</h1>", "<h1>O Girrr 5.0</h1>")
sost("<p>Prova ogni idea e dai un voto. Alla fine trovi il riassunto da mandare a Gianluca.</p>", "<p>Anteprima della nuova versione: così apparirà tutto quando andrà in linea.</p>")
sost('<span class="proto">Prototipo</span> <a class="back" href="../">Torna al Registro</a>', '<span class="proto">Anteprima</span> <a class="back" href="../lab/versione-5.html">Cosa c\'è e cosa manca</a>')
# nascondere il materiale da laboratorio
sost("</style>", ".where,.note,.lead,.fb,.proto-only{display:none!important}.hm{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}.hm button{display:flex;flex-direction:column;gap:4px;text-align:left;padding:14px;border-radius:16px;background:linear-gradient(160deg,#17214a,#2a1c52);border:1px solid var(--line);color:#fff;min-height:96px}.hm b{font-family:var(--fd);font-size:20px;font-weight:400}.hm small{color:var(--mute);font-size:12px;font-weight:600}.hm .big{grid-column:1/-1}</style>", 1)
# nav e Home
sost(re.search(r"var TABS=\[.*?\];", s).group(0), "var TABS=[['home','Home'],['sport','Girrr Sport'],['oro','Albo d\\'oro'],['spog','Spogliatoio'],['toto','Totogirrr'],['carriera','Carriera']];")
sost("var cur='prob',", "var cur='home',")
home = r"""function vHome(){var T=[['sport','Girrr Sport','Giornale, conferenze stampa, radio e sfide lanciate','big'],['oro','Albo d\'oro','Storia, stagioni, Era Precedente, derby e Albo di Latta'],['spog','Spogliatoio','Il Borsino e la tua squadra'],['toto','Totogirrr','Le probabilità e le quote'],['carriera','Carriera','Obiettivi, presidente e Cassa']];
  return '<div class="hm">'+T.map(function(t){return '<button data-tab="'+t[0]+'" class="'+(t[3]||'')+'">'+(t[0]==='sport'?'<img src="'+D.img.gs+'" alt="Girrr Sport" style="height:46px;width:auto;align-self:flex-start;border-radius:6px">':'<b>'+t[1]+'</b>')+'<small>'+t[2]+'</small></button>'}).join('')+'</div>'}
function vSpog(){return vBors()}function vToto(){return vProb()}
var V={spog:vSpog,toto:vToto,home:vHome,"""
sost("var V={", home)
sost("(cur==='parere'?'':fbBox())", "''")
sost("S.fb[cur]", "S.fb[cur]")

# --- Ristrutturazione: tutto dentro quattro tab grandi ---
sost("['derby','I derby'],['all','Gli allenatori']", "['derby','I derby'],['latta','Albo di Latta'],['all','Gli allenatori']")
sost("  if(S.oro==='storia')h+=", "  if(S.oro==='derby')return h+vDerby();if(S.oro==='latta')return h+vAlbo();\n  if(S.oro==='storia')h+=")
s = re.sub(r"\+'<div class=\"card\"><h3>Cosa cambia in Home</h3>.*?homeMock\(\)\+'</div>'", "", s, flags=re.S)
sost("['moviola','Moviola · presto']]", "['sfide','Sfide lanciate'],['moviola','Moviola · presto']]")
sost("sp==='radio'?spRadio():'';", "sp==='radio'?spRadio():sp==='sfide'?vSfide():'';")
extra = r"""
S.cr=S.cr||'ob';
var vCar0=vCar;
function vCarr(){return '<div class="seg" role="group" aria-label="Sezioni">'+[['ob','Obiettivi e presidente'],['cassa','Cassa · da decidere']].map(function(x){return '<button data-cr="'+x[0]+'" aria-pressed="'+(S.cr===x[0])+'">'+x[1]+'</button>'}).join('')+'</div>'+(S.cr==='cassa'?vCassa():vCar0())}
document.addEventListener('click',function(e){var b=e.target.closest('[data-cr]');if(!b)return;S.cr=b.dataset.cr;render()});
function route(t){var M={derby:['oro','oro','derby'],albo:['oro','oro','latta'],sfide:['sport','sp','sfide'],borsino:['spog'],prob:['toto'],cassa:['carriera','cr','cassa']};
  if(M[t]){if(M[t][1])S[M[t][1]]=M[t][2];return M[t][0]}return t}
"""
sost("var V={spog:vSpog,toto:vToto,home:vHome,", extra + "function vSpog(){return vBors()}function vToto(){return vProb()}\nvar V={spog:vSpog,toto:vToto,home:vHome,")
sost("function go(t){", "function go(t){t=route(t);")
sost("if(V[hh])cur=hh;", "if(V[hh])cur=route(hh);")
sost("carriera:vCar,", "carriera:vCarr,")
sost(".seg{display:flex;", ".seg{flex-wrap:wrap;display:flex;") if False else None
s_plain = s  # senza loghi nelle tab: serve alla grafica attuale
# tab più piccole con i loghi ufficiali
sost("</style>", "html{background:#141d3d}body::before{display:none!important}.seg{flex-wrap:wrap}.tabs{background:none!important;backdrop-filter:none}.tabs{gap:5px;padding:6px 0}.tabs button{padding:5px 11px 5px 7px;font-size:12px;display:inline-flex;align-items:center;gap:6px}.tabs button img.gsl{width:auto;height:22px;border-radius:3px}.tabs button img{width:18px;height:18px;object-fit:contain;border-radius:4px}</style>")
sost("""'<button role="tab" data-tab="'+t[0]+'" aria-selected="'+(cur===t[0])+'">'+t[1]+'</button>'""",
     """'<button role="tab" data-tab="'+t[0]+'" aria-selected="'+(cur===t[0])+'" aria-label="'+t[1]+'">'+(t[0]==='sport'?'<img class="gsl" src="'+D.img.gs+'" alt="Girrr Sport">':(({home:1,oro:1,spog:1,carriera:1})[t[0]]?'<img src="'+D.img.lega+'" alt="">':'')+t[1])+'</button>'""")
s = s.replace('src="voci/', 'src="../lab/voci/').replace("fetch('voci/", "fetch('../lab/voci/")
out = R / "anteprima" / "index.html"
out.write_text(s, encoding="utf-8")
print("scritto", out, len(s))
# Seconda versione: stesse funzioni, grafica attuale del sito (font Inter, sfondo a barre, tab a pillola)
skin = """<style id="skin-attuale">
:root{--fd:Inter,system-ui,sans-serif;--bg:#1d2a52}
html,body{background:#1d2a52}
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
s_plain = s_plain.replace('src="voci/', 'src="../lab/voci/').replace("fetch('voci/", "fetch('../lab/voci/")
a = s_plain.replace("</style>", "</style>" + skin, 1)
a = a.replace("<title>O Girrr · Anteprima 5.0</title>", "<title>O Girrr · Anteprima 5.0 (grafica attuale)</title>")
a = a.replace("family=Lobster&family=Inter", "family=Inter")
(R / "anteprima" / "attuale.html").write_text(a, encoding="utf-8")
print("scritto attuale.html")
