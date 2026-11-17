// Fiducia del presidente in Carriera (iPhone 13): opacità massima del numero nascosto durante il giro e foto della sequenza.
const {chromium,devices}=require('playwright');
const URL=process.argv[2];const TAG=process.argv[3];
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();
 await p.goto(URL,{waitUntil:'domcontentloaded'});
 await p.evaluate(()=>{window.__max=0;window.__fine=null;(function f(){const n=document.querySelector('.trust-visual .trust-number');if(n){const o=parseFloat(getComputedStyle(n).opacity);if(o>window.__max)window.__max=o;const t=document.querySelector('.tab-fid');if(t)window.__val=t.textContent}requestAnimationFrame(f)})()});
 const fr=[];for(let i=0;i<30;i++){await p.waitForTimeout(100);const el=await p.$('.trust-visual');if(el&&i%3===0)fr.push(await el.screenshot({path:__dirname+`/fid/${TAG}-${String(i).padStart(2,'0')}.png`}))}
 console.log(TAG,'opacità massima del numero nascosto:',await p.evaluate(()=>window.__max),'valore finale dei cartellini:',await p.evaluate(()=>document.querySelector('.tab-fid')&&[...document.querySelectorAll('.tab-fid .fl')].map(f=>f.dataset.v).join('')));
 await b.close()})();
