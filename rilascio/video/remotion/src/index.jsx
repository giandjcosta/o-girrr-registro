import React, { useEffect, useState } from 'react';
import { registerRoot, Composition, AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, spring, interpolate, Img, delayRender, continueRender, staticFile } from 'remotion';
import FONT from './font.js';

// Video della giornata con Remotion (Claude, 12 novembre 2026). Grafica ufficiale: Campionato rosso con il logo della lega e
// «Girrr Sport Live», Champions Cup azzurra con il logo della coppa e «Cup Girrr Live». Dati veri passati da fuori (inputProps).
const NOMI = { 'The Blue brothers': 'The Blues Brothers' };
const nm = s => NOMI[s] || s;
const CHIARO = '#fbf6ec', ORO = '#ffd166';
const TEMA = { lega: { acc: '#d62839', acc2: '#8e1a2a', logo: 'logo-lega.png', tv: 'tv-lega.png', nome: 'CAMPIONATO' }, coppa: { acc: '#3d93d6', acc2: '#1d5f99', logo: 'logo-coppa.png', tv: 'tv-coppa.png', nome: 'CHAMPIONS CUP' } };
// Righe delle classifiche: primi 3 (oro, argento, bronzo) e ultimo (rosso più scuro di quello della lega) con lo sfondo
// colorato ma trasparente come le altre righe; le altre righe hanno il numero bianco e la banda del colore ufficiale.
const MEDAGLIE = [[255, 209, 102], [223, 230, 243], [231, 164, 106]], ULTIMO = [158, 15, 34];
const rgb = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
const Riga = ({ pos, nome, pt, t, med, ult, s, mossa, conta }) => { const c = ult ? ULTIMO : med;
  return <div style={{ display: 'flex', alignItems: 'center', gap: 16, padding: '11px 18px', borderRadius: 14, background: c ? rgb(c, ult ? .42 : .2) : 'rgba(255,255,255,.08)', borderLeft: `8px solid ${c ? rgb(ult ? [196, 30, 52] : c, 1) : TEMA[t].acc}`, opacity: s, transform: mossa }}>
    <b style={{ font: F(900, 26), color: med && !ult ? rgb(med, 1) : CHIARO, width: 34 }}>{pos}</b><span style={{ font: F(800, 25), color: CHIARO, flex: 1 }}>{nm(nome)}</span><b style={{ font: F(900, 28), color: CHIARO }}>{conta}</b></div>; };
const F = (w, s) => `${w} ${s}px Inter, system-ui, sans-serif`;
const cl = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };

const Sfondo = ({ t }) => <AbsoluteFill style={{ background: `radial-gradient(700px 500px at 85% -5%, ${TEMA[t].acc}55, transparent 60%), radial-gradient(800px 600px at -10% 30%, rgba(61,147,214,.25), transparent 60%), linear-gradient(180deg,#24366e,#1d2a52 45%,#121a38)` }} />;

const Caratteri = () => { const [h] = useState(() => delayRender('caratteri'));
  useEffect(() => { const l = document.createElement('style'); l.textContent = FONT.split('FONT/').join(staticFile('font/')); document.head.appendChild(l);
    document.fonts.load('900 24px Inter').finally(() => continueRender(h)); }, []); return null; };

const Conta = ({ a, da }) => { const f = useCurrentFrame(); return <>{Math.round(interpolate(f, [da, da + 16], [0, a], cl))}</>; };
const Tv = ({ t }) => <Img src={staticFile(TEMA[t].tv)} style={{ position: 'absolute', top: 48, right: 40, width: 190, borderRadius: 6, boxShadow: '0 6px 18px rgba(0,0,0,.35)' }} />;

const Titolo = ({ t, k, tit }) => { const f = useCurrentFrame(), A = TEMA[t].acc;
  return <div style={{ position: 'relative', padding: '150px 56px 0' }}>
    <div style={{ font: F(900, 22), letterSpacing: '.3em', color: A === '#d62839' ? ORO : '#9fd0ff' }}>{k}</div>
    <div style={{ font: F(900, 54), color: CHIARO, marginTop: 6, letterSpacing: '-.01em' }}>{tit}</div>
    <div style={{ height: 12, marginTop: 22, borderRadius: 3, transform: 'skewX(-45deg)', width: `${interpolate(f, [0, 22], [0, 100], cl)}%`, background: `linear-gradient(90deg,${A} 0 14%,${ORO} 14% calc(14% + 12px),#0f1736 calc(14% + 12px) 100%)` }} /></div>; };

const Apertura = ({ n, nc }) => { const f = useCurrentFrame(), { fps } = useVideoConfig(); const s = spring({ frame: f, fps, config: { damping: 9, stiffness: 120 } }), s2 = spring({ frame: f - 14, fps, config: { damping: 10, stiffness: 120 } });
  return <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
    <div style={{ display: 'flex', gap: 34, alignItems: 'center' }}>
      <Img src={staticFile('logo-lega.png')} style={{ width: 210, transform: `scale(${s}) rotate(${(1 - s) * -20}deg)` }} />
      <Img src={staticFile('logo-coppa.png')} style={{ width: 190, transform: `scale(${s2}) rotate(${(1 - s2) * 20}deg)` }} /></div>
    <div style={{ font: F(900, 70), color: CHIARO, marginTop: 50, opacity: interpolate(f, [16, 32], [0, 1], cl) }}>La giornata</div>
    <div style={{ font: F(900, 26), letterSpacing: '.22em', color: ORO, marginTop: 14, opacity: interpolate(f, [26, 42], [0, 1], cl) }}>CAMPIONATO · {n}ª</div>
    <div style={{ font: F(900, 26), letterSpacing: '.22em', color: '#9fd0ff', marginTop: 8, opacity: interpolate(f, [32, 48], [0, 1], cl) }}>CHAMPIONS CUP · {nc}ª</div>
  </AbsoluteFill>; };

const Partita = ({ x, i, t, girone }) => { const f = useCurrentFrame(), { fps } = useVideoConfig(), da = 14 + i * 9, s = spring({ frame: f - da, fps, config: { damping: 12, stiffness: 140 } }), r = x.sc.split('-').map(Number), A = TEMA[t].acc;
  return <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', alignItems: 'center', gap: 14, padding: '20px 22px', borderRadius: 20, background: 'rgba(255,255,255,.09)', borderLeft: `10px solid ${A}`, opacity: s, transform: `translateX(${(1 - s) * 200}px)` }}>
    <b style={{ font: F(800, 25), color: r[0] > r[1] ? ORO : CHIARO }}>{nm(x.a)}</b>
    <span style={{ font: F(900, 48), color: CHIARO, background: 'rgba(0,0,0,.28)', borderRadius: 14, padding: '2px 16px', minWidth: 140, textAlign: 'center' }}><Conta a={r[0]} da={da + 6} /> - <Conta a={r[1]} da={da + 6} /></span>
    <b style={{ font: F(800, 25), textAlign: 'right', color: r[1] > r[0] ? ORO : CHIARO }}>{nm(x.b)}</b>
    {girone && <i style={{ gridColumn: '1 / 4', font: F(800, 15), letterSpacing: '.2em', color: '#9fd0ff', fontStyle: 'normal', marginTop: -6 }}>GIRONE {x.g}</i>}</div>; };

const Risultati = ({ t, n, m }) => <AbsoluteFill><Sfondo t={t} /><Tv t={t} /><Titolo t={t} k={`${TEMA[t].nome} · ${n}ª GIORNATA`} tit="I risultati" />
  <div style={{ position: 'relative', padding: '26px 56px', display: 'flex', flexDirection: 'column', gap: 16 }}>{m.map((x, i) => <Partita key={i} x={x} i={i} t={t} girone={t === 'coppa'} />)}</div></AbsoluteFill>;

const Podio = ({ n, c }) => { const f = useCurrentFrame(), { fps } = useVideoConfig();
  return <AbsoluteFill><Sfondo t="lega" /><Tv t="lega" /><Titolo t="lega" k="CAMPIONATO" tit={`Il podio dopo la ${n}ª`} />
    <div style={{ position: 'absolute', bottom: 120, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: 22 }}>
      {[[c[1], 2, 320, 20, '#dfe6f3'], [c[0], 1, 420, 8, ORO], [c[2], 3, 250, 30, '#e7a46a']].map(([q, pos, h, da, bg]) => { const s = spring({ frame: f - da, fps, config: { damping: 11, stiffness: 90 } });
        return <div key={pos} style={{ width: 190, textAlign: 'center' }}>
          <div style={{ font: F(800, 27), color: CHIARO, opacity: s }}>{nm(q.n)}</div>
          <div style={{ font: F(700, 25), color: ORO, margin: '6px 0 12px', opacity: s }}><Conta a={q.pt} da={da} /> punti</div>
          <div style={{ height: h * s, background: bg, borderRadius: '18px 18px 6px 6px', font: F(900, 84), color: '#1d2a52', paddingTop: 18 }}>{pos}</div></div>; })}</div></AbsoluteFill>; };

const Gironi = ({ nc, gir }) => { const f = useCurrentFrame(), { fps } = useVideoConfig();
  return <AbsoluteFill><Sfondo t="coppa" /><Tv t="coppa" /><Titolo t="coppa" k="CHAMPIONS CUP" tit={`I gironi dopo la ${nc}ª`} />
    <div style={{ position: 'relative', padding: '30px 56px', display: 'flex', flexDirection: 'column', gap: 26 }}>
      {Object.keys(gir).sort().map((g, gi) => <div key={g}><div style={{ font: F(900, 20), letterSpacing: '.25em', color: '#9fd0ff', marginBottom: 10 }}>GIRONE {g}</div>
        {gir[g].map((q, i) => { const s = spring({ frame: f - 10 - gi * 14 - i * 5, fps, config: { damping: 14, stiffness: 150 } });
          return <div key={q.n} style={{ marginBottom: 8 }}><Riga pos={i + 1} nome={q.n} pt={q.pt} t="coppa" ult={i === gir[g].length - 1} s={s} mossa={`translateY(${(1 - s) * 30}px)`} conta={q.pt} /></div>; })}</div>)}</div></AbsoluteFill>; };   /* nessuna regola di qualificazione: non la scriviamo se non è nei dati */

const Prossima = ({ n, big }) => { const f = useCurrentFrame(), { fps } = useVideoConfig(), s = spring({ frame: f - 8, fps, config: { damping: 10, stiffness: 110 } });
  return <AbsoluteFill><Sfondo t="lega" /><Tv t="lega" /><Titolo t="lega" k={`PROSSIMA GIORNATA · ${n + 1}ª`} tit="La partita da non perdere" />
    <div style={{ position: 'relative', margin: '70px 56px 0', padding: '44px 30px', borderRadius: 26, textAlign: 'center', background: 'linear-gradient(120deg,#d62839,#8e1a2a 60%,#141d3d 130%)', transform: `scale(${s})`, boxShadow: '0 30px 60px rgba(0,0,0,.4)' }}>
      <div style={{ font: F(900, 46), color: CHIARO }}>{nm(big[0])}</div><div style={{ font: F(900, 26), letterSpacing: '.3em', color: ORO, margin: '14px 0' }}>CONTRO</div><div style={{ font: F(900, 46), color: CHIARO }}>{nm(big[1])}</div></div>
    <div style={{ position: 'absolute', bottom: 110, width: '100%', textAlign: 'center' }}><Img src={staticFile('logo-lega.png')} style={{ width: 90, opacity: interpolate(f, [20, 35], [0, 1], cl) }} /><div style={{ font: F(800, 26), color: CHIARO, marginTop: 10 }}>Tutto su O Girrr</div></div></AbsoluteFill>; };


const Intro = ({ t, n }) => { const f = useCurrentFrame(), { fps } = useVideoConfig(), s = spring({ frame: f, fps, config: { damping: 9, stiffness: 120 } }), A = TEMA[t].acc;
  return <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}><Sfondo t={t} />
    <Img src={staticFile(TEMA[t].logo)} style={{ position: 'relative', width: 300, transform: `scale(${s}) rotate(${(1 - s) * (t === 'lega' ? -20 : 20)}deg)`, filter: 'drop-shadow(0 20px 40px rgba(0,0,0,.45))' }} />
    <div style={{ position: 'relative', font: F(900, 30), letterSpacing: '.24em', color: t === 'lega' ? ORO : '#9fd0ff', marginTop: 46, opacity: interpolate(f, [14, 30], [0, 1], cl) }}>{TEMA[t].nome}</div>
    <div style={{ position: 'relative', font: F(900, 72), color: CHIARO, marginTop: 8, opacity: interpolate(f, [20, 36], [0, 1], cl), transform: `translateY(${interpolate(f, [20, 36], [30, 0], cl)}px)` }}>{n}ª giornata</div>
    <div style={{ position: 'relative', width: interpolate(f, [26, 46], [0, 260], cl), height: 8, borderRadius: 4, background: A, marginTop: 22 }} /></AbsoluteFill>; };

const Classifica = ({ n, c }) => { const f = useCurrentFrame(), { fps } = useVideoConfig(), ult = c.length - 1;
  return <AbsoluteFill><Sfondo t="lega" /><Tv t="lega" /><Titolo t="lega" k="CAMPIONATO" tit={`La classifica dopo la ${n}ª`} />
    <div style={{ position: 'relative', padding: '22px 56px', display: 'flex', flexDirection: 'column', gap: 8 }}>
      {c.map((q, i) => { const s = spring({ frame: f - 8 - i * 3, fps, config: { damping: 14, stiffness: 150 } });
        return <Riga key={q.n} pos={i + 1} nome={q.n} t="lega" med={MEDAGLIE[i]} ult={i === ult} s={s} mossa={`translateX(${(1 - s) * 120}px)`} conta={<Conta a={q.pt} da={8 + i * 3} />} />; })}</div></AbsoluteFill>; };

const Riquadro = ({ t, k, a, b, da }) => { const f = useCurrentFrame(), { fps } = useVideoConfig(), s = spring({ frame: f - da, fps, config: { damping: 10, stiffness: 110 } }), A = TEMA[t];
  return <div style={{ position: 'relative', margin: '0 56px 26px', padding: '26px 26px 30px', borderRadius: 24, textAlign: 'center', background: `linear-gradient(120deg,${A.acc},${A.acc2} 60%,#141d3d 130%)`, transform: `scale(${s})`, opacity: s, boxShadow: '0 24px 50px rgba(0,0,0,.4)' }}>
    <Img src={staticFile(A.logo)} style={{ position: 'absolute', top: 16, left: 18, width: 54 }} />
    <div style={{ font: F(900, 18), letterSpacing: '.24em', color: t === 'lega' ? ORO : '#d6ecff' }}>{k}</div>
    <div style={{ font: F(900, 38), color: CHIARO, marginTop: 14 }}>{nm(a)}</div><div style={{ font: F(900, 20), letterSpacing: '.3em', color: t === 'lega' ? ORO : '#d6ecff', margin: '8px 0' }}>CONTRO</div><div style={{ font: F(900, 38), color: CHIARO }}>{nm(b)}</div></div>; };

const DaNonPerdere = ({ n, big, nc2, bigC }) => <AbsoluteFill><Sfondo t="lega" /><Titolo t="lega" k="PROSSIMO TURNO" tit="Da non perdere" />
  <div style={{ position: 'relative', marginTop: 34 }}><Riquadro t="lega" k={`CAMPIONATO · ${n + 1}ª GIORNATA`} a={big[0]} b={big[1]} da={8} />{bigC && <Riquadro t="coppa" k={`CHAMPIONS CUP · ${nc2}ª GIORNATA`} a={bigC[0]} b={bigC[1]} da={20} />}</div></AbsoluteFill>;

const Fine = () => { const f = useCurrentFrame(), { fps } = useVideoConfig(), s = spring({ frame: f, fps, config: { damping: 11, stiffness: 120 } });
  return <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}><Sfondo t="lega" />
    <div style={{ position: 'relative', display: 'flex', gap: 28, alignItems: 'center', transform: `scale(${s})` }}><Img src={staticFile('logo-lega.png')} style={{ width: 170 }} /><Img src={staticFile('logo-coppa.png')} style={{ width: 150 }} /></div>
    <div style={{ position: 'relative', font: F(900, 54), color: CHIARO, marginTop: 44, opacity: interpolate(f, [12, 28], [0, 1], cl) }}>Tutto su O Girrr</div>
    <div style={{ position: 'relative', font: F(800, 24), color: ORO, marginTop: 12, opacity: interpolate(f, [20, 36], [0, 1], cl) }}>Risultati, classifiche e Curva</div></AbsoluteFill>; };

// Passaggio tra le scene: tendina del colore della competizione che arriva
const Tendina = ({ t }) => { const f = useCurrentFrame(), x = interpolate(f, [0, 14], [-120, 120]);
  return <AbsoluteFill style={{ transform: `translateX(${x}%) skewX(-12deg)`, background: `linear-gradient(90deg,${TEMA[t].acc} 0 70%,${ORO} 70% 78%,transparent 78%)` }} />; };

const SC = [['introLega', 75], ['lega', 165], ['podio', 120], ['classifica', 160], ['introCoppa', 70], ['coppa', 150], ['gironi', 135], ['prossime', 140], ['fine', 80]];
let da = 0; const INIZI = SC.map(([k, d]) => { const s = da; da += d; return [k, s, d]; }); const TOT = da;
const COPPA = ['introCoppa', 'coppa', 'gironi'];
const Video = (p) => <AbsoluteFill style={{ background: '#1d2a52' }}><Caratteri />
  {INIZI.map(([k, s, d]) => <Sequence key={k} from={s} durationInFrames={d}>
    {k === 'introLega' ? <Intro t="lega" n={p.n} /> : k === 'lega' ? <Risultati t="lega" n={p.n} m={p.m} /> : k === 'podio' ? <Podio n={p.n} c={p.cl.slice(0, 3)} /> : k === 'classifica' ? <Classifica n={p.n} c={p.cl} /> : k === 'introCoppa' ? <Intro t="coppa" n={p.nc} /> : k === 'coppa' ? <Risultati t="coppa" n={p.nc} m={p.mc} /> : k === 'gironi' ? <Gironi nc={p.nc} gir={p.gir} /> : k === 'prossime' ? <DaNonPerdere n={p.n} big={p.big} nc2={p.nc2} bigC={p.bigC} /> : <Fine />}</Sequence>)}
  {INIZI.slice(1).map(([k, s]) => <Sequence key={'t' + k} from={s - 7} durationInFrames={15}><Tendina t={COPPA.indexOf(k) >= 0 ? 'coppa' : 'lega'} /></Sequence>)}
</AbsoluteFill>;

registerRoot(() => <Composition id="Giornata" component={Video} durationInFrames={TOT} fps={30} width={720} height={1280} defaultProps={{ n: 7, nc: 4, nc2: 5, m: [], mc: [], cl: [], gir: {}, big: ['', ''], bigC: null }} />);
