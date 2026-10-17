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
sost("var TABS=[['prob','Probabilità'],['sfide','Sfide'],['oro','Albo d\\'oro'],['albo','Albo di Latta'],['derby','Derby'],['borsino','Borsino'],['carriera','Carriera'],['cassa','Cassa'],['sport','Girrr Sport'],['parere','Il tuo parere']];",
     "var TABS=[['home','Home'],['sport','Girrr Sport'],['oro','Albo d\\'oro'],['albo','Albo di Latta'],['derby','Derby'],['sfide','Sfide'],['prob','Probabilità'],['borsino','Borsino'],['carriera','Carriera'],['cassa','Cassa']];")
sost("var cur='prob',", "var cur='home',")
home = r"""function vHome(){var T=[['sport','Girrr Sport','Radio, conferenza stampa e Giornale','big'],['oro','Albo d\'oro','Storia, stagioni, Era Precedente e derby'],['albo','Albo di Latta','Chi chiude in fondo'],['derby','Derby','Rivalità, sfide decisive, Totogirrr'],['sfide','Sfide','Una sfida a testa, con la posta'],['prob','Probabilità','Chi vince, chi sale, chi cade'],['borsino','Borsino','Il valore dei giocatori'],['carriera','Carriera','Presidente, obiettivi e fiducia'],['cassa','Cassa','I conti della lega']];
  return '<div class="hm">'+T.map(function(t){return '<button data-tab="'+t[0]+'" class="'+(t[3]||'')+'"><b>'+t[1]+'</b><small>'+t[2]+'</small></button>'}).join('')+'</div>'}
var V={home:vHome,"""
sost("var V={", home)
sost("(cur==='parere'?'':fbBox())", "''")
sost("S.fb[cur]", "S.fb[cur]")

# tab più piccole con i loghi ufficiali
sost("</style>", ".tabs{gap:5px;padding:6px 0}.tabs button{padding:5px 11px 5px 7px;font-size:12px;display:inline-flex;align-items:center;gap:6px}.tabs button img{width:18px;height:18px;object-fit:contain;border-radius:4px}</style>")
sost("""'<button role="tab" data-tab="'+t[0]+'" aria-selected="'+(cur===t[0])+'">'+t[1]+'</button>'""",
     """'<button role="tab" data-tab="'+t[0]+'" aria-selected="'+(cur===t[0])+'">'+(({sport:D.img.gs,home:D.img.lega,oro:D.img.lega,albo:D.img.lega,derby:D.img.lega})[t[0]]?'<img src="'+({sport:D.img.gs}[t[0]]||D.img.lega)+'" alt="">':'')+t[1]+'</button>'""")
out = R / "anteprima" / "index.html"
out.write_text(s, encoding="utf-8")
print("scritto", out, len(s))
