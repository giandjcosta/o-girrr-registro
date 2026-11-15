/* 6.2 · Albo d'oro › Record: MVP del campionato e partita più seguita (Claude, 15 novembre 2026, richiesta di Gianluca).
   Dati da v62_albo (preparata da ChatGPT). Finché non c'è, gli MVP si ricavano dall'archivio di mvp_stato e la partita
   più seguita resta «Dato non disponibile». Niente oro nell'Albo (decisione di Gianluca). */
(function(){'use strict';
const ROOT=new URL('./',document.currentScript.src).href;
const E=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const N=x=>String(x??'').replace(/The Blue brothers/g,'The Blues Brothers');
const box=(id,titolo,corpo,kicker)=>'<section class="pt-box" id="'+id+'">'+(kicker?'<div class="pt-kicker">'+E(kicker)+'</div>':'')+'<h2>'+E(titolo)+'</h2>'+corpo+'</section>';
let cfg=null,albo=null;
async function rpc(nome,args){const r=await fetch(cfg.url+'/rest/v1/rpc/'+nome,{method:'POST',headers:{apikey:cfg.publishableKey,'Content-Type':'application/json'},body:JSON.stringify(args),cache:'no-store'});if(!r.ok)throw Error(nome);const j=await r.json();if(j?.error)throw Error(nome);return j}
function daArchivio(stato){
 const mvp=(stato?.archivio||[]).filter(a=>a.chiusa&&a.classifica?.[0]?.team).map(a=>({giornata:a.giornata,team:a.classifica[0].team,chiusa:a.chiusa})).sort((a,b)=>a.giornata-b.giornata);
 const per={};mvp.forEach(m=>{(per[m.team]=per[m.team]||{team:m.team,mvp:0,giornate:[]});per[m.team].mvp++;per[m.team].giornate.push(m.giornata)});
 const classifica=Object.values(per).sort((a,b)=>b.mvp-a.mvp||Math.max(...b.giornate)-Math.max(...a.giornate));
 return {stagione:cfg.stagione,mvp,mvp_classifica:classifica,partite:null,stagione_conclusa:false};
}
function mvpCampionato(a){
 const c=a.mvp_classifica||[],fine=!!a.stagione_conclusa,k='Albo d’oro · Record · '+(a.stagione||cfg.stagione);
 const spiega='<p>Il titolo va alla squadra con più MVP dei tifosi nella stagione, giornata dopo giornata.</p>';
 if(!c.length)return box('pt-mvp-campionato',fine?'MVP del campionato':'Corsa all’MVP del campionato',spiega+'<p>Nessun verdetto ancora: il primo arriva alla chiusura della votazione dell’MVP dei tifosi.</p>',k);
 const max=c[0].mvp,primi=c.filter(x=>x.mvp===max);let pos=0,prec=null;
 const righe=c.map((x,i)=>{if(x.mvp!==prec){pos=i+1;prec=x.mvp}return '<tr><td>'+pos+'</td><td>'+E(N(x.team))+'</td><td><b>'+x.mvp+'</b></td><td>'+(x.giornate||[]).map(g=>g+'ª').join(', ')+'</td></tr>'}).join('');
 const testa=fine?'<p><b>MVP del campionato '+E(a.stagione||cfg.stagione)+': '+primi.map(x=>E(N(x.team))).join(' e ')+'</b>, con '+max+' '+(max===1?'MVP':'MVP')+(primi.length>1?' a pari merito':'')+'.</p>':'<p>In testa '+primi.map(x=>E(N(x.team))).join(' e ')+(primi.length>1?' a pari merito':'')+', con '+max+' MVP.</p>';
 return box('pt-mvp-campionato',fine?'MVP del campionato':'Corsa all’MVP del campionato',spiega+testa+'<table class="pt-table"><thead><tr><th>#</th><th>Squadra</th><th>MVP</th><th>Giornate</th></tr></thead><tbody>'+righe+'</tbody></table><p class="pt-sub">A pari numero di MVP le squadre sono a pari merito.</p>',k);
}
function partitaSeguita(a){
 const k='Albo d’oro · Record · '+(a.stagione||cfg.stagione),spiega='<p>Conta i voti ai sondaggi «Quale sfida seguire»: allenatori dall’app, redazione e personaggi della Curva.</p>';
 if(a.partite==null)return box('pt-partita-seguita','La partita più seguita',spiega+'<p>Dato non disponibile.</p>',k);
 const p=(a.partite||[]).slice(0,5);
 if(!p.length)return box('pt-partita-seguita','La partita più seguita',spiega+'<p>Nessun sondaggio delle partite ancora concluso.</p>',k);
 const det=v=>'Allenatori '+(v.allenatori||0)+' · Redazione '+(v.redazione||0)+' · Personaggi '+(v.personaggi||0);
 const nome=x=>E(N(x.partita||'').split(' - ').join(' – '));
 const top=p[0];
 return box('pt-partita-seguita','La partita più seguita',spiega+'<article class="pt-award-day"><h3>'+nome(top)+'</h3><p>'+top.giornata+'ª giornata · '+(top.voti?.totale||0)+' '+((top.voti?.totale||0)===1?'voto':'voti')+'</p><p class="pt-sub">'+det(top.voti||{})+'</p></article>'+(p.length>1?'<details><summary>Le altre più seguite</summary><ol class="pt-audit">'+p.slice(1).map(x=>'<li><b>'+nome(x)+'</b><small>'+x.giornata+'ª giornata · '+(x.voti?.totale||0)+' voti · '+det(x.voti||{})+'</small></li>').join('')+'</ol></details>':''),k);
}
function disegna(){
 const host=document.querySelector('[data-ap="rec"]');if(!host||!albo)return;
 for(const [id,html] of [['pt-mvp-campionato',mvpCampionato(albo)],['pt-partita-seguita',partitaSeguita(albo)]]){
  const el=document.getElementById(id);if(el){if(el.outerHTML!==html)el.outerHTML=html}else{const dopo=document.getElementById(id==='pt-mvp-campionato'?'pt-archivio':'pt-mvp-campionato');dopo&&dopo.parentElement===host?dopo.insertAdjacentHTML('afterend',html):host.insertAdjacentHTML('beforeend',html)}
 }
}
async function carica(){
 try{cfg=cfg||await fetch(ROOT+'girrr/v60/tifosi-config.json').then(r=>r.json())}catch(e){return}
 try{albo=await rpc('v62_albo',{p_stagione:cfg.stagione})}catch(e){try{albo=daArchivio(await rpc('mvp_stato',{p_stagione:cfg.stagione}))}catch(e2){albo=null}}
 disegna();
}
new MutationObserver(()=>{if(albo&&!document.getElementById('pt-partita-seguita'))disegna()}).observe(document.documentElement,{childList:true,subtree:true});
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',carica):carica();
document.addEventListener('visibilitychange',()=>{if(!document.hidden)carica()});
})();
