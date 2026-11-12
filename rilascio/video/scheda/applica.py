#!/usr/bin/env python3
"""Girrr Sport: scheda «Video» con il video della giornata e l'archivio di tutti i video, come la Radio (Claude, 12 novembre 2026).

Gianluca: «il video voglio che stia in un menu della TV, così che ognuno possa guardarseli tutti come la radio».
Girrr Sport è la TV della lega («La TV, il giornale e la radio della lega»): la scheda Video va accanto a Radio.
- In alto il video scelto (di partenza l'ultimo), verticale, con la sua copertina; sotto «Tutti i video», dal più recente.
  Toccando un video della lista parte nel riquadro in alto. I video restano tutti, da rivedere quando si vuole.
- I video e archivio.json stanno in girrr/video/ (li scrive il workflow dopo ogni giornata: fai_video.sh e archivio.py).
- Link diretto: app.html#video. Con «riduci movimento» lo scorrimento verso il video non è animato.

Uso: python3 rilascio/video/scheda/applica.py CARTELLA_DEL_SITO [--lab]
Con --lab i video si leggono dalla cartella del registro lab/video-giornata/archivio/ (prova nel Lab).
Scrive rilascio/video/pagine/girrr/app.html e rilascio/video/pagine/stadio/girrr/app.html.
"""
import os
import sys

CODICE = r'''
/* ---------- VIDEO (Claude, 12 novembre 2026: rilascio/video/scheda/applica.py) ---------- */
var VA=null,VSEL=0,VB=%(base)s;   /* VSEL: il video scelto dalla lista; riaprendo la pagina si riparte dall'ultimo */
function vidCarica(){if(VA!==null)return;VA=false;try{
  fetch(VB+'archivio.json?v='+Date.now(),{cache:'no-cache'}).then(function(r){if(!r.ok)throw new Error(r.status);return r.json()}).then(function(j){VA=Array.isArray(j)?j:'errore';if(cur==='sport'&&S.sp==='video')render()}).catch(function(){VA='errore';if(cur==='sport'&&S.sp==='video')render()})}catch(e){VA='errore'}}
function spVideo(){
  vidCarica();
  var intro='<h3>Il video della giornata</h3><p class="sm mut" style="margin:6px 0 12px">La giornata in mezzo minuto: risultati, podio, classifica, Champions Cup e le partite da non perdere. Ogni settimana un video nuovo, e restano tutti qui, da rivedere quando vuoi.</p>';
  if(VA===false||VA===null)return '<div class="card">'+intro+'<b>Carico i video…</b></div>';
  if(VA==='errore')return '<div class="card">'+intro+'<b>I video non si sono caricati</b><p class="sm mut">Riprova tra poco: se continua, avvisa Gianluca.</p></div>';
  if(!VA.length)return '<div class="card">'+intro+'<b>Nessun video ancora</b><p class="sm mut">Il primo arriva con la prossima giornata, e da lì restano tutti qui.</p></div>';
  var x=VA.filter(function(v){return v.n===VSEL})[0]||VA[0];
  var h='<div class="card">'+intro+'<div class="rtit"><b>'+esc(x.titolo)+'</b><span class="rbadge">'+esc(x.tag)+'</span></div>'
   +'<video id="vid-player" class="vid-v" controls playsinline preload="metadata"'+(x.img?' poster="'+VB+esc(x.img)+'"':'')+' src="'+VB+esc(x.file)+'"></video></div>';
  if(VA.length>1)h+='<div class="card"><h3>Tutti i video</h3><div class="vid-l">'+VA.map(function(v){return '<button type="button" class="vid-i" data-vid="'+v.n+'" aria-pressed="'+(v.n===x.n)+'">'+(v.img?'<img src="'+VB+esc(v.img)+'" alt="" loading="lazy">':'<i></i>')+'<span><b>'+esc(v.titolo)+'</b><small>'+esc(v.tag)+'</small></span></button>'}).join('')+'</div></div>';
  return h}
document.addEventListener('click',function(e){var b=e.target.closest('[data-vid]');if(!b)return;VSEL=+b.dataset.vid;render();
  var v=document.getElementById('vid-player');if(!v)return;var fermo=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  try{v.scrollIntoView({behavior:fermo?'auto':'smooth',block:'center'})}catch(er){}try{var p=v.play();if(p&&p.catch)p.catch(function(){})}catch(er){}});

/* ---------- MOVIOLA ---------- */'''

CSS = ('.vid-v{display:block;width:100%%;max-width:360px;aspect-ratio:9/16;margin:12px auto 2px;border-radius:14px;background:#000;object-fit:contain}'
       '.vid-l{display:grid;gap:10px;margin-top:10px}'
       '.vid-i{display:flex;gap:12px;align-items:center;text-align:left;width:100%%;padding:8px;border-radius:12px;border:1px solid var(--line);background:transparent;color:inherit;font:inherit;cursor:pointer;transition:background .25s ease,border-color .25s ease}'
       '.vid-i[aria-pressed=true]{border-color:var(--gold);background:rgba(255,209,102,.08)}'
       '.vid-i img,.vid-i i{flex:none;width:54px;aspect-ratio:9/16;border-radius:8px;object-fit:cover;background:#0b1230}'
       '.vid-i span{display:flex;flex-direction:column;gap:4px;min-width:0}.vid-i b{font-weight:800;line-height:1.25}.vid-i small{font-size:12px;opacity:.75}'
       '@media(prefers-reduced-motion:reduce){.vid-i{transition:none}}')

SOSTITUZIONI = [
    ("['radio','Radio'],['sfide','Sfide']", "['radio','Radio'],['video','Video'],['sfide','Sfide']"),
    ("sp==='radio'?spRadio():", "sp==='radio'?spRadio():sp==='video'?spVideo():"),
    ("if(t==='conf'||t==='radio'||t==='giornale'||t==='moviola'){S.sp=t;t='sport'}",
     "if(t==='conf'||t==='radio'||t==='giornale'||t==='moviola'||t==='video'){S.sp=t;t='sport'}"),
    ("if(hh==='conf'||hh==='radio'||hh==='moviola'){S.sp=hh;hh='sport'}", "if(hh==='conf'||hh==='radio'||hh==='moviola'||hh==='video'){S.sp=hh;hh='sport'}"),
    ("if(x==='moviola'||(V[x]&&x!==cur))go(x)", "if(x==='moviola'||x==='video'||(V[x]&&x!==cur))go(x)"),
    ("Giornale, conferenze stampa, radio e sfide lanciate", "Giornale, video, radio, conferenze stampa e sfide lanciate"),
    ("\n/* ---------- MOVIOLA ---------- */", None),
    (".mvsel{display:flex;", None),
]


def applica(t, base):
    for a, b in SOSTITUZIONI:
        n = t.count(a)
        assert n == 1, 'trovato %d volte: %s' % (n, a[:60])
        if b is None:
            b = (CODICE % {'base': base}) if 'MOVIOLA' in a else (CSS % ()) + a
        t = t.replace(a, b)
    return t


if __name__ == '__main__':
    sito, lab = sys.argv[1], '--lab' in sys.argv
    qui = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for rel, base_sito, base_lab in (('girrr/app.html', "'video/'", "'../../../video-giornata/archivio/'"),
                                     ('stadio/girrr/app.html', "'../../girrr/video/'", "'../../../../video-giornata/archivio/'")):
        t = open(os.path.join(sito, rel), encoding='utf-8').read()
        out = os.path.join(qui, 'pagine', rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(applica(t, base_lab if lab else base_sito))
        print('scritto', out)
