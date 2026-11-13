"""Regole server/editoriali su dati reali conservati; nessun servizio remoto."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest
import datetime as dt

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'redazione'));from tifosi import context,validate,publish
sys.path.insert(0,str(ROOT/'calcoli/tifosi'))
spec=importlib.util.spec_from_file_location('mvp_sync',ROOT/'calcoli/tifosi/sincronizza.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)


class TifosiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.derby=json.loads((ROOT/'lab/prova-tifosi/dati.json').read_text())['derby_ufficiali']
        cls.ctx,cls.raw=context(ROOT/'anteprima/pubblicata',cls.derby)
        cls.edition=json.loads((ROOT/'redazione/tifosi.json').read_text())

    def test_editorial_and_facts(self):
        self.assertTrue(validate(self.edition,self.ctx));w=self.ctx['giornate'][-1]
        self.assertEqual(self.ctx['ultima'],7);self.assertEqual(len(w['squadre']['Oranje VC']['partite']),2);self.assertEqual(len(w['squadre']['stif dc']['partite']),1)
        self.assertEqual(len(w['personaggi']),5);self.assertEqual(len({v['autore'] for v in w['personaggi']}),5)
        e=copy.deepcopy(self.edition);e['giornate']['7']['firma']='x'
        with self.assertRaisesRegex(ValueError,'Fatti modificati'):validate(e,self.ctx)
        e=copy.deepcopy(self.edition);e['giornate']['7']['squadre'].pop('Oranje VC')
        with self.assertRaisesRegex(ValueError,'tutte le squadre'):validate(e,self.ctx)

    def test_schedule_and_no_retroactive_awards(self):
        p,reason=sync.payload(self.ctx,self.raw,self.edition,dt.datetime(2026,11,13,tzinfo=dt.timezone.utc))
        self.assertIsNone(reason);self.assertEqual(p['p_giornata'],7)
        self.assertEqual(p['p_chiude'],'2026-11-21T14:00:00+00:00')
        self.assertEqual(len(p['p_personaggi']),5)
        p,reason=sync.payload(self.ctx,self.raw,self.edition,dt.datetime(2026,11,22,tzinfo=dt.timezone.utc))
        self.assertIsNone(p);self.assertIn('retroattivamente',reason)
        p,reason=sync.payload(self.ctx,self.raw,{'giornate':{}})
        self.assertIsNone(p);self.assertIn('redazione',reason)


if __name__=='__main__':unittest.main()
