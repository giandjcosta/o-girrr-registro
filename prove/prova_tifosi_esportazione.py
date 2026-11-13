"""Collauda la copia monofile effettivamente consegnata, separatamente dal server."""
from pathlib import Path
import json,os
from playwright.sync_api import sync_playwright,expect
R=Path(__file__).resolve().parents[1];result=[];OUT=Path(os.environ.get('TIFOSI_EXPORT_OUT',str(R/'qa_artifacts/tifosi-esportazione.json')))
def target(page,f,selector):
 try:f.locator(selector).wait_for(state='visible')
 except Exception:
  print('DIAGNOSI',page.url[-250:],flush=True)
  for fr in page.frames:
   print('FRAME',fr.url[:150],flush=True)
   if fr.parent_frame:
    print(fr.evaluate("({loc:window.__ptLocation?.href,base:document.baseURI,ready:document.readyState,status:document.getElementById('pt-status')?.textContent,section:document.getElementById('view')?.innerText?.slice(0,800),story:document.getElementById('pt-storia')?.outerHTML.slice(0,350),archive:document.getElementById('pt-archivio')?.outerHTML.slice(0,350)})"),flush=True)
    print(fr.locator('body').inner_text()[-1200:],flush=True)
  raise
with sync_playwright() as p:
 for name in os.environ.get('MOTORI','chromium,webkit,firefox').split(','):
  opts={'executable_path':os.environ['WEBKIT_PATH']} if name=='webkit' and os.environ.get('WEBKIT_PATH') else {}
  b=getattr(p,name).launch(**opts)
  for width in [int(x) for x in os.environ.get('LARGHEZZE','320,1280').split(',')]:
   page=b.new_page(viewport={'width':width,'height':900});page.set_default_timeout(25000);errors=[];writes=[]
   page.route('https://**',lambda r:r.abort())
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('request',lambda r:writes.append(r.url) if '.supabase.co/' in r.url or r.method not in ['GET','HEAD'] else None)
   page.goto((R/'consegna/revisione-girrr.html').as_uri(),wait_until='load');f=page.frame_locator('iframe')
   for skin,label in [('lega','Lega'),('stadio','Stadio')]:
    f.get_by_text('Apri '+label+' ›',exact=True).click();f.locator('#pt-home-story').wait_for();f.locator('#pt-home-story summary').click()
    expect(f.locator('#pt-home-story')).to_contain_text('2 incontri giocati')
    f.get_by_text('Rileggi la tua stagione ›',exact=True).click();target(page,f,'#pt-storia')
    expect(f.locator('[data-pt-day]')).to_have_count(7)
    f.locator('#pt-team').select_option('stif dc');expect(f.locator('[data-pt-day="7"]')).to_contain_text('1 incontro giocato')
    f.get_by_text('Mappa',exact=True).click();f.get_by_text('Apri '+label+' ›',exact=True).click();f.locator('a[href="albo.html"]').first.click();f.locator('[data-at=derby]').click();f.locator('#pt-derby-access').click();f.locator('#pt-derby').wait_for()
    f.locator('[data-pt-comp=cup]').click();expect(f.locator('#pt-derby tbody tr')).to_have_count(4)
    f.get_by_text('Mappa',exact=True).click();f.locator('a[href="'+skin+'/app.html?sezione=mvp#sport"]').click();f.locator('[data-pt-vote]').first.click();expect(f.locator('[data-pt-withdraw]')).to_be_visible()
    f.get_by_text('Il voto nella Curva ›',exact=True).click();expect(f.locator('[data-pt-withdraw]')).to_be_visible();f.locator('[data-pt-withdraw]').click()
    f.get_by_text('Archivio del premio ›',exact=True).click();target(page,f,'#pt-archivio')
    assert page.frames[-1].evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    f.get_by_text('Prima',exact=True).click();expect(f.locator('.pt-box')).to_have_count(0)
    page.wait_for_timeout(100)
    assert not errors,(name,width,skin,errors)
    assert not writes,(name,width,skin,writes)
    result.append(f'{name}/{width}/{skin}: PASS');print(result[-1],flush=True)
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    f.get_by_text('Mappa',exact=True).click()
   page.close()
  b.close()
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
