"""Prova la ricostruzione su veri repository temporanei, senza rete."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ramificazioni',ROOT/'ramificazioni.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)


class GraphTest(unittest.TestCase):
    def test_pr_closed_and_reopened_without_git_changes(self):
        with tempfile.TemporaryDirectory(prefix='girrr-pr-') as tmp:
            repo=Path(tmp)/'repo';repo.mkdir()
            def git(*args):return subprocess.check_output(['git','-C',str(repo),*args],text=True,stderr=subprocess.DEVNULL).strip()
            git('init','-b','main');git('config','user.name','Test locale');git('config','user.email','test@example.invalid')
            (repo/'registro-stato.json').write_text('{"versione":"6.0"}');git('add','.');git('commit','-m','Base')
            branch='chatgpt/prova';git('switch','-c',branch)
            (repo/'pagina').write_text('prova');git('add','.');git('commit','-m','Proposta');git('switch','main')
            pr={'number':55,'title':'Proposta','html_url':'https://github.com/example/repo/pull/55',
                'head':{'ref':branch},'base':{'ref':'main'},'state':'open','merged_at':None}
            original=M.collect(repo,'registro','example/repo',prs=[pr])
            out=Path(tmp)/'dati.json';M.save(out,[original]);first=json.loads(out.read_text())
            closed=M.collect(repo,'registro','example/repo',prs=[dict(pr,state='closed')])
            self.assertTrue(M.save(out,[closed]))
            before=next(b for b in original['branches'] if b['name']==branch)
            after=next(b for b in closed['branches'] if b['name']==branch)
            self.assertEqual(after['head'],before['head'])
            self.assertEqual(after['state'],'in-lavoro')  # Chiusa non significa unita.
            self.assertEqual(after['pr']['state'],'closed')
            self.assertNotEqual(json.loads(out.read_text())['fingerprint'],first['fingerprint'])
            self.assertFalse(M.save(out,[closed]))
            self.assertTrue(M.save(out,[original]))
            self.assertEqual(json.loads(out.read_text())['fingerprint'],first['fingerprint'])

    def test_graph_versions_and_unchanged_snapshot(self):
        with tempfile.TemporaryDirectory(prefix='girrr-rami-') as tmp:
            repo=Path(tmp)/'repo';repo.mkdir()
            def git(*args):return subprocess.check_output(['git','-C',str(repo),*args],text=True,stderr=subprocess.DEVNULL).strip()
            git('init','-b','main');git('config','user.name','Test locale');git('config','user.email','test@example.invalid')
            (repo/'registro-stato.json').write_text('{"versione":"5.8.2"}');git('add','.');git('commit','-m','Base del Registro');base=git('rev-parse','HEAD')
            git('switch','-c','chatgpt/nuova-pagina');(repo/'pagina').write_text('nuova');git('add','.');git('commit','-m','Pagina interattiva');feature=git('rev-parse','HEAD')
            git('switch','main');git('merge','--no-ff','chatgpt/nuova-pagina','-m','Unisce la pagina')
            git('branch','chatgpt/in-corso');git('switch','chatgpt/in-corso');(repo/'seconda').write_text('due');git('add','.');git('commit','-m','Lavoro non ancora unito');git('switch','main')
            git('branch',M.TECHNICAL)
            r=M.collect(repo,'registro','giandjcosta/o-girrr-registro',prs=[])
            branches={b['name']:b for b in r['branches']}
            self.assertNotIn(M.TECHNICAL,branches)
            self.assertEqual(branches['chatgpt/nuova-pagina']['state'],'integrato')
            self.assertEqual(branches['chatgpt/nuova-pagina']['ahead'],0)
            self.assertEqual(branches['chatgpt/in-corso']['ahead'],1)
            self.assertEqual(branches['chatgpt/nuova-pagina']['base'],feature)
            self.assertIn(feature,r['nodes']);self.assertEqual(r['version'],'5.8.2')
            self.assertEqual(branches['main']['head'],git('rev-parse','main'))
            self.assertEqual(M.color('ramo'),M.color('ramo'))
            out=Path(tmp)/'dati.json';self.assertTrue(M.save(out,[r]));before=out.read_bytes();self.assertFalse(M.save(out,[r]));self.assertEqual(before,out.read_bytes())
            (repo/'registro-stato.json').write_text('{"versione":"6.0"}');git('add','.');git('commit','-m','Versione successiva')
            new=M.collect(repo,'registro','giandjcosta/o-girrr-registro',prs=[])
            self.assertEqual(new['version'],'6.0');self.assertTrue(M.save(out,[new]))
            self.assertNotEqual(json.loads(before)['fingerprint'],json.loads(out.read_text())['fingerprint'])
            # Un gh-pages orfano non deve essere disegnato come una biforcazione inventata.
            git('switch','--orphan','gh-pages');(repo/'versioni.json').write_text('{"versioni":[{"v":"6.0"}]}');git('add','.');git('commit','-m','Sito pubblicato con storia indipendente')
            site=M.collect(repo,'sito','giandjcosta/o-fant-a-girrr',prs=[])
            published=next(b for b in site['branches'] if b['name']=='gh-pages')
            self.assertIsNone(published['base']);self.assertEqual(published['state'],'pubblicato');self.assertEqual(site['version'],'6.0')


if __name__=='__main__':unittest.main()
