import os, time
from google import genai
from google.genai import types
cl = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
for n in range(3):
    t = time.time()
    try:
        r = cl.models.generate_content(model="gemini-3.8-flash-tts", contents="Leggi in italiano, come un telecronista radiofonico al massimo dell'entusiasmo: Che mazzata! Apo Team vola a ottanta punti! Ahia!", config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon")))))
        print("OK", n, round(time.time() - t, 1), "s", len(r.candidates[0].content.parts[0].inline_data.data), flush=True)
    except Exception as e:
        print("ERRORE", n, round(time.time() - t, 1), "s", str(e)[:300].replace("\n", " "), flush=True)
