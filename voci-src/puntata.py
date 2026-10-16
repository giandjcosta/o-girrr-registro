"""Puntata di prova della Radio con quattro voci: conduttore, commentatore, inviata e Ciro (mercato)."""
import asyncio, json, pathlib
import edge_tts
R = pathlib.Path(__file__).parent
OUT = R.parent / "lab" / "voci"; OUT.mkdir(parents=True, exist_ok=True)
D = json.load(open(R / "dati.json", encoding="utf-8"))
NOMI = json.load(open(R / "nomi.json", encoding="utf-8"))
VOCI = {"B": "en-US-BrianMultilingualNeural", "G": "fr-FR-RemyMultilingualNeural", "S": "de-DE-SeraphinaMultilingualNeural", "C": "it-IT-GiuseppeMultilingualNeural"}
RUOLO = {"B": "Conduttore", "G": "Commentatore", "S": "Inviata speciale", "C": "Mercato"}
def f(x):
    x = float(x)
    return str(int(x)) if x == int(x) else str(x).replace(".", ",")
ORD = {1:"prima",2:"seconda",3:"terza",4:"quarta",5:"quinta",6:"sesta",7:"settima",8:"ottava",9:"nona",10:"decima"}
a = D["aw"][-1]; T = D["tab"]
DER = [("Grodah","WOA"),("stif dc","Real Madrink"),("Oranje VC","AFA SELECCION"),("Apo team","The Blue brothers"),("Mariana Coneja","Atletico ma non troppo")]
def derby(m): return any({x.lower(), y.lower()} == {m[0].lower(), m[1].lower()} for x, y in DER)
g = D["cal"][0]["m"]; der = next((m for m in g if derby(m)), g[0])
b, gg, s, c = NOMI["B"], NOMI["G"], NOMI["S"], NOMI["C"]
EXP = {"Oranje VC":4,"Apo team":5,"Grodah":3,"WOA":2,"Real Madrink":3,"stif dc":6,"Mariana Coneja":6,"AFA SELECCION":4,"The Blue brothers":7,"Atletico ma non troppo":8}
sup = max(((r["t"], EXP.get(r["t"], 5), r["pos"]) for r in T), key=lambda x: x[1]-x[2])
conf = next(((m[0], m[1]) for m in g if "Oranje VC" in m), (g[0][0], g[0][1]))
L = [
 ("B", f"Buongiorno a tutti e ben arrivati a Radio Girrr! Io sono {b}, qui con {gg}, e queste sono le notizie della settimana dopo la giornata {a['n']} di campionato."),
 ("G", f"Grazie {b}. Ragazzi, che giornata."),
 ("B", f"{a['mvp'][0]} si prende la corona di re della giornata, con {f(a['mvp'][1])} punti."),
 ("G", f"Non tutti hanno festeggiato però. {a['flop'][0]} si ferma a {f(a['flop'][1])} punti."),
 ("B", f"E la sconfitta più pesante è quella di {a['maz'][0]}, battuta da {a['maz'][3]} di {f(a['maz'][2])} punti."),
 ("G", f"In classifica comanda {T[0]['t']} con {T[0]['pts']} punti, seguita da {T[1]['t']} e {T[2]['t']}."),
 ("B", f"Ora ci colleghiamo con la nostra inviata dal campo. {s}, a te."),
 ("S", f"Grazie {b}, eccomi sul campo. Prima notizia: {sup[0]} sta superando le aspettative. Il presidente la voleva intorno al {sup[1]}° posto, e invece oggi è {ORD.get(sup[2], str(sup[2])+'ª')}."),
 ("S", f"Nuovo badge in bacheca: {a['mvp'][0]} sblocca il traguardo Re della giornata, con {f(a['mvp'][1])} punti."),
 ("S", f"Dalla sala stampa, alla vigilia di {conf[0]} contro {conf[1]}, l'allenatore non ha dubbi: «Chi non crede in noi può restare a casa.» Parole forti. Per ora è tutto, restituisco la linea in studio."),
]
cup = D["cup"][-1] if D.get("cup") else None
if cup:
    L.append(("B", f"Grazie {s}. E adesso le notizie della Coppa! Si è chiusa la giornata {cup['n']} della Champions Cup."))
    for i, m in enumerate(sorted(cup["m"], key=lambda m: -abs(m[2]-m[3]))[:2]):
        x, y = m[1], m[4]; ga, gb = m[5].split("-")
        frase = f"{x} e {y} si dividono la posta, {m[5]}." if ga == gb else (f"{x} batte {y} per {m[5]}." if int(ga) > int(gb) else f"{y} batte {x} per {gb}-{ga}.")
        L.append(("G" if i == 0 else "B", frase))
L += [
 ("B", f"E adesso uno spazio speciale: con noi c'è anche {c}, con le sue voci di mercato. {c}, a te."),
 ("C", f"Buongiorno a tutti, qui {c}. Sento aria di scambi per la prossima settimana: chi ha un portiere in più, alzi la mano. L'ho detto prima di tutti, ricordatevelo."),
 ("G", f"{c}, come sempre, sicurissimo."),
 ("B", f"Alla prossima giornata, occhio a {der[0]} contro {der[1]}."),
 ("G", "Sarà una bella giornata, questa lega migliora sempre."),
 ("B", "Per Radio Girrr è tutto. Ci sentiamo mercoledì prossimo!"),
]
import re
async def uno(voce, tx, fn, rate):
    c = edge_tts.Communicate(tx, voce, rate=rate) if rate else edge_tts.Communicate(tx, voce)
    await c.save(str(fn))

async def parla(k, testo, fn, i):
    """Prova la riga intera; se la voce non risponde la legge a frasi; come ultima scelta usa Isabella."""
    pulito = testo.replace("«", "").replace("»", "").replace("ª", "a").replace("°", "")
    for n, (tx, rate) in enumerate([(testo, "+4%"), (pulito, None)]):
        try:
            await uno(VOCI[k], tx, fn, rate); return
        except Exception as e:
            print("riga", i, VOCI[k], "intera, tentativo", n, "fallito:", type(e).__name__); await asyncio.sleep(1)
    frasi = [x for x in re.split(r"(?<=[.:!?])\s+", pulito) if x.strip()]
    pezzi = []
    for j, fr in enumerate(frasi):
        tmp = fn.with_suffix(f".{j}.part")
        try:
            await uno(VOCI[k], fr, tmp, None)
        except Exception as e:
            print("riga", i, "frase", j, VOCI[k], "fallita, uso Isabella:", fr[:50])
            await uno("it-IT-IsabellaNeural", fr, tmp, None)
        pezzi.append(tmp)
    with open(fn, "wb") as o:
        for q in pezzi: o.write(q.read_bytes()); q.unlink()

async def main():
    parti = []
    for i, (k, t) in enumerate(L):
        fn = OUT / f"_p{i}.tmp"
        await parla(k, t, fn, i); parti.append(fn)
    with open(OUT / "puntata.mp3", "wb") as o:
        for p in parti: o.write(p.read_bytes()); p.unlink()
    json.dump([{"chi": NOMI[k], "ruolo": RUOLO[k], "testo": t} for k, t in L], open(OUT / "puntata.json", "w"), ensure_ascii=False)
    print("ok", len(L))
asyncio.run(main())
