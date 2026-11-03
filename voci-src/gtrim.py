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
    # cerco il primo silenzio LUNGO (almeno 160 ms): le pause brevi dentro la parola
    # (la chiusura di una "t" in "mazzata") non sono la fine e non vanno tagliate.
    minimo = 8
    basso = zona < 0.01
    inizio = None
    i = 0
    while i < len(basso):
        if basso[i]:
            j = i
            while j < len(basso) and basso[j]: j += 1
            if j - i >= minimo or j == len(basso):
                inizio = i; break
            i = j
        else: i += 1
    if inizio is None: return _scoppio_breve(pcm, x, rms, fr)
    # silenzio lungo nella zona: tutto quello che segue è lo scoppio
    ultimo = len(rms) - fin + inizio
    # se dopo il primo silenzio della zona c'è parlato vero (non una coda corta), non taglio
    resto = rms[ultimo:]
    if np.mean(resto > 0.02) > 0.5 and len(resto) > int(0.45 / 0.02): return pcm
    fine = max(int(0.1 * SR), ultimo * fr)
    return _scoppio_breve(pcm[: fine * 2], x[: fine], rms[: fine // fr], fr)

def _scoppio_breve(pcm, x, rms, fr):
    """Il fruscio "da televisore senza canale" (puntata 6, dopo «Si parte!»): dopo una pausa breve (almeno 60 ms, troppo corta
    per il taglio sopra) arriva uno scoppio di rumore a banda larga di 100-300 ms, poi più niente. Si riconosce dallo spettro
    piatto (la voce ha l'energia concentrata in poche frequenze): si taglia dalla pausa in poi."""
    fin = min(len(rms), int(0.6 / 0.02))
    zona = rms[-fin:]
    i = len(zona) - 1
    while i >= 0 and zona[i] < 0.02: i -= 1          # coda già silenziosa
    if i < 0: return pcm
    j = i
    while j >= 0 and zona[j] >= 0.01: j -= 1          # lo scoppio, all'indietro fino alla pausa
    durata = i - j
    if j < 3 or not (2 <= durata <= 15): return pcm   # 40-300 ms, e prima ci deve essere qualcosa
    k = j
    while k >= 0 and zona[k] < 0.01: k -= 1
    if j - k < 3: return pcm                          # pausa prima dello scoppio di almeno 60 ms
    a = (len(rms) - fin + j + 1) * fr; b = (len(rms) - fin + i + 1) * fr
    w = x[a:b]
    S = np.abs(np.fft.rfft(w * np.hanning(len(w)))) + 1e-9
    piatto = np.exp(np.mean(np.log(S))) / np.mean(S)
    if piatto < 0.4: return pcm                       # è voce, non rumore
    taglio = (len(rms) - fin + k + 2) * fr            # 20 ms dopo la fine della voce
    return pcm[: max(int(0.1 * SR), taglio) * 2]

def rifinisci(pcm: bytes) -> bytes:
    """Transizione morbida tra una voce e l'altra: via il rumore in testa, dissolvenze brevi, un respiro di silenzio in coda."""
    x = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
    if len(x) < SR // 2: return pcm
    x = x - np.mean(x)
    fr = int(0.01 * SR); n = len(x) // fr
    rms = np.array([np.sqrt(np.mean(x[i * fr:(i + 1) * fr] ** 2)) for i in range(n)])
    # inizio: salto i primi frame sotto soglia, tengo 20 ms di margine
    voce = np.where(rms > 0.004)[0]
    ini = max(0, (voce[0] - 2) * fr) if len(voce) else 0
    # fine: ultimo frame con voce, 60 ms di margine
    fin = min(len(x), (voce[-1] + 10) * fr) if len(voce) else len(x)
    x = x[ini:fin].copy()
    a = int(0.012 * SR); b = int(0.07 * SR)
    x[:a] *= np.linspace(0, 1, a) ** 2
    x[-b:] *= np.linspace(1, 0, b) ** 2
    x = np.concatenate([x, np.zeros(int(0.3 * SR), dtype=np.float32)])
    return (np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()
