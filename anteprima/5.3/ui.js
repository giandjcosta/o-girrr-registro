/* O Girrr 5.3 — preview conservativa, nessuna scrittura al database */
(function(){
'use strict';
var root='https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/anteprima-53-integrata/anteprima/5.3/';
var mode=document.body.dataset.v53||'',skin=document.body.dataset.v53Skin||'lega',dataUrl='https://giandjcosta.github.io/o-fant-a-girrr/data.json';
var k='og:53:',teamList=[],D=null;
function el(id){return document.getElementById(id)}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function n(v){return Number(v)||0}
function dec(x){return Number.isFinite(Number(x))?Number(x).toLocaleString('it-IT',{maximumFractionDigits:2}):'—'}
function get(key,def){try{var x=localStorage.getItem(k+key);return x?JSON.parse(x):def}catch(e){return def}}
function set(key,x){try{localStorage.setItem(k+key,JSON.stringify(x))}catch(e){}}
function mark(t){return '<span class="v53-kicker">'+esc(t)+'</span>'}
function note(t){return '<div class="v53-empty">'+esc(t)+'</div>'}
function matchPlayed(m,cup){return Array.isArray(m)&&m[cup?5:4]&&m[cup?5:4]!=='-'}
function games(cup){return ((D&&D.cal&&(cup?D.cal.cup:D.cal.lega))||[]).slice()}
function completeRounds(cup){return games(cup).filter(function(g){return g.m&&g.m.length&&g.m.every(function(m){return matchPlayed(m,cup)})})}
function latest(){var g=completeRounds(false);return g[g.length-1]||null}
function next(){return games(false).find(function(g){return g.m&&g.m.some(function(m){return !matchPlayed(m,false)})})||null}
function mFor(g,t){return g&&g.m&&g.m.find(function(m){return m[0]===t||m[3]===t})}
function allFinished(){var out=[];games(false).forEach(function(g){(g.m||[]).forEach(function(m,i){if(matchPlayed(m,false))out.push({g:g,m:m,id:g.n+'-'+i})})});return out.reverse()}
function ranks(until){var map={};(D.teams||[]).forEach(function(t){map[t.name]={team:t.name,pt:0,fp:0,gf:0,gs:0,g:0}});
games(false).filter(function(g){return g.n<=until}).forEach(function(g){(g.m||[]).forEach(function(m){if(!matchPlayed(m,false))return;
var a=map[m[0]],b=map[m[3]],r=String(m[4]).split('-').map(Number);if(!a||!b||!Number.isFinite(r[0])||!Number.isFinite(r[1]))return;
a.g++;b.g++;a.pt+=r[0]>r[1]?3:r[0]===r[1]?1:0;b.pt+=r[0]<r[1]?3:r[0]===r[1]?1:0;
a.fp+=n(m[1]);b.fp+=n(m[2]);a.gf+=r[0];a.gs+=r[1];b.gf+=r[1];b.gs+=r[0]})});
return Object.values(map).sort(function(a,b){return b.pt-a.pt||b.fp-a.fp||b.gf-b.gs-(a.gf-a.gs)||a.team.localeCompare(b.team)})}
function href(which){return root+which+'-'+skin+'.html'}
function nav(){
var names=[['index','⌂','Home'],['tabellone','▤','Tabellone'],['albo','★','Albo d’oro'],['curva','♬','Curva'],['notifiche','◉','Notifiche']];
var current=mode==='home'?'index':mode;
var h='<nav class="v53 v53-menu" aria-label="Navigazione Anteprima 5.3">'+names.map(function(x){return '<a href="'+href(x[0])+'" '+(current===x[0]?'aria-current="page"':'')+'>'+x[1]+' '+esc(x[2])+'</a>'}).join('')+'</nav>';
var target=el('v53nav');if(target)target.innerHTML=h;
}
function redirect(){
document.addEventListener('click',function(e){
 var a=e.target.closest&&e.target.closest('a[href]');
 if(a&&a.closest('.v53'))return;
 if(a){var val=(a.getAttribute('href')||'').split('#')[0].split('?')[0],end=val.split('/').pop();if(['index.html','tabellone.html','albo.html','curva.html'].includes(end)&&!val.startsWith('https:')&&!val.startsWith('http:')){e.preventDefault();e.stopImmediatePropagation();location.href=root+end.replace('.html','')+'-'+skin+'.html';return}}
 if(mode==='curva'&&e.target.closest&&e.target.closest('button:not(.v53 button),textarea:not(.v53 textarea),input:not(.v53 input)')){e.preventDefault();e.stopImmediatePropagation();}
},true);
if(mode==='curva')document.addEventListener('submit',function(e){if(!e.target.closest('.v53')){e.preventDefault();e.stopImmediatePropagation()}},true);
}
function load(cb){fetch(dataUrl,{cache:'no-store'}).then(function(r){if(!r.ok)throw Error('Dati temporaneamente indisponibili');return r.json()}).then(function(v){if(!v||!v.cal||!v.teams)throw Error('Formato dati non riconosciuto');D=v;teamList=v.teams.map(function(t){return t.name});cb()}).catch(function(e){var ids=mode==='home'?['v53metrics','v53news']:mode==='notifications'?['v53notifications']:mode==='board'?['v53boardcontent']:mode==='albo'?['v53annual']:['v53poll'];ids.forEach(function(id){if(el(id))el(id).innerHTML=note('I dati della stagione non sono raggiungibili. La navigazione e le sezioni originali restano disponibili.')});console.warn('5.3 dati non caricati:',e.message)})}
function teamPicker(id,cb){
 var s=el(id);if(!s)return;var t=get('team',teamList[0]);if(teamList.indexOf(t)<0)t=teamList[0];s.innerHTML=teamList.map(function(x){return '<option value="'+esc(x)+'">'+esc(x)+'</option>'}).join('');s.value=t;s.addEventListener('change',function(){set('team',s.value);cb(s.value)});cb(t)
}
function home(){
teamPicker('v53team',function(t){
 var day=latest(),nm=day&&day.n,prev=nm&&nm>1?ranks(nm-1):[],cls=nm?ranks(nm):[],rank=cls.findIndex(function(x){return x.team===t})+1,prevRank=prev.findIndex(function(x){return x.team===t})+1;
 var nextDay=next(),op=mFor(nextDay,t),res=allFinished().find(function(x){return x.m[0]===t||x.m[3]===t});
 var txt='';
 txt+='<div class="v53-metric featured"><small>La tua squadra</small><b>'+esc(t)+'</b><em>'+(rank?rank+'ª posizione': 'Classifica in attesa')+(rank&&prevRank&&prevRank!==rank?' · '+(prevRank>rank?'↑ '+(prevRank-rank):'↓ '+(rank-prevRank))+' posizione/i':'')+'</em></div>';
 txt+='<div class="v53-metric"><small>Prossima giornata</small><b>'+esc(op?(op[0]===t?op[3]:op[0]):'Da definire')+'</b><em>'+(op?nextDay.n+'ª giornata':'Calendario in aggiornamento')+'</em></div>';
 txt+='<div class="v53-metric"><small>Ultimo risultato</small><b>'+esc(res?res.m[0]+' '+res.m[4]+' '+res.m[3]:'—')+'</b><em>'+(res?'Fantapunti '+dec(res.m[1])+'–'+dec(res.m[2]):'Nessuna partita conclusa')+'</em></div>';
 el('v53metrics').innerHTML=txt;
 var seen=get('seen:'+t,null),news=[],now={day:nm||0,rank:rank||0,op:op&&(op[0]===t?op[3]:op[0])||'',score:res&&res.m[4]||''};
 if(seen&&seen.day!==now.day)news.push('Nuovi risultati dopo la '+(nm||'ultima')+'ª giornata');
 if(seen&&seen.rank!==now.rank&&rank)news.push('La tua posizione in classifica è cambiata');
 if(seen&&seen.op!==now.op&&now.op)news.push('È cambiato il prossimo avversario');
 var aside=el('v53news');aside.innerHTML=news.length?news.map(function(x){return '<span class="v53-dot" style="display:inline-block;margin-right:6px"></span>'+esc(x)+' &nbsp; '}).join(''):'Risultati, Curva e notizie della Lega.';
 var b=el('v53read');if(b)b.onclick=function(){set('seen:'+t,now);aside.textContent='Tutto aggiornato per '+t+'.'};
 });
}
function board(){
var holder=el('v53boardcontent'),rounds=completeRounds(false),sets=ranks((latest()||{}).n||0);
if(!holder)return;
var buttons=el('v53boardtabs');
function switchTo(part){buttons.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-selected',b.dataset.view===part?'true':'false')});if(part==='compare')compare();else matchCenter()}
buttons.addEventListener('click',function(e){var b=e.target.closest('button[data-view]');if(b)switchTo(b.dataset.view)});
function compare(){
 var opts=rounds.map(function(g){return '<option value="'+g.n+'">'+g.n+'ª giornata</option>'}).join('');
 if(rounds.length<2){holder.innerHTML=note('Servono due giornate complete per confrontare i movimenti in classifica.');return}
 holder.innerHTML='<div class="v53-field"><label for="v53from">Dalla</label><select class="v53-select" id="v53from">'+opts+'</select><label for="v53to">Alla</label><select class="v53-select" id="v53to">'+opts+'</select></div><div id="v53delta" class="v53-row"></div><p class="v53-muted">Confronto aggiuntivo: il Tabellone originale sopra rimane completo e invariato.</p>';
 var a=el('v53from'),b=el('v53to');a.value=String(rounds[Math.max(0,rounds.length-3)].n);b.value=String(rounds[rounds.length-1].n);
 function update(){var x=ranks(n(a.value)),y=ranks(n(b.value));el('v53delta').innerHTML=y.map(function(t,i){var p=x.findIndex(function(v){return v.team===t.team})+1,d=p-(i+1);return '<div class="v53-box"><small>'+(i+1)+'º posto · '+esc(t.team)+'</small><strong>'+(d>0?'↑ '+d+' posizioni':d<0?'↓ '+(-d)+' posizioni':'= stessa posizione')+'</strong><small>'+t.pt+' punti · '+dec(t.fp)+' Fantapunti · DR '+(t.gf-t.gs)+'</small></div>'}).join('')}
 a.onchange=update;b.onchange=update;update();
}
function matchCenter(){
var matches=allFinished();if(!matches.length){holder.innerHTML=note('Il centro partita si aprirà dopo il primo incontro concluso.');return}
 holder.innerHTML='<div class="v53-field"><label for="v53match">Scegli la partita</label><select class="v53-select" id="v53match" style="flex:1;min-width:160px">'+matches.slice(0,70).map(function(x){return '<option value="'+esc(x.id)+'">'+x.g.n+'ª · '+esc(x.m[0]+' '+x.m[4]+' '+x.m[3])+'</option>'}).join('')+'</select></div><div id="v53matchstats"></div>';
 var select=el('v53match');function draw(){var x=matches.find(function(v){return v.id===select.value})||matches[0],m=x.m;el('v53matchstats').innerHTML='<div class="v53-row"><div class="v53-box"><span class="v53-mini-title">RISULTATO UFFICIALE</span><div class="score">'+esc(m[0]+' '+m[4]+' '+m[3])+'</div><small>Campionato · '+x.g.n+'ª giornata</small></div><div class="v53-box"><span class="v53-mini-title">DATI LEGHE FANTACALCIO</span><div class="score">'+dec(m[1])+' <em>–</em> '+dec(m[2])+'</div><small>Fantapunti · Non confondere con i gol</small></div></div><p class="v53-muted">Centro partita post-giornata: risultato, Fantapunti e collegamento alle formazioni reali dello Spogliatoio; nessun dato live inventato.</p>'}select.onchange=draw;draw()
}
switchTo('compare');
}
function annual(){
var tgt=el('v53annual');if(!tgt)return;var g=latest(),r=ranks(g&&g.n||0),gamesPlayed=allFinished(),teams=D.teams||[];
var all=gamesPlayed.reduce(function(z,x){var m=x.m;z.push({team:m[0],fp:n(m[1]),against:m[3],result:m[4],day:x.g.n});z.push({team:m[3],fp:n(m[2]),against:m[0],result:m[4],day:x.g.n});return z},[]);
var hi=all.slice().sort(function(a,b){return b.fp-a.fp})[0];
var rosters=teams.map(function(t){return {name:t.name,players:(t.pl||[]).length,value:(t.pl||[]).reduce(function(s,p){return s+n(p.c)},0)}}).sort(function(a,b){return b.value-a.value});
var cl='<ol>'+r.slice(0,3).map(function(x,i){return '<li><b>'+esc(x.team)+'</b> — '+x.pt+' punti ('+dec(x.fp)+' Fantapunti)</li>'}).join('')+'</ol>';
var year='<div class="v53-crumb">'+(g?'Campionato · giocata la '+g.n+'ª giornata':'Campionato · stagione in corso')+'. Nessun titolo assegnato prima della fine ufficiale.</div>';
var items=[
['Classifica e podio',cl+'<p class="v53-muted">Posizioni provvisorie. Titolo e podio definitivi soltanto a stagione conclusa.</p>'],
['Rose e valori','<ul>'+rosters.slice(0,10).map(function(x){return '<li>'+esc(x.name)+': '+x.players+' giocatori · '+dec(x.value)+' fantacrediti di costo registrato</li>'}).join('')+'</ul><p class="v53-muted">Il valore è ricavato dai dati di rosa disponibili, non è una valutazione di mercato.</p>'],
['Record di giornata',hi?'<p><strong>'+esc(hi.team)+'</strong>: '+dec(hi.fp)+' Fantapunti alla '+hi.day+'ª giornata contro '+esc(hi.against)+' (risultato '+esc(hi.result)+').</p>':note('Nessun record disponibile.')],
['Champions Cup','<p>Gironi, risultati, quarti, semifinali e finale sono consultabili nella scheda Champions Cup del Tabellone. Le vittorie sono assegnate solo quando i risultati sono pubblicati.</p><a class="v53-btn ghost" href="'+href('tabellone')+'">Apri la Champions Cup</a>'],
['Albo storico e stagioni precedenti','<p>Le stagioni precedenti mantengono tutti i dati dell’Albo già presente nella pagina. Nuovi record storici non conservati: <strong>Dato non conservato</strong>.</p>']
];
tgt.innerHTML=year+items.map(function(item,i){return '<details class="v53-details" '+(i===0?'open':'')+'><summary>'+esc(item[0])+'</summary><div class="v53-detailbody">'+item[1]+'</div></details>'}).join('');
}
function optsPoll(){var g=next(),games=(g&&g.m)||[];return {day:g&&g.n||0,opts:games.map(function(m){return m[0]+' – '+m[3]})}}
/* Le voci sono quelle della banca reale curva-banca.js. Tono distinto,
   variazioni deterministiche per giornata e, se disponibile, vere reazioni CVB. */
var BOT_FRASI=[
 ['il_barista','Il Barista',[
 'Per {sfida} ho già acceso la macchina del caffè. Il risultato lo discutiamo al bancone.',
 'Qui al bar abbiamo un pronostico per ogni partita. E un caffè per ogni pronostico sbagliato.',
 'Per la {giornata}ª giornata il tavolo vicino alla TV è già prenotato. Da tutti.']],
 ['mister_divano','Mister Divano',[
 'Io punterei su {sfida}. Se mi date un telecomando vi spiego pure il modulo.',
 'La partita da seguire? Quella in cui ascoltano finalmente il mio 4-3-3. Quindi nessuna.',
 'A {sfida} suggerisco pressing alto. Mi alzo dal divano solo per il gol.']],
 ['il_complottista','Il Complottista',[
 'Chi ha deciso che {sfida} è la sfida del giorno? Io voglio il verbale.',
 'Vi fidate davvero dei sondaggi? Io chiedo il controllo incrociato delle schede.',
 'Non dico che il calendario sia sospetto. Dico che lo sto guardando con una lente.']],
 ['il_super_tifoso','Il Super Tifoso',[
 'Per me la partita è {sfida}! Sempre sostenuta, da circa cinque minuti.',
 'Io tifo la prima. Quale? Aspetto che esca la nuova classifica.',
 'Per la {giornata}ª ci sarò. Sciarpa pronta e pronostico già dimenticato.']],
 ['nonno_cesare','Nonno Cesare',[
 'Ai miei tempi una partita bastava per tutta la domenica. Adesso vorrei vederle tutte.',
 'Ho già preparato la radiolina per {sfida}. E sì, funziona ancora.',
 'Una volta votavamo al bar con un cenno del capo. Ma mi piace vedere tutta la Curva qui.']],
 ['statistico_folle','Lo Statistico Folle',[
 'La capolista è {capolista}, ma io continuo a calcolare anche le probabilità del caffè.',
 'Le percentuali del sondaggio le voglio confrontare con la classifica dopo la {giornata}ª.',
 'Ho aperto un foglio di calcolo per decidere fra le partite. Il foglio è ancora indeciso.']],
 ['il_romantico_del_pallone','Il Romantico del Pallone',[
 '{sfida}: non conosco il finale, ed è proprio per questo che la seguirei.',
 'I sondaggi passano. Il ricordo della partita resta. Basta che sia una bella sfida.',
 'In fondo, alla {giornata}ª ci interessa ancora la stessa cosa: il pallone.']],
 ['gufo_professionista','Il Gufo Professionista',[
 'Mi aspetto grandi cose da {sfida}. Ora, dopo questa frase, non posso più guardarla.',
 'Voto con fiducia. Ma non è detto che la fiducia sia una buona notizia.',
 'Spero vincano tutti. È statisticamente impossibile, ma la gufata è pronta.']],
 ['telecronista_stanco','Il Telecronista Stanco',[
 'Un altro turno e un altro sondaggio. Vi voglio bene, ma mi manca il sonno.',
 'A {sfida} ci sarò. Se il microfono regge.',
 'La {giornata}ª sarà emozionante. Lo dico con le ultime energie disponibili.']],
 ['arbitro_in_pensione','L’Arbitro in Pensione',[
 'Per {sfida} voglio solo due cose: rispetto del regolamento e un bel fischio finale.',
 'Un voto nel sondaggio non equivale a un voto in campo. Lo preciso per regolamento.',
 'Chiunque vinca il sondaggio, in partita contano i gol. Come sempre.']]
];
function botComments(p){
 var top=latest()&&ranks(latest().n)[0],sfida=p.opts[p.day%p.opts.length]||p.opts[0],ctx={sfida:sfida,giornata:p.day,capolista:top?top.team:'da definire'};
 var list=BOT_FRASI.map(function(b,i){var arr=b[2],choice=(p.day+i*7)%arr.length;return [b[1],arr[choice].replace(/\{(\w+)\}/g,function(_,key){return ctx[key]||''})]});
 try{var bank=window.CVB;if(bank&&bank.reazioni&&bank.PERS){
   var ts=Date.now()-24*3600000;
   var replies=bank.reazioni('p53-sondaggio-'+p.day,ts,Date.now(),teamList,'Quale partita seguiresti alla '+p.day+'ª giornata?').r||[];
   var names={il_complottista:'Il Complottista',il_super_tifoso:'Il Super Tifoso',mister_divano:'Mister Divano',il_barista:'Il Barista',nonno_cesare:'Nonno Cesare',statistico_folle:'Lo Statistico Folle',il_romantico_del_pallone:'Il Romantico del Pallone',gufo_professionista:'Il Gufo Professionista',tifoso_arrabbiato:'Il Tifoso Arrabbiato',il_mago_cabala:'Il Mago della Cabala'};
   replies.filter(function(x){return bank.PERS[x.a]}).slice(0,5).forEach(function(x){list.push([names[x.a]||x.a,x.x])});
 }}catch(e){console.warn('Risposte CVB non disponibili nella prova',e.message)}
 return list;
}
function curva(){
var host=el('v53poll'),p=optsPoll(),key='poll-'+p.day;
if(!host)return;
if(!p.opts.length){host.innerHTML=note('Il sondaggio apparirà quando sarà disponibile il calendario del prossimo turno.');return}
var voted=get(key+'-vote',null),counts=get(key+'-counts',{}),comments=get(key+'-comments',[]);
var form='<div class="v53-sub">Prossimo turno · '+p.day+'ª giornata</div><h3>Quale sfida seguirai con più attenzione?</h3><form id="v53vote">'+p.opts.map(function(o,i){return '<label class="v53-poll-option"><input type="radio" name="v53choice" value="'+i+'" '+(voted===i?'checked':'')+'><span>'+esc(o)+'</span><small>'+n(counts[i])+' voti di prova</small></label>'}).join('')+'<button class="v53-btn" type="submit">Vota nel Lab</button></form><p class="v53-muted">Preferenze e commenti si salvano soltanto su questo dispositivo: non sono voti pubblicati nella Curva.</p>';
host.innerHTML=form+'<div class="v53-chat" id="v53dialog">'+botComments(p).map(function(t,i){return '<div class="v53-comment"><b>'+esc(t[0])+' · bot</b><p>'+esc(t[1])+'</p></div>'}).join('')+'</div><form id="v53comment" class="v53-field"><label for="v53message">Commenta il sondaggio</label><input class="v53-input" id="v53message" maxlength="280" required placeholder="Il tuo commento (solo locale)"><button class="v53-btn" type="submit">Commenta</button></form><div id="v53usercomments"></div>';
function redraw(){el('v53usercomments').innerHTML=comments.map(function(c){return '<div class="v53-comment"><b>Il tuo commento · locale</b><p>'+esc(c)+'</p></div>'}).join('')}
redraw();
el('v53vote').onsubmit=function(e){e.preventDefault();var v=el('v53vote').querySelector('input:checked');if(!v)return;var i=n(v.value);if(voted!==null)counts[voted]=Math.max(0,n(counts[voted])-1);counts[i]=n(counts[i])+1;voted=i;set(key+'-vote',i);set(key+'-counts',counts);curva()};
el('v53comment').onsubmit=function(e){e.preventDefault();var t=el('v53message').value.trim();if(!t)return;comments.push(t.slice(0,280));set(key+'-comments',comments);el('v53message').value='';redraw()};
}
function notifications(){
var to=el('v53notifications');if(!to)return;
var g=latest(),nx=next(),items=[];
if(g){items.push({key:'result-'+g.n,type:'partita',ic:'⚽',title:'Risultati della '+g.n+'ª giornata',detail:'Sono disponibili i risultati delle '+g.m.length+' partite di campionato.',link:href('tabellone')})}
if(g){var rs=ranks(g.n);if(rs.length)items.push({key:'ranking-'+g.n,type:'classifica',ic:'🏆',title:'Classifica aggiornata',detail:rs[0].team+' guida il campionato con '+rs[0].pt+' punti.',link:href('tabellone')})}
if(nx){items.push({key:'next-'+nx.n,type:'partita',ic:'📅',title:'Prossimo turno',detail:'La '+nx.n+'ª giornata è in calendario. Guarda gli incontri.',link:href('tabellone')})}
if(nx){items.push({key:'poll-'+nx.n,type:'curva',ic:'💬',title:'Sondaggio della Curva',detail:'Scegli la sfida più interessante del prossimo turno e commenta.',link:href('curva')})}
items.push({key:'annuario',type:'albo',ic:'📖',title:'Annuario 2026/27',detail:'Podio provvisorio, rose e record verificabili in un solo posto.',link:href('albo')});
var filters=el('v53filters'),chosen='tutte';
filters.innerHTML=[['tutte','Tutte'],['partita','Partite'],['classifica','Classifica'],['curva','Curva'],['albo','Albo']].map(function(x){return '<button class="v53-pill" data-f="'+x[0]+'" aria-selected="'+(chosen===x[0])+'">'+x[1]+'</button>'}).join('');
function render(){
var arr=items.filter(function(x){return chosen==='tutte'||x.type===chosen});to.innerHTML=arr.map(function(x){return '<article class="v53-notifcard" data-read="'+(!!get('read-'+x.key,false))+'"><span class="v53-ic">'+x.ic+'</span><div><b>'+esc(x.title)+'</b><p>'+esc(x.detail)+'</p><a href="'+x.link+'">Apri sezione ›</a></div></article>'}).join('')||note('Nessuna notifica per questo filtro.');
filters.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-selected',b.dataset.f===chosen?'true':'false')});
}
filters.onclick=function(e){var b=e.target.closest('button[data-f]');if(!b)return;chosen=b.dataset.f;render()};
el('v53markread').onclick=function(){items.forEach(function(x){set('read-'+x.key,true)});render()};
render();
}
/* Initial DOM integration: no existing Tabellone/Albo/Curva components are replaced. */
function init(){
nav();redirect();
if(mode==='home')load(home);
if(mode==='board')load(board);
if(mode==='albo')load(annual);
if(mode==='curva')load(curva);
if(mode==='notifications')load(notifications);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();