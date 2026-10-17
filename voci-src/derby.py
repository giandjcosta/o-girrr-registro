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
def _massimo():
    cl = classifica(); return max(1.0, cl[0][0])
def rivalita_storia(a, b):
    """Rivalità dalla sola storia, da 0 a 100."""
    return round(100 * punteggio(a, b) / _massimo(), 1)
def voto_amici(a, b, regole=None):
    """Quanto i suoi amici sentono la sfida come derby, da 0 a 100. Una coppia semplice vale 100; [a, b, 60] vale 60."""
    best = 0
    for p in ((regole or {}).get("derby_amici") or []):
        if {a, b} == set(p[:2]): best = max(best, p[2] if len(p) > 2 else 100)
    return best
def rivalita(a, b, regole=None):
    """Rivalità finale: la storia, più il peso dei voti degli amici. Un derby ha sempre una rivalità alta (almeno 70)."""
    v = voto_amici(a, b, regole); r = rivalita_storia(a, b)
    tot = min(100.0, r + 0.6 * v)
    if v >= 50: tot = max(70.0, tot)
    return round(tot, 1)
def intensita(a, b, regole=None):
    """Quanto è derby: i voti degli amici pesano il 60%, la storia il 40%."""
    return round(0.6 * voto_amici(a, b, regole) + 0.4 * rivalita_storia(a, b), 1)
def e_derby(a, b, partite=None, regole=None):
    """Derby se l'intensità arriva a 50. Se gli amici non hanno ancora detto niente, decide solo la storia: il quarto più alto di tutte le coppie."""
    if (regole or {}).get("derby_amici"):
        return intensita(a, b, regole) >= 50
    cl = classifica(); soglia = cl[len(cl) // 4][0]
    return punteggio(a, b) >= soglia and punteggio(a, b) > 0
if __name__ == "__main__":
    for p, x, y in classifica()[:12]: print(round(p, 1), x, "-", y, "rivalità", rivalita_storia(x, y))
