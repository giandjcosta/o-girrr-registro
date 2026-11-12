/* Calcoli puri, verificabili anche senza browser. Nessuna chiamata di rete. */
(function(root){
'use strict';
function complete(data){var names=data.teams.slice().sort().join('|'),out=[];
 for(var g of data.rounds.slice().sort((a,b)=>a.n-b.n)){
  if(g.n!==out.length+1||g.m.length*2!==data.teams.length||!g.m.every(m=>/^\d+-\d+$/.test(m[4]))||g.m.flatMap(m=>[m[0],m[3]]).sort().join('|')!==names)break;
  out.push(g);
 }return out}
function table(data,rounds){var rows=Object.fromEntries(data.teams.map(t=>[t,{team:t,pt:0,g:0,v:0,n:0,p:0,gf:0,gs:0,fp:0}]));
 rounds.forEach(g=>g.m.forEach(m=>{var s=m[4].split('-').map(Number);[0,1].forEach(i=>{var r=rows[m[i?3:0]],gf=s[i],gs=s[1-i];r.g++;r.gf+=gf;r.gs+=gs;r.fp+=Number(m[i?2:1])||0;if(gf>gs){r.v++;r.pt+=3}else if(gf===gs){r.n++;r.pt++}else r.p++})}));
 return Object.values(rows).sort((a,b)=>b.pt-a.pt||(b.gf-b.gs)-(a.gf-a.gs)||b.fp-a.fp||a.team.localeCompare(b.team));}
function ballot(data,day){var rounds=complete(data),g=rounds.find(g=>g.n===day)||rounds.at(-1);if(!g)return null;
 var prev=table(data,rounds.filter(r=>r.n<g.n));var candidates=g.m.flatMap(m=>{var s=m[4].split('-').map(Number);return [0,1].filter(i=>s[i]>s[1-i]).map(i=>{var team=m[i?3:0],op=m[i?0:3],opp=prev.findIndex(r=>r.team===op)+1;return {team,op,gf:s[i],gs:s[1-i],away:i===1,opPos:opp,score:10*(s[i]-s[1-i])+s[i]+(i?2:0)+(data.teams.length-opp)/10}})}).sort((a,b)=>b.score-a.score||a.team.localeCompare(b.team)).slice(0,3);
 // Nessuna candidatura inventata se ci sono meno di tre vincitrici.
 return {day:g.n,id:'mvp-club-2026-27-g'+g.n,candidates};}
function tally(b,vote){if(!b||!b.candidates.length)return [];var votes=Array.isArray(vote)?vote:[vote];return b.candidates.map((c,i)=>{var red=i===0?2:0,personaggi=(i===Math.min(1,b.candidates.length-1)?2:0)+(i===Math.min(2,b.candidates.length-1)?1:0),human=votes.filter(v=>v===c.team).length;return {...c,red,personaggi,human,total:red+personaggi+human}}).sort((a,b)=>b.total-a.total||b.red-a.red||a.team.localeCompare(b.team))}
function derbies(data){var out=data.teams.map(team=>({team,g:0,v:0,n:0,p:0,pt:0,gf:0,gs:0})),matches=[];complete(data).forEach(g=>g.m.forEach(m=>{var r=data.rivalita.find(r=>[r.a,r.b].includes(m[0])&&[r.a,r.b].includes(m[3]));if(!r)return;var s=m[4].split('-').map(Number);matches.push({day:g.n,a:m[0],b:m[3],score:m[4],name:r.n});[0,1].forEach(i=>{var row=out.find(x=>x.team===m[i?3:0]);row.g++;row.gf+=s[i];row.gs+=s[1-i];if(s[i]>s[1-i]){row.v++;row.pt+=3}else if(s[i]===s[1-i]){row.n++;row.pt++}else row.p++})}));return {rows:out.filter(r=>r.g).sort((a,b)=>b.pt-a.pt||(b.gf-b.gs)-(a.gf-a.gs)||b.gf-a.gf||a.team.localeCompare(b.team)),matches}}
function story(data,team){var rounds=complete(data),last=rounds.at(-1);if(!last)return null;var rows=table(data,rounds),row=rows.find(r=>r.team===team),recent=rounds.slice(-2).map(g=>{var m=g.m.find(m=>m[0]===team||m[3]===team),i=m[0]===team?0:1,s=m[4].split('-').map(Number);return {day:g.n,op:m[i?0:3],gf:s[i],gs:s[1-i],pt:s[i]>s[1-i]?3:s[i]===s[1-i]?1:0}}),points=recent.reduce((s,r)=>s+r.pt,0),next=data.rounds.find(g=>g.n===last.n+1),m=next&&next.m.find(m=>m[0]===team||m[3]===team),op=m&&m[m[0]===team?3:0];
 var dossier=data.dossier.ultima_giocata===last.n?data.dossier.squadre[team]:null;
 return {team,day:last.n,pos:rows.indexOf(row)+1,points:row.pt,recent,windowPoints:points,next:op,nextDay:next&&next.n,quote:dossier&&dossier.ultima_conferenza&&dossier.ultima_conferenza.risposte&&dossier.ultima_conferenza.risposte[0],history:rounds.map((g,i)=>({day:g.n,pos:table(data,rounds.slice(0,i+1)).findIndex(r=>r.team===team)+1}))};}
var api={complete,table,ballot,tally,derbies,story};if(typeof module!=='undefined')module.exports=api;else root.ProvaModel=api;
})(typeof window!=='undefined'?window:globalThis);
