/* Transizioni morbide: quando l'utente preme una tab / un selettore, il contenuto che cambia entra con una dissolvenza leggera. */
(function(){
if(window._fx)return;window._fx=1;
if(window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches)return;
var st=document.createElement('style');
st.textContent='@keyframes fxin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}.fx-in{animation:fxin .62s cubic-bezier(.22,.61,.36,1) both;animation-delay:calc(var(--fxd,0)*70ms)}[role=tab],.seg button,.at button,.chips button,.sw button,.ptabs button,.tabs button{transition:background-color .5s ease,color .5s ease,border-color .5s ease,opacity .5s ease,transform .5s ease}';
document.head.appendChild(st);
/* il logo della lega riporta alla Home dell'anteprima (stessa grafica) */
document.addEventListener('click',function(e){var l=e.target.closest&&e.target.closest('#lg,#olg');if(!l)return;var p=location.pathname,d=null;
if(p.indexOf('/ufficiale/nuovo/girrr/')>=0||p.indexOf('/ufficiale/girrr/')>=0){if(/\/index\.html$|\/girrr\/$/.test(p))return;d='index.html'}
else if(/\/anteprima\/attuale\.html$/.test(p))d='../ufficiale/girrr/index.html';else if(/\/anteprima\/(index\.html)?$/.test(p))d='../ufficiale/nuovo/girrr/index.html';
if(!d)return;e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();location.href=d},true);
var _ls=document.createElement('style');_ls.textContent='#lg,#olg{cursor:pointer}';document.head.appendChild(_ls);
var last=0;
function mark(){last=Date.now()}
document.addEventListener('pointerdown',mark,true);document.addEventListener('keydown',mark,true);document.addEventListener('click',mark,true);
function ok(n){return n.nodeType===1&&!/^(SCRIPT|STYLE|LINK|AUDIO|VIDEO|OPTION|INPUT|SELECT|TEXTAREA)$/.test(n.tagName)&&!n.closest('.fx-in')&&!n.closest('.tabs,.seg,.at,.chips,.sw,.ptabs,select,input,textarea,button')}
function anim(n,i){n.style.setProperty('--fxd',Math.min(i,6));n.classList.add('fx-in');n.addEventListener('animationend',function f(e){if(e.target!==n)return;n.classList.remove('fx-in');n.style.removeProperty('--fxd');n.removeEventListener('animationend',f)})}
function avvia(){
new MutationObserver(function(ms){
  if(Date.now()-last>800)return;
  var i=0;
  ms.forEach(function(m){m.addedNodes.forEach(function(n){if(ok(n)&&n.getBoundingClientRect().height>12)anim(n,i++)})})
}).observe(document.body,{childList:true,subtree:true});
/* pannelli mostrati/nascosti con l'attributo hidden (es. tab dell'Albo d'oro) */
new MutationObserver(function(ms){
  if(Date.now()-last>800)return;
  ms.forEach(function(m){var n=m.target;if(m.attributeName==='hidden'&&!n.hidden&&ok(n))anim(n,0)})
}).observe(document.body,{attributes:true,subtree:true,attributeFilter:['hidden']});
}
if(document.body)avvia();else document.addEventListener('DOMContentLoaded',avvia);
})();
