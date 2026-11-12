#!/usr/bin/env python3
"""Curva: aggiornamento pezzo per pezzo, pillola «Nuovi cori», bozza, link ai cori e Notifiche divise
(Claude, 12 novembre 2026). Prototipo per il Lab.

Oggi la Curva, a ogni ridisegno (cambio di scheda, applauso, aggiornamento ogni minuto), ricostruisce da zero
intestazione, barra in basso e contenuto con innerHTML: i loghi si ricaricano e lo script delle transizioni del sito
(transizioni.js) fa ricomparire in dissolvenza tutto quello che è «nuovo», cioè tutto.
Questo script cambia la pagina così:
  1. morfaIn(el, html): confronta il nuovo HTML con quello che c'è e aggiorna solo quello che è cambiato.
     I cori (article.post) si riconoscono dalla chiave data-k e si tengono anche se cambiano posto; i pezzi che non sono
     cambiati non si toccano (restano foto caricate, immagini nascoste perché mancanti).
     Intestazione e barra in basso restano ferme: cambia solo la scheda o la sezione accesa.
     Campi di testo: quello in cui stai scrivendo resta; gli altri tornano come li disegna la pagina (come prima);
     coro e risposta si svuotano dopo l'invio.
  2. Due ascoltatori del campo di scrittura si agganciano una volta sola (con gli elementi tenuti si sarebbero raddoppiati).
  3. Pillola «Nuovi cori»: l'aggiornamento di ogni minuto non riempie più il feed mentre lo leggi; se ci sono davvero
     cori nuovi e sei sceso, compare la pillola; toccandola il feed risale e si aggiorna.
  4. Bozza del coro (resta se esci, finché non lo lanci) e link a ogni coro (curva.html?coro=CHIAVE, anche in «Condividi»).
  5. Notifiche con due schede: «Attività» (applausi, rilanci, risposte, visualizzazioni, traguardi) e «Menzioni».

Uso: python3 rilascio/curva-os/applica.py CARTELLA_DEL_SITO [--lab]   (CARTELLA_DEL_SITO: una copia di gh-pages)
Con --lab aggiunge window.__curvaProva, l'aggancio per le prove automatiche (entrare come squadra, ridisegnare,
aprire le Notifiche, simulare cori nuovi): solo nel Lab, al rilascio si genera senza.
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
 if(a.tagName==='TEXTAREA'||a.tagName==='INPUT'||a.tagName==='SELECT'){   /* il campo in cui stai scrivendo resta; gli altri tornano come li disegna la pagina, come prima */
  if(a!==document.activeElement&&a.type!=='file'){if(a.tagName==='SELECT')a.selectedIndex=b.selectedIndex;else if(a.type==='checkbox'||a.type==='radio')a.checked=b.checked;else if(a.value!==b.value)a.value=b.value}
  return}
 if(!b.firstChild&&a.firstChild&&a.classList.contains('pimg')&&a.hasAttribute('data-id'))return;   /* foto già caricata */
 mfFigli(a,b)}
/* Bozza del coro (Claude, 12 novembre 2026): quello che scrivi resta se esci e rientri, finché non lanci il coro */
function cvBozzaK(){return 'cv-bozza-'+(me||'')}
function cvBozza(){try{return localStorage.getItem(cvBozzaK())||''}catch(e){return ''}}
function cvBozzaSalva(v){try{if(v)localStorage.setItem(cvBozzaK(),v);else localStorage.removeItem(cvBozzaK())}catch(e){}}
function cvSvuota(){var t=document.getElementById('tx');if(t)t.value='';cvBozzaSalva('')}
/* Pillola «Nuovi cori» (Claude, 12 novembre 2026): l'aggiornamento di ogni minuto non riempie più il feed mentre lo leggi.
   Se in cima alla scheda ci sono davvero cori nuovi e tu sei sceso, compare la pillola; toccandola il feed risale e si aggiorna.
   Se sei già in alto (o risali da solo) si aggiorna subito, come prima. */
var cvPend=false;
function cvFiltro(p){var k=acc(p.a).k;return filt==='tutti'||(filt==='seguiti'&&(isFol(p.a)||p.a===meH))||(filt==='squadre'&&k==='sq')||(filt==='notizie'&&(k==='org'||k==='pro'))}
function cvNuovi(){
 if(vista!=='home'||window.scrollY<150){renderFermo();return}
 var sh={},max=0;[].forEach.call(document.querySelectorAll('#vista article.post[data-k]'),function(a){sh[a.getAttribute('data-k')]=1});
 (POSTS||[]).forEach(function(p){if(sh[p.k]&&p.ts>max)max=p.ts});
 var L=costruisci().filter(function(p){return !sh[p.k]&&p.ts>max&&p.a!==meH&&cvFiltro(p)});
 if(!L.length){renderFermo();return}
 cvMostra(L)}
function cvPillola(){var b=document.getElementById('cv-nuovi');if(!b){b=document.createElement('button');b.id='cv-nuovi';b.className='cv-nuovi';b.type='button';b.onclick=cvSali;document.body.appendChild(b)}return b}
function cvMostra(L){var b=cvPillola(),visti={},av=[];L.forEach(function(p){if(!visti[p.a]&&av.length<3){visti[p.a]=1;av.push(AV(acc(p.a),'cvn-av'))}});
 b.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg><span class="cvn-avs">'+av.join('')+'</span><span>Nuovi cori</span>';
 b.setAttribute('aria-label','Nuovi cori: torna su e aggiorna');cvPosiziona(b);cvPend=true;b.classList.add('on')}
function cvPosiziona(b){var t=document.getElementById('top'),c=document.querySelector('.col'),rt=t?t.getBoundingClientRect():null,rc=c?c.getBoundingClientRect():null;
 b.style.top=((rt?Math.max(rt.bottom,0):0)+10)+'px';b.style.left=(rc?rc.left+rc.width/2:innerWidth/2)+'px'}
function cvNascondi(){var b=document.getElementById('cv-nuovi');if(b)b.classList.remove('on');cvPend=false}
function cvSali(){cvNascondi();var lisc=!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches),fatto=false,t0=Date.now();
 function vai(){if(fatto)return;fatto=true;render()}
 window.scrollTo({top:0,behavior:lisc?'smooth':'auto'});if(!lisc)return vai();
 (function aspetta(){if(window.scrollY<4||Date.now()-t0>1000)vai();else requestAnimationFrame(aspetta)})()}
window.addEventListener('scroll',function(){if(cvPend&&window.scrollY<4){cvNascondi();render()}},{passive:true});
window.addEventListener('resize',function(){var b=document.getElementById('cv-nuovi');if(b&&cvPend)cvPosiziona(b)});
(function(){var s=document.createElement('style');s.textContent=
 '.cv-nuovi{position:fixed;z-index:25;display:flex;align-items:center;gap:8px;border:0;border-radius:999px;padding:7px 15px 7px 10px;background:var(--blu);color:#fff;font:700 14px Inter,system-ui,sans-serif;box-shadow:0 6px 18px rgba(0,0,0,.25);cursor:pointer;opacity:0;pointer-events:none;transform:translate(-50%,-14px) scale(.92);transition:opacity .25s ease,transform .35s cubic-bezier(.2,.9,.3,1.2);-webkit-tap-highlight-color:transparent}'+
 '.cv-nuovi.on{opacity:1;pointer-events:auto;transform:translate(-50%,0)}.cv-nuovi svg{width:16px;height:16px;flex:none}'+
 '.cvn-avs{display:flex}.cvn-avs .av{width:22px!important;height:22px!important;min-width:0!important;font-size:9px!important;border:2px solid currentColor;margin:0 0 0 -7px!important;flex:none}.cvn-avs .av:first-child{margin-left:0!important}'+
 '.post{transition:background-color 1.4s ease}.post.cv-evidenza{background-color:color-mix(in srgb,var(--blu) 16%,transparent);transition:none}'+
 '@media (prefers-reduced-motion:reduce){.cv-nuovi{transition:opacity .2s}}';document.head.appendChild(s)})();
/* Link a ogni coro (Claude, 12 novembre 2026): curva.html?coro=CHIAVE apre la Curva su quel coro e lo evidenzia */
function cvLink(k){return location.origin+location.pathname+'?coro='+encodeURIComponent(k)}
(function(){var k=null;try{k=new URLSearchParams(location.search).get('coro')}catch(e){}if(!k)return;var n=0,t=setInterval(function(){
 if(++n>80){clearInterval(t);return}
 if(!POSTS||!POSTS.length||!document.querySelector('#vista article.post'))return;clearInterval(t);
 try{var u=new URL(location.href);u.searchParams.delete('coro');history.replaceState(null,'',u.pathname+u.search+u.hash)}catch(e){}
 var i=-1;POSTS.forEach(function(p,j){if(p.k===k)i=j});
 if(i<0){toast('Questo coro non c\'è più');return}
 vista='home';filt='tutti';FEED_SHOW=Math.max(FEED_SHOW,i+5);open[k]=true;render();
 var e=document.querySelector('#vista article.post[data-k="'+(window.CSS&&CSS.escape?CSS.escape(k):k)+'"]');
 if(e){e.scrollIntoView({block:'center'});e.classList.add('cv-evidenza');setTimeout(function(){e.classList.remove('cv-evidenza')},1800)}},300)})();
'''

SOSTITUZIONI = [
    # 1. intestazione, barra in basso e contenuto
    ("document.getElementById('nav').innerHTML=", "morfaIn(document.getElementById('nav'),"),
    ("Lancia un coro</button>'\n}", "Lancia un coro</button>')\n}"),
    ("document.getElementById('top').innerHTML=", "morfaIn(document.getElementById('top'),"),
    ("non scrivere.</div>':'');", "non scrivere.</div>':''));"),
    ("v.innerHTML=h;", "morfaIn(v,h);"),
    # 2. ascoltatori agganciati una volta sola; bozza del coro
    ("tx.addEventListener('input',conta)",
     "if(!tx.__conta){tx.__conta=1;tx.addEventListener('input',conta);tx.addEventListener('input',function(){cvBozzaSalva(tx.value)})}if(!tx.value&&cvBozza())tx.value=cvBozza()"),
    ("tx.addEventListener('input',function(){window.__scrivi=tx.value||null})",
     "if(!tx.__scr){tx.__scr=1;tx.addEventListener('input',function(){window.__scrivi=tx.value||null})}"),
    # 3. pillola: l'aggiornamento di ogni minuto passa da cvNuovi
    ("if(!occupato()&&firma()!==f0)renderFermo()", "if(!occupato()&&firma()!==f0)cvNuovi()"),
    # campi svuotati dopo l'invio (gli elementi ora restano, prima si ricreavano vuoti)
    ("pimg=null;if(vista!=='u'){filt='tutti'}", "pimg=null;cvSvuota();if(vista!=='u'){filt='tutti'}"),
    ("ev1('curva/risposta','Curva: risposta');open[k]=true;", "ev1('curva/risposta','Curva: risposta');i.value='';open[k]=true;"),
    # 4. link al coro nella condivisione
    ("navigator.share({files:[f],text:nm(a)+' sulla Curva'})", "navigator.share({files:[f],text:nm(a)+' sulla Curva: '+cvLink(k)})"),
    ("toast('Immagine salvata')}",
     "toast('Immagine salvata');try{navigator.clipboard.writeText(cvLink(k)).then(function(){toast('Immagine salvata e link del coro copiato')}).catch(function(){})}catch(e){}}"),
    # 5. Notifiche: Attività e Menzioni
    ('<button data-nf="tutte" class="\'+(ntab===\'tutte\'?\'on\':\'\')+\'">Tutte</button>',
     '<button data-nf="tutte" class="\'+(ntab===\'tutte\'?\'on\':\'\')+\'">Attività</button>'),
    ("ntab==='tutte'||o.tp==='men'", "ntab==='tutte'?o.tp!=='men':o.tp==='men'"),
    ("Ancora nessuna notifica.<br>Qui compaiono menzioni, risposte, rilanci e traguardi dei tuoi cori.",
     "Ancora nessuna attività.<br>Qui compaiono applausi, rilanci, risposte, visualizzazioni e traguardi dei tuoi cori. Le menzioni sono nell\\'altra scheda."),
]


PROVA = r'''
/* Solo nel Lab: aggancio per le prove automatiche (prove/prova_curva_ferma.js) */
window.__curvaProva={render:function(){render()},entra:function(t){me=t;code='PROVA';meH=hnd(t);render()},
 vai:function(v,n){vista=v;if(n)ntab=n;render()},notifiche:function(){return notifiche()},nuovi:function(){cvNuovi()},pubblica:function(){lancia()}};
'''


def applica(t, lab=False):
    for a, b in SOSTITUZIONI:
        n = t.count(a)
        assert n == 1, 'trovato %d volte: %s' % (n, a[:60])
        t = t.replace(a, b)
    k = 'function render(){'
    assert t.count(k) == 1
    # render() nasconde la pillola: dopo un ridisegno i cori nuovi sono già nel feed
    return t.replace(k, MORFA.strip() + '\n' + (PROVA.strip() + '\n' if lab else '') + k + 'cvNascondi();')


if __name__ == '__main__':
    sito = sys.argv[1]
    qui = os.path.dirname(os.path.abspath(__file__))
    for rel in ('girrr/curva.html', 'stadio/girrr/curva.html'):
        t = open(os.path.join(sito, rel), encoding='utf-8').read()
        out = os.path.join(qui, 'pagine', rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(applica(t, '--lab' in sys.argv))
        print('scritto', out)
