/* 17/11/2026: test isolato del motore temi, senza dipendenze o rete. Eseguire: node temi/prova_theme_engine.cjs */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname,'theme-engine.js'),'utf8');
const attrs = new Map([['data-skin','stadio']]);
const events=[];
const root = {
 setAttribute(k,v){attrs.set(k,v)},
 removeAttribute(k){attrs.delete(k)},
 getAttribute(k){return attrs.get(k)||null}
};
const win = {dispatchEvent(ev){events.push(ev.detail.id)}};
class CustomEvent {constructor(type,opts){this.type=type;this.detail=opts.detail}}
vm.runInNewContext(source,{window:win,document:{documentElement:root},CustomEvent,Date});
const engine=win.OGirrrTheme;
assert.equal(Object.isFrozen(engine),true);
assert.equal(engine.themes['vice-city'].name,'Vice City Edition');
engine.preview('vice-city');
assert.equal(root.getAttribute('data-event-theme'),'vice-city');
assert.equal(root.getAttribute('data-skin'),'stadio');
assert.throws(()=>engine.preview('non-esiste'),/Tema sconosciuto/);
assert.equal(root.getAttribute('data-event-theme'),'vice-city');
engine.clearPreview();
assert.equal(root.getAttribute('data-event-theme'),null);
assert.equal(root.getAttribute('data-skin'),'stadio');
assert.equal(engine.activateScheduled(new Date('2026-11-17T23:59:59+01:00')),null);
assert.equal(engine.activateScheduled(new Date('2026-11-18T00:00:00+01:00')),'vice-city');
assert.equal(engine.activateScheduled(new Date('2026-11-20T23:59:59+01:00')),'vice-city');
assert.equal(engine.activateScheduled(new Date('2026-11-21T00:00:00+01:00')),null);
assert.equal(root.getAttribute('data-skin'),'stadio');
assert.deepEqual(events,['vice-city',null,null,'vice-city','vice-city',null]);
console.log('PASS: 12 assert / preview, rollback, skin, schedule, invalid theme');
