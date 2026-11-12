const assert=require('node:assert/strict'),M=require('../lab/prova-tifosi/model.js'),D=require('../lab/prova-tifosi/dati.json');
const clone=()=>JSON.parse(JSON.stringify(D));
assert.equal(M.complete(D).length,7);assert.equal(M.ballot(D).day,7);
let d=clone();d.rounds[6].m[0][4]='-';assert.equal(M.complete(d).length,6);assert.equal(M.ballot(d).day,6);assert.equal(M.story(d,'Oranje VC').quote,null);
d=clone();d.rounds[2].m[0][0]=d.rounds[2].m[1][0];assert.equal(M.complete(d).length,2);
d=clone();d.rounds=d.rounds.filter(g=>g.n!==4);assert.equal(M.complete(d).length,3);
const b=M.ballot(D);assert.equal(b.candidates.length,3);assert(b.candidates.every(c=>c.gf>c.gs));
assert.deepEqual(M.ballot(D),M.ballot(D));assert.equal(M.tally(b,[]).reduce((s,r)=>s+r.total,0),5);
assert.deepEqual(M.tally(b,[b.candidates[1].team]),M.tally(b));
assert(M.tally(b).every(r=>!('human' in r)));
const der=M.derbies(D);assert.equal(der.matches.length,5);assert.equal(der.rows.reduce((s,r)=>s+r.g,0),der.matches.length*2);assert.equal(der.rows[0].team,'Grodah');assert.equal(der.rows[0].v,2);assert.equal(der.rows[1].rank,der.rows[2].rank);
assert(der.rows.every(r=>r.g===r.v+r.n+r.p&&!('pt' in r)));
const s=M.story(D,'Oranje VC');assert.equal(s.points,11);assert.equal(s.pos,5);assert.equal(s.windowPoints,4);assert.equal(s.next,'Mariana Coneja');assert.equal(s.quote,'Una partita alla volta, con umiltà.');
d=clone();d.rounds[0].m=d.rounds[0].m.map(m=>[m[0],70,70,m[3],'1-1']);d.rounds=d.rounds.slice(0,1);assert.equal(M.ballot(d).candidates.length,0);
console.log('PASS · Giornate parziali, buchi, duplicati, candidature, voto, Derby e racconto verificati.');

const old=M.story(D,'Oranje VC',4);assert.equal(old.day,4);assert.equal(old.points,7);assert.equal(old.quote,null);assert.equal(old.history.length,4);assert.equal(old.nextDay,5);
