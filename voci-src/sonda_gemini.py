import os, time
from google import genai
from google.genai import types
cl = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
for mod in ["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts", "gemini-3.1-flash-tts-preview"]:
    for n in range(4):
        t = time.time()
        try:
            r = cl.models.generate_content(model=mod, contents="Dì in italiano: buonasera a tutti.", config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon")))))
            print(mod, n, "ok", round(time.time() - t, 1), "s", flush=True)
        except Exception as e:
            print(mod, n, "ERRORE", round(time.time() - t, 1), "s", str(e)[:900], flush=True)
