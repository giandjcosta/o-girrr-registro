/* Transizioni morbide: quando l'utente preme una tab / un selettore, il contenuto che cambia entra con una dissolvenza leggera. */
(function(){
if(window._fx)return;window._fx=1;
if(window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches)return;
var st=document.createElement('style');
st.textContent='@keyframes fxin{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}.fx-in{animation:fxin .34s cubic-bezier(.2,.7,.2,1) both;animation-delay:calc(var(--fxd,0)*38ms)}[role=tab],.seg button,.at button,.chips button,.sw button,.ptabs button,.tabs button{transition:background-color .28s ease,color .28s ease,border-color .28s ease,opacity .28s ease,transform .28s ease}';
document.head.appendChild(st);
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
