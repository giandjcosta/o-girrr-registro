const fs=require('fs'),assert=require('assert');
for(const file of ['prod/girrr/app.html','prod/stadio/girrr/app.html']){
 const s=fs.readFileSync(file,'utf8');
 const start=s.indexOf('function ultimaGiornataVerificata()'),end=s.indexOf('function gioc(){',start);
 const a=s.slice(start,end);
 const x=s.indexOf('function defaultCarMilestone('),y=s.indexOf('function vCarL(){',x);
 assert(start>=0&&end>start&&x>=0&&y>x,file+' missing milestone functions');
 const b=s.slice(x,y);
 function fixture(full){
  const CL=Array.from({length:34},(_,i)=>({n:i+1,m:Array.from({length:5},()=>['A',70,69,'B',i<full?'1-0':'-'])}));
  const S={};const fn=new Function('CL','S','Math','Number','returnVal',a+b+"return function(t){aggiornaMilestone(t);return S.fdem}");
  return fn(CL,S,Math,Number,1);
 }
 // Inject utilities through a new Function so the production algorithm really executes
 for(const [played,expected] of [[4,2],[5,2],[6,6],[7,6],[8,8],[10,10],[18,18]]){
  const CL=Array.from({length:34},(_,i)=>({n:i+1,m:Array.from({length:5},()=>['A',70,69,'B',i<played?'1-0':'-'])}));
  const result=new Function('CL',a+b+"var S={};function gioc(){return 2}function row(){return {pos:5}}function aGiornata(n){return {pos:n===8?2:3}}aggiornaMilestone('A');return S.fdem")(CL);
  assert.equal(result.g,expected,file+' milestone G'+played);
  if(expected===8)assert.equal(result.p,2,file+' actual G8 position');
 }
 console.log('PASS',file,'G2/4/7/8/10/18');
}
