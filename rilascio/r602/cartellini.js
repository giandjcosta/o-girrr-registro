/* Ogni ribalta finisce prima di accettare il valore successivo. Il testo resta
   ancorato alle due metà: nessuna trasformazione percentuale sulla cifra. */
function fidTab(el,v){
 if(!el)return;
 var t=el.querySelector('.tab-fid'),nuovo=!t;
 if(nuovo){t=document.createElement('div');t.className='tab-fid';t.setAttribute('aria-hidden','true');el.appendChild(t)}
 var s=String(Math.max(0,Math.min(100,Math.round(v)))),n=Math.max(2,s.length,String(el.dataset.target||'').length);
 s=('000'+s).slice(-n);
 while(t.children.length<n){var f=document.createElement('span');f.className='fl';f.dataset.v=s.charAt(t.children.length);f.innerHTML='<span class="su"><b></b></span><span class="giu"><b></b></span><span class="a"><b></b></span><span class="b"><b></b></span>';t.appendChild(f);[].forEach.call(f.querySelectorAll('b'),function(b){b.textContent=f.dataset.v})}
 while(t.children.length>n){clearTimeout(t.firstChild._timer);t.removeChild(t.firstChild)}
 [].forEach.call(t.children,function(f,i){
  f._target=s.charAt(i);
  function testo(k,val){f.querySelector('.'+k+' b').textContent=val}
  function ferma(val){['su','giu','a','b'].forEach(function(k){testo(k,val)});f.dataset.v=val;f.classList.remove('gira');f._busy=false;clearTimeout(f._timer)}
  function ribalta(){
   if(!f.isConnected||f._busy||f.dataset.v===f._target)return;
   var da=f.dataset.v,a=f._target,id=(f._id||0)+1;f._id=id;f._busy=true;
   testo('su',a);testo('giu',da);testo('a',da);testo('b',a);
   function fine(){if(f._id!==id||!f._busy)return;ferma(a);if(f.isConnected&&f._target!==a)requestAnimationFrame(ribalta)}
   f.onanimationend=function(e){if(e.animationName==='fid-giu')fine()};
   f.classList.remove('gira');void f.offsetWidth;f.classList.add('gira');f._timer=setTimeout(function controlla(){
    if(!f.isConnected)return;
    var anim=f.getAnimations?f.getAnimations({subtree:true}):[];
    if(anim.some(function(a){return a.playState==='running'||a.playState==='pending'})){f._timer=setTimeout(controlla,180);return}
    fine();
   },650);
  }
  if(nuovo||window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){f._id=(f._id||0)+1;ferma(f._target)}else ribalta();
 });
}
