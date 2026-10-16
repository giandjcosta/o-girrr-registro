"""Confronto delle voci: stesse frasi lette da molte voci di Edge, e due dialoghi italiani completi."""
import asyncio, json, pathlib
import edge_tts
R = pathlib.Path(__file__).parent
OUT = R.parent / "lab" / "voci"; OUT.mkdir(parents=True, exist_ok=True)
rows = json.load(open(R / "radio.json", encoding="utf-8"))

IT = ["it-IT-DiegoNeural","it-IT-GiuseppeMultilingualNeural","it-IT-IsabellaNeural","it-IT-ElsaNeural",
      "en-US-AndrewMultilingualNeural","en-US-BrianMultilingualNeural","en-US-AvaMultilingualNeural","en-US-EmmaMultilingualNeural",
      "de-DE-FlorianMultilingualNeural","de-DE-SeraphinaMultilingualNeural","fr-FR-RemyMultilingualNeural","fr-FR-VivienneMultilingualNeural"]
EN = ["en-GB-RyanNeural","en-GB-ThomasNeural","en-GB-SoniaNeural","en-GB-LibbyNeural","en-GB-MaisieNeural",
      "en-US-GuyNeural","en-US-ChristopherNeural","en-US-EricNeural","en-US-AndrewMultilingualNeural","en-US-BrianMultilingualNeural","en-AU-WilliamNeural","en-IE-ConnorNeural"]

async def clip(voce, testo, f):
    await edge_tts.Communicate(testo, voce, rate="+4%").save(str(f))

async def dialogo(nome, v1, v2, campo):
    parts = []
    for i, r in enumerate(rows):
        f = OUT / f"_{nome}_{i}.tmp"
        await clip(v1 if r["s"] == "Steve" else v2, r[campo], f); parts.append(f)
    with open(OUT / f"{nome}.mp3", "wb") as o:
        for f in parts: o.write(f.read_bytes()); f.unlink()

async def main():
    esistenti = {v["ShortName"] for v in await edge_tts.list_voices()}
    elenco = []
    for lingua, voci, campo in (("it", IT, "it"), ("en", EN, "en")):
        testo = " ".join(r[campo] for r in rows[:3])
        for v in voci:
            if v not in esistenti:
                print("manca", v); continue
            nome = f"{lingua}_{v.replace('Neural','').replace('Multilingual','ML')}"
            try:
                await clip(v, testo, OUT / f"{nome}.mp3")
                elenco.append({"lingua": lingua, "voce": v.replace("Neural",""), "file": f"{nome}.mp3"})
                print("ok", v)
            except Exception as e:
                print("errore", v, e)
    await dialogo("radio-it-b", "it-IT-DiegoNeural", "it-IT-IsabellaNeural", "it")
    await dialogo("radio-it-c", "it-IT-GiuseppeMultilingualNeural", "it-IT-ElsaNeural", "it")
    elenco.append({"dialogo": True, "label": "Diego e Isabella", "file": "radio-it-b.mp3"})
    elenco.append({"dialogo": True, "label": "Giuseppe ed Elsa", "file": "radio-it-c.mp3"})
    json.dump(elenco, open(OUT / "elenco.json", "w"), ensure_ascii=False)
    print("voci disponibili it:", sorted(v for v in esistenti if v.startswith("it-")))
asyncio.run(main())
