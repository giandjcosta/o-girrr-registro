/* ===== 5.0 · dati veri e database =====
   Questo blocco va dentro la pagina delle novità (Girrr Sport, Spogliatoio, Totogirrr, Carriera), in fondo, dopo le funzioni del Laboratorio:
   le ridefinisce con la versione collegata. Modo "prova": un finto database nel browser (localStorage), per provare tutto senza toccare niente.
   Modo "reale": le funzioni vere del database (derby_*, conf_salva). */
var LV={mode:'@@MODE@@',url:'https://qmjqfgmvimsuxvghetgi.supabase.co',key:'sb_publishable_qPhimkrF4iUvIad7JPoH8A_i-eOqG7n',stag:'2026/27'};
var DBS={ok:false,sfide:[],voti:[],miei:[],conf:[]},DBN=0,DBSIG='';
S.mine={};S.veto={};S.sfnew=false;S.lerr='';S.cfok=false;

/* ---------- finto database (solo modo prova) ---------- */
var MOCK=(function(){
  var K='orr_mock5';
  function ld(){try{var m=JSON.parse(localStorage.getItem(K));if(m&&m.sfide)return ensure(m)}catch(e){}return ensure({n:0,sfide:[],voti:[],conf:[]})}
  function ensure(m){if(!m.cr){m.cr={};D.teams.forEach(function(t){m.cr[t]=300});m.cr['Real Madrink']=500;m.cr['Atletico ma non troppo']=120}if(!m.du)m.du=[];if(!m.dn)m.dn=0;return m}
  function sv(m){try{localStorage.setItem(K,JSON.stringify(m))}catch(e){}}
  function err(t){throw new Error(t)}
  function nm(x){x=(x==null?'':String(x)).replace(/^\s+|\s+$/g,'');return x||null}
  function okn(x){if(x!==null&&(x.length<3||x.length>40))err('Il nome deve avere da 3 a 40 caratteri')}
  function find(m,id){for(var i=0;i<m.sfide.length;i++)if(m.sfide[i].id===id)return m.sfide[i];return null}
  var F={
    derby_stato:function(b,m){
      var ok=!!b.p_team;
      var agg={};m.voti.forEach(function(v){var k=v.a+'|'+v.b;agg[k]=agg[k]||{a:v.a,b:v.b,si:0,no:0};if(v.si)agg[k].si++;else agg[k].no++});
      return {ok:ok,sfide:m.sfide.slice().sort(function(x,y){return y.ts-x.ts}).slice(0,60),voti:Object.keys(agg).map(function(k){return agg[k]}),
        miei:ok?m.voti.filter(function(v){return v.team===b.p_team}).map(function(v){return {a:v.a,b:v.b,si:v.si}}):[],
        conf:ok?m.conf.filter(function(c){return c.team===b.p_team}).sort(function(x,y){return x.giornata-y.giornata}):[]}},
    derby_sfida_lancia:function(b,m){
      var T=b.p_team,R=b.p_rival,n=nm(b.p_nome);
      if(R===T)err('Non puoi sfidare te stesso');if(D.teams.indexOf(R)<0)err('Squadra non valida');
      if(!(b.p_frase>=0&&b.p_frase<=2))err('Frase non valida');okn(n);
      if(m.sfide.some(function(s){return s.da===T&&s.stato==='attesa'}))err('Hai già una sfida in attesa');
      if(m.sfide.some(function(s){return ((s.da===T&&s.a===R)||(s.da===R&&s.a===T))&&s.stato==='accettata'&&s.nome_ok}))err('È già un Derby');
      if(m.sfide.filter(function(s){return s.da===T&&s.stagione===(b.p_stagione||LV.stag)}).length>=2)err('Hai usato le due sfide di questa stagione');
      var s={id:++m.n,stagione:b.p_stagione||LV.stag,da:T,a:R,frase:b.p_frase,nome:n,nome_da:n?T:null,nome_ok:false,stato:'attesa',ts:Date.now(),risp:null};
      m.sfide.push(s);return s.id},
    derby_sfida_rispondi:function(b,m){
      var s=find(m,b.p_id),n=nm(b.p_nome);
      if(!s||s.a!==b.p_team||s.stato!=='attesa')err('Nessuna sfida da rispondere');
      if(b.p_azione==='accetta'){okn(n);s.stato='accettata';s.risp=Date.now();s.nome_ok=false;if(n){s.nome=n;s.nome_da=b.p_team}}
      else if(b.p_azione==='rifiuta'){s.stato='rifiutata';s.risp=Date.now()}
      else err('Azione non valida')},
    derby_nome_proponi:function(b,m){
      var s=find(m,b.p_id),n=nm(b.p_nome)||'';if(n.length<3||n.length>40)err('Il nome deve avere da 3 a 40 caratteri');
      if(!s||s.stato!=='accettata'||s.nome_ok||(s.da!==b.p_team&&s.a!==b.p_team))err('Sfida non trovata o nome già concordato');
      if(s.nome_da===b.p_team)err('Hai già proposto un nome: aspetta la risposta');
      s.nome=n;s.nome_da=b.p_team},
    derby_nome_accetta:function(b,m){
      var s=find(m,b.p_id);
      if(!s||s.stato!=='accettata'||s.nome_ok||(s.da!==b.p_team&&s.a!==b.p_team))err('Sfida non trovata o nome già concordato');
      if(!s.nome)err('Nessun nome da accettare');if(s.nome_da===b.p_team)err("Il nome lo hai proposto tu: deve accettarlo l'altra squadra");
      s.nome_ok=true},
    derby_vota:function(b,m){
      var x=b.p_a<b.p_b?b.p_a:b.p_b,y=b.p_a<b.p_b?b.p_b:b.p_a;
      if(b.p_a===b.p_b)err('Coppia non valida');
      var v=m.voti.filter(function(z){return z.a===x&&z.b===y&&z.team===b.p_team})[0];
      if(v)v.si=!!b.p_si;else m.voti.push({a:x,b:y,team:b.p_team,si:!!b.p_si})},
    conf_salva:function(b,m){
      var c=m.conf.filter(function(z){return z.team===b.p_team&&z.giornata===b.p_giornata})[0];
      if(c&&c.esito)err('Conferenza già chiusa');
      if(b.p_libera&&b.p_libera.length>80)err('La risposta libera può avere al massimo 80 caratteri');
      if(b.p_promessa&&b.p_promessa.length>80)err('La promessa può avere al massimo 80 caratteri');
      var r={team:b.p_team,giornata:b.p_giornata,risposte:b.p_risposte,libera:b.p_libera||null,promessa:b.p_promessa||null,pesa:Math.max(0,Math.min(3,b.p_pesa==null?1:b.p_pesa)),esito:c?c.esito:null};
      if(c)m.conf[m.conf.indexOf(c)]=r;else m.conf.push(r)}
    ,duello_stato:function(b,m){var G=D.cal[0]&&D.cal[0].n;return {ok:!!b.p_team,prossima:G,inizio:null,crediti:m.cr,duelli:m.du.slice().sort(function(x,y){return y.id-x.id}).slice(0,60)}},
    duello_lancia:function(b,m){var T=b.p_team,R=b.p_rival,P=b.p_posta,G=D.cal[0].n;
      if(R===T)err('Non puoi sfidare te stesso');if(m.cr[R]==null)err('Quella squadra non ha ancora un conto Totogirrr');
      if(P!==Math.round(P)||P<10)err('Posta minima: 10 fantacrediti');if(P>200)err('Posta massima: 200 fantacrediti');
      if(P>m.cr[T])err('Non hai abbastanza fantacrediti');if(P>m.cr[R])err('Il tuo avversario ha solo '+m.cr[R]+' fantacrediti: abbassa la posta');
      if(m.du.some(function(d){return d.giornata===G&&(d.stato==='attesa'||d.stato==='accettato')&&((d.da===T&&d.a===R)||(d.da===R&&d.a===T))}))err("C'è già una sfida tra voi due per questa giornata");
      if(m.du.filter(function(d){return d.da===T&&d.giornata===G&&(d.stato==='attesa'||d.stato==='accettato')}).length>=3)err('Hai già tre sfide per questa giornata');
      m.cr[T]-=P;var d={id:++m.dn,giornata:G,da:T,a:R,posta:P,stato:'attesa',ts:Date.now(),pa:null,pb:null,vincitore:null};m.du.push(d);return {id:d.id,giornata:G}},
    duello_rispondi:function(b,m){var d=m.du.filter(function(x){return x.id===b.p_id})[0];
      if(!d||d.a!==b.p_team||d.stato!=='attesa')err('Nessuna sfida a cui rispondere');
      if(b.p_azione==='rifiuta'){m.cr[d.da]+=d.posta;d.stato='rifiutato'}
      else if(b.p_azione==='accetta'){if(m.cr[d.a]<d.posta)err('Non hai abbastanza fantacrediti per accettare (servono '+d.posta+')');m.cr[d.a]-=d.posta;d.stato='accettato'}
      else err('Azione non valida')},
    duello_chiudi_prova:function(b,m){var G=D.cal[0].n;m.du.forEach(function(d){if(d.stato!=='accettato'||d.giornata!==G)return;var x=Math.round(Math.random()*400+500)/10,y=Math.round(Math.random()*400+500)/10;d.pa=x;d.pb=y;d.stato='chiuso';
        if(x>y){m.cr[d.da]+=2*d.posta;d.vincitore=d.da}else if(y>x){m.cr[d.a]+=2*d.posta;d.vincitore=d.a}else{m.cr[d.da]+=d.posta;m.cr[d.a]+=d.posta}})}
  };
  return {
    rpc:function(n,b){var m=ld(),now=Date.now();m.sfide.forEach(function(s){if(s.stato==='attesa'&&now-s.ts>72*3600000){s.stato='scaduta';s.risp=now}});
      if(!F[n])err('Funzione non trovata');var r=F[n](b,m);sv(m);return JSON.parse(JSON.stringify(r===undefined?null:r))},
    avanza:function(){var m=ld();m.sfide.forEach(function(s){if(s.stato==='attesa')s.ts-=73*3600000});m.du.forEach(function(d){if(d.stato==='attesa'){d.stato='scaduto';m.cr[d.da]+=d.posta}});sv(m)},
    chiudiDuelli:function(){var m=ld();F.duello_chiudi_prova({},m);sv(m)},
    esito:function(team,g,e){var m=ld();m.conf.forEach(function(c){if(c.team===team&&c.giornata===g)c.esito=e});sv(m)},
    azzera:function(){try{localStorage.removeItem(K)}catch(e){}},
    rpcRaw:function(n,b){return this.rpc(n,b)}
  };
})();

function dbRpc(name,body){
  if(LV.mode==='prova')return Promise.resolve().then(function(){return MOCK.rpc(name,body)});
  return fetch(LV.url+'/rest/v1/rpc/'+name,{method:'POST',headers:{apikey:LV.key,Authorization:'Bearer '+LV.key,'Content-Type':'application/json'},body:JSON.stringify(body)})
    .then(function(r){return r.text().then(function(x){var j=null;try{j=x?JSON.parse(x):null}catch(e){}if(!r.ok)throw new Error(j&&j.message?j.message:'Errore di rete');return j})});
}
function lvToast(t){var d=document.createElement('div');d.textContent=t;d.setAttribute('role','status');d.style.cssText='position:fixed;left:50%;bottom:22px;transform:translateX(-50%);max-width:88vw;background:#ffd166;color:#1d2a52;font-weight:800;padding:11px 18px;border-radius:14px;z-index:99999;box-shadow:0 8px 24px rgba(0,0,0,.35);text-align:center';document.body.appendChild(d);setTimeout(function(){d.remove()},3600)}

/* ---------- stato dal database ---------- */
function dbApply(){
  S.vote={};S.pend={};S.dn={};S.veto={};S.mine={};
  DBS.voti.forEach(function(v){var k=rvKey(v.a,v.b);if(v.si>v.no)S.vote[k]=true;else if(v.no>v.si)S.veto[k]=true});
  DBS.miei.forEach(function(v){S.mine[rvKey(v.a,v.b)]=!!v.si});
  DBS.sfide.slice().reverse().forEach(function(s){var k=rvKey(s.da,s.a);
    if(s.stato==='accettata'&&s.nome_ok){S.vote[k]=true;S.dn[k]=s.nome;delete S.veto[k]}else S.pend[k]=true});
  /* conferenza della prossima giornata già pubblicata: la ricarico solo la prima volta, poi le modifiche sono quelle dell'utente */
  var G=D.cal[0]&&D.cal[0].n,row=DBS.conf.filter(function(c){return c.giornata===G})[0];
  if(row&&!S.cfok&&Array.isArray(row.risposte)){S.cfok=true;S.cf.a=[];S.cf.free=['','',''];row.risposte.forEach(function(r,i){S.cf.a[i]=r.a==='free'?'free':r.a;if(r.a==='free')S.cf.free[i]=r.t||''});S.cf.pub=true}
}
var LVTRY=0,LVBUSY=false,LVTIM=null;
function dbLoad(quiet){
  if(LVBUSY)return Promise.resolve();LVBUSY=true;
  return dbRpc('derby_stato',{p_team:ME,p_code:CODE}).then(function(r){
    if(!r||!r.sfide)throw new Error('stato');
    LVTRY=0;clearTimeout(LVTIM);
    var sig=JSON.stringify(r),era=DBN;
    if(r.ok===false){DBS=r;DBN=-2;dbApply();if(era!==-2)render();return}   /* il database non riconosce il codice di questa squadra */
    if(quiet&&sig===DBSIG&&DBN===1)return;
    DBSIG=sig;DBS=r;DBN=1;dbApply();
    var a=document.activeElement;if(quiet&&a&&/INPUT|TEXTAREA/.test(a.tagName))return;render()
  }).catch(function(){var era=DBN;DBN=-1;if(era!==-1&&!quiet)render();
    /* riprovo da solo, con attese sempre più lunghe (2, 4, 8, 15 secondi, poi ogni 30) finché non risponde */
    var d=[2000,4000,8000,15000,30000][Math.min(LVTRY,4)];LVTRY++;clearTimeout(LVTIM);LVTIM=setTimeout(function(){dbLoad(true)},d);
  }).then(function(){LVBUSY=false},function(){LVBUSY=false});
}
function lvCall(nome,body,ok){
  return dbRpc(nome,body).then(function(){if(ok)lvToast(ok);return dbLoad(false)}).catch(function(e){lvToast(e.message||'Qualcosa non ha funzionato');dbLoad(true)});
}
if(!GUEST){dbLoad(false);setInterval(function(){if(!document.hidden)dbLoad(true)},45000);document.addEventListener('visibilitychange',function(){if(!document.hidden)dbLoad(true)});
  if(LV.mode==='prova')window.addEventListener('storage',function(e){if(e.key==='orr_mock5')dbLoad(true)})}

/* ---------- Sfide ---------- */
function mshort(t){var m=mg(t),w=m.split(/[ &]/)[0];return m.indexOf('&')>=0?m.replace(' & ',' e '):w.charAt(0).toUpperCase()+w.slice(1)}
function lvLeft(ts){var ms=ts+72*3600000-Date.now();if(ms<=0)return null;var h=Math.floor(ms/3600000),d=Math.floor(h/24),o=h%24;return d>0?d+(d===1?' giorno':' giorni')+' e '+o+(o===1?' ora':' ore'):(h>0?h+(h===1?' ora':' ore')+' e '+Math.floor(ms%3600000/60000)+' minuti':Math.max(1,Math.floor(ms/60000))+' minuti')}
function gsPost(testo,quando){return '<div class="post" style="margin-top:8px"><div class="hd"><img src="'+D.img.gs+'" alt="Girrr Sport"><div><b>Girrr Sport</b><span class="mut sm">@girrrsport · '+(quando||'Adesso')+'</span></div></div><q>'+testo+'</q></div>'}
function lvTesto(s){var f=sfF(s.a,s.da);return (f[s.frase]||f[0]).replace('{X}',mshort(s.a))}
function lvAltro(s){return s.da===ME?s.a:s.da}
function lvAttive(){return DBS.sfide.filter(function(s){return s.stato==='attesa'||(s.stato==='accettata'&&!s.nome_ok)})}
function rxList(){return DBS.sfide.filter(function(s){return s.a===ME})}
function rxCount(){return rxList().filter(function(s){return (s.stato==='attesa'&&lvLeft(s.ts)!==null)||(s.stato==='accettata'&&!s.nome_ok&&s.nome&&s.nome_da!==ME)}).length}
function lvStato(){if(DBN===-2)return '<p class="sm" style="color:var(--bad)">Il sito non riconosce il codice della tua squadra. Esci e rientra con il tuo codice dalla pagina principale.</p>';return DBN===0?'<p class="sm mut">Carico le sfide…</p>':(DBN<0?'<p class="sm" style="color:var(--bad)">Non riesco a collegarmi in questo momento: riprovo da solo.</p>':'')}

function nomeFlow2(s){
  var rv=SFR[lvAltro(s)][0],id=s.id,h='',k=rvKey(s.da,s.a);
  if(s.nome&&s.nome_da!==ME)
    return '<p style="margin-top:6px"><b>'+esc(rv)+' propone «'+esc(s.nome)+'».</b> Accetti, o scrivi il tuo.</p><div class="row" style="gap:6px;flex-wrap:wrap;margin-top:6px"><button class="btn" data-lnome="ok" data-id="'+id+'">Accetto</button></div><div class="row" style="gap:6px;flex-wrap:wrap;margin-top:6px"><input class="nmin" maxlength="40" placeholder="Scrivo la mia proposta" style="flex:1;min-width:140px"><button class="btn" data-lnome="prop" data-id="'+id+'">Proponi il mio</button></div>';
  if(s.nome)
    return '<p style="margin-top:6px"><b>Hai proposto «'+esc(s.nome)+'».</b> Aspettiamo la risposta di '+esc(rv)+': può accettarlo o scriverne un altro.</p>';
  var sug=DNP[lvAltro(s)];
  return '<p style="margin-top:6px"><b>Scegli il nome del Derby.</b> '+esc(rv)+' potrà accettarlo o proporne un altro.</p><div class="row" style="gap:6px;flex-wrap:wrap;margin-top:6px"><button class="btn" data-lnome="prop" data-id="'+id+'" data-v="'+esc(sug)+'">'+esc(sug)+'</button></div><div class="row" style="gap:6px;flex-wrap:wrap;margin-top:6px"><input class="nmin" maxlength="40" placeholder="Oppure scrivi il tuo" style="flex:1;min-width:140px"><button class="btn o" data-lnome="prop" data-id="'+id+'">Proponi</button></div>';
}
function lvFatto(s){
  var k=rvKey(s.da,s.a);
  return '<p class="sm" style="margin-top:6px">Nome concordato: <b>'+esc(s.nome)+'</b></p>'+gsPost('<b>NASCE UN DERBY</b><br>'+esc(s.da)+' e '+esc(s.a)+' hanno trovato l\'accordo: da oggi è «'+esc(s.nome)+'». #GirrrSport #Derby')+'<p class="sm mut" style="margin-top:6px">Il Derby è ufficiale: compare tra i Derby della lega con la sua prima storia, e la rivalità tra le due squadre sale. Dura per sempre: se una delle due lascia la lega resta nell\'albo come Derby della storia.</p>';
}
function lvChiusa(s,mia){
  var altro=lvAltro(s),h='';
  if(s.stato==='rifiutata')h+='<p style="margin-top:8px"><b>'+(mia?esc(altro)+' ha rifiutato apertamente.':'Hai rifiutato la sfida di '+esc(SFR[altro][0])+'.')+'</b></p>'+gsPost('<b>RIFIUTO CLAMOROSO</b><br>'+esc(s.a)+' non considera '+esc(s.da)+' nemmeno degno di un Derby. La rivalità, intanto, sale. #GirrrSport')+'<p class="sm mut" style="margin-top:6px">Niente Derby, ma la rivalità resta un po\' più alta di prima.</p>';
  if(s.stato==='scaduta')h+='<p style="margin-top:8px"><b>'+(mia?'Nessuna risposta in tre giorni: la sfida decade.':'Tre giorni senza risposta: la sfida decade.')+'</b></p><p class="sm mut">Niente Derby, ma la rivalità resta un po\' più alta di prima.</p>';
  if(s.stato==='accettata'&&s.nome_ok)h+='<p style="margin-top:8px"><b>'+(mia?esc(altro)+' ha accettato la sfida.':'Hai accettato la sfida di '+esc(SFR[altro][0])+'.')+'</b></p>'+lvFatto(s);
  return h}

function sfidaCard(){
  var mine=DBS.sfide.filter(function(s){return s.da===ME}),usate=mine.filter(function(s){return s.stagione===LV.stag}).length,L=S.lancio;
  var h='<div class="card"><h3>Lancia una sfida</h3><p class="sm mut" style="margin-bottom:8px">Una dichiarazione in conferenza stampa fa salire la rivalità, ma il Derby diventa ufficiale solo se il rivale accetta. Una sfida alla volta, e al massimo due all\'anno per squadra.</p>'+lvStato();
  var act=mine.filter(function(s){return s.stato==='attesa'||(s.stato==='accettata'&&!s.nome_ok)})[0],last=mine[0];
  function postMio(s){return '<div class="post"><div class="hd">'+av(ME)+'<div><b>'+esc(ME)+'</b><span class="mut sm">In conferenza stampa</span></div></div><q>«'+esc(lvTesto(s))+'»</q></div>'+gsPost('<b>SFIDA LANCIATA</b><br>'+esc(s.da)+' contro '+esc(s.a)+': la dichiarazione fa rumore in lega. Sta per nascere un nuovo Derby? #GirrrSport #Derby','Esce in Curva al prossimo aggiornamento')}
  if(act){
    h+=postMio(act);
    if(act.stato==='attesa'){var lf=lvLeft(act.ts);h+='<p class="sm mut" style="margin-top:8px">La rivalità è già salita. '+esc(act.a)+' ha ancora '+(lf||'pochissimo tempo')+' per rispondere: accetta, rifiuta o lascia cadere la sfida.</p>'}
    else h+='<p style="margin-top:8px"><b>'+esc(act.a)+' ha accettato la sfida.</b> Ora serve il nome del Derby.</p>'+nomeFlow2(act);
    return h+'</div>'}
  if(last&&!S.sfnew){
    h+=postMio(last)+lvChiusa(last,true);
    h+=usate<2?'<button class="btn" data-lnew="1" style="margin-top:8px">Lancia un\'altra sfida</button>':'<p class="sm mut" style="margin-top:8px">Hai usato le due sfide di quest\'anno: le prossime dalla stagione nuova.</p>';
    return h+'</div>'}
  var OR=sfOrdine();if(!SFR[L.r]||sfInfo(L.r).der){var pr=OR.filter(function(z){return !z.der})[0];if(pr)L.r=pr.t}
  if(!OR.some(function(z){return !z.der}))return h+'<p class="sm mut">Con tutte le squadre sei già in un Derby: niente da sfidare.</p></div>';
  var x=SFR[L.r][1];
  h+='<div class="rvl" role="group" aria-label="Rivale">'+OR.map(function(z){return '<button data-lr="'+esc(z.t)+'" aria-pressed="'+(L.r===z.t)+'"'+(z.der?' disabled':'')+'><b>'+esc(SFR[z.t][0])+'</b><small>'+esc(z.t)+' · Rivalità '+rvWord(z.riv)+'</small>'+(z.der?'<em class="gia">Già un Derby</em>':(z.cons?'<em>Consigliato</em>':''))+'</button>'}).join('')+'</div>';
  h+='<div class="frs" role="group" aria-label="Frase">'+sfF(L.r).map(function(f,i){return '<button data-lf="'+i+'" aria-pressed="'+(L.f===i)+'">'+esc(f.replace('{X}',x))+'</button>'}).join('')+'</div>';
  h+='<button class="btn" data-lgo="1" style="margin-top:10px"'+(usate>=2||DBN!==1?' disabled style="opacity:.45;margin-top:10px"':'')+'>Lancia la sfida</button><p class="sm mut" style="margin-top:6px">'+(usate>=2?'Hai usato le due sfide di quest\'anno: le prossime dalla stagione nuova.':'Sfide usate quest\'anno: '+usate+' su 2.')+'</p>';
  return h+'</div>'}

function rxCard(){
  var L=rxList(),h='<div class="card"><h3>Sfide ricevute</h3>'+lvStato();
  if(!L.length)return h+(DBN===1?'<p class="sm mut">Nessuno ti ha sfidato. Quando succede compare qui.</p>':'')+'</div>';
  L.slice(0,5).forEach(function(s,i){var t=s.da;
    h+=(i?'<div style="border-top:1px solid var(--line);margin-top:14px;padding-top:6px"></div>':'')+'<div class="post"><div class="hd">'+av(t)+'<div><b>'+esc(SFR[t][0])+'</b><span class="mut sm">In conferenza stampa · '+esc(t)+'</span></div></div><q>«'+esc(lvTesto(s))+'»</q></div>';
    if(s.stato==='attesa'){var lf=lvLeft(s.ts);
      h+='<p style="margin-top:8px"><b>'+esc(SFR[t][0])+' ti ha lanciato una sfida: vuole un Derby con te.</b></p><p class="sm mut" style="margin-top:4px">Tempo per rispondere: <b>'+(lf||'scaduto')+'</b>. Se lasci passare i tre giorni la sfida decade e la rivalità resta un po\' più alta.</p><div class="row" style="gap:6px;flex-wrap:wrap;margin-top:8px"><button class="btn" data-lrx="accetta" data-id="'+s.id+'">Accetto la sfida</button><button class="btn o" data-lrx="rifiuta" data-id="'+s.id+'">Rifiuto</button></div><p class="sm mut" style="margin-top:6px">Se non rispondi, la sfida resta in attesa fino alla scadenza.</p>'}
    else if(s.stato==='accettata'&&!s.nome_ok)h+='<p style="margin-top:8px"><b>Hai accettato la sfida di '+esc(SFR[t][0])+'.</b> Ora si sceglie il nome del Derby.</p>'+nomeFlow2(s);
    else h+=lvChiusa(s,false)});
  return h+'</div>'}

function sfidaHub(){var n=rxCount();
  var h='<div class="seg" role="group" aria-label="Sfide">'+[['lancia','Lancia'],['rx','Ricevute'+(n?' ('+n+')':'')]].map(function(x){return '<button data-lt="'+x[0]+'" aria-pressed="'+(S.sft===x[0])+'">'+x[1]+'</button>'}).join('')+'</div>'+(S.sft==='rx'?rxCard():sfidaCard());
  if(LV.mode==='prova'){var altri={};DBS.sfide.forEach(function(s){if(s.da===ME)altri[s.a]=1;if(s.a===ME)altri[s.da]=1});
    h+='<div class="lvprova" style="margin-top:14px;padding:12px;border:1px dashed rgba(255,209,102,.6);border-radius:14px"><b style="color:#ffd166">Strumenti di prova</b><p class="sm mut" style="margin:8px 0">Qui il database è finto e vive solo in questo browser: puoi provare tutto senza disturbare nessuno. Per rispondere come un altro allenatore apri la stessa pagina con il suo nome.</p><div class="row" style="gap:6px;flex-wrap:wrap">'
      +Object.keys(altri).map(function(t){return '<a class="btn o" target="_blank" rel="noopener" href="?come='+encodeURIComponent(t)+(location.hash||'#sport')+'">Apri come '+esc(t)+'</a>'}).join('')
      +'<button class="btn o" data-lprova="avanza">Passano 3 giorni</button><button class="btn o" data-lprova="azzera">Azzera la prova</button></div></div>'}
  return h}
function vSfideDerby(){if(GUEST)return where('Girrr Sport','Sfide')+'<h2>Sfide</h2>'+lvGate('Le sfide');return where('Girrr Sport','Sfide')+'<h2>Sfide</h2><p class="lead">Sfida un rivale in conferenza stampa: la rivalità sale subito e, se lui accetta, nasce un Derby ufficiale.</p>'+sfidaHub()}


/* ---------- Sfida 1 contro 1 (fantacrediti veri di Totogirrr) ---------- */
var DU={ok:null,prossima:null,crediti:{},duelli:[]},DUBUSY=false;
function duLoad(quiet){
  if(GUEST||DUBUSY)return Promise.resolve();DUBUSY=true;
  return dbRpc('duello_stato',{p_team:ME,p_code:CODE}).then(function(r){
    if(!r)throw new Error('x');var sig=JSON.stringify(r),era=JSON.stringify(DU);DU=r;
    if(sig!==era){var a=document.activeElement;if(!(quiet&&a&&/INPUT|SELECT/.test(a.tagName)))render()}
  }).catch(function(){}).then(function(){DUBUSY=false},function(){DUBUSY=false});
}
function duCall(nome,body,ok){return dbRpc(nome,body).then(function(){if(ok)lvToast(ok);return duLoad(false)}).catch(function(e){lvToast(e.message||'Qualcosa non ha funzionato');duLoad(false)})}
if(!GUEST){duLoad(false);setInterval(function(){if(!document.hidden)duLoad(true)},45000);document.addEventListener('visibilitychange',function(){if(!document.hidden)duLoad(true)});
  if(LV.mode==='prova')window.addEventListener('storage',function(e){if(e.key==='orr_mock5')duLoad(true)})}
function duCap(o){var c=DU.crediti||{};return Math.max(0,Math.min(200,c[ME]||0,c[o]==null?0:c[o]))}
function vSfide(){
  var h=where('Totogirrr','Sfida 1 contro 1')+'<h2>Sfida 1 contro 1</h2>';
  if(GUEST)return h+lvGate('Le sfide 1 contro 1');
  h+='<p class="lead">Sfida un\'altra squadra con i tuoi fantacrediti di Totogirrr: nella prossima giornata <b>vince chi fa più punti</b> e prende la posta dell\'altro. In caso di pareggio ognuno si riprende i suoi. Puoi puntare al massimo 200 e mai più di quello che hanno tu e l\'avversario.</p>';
  if(DU.ok===null)return h+'<div class="card"><p class="sm mut">Carico i tuoi fantacrediti…</p></div>';
  if(DU.ok===false)return h+'<div class="card"><p class="sm">Non riesco a verificare il tuo conto Totogirrr. Controlla di aver fatto l\'accesso con il codice della tua squadra.</p></div>';
  var cr=DU.crediti||{},mio=cr[ME],G=DU.prossima;
  var opp=D.teams.filter(function(t){return t!==ME&&cr[t]!=null});
  if(mio==null)return h+'<div class="card"><p class="sm">La tua squadra non ha ancora un conto Totogirrr, quindi non può lanciare sfide. Apri Totogirrr per attivarlo.</p></div>';
  if(!S.opp||opp.indexOf(S.opp)<0)S.opp=opp[0];
  var mx=duCap(S.opp);if(!S.stake||S.stake>mx)S.stake=Math.min(mx,S.stake||50);if(mx>=10&&S.stake<10)S.stake=10;
  var att=DU.duelli.filter(function(d){return d.giornata===G&&(d.stato==='attesa'||d.stato==='accettato')&&d.da===ME}).length;
  h+='<div class="card"><h3>Lancia una sfida</h3><div class="ch"><div>'+av(ME,'me')+'<b style="display:block;margin-top:4px">'+esc(ME)+'</b><span class="mut sm">'+mio+' fantacrediti</span></div><div class="vs">vs</div><div><div style="display:flex;justify-content:center">'+av(S.opp)+'</div><select id="opp" aria-label="Avversario" style="margin-top:4px">'+opp.map(function(t){return '<option'+(t===S.opp?' selected':'')+'>'+esc(t)+'</option>'}).join('')+'</select><span class="mut sm">'+cr[S.opp]+' fantacrediti</span></div></div>';
  if(mx<10)h+='<p class="sm mut" style="margin-top:10px">Non puoi sfidare '+esc(S.opp)+': la posta minima è 10 e il massimo possibile tra voi due è '+mx+'.</p>';
  else h+='<div style="margin:14px 0 4px" class="row"><b>Posta</b><span class="grow"></span><b class="num" id="stk" style="font-size:20px;color:var(--gold)">'+S.stake+' fantacrediti</b></div><input type="range" id="stake" min="10" max="'+mx+'" step="1" value="'+S.stake+'" aria-label="Posta" style="accent-color:#ffd166"><p class="sm mut" style="margin-top:6px">Massimo '+mx+': è il minimo tra quello che hai tu, quello che ha l\'avversario e il tetto di 200. I tuoi fantacrediti restano bloccati finché lui non risponde: se rifiuta o non risponde in tre giorni tornano indietro.</p><button class="btn" data-dgo="1" style="width:100%;margin-top:12px"'+(att>=3?' disabled':'')+'>Sfida '+esc(mshort(S.opp))+' per '+S.stake+'</button>'+(att>=3?'<p class="sm mut" style="margin-top:6px">Hai già tre sfide per questa giornata.</p>':'');
  h+='</div>';
  var mie=DU.duelli.filter(function(d){return d.a===ME&&d.stato==='attesa'});
  if(mie.length){h+='<div class="card"><h3>Sfide ricevute</h3>';
    mie.forEach(function(d){h+='<div class="row" style="padding:10px 0;gap:8px;flex-wrap:wrap">'+av(d.da)+'<div class="grow"><b>'+esc(d.da)+'</b> ti sfida<div class="mut sm">Giornata '+d.giornata+' · Posta '+d.posta+'</div></div><button class="btn" data-dr="accetta" data-id="'+d.id+'"'+(mio<d.posta?' disabled':'')+'>Accetta</button><button class="btn o" data-dr="rifiuta" data-id="'+d.id+'">Rifiuta</button></div>'+(mio<d.posta?'<p class="sm mut">Per accettare servono '+d.posta+' fantacrediti, ne hai '+mio+'.</p>':'')});
    h+='</div>'}
  h+='<div class="card"><h3>Sfide della lega</h3>';
  var els=DU.duelli.filter(function(d){return d.stato!=='rifiutato'&&d.stato!=='scaduto'||d.da===ME||d.a===ME});
  if(!els.length)h+='<p class="sm mut">Ancora nessuna sfida.</p>';
  els.forEach(function(x,i){var ch=x.stato==='chiuso',tag=x.stato==='attesa'?'<span class="tag g">In attesa</span>':x.stato==='accettato'?'<span class="tag o">Accettata</span>':ch?'<span class="tag">Chiusa</span>':x.stato==='rifiutato'?'<span class="tag">Rifiutata</span>':'<span class="tag">Scaduta</span>';
    h+='<div class="row" style="padding:10px 0;border-top:'+(i?'1px solid var(--line)':'0')+'">'+av(x.da)+'<div class="grow"><b>'+esc(x.da)+'</b> vs <b>'+esc(x.a)+'</b><div class="mut sm">Giornata '+x.giornata+' · Posta '+x.posta+'</div>'+(ch?'<div class="sm">'+f1(x.pa)+' - '+f1(x.pb)+' · '+(x.vincitore?'Vince <b>'+esc(x.vincitore)+'</b>, incassa '+(x.posta*2):'Pareggio: ognuno si riprende i suoi')+'</div>':'')+'</div>'+tag+'</div>'});
  h+='</div>';
  if(LV.mode==='prova')h+='<div class="lvprova" style="margin-top:14px;padding:12px;border:1px dashed rgba(255,209,102,.6);border-radius:14px"><b style="color:#ffd166">Strumenti di prova</b><p class="sm mut" style="margin:8px 0">Database finto, solo in questo browser. Con questo bottone chiudi la giornata con punteggi a caso.</p><div class="row" style="gap:6px;flex-wrap:wrap"><button class="btn o" data-dprova="chiudi">Chiudi la giornata</button><button class="btn o" data-dprova="avanza">Passano 3 giorni</button><button class="btn o" data-lprova="azzera">Azzera la prova</button></div></div>';
  return h}

/* ---------- Conferenza stampa ---------- */
function lvDopo(t,ch,pw){
  var G=D.cal[0]&&D.cal[0].n,row=DBS.conf.filter(function(c){return c.giornata===G})[0];
  var h='<div class="card"><h3>Dopo la partita</h3>';
  h+='<p class="sm mut" style="margin-bottom:8px">'+(pw?'Hai fatto '+pw+(pw===1?' promessa':' promesse')+'. Il risultato decide cosa pensa la dirigenza.':'Non hai promesso niente: la dirigenza non ha niente da contestarti.')+'</p>';
  var e=row&&row.esito;
  if(!e)h+='<p class="sm">'+(row?'La conferenza è pubblicata. L\'esito arriva dopo la partita, su Girrr Sport.':'Pubblica la conferenza: dopo la partita compare qui l\'esito.')+'</p>';
  else{var win=e==='v',draw=e==='p',msg=!pw?'Nessun commento dalla dirigenza.':win?'La dirigenza apprezza: parola mantenuta.':draw?'Un pareggio: la dirigenza lo segna, ma non è una promessa mantenuta.':'Il presidente: «Potevate evitare di essere così sfacciati».';
    h+=gsPost('<b>'+(!pw?'PARTITA FINITA':win?'PAROLA MANTENUTA':draw?'PAREGGIO':'PAROLA TRADITA')+'</b><br>'+(pw?esc(t)+' aveva detto: «'+esc(ch.filter(function(c){return c.w})[0].t)+'». '+(win?'Detto, fatto.':draw?'Non è bastato.':'Non è andata così.'):''),'Dopo la partita')+'<p style="margin-top:8px"><b>'+esc(msg)+'</b></p>'}
  if(LV.mode==='prova'&&row&&!e)h+='<div class="lvprova" style="margin-top:10px;padding:12px;border:1px dashed rgba(255,209,102,.6);border-radius:14px"><b style="color:#ffd166">Strumenti di prova</b><div class="row" style="gap:6px;flex-wrap:wrap;margin-top:8px"><button class="btn o" data-lesito="v">Vinci</button><button class="btn o" data-lesito="p">Pareggi</button><button class="btn o" data-lesito="s">Perdi</button></div></div>';
  return h+'</div>'}
function lvConfPubblica(){
  var ch=confChosen(ME);if(!ch.every(function(c){return c}))return;
  var G=D.cal[0].n,risp=[0,1,2].map(function(i){var a=S.cf.a[i];return {a:a==='free'?'free':a,t:ch[i].t,k:ch[i].k,w:ch[i].w}});
  var lib=null,prom=null,pesa=0;risp.forEach(function(r){if(r.a==='free'&&lib===null)lib=r.t.slice(0,80);if(r.w){if(prom===null)prom=r.t.slice(0,80);pesa=Math.max(pesa,r.k===2?2:1)}});
  lvCall('conf_salva',{p_team:ME,p_code:CODE,p_giornata:G,p_risposte:risp,p_libera:lib,p_promessa:prom,p_pesa:pesa},'Conferenza pubblicata').then(function(){S.cf.pub=true;S.cfok=true;render();var c=$('.post');if(c&&c.scrollIntoView)c.scrollIntoView({block:'center',behavior:'smooth'})});
}

/* ---------- Fiducia: se c'è il calcolo completo (con le promesse) vale quello ---------- */
var fid0=fid;function fid(t){return (D.fid&&D.fid[t]!=null)?Math.round(D.fid[t]):fid0(t)}

/* ---------- tocchi ---------- */
document.addEventListener('click',function(e){
  var q=e.target.closest('[data-lr],[data-lf],[data-lt],[data-lgo],[data-lnew],[data-lrx],[data-lnome],[data-lvote],[data-lprova],[data-lesito],[data-dgo],[data-dr],[data-dprova]');if(!q)return;
  e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();
  var d=q.dataset,L=S.lancio;
  if(d.lt){S.sft=d.lt;return render()}
  if(d.lr){L.r=d.lr;return render()}
  if(d.lf){L.f=+d.lf;return render()}
  if(d.lnew){S.sfnew=true;return render()}
  if(d.lgo){if(DBN!==1)return;S.sfnew=false;return lvCall('derby_sfida_lancia',{p_team:ME,p_code:CODE,p_rival:L.r,p_frase:L.f,p_nome:null,p_stagione:LV.stag},'Sfida lanciata')}
  if(d.lrx)return lvCall('derby_sfida_rispondi',{p_team:ME,p_code:CODE,p_id:+d.id,p_azione:d.lrx,p_nome:null},d.lrx==='accetta'?'Hai accettato la sfida':'Hai rifiutato la sfida');
  if(d.lnome==='ok')return lvCall('derby_nome_accetta',{p_team:ME,p_code:CODE,p_id:+d.id},'Nome accettato');
  if(d.lnome==='prop'){var box=q.closest('.card'),ip=box&&box.querySelector('.nmin'),v=(d.v||(ip&&ip.value)||'').replace(/^\s+|\s+$/g,'').slice(0,40);
    if(v.length<3){lvToast('Il nome deve avere almeno 3 lettere');return}
    return lvCall('derby_nome_proponi',{p_team:ME,p_code:CODE,p_id:+d.id,p_nome:v},'Proposta inviata')}
  if(d.lvote){var k=d.lvote,ab=k.split('|'),pair=RIV.filter(function(o){return rvKey(o.a,o.b)===k})[0];if(!pair)return;
    return lvCall('derby_vota',{p_team:ME,p_code:CODE,p_a:pair.a,p_b:pair.b,p_si:!S.mine[k]})}
  if(d.dgo){if(DU.ok!==true)return;return duCall('duello_lancia',{p_team:ME,p_code:CODE,p_rival:S.opp,p_posta:+S.stake,p_giornata:null},'Sfida lanciata')}
  if(d.dr)return duCall('duello_rispondi',{p_team:ME,p_code:CODE,p_id:+d.id,p_azione:d.dr},d.dr==='accetta'?'Hai accettato la sfida':'Hai rifiutato la sfida');
  if(d.dprova){if(d.dprova==='chiudi')MOCK.chiudiDuelli();else MOCK.avanza();return duLoad(false)}
  if(d.lprova){if(d.lprova==='avanza')MOCK.avanza();else{MOCK.azzera();S.sfnew=false;duLoad(false);S.cfok=false;S.cf.pub=false;S.cf.a=[]}return dbLoad(false)}
  if(d.lesito){MOCK.esito(ME,D.cal[0].n,d.lesito);return dbLoad(false)}
},true);
