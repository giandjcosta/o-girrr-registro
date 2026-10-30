// Verifica formule universali Fiducia e premi sponsor, senza DB writes.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
for(const file of ['lab/index.html','anteprima/index.html','anteprima/attuale.html']){
 const html=fs.readFileSync(file,'utf8');
 const m=html.match(/function fiduciaScarto\(t,pos,g\)\{[\s\S]*?\n\}/);
 assert(m,file+': funzione assente');
 const env={EXP:{BigTeam:2,Emergente:5,Outsider:8},NG:34,Math};
 vm.createContext(env);vm.runInContext(m[0],env);
 const f=env.fiduciaScarto;
 for(const team of Object.keys(env.EXP)){
  const exp=env.EXP[team];
  assert.equal(f(team,exp,34),0);
  assert.equal(f(team,1,0),0);
  assert.equal(f(team,10,10),0);
  assert(f(team,1,34)>0,file+': bonus '+team);
  assert(f(team,10,34)<0,file+': malus '+team);
  for(const g of [0,4,10,16,22,28,34]){
    for(const position of [1,2,4,6,8,10]){
      const v=f(team,position,g);
      assert(v>=-11&&v<=11,file+': fuori scala');
      if(position<exp)assert(v>=0,file+': segno bonus errato');
      if(position>exp)assert(v<=0,file+': segno malus errato');
    }
  }
  assert(Math.abs(f(team,1,12))<=Math.abs(f(team,1,34)),file+': maturazione bonus');
  assert(Math.abs(f(team,10,12))<=Math.abs(f(team,10,34)),file+': maturazione malus');
 }
 assert(html.includes("Chiudi meglio/i.test(sp.testo)?125"),file+': premio alto assente');
 assert(html.includes("?100:/giornate/i.test(sp.testo)?75:50"),file+': livelli sponsor assenti');
 assert(html.includes("(50–125 secondo difficoltà)"),file+': testo premio assente');
 console.log('PASS',file,'3 categorie, 7 giornate, 6 posizioni, bonus/malus + premi 50/75/100/125');
}
