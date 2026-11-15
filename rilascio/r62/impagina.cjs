// Reimpaginazione in tre A4, senza FIT_JS, riduzioni dei caratteri o scale.
// Conserva i blocchi editoriali; elimina solo le metriche social inventate dal vecchio renderer.
module.exports=async function(p){return p.evaluate(()=>{
 const pagine=[...document.querySelectorAll('.pg')],stile=document.querySelector('style').textContent;
 const mast=pagine[0].querySelector('.mast').outerHTML,bar=pagine[0].querySelector('.bar').outerHTML;
 const blocchi=[];
 for(const pg of pagine)for(const e of [...pg.children]){
  if(e.matches('.bar,.mast,.foot'))continue;
  if(e.matches('.g2')){for(const col of e.children)for(const nodo of [...col.children])blocchi.push(nodo)}
  else if(e.matches('.cols')){for(const nodo of [...e.children])blocchi.push(nodo)}else blocchi.push(e);
 }
 for(const nodo of blocchi){
  const social=nodo.querySelector('.social');if(social){const testo=social.querySelector('.pt').innerHTML,nome=social.querySelector('.pn b').textContent;social.innerHTML='<p class="pt">'+testo+'</p><p class="nt">Dalla Curva · '+nome+'</p>'}
 }
 // L'undici rimane con gli stessi nomi, ruoli e voti, disposto in una riga di lettura.
 for(const nodo of blocchi){const fig=nodo.querySelector('.fig');if(fig){const righe=[...fig.querySelectorAll('svg text')].map(e=>e.textContent);fig.innerHTML='<p>'+righe.join(' · ')+'</p>'+fig.querySelector('p').outerHTML}}
 for(const nodo of blocchi){const w=document.createTreeWalker(nodo,NodeFilter.SHOW_TEXT);let t;while(t=w.nextNode())t.textContent=t.textContent.replace(/(·\s*)(\p{Ll})/gu,(_,a,b)=>a+b.toUpperCase())}
 for(const nodo of blocchi){if(nodo.querySelector('.pal')){const w=document.createTreeWalker(nodo,NodeFilter.SHOW_TEXT);let t;while(t=w.nextNode())t.textContent=t.textContent.replace(/\bpunti\b/g,'Fantapunti')}}
 const contenuto=blocchi.map(e=>e.outerHTML).join('');
 document.head.innerHTML='<meta charset="utf-8"><style>'+stile+`\n.pg{overflow:visible;padding:4mm 8mm 6mm}.pg:before{display:none}.flow{column-count:6;column-gap:5mm;column-fill:balance;width:592mm}.flow>*{break-inside:avoid}.flow .tab,.flow .bufala{break-inside:auto}.flow tr{break-inside:avoid}.flow h2,.flow h3{break-after:avoid}.flow .tab{margin-top:2mm}.flow .box{margin-bottom:2mm}.flow .g2{display:block}.flow .fig{width:auto!important}.flow .fig p{font-size:7.2pt}.flow .spb{gap:1mm;flex-wrap:wrap}.flow .spb img{height:10mm}.flow .social{padding:2mm}.flow .tit{overflow-wrap:anywhere}.flow .cols{gap:2mm}.flow .big{font-size:62pt}.flow .foot{display:none}.finestra{overflow:hidden;width:194mm}.foot{bottom:3mm}.mast{padding:0;border-bottom:.5mm solid var(--rule)}.bar{padding-bottom:.5mm}.flow .gm{grid-template-columns:1fr 5mm 1fr}.flow .fig svg{display:none}.flow table,.flow tbody{display:block}.flow tr{display:block;padding:1mm 0;border-bottom:.2mm solid var(--soft)}.flow th,.flow td{display:inline!important;width:auto!important;padding:0 .6mm;border:0}.flow .pgl .sq i{display:inline;margin:0 .5mm}.flow .pgl .cm{display:block!important}.flow .tab h2{line-height:1.05}.flow .nt{line-height:1.2}.flow .som{line-height:1.05}.flow .txt,.flow .nt,.flow .pt,.flow .pal,.flow .cm,.flow .bufala p,.flow .taglio,.flow .bt{line-height:1.05}.flow .occ{margin-top:1mm}.flow .tab{margin-top:1mm}.flow .box{margin-bottom:1mm}.flow tr{padding:.4mm 0}.flow .pal li{padding:.5mm 0}\n</style>`;
 document.body.innerHTML='<div id="misura" style="width:194mm"><div class="flow">'+contenuto+'</div></div>';
 const flow=document.querySelector('.flow');
 // 6 colonne da 94,5 mm, con cinque intervalli da 5 mm. Passo pagina: 199 mm.
 flow.style.width='592mm';
 const altezza=flow.getBoundingClientRect().height;
 document.body.innerHTML=Array.from({length:3},(_,i)=>'<section class="pg">'+bar+mast+'<div class="finestra" style="height:'+altezza+'px"><div class="flow" style="margin-left:-'+i*199+'mm">'+contenuto+'</div></div><div class="foot"><span>O Giornale del Girrr · Prova 6.2</span><span>Pag. '+(i+1)+' di 3</span></div></section>').join('');
 return {altezza,limite:document.querySelector('.foot').getBoundingClientRect().top-document.querySelector('.finestra').getBoundingClientRect().top,caratteri:blocchi.reduce((n,e)=>n+e.textContent.length,0)};
})};
