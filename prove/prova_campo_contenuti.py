#!/usr/bin/env python3
"""Campo: risultato e Fantapunti distinti, attesa/turni parziali e due identità."""
from playwright.sync_api import sync_playwright, expect
from collaudo_anteprima_53_browser import fixture
from rete_browser import browser, installa

ROOT = 'http://127.0.0.1:8765/anteprima/5.3/'
dati = fixture()
# Un pareggio a zero resta un dato valido, diverso da una partita non giocata.
dati['cal']['lega'][3]['m'][0][1:3] = [0, 0]
dati['cal']['lega'][3]['m'][0][4] = '0-0'
# Una partita conclusa non chiude le altre quattro né la classifica del turno.
dati['cal']['lega'][4]['m'][0][1:3] = [66, 65]
dati['cal']['lega'][4]['m'][0][4] = '1-0'

with sync_playwright() as pw:
    b = browser(pw)
    for skin in ('lega', 'stadio'):
        c = b.new_context(viewport={'width': 390, 'height': 950})
        installa(c)
        c.route('https://giandjcosta.github.io/o-fant-a-girrr/data.json',
                lambda r: r.fulfill(json=dati))
        p = c.new_page()
        p.goto(ROOT + f'campo-{skin}.html?giornata=4&partita=0')
        expect(p.locator('.pitch-state')).to_have_text('Risultato · Giornata 4')
        assert p.locator('.pitch-goals b').all_text_contents() == ['0', '0']
        assert p.locator('.pitch-goals div>span').all_text_contents() == ['0Fantapunti', '0Fantapunti']
        assert p.locator('.pitch-club strong').all_text_contents() == [dati['cal']['lega'][3]['m'][0][i] for i in (0, 3)]
        title_font = p.locator('h1').evaluate('(e)=>getComputedStyle(e).fontFamily')
        assert ('Lobster' in title_font) == (skin == 'stadio'), title_font
        assert p.locator('html').evaluate('(e)=>getComputedStyle(e).backgroundColor') == 'rgb(29, 42, 82)'
        p.locator('#next').click()
        expect(p.locator('.pitch-state')).to_have_text('Risultato · Giornata 5')
        assert p.locator('.pitch-goals b').all_text_contents() == ['1', '0']
        assert p.locator('.pitch-goals div>span').all_text_contents() == ['66Fantapunti', '65Fantapunti']
        expect(p.locator('.pitch-rank-date')).to_have_text('Classifica dopo la 4ª giornata')
        # Il nome più lungo deve rimanere interamente dentro il campo sul telefono.
        p.locator('#matches button').nth(2).click()
        assert 'Atletico ma non troppo' in p.locator('.pitch-club').all_text_contents()[0]
        assert p.locator('.pitch-club strong').evaluate_all('''nodes=>nodes.every(e=>
          e.scrollWidth<=e.clientWidth+1 && e.getBoundingClientRect().bottom<=e.closest('.pitch').getBoundingClientRect().bottom)''')
        p.locator('#matches button').last.click()
        expect(p.locator('.pitch-state')).to_have_text('Da giocare · Giornata 5')
        assert p.locator('.pitch-goals b').all_text_contents() == ['—', '—']
        assert p.locator('.pitch-goals div>span').all_text_contents() == ['—Fantapunti', '—Fantapunti']
        assert 'partita=4' in p.url
        p.get_by_role('link', name='Confronta il rendimento ↓').click()
        assert p.url.endswith('#rendimento')
        assert not p.evaluate('document.documentElement.scrollWidth>innerWidth+1')

        # I pannelli aggiunti alla Curva devono seguire anche il cambio chiaro/scuro.
        p.goto(ROOT + f'curva-{skin}.html')
        p.locator('#v53poll h3').wait_for()
        for tema in ('light', 'dark'):
            p.evaluate('(t)=>document.documentElement.dataset.theme=t', tema)
            colori = p.locator('#v53poll').evaluate('''e=>({
              titolo:getComputedStyle(e.querySelector('h3')).color,
              testo:getComputedStyle(document.body).color,
              fondo:getComputedStyle(e.closest('.v53-panel')).backgroundColor,
              pagina:getComputedStyle(document.body).backgroundColor})''')
            # Il corpo della Curva dissolve i colori in 250 ms.
            expect(p.locator('body')).to_have_css('color', colori['titolo'])
            expect(p.locator('body')).to_have_css('background-color', colori['fondo'])
        c.close()
        print('PASS Campo', skin, 'zero, attesa, turno parziale, cambio partita, skin e Curva chiara/scura', flush=True)
    b.close()
