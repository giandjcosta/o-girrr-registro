const fs=require('fs'),vm=require('vm'),assert=require('assert');
const base=['lab/index.html','anteprima/index.html','anteprima/attuale.html'];
for(const file of base){
 const html=fs.readFileSync(file,'utf8');
 for(const match of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)){
   if(match[1].trim()&&!match[0].includes('application/json'))new vm.Script(match[1],{filename:file});
 }
 for(const label of ['var _milestones=[2,6,8,10,18,26,34]','_played=Math.max(gioc(),(CL||[])','S.fdem.team!==t||S.fdem.anchor!==_anchor','aGiornata(_anchor,t)','function aGiornata(n,t){if(!CL||!CL.some(','totogirrr-premi-5-2.html'])
   assert(html.includes(label),file+' missing '+label);
 console.log('PASS syntax and milestones',file);
}
const preview=fs.readFileSync('anteprima/totogirrr-premi-5-2.html','utf8');
const index=preview.indexOf('const awards='),end=preview.indexOf(';',index);
assert(index>=0&&end>index,'award payload missing');
const awardSource=preview.slice(index,end+1)+'; return awards;';
const awards=new Function(awardSource)();
const expected={'AFA SELECCION':75,'Apo team':50,'Atletico ma non troppo':75,
  'Grodah':50,'Real Madrink':75,'stif dc':75,'WOA':50};
assert.deepStrictEqual(Object.keys(awards).sort(),Object.keys(expected).sort());
for(const [team,amount] of Object.entries(expected))assert.equal(awards[team].amount,amount);
assert(preview.includes("btn.textContent=claimed?'Riscattato nella demo':'Riscatta premio'"));
assert(preview.includes('sessionStorage.setItem(key,JSON.stringify(claims))'));
assert(!/fetch\(|XMLHttpRequest|supabase.co|rest\/v1\/rpc/.test(preview),'no live backend allowed in demo');
console.log('PASS 7 verified sponsors, 450 credits total, demo-only redemption');

// Calculation may use official calendar even when embedded mock table still reports round 2.
const c=fs.readFileSync('lab/index.html','utf8');
const start=c.indexOf('function aGiornata(n,t){'),stop=c.indexOf('/* esito',start);
assert(start>0&&stop>start,'aGiornata missing');
const source=c.slice(start,stop);
const context={CL:[
{n:2,m:[['A',78,70,'B','2-1'],['C',70,70,'D','1-1']]},
{n:8,m:[['A',80,70,'B','3-1'],['C',75,65,'D','2-1']]}],
gioc:()=>2,Math,Object};
vm.createContext(context);vm.runInContext(source,context);
assert.equal(context.aGiornata(8,'A').pos,1);
assert.equal(context.aGiornata(8,'D').pos,3);
assert.equal(context.aGiornata(7,'A'),null);
console.log('PASS official G8 milestone even if embedded table is still G2');
