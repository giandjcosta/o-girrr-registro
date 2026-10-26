/* Test isolati del wrapper lazy (nessuna dipendenza npm).
 * Eseguire dalla root del Registro: node prove/prova_spogliatoio_lazy.js
 */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const code = fs.readFileSync(path.join(__dirname,'../lab/spogliatoio-lazy.js'),'utf8');
const queue = [], rendered = [];
const buttons = ['rosa','day','swap','mkt','fa','pitch','bor','lega','stat'].map(t=>({
  dataset:{t},hidden:false,setAttribute(k,v){this[k]=v}
}));
const app = {innerHTML:''};
const document = {
  head:{appendChild(){}},
  getElementById(id){return id==='app'?app:null},
  createElement(){return {id:'',textContent:''}},
  querySelectorAll(){return buttons}
};
const window = {};
vm.runInNewContext(code,{window,document,requestAnimationFrame:fn=>queue.push(fn)});
function flush(){while(queue.length)queue.shift()()}
const state = {tab:'rosa',team:'Oranje VC',authed:true,data:{updated:'A'},filter:'ALL'};
const wrapper=window.spgLazyWrap(()=>rendered.push(state.tab),()=>({
  ...state,setTab(t){state.tab=t}
}));
wrapper();
assert.deepEqual(rendered,['rosa'],'Rosa immediata');
state.tab='swap';wrapper();
assert.match(app.innerHTML,/Carico Chi scambiare/);
assert.equal(rendered.length,1,'Render pesante differito');
flush();assert.equal(rendered.at(-1),'swap');
state.tab='mkt';wrapper();
state.tab='rosa';wrapper();flush();
assert.equal(rendered.at(-1),'rosa','Tab vecchia annullata');
state.authed=false;state.tab='swap';wrapper();
assert.equal(rendered.at(-1),'swap','Login originale senza differimento');
state.authed=true;state.tab='stat';state.team='Altra squadra';wrapper();flush();
assert.equal(state.tab,'rosa','Statistiche riservate');
state.team='Oranje VC';state.tab='bor';wrapper();flush();
state.data={updated:'A'};wrapper();
assert.match(app.innerHTML,/Carico Borsino/,'Nuovi dati invalidano la firma');
flush();assert.equal(rendered.at(-1),'bor');
state.filter='D';wrapper();
assert.match(app.innerHTML,/Carico Borsino/,'Cambio filtro invalida');
flush();
console.log('OK: lazy loading Spogliatoio — 8 controlli superati');
