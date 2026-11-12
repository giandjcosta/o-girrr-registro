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
const der=M.derbies(D);assert.equal(der.matches.length,7);assert.equal(der.rows.reduce((s,r)=>s+r.g,0),der.matches.length*2);assert.equal(der.rows[0].team,'Grodah');assert.equal(der.rows[0].v,2);assert.equal(der.rows[1].rank,der.rows[2].rank);
assert(der.rows.every(r=>r.g===r.v+r.n+r.p&&!('pt' in r)));
const s=M.story(D,'Oranje VC');assert.equal(s.points,11);assert.equal(s.pos,5);assert.equal(s.windowPoints,4);assert.equal(s.next,'Mariana Coneja');assert.equal(s.quote,'Una partita alla volta, con umiltà.');
d=clone();d.rounds[0].m=d.rounds[0].m.map(m=>[m[0],70,70,m[3],'1-1']);d.rounds=d.rounds.slice(0,1);assert.equal(M.ballot(d).candidates.length,0);
console.log('PASS · Giornate parziali, buchi, duplicati, candidature, voto, Derby e racconto verificati.');

const old=M.story(D,'Oranje VC',4);assert.equal(old.day,4);assert.equal(old.points,7);assert.equal(old.quote,null);assert.equal(old.history.length,4);assert.equal(old.nextDay,5);

const or=der.rows.find(r=>r.team==='Oranje VC');assert.deepEqual([or.v,or.n,or.p,or.g],[0,1,1,2]);
assert(der.matches.some(m=>m.name==='The Continental'));assert(der.matches.some(m=>m.name==="Derby dell'Emma"));
d=clone();d.derby_ufficiali.coppie=[];assert.equal(M.derbies(d).matches.length,0); // Nessuna rivalità diventa ufficiale per deduzione.
const R=require('../lab/prova-tifosi/racconti.js');
assert.equal(R.create(D,'Oranje VC',7).title,'Un passo ritrovato, prima della capolista');
assert.equal(new Set([1,2,3,4,5,6,7].map(n=>R.create(D,'Oranje VC',n).title)).size,7);
assert(R.create(D,'Oranje VC',6).paragraphs.join(' ').includes('The Continental'));
assert(!R.create(D,'Oranje VC',4).paragraphs.join(' ').includes('3–0'));
d=clone();d.rounds[0].m[0][4]='4-2';assert.equal(R.create(d,'Oranje VC',7).edited,false);
d=clone();d.rounds[7].m[0][4]='9-0';assert.deepEqual(R.create(d,'Oranje VC',4),R.create(D,'Oranje VC',4));
d=clone();d.dossier.squadre['Oranje VC'].ultima_conferenza.giornata=9;assert.equal(M.story(d,'Oranje VC',7).quote,null);
for(const t of D.teams)for(let n=1;n<=7;n++){let a=R.create(D,t,n);assert.equal(a.paragraphs.length,3);assert(!/Fantapunti|fantacrediti/i.test(a.paragraphs.join(' ')))}
console.log('PASS · Derby ufficiali Oranje, racconti, impronte dei fatti e cronologia delle citazioni.');

d=clone();d.rounds=d.rounds.slice(0,3);d.rounds.forEach(g=>{const m=g.m.find(m=>[m[0],m[3]].includes('Oranje VC'));m[4]='1-1'});assert(R.create(d,'Oranje VC',3).paragraphs.join(' ').includes('3 pareggi consecutivi'));
d.rounds.forEach(g=>{const m=g.m.find(m=>[m[0],m[3]].includes('Oranje VC'));m[4]=m[0]==='Oranje VC'?'0-1':'1-0'});assert(R.create(d,'Oranje VC',3).paragraphs.join(' ').includes('3 sconfitte consecutive'));
