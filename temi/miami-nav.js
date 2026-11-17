/* ChatGPT · 17 novembre 2026 · Miami Nights / navigation add-on.
   Monta una barra di navigazione evento sulle QUATTRO pagine vere del Lab sperimentale.
   Non modifica comportamenti, API, dati, skin permanenti né loader Claude. */
(function(){
'use strict';
function mount(){
  if(document.getElementById('miami-event-navigation'))return;
  var root=document.documentElement;
  root.classList.add('miami-ux');
  var path=location.pathname;
  var screen=/tabellone\.html$/.test(path)?'tabellone':/app\.html$/.test(path)?'carriera':/totogirrr\.html$/.test(path)?'totogirrr':'home';
  var nav=document.createElement('section');
  nav.className='miami-event-head';nav.id='miami-event-navigation';
  nav.setAttribute('aria-label','Navigazione evento Miami Nights');
  var brand=document.createElement('div');brand.className='miami-brand';
  var symbol=document.createElement('span');symbol.className='miami-mark';symbol.setAttribute('aria-hidden','true');
  var title=document.createElement('span');
  title.innerHTML='<strong class="miami-title">O GIRRR</strong><small class="miami-eyebrow">SPECIAL EDITION · PROVA LAB</small>';
  brand.append(symbol,title);
  var cursive=document.createElement('span');cursive.className='miami-event-script';cursive.textContent='Miami Nights';
  var tabs=document.createElement('nav');tabs.className='miami-tabs';
  tabs.setAttribute('aria-label','Sezioni O Girrr');
  var paths=[
    ['home','⌂','Home','index.html'],
    ['tabellone','♜','Tabellone','tabellone.html'],
    ['carriera','▥','Carriera','app.html#carriera'],
    ['totogirrr','◇','Totogirrr','totogirrr.html?demo']
  ];
  for(var i=0;i<paths.length;i++){
    var p=paths[i],a=document.createElement('a'),ic=document.createElement('span'),nm=document.createElement('span');
    a.href=p[3];a.dataset.miamiPage=p[0];ic.className='miami-tab-icon';ic.textContent=p[1];ic.setAttribute('aria-hidden','true');nm.textContent=p[2];
    if(p[0]===screen)a.setAttribute('aria-current','page');
    a.append(ic,nm);tabs.appendChild(a);
  }
  nav.append(brand,cursive,tabs);
  document.body.insertBefore(nav,document.body.firstChild);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount,{once:true});else mount();
})();
