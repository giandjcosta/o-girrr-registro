"""Utilità Gemini TTS: taglia lo scoppio di rumore che il modello mette alla fine di ogni clip."""
import numpy as np
SR = 24000
def taglia_coda(pcm: bytes) -> bytes:
    x = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
    fr = int(0.02 * SR); n = len(x) // fr
    if n < 20: return pcm
    rms = np.array([np.sqrt(np.mean(x[i * fr:(i + 1) * fr] ** 2)) for i in range(n)])
    fin = int(0.6 / 0.02)            # guardo gli ultimi 0.6 secondi
    zona = rms[-fin:]
    sil = np.where(zona < 0.01)[0]
    if len(sil) == 0: return pcm
    # ultimo silenzio nella zona: tutto quello che segue è lo scoppio
    ultimo = len(rms) - fin + sil[0]
    # se dopo il primo silenzio della zona c'è parlato vero (non una coda corta), non taglio
    resto = rms[ultimo:]
    if np.mean(resto > 0.02) > 0.5 and len(resto) > int(0.45 / 0.02): return pcm
    fine = max(int(0.1 * SR), ultimo * fr)
    return pcm[: fine * 2]
