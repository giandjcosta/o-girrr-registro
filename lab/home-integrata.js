/* Prima pagina in prova: aggiunta DOM alla Home originale; nessuna sezione precedente rimossa. */
(function(){
'use strict';
var ROOT='https://giandjcosta.github.io/o-fant-a-girrr/',local='og-lab-';
var skin=document.body.getAttribute('data-og-skin')==='stadio'?'stadio':'lega';
var target=document.getElementById('og-today'),pick=document.getElementById('og-team'),boxes=document.getElementById('og-items'),news=document.getElementById('og-news');
if(!target||!pick||!boxes||!news)return;
function esc(v){return String(v==null?'':v).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function saved(k,f){try{return JSON.parse(localStorage.getItem(local+k))||f}catch(e){return f}}
function store(k,x){try{localStorage.setItem(local+k,JSON.stringify(x))}catch(e){}}
function finished(m){return m[4]&&m[4]!=='-'}
function events(g){return (g||[]).filter(function(x){return x.m&&x.m.every(finished)})}
function record(d,t,n){var a={};d.teams.forEach(function(z){a[z.name]={pt:0,fp:0}});(d.cal.lega||[]).forEach(function(g){if(g.n>n)return;(g.m||[]).forEach(function(m){if(!finished(m))return;var x=a[m[0]],y=a[m[3]],p=m[4].split('-').map(Number);if(!x||!y)return;x.fp+=Number(m[1])||0;y.fp+=Number(m[2])||0;x.pt+=p[0]>p[1]?3:p[0]===p[1]?1:0;y.pt+=p[1]>p[0]?3:p[0]===p[1]?1:0})});return Object.keys(a).sort(function(u,v){return a[v].pt-a[u].pt||a[v].fp-a[u].fp}).indexOf(t)+1}
function card(l,v,s){return '<div class="og-item"><small>'+esc(l)+'</small><strong>'+esc(v)+'</strong>'+(s?'<small>'+esc(s)+'</small>':'')+'</div>'}
fetch(ROOT+'data.json',{cache:'no-store'}).then(function(r){if(!r.ok)throw Error('Dati non disponibili');return r.json()}).then(function(d){
var names=(d.teams||[]).map(function(x){return x.name});if(!names.length)throw Error('Squadre assenti');
var current=saved('team',names[0]);if(names.indexOf(current)<0)current=names[0];
pick.innerHTML=names.map(function(t){return '<option value="'+esc(t)+'">'+esc(t)+'</option>'}).join('');
function redraw(){
var t=pick.value,last=events(d.cal.lega),g=last[last.length-1],n=g&&g.n||0,rounds=(d.cal.lega||[]),next=rounds.find(function(x){return x.m&&x.m.some(function(m){return !finished(m)})}),lastMatch=null;
for(var i=last.length-1;i>=0;i--){var z=last[i].m.find(function(m){return m[0]===t||m[3]===t});if(z){lastMatch=z;break}}
var nm=next&&next.m.find(function(m){return m[0]===t||m[3]===t}),op=nm?nm[0]===t?nm[3]:nm[0]:'Da definire';
boxes.innerHTML=card('Posizione attuale',n?record(d,t,n)+'°':'—',n?'Dopo la '+n+'ª giornata':'Campionato in corso')+card('Ultimo risultato',lastMatch?lastMatch[0]+' '+lastMatch[4]+' '+lastMatch[3]:'—',lastMatch?'Risultato acquisito':'Non disponibile')+card('Prossimo avversario',op,next?next.n+'ª giornata':'Calendario da aggiornare');
var snapshot={n:n,op:op,ris:lastMatch&&lastMatch[4],pos:n?record(d,t,n):null},old=saved('home-seen-'+t,null),diff=[];
if(old){if(old.op!==snapshot.op)diff.push('È cambiato il tuo prossimo avversario.');if(old.ris!==snapshot.ris||old.n!==snapshot.n)diff.push('Ci sono risultati nuovi da consultare.');if(old.pos!==snapshot.pos)diff.push('La tua posizione in classifica è cambiata.')}
news.innerHTML='<b>Da non perdere</b>'+(diff.length?diff.map(esc).join(' · '):'Ultimi risultati, Girrr Sport, Curva e Annuario sono sempre a portata di mano.');
document.getElementById('og-status').textContent='Ultimi risultati disponibili'+(n?' · '+n+'ª giornata':'')+' · Nessun messaggio tecnico ai giocatori';
target.querySelector('[data-og-read]').onclick=function(){store('home-seen-'+t,snapshot);redraw()};
store('team',t);
}
pick.value=current;pick.onchange=redraw;redraw()
}).catch(function(){boxes.innerHTML='<div class="og-item"><small>I dati della stagione non sono disponibili in questo momento.</small></div>';news.textContent='Le altre sezioni della Home restano accessibili.'});
})();
