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

PERSONAGGI = r'''
/* Nuovi account della Curva (Claude, 12 novembre 2026): le frasi sono in curva-banca.js (PERS_N, dal giorno TAGLIO_N) */
(function(){var P=location.pathname.indexOf('/stadio/')>=0?'../../assets/':'../assets/';
 [['rodrigo_saudade','Rodrigo Saudade','Brasiliano a Torino. Joga bonito, tifa forte, cucina feijoada.','#1f9d55','#f2c230'],
  ['klaus_puenktlich','Klaus Pünktlich','Ingegnere bavarese. Formazione consegnata sempre alle 14:59. Ordnung muss sein.','#1b1b1b','#c8102e'],
  ['elpibe_rosario','El Pibe de Rosario','Fútbol, mate y garra. Da Rosario con passione.','#6cace4','#1c3f6e'],
  ['mister_tea','Mister Tea','Londra, 1966. Tea at five, formazione alle sei.','#1d3a6e','#b22234'],
  ['jp_chic','Jean-Pierre Chic','Il calcio è moda. Il 3-5-2 torna sempre. Voilà.','#1f3a93','#e5e5e5'],
  ['mamma_del_portiere','La Mamma del Portiere','Il portiere non sbaglia mai. Sbaglia la difesa.','#d17a22','#5c2e0b'],
  ['meteo_girrr','Il Meteorologo','Previsioni del tempo e dei gol. Affidabilità variabile.','#4ea8de','#1e3a5f'],
  ['ultra_da_divano','Ultrà da Divano','Sciarpa, telecomando e cori. Dal divano, dal 2009.','#8d0801','#1b1b1b'],
  ['pentito_del_fanta','Il Fantallenatore Pentito','Ogni lunedì mi pento. Ogni sabato ricomincio.','#6c757d','#343a40'],
  ['prof_di_mate','La Prof di Matematica','Statistica, probabilità e compiti per casa. Anche per voi.','#2a9d8f','#264653'],
  ['bomber99','xX_Bomber99_Xx','fanta, gaming e pizza. nn rispondo ai vocali','#7b2cbf','#240046'],
  ['utente84629','utente84629','','#8a8f98','#4a4f57']
 ].forEach(function(x){add(x[0],x[1],'fan','',x[2],[x[3],x[4]])});
 add('pizzeria_fuorigioco','Pizzeria Fuorigioco','fan','','La pizza della lega. Forno a legna e chiacchiere da bancone.',['#c8102e','#1e5631']);
 ACC.pizzeria_fuorigioco.img=P+'loghi/sponsor-pizzeria-fuorigioco.png';
 add('radio_girrr','Radio Girrr','org','oro','La radio della lega. Le voci della giornata, in onda dopo ogni turno.',['#13224f','#ffd166']);
 add('var_girrr','Il VAR del Girrr','org','oro','Gli episodi della giornata rivisti al monitor. La Moviola della lega.',['#0b1220','#3d93d6']);
 try{(CVB.COMUNI_N||[]).forEach(function(u){var h=hue(u[0]);add(u[0],u[1],'u','',BIOU[h%BIOU.length],['hsl('+h+' 45% 38%)','hsl('+((h+50)%360)+' 40% 22%)'])})}catch(e){}
})();
/* Immagini nuove dei personaggi, disegnate con i dati veri della lega (risultati, classifica, prossimo turno) */
function mpN(s){s=String(s||'');return s==='The Blue brothers'?'The Blues Brothers':s}   /* i nomi delle squadre come li scrive la lega (stif dc minuscolo); The Blues Brothers come in nomi.js */
var MEMEPLUS={
 lavagna_ris:function(c,T,PK,n,cx,W,H,F){var CH="'Marker Felt','Comic Sans MS','Segoe Print',cursive",R=cx.ris||[];c.fillStyle='#24382c';c.fillRect(0,0,W,H);c.strokeStyle='#8b5a2b';c.lineWidth=22;c.strokeRect(11,11,W-22,H-22);
  for(var i=0;i<30;i++){c.fillStyle='rgba(255,255,255,'+(.02+(i%3)*.01)+')';c.fillRect((i*137)%W,(i*71)%H,120,2)}
  T('BAR SPORT',W/2,82,'800 50px '+CH,'#f4f1de','center');T('Risultati della '+(cx.g||'')+'ª giornata',W/2,124,'600 28px '+CH,'#cfd8c4','center');
  R.slice(0,5).forEach(function(m,i){var y=180+i*62,g=String(m[2]).split('-');T(mpN(m[0]),W/2-70,y,'700 30px '+CH,'#f4f1de','right',300);T(g[0]+' - '+g[1],W/2,y,'800 34px '+CH,'#ffd166','center');T(mpN(m[1]),W/2+70,y,'700 30px '+CH,'#f4f1de','left',300)});
  T(PK(['Caffè offerto a chi ha vinto','Chi ha perso offre il cornetto','Il barista commenta gratis'],2),W/2,H-40,'600 26px '+CH,'#cfd8c4','center')},
 epoca2:function(c,T,PK,n,cx,W,H,F){var EP=PK([['Anno 1966 · la radiolina in tribuna','Si ascoltava tutto, si vedeva poco.'],['Anno 1974 · il pallone di cuoio','Pesava come un mattone. Ed era bellissimo.'],['Anno 1969 · la gita allo stadio','Partenza alle sei, panino col salame.'],['Anno 1977 · la squadra del paese','Maglie cucite dalla sarta, numeri col pennarello.'],['Anno 1963 · il campo di terra','Le righe le tracciava il custode, a occhio.'],['Anno 1981 · la televisione del bar','Tutto il paese davanti a un televisore solo.']],0);
  c.fillStyle='#d9c7a0';c.fillRect(0,0,W,H);c.fillStyle='#f4ead2';c.fillRect(70,40,W-140,H-80);var g=c.createLinearGradient(0,90,0,H-150);g.addColorStop(0,'#8a7354');g.addColorStop(1,'#4b3a26');c.fillStyle=g;c.fillRect(100,70,W-200,H-210);
  var k=n(1,3);c.fillStyle='rgba(30,20,10,.75)';for(var i=0;i<(k===0?7:k===1?5:9);i++){var x=150+i*((W-300)/(k===0?6:k===1?4:8)),y=H-210-20-(i%2)*30;c.beginPath();c.arc(x,y-60,22,0,7);c.fill();c.fillRect(x-24,y-38,48,60)}
  if(k===1){c.fillStyle='rgba(240,230,210,.8)';c.beginPath();c.arc(W/2,H-180,26,0,7);c.fill()}
  var v=c.createRadialGradient(W/2,H/2-40,100,W/2,H/2-40,460);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(60,35,10,.5)');c.fillStyle=v;c.fillRect(100,70,W-200,H-210);
  T(EP[0],W/2,H-98,"italic 700 30px Georgia,serif",'#3b2a14','center',W-180);T(EP[1],W/2,H-62,"italic 22px Georgia,serif",'#5b4630','center',W-180)},
 cartolina:function(c,T,PK,n,cx,W,H,F){var R=cx.ris||[],m=cx.vinc&&cx.sc?[cx.vinc,cx.perd,cx.sc]:(R.length?R[n(0,R.length)]:null);   /* la stessa partita del testo, se c'è */c.fillStyle='#fdf6e3';c.fillRect(0,0,W,H);
  var g=c.createLinearGradient(0,0,0,H);g.addColorStop(0,'#38b6ff');g.addColorStop(.6,'#ffd166');g.addColorStop(.61,'#1f9d55');g.addColorStop(1,'#0b6e3a');c.fillStyle=g;c.fillRect(30,30,W/2-40,H-60);
  c.fillStyle='#ffe66d';c.beginPath();c.arc(150,120,48,0,7);c.fill();c.fillStyle='#14532d';c.beginPath();c.moveTo(30,H-120);c.quadraticCurveTo(200,H-260,W/2-10,H-130);c.lineTo(W/2-10,H-30);c.lineTo(30,H-30);c.fill();
  T('SAUDAÇÕES',W/4+5,H/2+20,'900 46px '+F,'#ffffff','center',W/2-80);c.fillStyle='#c9b98f';c.fillRect(W/2+5,40,2,H-80);
  c.strokeStyle='#b23a48';c.lineWidth=4;c.setLineDash([6,6]);c.strokeRect(W-170,50,120,140);c.setLineDash([]);T('RIO',W-110,130,'900 34px '+F,'#b23a48','center');
  var H1="'Segoe Print','Comic Sans MS',cursive";T('Ciao ragazzi!',W/2+40,250,'700 30px '+H1,'#1d3557');
  T(m?'Qui tutti parlano di '+mpN(m[0]):'Qui si parla solo di calcio,',W/2+40,300,'26px '+H1,'#1d3557','left',W/2-80);T(m?m[2]+' contro '+mpN(m[1])+'.':'e io penso alla lega.',W/2+40,340,'26px '+H1,'#1d3557','left',W/2-80);
  T('Saudade, Rodrigo',W-60,H-70,'700 26px '+H1,'#1d3557','right')},
 tabelle:function(c,T,PK,n,cx,W,H,F){var L=cx.cls||[];c.fillStyle='#f5f5f2';c.fillRect(0,0,W,H);[['#000',0],['#dd0000',1],['#ffce00',2]].forEach(function(s){c.fillStyle=s[0];c.fillRect(0,s[1]*10,W,10)});
  T('TABELLE',40,90,'900 48px '+F,'#111');T((cx.g||'')+'. SPIELTAG · O FANT A GIRRR',W-40,88,'700 22px '+F,'#555','right');
  T('PLATZ',40,140,'800 18px '+F,'#777');T('MANNSCHAFT',140,140,'800 18px '+F,'#777');T('PUNKTE',W-40,140,'800 18px '+F,'#777','right');
  L.slice(0,6).forEach(function(t,i){var y=190+i*58;c.fillStyle=i%2?'#ffffff':'#ecece6';c.fillRect(30,y-38,W-60,54);T(String(i+1),60,y,'900 32px '+F,i===0?'#dd0000':'#111','center');T(mpN(t[0]),140,y,'700 30px '+F,'#111','left',520);T(String(t[1]),W-50,y,'900 32px '+F,'#111','right')});
  T('Ordnung muss sein.',W/2,H-18,'italic 600 20px '+F,'#555','center')},
 meteo:function(c,T,PK,n,cx,W,H,F){var L=cx.prox||[];var g=c.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1e3a5f');g.addColorStop(1,'#4ea8de');c.fillStyle=g;c.fillRect(0,0,W,H);
  T('PREVISIONI',40,70,'900 44px '+F,'#fff');T((cx.gn||'')+'ª giornata · Gol e nuvole',W-40,68,'700 22px '+F,'#d7ecff','right');
  function sole(x,y){c.fillStyle='#ffd166';c.beginPath();c.arc(x,y,18,0,7);c.fill()}function nuvola(x,y,s){c.fillStyle=s||'#f1f5f9';c.beginPath();c.arc(x-14,y,14,0,7);c.arc(x+2,y-8,18,0,7);c.arc(x+18,y,13,0,7);c.fill();c.fillRect(x-28,y,58,14)}
  L.slice(0,5).forEach(function(m,i){var y=135+i*80,k=n(i+2,4);c.fillStyle='rgba(255,255,255,.12)';c.fillRect(30,y-30,W-60,66);T(mpN(m[0])+' – '+mpN(m[1]),60,y+12,'700 28px '+F,'#fff','left',560);
   var x=W-100;if(k===0)sole(x,y+2);else if(k===1){sole(x-8,y-4);nuvola(x+6,y+8)}else if(k===2){nuvola(x,y,'#cbd5e1');c.strokeStyle='#bfe3ff';c.lineWidth=3;for(var j=0;j<3;j++){c.beginPath();c.moveTo(x-16+j*14,y+20);c.lineTo(x-22+j*14,y+34);c.stroke()}}else{nuvola(x,y,'#94a3b8');c.fillStyle='#ffd166';c.beginPath();c.moveTo(x,y+16);c.lineTo(x-8,y+32);c.lineTo(x+2,y+30);c.lineTo(x-4,y+44);c.lineTo(x+10,y+24);c.lineTo(x,y+26);c.fill()}});
  T('Affidabilità della previsione: variabile.',W/2,H-16,'italic 600 18px '+F,'#e0f2fe','center')},
 pizza:function(c,T,PK,n,cx,W,H,F){var L=cx.cls||[],R=cx.ris||[];c.fillStyle='#fff8ec';c.fillRect(0,0,W,H);for(var i=0;i<W;i+=40){c.fillStyle=(i/40)%2?'#c8102e':'#fff8ec';c.fillRect(i,0,40,24);c.fillRect(i,H-24,40,24)}
  T('PIZZERIA FUORIGIOCO',W/2,82,'900 40px Georgia,serif','#1e5631','center');T('Il menù della '+(cx.g||'')+'ª giornata',W/2,118,'italic 24px Georgia,serif','#7a5c3a','center');
  var v=[['La Capolista',L[0]?'Dedicata a '+mpN(L[0][0])+': in cima anche al menù':'Mozzarella e ambizione','9 €'],['La Rimonta',L[2]?'Per '+mpN(L[2][0])+', terza: ci crede ancora':'Pomodoro e speranza','8 €'],['La Diavola del risultato',R[0]?mpN(R[0][0])+' '+R[0][2]+' '+mpN(R[0][1])+': piccante':'Piccante come una sconfitta','8,50 €'],['La Margherita del lunedì','Semplice, per ricominciare','6 €']];
  v.forEach(function(x,i){var y=185+i*82;T(x[0],60,y,'700 30px Georgia,serif','#1e1e1e');T(x[1],60,y+30,'italic 20px Georgia,serif','#6b5b4b','left',620);T(x[2],W-60,y,'700 28px Georgia,serif','#c8102e','right')})},
 onda:function(c,T,PK,n,cx,W,H,F){var L=cx.prox||[],m=L[0];c.fillStyle='#0d1430';c.fillRect(0,0,W,H);c.fillStyle='#d62839';c.beginPath();c.arc(70,70,12,0,7);c.fill();T('ON AIR',96,80,'900 30px '+F,'#fff');
  T('RADIO GIRRR',W/2,180,'900 72px '+F,'#ffd166','center');T('La puntata della '+(cx.g||'')+'ª giornata',W/2,230,'700 28px '+F,'#e5e7eb','center');
  for(var i=0;i<46;i++){var h=20+((n(i%9,7)+i*13)%70);c.fillStyle=i%2?'#3d93d6':'#5fb0ef';c.fillRect(70+i*17,330-h/2,10,h)}
  if(m)T('Prossimo turno: '+mpN(m[0])+' – '+mpN(m[1]),W/2,H-60,'700 26px '+F,'#cbd5e1','center',W-80)},
 var:function(c,T,PK,n,cx,W,H,F){var R=cx.ris||[],m=cx.vinc&&cx.sc?[cx.vinc,cx.perd,cx.sc]:(R.length?R[n(0,R.length)]:null);   /* la stessa partita del testo, se c'è */c.fillStyle='#0b1220';c.fillRect(0,0,W,H);c.fillStyle='#1f2937';c.fillRect(110,60,W-220,H-150);c.fillStyle='#0f172a';c.fillRect(126,76,W-252,H-182);
  c.strokeStyle='#3d93d6';c.lineWidth=6;c.strokeRect(126,76,W-252,H-182);T('CHECK VAR',W/2,140,'900 52px '+F,'#3d93d6','center');
  if(m){var g=String(m[2]).split('-');T(mpN(m[0]),W/2-120,240,'800 30px '+F,'#fff','right',260);T(g[0]+' - '+g[1],W/2,244,'900 46px '+F,'#ffd166','center');T(mpN(m[1]),W/2+120,240,'800 30px '+F,'#fff','left',260)}
  c.fillStyle='#16a34a';c.fillRect(W/2-170,290,340,54);T('DECISIONE CONFERMATA',W/2,327,'900 26px '+F,'#fff','center');c.fillStyle='#374151';c.fillRect(W/2-60,H-90,120,30);c.fillRect(W/2-140,H-60,280,14);
  T('Il VAR del Girrr · '+(cx.g||'')+'ª giornata',W/2,H-14,'700 18px '+F,'#9ca3af','center')},
 quaderno:function(c,T,PK,n,cx,W,H,F){var L=cx.cls||[];c.fillStyle='#fdfdf8';c.fillRect(0,0,W,H);c.strokeStyle='#cfe3f3';c.lineWidth=1;for(var x=0;x<W;x+=26){c.beginPath();c.moveTo(x,0);c.lineTo(x,H);c.stroke()}for(var y=0;y<H;y+=26){c.beginPath();c.moveTo(0,y);c.lineTo(W,y);c.stroke()}
  c.strokeStyle='#e57373';c.lineWidth=3;c.beginPath();c.moveTo(80,0);c.lineTo(80,H);c.stroke();var HW="'Segoe Print','Comic Sans MS',cursive";
  T('Compito di matematica',110,70,'700 36px '+HW,'#1d3557');
  if(L.length>1){var d=L[0][1]-L[1][1];T('Problema: '+mpN(L[0][0])+' ha '+L[0][1]+' punti,',110,140,'26px '+HW,'#1d3557','left',W-150);T(mpN(L[1][0])+' ne ha '+L[1][1]+'. Quanti punti di distacco?',110,182,'26px '+HW,'#1d3557','left',W-150);
   T(L[0][1]+' − '+L[1][1]+' = '+d,110,260,'700 40px '+HW,'#1d3557');T(d===0?'Risposta: nessuno. Pari!':'Risposta: '+d+(d===1?' punto.':' punti.'),110,320,'700 30px '+HW,'#c62828')}
  T('Bravi. Ma studiate di più.',W-60,H-40,'italic 700 26px '+HW,'#c62828','right')},
 coreo:function(c,T,PK,n,cx,W,H,F){var cols=[['#d62839','#ffffff'],['#1d3557','#ffd166'],['#0b6e3a','#ffffff'],['#000','#ffd166']][n(0,4)];c.fillStyle='#111';c.fillRect(0,0,W,H);
  for(var y=0;y<9;y++)for(var x=0;x<18;x++){c.fillStyle=(x+y)%2?cols[0]:cols[1];if(y>=3&&y<=5)c.fillStyle=cols[0];c.fillRect(x*50+2,y*50+2,46,46)}
  T(PK(['CURVA GIRRR','SEMPRE CON VOI','NOI CI SIAMO','CANTA LA CURVA'],3),W/2,222,'900 64px '+F,cols[1],'center',W-60);   /* nessuna squadra a caso: il testo del coro può parlare di un'altra */T('Coreografia dal divano · 3 cuscini, 1 coperta',W/2,H-20,'700 20px '+F,'#ddd','center')}
};
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
    # immagini nuove dei personaggi (MEMEPLUS, in PERSONAGGI)
    ("if(t==='lavagna'){", "if(MEMEPLUS[t]){MEMEPLUS[t](c,T,PK,n,cx,W,H,F)}else if(t==='lavagna'){"),
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
 vai:function(v,n){vista=v;if(n)ntab=n;render()},notifiche:function(){return notifiche()},nuovi:function(){cvNuovi()},pubblica:function(){lancia()},dati:function(){return {D:D,SQ:SQ,ST:ST}},
 img:function(t){var c={sq:ST.cls[0].n,sq2:ST.cls[1].n,gio:'',g:ST.ult&&ST.ult.n,ris:ST.ult?ST.ult.m.map(function(m){return[m[0],m[3],m[4]]}):[],cls:ST.cls.slice(0,6).map(function(x){return[x.n,x.pt]}),gn:ST.next&&ST.next.n,prox:ST.next?ST.next.m.map(function(m){return[m[0],m[3]]}):[]};return memeImg({k:'prova-'+t,imgt:t,cx:c})}};
'''


def applica(t, lab=False):
    for a, b in SOSTITUZIONI:
        n = t.count(a)
        assert n == 1, 'trovato %d volte: %s' % (n, a[:60])
        t = t.replace(a, b)
    k = 'function render(){'
    assert t.count(k) == 1
    # render() nasconde la pillola: dopo un ridisegno i cori nuovi sono già nel feed
    return t.replace(k, MORFA.strip() + '\n' + IMPOSTAZIONI.strip() + '\n' + PERSONAGGI.strip() + '\n' + (PROVA.strip() + '\n' if lab else '') + k + 'cvNascondi();')


if __name__ == '__main__':
    sito = sys.argv[1]
    qui = os.path.dirname(os.path.abspath(__file__))
    for rel in ('girrr/curva.html', 'stadio/girrr/curva.html'):
        t = open(os.path.join(sito, rel), encoding='utf-8').read()
        out = os.path.join(qui, 'pagine', rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(applica(t, '--lab' in sys.argv))
        print('scritto', out)
