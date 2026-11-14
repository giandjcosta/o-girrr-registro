#!/usr/bin/env python3
"""Proposta 6.1.1: applicare a una COPIA della 6.1. Nessun commit o pubblicazione."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]


def sost(t, a, b):
    if t.count(a) != 1:
        raise ValueError('Curva diversa dalla base certificata: ' + a[:90])
    return t.replace(a, b)


def curva(t):
    if 'var cvModelloTs=0;' in t:
        return t
    t = sost(t, 'function render(){cvNascondi();cvColori();',
             '/* ChatGPT · 6.1.1: la navigazione riusa il modello; dati e reazioni lo ricostruiscono. */\nvar cvModelloTs=0;\nfunction render(soloVista){cvNascondi();cvColori();')
    t = sost(t, ' TR=tendenze();POSTS=costruisci();NOTI=me?notifiche():[];',
             ' if(!soloVista||!cvModelloTs||Date.now()-cvModelloTs>=60000){TR=tendenze();POSTS=costruisci();NOTI=me?notifiche():[];cvModelloTs=Date.now()}')
    t = sost(t, "  h+=(filt==='seguiti'", "  h+='<div class=\"cv-flusso\">';\n  h+=(filt==='seguiti'")
    t = sost(t, " }else if(vista==='notifiche'){", "  h+='</div>';\n }else if(vista==='notifiche'){")
    t = sost(t, "  h+=ptab==='risp'?rispHTML(rispostePosts(a)):feed(profiloPosts(a));",
             "  h+='<div class=\"cv-flusso\">'+(ptab==='risp'?rispHTML(rispostePosts(a)):feed(profiloPosts(a)))+'</div>';")
    for a, b in [
        ("if(d.nf){ntab=d.nf;render();return}", "if(d.nf){ntab=d.nf;render(true);return}"),
        ("if(d.pt){ptab=d.pt;render();return}", "if(d.pt){ptab=d.pt;render(true);return}"),
        ("if(d.f){filt=d.f;FEED_SHOW=20;scrollTo(0,0);render();return}", "if(d.f){filt=d.f;FEED_SHOW=20;scrollTo(0,0);render(true);return}"),
        ("if(d.v==='esplora')qs='';render();return}", "if(d.v==='esplora')qs='';render(true);return}"),
        ("filt=TF[n];FEED_SHOW=20;render();", "filt=TF[n];FEED_SHOW=20;render(true);")
    ]:
        t = sost(t, a, b)
    t = sost(t, " try{var mx=POSTS.length?POSTS[0].ts:0;localStorage.setItem('cv-ultimo',String(mx))}catch(e){}\n}",
             " try{var mx=POSTS.length?POSTS[0].ts:0;localStorage.setItem('cv-ultimo',String(mx))}catch(e){}\n document.dispatchEvent(new Event('og:curva-disegnata'));\n}")
    return t


def prepara(sito):
    # Prepara tutto prima di scrivere: un'ancora diversa non lascia una copia a metà.
    out = {}
    for skin in ('girrr', 'stadio/girrr'):
        p = sito / skin / 'curva.html'
        t = curva(p.read_text())
        t = re.sub(r'(curva-os\.(?:js|css))(?:\?[^\"\s<>]*)?', r'\1?v=611-1', t)
        out[p] = t
        p = sito / skin / 'app.html'
        out[p] = re.sub(r'(stagione\.js|giro-di-boa\.js)(?:\?[^\"\s<>]*)?', r'\1?v=611-1', p.read_text())
    for rel in ('stagione/stagione.js', 'curva-os/curva-os.js', 'curva-os/curva-os.css', 'r602/giro-di-boa.js'):
        out[sito / Path(rel).name] = (ROOT / 'rilascio' / rel).read_text()
    for p, t in out.items():
        p.write_text(t)
    print('6.1.1 preparata su una copia · Versioni e sito online non modificati')


if __name__ == '__main__':
    prepara(Path(sys.argv[1]).resolve())
