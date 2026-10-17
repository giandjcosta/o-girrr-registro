import sys
"""Puntata di prova della Radio con quattro voci: conduttore, commentatore, inviata e Ciro (mercato)."""
import asyncio, json, pathlib
import edge_tts
import edge_tts.communicate as _ec
# le voci multilingue a volte "sentono" una lingua sbagliata nelle frasi corte: diciamo loro che il testo è italiano
LANG_IT = [False]  # l'etichetta della lingua fa rifiutare le voci multilingue: lasciata spenta
_mk0 = _ec.mkssml
def _mk(tc, t):
    if LANG_IT[0] and "Multilingual" in tc.voice:
        if isinstance(t, bytes): t = t.decode("utf-8")
        t = f"<lang xml:lang='it-IT'>{t}</lang>"
    return _mk0(tc, t)
_ec.mkssml = _mk
R = pathlib.Path(__file__).parent
OUT = R.parent / "lab" / "voci"; OUT.mkdir(parents=True, exist_ok=True)
D = json.load(open(R / "dati.json", encoding="utf-8"))
NOMI = json.load(open(R / "nomi.json", encoding="utf-8"))
SUF = sys.argv[2] if len(sys.argv)>2 else ""
VOCI = {"B": "it-IT-DiegoNeural", "G": (sys.argv[1] if len(sys.argv)>1 else "en-US-AndrewMultilingualNeural"), "S": "it-IT-ElsaNeural", "C": "it-IT-GiuseppeMultilingualNeural"}
RUOLO = {"B": "Conduttore", "G": "Commentatore", "S": "Inviata speciale", "C": "Mercato"}
def f(x):
    x = float(x)
    return str(int(x)) if x == int(x) else str(x).replace(".", ",")
NUM = ["zero","uno","due","tre","quattro","cinque","sei","sette","otto","nove","dieci"]
PRON = {"Girrr": "Girr", "Champions Cup": "Cèmpions Càp", "AFA SELECCION": "Afa Selession", "WOA": "Uoa"}
ORD = {1:"prima",2:"seconda",3:"terza",4:"quarta",5:"quinta",6:"sesta",7:"settima",8:"ottava",9:"nona",10:"decima"}
a = D["aw"][-1]; T = D["tab"]
DER = [("Grodah","WOA"),("stif dc","Real Madrink"),("Oranje VC","AFA SELECCION"),("Apo team","The Blue brothers"),("Mariana Coneja","Atletico ma non troppo")]
def derby(m): return any({x.lower(), y.lower()} == {m[0].lower(), m[1].lower()} for x, y in DER)
g = D["cal"][0]["m"]; der = next((m for m in g if derby(m)), g[0])
import random, copione
MERC = json.load(open(R / "mercato.json", encoding="utf-8")) if (R / "mercato.json").exists() else {}
L = copione.build(D, random.Random(D["aw"][-1]["n"] * 7919), MERC, NOMI)
import re, os, wave, subprocess
ACC = {"rovesciata": "rovesciàta", "guardati": "guardàti", "riguardati": "riguardàti", "imparati": "imparàti", "risultati": "risultàti", "ancora": "ancòra",
       "subito": "sùbito", "favorito": "favorìto", "campionato": "campionàto", "mercato": "mercàto", "rovinato": "rovinàto", "infortunato": "infortunàto",
       "sparito": "sparìto", "riuscito": "riuscìto", "arrivato": "arrivàto", "cambiato": "cambiàto", "passato": "passàto", "tornato": "tornàto", "stato": "stàto", "guardato": "guardàto"}
def accenta(t):
    """Segna l'accento sulle parole che alcune voci leggono col suono sbagliato (es. Rovescia/Rovesciata, Guàrdati/guardàti)."""
    import re as _re
    def sost(m):
        w = m.group(0); n = ACC.get(w.lower())
        if not n: return w
        return n[:1].upper() + n[1:] if w[:1].isupper() else n
    return _re.sub(r"[A-Za-zÀ-ÿ]+", sost, t)
GKEY = os.environ.get("GEMINI_API_KEY", "")
GMOD = os.environ.get("MODELLO", "") or "gemini-3.8-flash-tts"
GVOCI = {"B": "Charon", "G": "Orus", "S": "Aoede", "C": "Fenrir"}
GRUOLO = {"B": "un conduttore radiofonico italiano, voce calda e professionale", "G": "un commentatore sportivo italiano, secondo telecronista, ironico e pungente",
          "S": "un'inviata giornalista italiana, voce chiara e vivace", "C": "un esperto di calciomercato italiano, tono da cronista di mercato"}
GTAG = {"urlo": "[shouting, excited] ", "sus": "[whispering] ", "ride": "[laughing] ", "sospiro": "[sighing] ", "stupore": "[surprised] ", "sarcasmo": "[sarcastic] ", "commosso": "[emotional, warm] ", "entusiasmo": "[enthusiastic] "}
_gcl = None
GSTOP = [False, False]
MOTORE = {}
def emozione(st, t):
    """Le emozioni passano dal modo in cui è scritto il testo (le etichette tra parentesi venivano lette)."""
    import re as _re
    if st == "urlo":
        fr = _re.split(r"(?<=[.!?])\s+", t.strip())
        for i in range(min(2, len(fr))):
            fr[i] = _re.sub(r"[.!?]+$", "", fr[i]).upper() + "!!!"
        return " ".join(fr)
    if st == "ride":
        m = _re.match(r"^(Ah ah ah|Ah ah),?\s*(.*)$", t)
        if m:
            resto = m.group(2)
            resto = resto[:1].upper() + resto[1:]
            return "Ahahahahah! " + resto.replace(", ", "... ahahah... ", 1)
        return t
    if st == "stupore":
        mp = {"Ma davvero?!": "Ma... davvero?! No!", "Non ci credo!": "No! Non ci posso credere!", "Cosa?! Ma com'è possibile?!": "Cosa?! Ma... com'è possibile?! No!"}
        return mp.get(t.strip(), t)
    return t
def gemini_uno(k, tx, fn, stile):
    global _gcl
    from google import genai
    from google.genai import types
    if _gcl is None: _gcl = genai.Client(api_key=GKEY)
    st = stile if isinstance(stile, str) or stile is None else None
    istr = ""
    tx = emozione(st, tx)
    r = _gcl.models.generate_content(model=GMOD, contents=istr + tx, config=types.GenerateContentConfig(response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=GVOCI[k])))))
    pcm = r.candidates[0].content.parts[0].inline_data.data
    from gtrim import taglia_coda, rifinisci
    pcm = rifinisci(taglia_coda(pcm))
    w = fn.with_suffix(".wav")
    with wave.open(str(w), "wb") as o: o.setnchannels(1); o.setsampwidth(2); o.setframerate(24000); o.writeframes(pcm)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(w), "-ar", "24000", "-ac", "1", "-b:a", "48k", "-f", "mp3", "-write_xing", "0", "-id3v2_version", "0", str(fn)], check=True)
    w.unlink()
CHIRP = {"B": "Charon", "G": "Orus", "S": "Aoede", "C": "Fenrir"}
_ccred = [None]
def chirp_uno(k, tx, fn, stile):
    import json, base64, urllib.request
    if _ccred[0] is None:
        import google.auth.transport.requests
        from google.oauth2 import service_account
        sa = os.environ.get("GOOGLE_TTS_JSON", "")
        if not sa: raise RuntimeError("manca GOOGLE_TTS_JSON")
        c = service_account.Credentials.from_service_account_info(json.loads(sa), scopes=["https://www.googleapis.com/auth/cloud-platform"])
        _ccred[0] = (c, google.auth.transport.requests.Request())
    c, rq_ = _ccred[0]
    if not c.valid: c.refresh(rq_)
    st = stile if isinstance(stile, str) or stile is None else None
    tx = emozione(st, tx)
    body = json.dumps({"input": {"text": tx}, "voice": {"languageCode": "it-IT", "name": "it-IT-Chirp3-HD-" + CHIRP[k]}, "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000, "speakingRate": 1.05}}).encode()
    rq = urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize", body, {"Content-Type": "application/json", "Authorization": "Bearer " + c.token})
    raw = base64.b64decode(json.load(urllib.request.urlopen(rq, timeout=60))["audioContent"])
    import io
    with wave.open(io.BytesIO(raw)) as wr: pcm = wr.readframes(wr.getnframes())
    from gtrim import rifinisci
    pcm = rifinisci(pcm)
    w = fn.with_suffix(".wav")
    with wave.open(str(w), "wb") as o: o.setnchannels(1); o.setsampwidth(2); o.setframerate(24000); o.writeframes(pcm)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(w), "-ar", "24000", "-ac", "1", "-b:a", "48k", "-f", "mp3", "-write_xing", "0", "-id3v2_version", "0", str(fn)], check=True)
    w.unlink()
STILI = {"urlo": dict(rate="+12%", pitch="+3Hz", volume="+6%"), "sus": dict(rate="-4%", pitch="-3Hz", volume="-10%"), None: dict(rate="+6%")}
async def uno(voce, tx, fn, stile):
    kw = STILI.get(stile, {}) if isinstance(stile, (str, type(None))) else {"rate": stile}
    c = edge_tts.Communicate(tx, voce, **kw)
    await c.save(str(fn))

async def parla(k, testo, fn, i, stile=None):
    """Prova la riga intera; se la voce non risponde la legge a frasi; come ultima scelta usa Isabella."""
    testo = testo.replace("«", "").replace("»", "")
    for a_, b_ in PRON.items(): testo = testo.replace(a_, b_)
    testo = accenta(testo)
    for nome, fun, ok_ in (("gemini", gemini_uno, bool(GKEY) and not GSTOP[0]), ("chirp", chirp_uno, bool(os.environ.get("GOOGLE_TTS_JSON")) and not GSTOP[1])):
        if not ok_: continue
        for n in range(6 if nome == "gemini" else 2):
            try:
                await asyncio.get_event_loop().run_in_executor(None, fun, k, testo, fn, stile)
                MOTORE[nome] = MOTORE.get(nome, 0) + 1
                await asyncio.sleep(3 if nome == "gemini" else 0.3); return
            except Exception as e:
                print("riga", i, nome, "tentativo", n, "fallito:", str(e).replace("\n", " ")[:1200], flush=True)
                import re as _r
                mm = _r.search(r"retry in ([\d.]+)(h|m|s)", str(e))
                if nome == "gemini" and "429" in str(e) and ("PerDay" in str(e) or "per_day" in str(e) or (mm and (mm.group(2) == "h" or (mm.group(2) == "m" and float(mm.group(1)) > 3)))):
                    GSTOP[0] = True; break
                if nome == "gemini" and "429" in str(e) and not mm:
                    await asyncio.sleep(25 * (n + 1)); continue
                if nome == "gemini" and "402" in str(e): GSTOP[0] = True; break
                await asyncio.sleep((float(mm.group(1)) + 2 if (mm and mm.group(2) == "s") else 5 * (n + 1)))
        else:
            if nome == "chirp": GSTOP[1] = True
        print("riga", i, nome, "non disponibile, passo al successivo", flush=True)
    MOTORE["edge"] = MOTORE.get("edge", 0) + 1
    print("riga", i, "uso edge-tts", flush=True)
    pulito = testo.replace("«", "").replace("»", "").replace("ª", "a").replace("°", "")
    for n, (tx, st_, lg) in enumerate([(testo, stile, False)] * 5 + [(pulito, "base", False)] * 3):
        LANG_IT[0] = lg
        try:
            await uno(VOCI[k], tx, fn, st_); return
        except Exception as e:
            print("riga", i, VOCI[k], "intera, tentativo", n, "fallito:", type(e).__name__); await asyncio.sleep(1.5)
    frasi = [x for x in re.split(r"(?<=[.:!?])\s+", pulito) if x.strip()]
    pezzi = []
    for j, fr in enumerate(frasi):
        tmp = fn.with_suffix(f".{j}.part")
        try:
            for _t in range(4):
                LANG_IT[0] = False
                try: await uno(VOCI[k], fr, tmp, "base"); break
                except Exception: await asyncio.sleep(1.5)
            else: raise RuntimeError("sempre fallita")
        except Exception as e:
            print("riga", i, "frase", j, VOCI[k], "fallita, uso Isabella:", fr[:50])
            await uno("it-IT-IsabellaNeural", fr, tmp, "base")
        pezzi.append(tmp)
    with open(fn, "wb") as o:
        for q in pezzi: o.write(q.read_bytes()); q.unlink()

def scegli_modello():
    """Prova una richiesta minuscola: usa il modello preferito, altrimenti l'altro; se nessuno risponde restituisce False."""
    global GMOD, _gcl
    from google import genai
    from google.genai import types
    ordine = [GMOD] + [m for m in ("gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts") if m != GMOD]
    cl = genai.Client(api_key=GKEY)
    for m in ordine:
        try:
            cl.models.generate_content(model=m, contents="Ciao.", config=types.GenerateContentConfig(response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon")))))
            GMOD = m; print("modello scelto:", m, flush=True); return True
        except Exception as e:
            print("modello", m, "non disponibile:", str(e).replace("\n", " ")[:300], flush=True)
    return False
SOLO = os.environ.get("SOLO_GEMINI", "") == "1"
async def main():
    ok_g = bool(GKEY) and scegli_modello()
    if not ok_g:
        GSTOP[0] = True
        if SOLO: print("SOLO_GEMINI: Gemini non disponibile, non pubblico nulla", flush=True); sys.exit(3)
    parti = []
    for i, riga in enumerate(L):
        k, t = riga[0], riga[1]; st = riga[2] if len(riga) > 2 else None
        fn = OUT / f"_p{i}.tmp"
        await parla(k, t, fn, i, st); parti.append(fn)
    if SOLO and (MOTORE.get("chirp") or MOTORE.get("edge")):
        print("SOLO_GEMINI: alcune battute non sono Gemini, non pubblico nulla:", MOTORE, flush=True); sys.exit(3)
    with open(R / "_voci.mp3", "wb") as o:
        for p in parti: o.write(p.read_bytes()); p.unlink()
    json.dump([{"chi": NOMI[k], "ruolo": RUOLO[k], "testo": t} for k, t, *_ in L], open(OUT / f"puntata{SUF}.json", "w"), ensure_ascii=False)
    print("ok", len(L), "| motori usati:", MOTORE)
asyncio.run(main())
