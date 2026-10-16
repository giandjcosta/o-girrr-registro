"""Puntata di prova della Radio con quattro voci: conduttore, commentatore, inviata e Ciro (mercato)."""
import asyncio, json, pathlib
import edge_tts
R = pathlib.Path(__file__).parent
OUT = R.parent / "lab" / "voci"; OUT.mkdir(parents=True, exist_ok=True)
D = json.load(open(R / "dati.json", encoding="utf-8"))
NOMI = json.load(open(R / "nomi.json", encoding="utf-8"))
VOCI = {"B": "it-IT-GiuseppeMultilingualNeural", "G": "en-US-BrianMultilingualNeural", "S": "de-DE-SeraphinaMultilingualNeural", "C": "fr-FR-RemyMultilingualNeural"}
RUOLO = {"B": "Conduttore", "G": "Commentatore", "S": "Inviata speciale", "C": "Mercato"}
f = lambda x: str(x).replace(".", ",")
a = D["aw"][-1]; T = D["tab"]
DER = [("Grodah","WOA"),("stif dc","Real Madrink"),("Oranje VC","AFA SELECCION"),("Apo team","The Blue brothers"),("Mariana Coneja","Atletico ma non troppo")]
def derby(m): return any({x.lower(), y.lower()} == {m[0].lower(), m[1].lower()} for x, y in DER)
g = D["cal"][0]["m"]; der = next((m for m in g if derby(m)), g[0])
b, gg, s, c = NOMI["B"], NOMI["G"], NOMI["S"], NOMI["C"]
L = [
 ("B", f"Buongiorno a tutti e ben arrivati a Radio Girrr! Io sono {b}, qui con {gg}, e queste sono le notizie della settimana dopo la giornata {a['n']} di campionato."),
 ("G", f"Grazie {b}. Ragazzi, che giornata."),
 ("B", f"{a['mvp'][0]} si prende la corona di re della giornata, con {f(a['mvp'][1])} punti."),
 ("G", f"Non tutti hanno festeggiato però. {a['flop'][0]} si ferma a {f(a['flop'][1])} punti."),
 ("B", f"E la sconfitta più pesante è quella di {a['maz'][0]}, battuta da {a['maz'][3]} di {f(a['maz'][2])} punti."),
 ("G", f"In classifica comanda {T[0]['t']} con {T[0]['pts']} punti, seguita da {T[1]['t']} e {T[2]['t']}."),
 ("B", f"Ora ci colleghiamo con la nostra inviata dal campo. {s}, a te."),
 ("S", f"Grazie {b}, eccomi. Notizie dall'infermeria: Raspadori dell'Atalanta ha un fastidio alla gamba e verrà valutato per il prossimo turno. Per Gudmundsson della Lazio, un problema alla spalla dopo una caduta, ed è in dubbio."),
 ("S", "Come sempre, controllate la formazione prima del calcio d'inizio. Per ora è tutto, restituisco la linea in studio."),
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
async def main():
    parti = []
    for i, (k, t) in enumerate(L):
        fn = OUT / f"_p{i}.tmp"
        await edge_tts.Communicate(t, VOCI[k], rate="+4%").save(str(fn)); parti.append(fn)
    with open(OUT / "puntata.mp3", "wb") as o:
        for p in parti: o.write(p.read_bytes()); p.unlink()
    json.dump([{"chi": NOMI[k], "ruolo": RUOLO[k], "testo": t} for k, t in L], open(OUT / "puntata.json", "w"), ensure_ascii=False)
    print("ok", len(L))
asyncio.run(main())
