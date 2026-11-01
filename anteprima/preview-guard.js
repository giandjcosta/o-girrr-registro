/* Isolamento della preview: nessuna richiesta viene inoltrata al database reale. */
(function(){
'use strict';
var nativeFetch=window.fetch.bind(window);
function db(u){try{return /(^|\.)supabase\.co$/i.test(new URL(u,location.href).hostname)}catch(e){return false}}
function path(resource){return typeof resource==='string'||resource instanceof URL?String(resource):resource&&resource.url||''}
function letturaLocale(u){
 var name=new URL(u,location.href).pathname.split('/').pop();
 var reads={curva_feed:{v:5,ok:false,posts:[],replies:[],react:[],mine:[],follow:[],prof:{},polls:[],adm:[],has_more:false},
 derby_stato:{voti:[],sfide:[]},toto_pr_pubblico:[],curva_adm_lista:[],curva_img:null,curva_adm_img:null};
 if(Object.prototype.hasOwnProperty.call(reads,name))return new Response(JSON.stringify(reads[name]),{status:200,headers:{'Content-Type':'application/json'}});
 return new Response(JSON.stringify({message:'Operazione non disponibile nell’anteprima locale'}),{status:403,headers:{'Content-Type':'application/json'}});
}
window.fetch=function(resource,options){var u=path(resource);if(db(u))return Promise.resolve(letturaLocale(u));return nativeFetch(resource,options)};
var open=XMLHttpRequest.prototype.open;
XMLHttpRequest.prototype.open=function(method,u){if(db(u))throw new Error('Richiesta al database bloccata nella preview');return open.apply(this,arguments)};
var beacon=navigator.sendBeacon&&navigator.sendBeacon.bind(navigator);
if(beacon)navigator.sendBeacon=function(u,data){return db(u)?false:beacon(u,data)};
})();
