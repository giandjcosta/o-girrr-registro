// ChatGPT 17/11/2026: QA su una sola grafica evento, quattro pagine reali di Claude, 3 dimensioni.
 // node temi/prova_miami_diretto.cjs http://localhost:8768/
 // Richiede: server Python alla root del repository e Playwright/Chromium locali.
 // Non scrive dati: controlla solo DOM e layout.
const {chromium}=require('playwright');
(async()=>{
const root=process.argv[2]||'http://localhost:8768/';
const browser=await chromium.launch({headless:true});
let ko=0;const results=[];
try{
  for(const skin of ['girrr']){
    for(const id of ['index.html','tabellone.html','app.html#carriera','totogirrr.html?demo']){
      for(const width of [320,390,1440]){
        const p=await browser.newPage({viewport:{width,height:900},hasTouch:width<=390,isMobile:width<=390});
        let out={skin,page:id,width};try{
          const path='lab/integrata-62/'+skin+'/'+id;
          const url=new URL(path,root);
          await p.goto(url.toString(),{waitUntil:'domcontentloaded',timeout:20000});
          await p.waitForSelector('#miami-event-navigation',{timeout:8000});
          const info=await p.evaluate(()=>{
            const d=document.documentElement,nav=document.getElementById('miami-event-navigation');
            const link=document.querySelector('[data-miami-ui][rel=stylesheet]');
            const score=document.querySelectorAll('.miami-tabs a');
            return {installed:d.classList.contains('miami-ux'),nav:!!nav,css:!!link,
              tabs:score.length,scroll:d.scrollWidth,view:d.clientWidth,
              displayed:nav?getComputedStyle(nav).display:''};
          });
          out={...out,...info};
          out.ok=info.installed&&info.nav&&info.css&&info.tabs===4&&info.displayed!=='none'&&info.scroll<=info.view+3;
        }catch(e){out.ok=false;out.error=String(e).slice(0,240)}
        if(!out.ok)ko++;results.push(out);
        console.log((out.ok?'OK':'KO')+' '+skin+' '+id+' '+width+(out.error?' '+out.error:''));
        await p.close();
      }
    }
  }
}finally{await browser.close()}
console.log(JSON.stringify({total:results.length,failed:ko,failures:results.filter(x=>!x.ok)},null,2));
process.exitCode=ko?1:0;
})().catch(e=>{console.error(e);process.exitCode=1});
