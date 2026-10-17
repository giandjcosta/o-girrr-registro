/* Novità 5.0 per l'Albo d'oro: storia della Lega, Era dei Titani, titoli di sempre, derby. Font e colori sono quelli del sito. */
(function(){
var st=document.createElement('style');st.textContent='.rac{margin:12px 0;padding:12px 14px;border-radius:14px;background:rgba(0,0,0,.2);border-left:3px solid var(--hi)}.rac .rt{font-weight:900;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--hi);margin-bottom:6px}.rac p{font-weight:600;font-size:14px;line-height:1.6;margin:0 0 8px}.rac p:last-child{margin:0}.nt{color:var(--sub);font-weight:600;font-size:12px;margin-top:8px;line-height:1.5}.nt-r{text-align:right!important}.nt-t td.num,.nt-t th.num{text-align:right}.nt-nv{display:inline-block;margin-left:8px;border-radius:999px;background:var(--acc);color:#fff;font-weight:900;font-size:10px;letter-spacing:.14em;padding:3px 8px;vertical-align:middle}';document.head.appendChild(st);
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
window.NOVITA=function(D){var N=window.NOV;if(!N)return {};
  var L=N.leg,tt={},P={};
  var h='<div class="card"><h3>La storia della Lega<span class="nt-nv">NOVITÀ</span></h3>'+L.libro.map(function(c){return '<div class="rac"><div class="rt">'+esc(c.t)+'</div>'+c.p.map(function(p){return '<p>'+esc(p)+'</p>'}).join('')+'</div>'}).join('')+'</div>';
  N.stag.forEach(function(x){if(x[1]!=='Coppa Campioni')tt[x[3]]=(tt[x[3]]||0)+1});N.pre.forEach(function(x){if(x[2])tt[x[2]]=(tt[x[2]]||0)+1});
  P.storia=h;h='';
  h+='<div class="card"><h3>'+esc(L.eras.prima)+'<span class="nt-nv">NOVITÀ</span></h3><p class="nt" style="margin:0 0 8px">Prima del cambio di lega del 2021. I dati sono andati persi: queste stagioni arrivano dai ricordi del gruppo.</p><table><tr><th>Stagione</th><th>Vincitore</th></tr>'+N.pre.map(function(x){return '<tr><td>'+x[0]+'</td><td>'+(x[2]?esc(x[1]||x[2])+(x[1]?'<small>'+esc(x[2])+'</small>':''):'<span style="color:var(--sub)">Non assegnato</span>')+'</td></tr>'}).join('')+'</table>'
   +L.titani.map(function(r){return '<div class="rac"><div class="rt">'+esc(r.t)+'</div><p>'+esc(r.p)+'</p></div>'}).join('')+'<p class="nt">'+esc(L.nota)+'</p></div>';
  P.titani=h;h='';
  h+='<div class="card"><h3>Titoli di sempre</h3><table class="nt-t"><tr><th>Allenatore</th><th class="num">Titoli</th></tr>'+Object.keys(tt).sort(function(a,b){return tt[b]-tt[a]}).map(function(u){return '<tr><td>'+esc(u)+'</td><td class="num">'+tt[u]+(N.pre.some(function(x){return x[2]===u})?'*':'')+'</td></tr>'}).join('')+'</table><p class="nt">* Include i titoli dell\'Era dei Titani, che arrivano dai ricordi e non da dati conservati. Contano solo i campionati, non la Coppa Campioni.</p></div>';
  P.titoli=h;h='';
  h+='<a class="card" href="derby.html" style="display:block;text-decoration:none;color:inherit"><h3>I derby della Lega<span class="nt-nv">NOVITÀ</span></h3><div style="font-weight:700;font-size:14px">Le rivalità, i derby con la loro storia e le sfide decisive → </div></a>';
  P.derby=h;return P}

window.ALBOTABS=function(D,x){
  var P=window.NOVITA?window.NOVITA(D):{};
  var S=[['storia','Storia',P.storia],['titani','Era dei Titani',P.titani],['titoli','Titoli',P.titoli],['all','Allenatori',x.allenatori],['stag','Stagioni',x.storico],['rec','Record',x.recs],['derby','Derby',P.derby]].filter(function(s){return s[2]});
  var cur=(location.hash||'').slice(1);if(!S.some(function(s){return s[0]===cur}))cur=S[0][0];
  var h=x.stato+'<div class="at" role="tablist">'+S.map(function(s){return '<button role="tab" data-at="'+s[0]+'" aria-selected="'+(s[0]===cur)+'">'+s[1]+'</button>'}).join('')+'</div>'
   +S.map(function(s){return '<div class="ap" data-ap="'+s[0]+'"'+(s[0]===cur?'':' hidden')+'>'+s[2]+'</div>'}).join('');
  setTimeout(function(){var root=document.getElementById('al');if(!root||root._at)return;root._at=1;
    root.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-at]');if(!b)return;var k=b.getAttribute('data-at');
      root.querySelectorAll('[data-at]').forEach(function(z){z.setAttribute('aria-selected',z===b)});root.querySelectorAll('[data-ap]').forEach(function(z){z.hidden=z.getAttribute('data-ap')!==k});
      try{history.replaceState(null,'','#'+k)}catch(_){}b.scrollIntoView({block:'nearest',inline:'center',behavior:'smooth'})})},0);
  return h};
var st2=document.createElement('style');st2.textContent='.at{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding:2px;margin:14px 0 12px}.at::-webkit-scrollbar{display:none}.at button{flex:none;height:38px;padding:0 16px;border-radius:19px;border:2px solid transparent;background:rgba(255,255,255,.08);color:var(--chiaro);font:800 14px Inter,system-ui,sans-serif;cursor:pointer;opacity:.6;transition:all .25s}.at button[aria-selected=true]{background:var(--acc);opacity:1}.ap[hidden]{display:none}';document.head.appendChild(st2);
})();
