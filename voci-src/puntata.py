import sys
"""Puntata di prova della Radio con quattro voci: conduttore, commentatore, inviata e Ciro (mercato)."""
import asyncio, json, pathlib
import edge_tts
R = pathlib.Path(__file__).parent
OUT = R.parent / "lab" / "voci"; OUT.mkdir(parents=True, exist_ok=True)
D = json.load(open(R / "dati.json", encoding="utf-8"))
NOMI = json.load(open(R / "nomi.json", encoding="utf-8"))
SUF = sys.argv[2] if len(sys.argv)>2 else ""
VOCI = {"B": "it-IT-DiegoNeural", "G": (sys.argv[1] if len(sys.argv)>1 else "en-US-AndrewMultilingualNeural"), "S": "de-DE-SeraphinaMultilingualNeural", "C": "it-IT-GiuseppeMultilingualNeural"}
RUOLO = {"B": "Conduttore", "G": "Commentatore", "S": "Inviata speciale", "C": "Mercato"}
def f(x):
    x = float(x)
    return str(int(x)) if x == int(x) else str(x).replace(".", ",")
NUM = ["zero","uno","due","tre","quattro","cinque","sei","sette","otto","nove","dieci"]
PRON = {"Girrr": "Giirrr", "Champions Cup": "Cèmpions Càp", "AFA SELECCION": "Afa Seleccion"}
ORD = {1:"prima",2:"seconda",3:"terza",4:"quarta",5:"quinta",6:"sesta",7:"settima",8:"ottava",9:"nona",10:"decima"}
a = D["aw"][-1]; T = D["tab"]
DER = [("Grodah","WOA"),("stif dc","Real Madrink"),("Oranje VC","AFA SELECCION"),("Apo team","The Blue brothers"),("Mariana Coneja","Atletico ma non troppo")]
def derby(m): return any({x.lower(), y.lower()} == {m[0].lower(), m[1].lower()} for x, y in DER)
g = D["cal"][0]["m"]; der = next((m for m in g if derby(m)), g[0])
b, gg, s, c = NOMI["B"], NOMI["G"], NOMI["S"], NOMI["C"]
b1, g1, s1, c1 = b.split()[0], gg.split()[0], s.split()[0], c.split()[0]
P = D["prob"]
def pct(x): return f(round(x))
fav = max(P, key=lambda t: P[t]["s"][-1])
nera = max(P, key=lambda t: P[t]["u"][-1])
salto = max(P, key=lambda t: abs(P[t]["s"][-1] - P[t]["s"][0]))
EXP = {"Oranje VC":4,"Apo team":5,"Grodah":3,"WOA":2,"Real Madrink":3,"stif dc":6,"Mariana Coneja":6,"AFA SELECCION":4,"The Blue brothers":7,"Atletico ma non troppo":8}
sup = max(((r["t"], EXP.get(r["t"], 5), r["pos"]) for r in T), key=lambda x: x[1]-x[2])
conf = next(((m[0], m[1]) for m in g if "Oranje VC" in m), (g[0][0], g[0][1]))
# stili di voce: urlo = entusiasta, sus = sussurrato/complice, None = normale
L = [
 ("B", f"Buongiorno, buonasera e buonanotte a tutti! Siete sintonizzati su Radio Girrr, la radio che non dorme mai! Io sono {b}, e qui con me, come sempre, c'è {gg}.", "urlo"),
 ("G", f"Grazie {b1}. Ho dormito poco, ho letto i punteggi e adesso sono sveglissimo. Che giornata, ragazzi."),
 ("B", f"Giornata numero {a['n']}, e partiamo subito con la corona! {a['mvp'][0]} si prende la giornata con {f(a['mvp'][1])} punti!", "urlo"),
 ("G", f"{f(a['mvp'][1])} punti, {b1}. Roba da scudetto. Da oggi {a['mvp'][0]} cammina a un metro da terra, e a un metro e mezzo dagli altri."),
 ("B", f"Ma c'è chi ha passato un weekend meno felice. Il flop di giornata è {a['flop'][0]}: ferma a {f(a['flop'][1])} punti."),
 ("G", f"{f(a['flop'][1])} punti. Io non voglio infierire. Dico solo che a quella squadra serve un abbraccio. Sottovoce, eh.", "sus"),
 ("B", f"E la sconfitta più pesante è quella di {a['maz'][0]}, battuta da {a['maz'][3]} con {f(a['maz'][2])} punti di scarto. Una mazzata, signori."),
 ("G", f"Altro che mazzata, è stata una cassa di birra data in testa. Però, {b1}, la classifica non mente."),
 ("B", f"Ed è qui che si fa interessante. Secondo i nostri calcoli, oggi il favorito per lo scudetto è {fav}, con il {pct(P[fav]['s'][-1])} per cento di probabilità!", "urlo"),
 ("G", f"Intanto {salto} passa dal {pct(P[salto]['s'][0])} al {pct(P[salto]['s'][-1])} per cento. Questo, nella vita, si chiama montagna russa."),
 ("B", f"E in fondo? La maglia nera, per ora, ha il nome di {nera}: il {pct(P[nera]['u'][-1])} per cento di finire ultimi. Coraggio, c'è ancora tempo!"),
 ("B", f"Ora ci colleghiamo con la nostra inviata sul campo. {s1}, siamo da te!", "urlo"),
 ("S", f"Grazie {b1}! Qui è un bel caos, vi assicuro, c'è un'aria che si taglia con il coltello. Prima notizia: {sup[0]} sta superando le aspettative! Il presidente la voleva intorno al {sup[1]}° posto, e invece oggi è {ORD.get(sup[2], str(sup[2])+'ª')}.", "urlo"),
 ("S", f"Ultim'ora: nuovo badge in bacheca! {a['mvp'][0]} sblocca il traguardo Re della giornata, con {f(a['mvp'][1])} punti. Una bella soddisfazione!"),
 ("S", f"E dalla sala stampa, alla vigilia di {conf[0]} contro {conf[1]}, l'allenatore non ha dubbi: «Chi non crede in noi può restare a casa.» Parole pesanti. {b1}, {g1}, restituisco la linea in studio!"),
 ("G", f"Grazie {s1}. Un allenatore, due frasi e già mezza lega è offesa. Questo è calcio."),
]
cup = D["cup"][-1] if D.get("cup") else None
if cup:
    L.append(("B", f"Passiamo alla coppa! Si è chiusa la giornata {cup['n']} della Champions Cup, la coppa della nostra lega.", "urlo"))
    for i, m in enumerate(sorted(cup["m"], key=lambda m: -abs(m[2]-m[3]))[:2]):
        x, y = m[1], m[4]; ga, gb = m[5].split("-"); ga, gb = int(ga), int(gb)
        if ga == gb: frase = f"In coppa, {x} e {y} si dividono la posta: la partita finisce {NUM[ga]} a {NUM[gb]}."
        elif ga > gb: frase = f"In coppa, vittoria di {x} contro {y}: il risultato finale è {NUM[ga]} a {NUM[gb]}."
        else: frase = f"In coppa, vittoria di {y} contro {x}: il risultato finale è {NUM[gb]} a {NUM[ga]}."
        L.append(("G" if i == 0 else "B", frase))
    L.append(("G", "E ricordate: le multe di chi dimentica la formazione vanno dritte nel montepremi. Se non mettete la formazione, pagate la coppa, ve lo diciamo con affetto."))
L += [
 ("B", f"E adesso uno spazio speciale: il mercato! Qui con noi c'è {c}. {c1}, a te la linea!", "urlo"),
 ("C", f"Pssst. Buongiorno a tutti, qui {c}. Sento aria di scambi per la prossima settimana. Chi ha un portiere in più, alzi la mano. Io l'ho detto prima di tutti, ricordatevelo.", "sus"),
 ("G", f"{c1}, come sempre, sicurissimo. Al cento per cento. Il cento per cento delle volte, sbagliato."),
 ("B", f"Alla prossima giornata, occhio al derby: {der[0]} contro {der[1]}! Tra queste due squadre non si scherza, e nemmeno noi.", "urlo"),
 ("G", "Prepariamo i popcorn. E le scuse, per chi perde."),
 ("B", "Per Radio Girrr è tutto. Mettete la formazione, vi vogliamo bene, ci sentiamo mercoledì prossimo! Ciao a tutti!", "urlo"),
]
import re
STILI = {"urlo": dict(rate="+12%", pitch="+3Hz", volume="+6%"), "sus": dict(rate="-4%", pitch="-3Hz", volume="-10%"), None: dict(rate="+6%")}
async def uno(voce, tx, fn, stile):
    kw = STILI.get(stile, {}) if isinstance(stile, (str, type(None))) else {"rate": stile}
    c = edge_tts.Communicate(tx, voce, **kw)
    await c.save(str(fn))

async def parla(k, testo, fn, i, stile=None):
    """Prova la riga intera; se la voce non risponde la legge a frasi; come ultima scelta usa Isabella."""
    for a_, b_ in PRON.items(): testo = testo.replace(a_, b_)
    pulito = testo.replace("«", "").replace("»", "").replace("ª", "a").replace("°", "")
    for n, (tx, st_) in enumerate([(testo, stile), (pulito, "base")]):
        try:
            await uno(VOCI[k], tx, fn, st_); return
        except Exception as e:
            print("riga", i, VOCI[k], "intera, tentativo", n, "fallito:", type(e).__name__); await asyncio.sleep(1)
    frasi = [x for x in re.split(r"(?<=[.:!?])\s+", pulito) if x.strip()]
    pezzi = []
    for j, fr in enumerate(frasi):
        tmp = fn.with_suffix(f".{j}.part")
        try:
            await uno(VOCI[k], fr, tmp, "base")
        except Exception as e:
            print("riga", i, "frase", j, VOCI[k], "fallita, uso Isabella:", fr[:50])
            await uno("it-IT-IsabellaNeural", fr, tmp, "base")
        pezzi.append(tmp)
    with open(fn, "wb") as o:
        for q in pezzi: o.write(q.read_bytes()); q.unlink()

async def main():
    parti = []
    for i, riga in enumerate(L):
        k, t = riga[0], riga[1]; st = riga[2] if len(riga) > 2 else None
        fn = OUT / f"_p{i}.tmp"
        await parla(k, t, fn, i, st); parti.append(fn)
    with open(R / "_voci.mp3", "wb") as o:
        for p in parti: o.write(p.read_bytes()); p.unlink()
    json.dump([{"chi": NOMI[k], "ruolo": RUOLO[k], "testo": t} for k, t, *_ in L], open(OUT / f"puntata{SUF}.json", "w"), ensure_ascii=False)
    print("ok", len(L))
asyncio.run(main())
