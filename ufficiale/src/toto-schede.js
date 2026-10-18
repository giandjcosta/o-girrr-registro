/* === Schede nuove di Totogirrr (5.0): Probabilità e Sfide 1 contro 1, nello stile della pagina === */
var LABDATI=@@DATI@@,PB=null,PBK='s',PBERR='',PBBUSY=false,NAVX=0;
function f1T(x){return (Math.round(x*10)/10).toFixed(1).replace('.',',')}
function avT(t){var i=(PB&&PB.teams?PB.teams:teams).indexOf(t),h=i<0?200:(i*36+10)%360;return '<span class="avt" style="background:hsl('+h+',58%,'+(h>40&&h<190?'32':'40')+'%)">'+esc(String(t).replace(/[^A-Za-z]/g,'').slice(0,2).toUpperCase())+'</span>'}
function probLoad(){
  if(PB||PBBUSY)return;PBBUSY=true;PBERR='';
  var i=0;(function tenta(){
    if(i>=LABDATI.length){PBBUSY=false;PBERR='Non riesco a leggere le probabilità adesso.';if(tab==='prob')render();return}
    fetch(LABDATI[i++],{cache:'no-cache'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){if(!j||!j.prob)throw 0;PB=j;PBBUSY=false;if(tab==='prob')render()}).catch(tenta)})();
}
function vProbT(){
  if(!PB){probLoad();return '<h2 class="ph">Chi vince la lega</h2><div class="vuoto">'+(PBERR||'Carico le probabilità…')+'</div>'}
  var k=PBK,lab={s:'Scudetto',p:'Podio',u:'Ultimo posto'}[k],g=0;(PB.tab||[]).forEach(function(r){g=Math.max(g,r.g||0)});
  var pr=function(t){return (PB.prob[t]||{s:[0,0],p:[0,0],u:[0,0]})[k]};
  var arr=PB.teams.slice().sort(function(a,b){return pr(b)[1]-pr(a)[1]});
  var h='<h2 class="ph">Chi vince la lega</h2><p class="psub">Dopo ogni giornata simulo le giornate rimaste migliaia di volte, partendo dai punti fatti finora e dal calendario vero. Il numero è la percentuale di stagioni in cui la squadra chiude in quella posizione.</p>';
  h+='<div class="seg2" role="group" aria-label="Tipo di probabilità">'+[['s','Scudetto'],['p','Podio'],['u','Ultimo']].map(function(x){return '<button data-pk="'+x[0]+'" class="'+(k===x[0]?'on':'')+'">'+x[1]+'</button>'}).join('')+'</div>';
  h+='<div class="card"><div class="gh"><span>'+lab.toUpperCase()+' · DOPO LA GIORNATA '+g+'</span></div>';
  arr.forEach(function(t){var p=pr(t),d=p[1]-p[0],row=(PB.tab||[]).filter(function(r){return r.t===t})[0]||{};
    h+='<div class="prt">'+avT(t)+'<div class="pg"><b>'+esc(t)+'</b> <small>'+(row.pos?row.pos+'° · '+row.pts+' pt':'')+'</small><div class="pbar'+(k==='u'?' u':'')+'"><i style="width:'+Math.min(100,p[1])+'%"></i></div></div><div class="ppc">'+f1T(p[1])+'%<small class="'+((k==='u'?d<0:d>0)?'up':'dn')+'">'+(d>=0?'+':'')+f1T(d)+' dalla G'+Math.max(1,g-1)+'</small></div></div>'});
  return h+'</div><p class="psub">Con poche giornate giocate le percentuali ballano molto: dalla quinta o sesta diventano affidabili.</p>';
}
/* ---- Sfida 1 contro 1 ---- */
var DU={ok:null,prossima:null,crediti:{},duelli:[]},DUBUSY=false,DUOPP=null,DUPOSTA=50;
function duLoad(quiet){
  if(DUBUSY||!team||!code||DEMO)return Promise.resolve();DUBUSY=true;
  return rpc('duello_stato',{p_team:team,p_code:code}).then(function(r){var a=JSON.stringify(DU),b=JSON.stringify(r);DU=r;
    if(a!==b&&tab==='sfide'){var e=document.activeElement;if(!(quiet&&e&&/INPUT|SELECT/.test(e.tagName)))render()}
  }).catch(function(){if(DU.ok===null){DU={ok:false,crediti:{},duelli:[]};if(tab==='sfide')render()}}).then(function(){DUBUSY=false},function(){DUBUSY=false});
}
function duCall(nome,body,ok){return rpc(nome,body).then(function(){toast(ok);return Promise.all([duLoad(false),carica()])}).catch(function(e){toast(e.message||'Qualcosa non ha funzionato',1);return duLoad(false)})}
function duCap(o){var c=DU.crediti||{};return Math.max(0,Math.min(200,c[team]||0,c[o]==null?0:c[o]))}
function vSfideT(){
  var h='<h2 class="ph">Sfida 1 contro 1</h2><p class="psub">Sfida un\'altra squadra con i tuoi fantacrediti: nella prossima giornata <b>vince chi fa più punti</b> e prende la posta dell\'altro. In caso di pareggio ognuno si riprende i suoi. Puoi puntare al massimo 200 e mai più di quello che hanno tu e l\'avversario.</p>';
  if(DEMO)return h+'<div class="vuoto">Nella prova le sfide 1 contro 1 non ci sono.</div>';
  if(DU.ok===null){duLoad(false);return h+'<div class="vuoto">Carico le sfide…</div>'}
  if(DU.ok===false)return h+'<div class="vuoto">Non riesco a leggere le sfide adesso. Riprova tra un attimo.</div>';
  var cr=DU.crediti||{},mio=cr[team],G=DU.prossima,opp=teams.filter(function(t){return t!==team&&cr[t]!=null});
  if(mio==null)return h+'<div class="vuoto">La tua squadra non ha ancora un conto: gioca una schedina e si attiva da solo.</div>';
  if(!DUOPP||opp.indexOf(DUOPP)<0)DUOPP=opp[0];
  var mx=duCap(DUOPP);if(DUPOSTA>mx)DUPOSTA=mx;if(mx>=10&&DUPOSTA<10)DUPOSTA=10;
  var att=DU.duelli.filter(function(d){return d.giornata===G&&(d.stato==='attesa'||d.stato==='accettato')&&d.da===team}).length;
  h+='<div class="card"><div class="gh"><span>LANCIA UNA SFIDA</span><small>Giornata '+G+'</small></div><div class="vsr"><div>'+avT(team)+'<b>'+esc(team)+'</b><small>'+f2(mio)+' fantacrediti</small></div><div class="vsx">vs</div><div>'+avT(DUOPP)+'<select id="dopp" aria-label="Avversario">'+opp.map(function(t){return '<option'+(t===DUOPP?' selected':'')+'>'+esc(t)+'</option>'}).join('')+'</select><small>'+f2(cr[DUOPP])+' fantacrediti</small></div></div>';
  if(mx<10)h+='<p class="psub">Non puoi sfidare '+esc(DUOPP)+': la posta minima è 10 e il massimo possibile tra voi due è '+f2(mx)+'.</p>';
  else h+='<div class="prow"><b>Posta</b><b class="pv" id="dstk">'+DUPOSTA+' fantacrediti</b></div><input type="range" id="dstake" min="10" max="'+Math.floor(mx)+'" step="1" value="'+DUPOSTA+'" aria-label="Posta"><p class="psub">Massimo '+Math.floor(mx)+': il minimo tra quello che hai tu, quello che ha l\'avversario e il tetto di 200. I tuoi fantacrediti restano bloccati finché lui non risponde: se rifiuta o non risponde in tre giorni tornano indietro.</p><button class="go" id="dgo" style="width:100%"'+(att>=3?' disabled':'')+'>Sfida per <span id="dgo2">'+DUPOSTA+'</span></button>'+(att>=3?'<p class="psub">Hai già tre sfide per questa giornata.</p>':'');
  h+='</div>';
  var rx=DU.duelli.filter(function(d){return d.a===team&&d.stato==='attesa'});
  if(rx.length){h+='<div class="card"><div class="gh"><span>SFIDE RICEVUTE</span></div>';
    rx.forEach(function(d){h+='<div class="dr">'+avT(d.da)+'<div class="pg"><b>'+esc(d.da)+'</b> ti sfida<small>Giornata '+d.giornata+' · Posta '+f2(d.posta)+'</small></div><button class="go" data-dr="accetta" data-id="'+d.id+'"'+(mio<d.posta?' disabled':'')+'>Accetta</button><button class="x" data-dr="rifiuta" data-id="'+d.id+'">Rifiuta</button></div>'+(mio<d.posta?'<p class="psub">Per accettare servono '+f2(d.posta)+' fantacrediti, ne hai '+f2(mio)+'.</p>':'')});
    h+='</div>'}
  var els=DU.duelli.filter(function(d){return d.stato==='attesa'||d.stato==='accettato'||d.stato==='chiuso'||d.da===team||d.a===team});
  h+='<div class="card"><div class="gh"><span>SFIDE DELLA LEGA</span></div>';
  if(!els.length)h+='<p class="psub">Ancora nessuna sfida.</p>';
  els.forEach(function(x){var tag={attesa:'In attesa',accettato:'Accettata',chiuso:'Chiusa',rifiutato:'Rifiutata',scaduto:'Scaduta'}[x.stato]||x.stato;
    h+='<div class="dr">'+avT(x.da)+'<div class="pg"><b>'+esc(x.da)+'</b> vs <b>'+esc(x.a)+'</b><small>Giornata '+x.giornata+' · Posta '+f2(x.posta)+'</small>'+(x.stato==='chiuso'?'<small>'+f1T(x.pa)+' - '+f1T(x.pb)+' · '+(x.vincitore?'Vince '+esc(x.vincitore)+', incassa '+f2(x.posta*2):'Pareggio: ognuno si riprende i suoi')+'</small>':'')+'</div><span class="tg">'+tag+'</span></div>'});
  return h+'</div>';
}
document.addEventListener('click',function(e){var t=e.target,b;
  if(b=t.closest('[data-pk]')){PBK=b.getAttribute('data-pk');render();return}
  if(t.id==='dgo'||(t.closest&&t.closest('#dgo'))){if(DU.ok!==true)return;var bt=document.getElementById('dgo');if(bt)bt.disabled=true;duCall('duello_lancia',{p_team:team,p_code:code,p_rival:DUOPP,p_posta:DUPOSTA,p_giornata:null},'Sfida lanciata a '+DUOPP);return}
  if(b=t.closest('[data-dr]')){var az=b.getAttribute('data-dr');b.disabled=true;duCall('duello_rispondi',{p_team:team,p_code:code,p_id:Number(b.getAttribute('data-id')),p_azione:az},az==='accetta'?'Hai accettato la sfida':'Hai rifiutato la sfida');return}
});
document.addEventListener('change',function(e){if(e.target.id==='dopp'){DUOPP=e.target.value;render()}});
document.addEventListener('input',function(e){if(e.target.id==='dstake'){DUPOSTA=Number(e.target.value);var a=document.getElementById('dstk'),b=document.getElementById('dgo2');if(a)a.textContent=DUPOSTA+' fantacrediti';if(b)b.textContent=DUPOSTA}});
setInterval(function(){if(tab==='sfide'&&!document.hidden)duLoad(true)},45000);
/* ---- Menu a scorrimento: non gira all'infinito, la scheda toccata si vede per intero, agli estremi rimbalza ---- */
function navPre(){var n=document.querySelector('nav');if(n)NAVX=n.scrollLeft}
function navPost(){var n=document.querySelector('nav');if(!n)return;n.scrollLeft=NAVX;
  var b=n.querySelector('button.on');
  if(b){var sl=n.scrollLeft,cw=n.clientWidth,l=b.offsetLeft,r=l+b.offsetWidth,m=10,to=null;
    if(l-m<sl)to=Math.max(0,l-m);else if(r+m>sl+cw)to=Math.min(n.scrollWidth-cw,r+m-cw);
    if(to!==null&&Math.abs(to-sl)>1)n.scrollTo({left:to,behavior:'smooth'})}
  navBounce(n)}
function navBounce(n){
  var inn=n.firstChild;if(!inn||!inn.classList||!inn.classList.contains('nvi'))return;
  var ios=/iP(hone|ad|od)/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  var over=0,edge=null,drag=null,tm=null;
  function set(v,molla){over=v;inn.style.transition=molla?'transform .55s cubic-bezier(.2,1.35,.4,1)':'none';inn.style.transform=v?'translate3d('+v+'px,0,0)':''}
  function atEdge(dir){return dir>0?n.scrollLeft<=0:n.scrollLeft>=n.scrollWidth-n.clientWidth-1}
  function res(d){return Math.max(-70,Math.min(70,d*0.4))}
  if(!ios){
    n.addEventListener('touchstart',function(ev){edge=null;drag=ev.touches[0].clientX;set(0,false)},{passive:true});
    n.addEventListener('touchmove',function(ev){var x=ev.touches[0].clientX,dx=x-drag;
      if(edge===null){if(dx!==0&&atEdge(dx>0?1:-1))edge=drag}
      if(edge!==null){var d=x-edge;if((d>0&&atEdge(1))||(d<0&&atEdge(-1)))set(res(d),false);else{edge=null;set(0,false)}}},{passive:true});
    n.addEventListener('touchend',function(){edge=null;set(0,true)},{passive:true});
    n.addEventListener('touchcancel',function(){edge=null;set(0,true)},{passive:true});
  }
  /* mouse: trascinamento con il pulsante premuto */
  var md=null;
  n.addEventListener('pointerdown',function(ev){if(ev.pointerType!=='mouse'||ev.button!==0)return;md={x:ev.clientX,s:n.scrollLeft,moved:false,id:ev.pointerId}});
  n.addEventListener('pointermove',function(ev){if(!md||ev.pointerType!=='mouse')return;var dx=ev.clientX-md.x;
    if(!md.moved&&Math.abs(dx)>4){md.moved=true;try{n.setPointerCapture(md.id)}catch(x){}}
    if(!md.moved)return;
    var want=md.s-dx,max=n.scrollWidth-n.clientWidth;
    if(want<0){n.scrollLeft=0;set(res(-want),false)}else if(want>max){n.scrollLeft=max;set(res(-(want-max)),false)}else{n.scrollLeft=want;if(over)set(0,false)}});
  function fine(){if(md&&md.moved){var h=function(c){c.stopPropagation();c.preventDefault()};n.addEventListener('click',h,true);setTimeout(function(){n.removeEventListener('click',h,true)},120)}md=null;if(over)set(0,true)}
  n.addEventListener('pointerup',fine);n.addEventListener('pointercancel',fine);
  /* trackpad e rotella orizzontale */
  n.addEventListener('wheel',function(ev){var dx=Math.abs(ev.deltaX)>Math.abs(ev.deltaY)?ev.deltaX:0;if(!dx)return;
    var dir=dx<0?1:-1;if(atEdge(dir)){set(res(over-dx),false);clearTimeout(tm);tm=setTimeout(function(){set(0,true)},110)}},{passive:true});
}
