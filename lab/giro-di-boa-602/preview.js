/* Un visualizzatore del JSON, senza un secondo calcolo nel Lab. */
(function () {
  const b=document.getElementById('grafica');
  function grafica(stadio) { document.documentElement.dataset.skin=stadio?'stadio':'lega';b.setAttribute('aria-checked',String(stadio));b.textContent=stadio?'Grafica: Stadio · Passa a Lega':'Grafica: Lega · Passa a Stadio';try{localStorage.setItem('girrr-boa-grafica',stadio?'stadio':'lega');}catch(e){} }
  b.onclick=()=>grafica(document.documentElement.dataset.skin!=='stadio');
  let skin;try{skin=localStorage.getItem('girrr-boa-grafica');}catch(e){}grafica(skin==='stadio');
  (async function () {
    let fonte=new URL('esempio.json',location.href).href;
    try {
      const root=new URL('/o-fant-a-girrr/',location.href).href,r=await fetch(root+'versioni.json',{cache:'no-cache'});
      if(r.ok){const j=await r.json(),v=String(j.versioni?.[0]?.v||'').split('.').map(Number);if((v[0]||0)>6||v[0]===6&&((v[1]||0)>0||(v[2]||0)>=2))fonte=root;}
    }catch(e){}
    await GirrrBoa.monta(document.getElementById('scheda'),'Oranje VC',fonte);
  })();
})();
