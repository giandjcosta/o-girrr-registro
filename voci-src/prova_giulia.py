import asyncio, edge_tts
V = "de-DE-SeraphinaMultilingualNeural"
FR = ["Ultim'ora: nuovo badge in bacheca!", "Apo team sblocca il traguardo Re della giornata, con 80 punti.", "Una bella soddisfazione!", "Chi non crede in noi può restare a casa.", "Parole pesanti."]
VAR = {"base": lambda t: t, "minuscolo": lambda t: t[0].lower()+t[1:], "puntini": lambda t: t.rstrip("!.")+"...", "senza_punt": lambda t: t.rstrip("!."), "prefisso": lambda t: "Allora, "+t, "virgolette": lambda t: "«"+t+"»", "doppia": lambda t: t+" "+t}
async def main():
    for nome, fn in VAR.items():
        ok = 0
        for t in FR:
            try:
                c = edge_tts.Communicate(fn(t), V); n = 0
                async for ch in c.stream():
                    if ch["type"] == "audio": n += 1
                ok += 1 if n else 0
            except Exception as e:
                print("KO", nome, "|", t[:30], type(e).__name__)
        print("RISULTATO", nome, ok, "su", len(FR))
asyncio.run(main())
