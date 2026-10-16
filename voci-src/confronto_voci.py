import asyncio, pathlib, edge_tts
import edge_tts.communicate as _ec
_mk0 = _ec.mkssml
def _mk(tc, t):
    if "Multilingual" in tc.voice:
        if isinstance(t, bytes): t = t.decode("utf-8")
        t = f"<lang xml:lang='it-IT'>{t}</lang>"
    return _mk0(tc, t)
_ec.mkssml = _mk
R = pathlib.Path(__file__).parent
OUT = R.parent / "lab" / "voci" / "confronto"; OUT.mkdir(parents=True, exist_ok=True)
TESTO = "Grazie Beppe! Qui è un bel caos! Prima notizia: Apo team sta superando le aspettative. Il presidente la voleva intorno al quinto posto, e invece oggi è primo! Parole pesanti, signori."
FEM = {"Isabella (italiana)": "it-IT-IsabellaNeural", "Elsa (italiana)": "it-IT-ElsaNeural", "Seraphina (tedesca)": "de-DE-SeraphinaMultilingualNeural", "Ava (americana)": "en-US-AvaMultilingualNeural", "Emma (americana)": "en-US-EmmaMultilingualNeural", "Vivienne (francese)": "fr-FR-VivienneMultilingualNeural"}
MAS = {"Giuseppe (italiano)": "it-IT-GiuseppeMultilingualNeural", "Diego (italiano)": "it-IT-DiegoNeural", "Andrew (americano)": "en-US-AndrewMultilingualNeural", "Brian (americano)": "en-US-BrianMultilingualNeural", "Rémy (francese)": "fr-FR-RemyMultilingualNeural", "Florian (tedesco)": "de-DE-FlorianMultilingualNeural"}
async def gen(nome, voce, i):
    for t in range(6):
        try:
            await edge_tts.Communicate(TESTO, voce, rate="+6%").save(str(OUT / f"{i}.mp3")); return True
        except Exception as e:
            await asyncio.sleep(1.5)
    return False
async def main():
    html = ["<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><meta name=robots content=noindex><title>Confronto voci</title><body style='font-family:system-ui;max-width:640px;margin:0 auto;padding:16px'><h2>Quale voce è più realistica?</h2><p>Stessa frase letta da ogni voce.</p>"]
    i = 0
    for titolo, gruppo in (("Voci femminili", FEM), ("Voci maschili", MAS)):
        html.append(f"<h3>{titolo}</h3>")
        for nome, voce in gruppo.items():
            ok = await gen(nome, voce, i)
            if ok: html.append(f"<p><b>{nome}</b><br><audio controls preload=none src='voci/confronto/{i}.mp3?v=1' style='width:100%'></audio></p>")
            else: html.append(f"<p><b>{nome}</b>: non è stato possibile generarla.</p>")
            i += 1
    (R.parent / "lab" / "confronto-voci.html").write_text("".join(html), encoding="utf-8")
asyncio.run(main())
