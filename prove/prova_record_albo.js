#!/usr/bin/env node
/* Collaudo isolato del calcolo record delle due anteprime Albo. Non accede alla rete. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const fixtures = {
  cal: {
    lega:[{n:1,sa:5,m:[['A',72,72,'B','1-1'],['C',75,65,'D','2-0']]}],
    cup:[{n:1,sa:6,m:[['A','A',80,80,'B','2-2'],['A','C',76,70,'D','3-1']]}]
  }
};
for(const f of ['lab/prova-record-albo.html','lab/prova-record-albo-stadio.html']){
  const html=fs.readFileSync(f,'utf8');
  const first=html.indexOf('function tutte(){');
  const last=html.indexOf('/* Storico',first);
  assert(first>=0 && last>first,f+' calcolo mancante');
  const source=html.slice(first,last);
  const code="function cap(x){return String(x)}function esc(x){return String(x)}function pt(x){return String(x)}\n"+source+"\nreturn {html:recs(),serie:serie(tutte()),partite:tutte()};";
  const result=Function('D',code)(fixtures);
  assert.match(result.html,/Vittoria più larga/);
  assert.match(result.html,/Vittoria più sofferta/);
  assert.match(result.html,/Pareggio con più gol/);
  assert.match(result.html,/Champions Cup · 1ª giornata/);
  assert.match(result.html,/Campionato · 1ª giornata/);
  assert.equal(result.serie.best.t,'C','La serie di vittorie deve appartenere a C, non ad A (pareggi)');
  assert.equal(result.serie.best.n,2);
  assert.equal(result.serie.best.primo.comp,'Campionato');
  assert.equal(result.serie.best.ultimo.comp,'Champions Cup');
  console.log('PASS',f,'pareggi non classificati come vittorie, competizione/giornata, serie mista');
}
