import os, sys, json, base64, urllib.request, pathlib, time
R = pathlib.Path(__file__).parent
OUT = R.parent / "lab" / "voci" / "chirp"; OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob("*"): f.unlink()
key = os.environ.get("GOOGLE_TTS_KEY") or os.environ.get("GEMINI_API_KEY", "")
if not key: print("Manca la chiave"); sys.exit(1)
PROVE = [
 ("Apertura", 1.05, "Buonasera a tutti e benvenuti a Radio Giirrr, la radio ufficiale della Lega! Io sono Beppe Rovesciata, e questa sera abbiamo davvero tanto da raccontarvi.", ["Charon", "Orus", "Fenrir"]),
 ("Gol", 1.15, "Che mazzata! Apo Team vola a ottanta punti e il resto della lega guarda da lontano! Ahia!", ["Fenrir", "Puck", "Orus"]),
 ("Inviata", 1.05, "Qui Giulia Cronaca, dalla sala stampa. Il presidente la voleva al quinto posto, e oggi è primo in classifica.", ["Aoede", "Kore", "Leda"]),
 ("Mercato", 0.92, "Lo dirò sottovoce... semi ufficiale, prendetelo con le pinze! Raspadori sarebbe infortunato.", ["Charon", "Orus", "Fenrir"]),
]
res = []
for nome, rate, testo, voci in PROVE:
    for v in voci:
        fn = f"{nome.lower()}-{v.lower()}"; ok = False
        body = json.dumps({"input": {"text": testo}, "voice": {"languageCode": "it-IT", "name": f"it-IT-Chirp3-HD-{v}"}, "audioConfig": {"audioEncoding": "MP3", "speakingRate": rate}}).encode()
        for t in range(3):
            try:
                rq = urllib.request.Request(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={key}", body, {"Content-Type": "application/json"})
                d = json.load(urllib.request.urlopen(rq, timeout=60))
                (OUT / (fn + ".mp3")).write_bytes(base64.b64decode(d["audioContent"])); ok = True; break
            except Exception as e:
                msg = getattr(e, "read", lambda: b"")().decode()[:400] if hasattr(e, "read") else str(e)
                print("errore", fn, e, msg, flush=True); time.sleep(3)
        res.append((nome, v, testo, fn, ok))
h = ["<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><meta name=robots content=noindex><title>Prova Chirp</title><body style='font-family:system-ui;max-width:640px;margin:0 auto;padding:16px'><h2>Voci Chirp 3 HD</h2>"]
cur = None
for nome, v, testo, fn, ok in res:
    if nome != cur: h.append(f"<h3>{nome}</h3><p style='color:#555'>{testo}</p>"); cur = nome
    h.append(f"<p><b>{v}</b>" + (f"<br><audio controls preload=none src='voci/chirp/{fn}.mp3?v=1' style='width:100%'></audio>" if ok else " — non riuscita") + "</p>")
(R.parent / "lab" / "chirp.html").write_text("".join(h), encoding="utf-8")
