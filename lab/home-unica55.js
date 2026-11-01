(function(){'use strict';
const $=id=>document.getElementById(id),q=new URLSearchParams(location.search),ROOT='../anteprima/5.5/';
let skin=q.get('skin')==='stadio'?'stadio':'lega',bozza=q.get('bozza')==='b'?'b':'a',team=q.get('squadra')||'Oranje VC',D=null,rounds=[],history=[],eventi=null;
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const dec=n=>Number(n).toLocaleString('it-IT',{maximumFractionDigits:2});
const ORDINE=['The Blue brothers','Apo team','Mariana Coneja','stif dc','Real Madrink','Atletico ma non troppo','Oranje VC','AFA SELECCION','Grodah','WOA'];
function url(page,n){return ROOT+page+'-'+skin+'.html'+(n?'#lega-'+n:'')}
function calcola(){
 const names=D.teams.map(t=>t.name).sort(),tab=Object.fromEntries(names.map(t=>[t,{team:t,pt:0,fp:0,gf:0,gs:0}]));
 for(const g of [...D.cal.lega].sort((a,b)=>a.n-b.n)){
  const matches=g.m||[],presenti=matches.flatMap(m=>[m[0],m[3]]).sort();
  if(g.n!==rounds.length+1||!matches.length||!matches.every(m=>m.length===5&&/^\d+-\d+$/.test(m[4]))||JSON.stringify(presenti)!==JSON.stringify(names))break;
  rounds.push(g);
  for(const m of matches){const [a,b]=m[4].split('-').map(Number),x=tab[m[0]],y=tab[m[3]];x.pt+=a>b?3:a===b?1:0;y.pt+=b>a?3:a===b?1:0;x.fp+=+m[1];y.fp+=+m[2];x.gf+=a;x.gs+=b;y.gf+=b;y.gs+=a;}
  const table=Object.values(tab).map(x=>({...x})).sort((a,b)=>b.pt-a.pt||b.fp-a.fp||(b.gf-b.gs)-(a.gf-a.gs)||b.gf-a.gf||ORDINE.indexOf(a.team)-ORDINE.indexOf(b.team));
  history.push({n:g.n,table});
 }
}
function linea(serie){
 if(!serie.length)return '<p class="chart-note">L’andamento sarà visibile dopo la prima giornata conclusa.</p>';
 const x=i=>serie.length===1?180:34+i*292/(serie.length-1),y=v=>28+(v-1)*7.8,points=serie.map((s,i)=>x(i)+','+y(s.pos)).join(' ');
 return '<svg viewBox="0 0 360 132" role="img" aria-label="Posizioni nelle ultime '+serie.length+' giornate: '+serie.map(s=>s.n+'ª, '+s.pos+'º posto').join('; ')+'"><defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#82cef3" stop-opacity=".17"/><stop offset="1" stop-color="#82cef3" stop-opacity="0"/></linearGradient></defs>'+[1,5,10].map(v=>'<path class="grid" d="M25 '+y(v)+'H341"/><text x="3" y="'+(y(v)+4)+'">'+v+'</text>').join('')+'<polygon class="area" points="'+x(0)+',105 '+points+' '+x(serie.length-1)+',105"/><polyline class="trace" points="'+points+'"/>'+serie.map((s,i)=>'<a href="'+url('tabellone',s.n)+'" aria-label="Classifica dopo la '+s.n+'ª giornata, '+s.pos+'º posto"><g class="'+(i===serie.length-1?'last':'')+'"><circle cx="'+x(i)+'" cy="'+y(s.pos)+'" r="4"/><text class="value" text-anchor="middle" x="'+x(i)+'" y="'+(y(s.pos)-11)+'">'+s.pos+'º</text><text text-anchor="middle" x="'+x(i)+'" y="126">'+s.n+'ª</text></g></a>').join('')+'</svg>';
}
function barre(serie){
 if(!serie.length)return '<p class="chart-note">Forma disponibile dopo la prima giornata.</p>';
 const x=i=>40+i*60;
 return '<svg viewBox="0 0 360 130" role="img" aria-label="Punti nelle ultime '+serie.length+' giornate: '+serie.map(s=>s.n+'ª, '+s.pt+' punti').join('; ')+'">'+[0,1,3].map(v=>'<path class="grid" d="M25 '+(96-v*20)+'H345"/><text x="3" y="'+(100-v*20)+'">'+v+'</text>').join('')+serie.map((s,i)=>'<a href="'+url('tabellone',s.n)+'" aria-label="'+s.n+'ª giornata, '+s.label+'"><rect class="'+(s.pt===3?'win-bar':s.pt===1?'draw-bar':'loss-bar')+'" x="'+x(i)+'" y="'+(96-Math.max(3,s.pt*20))+'" width="30" height="'+Math.max(3,s.pt*20)+'" rx="4"/><text class="value" x="'+(x(i)+15)+'" y="'+(86-Math.max(3,s.pt*20))+'" text-anchor="middle">'+s.sigla+'</text><text x="'+(x(i)+15)+'" y="124" text-anchor="middle">'+s.n+'ª</text></a>').join('')+'</svg>';
}
function render(){
 document.body.dataset.skin=skin;document.body.dataset.bozza=bozza;
 document.querySelectorAll('button[data-bozza]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.bozza===bozza));
 document.querySelectorAll('button[data-skin]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.skin===skin));
 $('home-link').href=url('index');document.querySelectorAll('[data-page]').forEach(a=>a.href=url(a.dataset.page));
 $('idea').textContent=bozza==='a'?'A · Posizione e andamento al centro, risultati in due righe. Un unico riquadro.':'B · Ultima partita in primo piano, punti conquistati nelle cinque giornate. Un unico riquadro.';
 const u=new URL(location.href);u.searchParams.set('skin',skin);u.searchParams.set('bozza',bozza);u.searchParams.set('squadra',team);window.history.replaceState(null,'',u);
 if(!D)return;
 $('team').style.fontSize=team.length>18?'clamp(16px,2.5vw,22px)':'';
 const last=history.at(-1),pos=last?last.table.findIndex(t=>t.team===team)+1:0,row=last&&last.table[pos-1],previous=history.at(-2),old=previous?previous.table.findIndex(t=>t.team===team)+1:pos,delta=old-pos;
 const move=!pos?'<span class="movement">Classifica in attesa</span>':delta?'<span class="movement '+(delta>0?'up':'down')+'">'+(delta>0?'↑ ':'↓ ')+Math.abs(delta)+' '+(Math.abs(delta)===1?'posizione':'posizioni')+'</span>':'<span class="movement">Posizione invariata</span>';
 const serie=history.slice(-5).map(s=>({n:s.n,pos:s.table.findIndex(t=>t.team===team)+1}));
 const recent=rounds.slice(-5).map(g=>{const m=g.m.find(m=>m[0]===team||m[3]===team),casa=m[0]===team,[a,b]=m[4].split('-').map(Number),gf=casa?a:b,gs=casa?b:a;return {n:g.n,m,pt:gf>gs?3:gf===gs?1:0,sigla:gf>gs?'V':gf===gs?'N':'P',label:gf>gs?'Vittoria':gf===gs?'Pareggio':'Sconfitta',casa};});
 const result=recent.at(-1),next=[...D.cal.lega].sort((a,b)=>a.n-b.n).find(g=>g.n>(last?last.n:0)),nextmatch=next&&next.m.find(m=>m[0]===team||m[3]===team),avversario=nextmatch?(nextmatch[0]===team?nextmatch[3]:nextmatch[0]):'Da definire';
 const nextText='<span class="caption">Prossima sfida · '+(next?next.n+'ª giornata':'Da definire')+'</span><strong>'+escape(avversario)+'</strong><span class="away-note">'+(nextmatch?(nextmatch[0]===team?'In casa':'In trasferta'):'Calendario in aggiornamento')+'</span>';
 $('day').textContent=last?'Dopo la '+last.n+'ª giornata':'Stagione in attesa';
 const scoreSquadra=result?(result.casa?result.m[4].split('-'):result.m[4].split('-').reverse()).join('–'):'';
 const ultima=result?'<div class="fixture-line"><strong class="result '+(result.pt===0?'loss':result.pt===3?'win':'')+'">'+escape(scoreSquadra)+'</strong><div>'+escape(result.label+' contro '+(result.casa?result.m[3]:result.m[0]))+'<small>Fantapunti '+dec(result.m[result.casa?1:2])+'–'+dec(result.m[result.casa?2:1])+'</small></div></div>':'<p>Nessuna partita conclusa.</p>';
 if(bozza==='a'){
  $('contenuto').innerHTML='<div class="summary"><div class="standing"><div><div class="position">'+(pos?pos:'—')+'<sup>'+(pos?'ª':'')+'</sup></div><div class="position-label">Posizione in classifica</div>'+move+'</div><div class="points"><b>'+(row?row.pt:'—')+'</b><span>Punti</span></div></div><div class="chart"><div class="chart-label"><b>Il cammino in classifica</b><span>Ultime '+serie.length+' giornate</span></div>'+linea(serie)+'<p class="chart-note">Più in alto, migliore posizione · Tocca un punto</p></div></div><div class="fixtures"><div><span class="caption">Ultimo risultato'+(result?' · '+result.n+'ª giornata':'')+'</span>'+ultima+'</div><div>'+nextText+'</div></div>';
 }else{
  $('contenuto').innerHTML='<div class="ribbon"><div><b>'+(pos?pos+'º':'—')+' posto</b>'+move+'</div><span class="pts"><b>'+(row?row.pt:'—')+'</b>Punti</span></div><div class="score-focus"><div><span class="caption">Ultimo risultato'+(result?' · '+result.n+'ª giornata':'')+'</span>'+(result?'<div class="teams"><strong>'+escape(result.m[0])+'</strong><span class="big-score">'+escape(result.m[4].replace('-','–'))+'</span><strong>'+escape(result.m[3])+'</strong></div><p class="score-note">Fantapunti '+dec(result.m[1])+'–'+dec(result.m[2])+' · '+escape(result.label)+' per '+escape(team)+'</p>':'<p>Nessuna partita conclusa.</p>')+'</div><div class="chart"><div class="chart-label"><b>La forma, in punti</b><span>Ultime '+recent.length+'</span></div>'+barre(recent)+'<div class="form-key"><span><i></i>Vittoria</span><span><i class="n"></i>Pareggio</span><span><i class="p"></i>Sconfitta</span></div></div></div><div class="next-ribbon"><div>'+nextText+'</div><span class="next-icon" aria-hidden="true">↗</span></div>';
 }
 const firma=JSON.stringify(rounds.map(g=>({n:g.n,m:g.m}))),story=eventi&&eventi.firma===firma&&eventi.eventi.find(e=>e.giornata===(last&&last.n));
 $('news-text').textContent=story?story.titolo+': '+story.testo:'Le notizie della Lega sono nelle Notifiche.';
 $('read').hidden=false;document.querySelector('.news-dot').hidden=false;
}
document.querySelectorAll('button[data-bozza]').forEach(b=>b.onclick=()=>{bozza=b.dataset.bozza;render();});
document.querySelectorAll('button[data-skin]').forEach(b=>b.onclick=()=>{skin=b.dataset.skin;render();});
$('team').onchange=()=>{team=$('team').value;render();};
$('read').onclick=()=>{$('news-text').textContent='Nessuna novità da leggere.';$('read').hidden=true;document.querySelector('.news-dot').hidden=true;};
render();
Promise.all([fetch('https://giandjcosta.github.io/o-fant-a-girrr/data.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Calendario non disponibile');return r.json();}),fetch(ROOT+'cronache.json',{cache:'no-store'}).then(r=>r.ok?r.json():null).catch(()=>null)])
 .then(([d,cr])=>{D=d;eventi=cr;calcola();if(!D.teams.some(t=>t.name===team))team=D.teams[0].name;$('team').innerHTML=D.teams.map(t=>'<option value="'+escape(t.name)+'">'+escape(t.name)+'</option>').join('');$('team').value=team;render();})
 .catch(()=>{$('contenuto').innerHTML='<p>Il calendario non è raggiungibile. Riprova tra poco.</p>';$('team').disabled=true;});
})();
