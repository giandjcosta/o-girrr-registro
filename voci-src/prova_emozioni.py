import os, sys, time, wave, subprocess, pathlib
R = pathlib.Path(__file__).parent; sys.path.insert(0, str(R))
from gtrim import taglia_coda
OUT = R.parent / "lab" / "voci" / "emozioni"; OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob("*"): f.unlink()
from google import genai
from google.genai import types
cl = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
CASI = [
 ("Urlo da gol", [("A normale", "Che mazzata! Apo Team vola a ottanta punti e il resto della lega guarda da lontano!"), ("B maiuscolo", "CHE MAZZATA!!! APO TEAM VOLA A OTTANTA PUNTI e il resto della lega guarda da lontano!!!"), ("C ripetuto", "Che mazzata! Che mazzata! Apo Team vola, vola a ottanta punti!")]),
 ("Risata", [("A normale", "Ah ah ah, scusate, non ce la faccio!"), ("B lunga", "Ahahahahah! Scusate... ahahah... non ce la faccio!")]),
 ("Sospiro", [("A normale", "Eh... che dolore. Poveretto."), ("B lungo", "Ehhhh... che dolore... Poveretto... mamma mia.")]),
 ("Stupore", [("A normale", "Ma davvero?! Non ci credo!"), ("B drammatico", "Ma... davvero?! No! Non ci posso credere!")]),
 ("Sussurro", [("A normale", "Lo dirò sottovoce: semi ufficiale, prendetelo con le pinze!"), ("B puntini", "Lo dirò... sottovoce... semi ufficiale... prendetelo con le pinze...")]),
]
def clip(testo, nome):
    for t in range(2):
        try:
            r = cl.models.generate_content(model="gemini-3.8-flash-tts", contents=testo, config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon")))))
            pcm = taglia_coda(r.candidates[0].content.parts[0].inline_data.data)
            w = OUT / (nome + ".wav")
            with wave.open(str(w), "wb") as o: o.setnchannels(1); o.setsampwidth(2); o.setframerate(24000); o.writeframes(pcm)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(w), "-b:a", "64k", str(OUT / (nome + ".mp3"))], check=True); w.unlink(); return True
        except Exception as e:
            import traceback; print("errore", nome, type(e).__name__, str(e)[:200], flush=True); traceback.print_exc(limit=3); time.sleep(5)
    return False
h = ["<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><meta name=robots content=noindex><title>Prova emozioni</title><body style='font-family:system-ui;max-width:640px;margin:0 auto;padding:16px'><h2>Emozioni: come si scrive il testo</h2><p>Stessa voce (Charon), testi diversi. Fine clip tagliata senza rumore.</p>"]
for i, (nome, vs) in enumerate(CASI):
    h.append(f"<h3>{nome}</h3>")
    for j, (lab, tx) in enumerate(vs):
        fn = f"e{i}{j}"; ok = clip(tx, fn)
        h.append(f"<p><b>{lab}</b> — <i>{tx}</i>" + (f"<br><audio controls preload=none src='voci/emozioni/{fn}.mp3?v=1' style='width:100%'></audio>" if ok else " — non riuscita") + "</p>")
        time.sleep(4)
(R.parent / "lab" / "emozioni.html").write_text("".join(h), encoding="utf-8")
