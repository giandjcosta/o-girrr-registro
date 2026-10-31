"""Casi controllati per giorni parziali, record e sicurezza delle metriche."""
import json
import subprocess
from pathlib import Path
from collaudo_anteprima_53_browser import fixture
R=Path(__file__).resolve().parent.parent
js="""
const fs=require('fs'),vm=require('vm');
const c={window:{},console};vm.createContext(c);vm.runInContext(fs.readFileSync('lab/annuario.js','utf8'),c);
const D=JSON.parse(fs.readFileSync(0,'utf8'));
const x=c.window.OAnnuario.calcola(D);
if(x.completa||x.classifica!==null)throw Error('Titolo attribuito prima della chiusura');
if(x.giornate!==4)throw Error('Turno parziale conteggiato');
const pareggi=JSON.parse(JSON.stringify(D));pareggi.cal.lega.forEach(g=>g.m.forEach(m=>m[4]='0-0'));
if(c.window.OAnnuario.calcola(pareggi).scarto!==null)throw Error('Pareggio contato come vittoria');
const buco=JSON.parse(JSON.stringify(D));buco.cal.lega[1].m[0][4]='-';
if(c.window.OAnnuario.calcola(buco).giornate!==1)throw Error('Ignorata giornata incompleta');
console.log('PASS Annuario: turno parziale, stagione non conclusa, pareggi esclusi dalle vittorie, continuità');
"""
subprocess.run(['node','-e',js],input=json.dumps(fixture()),text=True,cwd=R,check=True)
