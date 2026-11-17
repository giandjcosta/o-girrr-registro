// O Girrr · Home V3 — QA Chromium locale, 17/11/2026
// Richiede Playwright installato nell'ambiente locale. NESSUN deploy o database.
// Uso: (nella root del repository) python3 -m http.server 8768
// In un altro terminale: node temi/prova_home_v3.cjs http://127.0.0.1:8768/temi/
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
(async () => {
  const base = process.argv[2] || 'http://127.0.0.1:8768/temi/';
  const output = process.env.O_GIRRR_SCREEN_DIR || '/tmp/ogirrr-home-v3-screens';
  fs.mkdirSync(output, {recursive:true});
  const browser = await chromium.launch({headless:true});
  let count = 0;
  try {
    for (const width of [320,375,390,768,1280,1920]) {
      const context = await browser.newContext({viewport:{width,height:Math.min(1000, Math.round(width*1.6))},deviceScaleFactor:1,reducedMotion:'reduce'});
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      const response = await page.goto(base + 'anteprima-home-v3.html', {waitUntil:'domcontentloaded'});
      assert.equal(response.status(),200,`HTTP ${width}`);
      count++;
      await page.locator('.tabs a').first().waitFor({state:'visible'});
      for (const name of ['Home','Tabellone','Carriera','Totogirrr']) {
        assert.equal(await page.getByRole('navigation',{name:'Sezioni principali demo'}).getByRole('link',{name}).count(),1,`tab ${name} @${width}`);
        count++;
      }
      const measured = await page.evaluate(() => ({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,theme:document.documentElement.dataset.eventTheme}));
      assert.ok(measured.scroll <= measured.client+1,`overflow ${width}: ${JSON.stringify(measured)}`);count++;
      assert.equal(measured.theme,'vice-city');count++;
      assert.equal(await page.getByText('PROTOTIPO VISIVO · DATI DIMOSTRATIVI').count(),1);count++;
      const toggle=page.getByRole('button',{name:'Attiva la modalità notturna'});
      await toggle.click();
      assert.equal(await page.locator('html').getAttribute('data-night'),'true');count++;
      await page.getByRole('button',{name:'Torna al tramonto'}).click();
      assert.equal(await page.locator('html').getAttribute('data-night'),'false');count++;
      assert.deepEqual(errors,[],`JavaScript @${width}`);count++;
      await page.screenshot({path:path.join(output,`home-v3-${width}.png`),fullPage:true,animations:'disabled'});
      await context.close();
    }
    console.log('Home V3: '+count+' asserzioni superate. Screenshot: '+output);
  } finally {await browser.close();}
})().catch(e => {console.error(e);process.exit(1)});
