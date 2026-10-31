"""Rete browser verificata con CA del runtime; cache solo per letture pubbliche.

Chromium di sistema non usa il bundle CA del proxy. Il bridge usa urllib/TLS
verificato: nessun ignore_https_errors. Le RPC sono simulate e mai inoltrate.
"""
import hashlib
import json
import mimetypes
import os
import re
import urllib.request
from pathlib import Path
CACHE = Path('/tmp/girrr-browser-cache'); CACHE.mkdir(exist_ok=True)

def installa(ctx):
    def handler(route):
        u=route.request.url
        if '.supabase.co/' in u:
            route.fulfill(status=200,content_type='application/json',body='{"voti":[],"sfide":[]}');return
        if route.request.method!='GET':
            raise AssertionError('Scrittura di rete bloccata: '+u)
        name=CACHE/hashlib.sha256(u.encode()).hexdigest()
        try:
            meta=name.with_suffix('.json')
            if name.exists() and meta.exists():
                headers=json.loads(meta.read_text());body=name.read_bytes()
            else:
                with urllib.request.urlopen(u,timeout=30) as r:
                    body=r.read();headers={'content-type':r.headers.get('Content-Type','application/octet-stream')}
                name.write_bytes(body);meta.write_text(json.dumps(headers))
            route.fulfill(status=200,headers=headers,body=body)
        except Exception as e:
            print('ERRORE RISORSA',u,str(e));route.fulfill(status=502,body=str(e))
    ctx.route(re.compile(r'https://.*'),handler)

def browser(pw):
    exe=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium')
    return pw.chromium.launch(headless=True,**({'executable_path':exe} if Path(exe).exists() else {}),args=['--no-sandbox'])
