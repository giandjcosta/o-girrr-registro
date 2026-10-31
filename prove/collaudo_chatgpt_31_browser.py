#!/usr/bin/env python3
"""Browser 320px e prova della bio Curva su un turno aggiunto soltanto in memoria."""
import json
import re
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8765'
ART = Path('qa_artifacts')
ART.mkdir(exist_ok=True)
def width(p):
    size = p.evaluate('({viewport: innerWidth, contenuto: document.documentElement.scrollWidth})')
    assert size['contenuto'] <= size['viewport'] + 1, f"Scorrimento orizzontale a 320px: {p.url}: {size}"
    print('PASS 320px', p.url, size)

def visit(context, path, name):
    page=context.new_page(viewport={'width':320,'height':740})
    errors=[]
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(BASE+path,wait_until='domcontentloaded',timeout=30000)
    page.wait_for_timeout(750)
    width(page)
    assert not errors, f"Errori Javascript {path}: {errors}"
    page.screenshot(path=str(ART/(name+'.png')),full_page=True)
    print('PASS console e screenshot',path)
    return page

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':320,'height':740}, device_scale_factor=1)
    # Nessuna chiamata al database di produzione, neanche in sola lettura.
    context.route(re.compile(r'https?://[^/]+\.supabase\.co/.*'),lambda route: route.fulfill(status=200,content_type='application/json',body='{"voti":[],"sfide":[]}'))
    lab=visit(context,'/lab/index.html#oro','lab-320')
    lab.locator('button[data-oro="annuario"]').click()
    lab.wait_for_timeout(3000)
    width(lab)
    assert 'Annuario' in lab.locator('body').inner_text()
    assert lab.locator('body').get_by_text('Lautaro Martinez').count()>0, 'Annuario: dati reali del sito non caricati'
    lab.screenshot(path=str(ART/'annuario-320.png'),full_page=True)
    print('PASS Annuario da dati reali, Lautaro Martinez')
    for path,name in [
      ('/anteprima/index.html#oro','stadio-320'),
      ('/anteprima/attuale.html#oro','lega-320'),
      ('/anteprima/totogirrr-52.html?demo&skin=stadio','totogirrr-stadio-320'),
      ('/lab/prova-storia-17peppe17.html','storia-320'),
    ]:
      p=visit(context,path,name)
      if name=='totogirrr-stadio-320':
        assert p.locator('#skin-stadio').count()==1, 'Totogirrr Stadio senza skin'
      if name in ('stadio-320','lega-320'):
        p.goto(BASE+path.replace('#oro','#carriera'),wait_until='domcontentloaded')
        p.locator('button[data-cr="cassa"]').click()
        assert 'La cassa della lega' in p.locator('body').inner_text(), 'Cassa non raggiungibile'
        print('PASS Cassa raggiungibile',name)
      p.close()
    # Curva: test delle funzioni REALI nel browser con risultati della sesta giornata
    # alterati esclusivamente nella memoria locale del test, senza scrivere dati.
    with urllib.request.urlopen('https://giandjcosta.github.io/o-fant-a-girrr/data.json', timeout=20) as response:
      current=json.load(response)
    source=Path('ufficiale/src/sito/girrr/curva.html').read_text(encoding='utf8')
    needle='})();\n</script>'
    assert source.count(needle)==1, 'Punto inserimento Curva non univoco'
    source=source.replace(needle,
      'window.__testBio={calcola:calcola,posiz:posiz,seguaci:seguaci};\n})();\n</script>')
    def curva_mock(route):
      route.fulfill(status=200,content_type='text/html; charset=utf-8',body=source)
    context.route('**/ufficiale/src/sito/girrr/curva.html',curva_mock)
    context.route('**/data.json',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(current)))
    curva=visit(context,'/ufficiale/src/sito/girrr/curva.html','curva-320')
    curva.wait_for_function('Boolean(window.__testBio)', timeout=15000)
    result=curva.evaluate("""d=>{
      var api=window.__testBio,team='Oranje VC';
      api.calcola(d);
      var prima={posto:api.posiz(team),follower:api.seguaci(team)};
      var g=d.cal.lega.find(x=>x.m.some(m=>m[4]==='-'));
      if(!g)throw Error('Manca il prossimo turno');
      g.m.forEach(m=>{m[1]=70;m[2]=70;m[4]=m[0]===team?'5-0':m[3]===team?'0-5':'0-0'});
      api.calcola(d);
      var dopo={posto:api.posiz(team),follower:api.seguaci(team)};
      return {prima,dopo,turno:g.n};
    }""",current)
    print('Curva calcolo prima/dopo turno simulato:',result)
    assert result['prima']!=result['dopo'], 'La posizione e i follower sono rimasti invariati'
    print('PASS bio Curva: classifica e follower ricalcolati dopo turno simulato in browser')
    browser.close()
