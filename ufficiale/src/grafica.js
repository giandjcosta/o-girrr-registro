/* Interruttore della grafica nella Home, a destra del titolo. Si sceglie una volta e la scelta resta (orr_gv).
   Nomi provvisori delle due grafiche: si cambiano solo qui e in confronto.html (NOMI). */
(function(){
var NOMI={a:'Vecchia scuola',n:'Nuova era'};
function go(){
var h=document.querySelector('.hero');if(!h||document.getElementById('gsw'))return;
var nuova=location.pathname.indexOf('/ufficiale/nuovo/')>=0;
var st=document.createElement('style');
st.textContent='.hero{flex-wrap:wrap}#gsw{margin-left:auto;display:flex;align-items:center;gap:8px;color:#fbf6ec;font:800 12px Inter,system-ui,sans-serif;letter-spacing:.02em;user-select:none;-webkit-tap-highlight-color:transparent}#gsw span{opacity:.55;transition:opacity .25s;white-space:nowrap}#gsw span.on{opacity:1}#gsw button{position:relative;flex:none;width:52px;height:30px;border-radius:999px;background:#1d2a52;border:1px solid rgba(255,255,255,.28);padding:0;cursor:pointer;transition:background .3s,border-color .3s}#gsw button::after{content:"";position:absolute;top:3px;left:3px;width:22px;height:22px;border-radius:50%;background:#fff;box-shadow:0 2px 5px rgba(0,0,0,.4);transition:transform .3s cubic-bezier(.3,1.3,.5,1)}#gsw button[aria-checked=true]{background:#d62839;border-color:#d62839}#gsw button[aria-checked=true]::after{transform:translateX(22px)}@media(max-width:560px){#gsw{flex:1 0 100%;justify-content:center;margin-top:4px}}';
document.head.appendChild(st);
var d=document.createElement('label');d.id='gsw';
d.innerHTML='<span class="'+(nuova?'':'on')+'">'+NOMI.a+'</span><button role="switch" aria-checked="'+nuova+'" aria-label="Grafica '+NOMI.n+'"></button><span class="'+(nuova?'on':'')+'">'+NOMI.n+'</span>';
h.appendChild(d);
d.querySelector('button').onclick=function(e){e.preventDefault();var m=nuova?'a':'n';
try{localStorage.setItem('orr_gv',m)}catch(x){}
if(window.top!==window.self){try{window.parent.postMessage({orrGrafica:m},location.origin)}catch(x){}return}
var p=location.pathname;
location.href=(m==='n'?p.replace('/ufficiale/girrr/','/ufficiale/nuovo/girrr/'):p.replace('/ufficiale/nuovo/girrr/','/ufficiale/girrr/'))+location.search+location.hash};
}
if(document.body)go();else document.addEventListener('DOMContentLoaded',go);
})();
