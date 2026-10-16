import os
from google import genai
from google.genai import types
cl = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
for mod in ["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts"]:
    try:
        r = cl.models.generate_content(model=mod, contents="Ciao.", config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon")))))
        print(mod, "OK", len(r.candidates[0].content.parts[0].inline_data.data), flush=True)
    except Exception as e:
        print(mod, "ERRORE", str(e).replace("\n", " ")[:2000], flush=True)
