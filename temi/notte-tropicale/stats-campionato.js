/* O Fant A Girrr · Numeri del Campionato · ChatGPT, 17 novembre 2026.
   Fonte: data.json, SOLO d.cal.lega. ES5, nessuna libreria.
   I gol dei risultati, i punti in classifica e i Fantapunti sono distinti.
   Un risultato "-" non è una partita giocata. */
function statsCampionato(d) {
  var turni = d && d.cal &&
    Object.prototype.toString.call(d.cal.lega) === '[object Array]' ? d.cal.lega.slice() : [];
  var squadre = Object.create(null);
  var disputate = [], giornateGiocate = 0, giornateParziali = 0;
  var golTotali = 0, pareggi = 0, fantapuntiMassimi = null, fantapuntiMinimi = null;
  var partitaPiuGol = null, vittoriaPiuLarga = null;

  function numero(x) {
    if (x === null || x === undefined || x === '') return null;
    var n = Number(x);
    return isFinite(n) ? n : null;
  }
  function squadra(nome) {
    if (!squadre[nome]) squadre[nome] = {
      squadra:nome, partite:0, vittorie:0, pareggi:0, sconfitte:0,
      puntiClassifica:0, golFatti:0, golSubiti:0, fantapuntiTotali:0,
      casa:0, sconfitteCasa:0, trasferta:0, sconfitteTrasferta:0, sequenza:[]
    };
    return squadre[nome];
  }
  function miglioreAttuale(attuale, candidato, campo, massimo) {
    if (!attuale || (massimo ? candidato[campo] > attuale[campo] : candidato[campo] < attuale[campo])) return candidato;
    return attuale;
  }
  function aggiornaFantapunti(nome, valore, giornata, campo) {
    var n = numero(valore);
    if (n === null) return;
    var o = { squadra:nome, fantapunti:n, giornata:giornata, campo:campo };
    fantapuntiMassimi = miglioreAttuale(fantapuntiMassimi, o, 'fantapunti', true);
    fantapuntiMinimi = miglioreAttuale(fantapuntiMinimi, o, 'fantapunti', false);
    squadra(nome).fantapuntiTotali += n;
  }
  function aggiorna(nome, fatti, subiti, fantapunti, giornata, campo) {
    var t = squadra(nome), esito = fatti > subiti ? 'V' : fatti === subiti ? 'P' : 'S';
    t.partite++;
    t.golFatti += fatti; t.golSubiti += subiti;
    if (esito === 'V') { t.vittorie++; t.puntiClassifica += 3; }
    if (esito === 'P') { t.pareggi++; t.puntiClassifica++; }
    if (esito === 'S') t.sconfitte++;
    if (campo === 'Casa') { t.casa++; if (esito === 'S') t.sconfitteCasa++; }
    else { t.trasferta++; if (esito === 'S') t.sconfitteTrasferta++; }
    t.sequenza.push({ giornata:giornata, esito:esito });
    aggiornaFantapunti(nome, fantapunti, giornata, campo);
  }

  turni.sort(function(a, b) { return Number(a.n) - Number(b.n); });
  turni.forEach(function (g) {
    var partite = g && Object.prototype.toString.call(g.m) === '[object Array]' ? g.m : [];
    var valide = 0;
    partite.forEach(function (m) {
      if (!m || m.length < 5 || typeof m[0] !== 'string' || typeof m[3] !== 'string') return;
      var r = /^(\d+)-(\d+)$/.exec(String(m[4]));
      if (!r) return; /* Non usare i risultati non disputati. */
      var gc = Number(r[1]), go = Number(r[2]), giornata = Number(g.n);
      var info = { giornata:giornata, casa:m[0], ospite:m[3],
        risultato:gc + '-' + go, golTotali:gc + go };
      valide++; disputate.push(info); golTotali += gc + go;
      if (gc === go) pareggi++;
      partitaPiuGol = miglioreAttuale(partitaPiuGol, info, 'golTotali', true);
      if (gc !== go) {
        var scarto = { giornata:giornata, casa:m[0], ospite:m[3],
          risultato:info.risultato, scarto:Math.abs(gc - go) };
        vittoriaPiuLarga = miglioreAttuale(vittoriaPiuLarga, scarto, 'scarto', true);
      }
      aggiorna(m[0], gc, go, m[1], giornata, 'Casa');
      aggiorna(m[3], go, gc, m[2], giornata, 'Trasferta');
    });
    if (partite.length && valide === partite.length) giornateGiocate++;
    else if (valide) giornateParziali++;
  });

  function preferisciSerie(record, migliore) {
    if (!migliore || record.numero > migliore.numero ||
        (record.numero === migliore.numero && record.squadra.localeCompare(migliore.squadra) < 0)) return record;
    return migliore;
  }
  var nomi = Object.keys(squadre).sort(function(a,b){return a.localeCompare(b);});
  var attacco = null, difesa = null, vittorieConsecutive = null, imbattibilita = null;
  var imbattuteCasa = [], imbattuteTrasferta = [];
  nomi.forEach(function(nome) {
    var t = squadre[nome], v = 0, i = 0, daV = null, daI = null;
    if (!attacco || t.golFatti > attacco.gol) attacco = {squadra:nome, gol:t.golFatti};
    if (!difesa || t.golSubiti < difesa.golSubiti) difesa = {squadra:nome, golSubiti:t.golSubiti};
    if (t.casa && !t.sconfitteCasa) imbattuteCasa.push(nome);
    if (t.trasferta && !t.sconfitteTrasferta) imbattuteTrasferta.push(nome);
    t.sequenza.forEach(function(p) {
      if (p.esito === 'V') { if (!v) daV = p.giornata; v++; } else v = 0;
      if (p.esito !== 'S') { if (!i) daI = p.giornata; i++; } else i = 0;
      if (v) vittorieConsecutive = preferisciSerie({
        squadra:nome, numero:v, daGiornata:daV, aGiornata:p.giornata
      }, vittorieConsecutive);
      if (i) imbattibilita = preferisciSerie({
        squadra:nome, numero:i, daGiornata:daI, aGiornata:p.giornata
      }, imbattibilita);
    });
  });
  var riepilogoSquadre = nomi.map(function(n) {
    var t=squadre[n];
    return { squadra:n, partite:t.partite, puntiClassifica:t.puntiClassifica,
      golFatti:t.golFatti, golSubiti:t.golSubiti,
      fantapuntiTotali:Math.round(t.fantapuntiTotali * 100) / 100 };
  });
  return {
    squadre:nomi.length, giornateGiocate:giornateGiocate, giornateParziali:giornateParziali,
    partiteGiocate:disputate.length, golTotali:golTotali,
    golAPartita:disputate.length ? Math.round(golTotali / disputate.length * 100) / 100 : 0,
    pareggi:pareggi, migliorAttacco:attacco, migliorDifesa:difesa,
    piuVittorieConsecutive:vittorieConsecutive, imbattibilitaPiuLunga:imbattibilita,
    partitaPiuGol:partitaPiuGol, vittoriaPiuLarga:vittoriaPiuLarga,
    fantapuntiMassimi:fantapuntiMassimi, fantapuntiMinimi:fantapuntiMinimi,
    imbattuteCasa:imbattuteCasa, imbattuteTrasferta:imbattuteTrasferta,
    riepilogoSquadre:riepilogoSquadre
  };
}

function renderStats(s) {
  /* Escaping di TUTTI i dati, inclusi i nomi delle squadre. */
  function esc(x) {
    return String(x === null || x === undefined ? '—' : x).replace(/[&<>"']/g,function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }
  function fmt(n) { return n === null || n === undefined ? '—' : String(n).replace('.',','); }
  function box(titolo,valore,dettaglio,grande) {
    return '<article class="nt-stat' + (grande ? ' nt-stat-grande':'') + '">' +
      '<h3>'+esc(titolo)+'</h3><strong>'+esc(valore)+'</strong><p>'+esc(dettaglio||'')+'</p></article>';
  }
  function risultato(p){return p ? p.casa+' '+p.risultato+' '+p.ospite : '—';}
  function giornata(p){return p ? 'Giornata '+p.giornata : 'Nessuna partita';}
  var h='<section class="nt-numeri" aria-labelledby="nt-numeri-titolo">' +
    '<h2 id="nt-numeri-titolo">Numeri del Campionato</h2><div class="nt-stat-griglia">';
  h+=box('Giornate giocate',fmt(s.giornateGiocate),
    s.giornateParziali+' giornate parziali',true);
  h+=box('Gol totali',fmt(s.golTotali),s.partiteGiocate+' partite disputate',true);
  h+=box('Gol a partita',fmt(s.golAPartita),'Media dei gol nei risultati',true);
  h+=box('Pareggi',fmt(s.pareggi),'Partite terminate in parità',true);
  h+=box('Miglior attacco',s.migliorAttacco?s.migliorAttacco.squadra:'—',
    s.migliorAttacco?s.migliorAttacco.gol+' gol segnati':'Nessun dato');
  h+=box('Miglior difesa',s.migliorDifesa?s.migliorDifesa.squadra:'—',
    s.migliorDifesa?s.migliorDifesa.golSubiti+' gol subiti':'Nessun dato');
  h+=box('Più vittorie consecutive',s.piuVittorieConsecutive?s.piuVittorieConsecutive.squadra:'—',
    s.piuVittorieConsecutive?s.piuVittorieConsecutive.numero+
      ' vittorie · Dalla giornata '+s.piuVittorieConsecutive.daGiornata+
      ' alla '+s.piuVittorieConsecutive.aGiornata:'Nessun dato');
  h+=box('Imbattibilità più lunga',s.imbattibilitaPiuLunga?s.imbattibilitaPiuLunga.squadra:'—',
    s.imbattibilitaPiuLunga?s.imbattibilitaPiuLunga.numero+
      ' partite · Dalla giornata '+s.imbattibilitaPiuLunga.daGiornata+
      ' alla '+s.imbattibilitaPiuLunga.aGiornata:'Nessun dato');
  h+=box('Partita con più gol',risultato(s.partitaPiuGol),
    s.partitaPiuGol?giornata(s.partitaPiuGol)+' · '+s.partitaPiuGol.golTotali+' gol':'Nessun dato');
  h+=box('Vittoria più larga',risultato(s.vittoriaPiuLarga),
    s.vittoriaPiuLarga?giornata(s.vittoriaPiuLarga)+' · Scarto di '+s.vittoriaPiuLarga.scarto+' gol':'Nessun dato');
  h+=box('Fantapunti più alti',s.fantapuntiMassimi?s.fantapuntiMassimi.squadra:'—',
    s.fantapuntiMassimi?fmt(s.fantapuntiMassimi.fantapunti)+' Fantapunti · '+
      giornata(s.fantapuntiMassimi)+' · '+s.fantapuntiMassimi.campo:'Nessun dato');
  h+=box('Fantapunti più bassi',s.fantapuntiMinimi?s.fantapuntiMinimi.squadra:'—',
    s.fantapuntiMinimi?fmt(s.fantapuntiMinimi.fantapunti)+' Fantapunti · '+
      giornata(s.fantapuntiMinimi)+' · '+s.fantapuntiMinimi.campo:'Nessun dato');
  h+=box('Imbattute in casa',s.imbattuteCasa.length?s.imbattuteCasa.join(', '):'Nessuna',
    'Almeno una partita in casa, zero sconfitte');
  h+=box('Imbattute in trasferta',s.imbattuteTrasferta.length?s.imbattuteTrasferta.join(', '):'Nessuna',
    'Almeno una partita fuori casa, zero sconfitte');
  return h+'</div></section>';
}
