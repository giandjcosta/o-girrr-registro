import os, time, wave
from google import genai
from google.genai import types
cl = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
CASI = [
 ("urlo", "[shouting, excited] Che mazzata! Apo Team vola a ottanta punti e il resto della lega guarda da lontano!"),
 ("ride", "[laughing] Ah ah ah, scusate, non ce la faccio!"),
 ("sospiro", "[sighing] Eh... che dolore. Poveretto."),
 ("stupore", "[surprised] Ma davvero?! Non ci credo!"),
 ("sarcasmo", "[sarcastic] Bravi, eh. Però il vero esame è la prossima settimana."),
 ("commosso", "[emotional, warm] Ragazzi, mi emoziono ancora. Il calcio è anche questo: i ritorni."),
 ("sussurro", "[whispering] Lo dirò sottovoce: semi ufficiale, prendetelo con le pinze!"),
 ("entusiasmo", "[enthusiastic] Grazie Beppe! Qui è un bel caos! Prima notizia: Oranje VC sta superando le aspettative!"),
]
from faster_whisper import WhisperModel
wm = WhisperModel("small", device="cpu", compute_type="int8")
for k, c in CASI:
    try:
        r = cl.models.generate_content(model="gemini-3.8-flash-tts", contents=c, config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon")))))
        pcm = r.candidates[0].content.parts[0].inline_data.data
        fn = f"/tmp/{k}.wav"
        with wave.open(fn, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
        seg, _ = wm.transcribe(fn, language="it")
        print(k, round(len(pcm) / 48000, 1), "s |", c, "|| TRASCRITTO:", " ".join(s.text.strip() for s in seg), flush=True)
    except Exception as e:
        print(k, "ERRORE", str(e)[:200].replace("\n", " "), flush=True)
