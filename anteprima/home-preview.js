/* Home originale: riempie la testata soltanto con letture pubbliche. */
(function(){
 var sito='https://giandjcosta.github.io/o-fant-a-girrr/';
 document.getElementById('bh').textContent='La giornata del Girrr';
 document.getElementById('bp').textContent='Risultati, classifica e storie della Lega.';
 fetch(sito+'data.json',{cache:'no-store'}).then(function(r){if(!r.ok)throw Error(r.status);return r.json()}).then(function(d){
  var complete=(d.cal.lega||[]).filter(function(g){return g.m.length===d.teams.length/2&&g.m.every(function(m){return /^\d+-\d+$/.test(m[4])})});
  if(!complete.length)return;var g=complete[complete.length-1];document.getElementById('bh').textContent='Il racconto della '+g.n+'ª giornata';document.getElementById('bk').textContent='CAMPIONATO · SERIE A '+g.sa;document.getElementById('bp').textContent=g.m.map(function(m){return m[0]+' '+m[4]+' '+m[3]}).join(' · ');
 }).catch(function(){document.getElementById('bp').textContent='Il calendario non è disponibile. Apri il Tabellone per riprovare.'});
 fetch(sito+'riepiloghi/indice.json',{cache:'no-store'}).then(function(r){if(!r.ok)throw Error(r.status);return r.json()}).then(function(a){if(a[0]&&a[0].copertina){document.getElementById('bc').src=sito+a[0].copertina}}).catch(function(){document.getElementById('bc').hidden=true});
})();
