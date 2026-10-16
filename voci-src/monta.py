"""Monta la puntata: sigla di apertura (folla, fischio, jingle che scende sotto la voce), voci, sigla di chiusura."""
import sys, pathlib, subprocess, tempfile, numpy as np, scipy.io.wavfile as wf
R = pathlib.Path(__file__).parent; SU = R / "suoni"; SR = 24000
voci_mp3 = pathlib.Path(sys.argv[1]); out_mp3 = pathlib.Path(sys.argv[2])
tmp = pathlib.Path(tempfile.mkdtemp())
def load(f, extra=()):
    w = tmp / "x.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(f), "-ac", "1", "-ar", str(SR), *extra, str(w)], check=True)
    return np.clip(wf.read(w)[1].astype(float) / 32767, -1, 1)
def seg(a, s, d, gain, fin=0.03, fout=0.5):
    x = a[int(s*SR):int((s+d)*SR)].copy(); x = x / np.sqrt((x**2).mean()) * gain
    e = np.ones(len(x)); i = int(fin*SR); o = int(fout*SR); e[:i] = np.linspace(0, 1, i); e[-o:] = np.linspace(1, 0, o); return x * e
def seg_pre(a, s, d, gain, pre=2.0, base=0.10, fin=0.03, fout=0.5):
    """Come seg(), ma con 'pre' secondi di anticipo: la canzone sale piano da 'base' fino al volume pieno proprio dove partiva prima."""
    k = gain / np.sqrt((a[int(s*SR):int((s+d)*SR)]**2).mean())
    x = a[int((s-pre)*SR):int((s+d)*SR)].copy() * k
    e = np.ones(len(x)); n = int(pre*SR)
    e[:n] = base + (1 - base) * np.linspace(0, 1, n) ** 2
    o = int(fout*SR); e[-o:] *= np.linspace(1, 0, o); e[:int(fin*SR)] *= np.linspace(0, 1, int(fin*SR)); return x * e
def mix(parts, total):
    out = np.zeros(int(SR*total))
    for off, a in parts:
        i = int(SR*off); out[i:i+len(a)] += a[:len(out)-i]
    return out
def duck(x, t0, t1, l): x = x.copy(); x[int(t0*SR):int(t1*SR)] *= l; return x
J = load(SU / "jingle-sport.mp3"); C = load(SU / "folla-stadio.mp3"); W = load(SU / "fischio-arbitro.mp3", ("-t", "0.9"))
W = W / np.abs(W).max() * 0.95; W[-int(0.15*SR):] *= np.linspace(1, 0, int(0.15*SR))
V = load(voci_mp3)
PRE = 2.0; t_j = 1.35 + PRE; t_voce = t_j + 7.0
JA = seg_pre(J, 49.5, 12.2, 0.19, PRE, 0.10, 0.15, 0.05); bed = seg(C, 8.0, 6.0, 0.12, 0.3, 2.5)
# la musica scende già quando parte il primo presentatore e poi si dissolve piano piano
tt = np.arange(len(JA)) / SR; tv = t_voce - t_j + PRE
env = np.interp(tt, [0, tv - 0.5, tv + 0.4, tt[-1]], [1.0, 1.0, 0.38, 0.0])
JA = JA * env
ap = mix([(0.0, duck(bed, 1.3, 6.0 + PRE, 0.5)), (0.3, W*0.9), (t_j - PRE, JA)], t_voce + 11.0)
jc = seg_pre(J, 126.4, 9.8, 0.19, PRE, 0.10, 0.4, 0.2); bed2 = seg(C, 7.5, 6.5, 0.13, 0.8, 2.2)
ch = mix([(0.0, duck(bed2, 2.2, 6.5, 0.5)), (0.2, W*0.85), (1.0, W*0.85), (1.8, W), (2.5, jc)], 12.4 + PRE)
tot = np.zeros(int(SR*(t_voce + len(V)/SR + 0.6 + len(ch)/SR))); tot[:len(ap)] += ap
i = int(t_voce*SR); tot[i:i+len(V)] += V
j = i + len(V) + int(0.5*SR); tot[j:j+len(ch)] += ch[:len(tot)-j]
tot = np.tanh(tot*1.05); tot = tot / np.abs(tot).max() * 0.92; tot[-int(SR*0.15):] *= np.linspace(1, 0, int(SR*0.15))
wf.write(tmp / "p.wav", SR, (tot*32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "p.wav"), "-ac", "1", "-ar", "24000", "-b:a", "64k", "-codec:a", "libmp3lame", "-write_xing", "0", "-id3v2_version", "0", "-write_id3v1", "0", str(out_mp3)], check=True)
print("montata", round(len(tot)/SR, 1), "s")
