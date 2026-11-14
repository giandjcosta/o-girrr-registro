// Verifica la grafica effettivamente disegnata: centratura dei glifi e palette separate dalle bande.
const assert=require('assert/strict'),fs=require('fs'),path=require('path'),{devices}=require('playwright');
const {browser}=require('./browser_certificato');
const M=process.env.MOTORE||'chromium',B=process.env.REGISTRO||'http://127.0.0.1:8890/o-girrr-registro/',F=process.env.FOTO||'/tmp/boa-colori';
const schermi=[['iPhone320',{...devices['iPhone SE'],viewport:{width:320,height:568}}],...['iPhone SE','iPhone 15 Pro','iPhone 15 Pro Max','Galaxy S8','Pixel 7','Galaxy S9+','iPad Mini','iPad (gen 7) landscape','iPad Pro 11','Galaxy Tab S4','Galaxy Tab S4 landscape'].map(n=>[n,devices[n]]),...[1280,1920,2560].map(w=>['PC'+w,{viewport:{width:w,height:1080}}]),['TV',{viewport:{width:1920,height:1080},deviceScaleFactor:2}]];
(async()=>{const br=await browser(M),record=[];fs.mkdirSync(F,{recursive:true});
 for(const [nome,o] of schermi){const c=await br.newContext({...o,serviceWorkers:'block'});await c.addInitScript(()=>{
  window.__misuraInchiostro=(cv,x,y,r)=>{const ctx=cv.getContext('2d'),left=Math.floor(x-r),top=Math.floor(y-r),w=Math.ceil(2*r),data=ctx.getImageData(left,top,w,w).data;let xmin=Infinity,xmax=-Infinity,ymin=Infinity,ymax=-Infinity,n=0;
   for(let j=0;j<w;j++)for(let i=0;i<w;i++){const xx=left+i+.5,yy=top+j+.5;if(Math.hypot(xx-x,yy-y)>r*.82)continue;const k=4*(j*w+i);if(Math.abs(data[k]-17)+Math.abs(data[k+1]-36)+Math.abs(data[k+2]-58)<18){xmin=Math.min(xmin,xx);xmax=Math.max(xmax,xx);ymin=Math.min(ymin,yy);ymax=Math.max(ymax,yy);n++;}}
   return {n,dx:(xmin+xmax)/2-x,dy:(ymin+ymax)/2-y};};
 });const p=await c.newPage(),errori=[];p.on('pageerror',e=>errori.push(e.message));
 try{await p.goto(B+'lab/giro-di-boa-602/');await p.waitForSelector('[data-pronto="1"]');await p.evaluate(()=>document.fonts.ready);
  for(const skin of ['lega','stadio']){
   await p.evaluate(v=>document.documentElement.dataset.skin=v,skin);await p.selectOption('[data-gb-ambito]','squadra');await p.selectOption('[data-gb-squadra]','Oranje VC');
   await p.click('[data-gb-vista="0"]');assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Scorrimento orizzontale');
   const st=await p.locator('.gb-kpi>div').first().evaluate(e=>{const s=getComputedStyle(e);return {bordo:s.borderLeftColor,w:parseFloat(s.borderLeftWidth)};});assert.equal(st.bordo,skin==='lega'?'rgb(214, 40, 57)':'rgb(255, 209, 102)');assert(Math.abs(st.w-(skin==='lega'?8:6))<.5);
   const titolo=await p.locator('.gb-riquadro h4').first().evaluate(e=>getComputedStyle(e).color);assert.equal(titolo,skin==='lega'?'rgb(166, 220, 255)':'rgb(180, 238, 226)');assert.notEqual(titolo,st.bordo);
   // Raster del DOM, non il riquadro di layout del testo: V, N e P devono essere centrate visivamente.
   if(nome==='iPhone320')for(let i=0;i<3;i++){
    const png=await p.locator('.gb-legenda span').nth(i).screenshot();
    const pos=await p.evaluate(async data=>{const im=new Image();im.src='data:image/png;base64,'+data;await im.decode();const cv=document.createElement('canvas');cv.width=im.naturalWidth;cv.height=im.naturalHeight;cv.getContext('2d').drawImage(im,0,0);return __misuraInchiostro(cv,cv.width/2,cv.height/2,cv.width/2);},png.toString('base64'));
    assert(pos.n>3&&Math.abs(pos.dx)<=1.2*o.deviceScaleFactor&&Math.abs(pos.dy)<=1.2*o.deviceScaleFactor,'Lettera nel DOM decentrata: '+JSON.stringify(pos));
   }
   await p.click('[data-gb-vista="1"]');const voci=await p.locator('.gb-voce>small').evaluateAll(es=>es.map(e=>getComputedStyle(e).color));assert.equal(voci[0],skin==='lega'?'rgb(166, 220, 255)':'rgb(197, 221, 255)');assert.equal(voci[1],'rgb(162, 237, 205)');assert(voci.every(x=>x!==st.bordo));
   await p.selectOption('[data-gb-ambito]','lega');await p.click('[data-gb-vista="0"]');assert.equal(await p.locator('.gb-classifica>div').count(),10);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   if(nome==='iPhone320'){
    const res=await p.evaluate(async stadio=>{const j=await GirrrBoa.carica(new URL('esempio.json',location.href).href),out=[];
     for(const ambito of ['squadra','lega']){const a=await GirrrBoa.album(j,{squadra:'Oranje VC',ambito,stadio});const cv=a[0].canvas;
      // Tre taglie reali: risultati, legenda e classifica. La legenda garantisce tutte le lettere V/N/P.
      const centri=ambito==='squadra'?[[84,933,23],[276,933,23],[468,933,23],[80,1046,16],[390,1046,16],[700,1046,16]]:[[867,509,13],[900,509,13],[933,509,13],[80,1216,16],[390,1216,16],[700,1216,16]];
      out.push(...centri.map(([x,y,r])=>__misuraInchiostro(cv,x,y,r)));a.forEach(f=>URL.revokeObjectURL(f.url));
     }return out;},skin==='stadio');
    for(const r of res)assert(r.n>3&&Math.abs(r.dx)<=1&&Math.abs(r.dy)<=1,'Lettera nella foto decentrata: '+JSON.stringify(r));
   }
   record.push({schermo:nome,grafica:skin,problemi:[]});
  }assert.deepEqual(errori,[]);console.log('OK '+M+' '+nome);
 }catch(e){record.push({schermo:nome,problemi:[e.message,...errori]});console.log('KO '+M+' '+nome+': '+e.message);}
 await c.close();}
 await br.close();const problemi=record.filter(r=>r.problemi.length).length;fs.writeFileSync(path.join(F,'grafica-'+M+'.json'),JSON.stringify({motore:M,visite:record.filter(r=>r.grafica).length,problemi,record},null,2));console.log(M+': '+problemi+' problemi');process.exitCode=problemi?1:0;
})().catch(e=>{console.error(e);process.exitCode=1});
