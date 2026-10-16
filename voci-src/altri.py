"""Altri generatori gratuiti: Kokoro e Piper (modelli aperti, senza chiavi)."""
import json, pathlib, subprocess, sys, traceback
R = pathlib.Path(__file__).parent
OUT = R.parent / "lab" / "voci"; OUT.mkdir(parents=True, exist_ok=True)
TMP = R / "tmp2"; TMP.mkdir(exist_ok=True)
rows = json.load(open(R / "radio.json", encoding="utf-8"))
elenco = []

def mp3(wav, nome):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1", "-b:a", "64k", str(OUT / nome)], check=True)

# ---------- Kokoro ----------
def kokoro():
    import numpy as np, soundfile as sf
    from kokoro import KPipeline
    pipes = {}
    def parla(lang, voce, testo):
        p = pipes.setdefault(lang, KPipeline(lang_code=lang))
        return np.concatenate([np.asarray(a) for _, _, a in p(testo, voice=voce) if a is not None])
    VOCI = {"i": ["if_sara", "im_nicola"], "b": ["bm_george", "bm_fable", "bm_lewis", "bf_emma", "bf_isabella"], "a": ["af_heart", "af_bella", "am_adam", "am_michael"]}
    for lang, voci in VOCI.items():
        campo = "it" if lang == "i" else "en"
        testo = " ".join(r[campo] for r in rows[:3])
        for v in voci:
            try:
                wav = TMP / f"{v}.wav"; sf.write(wav, parla(lang, v, testo), 24000)
                nome = f"k_{v}.mp3"; mp3(wav, nome)
                elenco.append({"gen": "Kokoro", "lingua": "it" if lang == "i" else "en", "voce": v, "file": nome}); print("ok kokoro", v)
            except Exception:
                print("errore kokoro", v); traceback.print_exc()
    for nome, lang, v1, v2, campo, label in (("k-dialogo-it", "i", "im_nicola", "if_sara", "it", "Kokoro: Nicola e Sara"), ("k-dialogo-en", "b", "bm_george", "bf_emma", "en", "Kokoro: George ed Emma (inglese)")):
        try:
            pezzi = []
            for r in rows:
                pezzi.append(parla(lang, v1 if r["s"] == "Steve" else v2, r[campo]))
                pezzi.append(np.zeros(int(24000 * 0.25)))
            wav = TMP / f"{nome}.wav"; sf.write(wav, np.concatenate(pezzi), 24000); mp3(wav, nome + ".mp3")
            elenco.append({"gen": "Kokoro", "dialogo": True, "label": label, "file": nome + ".mp3"}); print("ok dialogo", nome)
        except Exception:
            print("errore dialogo", nome); traceback.print_exc()

# ---------- Piper ----------
def piper():
    d = TMP / "piper"; d.mkdir(exist_ok=True)
    VOCI = [("it", "it_IT-paola-medium"), ("it", "it_IT-riccardo-x_low"),
            ("en", "en_GB-alan-medium"), ("en", "en_GB-northern_english_male-medium"), ("en", "en_GB-jenny_dioco-medium"), ("en", "en_US-ryan-high"), ("en", "en_US-lessac-high")]
    for lingua, v in VOCI:
        try:
            subprocess.run([sys.executable, "-m", "piper.download_voices", v, "--download-dir", str(d)], check=True)
            testo = " ".join(r[lingua] for r in rows[:3]); wav = TMP / f"{v}.wav"
            subprocess.run([sys.executable, "-m", "piper", "-m", v, "--data-dir", str(d), "-f", str(wav)], input=testo.encode(), check=True)
            nome = f"p_{v}.mp3"; mp3(wav, nome)
            elenco.append({"gen": "Piper", "lingua": lingua, "voce": v, "file": nome}); print("ok piper", v)
        except Exception:
            print("errore piper", v); traceback.print_exc()

for f in (kokoro, piper):
    try: f()
    except Exception: print("errore generale", f.__name__); traceback.print_exc()
json.dump(elenco, open(OUT / "elenco2.json", "w"), ensure_ascii=False)
print("totale", len(elenco))
