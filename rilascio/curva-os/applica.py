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
  5. Impostazioni (pulsante della luna): Aspetto Automatico, Chiaro o Scuro; suono dell'applauso. Condividi manda anche la
     foto del coro. Anteprima del link per WhatsApp (Open Graph, immagine assets/curva/anteprima-curva.png da pubblicare).
  6. Notifiche con due schede: «Attività» (applausi, rilanci, risposte, visualizzazioni, traguardi) e «Menzioni».

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
 '.post{transition:background-color .6s ease}.post.cv-evidenza{background-color:color-mix(in srgb,var(--tx) 7%,transparent);transition-duration:.15s}'+   /* lampo grigio brevissimo, nessun riquadro colorato */
 '@media (prefers-reduced-motion:reduce){.cv-nuovi{transition:opacity .2s}}';document.head.appendChild(s)})();
/* Link a ogni coro (Claude, 12 novembre 2026): curva.html?coro=CHIAVE apre la Curva su quel coro; un lampo grigio di mezzo secondo fa capire quale */
function cvLink(k){return location.origin+location.pathname+'?coro='+encodeURIComponent(k)}
(function(){var k=null;try{k=new URLSearchParams(location.search).get('coro')}catch(e){}if(!k)return;var n=0,t=setInterval(function(){
 if(++n>80){clearInterval(t);return}
 if(!POSTS||!POSTS.length||!document.querySelector('#vista article.post'))return;clearInterval(t);
 try{var u=new URL(location.href);u.searchParams.delete('coro');history.replaceState(null,'',u.pathname+u.search+u.hash)}catch(e){}
 var i=-1;POSTS.forEach(function(p,j){if(p.k===k)i=j});
 if(i<0){toast('Questo coro non c\'è più');return}
 vista='home';filt='tutti';FEED_SHOW=Math.max(FEED_SHOW,i+5);open[k]=true;render();
 var e=document.querySelector('#vista article.post[data-k="'+(window.CSS&&CSS.escape?CSS.escape(k):k)+'"]');
 if(e){e.scrollIntoView({block:'center'});if(!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)){e.classList.add('cv-evidenza');setTimeout(function(){e.classList.remove('cv-evidenza')},350)}}},300)})();
'''

IMPOSTAZIONI = r'''
/* Impostazioni della Curva (Claude, 12 novembre 2026): il pulsante della luna apre un foglio con
   Aspetto (Automatico, Chiaro, Scuro: Automatico segue il telefono e cambia da solo) e Suoni (applauso con suono). */
function cvAspettoT(v){return v==='auto'?(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'):v}
function cvAspetto(v){window.__cvAspetto=v;try{localStorage.setItem('cv-aspetto',v)}catch(e){}tema(cvAspettoT(v));render()}
/* Di partenza il suono è acceso solo su iPhone e iPad, dove tace con il silenzioso; su Android e sul computer una pagina web
   non può sapere se il telefono è in silenzioso, quindi parte spento e si accende a mano. */
function cvIos(){var u=navigator.userAgent||'';return /iPhone|iPad|iPod/.test(u)||(/Macintosh/.test(u)&&navigator.maxTouchPoints>1)}
function cvSuonoOn(){var v=null;try{v=localStorage.getItem('cv-suoni')}catch(e){}return v===null?cvIos():v==='1'}
function cvSuonoSalva(v){try{localStorage.setItem('cv-suoni',v?'1':'0')}catch(e){}}
/* Suono dell'applauso: due note brevi fatte dal browser (nessun file). Su iPhone tace con il silenzioso (sessione audio «ambient»);
   su Android segue il volume dei contenuti multimediali. */
var cvAC=null;
function cvSuono(){if(!cvSuonoOn())return;try{if(navigator.audioSession)navigator.audioSession.type='ambient';var C=window.AudioContext||window.webkitAudioContext;if(!C)return;
 cvAC=cvAC||new C();if(cvAC.state==='suspended')cvAC.resume();var t=cvAC.currentTime;
 [[740,0],[1110,.07]].forEach(function(n){var o=cvAC.createOscillator(),g=cvAC.createGain();o.type='sine';o.frequency.setValueAtTime(n[0],t+n[1]);
  g.gain.setValueAtTime(.0001,t+n[1]);g.gain.exponentialRampToValueAtTime(.16,t+n[1]+.012);g.gain.exponentialRampToValueAtTime(.0001,t+n[1]+.16);
  o.connect(g);g.connect(cvAC.destination);o.start(t+n[1]);o.stop(t+n[1]+.18)})}catch(e){}}
function cvImpostazioni(){if(document.getElementById('cv-imp')){cvChiudiImp();return}
 var a=window.__cvAspetto||'auto',s=cvSuonoOn(),o=document.createElement('div');o.id='cv-imp';o.className='cv-imp';
 o.innerHTML='<div class="cv-imp-f"></div><div class="cv-imp-p" role="dialog" aria-modal="true" aria-label="Impostazioni della Curva"><i class="cv-imp-m" aria-hidden="true"></i><b>Aspetto</b><div class="cv-imp-seg">'+
  [['auto','Automatico'],['light','Chiaro'],['dark','Scuro']].map(function(x){return '<button type="button" data-asp="'+x[0]+'" aria-pressed="'+(a===x[0])+'">'+x[1]+'</button>'}).join('')+
  '</div><small>Automatico segue il telefono: scuro quando lo è il telefono, anche la sera.</small><b>Suoni</b><div class="cv-imp-seg"><button type="button" data-suono="1" aria-pressed="'+s+'">Sì</button><button type="button" data-suono="0" aria-pressed="'+(!s)+'">No</button></div><small>'+(cvIos()?'Un suono breve quando metti un applauso. Tace quando l\'iPhone è in silenzioso.':'Un suono breve quando metti un applauso. Il sito non può sapere se il telefono è in silenzioso: per questo parte spento, e segue il volume dei contenuti.')+'</small><button type="button" class="cv-imp-ok">Fatto</button></div>';
 document.body.appendChild(o);void o.offsetWidth;o.classList.add('on');
 o.addEventListener('click',function(e){if(e.target.classList.contains('cv-imp-f')||e.target.classList.contains('cv-imp-ok')){cvChiudiImp();return}var b=e.target.closest('button');if(!b)return;
  if(b.dataset.asp)cvAspetto(b.dataset.asp);else if(b.dataset.suono){cvSuonoSalva(b.dataset.suono==='1');if(b.dataset.suono==='1')cvSuono()}else return;
  [].forEach.call(b.parentNode.children,function(x){x.setAttribute('aria-pressed',String(x===b))})});
 var p=o.querySelector('[aria-pressed=true]');if(p)p.focus({preventScroll:true})}
function cvChiudiImp(){var o=document.getElementById('cv-imp');if(!o)return;o.classList.remove('on');setTimeout(function(){o.remove()},320);var g=document.getElementById('tg');if(g)g.focus({preventScroll:true})}
document.addEventListener('keydown',function(e){if(e.key==='Escape')cvChiudiImp()});
if(window.matchMedia){var cvMQ=matchMedia('(prefers-color-scheme: dark)'),cvMQf=function(){if((window.__cvAspetto||'auto')==='auto'){tema(cvAspettoT('auto'));try{render()}catch(e){}}};if(cvMQ.addEventListener)cvMQ.addEventListener('change',cvMQf);else if(cvMQ.addListener)cvMQ.addListener(cvMQf)}
/* Condividi: insieme all'immagine del coro anche la sua foto, se c'è */
function cvFoto(src){if(!src)return Promise.resolve(null);return fetch(src).then(function(r){return r.blob()}).then(function(b){var ty=b.type||'image/jpeg';return new File([b],'foto-coro.'+(/png/.test(ty)?'png':'jpg'),{type:ty})}).catch(function(){return null})}
(function(){var s=document.createElement('style');s.textContent=
 '.cv-imp{position:fixed;inset:0;z-index:90}.cv-imp-f{position:absolute;inset:0;background:rgba(0,0,0,.35);opacity:0;transition:opacity .3s ease}'+
 '.cv-imp-p{position:absolute;left:0;right:0;bottom:0;margin:0 auto;max-width:520px;background:var(--bg);color:var(--tx);border-radius:22px 22px 0 0;padding:10px 20px calc(18px + env(safe-area-inset-bottom));box-shadow:0 -10px 40px rgba(0,0,0,.25);transform:translateY(105%);transition:transform .38s cubic-bezier(.2,.9,.25,1);display:flex;flex-direction:column;gap:8px}'+
 '.cv-imp.on .cv-imp-f{opacity:1}.cv-imp.on .cv-imp-p{transform:none}.cv-imp-m{display:block;width:40px;height:5px;border-radius:3px;background:var(--ln);margin:2px auto 8px}'+
 '.cv-imp-p b{font:800 15px Inter,system-ui,sans-serif;margin-top:6px}.cv-imp-p small{color:var(--mu);font:500 13px/1.4 Inter,system-ui,sans-serif}'+
 '.cv-imp-seg{display:flex;gap:4px;padding:4px;border-radius:14px;background:var(--hv);border:1px solid var(--ln)}'+
 '.cv-imp-seg button{flex:1;border:0;border-radius:10px;padding:11px 6px;background:transparent;color:var(--tx);font:700 14px Inter,system-ui,sans-serif;cursor:pointer;transition:background-color .25s,color .25s}'+
 '.cv-imp-seg button[aria-pressed=true]{background:var(--acc);color:#fff}'+
 '.cv-imp-ok{margin-top:10px;border:0;border-radius:999px;padding:13px;background:var(--tx);color:var(--bg);font:800 15px Inter,system-ui,sans-serif;cursor:pointer}'+
 '@media (min-width:760px){.cv-imp-p{bottom:auto;top:50%;border-radius:22px;transform:translateY(-40%) scale(.96);opacity:0;transition:transform .3s ease,opacity .3s ease}.cv-imp.on .cv-imp-p{transform:translateY(-50%);opacity:1}}'+
 '@media (prefers-reduced-motion:reduce){.cv-imp-p,.cv-imp-f{transition:opacity .2s!important}.cv-imp-p{transform:none!important}}';document.head.appendChild(s)})();
'''

ANTEPRIMA = ('<meta property="og:type" content="website"><meta property="og:site_name" content="O Fant A Girrr">'
             '<meta property="og:title" content="Curva · O Fant A Girrr"><meta property="og:description" content="Cori, applausi e notizie della lega.">'
             '<meta property="og:image" content="https://giandjcosta.github.io/o-fant-a-girrr/assets/curva/anteprima-curva.png">'
             '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">')

SOSTITUZIONI = [
    # impostazioni: aspetto (Automatico, Chiaro, Scuro) e suoni; anteprima del link (WhatsApp)
    ("document.getElementById('tg').onclick=function(){tema(curTema()==='dark'?'light':'dark');render()};",
     "document.getElementById('tg').onclick=function(){cvImpostazioni()};document.getElementById('tg').setAttribute('aria-label','Impostazioni: aspetto e suoni');"),
    ("(function(){var t=null;try{t=localStorage.getItem('cv-tema')}catch(e){}if(!t)t=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';tema(t)})();",
     "(function(){var a=null;try{a=localStorage.getItem('cv-aspetto')}catch(e){}if(a!=='light'&&a!=='dark')a='auto';window.__cvAspetto=a;"
     "tema(a==='auto'?(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'):a)})();   /* Claude: Aspetto Automatico, Chiaro o Scuro (cv-aspetto) */"),
    ('<meta name="theme-color" content="#ffffff" id="tc">', '<meta name="theme-color" content="#ffffff" id="tc">' + ANTEPRIMA),
    # suono dell'applauso
    ("var key=k+'|'+kind,on=!MN[key];", "var key=k+'|'+kind,on=!MN[key];if(on&&kind==='a')cvSuono();"),
    # condividi con la foto del coro
    ("Promise.all([carica(imgP(a,'a')),carica(ph)]).then(function(r){var av=r[0],im=r[1],",
     "Promise.all([carica(imgP(a,'a')),carica(ph),cvFoto(ph)]).then(function(r){var av=r[0],im=r[1],f2=r[2],"),
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
    ("if(navigator.canShare&&navigator.canShare({files:[f]})){navigator.share({files:[f],text:nm(a)+' sulla Curva'}).catch(function(){}).then(riallinea)}",
     "if(navigator.canShare&&navigator.canShare({files:[f]})){var fs=f2&&navigator.canShare({files:[f,f2]})?[f,f2]:[f];navigator.share({files:fs,text:nm(a)+' sulla Curva: '+cvLink(k)}).catch(function(){}).then(riallinea)}"),
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
    return t.replace(k, MORFA.strip() + '\n' + IMPOSTAZIONI.strip() + '\n' + (PROVA.strip() + '\n' if lab else '') + k + 'cvNascondi();')


if __name__ == '__main__':
    sito = sys.argv[1]
    qui = os.path.dirname(os.path.abspath(__file__))
    for rel in ('girrr/curva.html', 'stadio/girrr/curva.html'):
        t = open(os.path.join(sito, rel), encoding='utf-8').read()
        out = os.path.join(qui, 'pagine', rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(applica(t, '--lab' in sys.argv))
        print('scritto', out)
