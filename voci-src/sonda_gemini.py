import os, json, time, base64, urllib.request
import google.auth.transport.requests
from google.oauth2 import service_account
cred = service_account.Credentials.from_service_account_info(json.loads(os.environ["GOOGLE_TTS_JSON"]), scopes=["https://www.googleapis.com/auth/cloud-platform"])
cred.refresh(google.auth.transport.requests.Request())
for mod in ["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts", "gemini-2.5-flash-tts"]:
    body = json.dumps({"input": {"prompt": "Leggi in italiano, come un telecronista radiofonico al massimo dell'entusiasmo.", "text": "Che mazzata! Apo Team vola a ottanta punti! Ahia!"},
        "voice": {"languageCode": "it-IT", "name": "Charon", "modelName": mod}, "audioConfig": {"audioEncoding": "MP3"}}).encode()
    t = time.time()
    try:
        rq = urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize", body, {"Content-Type": "application/json", "Authorization": "Bearer " + cred.token})
        d = json.load(urllib.request.urlopen(rq, timeout=90))
        print(mod, "OK", round(time.time() - t, 1), "s", len(d["audioContent"]), flush=True)
    except Exception as e:
        print(mod, "ERRORE", round(time.time() - t, 1), "s", e, (e.read().decode()[:500] if hasattr(e, "read") else ""), flush=True)
