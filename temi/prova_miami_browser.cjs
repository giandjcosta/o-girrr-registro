// ChatGPT 17/11/2026. Esegue il browser QA della UI VERA (non mockup).
// Avvio: dalla root del Registro: python3 -m http.server 8768
// In altra console: node temi/prova_miami_browser.cjs http://localhost:8768/temi/
// Richiede Playwright + Chromium, non esegue scritture, deploy o chiamate a strumenti a pagamento.
const {chromium}=require('playwright');
(async()=>{
const base=process.argv[2]||'http://localhost:8768/temi/';
const browser=await chromium.launch({headless:true});
const cases=[];const sizes=[{w:320,h:700},{w:390,h:844},{w:1440,h:900}];
try{
for(const screen of ['home','tabellone','carriera','totogirrr'])for(const size of sizes){
 const context=await browser.newContext({viewport:{width:size.w,height:size.h},hasTouch:size.w<=390,isMobile:size.w<=390});
 const page=await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const url=new URL('miami-prova.html',base);
 url.search=new URLSearchParams({screen,view:'desktop'}).toString();
 let ok=false;let state={};let failure='';
 try{
   await page.goto(url.toString(),{waitUntil:'domcontentloaded',timeout:15000});
   await page.waitForFunction(()=>{let f=document.getElementById('stage');return f&&f.contentDocument&&f.contentDocument.documentElement.classList.contains('miami-ux')},null,{timeout:10000});
   state=await page.evaluate(()=>{
     const f=document.getElementById('stage'),d=f.contentDocument,root=d.documentElement;
     const nav=d.getElementById('miami-event-navigation');
     const css=d.getElementById('miami-ui-live-css');
     const navLinks=nav?[...nav.querySelectorAll('a')]:[];
     const selected=navLinks.find(x=>x.getAttribute('aria-current')==='page');
     const box=nav&&d.defaultView.getComputedStyle(nav).getPropertyValue('display');
     const docWidth=d.documentElement.scrollWidth,viewWidth=d.documentElement.clientWidth;
     return {css:!!css,activated:root.classList.contains('miami-ux'),links:navLinks.length,
       selected:selected?.dataset.miamiPage||null,navDisplay:box,docWidth,viewWidth,
       path:f.contentWindow.location.pathname};
   });
   ok=state.css&&state.activated&&state.links===4&&state.selected===screen&&state.docWidth<=state.viewWidth+3;
 }catch(e){failure=e.message}
 cases.push({screen,viewport:size.w,ok,error:failure,errors:errors.slice(0,3),...state});
 console.log((ok?'OK':'KO')+' '+screen+' '+size.w+' '+(failure||''));
 await context.close();
}
}finally{await browser.close()}
const failures=cases.filter(x=>!x.ok);
console.log(JSON.stringify({checked:cases.length,passed:cases.length-failures.length,failed:failures.length,failures},null,2));
process.exitCode=failures.length?1:0;
})().catch(e=>{console.error(e);process.exitCode=1});
