#!/usr/bin/env python3
"""Campo: risultato, partite da giocare, identità Lega/Stadio della pagina e Curva chiara/scura."""
from playwright.sync_api import sync_playwright, expect
from collaudo_anteprima_53_browser import fixture
from rete_browser import browser, installa

ROOT = 'http://127.0.0.1:8765/anteprima/5.5/'
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
        formazioni = {}
        c.route('https://giandjcosta.github.io/o-fant-a-girrr/formazioni.json',
                lambda r: r.fulfill(json=formazioni))
        p = c.new_page()
        p.goto(ROOT + f'campo-{skin}.html?giornata=4&partita=0')
        # Il campo con le formazioni (giornata senza formazioni nella fixture: campo con le sigle).
        p.locator('.pitch').wait_for()
        expect(p.locator('.match-head .score')).to_have_text('0 : 0')
        title_font = p.locator('h1').evaluate('(e)=>getComputedStyle(e).fontFamily')
        assert ('Lobster' in title_font) == (skin == 'stadio'), title_font
        assert p.locator('html').evaluate('(e)=>getComputedStyle(e).backgroundColor') == 'rgb(29, 42, 82)'
        p.locator('#next').click()
        expect(p.locator('.match-head .score')).to_have_text('1 : 0')
        p.locator('#matches button').last.click()
        expect(p.locator('.match-head .score')).to_have_text('— : —')
        assert 'partita=4' in p.url or p.locator('#matches button').last.get_attribute('aria-pressed') == 'true'
        assert not p.evaluate('document.documentElement.scrollWidth>innerWidth+1')

        # Formazioni controllate: verifica che tastiera e clic aprano gli stessi dettagli.
        g = dati['cal']['lega'][3]
        sa = str(g['sa'])
        formazioni[sa] = {}
        for lato, squadra in enumerate((g['m'][0][0], g['m'][0][3])):
            tit = []
            for i, ruolo in enumerate('PDDDCCCCAAA'):
                pid = 90000 + lato * 100 + i
                tit.append(pid)
                dati['P'][str(pid)] = {'n': f'Giocatore di prova {lato}-{i}', 'r': ruolo}
                dati['votes'][str(pid)] = {sa: {'v': 6, 'f': 6, 'b': []}}
            formazioni[sa][squadra] = {'tit': tit, 'pan': []}
        p.goto(ROOT + f'campo-{skin}.html?giornata=4&partita=0')
        expect(p.locator('.pl')).to_have_count(22)
        giocatori = p.locator('.pl')
        giocatori.first.focus()
        giocatori.first.press('Enter')
        expect(p.locator('#xi-det')).to_have_text(giocatori.first.get_attribute('data-det'))
        giocatori.last.focus()
        giocatori.last.press('Space')
        expect(p.locator('#xi-det')).to_have_text(giocatori.last.get_attribute('data-det'))

        # Una squadra può aver schierato dieci uomini: nessuno va aggiunto o nascosto.
        formazioni[sa][g['m'][0][0]]['tit'].pop()
        p.reload()
        expect(p.locator('.pl.home')).to_have_count(10)
        expect(p.locator('.pl.away')).to_have_count(11)
        assert 'Giocatore di prova 0-10' not in p.locator('.pitch').inner_text()

        # I pannelli aggiunti alla Curva devono seguire anche il cambio chiaro/scuro.
        p.goto(ROOT + f'curva-{skin}.html')
        p.locator('#v53poll .v55-pp-q').first.wait_for()
        for tema in ('light', 'dark'):
            p.evaluate('(t)=>document.documentElement.dataset.theme=t', tema)
            colori = p.locator('#v53poll').evaluate('''e=>({
              titolo:getComputedStyle(e.querySelector('.v55-pp-q')).color,
              testo:getComputedStyle(document.body).color,
              fondo:getComputedStyle(e.querySelector('.v55-pollpost')).backgroundColor,
              pagina:getComputedStyle(document.body).backgroundColor})''')
            # Il corpo della Curva dissolve i colori in 250 ms.
            expect(p.locator('body')).to_have_css('color', colori['titolo'])
            expect(p.locator('body')).to_have_css('background-color', colori['fondo'])
        c.close()
        print('PASS Campo', skin, 'risultato, attesa, cambio partita, skin e Curva chiara/scura', flush=True)
    b.close()
