/* Post nuovi della 5.0, mostrati dentro il feed vero della Curva (solo in anteprima: non vengono salvati da nessuna parte). */
window.ANT_POSTS=function(){var n=Date.now(),m=60000,N=window.NOV||{};
  function r(a,b){return N.riv&&N.riv.filter(function(o){return (o.a===a&&o.b===b)||(o.a===b&&o.b===a)})[0]}
  var P=[
   {h:'girrr_sport',m:6,body:'SFIDA DECISIVA\nA gennaio, quando due squadre si giocano il titolo, la Curva se ne accorge. Apo contro Riky: la finalissima della Lega. #GirrrSport #Derby'},
   {h:'lega_ofantagirrr',m:34,body:'Novità dall\'Albo d\'oro: arriva l\'Era dei Titani, con i campionati 2016/17, 2017/18 e 2018/19: Mario, Apo e Urba tornano nella storia della Lega. #AlboDoro'},
   {h:'girrr_sport',m:71,body:'RIVALITÀ\nSono anni che si incontrano in alto, e quando succede la sfida pesa. Un gradino sotto il Derby, ma non troppo. #GirrrSport'},
   {h:'giornale_girrr',m:130,body:'Il Derby delle Due Finali e il Derby di Andata e Ritorno entrano nell\'Albo d\'oro: ognuno con la sua storia. #Derby'}
  ];
  return P.map(function(p,i){return {id:900001+i,ts:n-p.m*m,body:p.body,h:p.h,hi:null,ant:1}})};
