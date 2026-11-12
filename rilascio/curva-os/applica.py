#!/usr/bin/env python3
"""Curva: aggiornamento pezzo per pezzo e Notifiche divise (Claude, 12 novembre 2026). Prototipo per il Lab.

Oggi la Curva, a ogni ridisegno (cambio di scheda, applauso, aggiornamento ogni minuto), ricostruisce da zero
intestazione, barra in basso e contenuto con innerHTML: i loghi si ricaricano e lo script delle transizioni del sito
(transizioni.js) fa ricomparire in dissolvenza tutto quello che è «nuovo», cioè tutto.
Questo script cambia la pagina così:
  1. morfaIn(el, html): confronta il nuovo HTML con quello che c'è e aggiorna solo quello che è cambiato.
     I cori (article.post) si riconoscono dalla chiave data-k e si tengono anche se cambiano posto; i pezzi che non sono
     cambiati non si toccano (restano foto caricate, immagini nascoste perché mancanti, testo che stai scrivendo).
     Intestazione e barra in basso restano ferme: cambia solo la scheda o la sezione accesa.
  2. Due ascoltatori del campo di scrittura si agganciano una volta sola (con gli elementi tenuti si sarebbero raddoppiati).
  3. Notifiche con due schede: «Attività» (applausi, rilanci, risposte, visualizzazioni, traguardi) e «Menzioni».

Uso: python3 rilascio/curva-os/applica.py CARTELLA_DEL_SITO [--lab]   (CARTELLA_DEL_SITO: una copia di gh-pages)
Con --lab aggiunge window.__curvaProva, l'aggancio per le prove automatiche (entrare come squadra, ridisegnare,
aprire le Notifiche): solo nel Lab, al rilascio si genera senza.
Scrive rilascio/curva-os/pagine/girrr/curva.html e rilascio/curva-os/pagine/stadio/girrr/curva.html.
"""
import os
import sys

MORFA = r'''
/* Aggiornamento pezzo per pezzo (Claude, 12 novembre 2026): invece di ricostruire tutto con innerHTML,
   confronta il nuovo HTML con quello che c'è e cambia solo quello che è diverso. Vedi rilascio/curva-os/applica.py */
function morfaIn(el,html){if(!el)return;if(el.__h===html)return;el.__h=html;var t=document.createElement('template');t.innerHTML=html;mfFigli(el,t.content)}
function mfChiave(n){return n.nodeType===1&&n.tagName==='ARTICLE'&&n.getAttribute('data-k')||null}
function mfSegna(n){if(n.nodeType===1)n.__src=n.outerHTML;return n}
function mfFigli(a,b){var vec={},n=a.firstChild,k;while(n){k=mfChiave(n);if(k)vec[k]=n;n=n.nextSibling}
 var nuovi=[].slice.call(b.childNodes),cur=a.firstChild;
 for(var i=0;i<nuovi.length;i++){var nb=nuovi[i],es=null;k=mfChiave(nb);
  if(k&&vec[k]){es=vec[k];delete vec[k]}
  else if(!k&&cur&&!mfChiave(cur)&&cur.nodeType===nb.nodeType&&cur.nodeName===nb.nodeName)es=cur;
  if(es){if(es===cur)cur=cur.nextSibling;else a.insertBefore(es,cur);mfUno(es,nb)}
  else a.insertBefore(mfSegna(nb),cur)}
 while(cur){var nx=cur.nextSibling;a.removeChild(cur);cur=nx}}
function mfUno(a,b){
 if(a.nodeType!==1){if(a.nodeValue!==b.nodeValue)a.nodeValue=b.nodeValue;return}
 var src=b.outerHTML;if(a.__src===src)return;a.__src=src;   /* pezzo non cambiato: non si tocca */
 var i,at;for(i=a.attributes.length-1;i>=0;i--){at=a.attributes[i].name;if(!b.hasAttribute(at))a.removeAttribute(at)}
 for(i=0;i<b.attributes.length;i++){at=b.attributes[i];if(a.getAttribute(at.name)!==at.value)a.setAttribute(at.name,at.value)}
 if(a.tagName==='TEXTAREA'||a.tagName==='INPUT'||a.tagName==='SELECT')return;   /* quello che stai scrivendo resta */
 if(!b.firstChild&&a.firstChild&&a.classList.contains('pimg')&&a.hasAttribute('data-id'))return;   /* foto già caricata */
 mfFigli(a,b)}
'''

SOSTITUZIONI = [
    # 1. intestazione, barra in basso e contenuto
    ("document.getElementById('nav').innerHTML=", "morfaIn(document.getElementById('nav'),"),
    ("Lancia un coro</button>'\n}", "Lancia un coro</button>')\n}"),
    ("document.getElementById('top').innerHTML=", "morfaIn(document.getElementById('top'),"),
    ("non scrivere.</div>':'');", "non scrivere.</div>':''));"),
    ("v.innerHTML=h;", "morfaIn(v,h);"),
    # 2. ascoltatori agganciati una volta sola
    ("tx.addEventListener('input',conta)", "if(!tx.__conta){tx.__conta=1;tx.addEventListener('input',conta)}"),
    ("tx.addEventListener('input',function(){window.__scrivi=tx.value||null})",
     "if(!tx.__scr){tx.__scr=1;tx.addEventListener('input',function(){window.__scrivi=tx.value||null})}"),
    # 3. Notifiche: Attività e Menzioni
    ('<button data-nf="tutte" class="\'+(ntab===\'tutte\'?\'on\':\'\')+\'">Tutte</button>',
     '<button data-nf="tutte" class="\'+(ntab===\'tutte\'?\'on\':\'\')+\'">Attività</button>'),
    ("ntab==='tutte'||o.tp==='men'", "ntab==='tutte'?o.tp!=='men':o.tp==='men'"),
    ("Ancora nessuna notifica.<br>Qui compaiono menzioni, risposte, rilanci e traguardi dei tuoi cori.",
     "Ancora nessuna attività.<br>Qui compaiono applausi, rilanci, risposte, visualizzazioni e traguardi dei tuoi cori. Le menzioni sono nell\\'altra scheda."),
]


PROVA = r'''
/* Solo nel Lab: aggancio per le prove automatiche (prove/prova_curva_ferma.js) */
window.__curvaProva={render:function(){render()},entra:function(t){me=t;code='PROVA';meH=hnd(t);render()},
 vai:function(v,n){vista=v;if(n)ntab=n;render()},notifiche:function(){return notifiche()}};
'''


def applica(t, lab=False):
    for a, b in SOSTITUZIONI:
        n = t.count(a)
        assert n == 1, 'trovato %d volte: %s' % (n, a[:60])
        t = t.replace(a, b)
    k = 'function render(){'
    assert t.count(k) == 1
    return t.replace(k, MORFA.strip() + '\n' + (PROVA.strip() + '\n' if lab else '') + k)


if __name__ == '__main__':
    sito = sys.argv[1]
    qui = os.path.dirname(os.path.abspath(__file__))
    for rel in ('girrr/curva.html', 'stadio/girrr/curva.html'):
        t = open(os.path.join(sito, rel), encoding='utf-8').read()
        out = os.path.join(qui, 'pagine', rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(applica(t, '--lab' in sys.argv))
        print('scritto', out)
