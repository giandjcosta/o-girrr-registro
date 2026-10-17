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
js = "var RIV=%s;\nvar PRE=%s;\nvar STAG=%s;\nconsole.log(JSON.stringify({riv:RIV,pre:PRE,stag:STAG}));" % (estrai("RIV", ";\nS.vote="), estrai("PRE", ";\nvar OROSEZ"), estrai("STAG", ";\nS.oro="))
(R / "ufficiale" / "_x.js").write_text(js, encoding="utf-8")
dati = json.loads(subprocess.check_output(["node", str(R / "ufficiale" / "_x.js")]))
(R / "ufficiale" / "_x.js").unlink()
# racconti della storia della Lega: dal testo del Laboratorio
sto = re.search(r"<div class=\"rt\">Prima del 2021</div>(.*?)</div></div>", lab, re.S).group(1)
dati["storia"] = [p.strip() for p in re.findall(r"<p>(.*?)</p>", sto, re.S)]
rac = re.search(r"<div class=\"rac\"><div class=\"rt\">Il primo campionato</div>.*?(?=<p class=\"note\")", lab, re.S).group(0)
dati["racconti"] = [[t, p.replace("\\'", "'")] for t, p in re.findall(r"<div class=\"rt\">(.*?)</div><p>(.*?)</p></div>", rac, re.S)]
dati["storia"] = [p.replace("\\'", "'") for p in dati["storia"]]
vt = re.search(r"S\.vote=S\.vote\|\|\{\};S\.pend=S\.pend\|\|\{\};\[(.*?)\]\.forEach", lab, re.S).group(1)
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

# 3) Home: riquadro I derby
patch("index.html", '<a class="mn" href="albo.html">', '<a class="mn" href="derby.html"><div class="mi">⚔️</div><div><b>I derby</b><span>Rivalità, sfide e sfide decisive</span></div></a><a class="mn" href="albo.html">')
# 4) Albo: sezioni nuove
patch("albo.html", "</head>", '<script src="novita.js"></script>\n</head>')
patch("albo.html", "document.getElementById('al').innerHTML=stato()+allenatori()+storico()+recs();", "document.getElementById('al').innerHTML=stato()+(window.NOVITA?NOVITA(D):'')+allenatori()+storico()+recs();")
# 5) Curva: post nuovi dentro il feed
patch("curva.html", "</head>", '<script src="novita-curva.js"></script>\n</head>')
patch("curva.html", "function costruisci(){", "function costruisci(){if(window.ANT_POSTS)S.adm=(S.adm||[]).filter(function(u){return !u.ant}).concat(window.ANT_POSTS());")
# 6) Pagina Derby: stessa grafica dell'Albo
alb = (OUT / "albo.html").read_text(encoding="utf-8")
a0 = alb.index("<script>\n(function(){\nvar D=null;"); a1 = alb.index("</script>\n<script src=\"" + LIVE + "assets/app.js\">")
der = alb[:a0] + '<script src="derby.js"></script>\n' + alb[a1 + len("</script>\n"):]
der = der.replace("<h1>Albo d'oro</h1>", "<h1>I derby</h1>").replace("<title>Albo d'oro", "<title>I derby").replace('<div class="vuoto">Carico i record…</div>', '<div class="vuoto">Carico i derby…</div>')
der = der.replace("<script src=\"novita.js\"></script>\n", "")
(OUT / "derby.html").write_text(der, encoding="utf-8")

# 7) dati e script nuovi
(OUT / "novita-dati.js").write_text("window.NOV=" + json.dumps(dati, ensure_ascii=False) + ";", encoding="utf-8")
for n in ["novita.js", "derby.js", "novita-curva.js"]:
    sorg = (R / "ufficiale" / "src" / n).read_text(encoding="utf-8")
    sorg = sorg.replace("'../data.json'", "'" + LIVE + "data.json'")
    (OUT / n).write_text(sorg, encoding="utf-8")
for f in ["albo.html", "derby.html", "curva.html"]:
    p = OUT / f; t = p.read_text(encoding="utf-8")
    p.write_text(t.replace("</head>", '<script src="novita-dati.js"></script>\n</head>', 1), encoding="utf-8")
(R / "ufficiale" / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=girrr/index.html"><a href="girrr/index.html">Apri l\'anteprima</a>', encoding="utf-8")
print("scritto", OUT, len(list(OUT.iterdir())), "file")
