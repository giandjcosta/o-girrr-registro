"""Spogliatoio 5.5: grafica Stadio e scelta delle grafiche in un menu a tendina.

Parte dallo Spogliatoio vero (index.html di gh-pages del sito) e scrive:
  - con --lab: lab/prova-spogliatoio-55.html (copia di prova con <base> verso il sito, senza contatore visite);
  - con --sito PERCORSO: la pagina da pubblicare (solo al rilascio, con il «vai» di Gianluca).
Uso: python3 rilascio/spogliatoio55.py SORGENTE.html --lab
Regola grafica (AGENTS.md): Lega con riquadri grandi dritti e banda rossa dritta di 8 px, pillole tonde;
Stadio con riquadri tondi (12 px) e banda curva in oro, schede e pillole tonde, titoli in Lobster. Accento rosso nella Lega, oro nello Stadio.
"""
import re, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
SKINS_VECCHIE = "[['girrr','Stile O Girrr'],['viola','Stile FantaLab'],['azzurro','Stile Leghe'],['seriea','Stile Serie A'],['campo','Stile Figurine']]"
SKINS_NUOVE = "[['girrr','Stile O Girrr · Lega'],['stadio','Stile O Girrr · Stadio'],['viola','Stile FantaLab'],['azzurro','Stile Leghe'],['seriea','Stile Serie A'],['campo','Stile Figurine']]"

CSS = r"""
/* 5.5 — Stile O Girrr in due grafiche (regola di Gianluca, 1° novembre 2026) */
:root[data-skin="girrr"]{--fh:Inter,system-ui,-apple-system,sans-serif}
:root[data-skin="girrr"] h1,:root[data-skin="girrr"] h2.sec{font-family:Inter,system-ui,sans-serif;font-weight:900;letter-spacing:-.01em}
:root[data-skin="girrr"] header,:root[data-skin="girrr"] .card,:root[data-skin="girrr"] .note,:root[data-skin="girrr"] .empty,:root[data-skin="girrr"] .tw{border-radius:4px 14px 14px 4px!important;border-left:8px solid #d62839!important}
:root[data-skin="girrr"] nav button[aria-selected=true],:root[data-skin="girrr"] .seg button[aria-pressed=true]{background:#d62839;box-shadow:none}
:root[data-skin="stadio"] header,:root[data-skin="stadio"] .card,:root[data-skin="stadio"] .note,:root[data-skin="stadio"] .empty,:root[data-skin="stadio"] .tw{border-radius:12px!important;border-left:8px solid #ffd166!important}
:root[data-skin="stadio"] nav button[aria-selected=true],:root[data-skin="stadio"] .seg button[aria-pressed=true]{background:linear-gradient(160deg,#ffe08a,#f0b93a);color:#1d2a52;border-color:#ffe7a3;box-shadow:inset 0 1px 0 rgba(255,255,255,.6),0 6px 20px rgba(255,209,102,.35)}
:root[data-skin="stadio"] header::after{background:linear-gradient(90deg,#ffd166 0 60%,#d62839 60% 100%)}
/* le voci della tendina hanno uno sfondo pieno (su PC erano bianche su bianco) */
:root:is([data-skin="girrr"],[data-skin="stadio"]) select option{background:#1d2a52;color:#fbf6ec}
:root[data-skin="stadio"] nav button,:root[data-skin="stadio"] .seg button,:root[data-skin="stadio"] .skin-menu button,:root[data-skin="stadio"] .verdict,:root[data-skin="stadio"] .stb,:root[data-skin="stadio"] .fx,:root[data-skin="stadio"] .btn{border-radius:999px!important}
/* Menu delle grafiche: un solo bottone che apre l'elenco */
.skin-menu{position:relative;margin-bottom:12px;max-width:100%}
.skin-menu>summary{list-style:none;display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink);font:700 .85rem var(--fb);cursor:pointer;user-select:none}
.skin-menu>summary::-webkit-details-marker{display:none}
.skin-menu>summary b{font-weight:800}
.skin-menu>summary i{font-style:normal;display:inline-block;transition:transform .3s cubic-bezier(.22,.61,.36,1)}
.skin-menu[open]>summary i{transform:rotate(180deg)}
.skin-menu .skin{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px;margin:8px 0 0;padding:8px;border:1px solid var(--line);border-radius:14px;background:var(--card);box-shadow:0 10px 30px rgba(0,0,0,.25)}
.skin-menu .skin button{display:flex;align-items:center;gap:8px;min-height:44px;text-align:left;border-radius:10px}
.skin-menu .skin button::before{content:'';flex:none;width:18px;height:18px;border-radius:50%;border:2px solid rgba(255,255,255,.6);background:var(--sw,#888)}
.skin-menu .skin button[data-skin=girrr]{--sw:linear-gradient(135deg,#1d2a52 50%,#d62839 50%)}
.skin-menu .skin button[data-skin=stadio]{--sw:linear-gradient(135deg,#1d2a52 50%,#ffd166 50%)}
.skin-menu .skin button[data-skin=viola]{--sw:linear-gradient(135deg,#2a1c52 50%,#8b5cf6 50%)}
.skin-menu .skin button[data-skin=azzurro]{--sw:linear-gradient(135deg,#fff 50%,#3d93d6 50%)}
.skin-menu .skin button[data-skin=seriea]{--sw:linear-gradient(135deg,#0a1f5c 50%,#00b4ff 50%)}
.skin-menu .skin button[data-skin=campo]{--sw:linear-gradient(135deg,#f5ecd7 50%,#2e8b57 50%)}
.skin-menu .skin button[aria-pressed=true]{outline:2px solid currentColor;outline-offset:-2px}
@media(max-width:360px){.skin-menu .skin{grid-template-columns:1fr}}
"""

JS = r"""<script>/* 5.5: menu delle grafiche — si apre e si chiude con una dissolvenza, si chiude dopo la scelta o toccando fuori */
(function(){var m=document.querySelector('.skin-menu');if(!m)return;var calmo=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function nome(){var b=m.querySelector('.skin button[aria-pressed=true]');m.querySelector('summary b').textContent=b?b.textContent:'Stile O Girrr · Lega'}
new MutationObserver(nome).observe(m.querySelector('.skin'),{childList:true,subtree:true,attributes:true});nome();
m.addEventListener('toggle',function(){if(m.open&&!calmo&&m.querySelector('.skin').animate)m.querySelector('.skin').animate({opacity:[0,1],transform:['translateY(-6px)','none']},{duration:260,easing:'cubic-bezier(.22,.61,.36,1)'})});
m.querySelector('.skin').addEventListener('click',function(e){if(e.target.closest('button'))setTimeout(function(){m.open=false},120)});
document.addEventListener('click',function(e){if(m.open&&!m.contains(e.target))m.open=false});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&m.open){m.open=false;m.querySelector('summary').focus()}});
})();</script>"""


def trasforma(s):
    def sost(a, b, n=1):
        nonlocal s
        assert s.count(a) >= 1, 'non trovato: ' + a[:80]
        s = s.replace(a, b, n)
    # la grafica Stadio parte dallo Stile O Girrr di oggi (Lobster, vetro) e ne eredita tutte le regole
    s = s.replace(':root[data-skin="girrr"]', ':root:is([data-skin="girrr"],[data-skin="stadio"])')
    sost(SKINS_VECCHIE, SKINS_NUOVE)
    sost("['girrr','viola','azzurro','seriea','campo'].indexOf(s)<0", "['girrr','stadio','viola','azzurro','seriea','campo'].indexOf(s)<0")
    sost('<div class="skin" id="skin" role="group" aria-label="Stile grafico"></div>',
         '<details class="skin-menu"><summary aria-label="Scegli la grafica">Grafica: <b>Stile O Girrr · Lega</b> <i aria-hidden="true">▾</i></summary><div class="skin" id="skin" role="group" aria-label="Stile grafico"></div></details>')
    i = s.rindex('</style>')  # in fondo all'ultimo foglio, dopo le regole dello Stile O Girrr
    s = s[:i] + CSS + s[i:]
    sost('</body>', JS + '</body>')
    return s


def main():
    src = Path(sys.argv[1]).read_text(encoding='utf-8')
    out = trasforma(src)
    if '--lab' in sys.argv:
        out = out.replace('<head>', '<head>\n<base href="https://giandjcosta.github.io/o-fant-a-girrr/">', 1)
        out = re.sub(r'<script>window\.goatcounter=.*?</script>\s*<script data-goatcounter=[^>]*></script>', '', out, count=1, flags=re.S)
        out = out.replace('<title>', '<title>Prova 5.5 · ', 1)
        (R / 'lab/prova-spogliatoio-55.html').write_text(out, encoding='utf-8')
        print('scritto lab/prova-spogliatoio-55.html')
    elif '--sito' in sys.argv:
        Path(sys.argv[sys.argv.index('--sito') + 1]).write_text(out, encoding='utf-8')
        print('scritto', sys.argv[sys.argv.index('--sito') + 1])


if __name__ == '__main__':
    main()
