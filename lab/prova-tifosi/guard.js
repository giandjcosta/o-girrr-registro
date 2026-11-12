/* Prima di qualsiasi script originale: nessuna RPC, autenticazione o invio reale. */
(function(){
'use strict';
var nativeFetch=window.fetch.bind(window), blocked=[];
window.PROVA_TIFOSI={blocked:blocked};
function forbidden(url){try{var u=new URL(url,document.baseURI);return u.origin!==location.origin}catch(e){return true}}
window.fetch=function(input,init){var url=typeof input==='string'?input:input.url, method=((init&&init.method)||(input&&input.method)||'GET').toUpperCase();
 if(forbidden(url)||!['GET','HEAD'].includes(method)){blocked.push(String(url));return Promise.resolve(new Response(JSON.stringify({ok:false,prova:true,error:'Operazione non disponibile nella prova',voti:[],sfide:[],post:[],posts:[],replies:[],react:[],mine:[],follow:[],prof:{},commenti:[],eventi:[],notifiche:[]}),{status:200,headers:{'Content-Type':'application/json'}}))}
 var mapped=new URL(url,document.baseURI);if(mapped.origin===location.origin&&mapped.pathname.startsWith('/o-girrr-registro/')){var repo=new URL('../../',own);input=new URL(mapped.pathname.slice('/o-girrr-registro/'.length)+mapped.search,repo).href}return nativeFetch(input,init)};
var open=XMLHttpRequest.prototype.open,send=XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.open=function(m,u){this._provaBlocked=forbidden(u)||!['GET','HEAD'].includes(String(m).toUpperCase());return open.apply(this,arguments)};
XMLHttpRequest.prototype.send=function(){if(this._provaBlocked){blocked.push('XHR bloccata');return}return send.apply(this,arguments)};
if(navigator.sendBeacon)navigator.sendBeacon=function(){blocked.push('Beacon bloccato');return false};
if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(Error('Service worker escluso dalla prova'))};
// Non leggere o alterare la sessione fg reale: identità originale temporanea e solo in memoria.
var get=Storage.prototype.getItem,set=Storage.prototype.setItem,remove=Storage.prototype.removeItem;
Storage.prototype.getItem=function(k){if(this===localStorage&&k==='fg')return JSON.stringify({team:new URLSearchParams(location.search).get('squadra')||'Oranje VC',code:'prova-locale'});return get.call(this,k)};
Storage.prototype.setItem=function(k,v){if(this===localStorage&&!String(k).startsWith('og:prova-tifosi:'))return;return set.call(this,k,v)};
Storage.prototype.removeItem=function(k){if(this===localStorage&&!String(k).startsWith('og:prova-tifosi:'))return;return remove.call(this,k)};
// Le copie non aprono azioni o pagine di produzione, neppure da un menu nativo.
document.addEventListener('submit',function(e){e.preventDefault();e.stopImmediatePropagation()},true);
var own=new URL('../../../lab/prova-tifosi/',document.baseURI);
if(document.baseURI.includes('/stadio/'))own=new URL('../../../../lab/prova-tifosi/',document.baseURI);
window.PROVA_TIFOSI.root=own.href;
window.PROVA_TIFOSI.mirror=new URL('../../anteprima/pubblicata/',own).href;
// Adattatore dei percorsi del sito: i moduli originali restano invariati.
window.OG55={sito:true,dir:function(sk){return new URL('../../anteprima/pubblicata/'+(sk==='stadio'?'stadio/girrr/':'girrr/'),own).href},pagina:function(which,sk){var u=new URL(sk+'/'+(which==='albo'?'albo':which)+'.html',own);u.search=location.search;return u.href},nome:function(p){return p.split('/').pop().replace('.html','')}};

document.addEventListener('click',function(e){
 var back=e.target.closest&&e.target.closest('#lg,#olg,[data-lega]');if(back){e.preventDefault();e.stopImmediatePropagation();var home=new URL((location.pathname.includes('/stadio/')?'stadio':'lega')+'/index.html',own);home.search=location.search;location.href=home.href;return}
 var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;
 var raw=a.getAttribute('href'),u=new URL(a.href),skin=location.pathname.includes('/stadio/')?'stadio':'lega',page=u.pathname.split('/').pop()||'index.html';
 if(a.hasAttribute('download'))return;
 if(raw.startsWith('#'))return;
 if(/\/stadio\//.test(u.pathname))skin='stadio';else if(/\/girrr\//.test(u.pathname))skin='lega';
 if(u.href.startsWith(own.href)&&!u.pathname.includes('/anteprima/'))return;
 e.preventDefault();e.stopImmediatePropagation();
 if(['index.html','curva.html','derby.html','app.html','giornale.html','albo.html'].includes(page)){
 var dest=new URL(skin+'/'+page,own);dest.search=u.search;dest.hash=u.hash;var q=new URLSearchParams(location.search);for(var k of ['prima','squadra'])if(q.has(k))dest.searchParams.set(k,q.get(k));location.href=dest.href;
 }else{var msg=document.getElementById('pt-status');if(msg)msg.textContent='Questo collegamento resta fuori dalla prova: '+(a.textContent.trim()||page)}
},true);
})();
