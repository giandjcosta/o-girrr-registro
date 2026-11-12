import React, { useEffect, useState } from 'react';
import { registerRoot, Composition, AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, spring, interpolate, Img, delayRender, continueRender, staticFile } from 'remotion';

// Strada B (Claude, 12 novembre 2026): lo stesso video della giornata fatto con Remotion. Dati veri passati da fuori (inputProps).
const NOMI = { 'The Blue brothers': 'The Blues Brothers' };
const nm = s => NOMI[s] || s;
const ORO = '#ffd166', CHIARO = '#fbf6ec', ROSSO = '#d62839';

const Sfondo = () => <AbsoluteFill style={{ background: 'radial-gradient(700px 500px at 85% -5%, rgba(214,40,57,.35), transparent 60%), radial-gradient(800px 600px at -10% 30%, rgba(61,147,214,.3), transparent 60%), linear-gradient(180deg,#2c3f7c,#1d2a52 45%,#141d3d)' }} />;

const Caratteri = () => {
  const [h] = useState(() => delayRender('caratteri'));
  useEffect(() => { const l = document.createElement('style'); l.textContent = `@font-face{font-family:'Inter';font-weight:700;font-style:normal;src:url(FONT/f0.woff2) format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF}
@font-face{font-family:'Inter';font-weight:700;font-style:normal;src:url(FONT/f1.woff2) format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}
@font-face{font-family:'Inter';font-weight:800;font-style:normal;src:url(FONT/f2.woff2) format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF}
@font-face{font-family:'Inter';font-weight:800;font-style:normal;src:url(FONT/f3.woff2) format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}
@font-face{font-family:'Inter';font-weight:900;font-style:normal;src:url(FONT/f4.woff2) format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF}
@font-face{font-family:'Inter';font-weight:900;font-style:normal;src:url(FONT/f5.woff2) format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}
@font-face{font-family:'Lobster';font-weight:400;font-style:normal;src:url(FONT/f6.woff2) format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF}
@font-face{font-family:'Lobster';font-weight:400;font-style:normal;src:url(FONT/f7.woff2) format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}`.split('FONT/').join(staticFile('font/')); document.head.appendChild(l);   /* caratteri in locale (public/font) */
    Promise.all([document.fonts.load('64px Lobster'), document.fonts.load('900 24px Inter')]).finally(() => continueRender(h)); }, []);
  return null;
};

// Numero che «sale» fino al valore (i gol del risultato contano da 0)
const Conta = ({ a, da }) => { const f = useCurrentFrame(); const v = Math.round(interpolate(f, [da, da + 18], [0, a], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })); return <>{v}</>; };

const Apertura = ({ n }) => { const f = useCurrentFrame(), { fps } = useVideoConfig(); const s = spring({ frame: f, fps, config: { damping: 9, stiffness: 120 } });
  return <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
    <Img src={staticFile('logo.png')} style={{ width: 300, transform: `scale(${s}) rotate(${(1 - s) * -25}deg)` }} />
    <div style={{ font: '96px Lobster', color: CHIARO, marginTop: 40, opacity: interpolate(f, [12, 30], [0, 1], { extrapolateRight: 'clamp' }), transform: `translateY(${interpolate(f, [12, 30], [40, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })}px)` }}>{n}ª giornata</div>
    <div style={{ font: '900 26px Inter', letterSpacing: '.3em', color: ORO, marginTop: 10, opacity: interpolate(f, [24, 40], [0, 1], { extrapolateRight: 'clamp' }) }}>CAMPIONATO · I RISULTATI</div>
  </AbsoluteFill>; };

const Titolo = ({ k, t }) => { const f = useCurrentFrame(); return <div style={{ padding: '90px 56px 0' }}>
  <div style={{ font: '900 24px Inter', letterSpacing: '.3em', color: ORO }}>{k}</div>
  <div style={{ font: '64px Lobster', color: CHIARO, marginTop: 6 }}>{t}</div>
  <div style={{ height: 14, marginTop: 24, borderRadius: 3, transform: 'skewX(-45deg)', width: `${interpolate(f, [0, 25], [0, 100], { extrapolateRight: 'clamp' })}%`, background: `linear-gradient(90deg,${ROSSO} 0 12%,${ORO} 12% calc(12% + 14px),#0f1736 calc(12% + 14px) 100%)` }} /></div>; };

const Risultati = ({ n, m }) => { const f = useCurrentFrame(), { fps } = useVideoConfig();
  return <AbsoluteFill><Titolo k={`CAMPIONATO · ${n}ª GIORNATA`} t="I risultati" />
    <div style={{ padding: '30px 56px', display: 'flex', flexDirection: 'column', gap: 22 }}>
      {m.map((x, i) => { const da = 15 + i * 12, s = spring({ frame: f - da, fps, config: { damping: 12, stiffness: 140 } }); const r = x[4].split('-').map(Number);
        return <div key={i} style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', alignItems: 'center', gap: 16, padding: '24px 26px', borderRadius: 22, background: 'rgba(255,255,255,.09)', borderLeft: `10px solid ${ROSSO}`, opacity: s, transform: `translateX(${(1 - s) * 200}px)` }}>
          <b style={{ font: '800 27px Inter', color: r[0] > r[1] ? ORO : CHIARO }}>{nm(x[0])}</b>
          <span style={{ font: '900 52px Inter', color: CHIARO, background: 'rgba(0,0,0,.28)', borderRadius: 16, padding: '4px 18px', minWidth: 150, textAlign: 'center' }}><Conta a={r[0]} da={da + 8} /> - <Conta a={r[1]} da={da + 8} /></span>
          <b style={{ font: '800 27px Inter', textAlign: 'right', color: r[1] > r[0] ? ORO : CHIARO }}>{nm(x[3])}</b></div>; })}
    </div></AbsoluteFill>; };

const Podio = ({ n, c }) => { const f = useCurrentFrame(), { fps } = useVideoConfig();
  const col = [[c[1], 2, 320, 20, '#dfe6f3'], [c[0], 1, 420, 8, ORO], [c[2], 3, 250, 30, '#e7a46a']];
  return <AbsoluteFill><Titolo k="CAMPIONATO" t={`La classifica dopo la ${n}ª`} />
    <div style={{ position: 'absolute', bottom: 120, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: 22 }}>
      {col.map(([t, pos, h, da, bg]) => { const s = spring({ frame: f - da, fps, config: { damping: 11, stiffness: 90 } });
        return <div key={pos} style={{ width: 190, textAlign: 'center' }}>
          <div style={{ font: '800 28px Inter', color: CHIARO, opacity: s }}>{nm(t.n)}</div>
          <div style={{ font: '700 26px Inter', color: ORO, margin: '6px 0 12px', opacity: s }}><Conta a={t.pt} da={da} /> punti</div>
          <div style={{ height: h * s, background: bg, borderRadius: '18px 18px 6px 6px', font: '90px Lobster', color: '#1d2a52', paddingTop: 16 }}>{pos}</div></div>; })}
    </div></AbsoluteFill>; };

const Prossima = ({ n, big, altre }) => { const f = useCurrentFrame(), { fps } = useVideoConfig(); const s = spring({ frame: f - 8, fps, config: { damping: 10, stiffness: 110 } });
  return <AbsoluteFill><Titolo k={`PROSSIMA GIORNATA · ${n + 1}ª`} t="La partita da non perdere" />
    <div style={{ margin: '60px 56px 0', padding: '40px 30px', borderRadius: 26, textAlign: 'center', background: `linear-gradient(120deg,${ROSSO},#8e1a2a 60%,#141d3d 130%)`, transform: `scale(${s})`, boxShadow: '0 30px 60px rgba(0,0,0,.4)' }}>
      <div style={{ font: '900 46px Inter', color: CHIARO }}>{nm(big[0])}</div><div style={{ font: '56px Lobster', color: ORO, margin: '8px 0' }}>contro</div><div style={{ font: '900 46px Inter', color: CHIARO }}>{nm(big[1])}</div></div>
    <div style={{ marginTop: 34, display: 'flex', flexDirection: 'column', gap: 12, alignItems: 'center' }}>
      {altre.map((x, i) => <span key={i} style={{ font: '700 25px Inter', color: 'rgba(251,246,236,.9)', opacity: interpolate(f, [20 + i * 5, 30 + i * 5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) }}>{nm(x[0])} - {nm(x[1])}</span>)}</div>
    <div style={{ position: 'absolute', bottom: 90, width: '100%', textAlign: 'center', font: '800 28px Inter', color: CHIARO }}>Tutto su O Girrr</div></AbsoluteFill>; };

// Passaggio tra le scene: una tendina rossa e oro che scorre
const Tendina = () => { const f = useCurrentFrame(); const x = interpolate(f, [0, 14], [-120, 120]);
  return <AbsoluteFill style={{ transform: `translateX(${x}%) skewX(-12deg)`, background: `linear-gradient(90deg,${ROSSO} 0 70%,${ORO} 70% 78%,transparent 78%)` }} />; };

const Video = (p) => <AbsoluteFill><Caratteri /><Sfondo />
  <Sequence durationInFrames={84}><Apertura n={p.n} /></Sequence>
  <Sequence from={84} durationInFrames={186}><Risultati n={p.n} m={p.m} /></Sequence>
  <Sequence from={270} durationInFrames={126}><Podio n={p.n} c={p.c} /></Sequence>
  <Sequence from={396}><Prossima n={p.n} big={p.big} altre={p.altre} /></Sequence>
  {[77, 263, 389].map(d => <Sequence key={d} from={d} durationInFrames={15}><Tendina /></Sequence>)}
</AbsoluteFill>;

registerRoot(() => <Composition id="Giornata" component={Video} durationInFrames={480} fps={30} width={720} height={1280} defaultProps={{ n: 7, m: [], c: [{}, {}, {}], big: ['', ''], altre: [] }} />);
