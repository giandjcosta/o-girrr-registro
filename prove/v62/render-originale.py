import importlib.util,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
w=Path(sys.argv[1]);sys.path.insert(0,str(w/'scripts'));import pdf_giornale as g
import mvp_giornale62 as mg
integra=mg.integra;mg.integra=lambda t,d,n:t
base,n=g.costruisci(json.loads((w/'testi.json').read_text()));mg.integra=integra
h,n=g.costruisci(json.loads((w/'testi.json').read_text()))
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page();page.route('**/*',lambda r:r.abort());page.set_content(base);page.emulate_media(media='print');fit_base=page.evaluate(g.FIT_JS);page.set_content(h);fit=page.evaluate(g.FIT_JS)
 assert [(f['livello'],f['scala']) for f in fit]==[(f['livello'],f['scala']) for f in fit_base],('La nuova frase cambia i caratteri',fit_base,fit)
 assert len(fit)==4 and all(x['ci_sta'] for x in fit),fit
 page.pdf(path=str(w/'giornale.pdf'),prefer_css_page_size=True,print_background=True);(w/'giornale.html').write_text(page.content())
 for i in range(4):page.locator('.pg').nth(i).screenshot(path=str(w/f'pagina-{i+1}.png'))
 (w/'esito.json').write_text(json.dumps({'giornata':n,'pagine':4,'renderer':'originale','fit':fit,'baseline':fit_base,'fontVariati':False},indent=2));b.close()
import fitz
assert len(fitz.open(w/'giornale.pdf'))==4
print('PASS quattro pagine originali',n,fit)
