import os, wave
from google import genai
from google.genai import types
cl = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
from faster_whisper import WhisperModel
wm = WhisperModel("small", device="cpu", compute_type="int8")
def gen(contents, si=None):
    cfg = dict(response_modalities=["AUDIO"], speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon"))))
    if si: cfg["system_instruction"] = si
    r = cl.models.generate_content(model="gemini-3.8-flash-tts", contents=contents, config=types.GenerateContentConfig(**cfg))
    return r.candidates[0].content.parts[0].inline_data.data
def tr(pcm, k):
    import numpy as np
    from scipy.signal import resample_poly
    x = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
    x = resample_poly(x, 2, 3).astype(np.float32)
    seg, _ = wm.transcribe(x, language="it"); return " ".join(s.text.strip() for s in seg)
CASI = [
 ("tag_ride", "[laughing] Ah ah ah, scusate, non ce la faccio!", None),
 ("tag_sussurro", "[whispering] Lo dirò sottovoce: semi ufficiale, prendetelo con le pinze!", None),
 ("tag_urlo", "[shouting] Che mazzata! Apo Team vola a ottanta punti!", None),
]
for k, c, si in CASI:
    try:
        pcm = gen(c, si)
        print(k, round(len(pcm) / 48000, 1), "s | testo:", c, "|| TRASCRITTO:", tr(pcm, k), flush=True)
    except Exception as e:
        print(k, "ERRORE", str(e)[:300].replace("\n", " "), flush=True)
