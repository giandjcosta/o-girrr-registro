import os, time
from google import genai
from google.genai import types
cl = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
for mod in ["gemini-3.8-flash-tts"]:
    for n in range(14):
        t = time.time()
        try:
            r = cl.models.generate_content(model=mod, contents="Dì in italiano: buonasera a tutti.", config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon")))))
            print(mod, n, "ok", round(time.time() - t, 1), "s", flush=True)
        except Exception as e:
            if "429" in str(e): print(mod, n, "ERRORE", str(e)[:260].replace("\n"," "), flush=True); break
            print(mod, n, "ERRORE", round(time.time() - t, 1), "s", str(e)[:260], flush=True)
