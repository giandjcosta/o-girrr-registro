/* O Girrr · Laboratorio: lettura dati pubblici, interazioni locali e nessuna scrittura al database. */
(function(){
'use strict';
var ORIGIN='https://giandjcosta.github.io/o-fant-a-girrr/',D=null,F=null,L=null,error='',loading=true;
var NAV=[['home','Oggi al Girrr'],['notifiche','Notifiche'],['sondaggio','Sondaggio'],['curva','La Curva'],['partita','Centro partita'],['tabellone','Tabellone'],['annuario','Annuario']];
var SECTIONS={partita:'Partite',classifica:'Tabellone',carriera:'Carriera',giornale:'Giornale',radio:'Radio',curva:'Curva',annuario:'Albo d’oro'};
var LINKS={partita:'girrr/tabellone.html',classifica:'girrr/tabellone.html',carriera:'girrr/app.html#carriera',giornale:'girrr/giornale.html',radio:'girrr/app.html#radio',curva:'girrr/curva.html',annuario:'girrr/albo.html'};
var S={tab:(location.hash||'#home').slice(1).split('?')[0],team:'Oranje VC',notif:'tutte',match:null,round1:1,round2:1,push:0,settings:{partita:true,classifica:true,carriera:true,giornale:true,radio:true,curva:true},pollSeen:false};
if(!NAV.some(function(x){return x[0]===S.tab}))S.tab='home';
function $(id){return document.getElementById(id)}
function safe(t){return String(t==null?'':t).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c]})}
function nfmt(n){return Number(n).toLocaleString('it-IT',{maximumFractionDigits:2})}
function read(k,def){try{var v=JSON.parse(localStorage.getItem('og-lab-'+k));return v===null?def:v}catch(e){return def}}
function save(k,v){try{localStorage.setItem('og-lab-'+k,JSON.stringify(v))}catch(e){}}
function played(m,cup){return String(m[cup?5:4])!=='-'}
function rounds(){return D&&D.cal&&D.cal.lega||[]}
function games(){return rounds().filter(function(r){return r.m&&r.m.some(function(m){return played(m,false)})})}
function lastDay(){var g=games();return g.length?g[g.length-1]:null}
function firstNext(){return rounds().filter(function(r){return r.m&&r.m.some(function(m){return !played(m,false)})})[0]||null}
function squadre(){return (D&&D.teams||[]).map(function(x){return x.name})}
function teamMatch(g,t){return g&&g.m&&g.m.filter(function(m){return m[0]===t||m[3]===t})[0]}
function avversario(m,t){return m?(m[0]===t?m[3]:m[0]):''}
function esito(m,t){if(!m||!played(m,false))return null;var k=String(m[4]).split('-').map(Number);return{gf:m[0]===t?k[0]:k[1],gs:m[0]===t?k[1]:k[0]}}
function lastMatch(t){var g=games().slice().reverse();for(var i=0;i<g.length;i++){var m=teamMatch(g[i],t);if(m&&played(m,false))return {g:g[i],m:m}}return null}
function classifica(n){var names=squadre(),a={};names.forEach(function(t){a[t]={t:t,pt:0,fp:0,g:0,v:0,p:0,n:0,gf:0,gs:0}});
rounds().forEach(function(g){if(g.n>n)return;(g.m||[]).forEach(function(m){if(!played(m,false))return;var x=a[m[0]],y=a[m[3]],sc=String(m[4]).split('-').map(Number);if(!x||!y||sc.length!==2)return;
x.g++;y.g++;x.fp+=Number(m[1])||0;y.fp+=Number(m[2])||0;x.gf+=sc[0];x.gs+=sc[1];y.gf+=sc[1];y.gs+=sc[0];
if(sc[0]>sc[1]){x.pt+=3;x.v++;y.p++}else if(sc[0]===sc[1]){x.pt++;y.pt++;x.n++;y.n++}else{y.pt+=3;y.v++;x.p++}
})});return Object.values(a).sort(function(x,y){return y.pt-x.pt||y.fp-x.fp||y.gf-y.gs-(x.gf-x.gs)||x.t.localeCompare(y.t)})}
function rankOf(n,t){return classifica(n).findIndex(function(x){return x.t===t})+1}
function snapshot(t){var day=lastDay(),lm=lastMatch(t),c=day?classifica(day.n):[],x=c.filter(function(z){return z.t===t})[0],next=firstNext(),m=teamMatch(next,t);
return {round:day?day.n:0,match:lm?lm.g.n+':'+lm.m[4]:'',position:x?c.indexOf(x)+1:null,pt:x?x.pt:0,opponent:avversario(m,t),updated:String(D.updated||'')}}
function snapshotKey(t){return 'seen-'+t.toLowerCase().replace(/[^a-z0-9]/g,'_')}
function notifs(){
var t=S.team,now=snapshot(t),old=read(snapshotKey(t),null),playedLast=lastMatch(t),up=firstNext(),m=teamMatch(up,t),arr=[];
if(up&&m)arr.push({id:'prossimo-'+up.n,cat:'partita',icon:'⚽',title:'Il prossimo avversario',body:'Alla '+up.n+'ª giornata affronti '+avversario(m,t)+'.',new:!!old&&old.opponent!==now.opponent,link:'partita'});
if(playedLast){var x=esito(playedLast.m,t);arr.push({id:'risultato-'+playedLast.g.n,cat:'partita',icon:'🏟️',title:'La tua ultima partita',body:t+' '+x.gf+'–'+x.gs+' '+avversario(playedLast.m,t)+' · '+playedLast.g.n+'ª giornata.',new:!!old&&old.match!==now.match,link:'partita'})}
if(now.position)arr.push({id:'classifica-'+now.round,cat:'classifica',icon:'📈',title:'La tua posizione',body:now.position+'° posto e '+now.pt+' punti dopo la '+now.round+'ª giornata.',new:!!old&&old.position!==now.position,link:'tabellone'});
var fid=L&&L.fid&&L.fid[t];if(fid!=null)arr.push({id:'fiducia-'+now.round,cat:'carriera',icon:'🤝',title:'Fiducia del presidente',body:'Valore attuale: '+nfmt(fid)+'. Consulta la Carriera per i dettagli.',new:false,link:'home'});
arr.push({id:'giornale',cat:'giornale',icon:'📰',title:'Girrr Sport',body:'Leggi il Giornale e il racconto dell’ultima giornata.',new:false,url:LINKS.giornale});
arr.push({id:'radio',cat:'radio',icon:'🎙️',title:'Radio Girrr',body:'Ascolta i commenti, le interviste e le rivalità.',new:false,url:LINKS.radio});
arr.push({id:'curva',cat:'curva',icon:'💬',title:'La Curva',body:'Apri le risposte alle conferenze e le discussioni tra allenatori.',new:false,url:LINKS.curva});
return arr}
function eventHtml(e){var l=e.link?'#'+e.link:e.url?ORIGIN+e.url:'#home';return '<a class="event" href="'+safe(l)+'"'+(e.url?' target="_blank" rel="noopener noreferrer"':'')+' style="text-decoration:none;color:inherit"><span class="ic">'+e.icon+'</span><span><b>'+safe(e.title)+(e.new?' <span class="tag gold">Novità</span>':'')+'</b><p>'+safe(e.body)+'</p><small>'+safe(SECTIONS[e.cat]||e.cat)+' · Apri ›</small></span></a>'}
function nav(){var num=D?notifs().filter(function(e){return e.new}).length:0;$('nav').innerHTML=NAV.map(function(x){return '<button type="button" data-nav="'+x[0]+'" class="'+(S.tab===x[0]?'on':'')+'" aria-pressed="'+(S.tab===x[0])+'">'+safe(x[1])+(x[0]==='notifiche'&&num?'<span class="count">'+num+'</span>':'')+'</button>'}).join('')}
function head(t,sub,choose){return '<div class="headline"><div><h2>'+t+'</h2><p>'+sub+'</p></div>'+(choose===false?'':'<div class="person"><label for="teamSelect">La tua squadra</label><select id="teamSelect">'+squadre().map(function(x){return '<option '+(x===S.team?'selected':'')+' value="'+safe(x)+'">'+safe(x)+'</option>'}).join('')+'</select></div>')+'</div>'}
function annualMini(){var teams=(D.teams||[]).map(function(t){return {n:t.name,total:(t.pl||[]).reduce(function(s,p){return s+(Number(p.c)||0)},0)}}).sort(function(a,b){return b.total-a.total}),h=null;
rounds().forEach(function(g){g.m.forEach(function(m){if(!played(m,false))return;[0,1].forEach(function(side){var x=Number(m[side?2:1]);if(!Number.isFinite(x))return;if(!h||x>h.val)h={val:x,t:m[side?3:0],g:g.n}})})});
return '<div class="anno"><span class="tag gold">Annuario · 2026/27</span><b>La stagione, in numeri</b><div class="grid2"><div class="mini"><small>Rosa più cara</small><strong>'+safe(teams[0]&&teams[0].n||'—')+'</strong><span class="tiny">'+nfmt(teams[0]&&teams[0].total||0)+' milioni</span></div><div class="mini"><small>Fantapunti più alti</small><strong>'+safe(h&&h.t||'—')+'</strong><span class="tiny">'+(h?nfmt(h.val)+' · '+h.g+'ª':'Non disponibile')+'</span></div></div><div class="annmenu"><a href="#annuario">Apri il riquadro completo ›</a><a href="index.html">Lab · Albo d’oro ›</a></div></div>'}

/* Voci editoriali: solo avvenimenti ricavati dalle partite della Lega */
/* Dialoghi ricavati dalle vere regole di curva-banca.js, soltanto in prova. */
var BOT_NOMI={
 il_complottista:'Il Complottista',il_super_tifoso:'Il Super Tifoso',mister_divano:'Mister Divano',
 il_romantico_del_pallone:'Il Romantico del Pallone',nonno_cesare:'Nonno Cesare',
 tifoso_arrabbiato:'Il Tifoso Arrabbiato',statistico_folle:'Lo Statistico Folle',
 il_barista:'Il Barista',il_mago_cabala:'Il Mago della Cabala',gufo_professionista:'Il Gufo Professionista',
 arbitro_in_pensione:'L’Arbitro in Pensione',ing_stadi:'L’Ingegnere degli Stadi',
 radio_spogliatoio:'Radio Spogliatoio',ciro_trattativa:'Ciro Trattativa',
 il_filosofo_del_pallone:'Il Filosofo del Pallone',telecronista_stanco:'Il Telecronista Stanco',
 bomber_da_bar:'Il Bomber da Bar',ex_ds_provincia:'L’Ex Direttore Sportivo',il_cugino_del_dt:'Il Cugino del DT',
 fc27_ratings:'FC27 Ratings',mamma_di_capitan:'Mamma di Capitan',la_suocera:'La Suocera',
 il_tassista:'Il Tassista',var_parlante:'Il VAR Parlante',americano_spaesato:'L’Americano Spaesato',
 fidanzata_stufa:'La Fidanzata Stufa'
};
function botReplies(k,txt){
 var b=window.CVB;if(!b||!b.reazioni)return[];
 var ris=b.reazioni('p8:'+k,Date.now()-10*3600000,Date.now(),squadre(),txt).r||[];
 return ris.filter(function(x){return b.PERS&&b.PERS[x.a]}).slice(0,10);
}
function curvaViva(){
 var g=lastDay(),playedMatches=g?(g.m||[]).filter(function(m){return played(m,false)}):[],next=firstNext(),leader=g?classifica(g.n)[0]:null,p=playedMatches[0],pari=playedMatches.find(function(m){var z=m[4].split('-').map(Number);return z[0]===z[1]});
 var posts=[];
 if(p)posts.push({h:'Il Barista',id:'il_barista',tag:'Terzo tempo',body:'Dalla '+g.n+'ª giornata: '+p[0]+' '+p[4]+' '+p[3]+'. Qui al bancone si commenta il risultato, non si rigioca la partita.'});
 if(leader)posts.push({h:'Lo Statistico Folle',id:'statistico_folle',tag:'Analisi',body:leader.t+' guida con '+leader.pt+' punti dopo la '+g.n+'ª. Il margine si misura in classifica, non nelle impressioni.'});
 if(pari)posts.push({h:'Il Romantico del Pallone',id:'il_romantico_del_pallone',tag:'Pareggi',body:pari[0]+' e '+pari[3]+' si fermano sul '+pari[4]+'. Un punto ciascuno: non è una vittoria, né una sconfitta.'});
 if(next&&next.m&&next.m.length)posts.push({h:'Mister Divano',id:'mister_divano',tag:'Prossimo turno',body:'Alla '+next.n+'ª giornata '+next.m[0][0]+' affronta '+next.m[0][3]+'. Dal divano ho già pronto il modulo. Senza nemmeno sapere la formazione.'});
 if(playedMatches.length)posts.push({h:'Il Complottista',id:'il_complottista',tag:'Dietro le quinte',body:'Risultati acquisiti, classifiche aggiornate. E io che volevo un complotto da discutere. Apriamo il dibattito.'});
 if(next)posts.push({h:'Il Super Tifoso',id:'il_super_tifoso',tag:'Gli spalti',body:'La '+next.n+'ª si avvicina. Sono pronto a sostenere la capolista. Anche se la settimana scorsa tifavo qualcun altro.'});
 return head('La Curva','I personaggi originali parlano delle partite e si rispondono. La loro banca di frasi e le regole esistenti restano la base.')+
 '<div class="layout"><section class="stack">'+posts.map(function(p,i){var replies=botReplies('curva:'+g?.n+':'+i,p.body);return '<article class="card thread"><div class="between"><b>'+safe(p.h)+'</b><span class="tag">'+safe(p.tag)+'</span></div><p>'+safe(p.body)+'</p><div class="line"></div><div class="between"><h4>Dialogo della Curva · '+replies.length+' risposte</h4><span class="tiny muted">Simulazione</span></div><div class="comments">'+replies.map(function(r){return '<div class="comment"><b>'+safe(BOT_NOMI[r.a]||r.a)+'</b><p>'+safe(r.x)+'</p></div>'}).join('')+'</div></article>'}).join('')+'</section>'+
 '<aside class="stack"><div class="card"><h3>Personaggi e regole già presenti</h3><p>Non cambiamo identità ai bot: gli stili, la banca di risposte, la variazione dei testi e il comportamento deterministico sono in <b>curva-banca.js</b>. Questa è una copia sperimentale con più dialoghi, non una pubblicazione nella Curva vera.</p><p>Le battute polemiche e ironiche sono commenti dei personaggi. Punteggi, partite e classifiche sono ricavati dai dati disponibili.</p><a class="action2" href="#sondaggio">Sondaggio con commenti ›</a></div></aside></div>';
}
function home(){
var t=S.team,day=lastDay(),next=firstNext(),m=teamMatch(next,t),last=lastMatch(t),r=day?rankOf(day.n,t):null,items=notifs(),priority=items.filter(function(e){return e.new}),top=priority.concat(items.filter(function(e){return !e.new})).slice(0,3),prev=read(snapshotKey(t),null);
return head('Oggi al Girrr',prev?'Da dove eri rimasto? Le notizie essenziali per la tua squadra.':'Il tuo punto di partenza: partite, situazione e novità.')+
'<div class="layout"><section class="stack"><div class="card"><div class="between"><span class="tag gold">IL TUO GIRRR</span><span class="tiny muted">'+(day?'Dopo la '+day.n+'ª giornata':'Stagione 2026/27')+'</span></div><p class="lead">'+safe(t)+'</p><div class="grid2">'+
'<div class="mini"><small>Posizione</small><strong>'+(r?r+'°':'—')+'</strong></div><div class="mini"><small>Prossimo avversario</small><strong>'+safe(avversario(m,t)||'Da definire')+'</strong><span class="tiny">'+(next?next.n+'ª giornata':'')+'</span></div>'+
'</div><div class="line"></div><div class="between"><a class="action" href="#partita">Centro partita ›</a><a class="action2" href="#tabellone">Apri Tabellone</a></div></div>'+
'<div class="card"><div class="between"><h3>Da non perdere</h3><button class="action2" data-mark>Segna come letto</button></div><div class="events">'+top.map(eventHtml).join('')+'</div></div>'+
'<div class="card"><div class="between"><h3>La voce della Lega</h3><a class="action2" href="#sondaggio">Vota e commenta</a></div><p>Quale sfida del prossimo turno merita più attenzione?</p><div class="grid2"><div class="mini"><small>Discussione</small><strong>Sondaggio della giornata</strong></div><div class="mini"><small>Commenti</small><strong>'+(read('comments-'+(next?next.n:0),[]).length+botReplies('poll:'+(next?next.n:0),'Quale partita seguiresti con più interesse?').length)+'</strong></div></div></div>'+
'</section><aside class="stack"><div class="card"><h3>Ultima partita</h3>'+(last?'<span class="score">'+safe(last.m[0])+' '+safe(last.m[4])+' '+safe(last.m[3])+'</span><p>'+last.g.n+'ª giornata · Risultato ufficiale</p>':'<p>Nessun risultato disponibile.</p>')+'<a class="action2" href="#partita">Rivedi la partita ›</a></div>'+
annualMini()+'<div class="card"><h3>Le sezioni restano tutte</h3><p>Spogliatoio, Curva, Tabellone, Giornale, Radio, Carriera e Totogirrr non vengono sostituiti. Il centro notifiche ha una propria voce nel menu.</p><a class="action2" href="#notifiche">Vai alle notifiche ›</a></div></aside></div>'}
function notifications(){
var arr=notifs().filter(function(e){return S.notif==='tutte'||e.cat===S.notif}),push=previewPush();
return head('Notifiche intelligenti','Tutti gli aggiornamenti in un posto solo, con filtri, stato letto e collegamenti alle sezioni.')+
'<div class="layout"><section class="stack"><div class="card"><div class="between"><h3>Centro notifiche</h3><button class="action2" data-mark>Segna tutto come letto</button></div><div class="filters">'+[['tutte','Tutte'],['partita','Partite'],['classifica','Classifica'],['carriera','Carriera'],['giornale','Giornale'],['radio','Radio'],['curva','Curva']].map(function(o){return '<button data-filter="'+o[0]+'" class="'+(S.notif===o[0]?'on':'')+'">'+o[1]+'</button>'}).join('')+'</div><div class="events">'+arr.map(eventHtml).join('')+'</div></div>'+
'<div class="card"><h3>Preferenze</h3><p>Scegli cosa sarebbe importante ricevere anche fuori dal sito.</p>'+Object.keys(S.settings).map(function(x){return '<label class="setting"><input type="checkbox" data-setting="'+x+'" '+(S.settings[x]?'checked':'')+'><span>'+safe(SECTIONS[x])+'</span></label>'}).join('')+'</div></section>'+
'<aside class="stack"><div class="card"><h3>Come apparirebbe una notifica push</h3><div class="phone"><div class="clock">09:41</div><div class="date">Sabato · O Girrr</div><div class="pushcard"><small>O GIRRR · adesso</small><b>'+safe(push.title)+'</b><p>'+safe(push.body)+'</p></div></div><div class="between"><button class="action" data-push>Simula un’altra push</button><span class="tag">Anteprima</span></div><p class="tiny">La simulazione non richiede autorizzazioni e non invia notifiche al dispositivo.</p></div>'+
'<div class="card"><h3>Push: cosa serve</h3><div class="events"><div class="event"><span class="ic">📱</span><span><b>iPhone e iPad</b><p>App aggiunta alla schermata Home, iOS 16.4 o successivo e permesso richiesto dopo un tocco.</p></span></div><div class="event"><span class="ic">🔔</span><span><b>Invio vero</b><p>Service worker, Push API, abbonamento dispositivo e invio da server con consenso.</p></span></div></div><p class="tiny" id="compat">Compatibilità del dispositivo da verificare.</p></div></aside></div>'}
function previewPush(){var e=notifs().filter(function(x){return S.settings[x.cat]&&x.cat!=='giornale'&&x.cat!=='radio'&&x.cat!=='curva'});return e.length?e[S.push%e.length]:{title:'Girrr Sport',body:'La tua Lega ti aspetta.'}}
function choices(){var next=firstNext(),list=next?next.m:[],a=list.map(function(m){return m[0]+' – '+m[3]});return {n:next?next.n:0,a:a.length?a:['Il prossimo Derby','La corsa al titolo','La sfida per la salvezza']}}
function poll(){var c=choices(),key='poll-'+c.n,votes=read(key,{}),my=read(key+'-'+S.team,null),comments=read('comments-'+c.n,[]),bcom=botReplies('poll:'+c.n,'Quale partita del prossimo turno seguiresti con più interesse?'),total=Object.values(votes).reduce(function(s,x){return s+Number(x||0)},0);
return head('Il sondaggio della Lega','Una domanda per giornata. Si vota e si discute nello stesso posto.')+
'<div class="layout"><section class="stack"><div class="card"><span class="tag gold">Curva · '+(c.n?c.n+'ª giornata':'Prossimo turno')+'</span><p class="lead">Quale partita seguiresti con più interesse?</p><form id="voteForm"><div class="options">'+c.a.map(function(x,i){var v=Number(votes[i]||0),pct=total?Math.round(v/total*100):0;return '<label class="option"><input type="radio" name="voto" value="'+i+'" '+(my===i?'checked':'')+'><span>'+safe(x)+'</span><span class="pct">'+(total?pct+'%':'—')+'</span></label>'}).join('')+'</div><div class="between"><span class="tiny muted">'+total+' preferenze su questo dispositivo</span><button class="action" type="submit">Esprimi preferenza</button></div></form><p class="tiny">Il voto si può cambiare. Qui la prova rimane sul dispositivo; per condividerla con i dieci allenatori servirà il salvataggio nella Curva.</p></div>'+
'<div class="card"><h3>Commenti · '+(comments.length+bcom.length)+'</h3><div class="comments">'+(comments.length?comments.map(function(x){return '<div class="comment"><b>'+safe(x.team)+'</b><p>'+safe(x.body)+'</p></div>'}).join('') :'<p>Apri tu la discussione.</p>')+bcom.map(function(r){return '<div class="comment"><b>'+safe(BOT_NOMI[r.a]||r.a)+'</b><p>'+safe(r.x)+'</p></div>'}).join('')+'</div><form id="commentForm" class="addcomment"><input id="commentText" maxlength="280" required placeholder="Scrivi il tuo commento…" aria-label="Commenta il sondaggio"><button class="action" type="submit">Pubblica</button></form><p class="tiny">I tuoi commenti restano su questo dispositivo. Le risposte dei bot provengono dalla loro banca sperimentale; non sono pubblicate.</p></div></section><aside class="stack"><div class="card"><h3>Come funzionerebbe nella Curva</h3><p>Una sola scheda con domanda, preferenze e discussione. Ogni allenatore vota una volta e può cambiare idea. I commenti seguono le normali regole della Curva.</p><div class="event"><span class="ic">🔔</span><span><b>Notifica pertinente</b><p>La domanda della giornata e le risposte ricevute possono comparire nel centro notifiche.</p></span></div></div></aside></div>'}
function allMatches(){var a=[];games().slice().reverse().forEach(function(g){g.m.forEach(function(m,j){if(played(m,false))a.push({g:g,m:m,id:g.n+'-'+j})})});return a}
function lineups(t,sa){var day=F&&F[String(sa)],ro=day&&day[t];if(!ro)return '<p>La formazione della giornata non è disponibile.</p>';var ids=ro.tit||[],v=D.votes||{},P=D.P||{};
return '<table class="playertable"><thead><tr><th>Giocatore</th><th>Ruolo</th><th>Voto</th></tr></thead><tbody>'+ids.map(function(id){var p=P[id]||{},vote=v[id]&&v[id][String(sa)],score=vote&&Number.isFinite(Number(vote.f))?nfmt(vote.f):'—';return '<tr><td>'+safe(p.n||'Giocatore '+id)+'</td><td>'+safe(p.r||'—')+'</td><td>'+score+'</td></tr>'}).join('')+'</tbody></table><p class="tiny">Undici schierato nella nostra Lega per questa giornata, non la formazione titolare del club di Serie A.</p>'}
function matchCenter(){
var all=allMatches();if(!S.match&&all.length)S.match=all[0].id;var z=all.filter(function(x){return x.id===S.match})[0]||all[0],m=z&&z.m,sa=z&&z.g.sa;
return head('Centro partita','Il racconto post-partita della nostra Lega, con risultati e formazioni effettivamente schierate.')+
'<div class="layout"><section class="stack"><div class="card"><div class="between"><h3>Rivivi una partita</h3><span class="tag gold">Post-partita</span></div><label class="tiny">Scegli l’incontro<br><select id="matchSel" style="width:100%;margin-top:6px">'+all.slice(0,55).map(function(x){return '<option value="'+safe(x.id)+'" '+(z&&z.id===x.id?'selected':'')+'>'+x.g.n+'ª · '+safe(x.m[0])+' '+safe(x.m[4])+' '+safe(x.m[3])+'</option>'}).join('')+'</select></label>'+(m?'<div class="mini" style="margin-top:12px;text-align:center"><small>'+z.g.n+'ª giornata · Serie A '+sa+'</small><div class="score">'+safe(m[0])+' &nbsp;'+safe(m[4])+'&nbsp; '+safe(m[3])+'</div><p>'+nfmt(m[1])+' – '+nfmt(m[2])+' punti</p></div>':'<p>Non ci sono ancora incontri conclusi.</p>')+'</div>'+
(m?'<div class="card"><h3>Le formazioni della Lega</h3><div class="two"><section><h4>'+safe(m[0])+'</h4>'+lineups(m[0],sa)+'</section><section><h4>'+safe(m[3])+'</h4>'+lineups(m[3],sa)+'</section></div></div>':'')+
'</section><aside class="stack"><div class="card"><h3>Il racconto della sfida</h3><div class="events">'+(m?'<div class="event"><span class="ic">🏁</span><span><b>Risultato finale</b><p>'+safe(m[0])+' '+safe(m[4])+' '+safe(m[3])+'</p></span></div><div class="event"><span class="ic">🧑‍🏫</span><span><b>Scelte degli allenatori</b><p>Le formazioni sono quelle consegnate per la nostra giornata.</p></span></div>':'')+'<div class="event"><span class="ic">🎙️</span><span><b>Reazioni</b><p>Giornale, Radio, Moviola e conferenze completano il racconto dopo la partita.</p></span></div></div><div class="annmenu"><a href="'+ORIGIN+'girrr/curva.html" target="_blank" rel="noopener noreferrer">Vai alla Curva ›</a><a href="'+ORIGIN+'girrr/app.html#moviola" target="_blank" rel="noopener noreferrer">Moviola ›</a></div></div>'+
'<div class="card"><h3>E durante la giornata?</h3><p>Una scheda pre-partita può mostrare le formazioni depositate; un punteggio in diretta richiede aggiornamenti affidabili della fonte. Senza questi, non presentiamo aggiornamenti in tempo reale come ufficiali.</p><span class="tag">Priorità: post-partita</span></div></aside></div>'}
function cupRank(){var c=D.cal&&D.cal.cup||[],a={A:{},B:{}};c.forEach(function(g){(g.m||[]).forEach(function(m){var gr=m[0];if(!a[gr]||!played(m,true))return;var p=a[gr],x=p[m[1]]||(p[m[1]]={t:m[1],pt:0,fp:0}),y=p[m[4]]||(p[m[4]]={t:m[4],pt:0,fp:0}),r=String(m[5]).split('-').map(Number);x.fp+=Number(m[2])||0;y.fp+=Number(m[3])||0;x.pt+=r[0]>r[1]?3:r[0]===r[1]?1:0;y.pt+=r[1]>r[0]?3:r[0]===r[1]?1:0})});return Object.fromEntries(Object.entries(a).map(function(k){return [k[0],Object.values(k[1]).sort(function(x,y){return y.pt-x.pt||y.fp-x.fp})]}))}
function bracket(){
var ranks=cupRank(),groupsOver=(D.cal.cup||[]).slice(0,10).length===10&&(D.cal.cup||[]).slice(0,10).every(function(x){return x.m.every(function(m){return played(m,true)})});
function get(gr,i){return groupsOver&&ranks[gr]&&ranks[gr][i-1]?safe(ranks[gr][i-1].t):i+'° '+gr}
var quarti=[['A',1,'B',4],['B',2,'A',3],['B',1,'A',4],['A',2,'B',3]];
return '<div class="card"><div class="between"><h3>Champions Cup · Fase finale</h3><span class="tag">'+(groupsOver?'Accoppiamenti':'Qualificazioni in corso')+'</span></div><p>Quarti, semifinali e finale. Prima della chiusura dei gironi si vedono le posizioni previste dal regolamento, non qualificazioni ufficiali.</p><div class="bracket"><section><h4>Quarti · 11ª</h4>'+quarti.map(function(q){return '<div class="brmatch"><b>'+get(q[0],q[1])+'</b><b>'+get(q[2],q[3])+'</b></div>'}).join('')+'</section><section><h4>Semifinali · 12ª</h4><div class="brmatch"><b>Vincente quarto 1</b><b>Vincente quarto 2</b></div><div class="brmatch"><b>Vincente quarto 3</b><b>Vincente quarto 4</b></div></section><section><h4>Finale · 13ª</h4><div class="brmatch"><b>Vincente semifinale 1</b><b>Vincente semifinale 2</b><small>Il titolo si decide qui</small></div></section></div></div>'}
function compares(){var g=games(),max=g.length?g[g.length-1].n:1;if(!S.round2||S.round2>max)S.round2=max;if(S.round1>max)S.round1=Math.max(1,max-1);
var p=classifica(S.round1),q=classifica(S.round2);
return '<div class="card"><h3>Confronta due giornate</h3><p>Confronta classifica, punti e posizioni senza lasciare il Tabellone.</p><div class="controls"><label>Da giornata<select id="fromRound">'+g.map(function(x){return '<option value="'+x.n+'" '+(x.n===S.round1?'selected':'')+'>'+x.n+'ª</option>'}).join('')+'</select></label><label>A giornata<select id="toRound">'+g.map(function(x){return '<option value="'+x.n+'" '+(x.n===S.round2?'selected':'')+'>'+x.n+'ª</option>'}).join('')+'</select></label></div><table class="standtable"><thead><tr><th>#</th><th>Squadra</th><th>Pt</th><th>Δ</th></tr></thead><tbody>'+
q.map(function(x,i){var k=p.findIndex(function(y){return y.t===x.t}),dif=k-i;return '<tr><td>'+(i+1)+'</td><td>'+safe(x.t)+'</td><td>'+x.pt+'</td><td class="'+(dif>0?'diffup':dif<0?'diffdown':'')+'">'+(dif>0?'▲ '+dif:dif<0?'▼ '+Math.abs(dif):'—')+'</td></tr>'}).join('')+'</tbody></table><p class="tiny">La variazione confronta le posizioni delle due giornate selezionate; ▲ indica una risalita.</p></div>'}
function tableBoard(){
var day=lastDay(),next=firstNext(),cl=day?classifica(day.n):[],a=next&&next.m||[];
return head('Tabellone','Il Tabellone attuale resta identico: queste sono soltanto prove aggiuntive di confronto e fase finale.')+
'<div class="card" style="margin-bottom:12px"><div class="between"><div><h3>Il Tabellone completo non cambia</h3><p>La versione già preparata con forma, frecce, colori e tutti i dati rimane la vista principale.</p></div><a class="action" href="prova-tabellone-'+(document.body.dataset.skin==='stadio'?'stadio':'lega')+'.html">Apri il Tabellone completo ›</a></div></div>'+
'<div class="layout"><section class="stack"><div class="card"><div class="between"><h3>Classifica · Campionato</h3><span class="tag">'+(day?day.n+'ª giornata':'—')+'</span></div><table class="standtable"><thead><tr><th>#</th><th>Squadra</th><th>Pt</th><th>Δ</th></tr></thead><tbody>'+cl.map(function(x,i){var prev=day&&day.n>1?rankOf(day.n-1,x.t):i+1,dif=prev-(i+1);return '<tr><td>'+(i+1)+'</td><td>'+safe(x.t)+'</td><td>'+x.pt+'</td><td class="'+(dif>0?'diffup':dif<0?'diffdown':'')+'">'+(dif>0?'▲ '+dif:dif<0?'▼ '+Math.abs(dif):'—')+'</td></tr>'}).join('')+'</tbody></table></div>'+
'<div class="card"><div class="between"><h3>Prossimo turno</h3><span class="tag gold">'+(next?next.n+'ª giornata':'')+'</span></div><div class="matches">'+(a.length?a.map(function(m){return '<div class="match"><b>'+safe(m[0])+' – '+safe(m[3])+'</b><small>Partita in programma</small></div>'}).join(''):'<p>Calendario da completare.</p>')+'</div><p class="tiny">Questo riquadro va subito sotto la classifica, anche da telefono.</p></div>'+
compares()+'</section><aside class="stack">'+bracket()+'</aside></div>'}
function fullAnnual(){var d=lastDay(),cl=d?classifica(d.n):[],t=cl[0],m=lastMatch(S.team);return head('Annuario','Le sezioni espandibili si aggiungono alle informazioni dell’Albo esistente: nessun dato o tab viene eliminato.',false)+
'<div class="layout"><section class="stack"><div class="card"><span class="tag gold">2026/27 · Stagione in corso</span><p class="lead">La storia si scrive ogni giornata.</p>'+annualMini()+'<div class="line"></div><details open><summary><b>Classifica e podio</b></summary><p>'+(t?'Capolista provvisoria: '+safe(t.t)+'.':'Da definire.')+' Il campione sarà assegnato alla conclusione del torneo.</p></details><div class="line"></div><details><summary><b>Giocatori e rose</b></summary><p>Prezzi, valore delle rose e capocannoniere vengono dai dati della stagione.</p></details><div class="line"></div><details><summary><b>Record e serie</b></summary><p>Massimi e minimi di giornata, vittoria più larga e sequenze di successi: tutti calcolati dai risultati conservati.</p></details><div class="line"></div><details><summary><b>Champions Cup</b></summary><p>Gironi, quarti, semifinali e finale; il percorso completo a eliminazione diretta apparirà a stagione conclusa.</p></details></div></section>'+
'<aside class="stack"><div class="card"><h3>Le stagioni passate</h3><p>Per gli anni precedenti riportiamo soltanto i risultati e i protagonisti già archiviati. Dove mancano informazioni, compare «Dato non conservato».</p><span class="tag">Nessuna ricostruzione arbitraria</span></div><div class="card"><h3>Archivio finale Leghe FC</h3><p>Il 2026/27 si aggiorna durante il campionato. A fine stagione i dati esportati da Leghe FC possono essere salvati come fotografia storica verificata, senza modificare i risultati precedenti.</p></div></aside></div>'}
function render(){
nav();if(!D){$('content').innerHTML='<div class="card">'+(loading?'Carico calendario e squadre…':safe(error||'Dati non disponibili'))+'</div>';return}
$('content').innerHTML=({home:home,notifiche:notifications,sondaggio:poll,curva:curvaViva,partita:matchCenter,tabellone:tableBoard,annuario:fullAnnual}[S.tab]||home)();
var compat=$('compat');if(compat){var sw='serviceWorker' in navigator,push='PushManager' in window,perm=('Notification' in window)?Notification.permission:'non disponibile';compat.textContent='Controllo dispositivo: Service worker '+(sw?'disponibile':'non disponibile')+', Push API '+(push?'disponibile':'non disponibile')+', permesso '+perm+'.'}
}
function route(t){if(!NAV.some(function(x){return x[0]===t}))t='home';S.tab=t;location.hash=t;render();window.scrollTo({top:0,behavior:'instant'})}
document.addEventListener('click',function(e){
var nav=e.target.closest('[data-nav]');if(nav){route(nav.getAttribute('data-nav'));return}
var mk=e.target.closest('[data-mark]');if(mk){save(snapshotKey(S.team),snapshot(S.team));render();return}
var fl=e.target.closest('[data-filter]');if(fl){S.notif=fl.dataset.filter;render();return}
var pu=e.target.closest('[data-push]');if(pu){S.push++;render();return}
var local=e.target.closest('a[href^="#"]');if(local){var h=local.getAttribute('href').slice(1);if(NAV.some(function(z){return z[0]===h})){e.preventDefault();route(h)}}
});
document.addEventListener('change',function(e){var z=e.target;
if(z.id==='teamSelect'){S.team=z.value;save('team',S.team);render()}
if(z.id==='matchSel'){S.match=z.value;render()}
if(z.id==='fromRound'){S.round1=Number(z.value);render()}
if(z.id==='toRound'){S.round2=Number(z.value);render()}
if(z.dataset.setting){S.settings[z.dataset.setting]=z.checked;save('settings',S.settings);render()}
});
document.addEventListener('submit',function(e){
if(e.target.id==='voteForm'){e.preventDefault();var sel=e.target.querySelector('input[name="voto"]:checked');if(!sel)return;var c=choices(),key='poll-'+c.n,i=Number(sel.value),old=read(key+'-'+S.team,null),votes=read(key,{});if(old!==null)votes[old]=Math.max(0,(votes[old]||0)-1);votes[i]=(votes[i]||0)+1;save(key,votes);save(key+'-'+S.team,i);render()}
if(e.target.id==='commentForm'){e.preventDefault();var text=$('commentText').value.trim();if(!text)return;var c=choices(),key='comments-'+c.n,comments=read(key,[]);comments.push({team:S.team,body:text.slice(0,280)});save(key,comments);render()}
});
window.addEventListener('hashchange',function(){var t=location.hash.slice(1);if(NAV.some(function(z){return z[0]===t})&&S.tab!==t){S.tab=t;render()}});
S.team=read('team',S.team);S.settings=read('settings',S.settings);
render();
Promise.all([
fetch(ORIGIN+'data.json',{cache:'no-store'}).then(function(r){if(!r.ok)throw Error('Calendario non disponibile');return r.json()}),
fetch(ORIGIN+'formazioni.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null}),
fetch(ORIGIN+'girrr/dati/lab-dati.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null})
]).then(function(x){D=x[0];F=x[1];L=x[2];if(squadre().indexOf(S.team)<0)S.team=squadre()[0]||'';loading=false;render()}).catch(function(e){loading=false;error='Il caricamento dei dati della Lega non è riuscito. Riprova quando la connessione è disponibile.';render()});
})();
