/* 17/11/2026: QA browser locale per i prototipi Vice City.
 * Esecuzione: node temi/prova_browser.cjs
 * Richiede playwright già installato e browser Chromium disponibili; non scarica nulla.
 * NON usa dati reali né servizi esterni.
 */
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const assert = require('node:assert/strict');
let chromium;
try { ({chromium} = require('playwright')); }
catch (error) { console.error('NON ESEGUITO: playwright non installato.'); process.exit(2); }
const files = ['index.html','anteprima-home.html','anteprima-tabellone.html','anteprima-carriera.html','anteprima-totogirrr.html'];
const sizes = [{width:320,height:700},{width:390,height:844},{width:768,height:1024},{width:1280,height:800},{width:1920,height:1080},{width:2560,height:1440}];
(async () => {
 const browser = await chromium.launch({headless:true});
 let count=0;
 try {
  for (const file of files) for (const viewport of sizes) {
   const page = await browser.newPage({viewport, reducedMotion:'reduce'});
   const errors=[];
   page.on('pageerror', error => errors.push(error.message));
   await page.goto(pathToFileURL(path.join(__dirname,file)).href,{waitUntil:'load'});
   await page.evaluate(() => document.fonts.ready);
   const result = await page.evaluate(() => ({
    overflow: document.documentElement.scrollWidth > innerWidth + 1,
    skin: document.documentElement.getAttribute('data-skin'),
    event: document.documentElement.getAttribute('data-event-theme'),
    title: document.title
   }));
   assert.equal(result.overflow,false,`${file} overflow a ${viewport.width}px`);
   if(file !== 'index.html') {
    assert.equal(result.skin,'girrr',`${file} skin iniziale`);
    assert.equal(result.event,'vice-city',`${file} evento iniziale`);
    // 17/11/2026: verifica che il tema possa spegnersi e riaccendersi senza mutare la skin.
    const toggle = await page.evaluate(() => {
      const before = document.documentElement.getAttribute('data-skin');
      if (!window.OGirrrTheme) return {error:'API assente'};
      window.OGirrrTheme.clearPreview();
      const off = document.documentElement.getAttribute('data-event-theme');
      window.OGirrrTheme.preview('vice-city');
      return {before, after:document.documentElement.getAttribute('data-skin'), off,
        on:document.documentElement.getAttribute('data-event-theme')};
    });
    assert.equal(toggle.error,undefined,`${file} API`);
    assert.equal(toggle.off,null,`${file} spegnimento`);
    assert.equal(toggle.on,'vice-city',`${file} riaccensione`);
    assert.equal(toggle.after,toggle.before,`${file} skin preservata`);
   } else {
    assert.equal(await page.locator('a[href="anteprima-home.html"]').count(),1,'Hub: Home raggiungibile');
    assert.equal(await page.locator('a[href="anteprima-tabellone.html"]').count(),1,'Hub: Tabellone raggiungibile');
   }
   assert.deepEqual(errors,[],`${file} JS errors`);
   // Controllo di base: link senza destinazione e pulsanti senza nome accessibile.
   const unnamed = await page.evaluate(() => [...document.querySelectorAll('button,a')]
     .filter(el => !((el.getAttribute('aria-label')||el.innerText||el.textContent||'').trim()))
     .map(el => el.outerHTML.slice(0,120)));
   assert.deepEqual(unnamed,[],`${file} controlli senza nome`);
   console.log('OK',file,viewport.width+'px');
   count++;
   await page.close();
  }
  console.log('PASS:',count,'combinazioni Chromium');
 } finally { await browser.close(); }
})().catch(e => { console.error('FAIL:',e.stack);process.exitCode=1; });
