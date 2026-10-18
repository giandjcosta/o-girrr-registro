/* Interruttore della grafica nella Home, a destra del titolo. Si sceglie una volta e la scelta resta (orr_gv).
   Nomi provvisori delle due grafiche: si cambiano solo qui e in confronto.html (NOMI). */
(function(){
var NOMI={a:'Lega',n:'Stadio'};
function go(){
var h=document.querySelector('.hero');if(!h||document.getElementById('gsw'))return;
var nuova=location.pathname.indexOf('/ufficiale/nuovo/')>=0;
var st=document.createElement('style');
st.textContent='.hero{position:relative}#gsw{position:absolute;top:0;right:0;z-index:2;display:flex;gap:2px;padding:3px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.22);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);user-select:none;-webkit-tap-highlight-color:transparent}#gsw button{border:0;border-radius:999px;padding:5px 13px;font:800 11.5px Inter,system-ui,sans-serif;letter-spacing:.04em;color:#fbf6ec;background:transparent;opacity:.7;cursor:pointer;transition:background-color .35s,color .35s,opacity .35s}#gsw button[aria-pressed=true]{opacity:1;background:#d62839;color:#fff;cursor:default}#gsw button[data-m=n][aria-pressed=true]{background:#ffd166;color:#1d2a52}@media(max-width:700px){.hero:not(.gsw-su){padding-top:40px}}.app-bar #gsw{position:static;margin-right:8px;align-self:center}';
document.head.appendChild(st);
var d=document.createElement('div');d.id='gsw';d.setAttribute('role','group');d.setAttribute('aria-label','Grafica');
d.innerHTML=['a','n'].map(function(m){return '<button data-m="'+m+'" aria-pressed="'+((m==='n')===nuova)+'">'+NOMI[m]+'</button>'}).join('');
h.appendChild(d);
/* Se il sito è aperto come app (aggiunto alla Home) c'è la riga con il tasto Aggiorna: il selettore va sulla stessa riga, a sinistra di Aggiorna */
var n=0;(function su(){var b=document.querySelector('.app-bar');if(b){b.insertBefore(d,b.firstChild);h.classList.add('gsw-su');return}if(n++<12)setTimeout(su,250)})();
d.onclick=function(e){var bt=e.target.closest('button');if(!bt)return;var m=bt.dataset.m;if((m==='n')===nuova)return;
try{localStorage.setItem('orr_gv',m)}catch(x){}
if(window.top!==window.self){try{window.parent.postMessage({orrGrafica:m},location.origin)}catch(x){}return}
var p=location.pathname;
location.href=(m==='n'?p.replace('/ufficiale/girrr/','/ufficiale/nuovo/girrr/'):p.replace('/ufficiale/nuovo/girrr/','/ufficiale/girrr/'))+location.search+location.hash};
}
if(document.body)go();else document.addEventListener('DOMContentLoaded',go);
})();
