#!/usr/bin/env node
/* Home conservativa: prova DOM statica e ruoli, senza connessioni al sito vero. */
const fs=require('node:fs'),assert=require('node:assert/strict');
for(const skin of ['lega','stadio']){
 const src='lab/prova-home-integrata-'+skin+'.html',h=fs.readFileSync(src,'utf8');
 const must=[
   '<header class="hero">','<div class="lg-leghe">','<section class="big"',
   '<section class="strip"','<section class="cards">',
   '<h2>Spogliatoio</h2>','<h2>Girrr Sport', '<h2>Tabellone</h2>',
   '<h2>Albo d\'oro','<h2>Carriera','Totogirrr','id="cvw"',
   '<section class="mini"','>Statistiche</b>','Gentilmente offerto da',
   'id="og-today"','id="og-team"','id="og-items"','id="og-news"',
   'class="mini og-menu-notif"','prova-esperienza-'+skin+'.html#notifiche',
   'home-integrata.js'
 ];
 for(const x of must)assert(h.includes(x),skin+': manca '+x);
 assert(h.indexOf('id="og-today"')<h.indexOf('<div class="lg-leghe">'),skin+': Oggi deve essere prima dei contenuti esistenti');
 assert(h.indexOf('id="og-today"')<h.indexOf('<section class="big"'),skin+': Oggi precede il Giornale');
 assert(!h.includes('Automazioni e controlli finali completati'),skin+': i controlli non devono comparire in Home');
 assert(!h.includes('Giornata conclusa'),skin+': non dichiarare una giornata conclusa senza conferme');
 assert.equal((h.match(/<section class="cards">/g)||[]).length,1,skin+': elenco originale conservato');
 console.log('PASS Home integrata',skin,'struttura originale conservata, Oggi per primo, Notifiche separate, niente avvisi tecnici');
}
