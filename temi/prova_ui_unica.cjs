/* ChatGPT, 17/11/2026 — QA della grafica evento UNICA.
   Non eseguire se il Lab è in aggiornamento; dati veri di sola lettura, nessun login/scrittura.
   Uso: python3 -m http.server 8770 (dalla root), poi node temi/prova_ui_unica.cjs
   Richiede Playwright e Chromium nell'ambiente di esecuzione.
   QUESTO TEST NON È STATO ESEGUITO NEL BROWSER SUL LAB: è un piano QA ripetibile. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const base = process.env.LAB_URL || 'http://127.0.0.1:8770/lab/integrata-62/';
const origins=['girrr/index.html','stadio/girrr/index.html'];
const widths=[320,375,390,768,1280,1920];
(async()=>{
 const browser=await chromium.launch({headless:true});
 let cases=0;
 try {
  for(const width of widths) {
   const ctx=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
   const snapshots=[];
   for (const origin of origins) {
    const page=await ctx.newPage();
    const errs=[];page.on('pageerror',e=>errs.push(String(e)));
    const u=new URL(origin+'?ospite=1&evento=notte-tropicale',base);
    const r=await page.goto(u.href,{waitUntil:'domcontentloaded'});
    assert.equal(r.status(),200);
    await page.locator('html[data-event-theme="notte-tropicale"]').waitFor();
    await page.waitForTimeout(300);
    const x=await page.evaluate(()=>({
      accent:getComputedStyle(document.body).getPropertyValue('--acc').trim(),
      hi:getComputedStyle(document.body).getPropertyValue('--hi').trim(),
      linkAccent:getComputedStyle(document.body).getPropertyValue('--v53-accent').trim(),
      headline:getComputedStyle(document.querySelector('header.hero h1')).fontFamily,
      scroll:document.documentElement.scrollWidth,
      width:document.documentElement.clientWidth,
      cards:getComputedStyle(document.querySelector('.cards')).gridTemplateColumns,
      logo:getComputedStyle(document.querySelector('header.hero>a img')).display
    }));
    assert.ok(x.scroll <= x.width+1, 'Overflow '+origin+' '+width+': '+JSON.stringify(x));
    assert.equal(x.accent,'#ff4bac');
    assert.equal(x.hi,'#ffb875');
    assert.equal(x.logo,'none');
    assert.deepEqual(errs,[]);
    snapshots.push(x);
    cases++;
    await page.close();
   }
   assert.equal(snapshots[0].accent,snapshots[1].accent);
   assert.equal(snapshots[0].hi,snapshots[1].hi);
   assert.equal(snapshots[0].linkAccent,snapshots[1].linkAccent);
   cases+=3;
   await ctx.close();
  }
  console.log('PASS: '+cases+' casi/asserzioni completati; GUI delle due origini con stessa identità evento');
 } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
