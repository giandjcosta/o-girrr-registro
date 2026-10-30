const fs=require('fs'),vm=require('vm'),assert=require('assert');
const base=['lab/index.html','anteprima/index.html','anteprima/attuale.html'];
for(const file of base){
 const html=fs.readFileSync(file,'utf8');
 for(const match of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)){
   if(match[1].trim()&&!match[0].includes('application/json'))new vm.Script(match[1],{filename:file});
 }
 for(const label of ['var _milestones=[2,6,8,10,18,26,34]','_played=Math.max(gioc(),(CL||[])','S.fdem.team!==t||S.fdem.anchor!==_anchor','aGiornata(_anchor,t)','function aGiornata(n,t){if(!CL||ultimaGiornataVerificata()<n)','function ultimaGiornataVerificata()','function bolla52(t)','function premioSponsor(t)'])
   assert(html.includes(label),file+' missing '+label);
 console.log('PASS syntax and milestones',file);
}
// Totogirrr finto dell'anteprima: squadra e premi dalla Carriera, niente login, niente database
const toto=fs.readFileSync('anteprima/totogirrr-52.html','utf8');
for(const m of toto.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g))if(m[1].trim())new vm.Script(m[1],{filename:'totogirrr-52.html'});
assert(!/supabase\.co|rest\/v1\/rpc|function gate\(/.test(toto),'totogirrr-52: niente database né login');
for(const label of ["P52K='ogirrr52-v2'","P52Q.get('team')",'class="tback"'])assert(toto.includes(label),'totogirrr-52 missing '+label);
// la Carriera dell'anteprima porta al Totogirrr finto; nel rilascio i premi finti sono spenti (build.py)
for(const file of ['anteprima/index.html','anteprima/attuale.html']){const h=fs.readFileSync(file,'utf8');
  assert(h.includes("var PREMI52=true,TOTO52='../anteprima/totogirrr-52.html'"),file+': collegamento Totogirrr 5.2');
  assert(!/DEMO52|demo52/.test(h),file+': vecchia simulazione a mano')}
assert(fs.readFileSync('anteprima/build.py','utf8').includes('sost("var PREMI52=true,", "var PREMI52=false,")'),'build.py: premi finti spenti nel rilascio');
console.log('PASS Totogirrr 5.2 legato alla Carriera, senza database');

// Calculation may use official calendar even when embedded mock table still reports round 2.
const c=fs.readFileSync('lab/index.html','utf8');
const v0=c.indexOf('function ultimaGiornataVerificata(){'),v1=c.indexOf('\nfunction gioc(){',v0);
const start=c.indexOf('function aGiornata(n,t){'),stop=c.indexOf('/* esito',start);
assert(v0>0&&v1>v0&&start>0&&stop>start,'aGiornata/ultimaGiornataVerificata missing');
const source=c.slice(v0,v1)+'\n'+c.slice(start,stop);
// 8 giornate complete (5 partite con risultato): A vince sempre, D perde sempre
const T=['A','B','C','D','E','F','G','H','I','J'],giornata=n=>({n,m:[['A',80,70,'B','3-1'],['C',75,65,'D','2-1'],['E',70,70,'F','1-1'],['G',70,70,'H','1-1'],['I',70,70,'J','1-1']]});
const context={CL:[1,2,3,4,5,6,7,8].map(giornata).concat([{n:9,m:[['A',0,0,'B','-']]}]),gioc:()=>2,Math,Object,Number};
vm.createContext(context);vm.runInContext(source,context);
assert.equal(context.ultimaGiornataVerificata(),8);
assert.equal(context.aGiornata(8,'A').pos,1);
assert.equal(context.aGiornata(8,'D').pos,10);
assert.equal(context.aGiornata(9,'A'),null);
// una giornata incompleta in mezzo blocca le successive
const ctx2={CL:[giornata(1),{n:2,m:[['A',80,70,'B','3-1']]},giornata(3)],gioc:()=>0,Math,Object,Number};
vm.createContext(ctx2);vm.runInContext(source,ctx2);
assert.equal(ctx2.ultimaGiornataVerificata(),1);assert.equal(ctx2.aGiornata(3,'A'),null);
console.log('PASS official G8 milestone only on complete, consecutive rounds');
