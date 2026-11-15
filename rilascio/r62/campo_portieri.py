"""Simboli laterali dei soli portieri, con pallone barrato per i gol subiti."""
from pathlib import Path
import sys
ICON='<span class="gs-icon" aria-hidden="true">⚽<sup>×</sup></span>'
def prepara(base):
 for skin in ('girrr','stadio/girrr'):
  p=base/skin/'campo.html';s=p.read_text()
  if 'id="portieri62"' not in s:
   s=s.replace("(lato==='away'&&g.r==='P'?' basso':'')", "(g.r==='P'?' portiere':'')")
   old="(g.gs?g.gs+'🥅':'')";new="(g.gs?'"+ICON+"<span class=\"gs-num\">'+g.gs+'</span>':'')"
   if old not in s:raise ValueError('Simboli Campo diversi dalla base attesa')
   s=s.replace(old,new).replace('<span class="legend-symbol" aria-hidden="true">🥅</span>', '<span class="legend-symbol">'+ICON+'</span>')
   css='''<style id="portieri62">.pitch .pl.portiere i{left:calc(50% + 19px);top:0;bottom:auto;transform:none;margin:0;display:flex;align-items:center;flex-wrap:wrap;gap:2px;width:max-content;max-width:70px;white-space:normal}.gs-icon{display:inline-block!important;position:relative!important;background:none!important;padding:0!important;margin:0!important;overflow:visible!important;font:inherit!important;line-height:1!important;color:inherit!important}.gs-icon sup{position:absolute;right:-2px;bottom:-1px;font:bold 8px/1 Arial;color:#fff;background:#b9172c;border-radius:50%;width:8px;height:8px;text-align:center}.gs-num{display:inline!important;background:none!important;padding:0!important;margin:0 2px 0 1px!important;font:inherit!important;color:inherit!important}</style>'''
   s=s.replace('</head>',css+'</head>')
  p.write_text(s)
if __name__=='__main__':prepara(Path(sys.argv[1]))
