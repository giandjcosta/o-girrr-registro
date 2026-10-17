"""Derby: se gli amici di Gianluca ne segnalano, vincono loro. Altrimenti si calcola dalla storia della lega (storico.json, preso dall'Albo d'oro)."""
import json, pathlib, itertools
R = pathlib.Path(__file__).parent
# chi c'è dietro ogni squadra di oggi (nomi come nello storico). AFA SELECCION: da confermare
ALLENATORI = {"Apo team": ["apo"], "WOA": ["ser"], "Grodah": ["RikyArma"], "Real Madrink": ["AndrewTT"], "stif dc": ["stifson"],
              "Mariana Coneja": ["Mark Lenders"], "The Blue brothers": ["Mario", "Leanzino"], "Atletico ma non troppo": ["Riccardo"], "Oranje VC": ["DJ Cst Brazil"]}
def carica():
    S = json.load(open(R / "storico.json", encoding="utf-8")); al = S["alias"]
    per = {}   # allenatore -> {stagione: posizione}
    for e in S["storico"]:
        if "t" not in e: continue   # la Coppa Campioni non è il campionato
        for pos, riga in enumerate(e["t"], 1):
            m = al.get(riga[1], riga[1]); per.setdefault(m, {})[e["y"]] = pos
    return per
def prestigio(pos):
    return sum({1: 3, 2: 2, 3: 1}.get(p, 0) for p in pos.values())
def punteggio(a, b, per=None):
    """Più è alto, più la sfida è sentita: stagioni insieme, stagioni insieme nelle zone alte, peso dei podi e anzianità."""
    per = per or carica()
    A = {}; B = {}
    for m in ALLENATORI.get(a, []):
        for y, p in per.get(m, {}).items(): A[y] = min(p, A.get(y, 99))
    for m in ALLENATORI.get(b, []):
        for y, p in per.get(m, {}).items(): B[y] = min(p, B.get(y, 99))
    if not A or not B: return 0.0
    insieme = set(A) & set(B)
    zone_alte = sum(1 for y in insieme if A[y] <= 4 and B[y] <= 4)
    return 2 * len(insieme) + 2 * zone_alte + min(prestigio(A), prestigio(B)) + min(len(A), len(B))
def classifica():
    per = carica(); sq = list(ALLENATORI)
    return sorted(((punteggio(x, y, per), x, y) for x, y in itertools.combinations(sq, 2)), reverse=True)
def e_derby(a, b, partite, regole=None):
    """True se la sfida a-b è un derby. 'amici' (voti dei suoi amici) ha la precedenza; senza voti si usa la storia, tenendo il quarto più alto di tutte le coppie."""
    amici = [tuple(x) for x in ((regole or {}).get("derby_amici") or [])]
    if amici: return any({a, b} == set(p) for p in amici)
    cl = classifica(); soglia = cl[len(cl) // 4][0]
    return punteggio(a, b) >= soglia and punteggio(a, b) > 0
if __name__ == "__main__":
    for p, x, y in classifica()[:12]: print(round(p, 1), x, "-", y)
