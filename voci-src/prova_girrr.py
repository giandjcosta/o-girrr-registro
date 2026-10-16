import asyncio, pathlib, edge_tts
R = pathlib.Path(__file__).parent
OUT = R.parent / "lab" / "voci" / "girrr"; OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob("*.mp3"): f.unlink()
VOCI = {"steve": "en-US-AndrewMultilingualNeural", "beppe": "it-IT-DiegoNeural"}
GRAFIE = ["Ahia!", "Aia!", "Ahi ahi ahi!", "Ahiaaa!", "Ahìa, che male!", "Ahi, ahi, ahi, questa fa male!", "Ahi!"]
async def main():
    for v, voce in VOCI.items():
        for i, g in enumerate(GRAFIE):
            ok = False
            for t in range(5):
                try:
                    c = edge_tts.Communicate(g, voce, rate="+12%", pitch="+3Hz", volume="+6%")
                    await c.save(str(OUT / f"{v}-{i}.mp3")); ok = True; break
                except Exception as e:
                    print("errore", v, g, type(e).__name__)
    html = ["<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><meta name=robots content=noindex><title>Prova Ahia</title><body style='font-family:system-ui;max-width:640px;margin:0 auto;padding:16px'><h2>Come suona Ahia?</h2>"]
    for v in VOCI:
        html.append(f"<h3>{v.capitalize()}</h3>")
        for i, g in enumerate(GRAFIE):
            if (OUT / f"{v}-{i}.mp3").exists():
                html.append(f"<p>Scritto «{g}»<br><audio controls preload=none src='voci/girrr/{v}-{i}.mp3?v=2' style='width:100%'></audio></p>")
    (R.parent / "lab" / "girrr.html").write_text("".join(html), encoding="utf-8")
asyncio.run(main())
