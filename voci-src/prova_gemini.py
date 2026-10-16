import os, sys, time, wave, subprocess, pathlib, json
R = pathlib.Path(__file__).parent
TAG = os.environ.get("MODELLO", "").replace(".", "-") or "auto"
OUT = R.parent / "lab" / "voci" / ("gemini-" + TAG); OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob("*"): f.unlink()
key = os.environ.get("GEMINI_API_KEY", "")
if not key: print("Manca GEMINI_API_KEY"); sys.exit(1)
from google import genai
from google.genai import types
cl = genai.Client(api_key=key)
modelli = [m.name for m in cl.models.list() if "tts" in m.name.lower()]
print("Modelli TTS:", modelli)
pref = [m for m in modelli if "flash" in m and "lite" not in m] or modelli
MODELLO = os.environ.get("MODELLO") or (pref[0].split("/")[-1] if pref else "gemini-2.5-flash-preview-tts")
print("Uso:", MODELLO)
STILE = {
 "urlo": "Sei un telecronista radiofonico italiano al massimo dell'entusiasmo, voce potente e squillante, ritmo veloce, come Fabio Caressa: ",
 "norm": "Sei un conduttore radiofonico italiano, voce calda e professionale, ritmo vivace ma chiaro: ",
 "sus": "Sussurra in italiano, in tono complice e confidenziale, come se rivelassi un segreto: ",
}
PROVE = [
 ("Apertura", "norm", "Buonasera a tutti e benvenuti a Radio Giirrr, la radio ufficiale della Lega! Io sono Beppe Rovesciata, e questa sera abbiamo davvero tanto da raccontarvi.", ["Charon", "Orus", "Fenrir"]),
 ("Gol", "urlo", "Che mazzata! Apo Team vola a ottanta punti e il resto della lega guarda da lontano! Ahia!", ["Fenrir", "Puck", "Algenib"]),
 ("Inviata", "norm", "Qui Giulia Cronaca, dalla sala stampa. Il presidente la voleva al quinto posto, e oggi è primo in classifica.", ["Kore", "Aoede", "Leda"]),
 ("Mercato", "sus", "Lo dirò sottovoce: semi ufficiale, prendetelo con le pinze! Raspadori sarebbe infortunato.", ["Enceladus", "Charon", "Orus"]),
]
def wav(path, pcm):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
res = []
for nome, st, testo, voci in PROVE:
    for v in voci:
        fn = f"{nome.lower()}-{v.lower()}"
        ok = False
        for t in range(5):
            try:
                r = cl.models.generate_content(model=MODELLO, contents=STILE[st] + testo,
                    config=types.GenerateContentConfig(response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=v)))))
                pcm = r.candidates[0].content.parts[0].inline_data.data
                wav(OUT / (fn + ".wav"), pcm)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(OUT / (fn + ".wav")), "-b:a", "64k", str(OUT / (fn + ".mp3"))], check=True)
                (OUT / (fn + ".wav")).unlink(); ok = True; break
            except Exception as e:
                print("errore", fn, str(e)[:200]); time.sleep(12 * (t + 1))
        res.append((nome, v, testo, fn, ok)); time.sleep(8)
h = ["<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><meta name=robots content=noindex><title>Prova Gemini</title><body style='font-family:system-ui;max-width:640px;margin:0 auto;padding:16px'><h2>Voci Gemini</h2><p>Modello: " + MODELLO + "</p>"]
cur = None
for nome, v, testo, fn, ok in res:
    if nome != cur: h.append(f"<h3>{nome}</h3><p style='color:#555'>{testo}</p>"); cur = nome
    h.append(f"<p><b>{v}</b>" + (f"<br><audio controls preload=none src='voci/gemini-{TAG}/{fn}.mp3?v=1' style='width:100%'></audio>" if ok else " — non riuscita") + "</p>")
(R.parent / "lab" / f"gemini-{TAG}.html").write_text("".join(h), encoding="utf-8")
