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
const files = ['anteprima-home.html','anteprima-tabellone.html','anteprima-carriera.html','anteprima-totogirrr.html'];
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
   assert.equal(result.skin,'girrr',`${file} skin iniziale`);
   assert.equal(result.event,'vice-city',`${file} evento iniziale`);
   assert.deepEqual(errors,[],`${file} JS errors`);
   console.log('OK',file,viewport.width+'px');
   count++;
   await page.close();
  }
  console.log('PASS:',count,'combinazioni Chromium');
 } finally { await browser.close(); }
})().catch(e => { console.error('FAIL:',e.stack);process.exitCode=1; });
