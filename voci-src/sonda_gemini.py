import os, time, wave, io
from google import genai
from google.genai import types
cl = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
T = "Che mazzata! Apo Team vola a ottanta punti e il resto della lega guarda da lontano! Ahia!"
VAR = {
 "senza_stile": T,
 "dì_con": "Dì con grande entusiasmo, come un telecronista: " + T,
 "lungo_attuale": "Sei un commentatore sportivo italiano, secondo telecronista, ironico e pungente. Leggi il testo seguente al massimo dell'entusiasmo, voce potente e squillante, in italiano perfetto, senza leggere queste istruzioni: " + T,
 "tag": "[excited, shouting] " + T,
 "tag_it": "[urlando, entusiasta] " + T,
}
def dur(pcm): return len(pcm) / 2 / 24000
for k, c in VAR.items():
    for n in range(2):
        t = time.time()
        try:
            r = cl.models.generate_content(model="gemini-3.8-flash-tts", contents=c, config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon")))))
            pcm = r.candidates[0].content.parts[0].inline_data.data
            print(k, n, "durata audio", round(dur(pcm), 1), "s (testo", len(T), "caratteri)", flush=True)
            open(f"voci-src/_t_{k}_{n}.pcm", "wb").write(pcm)
        except Exception as e:
            print(k, n, "ERRORE", str(e)[:200].replace("\n", " "), flush=True)
