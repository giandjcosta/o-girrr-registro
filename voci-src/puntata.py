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
import random, copione
MERC = json.load(open(R / "mercato.json", encoding="utf-8")) if (R / "mercato.json").exists() else {}
L = copione.build(D, random.Random(D["aw"][-1]["n"] * 7919), MERC)
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
    for n, (tx, st_) in enumerate([(testo, stile)] * 4 + [(pulito, "base")] * 3):
        try:
            await uno(VOCI[k], tx, fn, st_); return
        except Exception as e:
            print("riga", i, VOCI[k], "intera, tentativo", n, "fallito:", type(e).__name__); await asyncio.sleep(1.5)
    frasi = [x for x in re.split(r"(?<=[.:!?])\s+", pulito) if x.strip()]
    pezzi = []
    for j, fr in enumerate(frasi):
        tmp = fn.with_suffix(f".{j}.part")
        try:
            for _t in range(4):
                try: await uno(VOCI[k], fr, tmp, "base"); break
                except Exception: await asyncio.sleep(1.5)
            else: raise RuntimeError("sempre fallita")
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
