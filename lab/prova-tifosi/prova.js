(function(){
'use strict';
const root=PROVA_TIFOSI.root,skin=location.pathname.includes('/stadio/')?'stadio':'lega',page=location.pathname.split('/').pop(),q=new URLSearchParams(location.search),before=q.get('prima')==='1';
document.documentElement.dataset.ptSkin=skin;
const E=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const N=t=>t==='The Blue brothers'?'The Blues Brothers':t==='stif dc'?'STIF DC':t;
let data,editoriale,team=q.get('squadra')||'Oranje VC',competition='lega',sportMvp=q.get('sezione')==='mvp',careerWeek=q.get('sezione')==='settimana';
function url(file,hash='',other=skin){const u=new URL(other+'/'+file,root);u.searchParams.set('squadra',team);if(before)u.searchParams.set('prima','1');if(file==='app.html'&&hash.replace(/^#/,'')==='sport')u.searchParams.set('sezione','mvp');if(file==='app.html'&&hash.replace(/^#/,'')==='carriera')u.searchParams.set('sezione','settimana');u.hash=hash;return u.href}
function skinUrl(){const u=new URL((skin==='lega'?'stadio':'lega')+'/'+page,root);u.search=location.search;u.hash=location.hash;return u.href}
const link=(f,h,t)=>'<a href="'+E(url(f,h))+'">'+t+' ›</a>';
const box=(id,title,body,kicker='')=>'<section class="pt-box" id="'+id+'">'+(kicker?'<div class="pt-kicker">'+E(kicker)+'</div>':'')+'<h2>'+E(title)+'</h2>'+body+'</section>';
const toolbar=document.createElement('aside');toolbar.className='pt-tools';toolbar.setAttribute('aria-label','Comandi della preview');
const change=flag=>{const u=new URL(location.href);u.searchParams.set('prima',flag);return u.href};
toolbar.innerHTML='<b>Laboratorio · Le tre novità</b><a href="'+E(change('1'))+'" aria-current="'+before+'">Prima</a><a href="'+E(change('0'))+'" aria-current="'+!before+'">Con proposte</a><a data-pt-skin href="'+E(skinUrl())+'">Grafica '+(skin==='lega'?'Stadio':'Lega')+'</a><a href="'+root+'index.html">Mappa</a><label>La tua squadra <select id="pt-team" aria-label="Squadra della preview"></select></label><small>Preview · Voti e giurie dimostrativi, salvati soltanto in questo browser. Nessuna pubblicazione o scrittura sul sito.</small><small id="pt-status" role="status"></small>';
document.body.prepend(toolbar);
function ballot(){return ProvaModel.ballot(data)}
function voteKey(){return 'og:prova-tifosi:voti:'+ballot().id}
function votes(){try{const v=JSON.parse(localStorage.getItem(voteKey())||'{}');return Object.fromEntries(Object.entries(v).filter(([t,c])=>data.teams.includes(t)&&ballot().candidates.some(x=>x.team===c)))}catch(e){return {}}}
function tally(){return ProvaModel.tallyOptional(ballot(),votes())}
function reason(c){return (c.away?'In trasferta':'In casa')+' contro '+N(c.op)+': '+c.gf+'–'+c.gs+'.'}
function episode(day){
 const done=ProvaModel.complete(data).filter(g=>g.n<=day),firma=JSON.stringify({league:done,cup:(data.cupRounds||[]).filter(c=>c.sa<=(done.at(-1)?.sa||0))});
 if(day===editoriale.giornata&&firma===editoriale.firma&&editoriale.squadre[team]){const e=editoriale.squadre[team];return {title:e.titolo,paragraphs:e.paragrafi}}
 const e=RaccontiSettimana.create(data,team,day),matches=ProvaModel.weeklyMatches(data,team,day),cup=matches.find(m=>m.comp==='Champions Cup');
 if(cup){const isHome=cup.a===team,s=cup.score.split('-').map(Number),gf=s[isHome?0:1],gs=s[isHome?1:0];e.paragraphs=e.paragraphs.slice();e.paragraphs[1]+=' La settimana comprende anche la Champions Cup: '+(gf>gs?'vittoria':gf===gs?'pareggio':'sconfitta')+' per '+gf+'–'+gs+' contro '+N(isHome?cup.b:cup.a)+'. Sono due incontri distinti nelle due competizioni.'}
 return e;
}
function storyCard(day,compact=false){const e=episode(day),matches=ProvaModel.weeklyMatches(data,team,day);return '<article class="pt-article-copy"><div class="pt-result">'+matches.length+' '+(matches.length===1?'incontro giocato':'incontri giocati')+' · '+matches.map(m=>m.comp).join(' + ')+'</div><h3>'+E(e.title)+'</h3>'+e.paragraphs.map(p=>'<p>'+E(p)+'</p>').join('')+(compact?'<div class="pt-links">'+link('app.html','carriera','Rileggi la tua stagione')+'</div>':'')+'</article>'}
function story(){const rounds=ProvaModel.complete(data).slice().reverse();return box('pt-storia','La mia settimana','<p class="pt-sub">'+E(N(team))+' · Un racconto diverso per ogni giornata e per il suo percorso.</p>'+rounds.map((g,i)=>'<details class="pt-week" data-pt-day="'+g.n+'"'+(i===0?' open':'')+'><summary><span class="pt-day">'+g.n+'</span><span class="pt-week-title"><b>'+g.n+'ª giornata</b><small>'+E(episode(g.n).title)+'</small></span></summary><div class="pt-week-body">'+storyCard(g.n)+'</div></details>').join(''),'La tua stagione · 2026/27')}
function poll(){const b=ballot();if(!b?.candidates.length)return box('pt-mvp','Squadra della settimana','<p>Le candidature saranno disponibili dopo una giornata completa.</p>');const rows=tally(),human=votes(),totalHuman=Object.keys(human).length;
 return box('pt-mvp','Squadra della settimana','<p>Quale club ha lasciato il segno nella '+b.day+'ª giornata? Redazione e personaggi della Curva partecipano sempre. Il tuo voto è facoltativo.</p><div class="pt-jury"><div><b>Redazione</b><span>'+ (totalHuman?'40%':'50%')+' del risultato</span></div><div><b>Personaggi della Curva</b><span>'+(totalHuman?'40%':'50%')+' del risultato</span></div><div><b>Allenatori</b><span>'+(totalHuman?'20% · '+totalHuman+' '+(totalHuman===1?'voto':'voti'):'Nessun voto · Nessuna attesa')+'</span></div></div><div class="pt-grid">'+rows.map((r,i)=>'<article class="pt-candidate"><div><span class="pt-chip">'+(i===0?'In testa':'Candidata')+'</span><h3>'+E(N(r.team))+'</h3></div><span class="pt-number">'+r.total.toLocaleString('it-IT',{maximumFractionDigits:1})+'<small>%</small></span><p>'+E(reason(r))+'</p><div class="pt-meter"><span style="width:'+r.total+'%"></span></div><small class="pt-sub">Redazione '+r.red+' · Personaggi '+r.personaggi+' · Allenatori '+r.umani+'</small><button type="button" data-pt-vote="'+E(r.team)+'" aria-pressed="'+(human[team]===r.team)+'">'+(human[team]===r.team?'Il tuo voto ✓':'Vota '+E(N(r.team)))+'</button></article>').join('')+'</div><p id="pt-vote-status" role="status">'+(human[team]?'Hai votato '+E(N(human[team]))+'. Puoi cambiare o ritirare il voto.':'Non hai votato. Il premio viene assegnato anche senza il tuo voto.')+'</p>'+(human[team]?'<button type="button" data-pt-withdraw>Ritira il mio voto</button>':'')+'<details><summary>Giurie e criteri</summary><p>Con i voti degli allenatori: 40% redazione, 40% personaggi e 20% allenatori. Senza voti umani: 50% per ciascuna delle prime due giurie. I voti dei personaggi sono normalizzati, così il loro numero non decide da solo il premio.</p><p>Tre candidature basate sulle vittorie della giornata, sul margine del risultato e sull’avversario. La redazione motiva la scelta. In questa preview le preferenze automatiche sono esempi, non voti già espressi dai servizi della lega.</p></details><div class="pt-links">'+link('curva.html','pt-mvp','Il voto nella Curva')+link('albo.html','pt-archivio','Archivio del premio')+'</div>','MVP dei tifosi · Club · '+b.day+'ª giornata');
}
function derby(){const x=ProvaModel.derbyClassifica(data,competition);return box('pt-derby','Classifica dei Derby','<p>I punti conquistati negli scontri fra le coppie ufficiali della stagione.</p><div class="seg pt-competition" role="group" aria-label="Competizione dei Derby"><button data-pt-comp="lega" aria-pressed="'+(competition==='lega')+'">Campionato</button><button data-pt-comp="cup" aria-pressed="'+(competition==='cup')+'">Champions Cup</button></div>'+(x.rows.length?'<table class="pt-table"><thead><tr><th>#</th><th>Squadra</th><th>Pti</th><th>G</th><th>V</th><th>N</th><th>P</th></tr></thead><tbody>'+x.rows.map(r=>'<tr'+(r.team===team?' class="pt-you"':'')+'><td>'+r.rank+'</td><td>'+E(N(r.team))+'</td><td class="pt-wins">'+r.pt+'</td><td>'+r.g+'</td><td>'+r.v+'</td><td>'+r.n+'</td><td>'+r.p+'</td></tr>').join('')+'</tbody></table>':'<p>Nessun Derby concluso in questa competizione.</p>')+'<p class="pt-sub">Pti = Punti · G = Giocati · V = Vittorie · N = Pareggi · P = Sconfitte. Vittoria 3 punti, pareggio 1. A pari punti: vittorie e differenza reti; altrimenti pari merito.</p><details><summary>Le '+x.matches.length+' partite conteggiate</summary><ul class="pt-audit">'+x.matches.map(m=>'<li><b>'+E(N(m.a))+' '+m.score+' '+E(N(m.b))+'</b><small>'+m.day+'ª giornata · '+E(m.name)+'</small></li>').join('')+'</ul><p class="pt-sub">Registro dei Derby ufficiali verificato il 12 novembre. Non ricostruisce cambi storici di ufficialità non conservati.</p></details>','Derby · Stagione 2026/27').replace('<section','<section data-pt-competition="'+competition+'"')}
function archive(){return box('pt-archivio','MVP dei tifosi','<p>Qui resteranno la squadra vincitrice, la giornata e la motivazione della redazione.</p><p class="pt-sub">Il premio è in prova: alle giornate precedenti non attribuiamo vincitrici mai votate.</p>'+link('app.html','sport','Apri la votazione'),'Albo d’oro · Record')}
function insert(host,id,content,first=false){if(host&&!document.getElementById(id))host.insertAdjacentHTML(first?'afterbegin':'beforeend',content)}
function home(){const summary=document.querySelector('.v55-summary');if(!summary)return;
 if(!document.getElementById('pt-home-story'))summary.insertAdjacentHTML('afterend','<section class="pt-box pt-compact" id="pt-home-story"><details><summary>La tua settimana · '+E(N(team))+'</summary>'+storyCard(ProvaModel.complete(data).at(-1).n,true)+'</details></section>');
 const host=document.getElementById('v53news');if(host&&!document.getElementById('pt-mvp-notice'))host.insertAdjacentHTML('afterbegin','<a class="v55-news-link" id="pt-mvp-notice" href="'+E(url('app.html','sport'))+'"><span class="v53-dot"></span><span><b>Squadra della settimana</b><small>Scopri le candidate · Puoi votare anche tu</small></span><span>›</span></a>');
}
function sport(){if(!location.hash.includes('sport'))return;const nav=[...document.querySelectorAll('#view .seg')].find(e=>e.querySelector('[data-sp]'));if(!nav)return;
 if(!nav.querySelector('[data-pt-sport]'))nav.querySelector('[data-sp="giornale"]').insertAdjacentHTML('afterend','<button type="button" data-pt-sport="mvp" aria-pressed="false">Squadra della settimana</button>');
 const btn=nav.querySelector('[data-pt-sport]');btn.setAttribute('aria-pressed',String(sportMvp));
 const view=document.getElementById('view');let after=false;[...view.children].forEach(el=>{if(el===nav){after=true;return}if(after&&el.id!=='pt-mvp')el.hidden=sportMvp});
 if(sportMvp){nav.querySelectorAll('[data-sp]').forEach(b=>b.setAttribute('aria-pressed','false'));insert(view,'pt-mvp',poll())}else document.getElementById('pt-mvp')?.remove();
}
function career(){if(!location.hash.includes('carriera'))return;const nav=document.querySelector('#view [data-ctab]')?.closest('.seg');if(!nav)return;
 if(!nav.querySelector('[data-pt-week]'))nav.insertAdjacentHTML('beforeend','<button type="button" data-pt-week aria-pressed="false">La mia settimana</button>');
 nav.querySelector('[data-pt-week]').setAttribute('aria-pressed',String(careerWeek));
 const view=document.getElementById('view');let after=false;[...view.children].forEach(el=>{if(el===nav){after=true;return}if(after&&el.id!=='pt-storia')el.hidden=careerWeek});
 if(careerWeek){nav.querySelectorAll('[data-ctab]').forEach(b=>b.setAttribute('aria-pressed','false'));insert(view,'pt-storia',story())}else document.getElementById('pt-storia')?.remove();
}
function section(value){const u=new URL(location.href);if(value)u.searchParams.set('sezione',value);else u.searchParams.delete('sezione');history.replaceState(null,'',u);document.querySelector('a[data-pt-skin]').href=skinUrl()}
function mount(){if(before||!data)return;
 if(page==='index.html')home();
 if(page==='curva.html')insert(document.getElementById('v53sondaggio'),'pt-mvp',poll(),true);
 if(page==='derby.html')insert(document.getElementById('al'),'pt-derby',derby(),true);
 if(page==='derby-stagione.html')insert(document.getElementById('al'),'pt-derby',derby(),true);
 if(page==='app.html'){
  sport();
  career();
 }
 if(page==='albo.html'){
  insert(document.querySelector('[data-ap="rec"]'),'pt-archivio',archive());
  insert(document.querySelector('[data-ap="derby"]'),'pt-derby-access','<a class="card" id="pt-derby-access" href="'+E(url('derby.html','pt-derby'))+'" style="display:block;text-decoration:none;color:inherit"><h3>Classifica dei Derby</h3><div style="font-weight:700;font-size:14px">I punti conquistati contro i rivali ufficiali →</div></a>');
  if(location.hash==='#pt-archivio'){const b=document.querySelector('[data-at="rec"]');if(b&&b.getAttribute('aria-selected')!=='true')b.click()}
 }
}
document.addEventListener('click',e=>{
 const vote=e.target.closest('[data-pt-vote],[data-pt-withdraw]');if(vote&&data){e.preventDefault();e.stopImmediatePropagation();const v=votes();if(vote.hasAttribute('data-pt-withdraw'))delete v[team];else v[team]=vote.dataset.ptVote;localStorage.setItem(voteKey(),JSON.stringify(v));const p=document.getElementById('pt-mvp');if(p)p.outerHTML=poll();return}
 const comp=e.target.closest('[data-pt-comp]');if(comp){e.preventDefault();e.stopImmediatePropagation();competition=comp.dataset.ptComp;document.getElementById('pt-derby').outerHTML=derby();return}
 const sp=e.target.closest('[data-pt-sport]');if(sp){e.preventDefault();e.stopImmediatePropagation();sportMvp=true;section('mvp');mount();return}
 if(e.target.closest('[data-sp]')){sportMvp=false;section('');document.getElementById('pt-mvp')?.remove();document.querySelectorAll('#view>[hidden]').forEach(x=>x.hidden=false)}
 if(e.target.closest('[data-pt-week]')){e.preventDefault();e.stopImmediatePropagation();careerWeek=true;section('settimana');mount();return}
 if(e.target.closest('[data-ctab]')){careerWeek=false;section('');document.getElementById('pt-storia')?.remove();document.querySelectorAll('#view>[hidden]').forEach(x=>x.hidden=false)}
},true);
Promise.all([fetch(root+'dati.json').then(r=>r.json()),fetch(root+'editoriale.json').then(r=>r.json())]).then(([d,ed])=>{data=d;editoriale=ed;if(!d.teams.includes(team))team='Oranje VC';const select=document.getElementById('pt-team');select.innerHTML=d.teams.map(t=>'<option value="'+E(t)+'"'+(t===team?' selected':'')+'>'+E(N(t))+'</option>').join('');select.addEventListener('change',()=>{const u=new URL(location.href);u.searchParams.set('squadra',select.value);location.href=u.href});mount();let queued=false;new MutationObserver(()=>{if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;mount()})}).observe(document.body,{subtree:true,childList:true})}).catch(e=>{document.getElementById('pt-status').textContent='La preview non ha caricato i dati locali: '+e.message});
window.addEventListener('hashchange',mount);
})();
