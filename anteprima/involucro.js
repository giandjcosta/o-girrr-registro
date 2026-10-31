/* Cornice Anteprima del Registro: conserva il percorso quando cambia la grafica. */
(function(){
'use strict';
var base=new URL('../',location.href),dir=new URL('anteprima/5.3/',base);
var frame=document.getElementById('f'),toggle=document.getElementById('tg');
var la=document.getElementById('la'),ln=document.getElementById('ln');
function home(m){return new URL('index-'+(m==='n'?'stadio':'lega')+'.html',dir)}
function pulisci(u){var x=new URL(u,location.href);x.searchParams.delete('_t');return x}
function interno(u){return u.origin===base.origin&&u.pathname.indexOf(base.pathname)===0}
function modo(u){
 var x=new URL(u,location.href);
 return x.searchParams.get('skin')==='stadio'||/\/ufficiale\/nuovo\//.test(x.pathname)||/\/(index|home|tabellone|albo|curva|notifiche|campo)-stadio\.html$/.test(x.pathname)||/\/anteprima\/(index\.html)?$/.test(x.pathname)?'n':'a';
}
function conv(u,m){
 var x=pulisci(u),skin=m==='n'?'stadio':'lega',app=m==='n'?'index.html':'attuale.html';
 if(!interno(x))return home(m);
 var rel=x.pathname.slice(base.pathname.length),file=rel.split('/').pop();
 var legacy=/^ufficiale\/(nuovo\/)?girrr\//.test(rel);
 var modern=rel.indexOf('anteprima/')===0;
 if(legacy){
  var dest={'':'index','index.html':'index','albo.html':'albo','tabellone.html':'tabellone','curva.html':'curva','notifiche.html':'notifiche'}[file];
  if(dest){x.pathname=dir.pathname+dest+'-'+skin+'.html';return x}
  if(file==='app.html'&&x.hash==='#oro'){x.pathname=dir.pathname+'albo-'+skin+'.html';return x}
  x.pathname=base.pathname+'ufficiale/'+(m==='n'?'nuovo/':'')+'girrr/'+file;return x;
 }
 if(modern){
  var section=/^(index|home|tabellone|albo|curva|notifiche|campo)-(lega|stadio)\.html$/.exec(file);
  if(section){x.pathname=dir.pathname+(section[1]==='home'?'index':section[1])+'-'+skin+'.html';if(section[1]==='campo')x.searchParams.set('skin',skin);return x}
  if(file==='campo.html'){x.pathname=dir.pathname+'campo-'+skin+'.html';x.searchParams.set('skin',skin);return x}
  if(file==='totogirrr-52.html'){x.pathname=base.pathname+'anteprima/totogirrr-52.html';x.searchParams.set('skin',skin);return x}
  if(file==='index.html'||file==='attuale.html'||file===''){
   if(!x.hash)return home(m);
   if(x.hash==='#oro'){x.pathname=dir.pathname+'albo-'+skin+'.html';return x}
   x.pathname=base.pathname+'anteprima/'+app;return x;
  }
 }
 return home(m);
}
function fresco(u){var x=new URL(u);x.searchParams.set('_t',Date.now());return x.href}
function mark(m){toggle.setAttribute('aria-checked',String(m==='n'));la.className=m==='a'?'on':'';ln.className=m==='n'?'on':''}
function scrivi(k,v){try{localStorage.setItem(k,v)}catch(e){}}
function attuale(){try{var u=frame.contentWindow.location.href;return u!=='about:blank'?u:null}catch(e){return null}}
function carica(u,m){mark(m);scrivi('orr_gv',m);frame.classList.add('out');frame.src=fresco(u)}
function cambia(m){var u=attuale();carica(u?conv(u,m):home(m),m)}
toggle.addEventListener('click',function(){cambia(toggle.getAttribute('aria-checked')==='true'?'a':'n')});
window.addEventListener('message',function(e){
 if(e.origin===location.origin&&e.source===frame.contentWindow&&e.data&&(e.data.orrGrafica==='a'||e.data.orrGrafica==='n'))cambia(e.data.orrGrafica);
});
frame.addEventListener('load',function(){
 frame.classList.remove('out');var u=attuale();if(!u)return;
 var m=modo(u),clean=pulisci(u),dest=conv(u,m);
 if(interno(clean)&&dest.href!==clean.href){carica(dest,m);return}
 mark(m);scrivi('orr_gv',m);if(interno(clean))scrivi('orr_gu',clean.href);
});
var scelta='a',ricordo='';try{scelta=localStorage.getItem('orr_gv')==='n'?'n':'a';ricordo=localStorage.getItem('orr_gu')||''}catch(e){}
if(location.hash==='#nuova'||location.hash==='#attuale'){scelta=location.hash==='#nuova'?'n':'a';ricordo=''}
var prima=home(scelta);if(ricordo){try{prima=conv(ricordo,scelta)}catch(e){}}
carica(prima,scelta);
})();
