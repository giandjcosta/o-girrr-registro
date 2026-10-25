"""Aggiorna la copia salvata del Changelog (SNAP in index.html) con i commit pubblici del sito.
python3 changelog.py   (dalla cartella del repo)
La pagina legge da sola da GitHub solo le ultime 100 modifiche: il resto lo prende da qui."""
import json, pathlib, re, urllib.request
R = pathlib.Path(__file__).resolve().parent
NOISE = re.compile(r"^(risultati reali|aggiorna |riavvia|ripristina|rimuove cache|prova rete|merge|initial commit|tolgo la pagina novit|novità 4.5|sql prestiti)", re.I)
out, p = [], 1
while True:
    u = f"https://api.github.com/repos/giandjcosta/o-fant-a-girrr/commits?sha=gh-pages&per_page=100&page={p}"
    j = json.load(urllib.request.urlopen(u))
    out += [[c["commit"]["committer"]["date"], c["commit"]["message"].split("\n")[0]] for c in j]
    if len(j) < 100: break
    p += 1
out = [x for x in out if not NOISE.search(x[1])]
f = R / "index.html"
s = f.read_text()
s = re.sub(r"var SNAP=\[.*?\]\],AREE=", lambda m: "var SNAP=" + json.dumps(out, ensure_ascii=False) + ",AREE=", s, count=1, flags=re.S)
f.write_text(s)
print(len(out), "modifiche, l'ultima del", out[0][0][:10])
