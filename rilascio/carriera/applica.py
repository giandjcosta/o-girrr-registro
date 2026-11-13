#!/usr/bin/env python3
"""Carriera: numero della fiducia «a cartellini» e schede centrate (Claude, 12 novembre 2026). Prototipo per il Lab.

Segnalazioni di Gianluca (foto dal sito vero):
  - il numero della fiducia, durante l'animazione, «resta in alto ed è un po' buggato»: in WebKit la ribalta in 3D del testo
    dentro l'SVG lo schiaccia verso l'alto (alto 15 px invece di 57) e il conteggio salta da 0 a 47;
  - «Panoramica» non è centrata: la fila delle schede (.oro-scroll) ha lo scroll snap che aggancia la prima scheda al bordo
    e si mangia i 4 px di margine a sinistra.
Questo script:
  1. .oro-scroll con scroll-padding-inline: la prima scheda resta a 5 px dal bordo come sopra e sotto (tutte le file uguali);
  2. il numero diventa un tabellone a cartellini (HTML sopra l'arco): ogni cifra si ribalta a metà quando cambia, mentre l'arco
     si colora; conteggio un po' più lento (circa 1,5 s) per leggere i cambi; con «riduci movimento» niente ribalte.

Uso: python3 rilascio/carriera/applica.py CARTELLA_DEL_SITO   (una copia di gh-pages)
Scrive rilascio/carriera/pagine/girrr/app.html e rilascio/carriera/pagine/stadio/girrr/app.html.
"""
import os
import sys

STILE = r'''<style id="cartellini-fiducia">
/* Claude, 12 novembre 2026: schede centrate e numero della fiducia a cartellini (rilascio/carriera/applica.py) */
.oro-scroll{scroll-padding-inline:4px}
.trust-visual{position:relative}
.trust-visual .trust-number{opacity:0}
.tab-fid{position:absolute;left:50%;top:64%;transform:translate(-50%,-50%);display:flex;gap:5px;font:900 clamp(30px,10vw,42px)/1 Inter,system-ui,sans-serif;pointer-events:none}
.tab-fid .fl{position:relative;width:.78em;height:1.18em;perspective:300px;border-radius:7px;box-shadow:0 4px 12px rgba(0,0,0,.35)}
.tab-fid .fl>span{position:absolute;left:0;right:0;height:50%;overflow:hidden;background:linear-gradient(180deg,#22305e,#18234a);color:#fbf6ec}
.tab-fid .fl>span b{display:block;height:200%;line-height:1.18em;text-align:center;font-weight:900}
.tab-fid .fl .su,.tab-fid .fl .a{top:0;border-radius:7px 7px 0 0;transform-origin:50% 100%}
.tab-fid .fl .giu,.tab-fid .fl .b{bottom:0;border-radius:0 0 7px 7px;transform-origin:50% 0;background:linear-gradient(180deg,#141d3d,#1b2650)}
.tab-fid .fl .giu b,.tab-fid .fl .b b{transform:translateY(-50%)}
.tab-fid .fl::after{content:'';position:absolute;left:0;right:0;top:50%;height:1px;background:rgba(0,0,0,.55);z-index:3}
.tab-fid .fl .a,.tab-fid .fl .b{visibility:hidden;z-index:2}
.tab-fid .fl.gira .a{visibility:visible;animation:fl-a var(--fl,.16s) ease-in both}
.tab-fid .fl.gira .b{visibility:visible;animation:fl-b var(--fl,.16s) ease-out var(--fl,.16s) both}
@keyframes fl-a{from{transform:rotateX(0)}to{transform:rotateX(-90deg)}}
@keyframes fl-b{from{transform:rotateX(90deg)}to{transform:rotateX(0)}}
@media (prefers-reduced-motion:reduce){.tab-fid .fl.gira .a,.tab-fid .fl.gira .b{animation:none;visibility:hidden}}
</style>'''

CODICE = r'''
/* Numero della fiducia a cartellini (Claude, 12 novembre 2026): ogni cifra è un cartellino che si ribalta a metà quando cambia */
function fidTab(el,v){if(!el)return;var t=el.querySelector('.tab-fid');
 if(!t){t=document.createElement('div');t.className='tab-fid';t.setAttribute('aria-hidden','true');el.appendChild(t)}
 var s=String(Math.max(0,Math.min(100,Math.round(v)))),n=Math.max(2,s.length);s=('000'+s).slice(-n);
 while(t.children.length<n){var f=document.createElement('span');f.className='fl';f.dataset.v='0';f.innerHTML='<span class="su"><b>0</b></span><span class="giu"><b>0</b></span><span class="a"><b>0</b></span><span class="b"><b>0</b></span>';t.appendChild(f)}
 while(t.children.length>n)t.removeChild(t.firstChild);
 [].forEach.call(t.children,function(f,i){var o=f.dataset.v,c=s.charAt(i);if(o===c)return;f.dataset.v=c;
  var q=function(k){return f.querySelector('.'+k+' b')};q('su').textContent=c;q('a').textContent=o;q('b').textContent=c;
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){q('giu').textContent=c;return}
  f.classList.remove('gira');void f.offsetWidth;f.classList.add('gira');
  clearTimeout(f._t);f._t=setTimeout(function(){q('giu').textContent=f.dataset.v;f.classList.remove('gira')},340)})}
'''

SOSTITUZIONI = [
    # il tabellone segue il numero mentre sale, e alla fine
    ("shown=r;number.textContent=String(r);", "shown=r;number.textContent=String(r);fidTab(el,r);"),
    ("TRUSTANIM.giro=null;number.textContent=String(v);", "TRUSTANIM.giro=null;number.textContent=String(v);fidTab(el,v);"),
    # conteggio un po' più lento, per leggere i cartellini che cambiano
    ("duration:Math.max(700,Math.min(1500,v*18))", "duration:Math.max(1100,Math.min(1900,v*30))"),
]


def applica(t):
    for a, b in SOSTITUZIONI:
        n = t.count(a)
        assert n == 1, 'trovato %d volte: %s' % (n, a[:60])
        t = t.replace(a, b)
    k = 'function animaFiducia(t,v){'
    assert t.count(k) == 1
    t = t.replace(k, CODICE.strip() + '\n' + k)
    assert t.count('</head>') == 1
    return t.replace('</head>', STILE + '</head>')


if __name__ == '__main__':
    sito = sys.argv[1]
    qui = os.path.dirname(os.path.abspath(__file__))
    for rel in ('girrr/app.html', 'stadio/girrr/app.html'):
        t = open(os.path.join(sito, rel), encoding='utf-8').read()
        out = os.path.join(qui, 'pagine', rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(applica(t))
        print('scritto', out)
