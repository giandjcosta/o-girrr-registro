"""Crea gli audio di prova della Radio con le voci neurali di Edge (edge-tts)."""
import asyncio, json, subprocess, pathlib, sys
import edge_tts
R = pathlib.Path(__file__).parent
OUT = R.parent / "lab" / "voci"; OUT.mkdir(parents=True, exist_ok=True)
TMP = R / "tmp"; TMP.mkdir(exist_ok=True)
rows = json.load(open(R / "radio.json", encoding="utf-8"))

async def scegli(locale, preferite):
    voci = await edge_tts.list_voices()
    nomi = {v["ShortName"] for v in voci if v["Locale"].startswith(locale[:2])}
    print(locale, sorted(n for n in nomi if n.startswith(locale))[:20])
    for n in preferite:
        if n in nomi: return n
    return next(iter(sorted(n for n in nomi if n.startswith(locale))))

async def fai(nome, campo, voci, rate):
    files = []
    for i, r in enumerate(rows):
        v = voci[0] if r["s"] == "Steve" else voci[1]
        f = TMP / f"{nome}_{i:02d}.mp3"
        await edge_tts.Communicate(r[campo], v, rate=rate).save(str(f))
        files.append(f)
    lst = TMP / f"{nome}.txt"
    lst.write_text("".join(f"file '{f.resolve()}'\n" for f in files))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "libmp3lame", "-b:a", "96k", str(OUT / f"{nome}.mp3")], check=True)
    print("creato", nome, voci)

async def main():
    en = [await scegli("en-GB", ["en-GB-RyanNeural"]), await scegli("en-GB", ["en-GB-ThomasNeural", "en-GB-AlfieNeural"])]
    it = [await scegli("it-IT", ["it-IT-DiegoNeural"]), await scegli("it-IT", ["it-IT-GiuseppeMultilingualNeural", "it-IT-GiuseppeNeural", "it-IT-BenignoNeural"])]
    await fai("radio-en", "en", en, "+4%")
    await fai("radio-it", "it", it, "+4%")
asyncio.run(main())
