"""Esporta solo le pagine native di prova. Non scrive nel sito o in ufficiale/src/sito."""
from pathlib import Path
import argparse,json,shutil,re
R=Path(__file__).resolve().parents[2]
FILES=['sondaggi62.js','conferenze.js','stagione.js','curva-os.js','curva-os.css','giro-di-boa.js','giro-di-boa.css','condividi.js','nomi.js','pillole.js','tv.js','offline.js','ospite.js','versioni.js','versioni.json','data.json','formazioni.json','toto-quote.json','push.js','notifiche-lette.js','cerca.js']
def esporta(site,out):
 out.mkdir(parents=True,exist_ok=True)
 for f in FILES:
  if (site/f).is_file():shutil.copyfile(site/f,out/f)
 for directory in ['girrr','stadio/girrr','formazioni','assets','riepiloghi']:
  # I file nativi restano quelli della copia preparata; nessuna UI del vecchio simulatore.
  if (site/directory).is_dir():shutil.copytree(site/directory,out/directory,dirs_exist_ok=True,ignore=shutil.ignore_patterns('voci','video'))
 for skin in ['girrr','stadio/girrr']:
  for f in (site/skin/'voci').glob('*.json'):
   (out/skin/'voci').mkdir(exist_ok=True);shutil.copyfile(f,out/skin/'voci'/f.name)
 shutil.copytree(R/'prove/v62/font',out/'font',dirs_exist_ok=True)
 for p in out.rglob('*.html'):

  rel=p.relative_to(out);prof=len(rel.parts)-1;prefix='../'*prof
  text=p.read_text()
  guard=f'<script src="{prefix}lab62.js"></script>'
  if re.search(r'<head(?:\s|>)',text,re.I):text=re.sub(r'<head([^>]*)>',lambda m:m.group(0)+guard,text,count=1,flags=re.I)
  else:text=re.sub(r'^(<!doctype[^>]*>)?',lambda m:m.group(0)+guard,text,count=1,flags=re.I)
  first=re.search(r'<script\b[^>]*>',text,re.I)
  if not first or 'lab62.js' not in first.group(0):raise ValueError('Protezione Lab non prima degli script: '+str(rel))
  text=re.sub(r'https://fonts.googleapis.com/css2[^\"<>]*',prefix+'font/originali.css',text)
  p.write_text(text)
 (out/'lab62.js').write_text((R/'rilascio/r62/lab62.js').read_text())
 (out/'sw.js').write_text("self.addEventListener('install',()=>self.skipWaiting());self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));self.addEventListener('fetch',e=>{if(new URL(e.request.url).hostname.endsWith('.supabase.co'))e.respondWith(new Response('Database reale disabilitato nel Lab',{status:403}))});\n")
 shutil.copytree(R/'prove/v62/fixture',out/'fixture',dirs_exist_ok=True)
 for n in (6,7):
  pdf=R/f'lab/giornale-62/g{n}/giornale.pdf'
  if pdf.exists():shutil.copyfile(pdf,out/f'riepiloghi/settimana-{n:02}.pdf')
 (out/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Anteprima integrata 6.2</title><a href="girrr/campo.html">Lega</a> · <a href="stadio/girrr/campo.html">Stadio</a>')
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('sito',type=Path);p.add_argument('--out',type=Path,default=R/'lab/integrata-62');a=p.parse_args();esporta(a.sito,a.out)
