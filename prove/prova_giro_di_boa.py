#!/usr/bin/env python3
"""Prove dei fatti del bilancio e del testo Radio, senza rete né voci a pagamento."""
import copy
import datetime as dt
import importlib.util
import json
import random
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'calcoli'))
from giro_di_boa import calcola, MANCANTE
spec=importlib.util.spec_from_file_location('segmento_radio_boa',ROOT/'voci-src/segmento_giro_boa.py')
radio=importlib.util.module_from_spec(spec);spec.loader.exec_module(radio)


def dati(n=3):
    mm=[['A',72,70,'B','2-0'],['C',66,66,'D','1-1']]
    turns=[mm,[['B',70,67,'A','1-1'],['D',76,60,'C','3-0']],
           [['A',71,71.5,'B','1-2'],['C',60,61,'D','0-0']]]
    return {'teams':[{'name':t} for t in 'ABCD'],'updated':'2026-11-13',
            'cal':{'lega':[{'n':i+1,'sa':i+5,'m':copy.deepcopy(turns[i%3])} for i in range(n)],'cup':[]}}


class Giro(unittest.TestCase):
    def test_voci_firmate_pertinenti_non_inventate(self):
        from giro_di_boa import firma_settimana, giornate_pubblicate
        d=dati();ora=dt.datetime(2026,11,14,tzinfo=dt.timezone.utc).timestamp()
        firma=firma_settimana(d,giornate_pubblicate(d,ora),3,'2026/27',ora)
        ed={'stagione':'2026/27','giornate':{'3':{'firma':firma,'squadre':{'A':{'titolo':'La corsa di A','paragrafi':['A ritrova la vittoria.']}}}}}
        feed={'posts':[{'id':1,'team':'B','body':'Complimenti alla A per la partita e per questa vittoria in campionato.','ts':(ora-10)*1000},
                       {'id':2,'team':'A','body':'La maglia presentata questa settimana ha tre colori.','ts':(ora-5)*1000},
                       {'id':3,'team':'A','body':'Domani vinciamo questa partita con la squadra A.','ts':(ora+100)*1000}],
              'replies':[],'react':[]}
        out=calcola(d,ora=ora,edizione=ed,curva=feed)['periodi']['finora']['squadre']['A']['voci']
        self.assertEqual(out['redazione']['testo'],'A ritrova la vittoria.')
        self.assertEqual([p['id'] for p in out['curva']],['p1'])
        self.assertEqual(out['curva'][0]['autore'],'B')
        ed['giornate']['3']['firma']='obsoleta'
        self.assertIsNone(calcola(d,ora=ora,edizione=ed)['periodi']['finora']['squadre']['A']['voci']['redazione'])

    def test_voci_storiche_non_includono_commenti_futuri(self):
        d=dati(19);ora=dt.datetime(2026,11,14,tzinfo=dt.timezone.utc).timestamp()
        d['votiTs']={'21':'2026-11-01T18:00:00Z'} # 17ª giornata
        feed={'posts':[{'id':1,'team':'A','body':'La squadra A risponde con una grande vittoria in campionato.','ts':(ora-100)*1000}]}
        p=calcola(d,ora=ora,curva=feed)['periodi']
        self.assertEqual(len(p['finora']['squadre']['A']['voci']['curva']),1)
        self.assertEqual(p['andata']['squadre']['A']['voci']['curva'],[])

    def test_risultati_unita_casa_trasferta_serie(self):
        s=calcola(dati())['periodi']['finora']['squadre']['A']
        self.assertEqual((s['punti_classifica'],s['posizione']),(4,3))
        self.assertEqual((s['bilancio']['vittorie'],s['bilancio']['pareggi'],s['bilancio']['sconfitte']),(1,1,1))
        self.assertEqual((s['bilancio']['gol_fatti'],s['bilancio']['gol_subiti']),(4,3))
        self.assertEqual(s['casa']['giocate'],2);self.assertEqual(s['trasferta']['giocate'],1)
        self.assertEqual(s['serie']['senza_vittorie'],{'partite':2,'dalla':2,'alla':3})
        self.assertEqual(s['serie']['imbattibilita']['partite'],2)
        self.assertEqual(s['numeri']['totali'],210);self.assertEqual(s['numeri']['unita'],'Fantapunti')
        self.assertEqual(s['sul_filo'][0]['giornata'],3)
        self.assertEqual(s['sul_filo'][0]['scarto_fantapunti'],0.5)
        self.assertEqual((s['distacco_vetta'],s['margine_ultimo_posto']),(1,2))

    def test_parita_come_tabellone_fp_prima_dr(self):
        rows=calcola(dati())['periodi']['finora']['classifica']
        self.assertEqual([x['squadra'] for x in rows],['D','B','A','C'])
        self.assertGreater(rows[2]['gol_fatti']-rows[2]['gol_subiti'],rows[1]['gol_fatti']-rows[1]['gol_subiti'])

    def test_giornata_incompleta_blocca_anche_turni_futuri(self):
        d=dati();d['cal']['lega'][1]['m'][0][4]='-'
        self.assertEqual(calcola(d)['ultima_pubblicata'],1)
        d=dati();d['cal']['lega'][1]['m'].pop()
        self.assertEqual(calcola(d)['ultima_pubblicata'],1)

    def test_pubblicazione_un_ora_e_fuso(self):
        d=dati();d['votiTs']={'6':'2026-11-14T15:00:00+01:00'};d['calcTs']={'6':'2026-11-14T14:10:00Z'}
        ora=dt.datetime(2026,11,14,15,9,tzinfo=dt.timezone.utc).timestamp()
        self.assertEqual(calcola(d,ora=ora)['ultima_pubblicata'],1)
        self.assertEqual(calcola(d,ora=ora+60)['ultima_pubblicata'],3)

    def test_andata_fissa_e_ritorno_separato(self):
        a=calcola(dati(17));b=calcola(dati(19))
        self.assertNotIn('andata',calcola(dati(16))['periodi'])
        self.assertEqual(a['periodi']['andata'],b['periodi']['andata'])
        self.assertEqual(b['periodi']['ritorno']['squadre']['A']['bilancio']['giocate'],2)
        self.assertEqual(b['periodi']['finora']['squadre']['A']['bilancio']['giocate'],19)
        self.assertTrue(b['periodi']['andata']['completo'])

    def test_fonti_opzionali_assenti_non_sono_zero_certificati(self):
        s=calcola(dati())['periodi']['finora']['squadre']['A']
        self.assertFalse(s['derby']['disponibile']);self.assertFalse(s['mvp']['disponibile']);self.assertFalse(s['promesse']['disponibile'])
        self.assertEqual(s['dirigenza']['fascia'],MANCANTE);self.assertIsNone(s['dirigenza']['fiducia'])
        self.assertTrue(calcola(dati(),mvp={'archivio':[]})['periodi']['finora']['squadre']['A']['mvp']['disponibile'])

    def test_attese_fiducia_storica_promesse_mvp_derby(self):
        f={'giornata':7,'squadre':{'A':{'fiducia':90,'storico':[{'giornata':3,'fiducia':48}],
           'promesse':[{'giornata':1,'esito':'v'},{'giornata':2,'esito':'s'},{'giornata':3,'esito':'p'},{'giornata':4,'esito':'v'}]}}}
        m={'archivio':[{'giornata':1,'classifica':[{'team':'A'}]},{'giornata':4,'classifica':[{'team':'A'}]}]}
        de={'coppie':[{'a':'A','b':'B','n':'Derby ufficiale'}]}
        s=calcola(dati(),f,{'squadre':{'A':{'attesa':1,'obiettivo':'Vincere','fascia':'Big'}}},de,m)['periodi']['finora']['squadre']['A']
        self.assertEqual(s['dirigenza']['fiducia'],48);self.assertEqual(s['dirigenza']['scostamento_posizioni'],-2)
        self.assertEqual([s['promesse'][k] for k in ('mantenute','pari','tradite')],[1,1,1])
        self.assertEqual(s['mvp']['giornate'],[1]);self.assertEqual(s['derby']['giocate'],3)

    def test_coppa_non_legge_partite_parziali_o_future(self):
        d=dati();d['cal']['cup']=[{'n':1,'sa':5,'m':[['A','A',71,66,'B','2-1'],['A','C',60,60,'D','-']]},
                                {'n':2,'sa':6,'m':[['A','B',70,72,'A','1-2']]},
                                {'n':3,'sa':100,'m':[['A','A',90,50,'B','5-0']]}]
        c=calcola(d)['periodi']['finora']['squadre']['A']['coppa']
        self.assertEqual(c['giocate'],1);self.assertEqual(c['punti_girone'],3);self.assertEqual(c['partite'][0]['giornata'],2)

    def test_coppa_girone_chiuso_e_fase_finale(self):
        from itertools import combinations
        d=dati(19);d['cal']['cup']=[{'n':i+1,'sa':i+5,'m':[['A',a,76,66,b,'3-1']]} for i,(a,b) in enumerate(combinations('ABCDE',2))]
        out=calcola(d)['periodi']['finora']['squadre']
        self.assertEqual(out['A']['coppa']['qualificazione'],'Qualificata ai quarti')
        d['cal']['cup'].append({'n':11,'sa':16,'m':[['QF','A',76,66,'B','3-1']]})
        self.assertEqual(calcola(d)['periodi']['finora']['squadre']['B']['coppa']['qualificazione'],'Eliminata ai quarti')
        d['cal']['cup'].append({'n':12,'sa':17,'m':[['A','A',76,66,'C','3-1']]})
        c=calcola(d)['periodi']['finora']['squadre']['A']['coppa']
        self.assertEqual(c['qualificazione'],'Qualificata in finale');self.assertEqual(c['punti_girone'],12)
        d['cal']['cup'].append({'n':13,'sa':18,'m':[['A','A',66,76,'D','1-3']]})
        self.assertEqual(calcola(d)['periodi']['finora']['squadre']['A']['coppa']['qualificazione'],'Finalista')

    def test_record_e_zona_ultimo_posto(self):
        p=calcola(dati())['periodi']['finora'];s=p['squadre']['A']
        self.assertEqual(s['vittoria_piu_larga']['partita']['giornata'],1)
        self.assertEqual(s['sconfitta_piu_pesante']['partita']['giornata'],3)
        self.assertEqual([t for t,s in p['squadre'].items() if s['in_zona_retrocessione']],['C'])

    def test_input_non_certificabile_non_inventa_ranking(self):
        d=dati();d['cal']['lega'][0]['m'][0][1]=None
        with self.assertRaisesRegex(ValueError,'Fantapunti non conservati'):calcola(d)

    def test_radio_periodi_fonte_identica_e_regole_editoriali(self):
        for n,k in [(17,'andata'),(19,'ritorno')]:
            j=calcola(dati(n));lines=radio.segmento(j,n);txt=' '.join(x[1] for x in lines)
            self.assertIn('Giro di boa',txt);self.assertNotIn('Fantapunti totali',txt);self.assertNotIn('Fantapunti di media',txt)
            self.assertNotIn('scommess',txt.lower());self.assertEqual(len(lines),7 if n==17 else 6)
            self.assertEqual(j['periodi'][k]['squadre']['A']['bilancio']['giocate'],17 if n==17 else 2)
        self.assertEqual(radio.segmento(calcola(dati(16)),16),[])
        with self.assertRaises(ValueError):radio.segmento(calcola(dati(17)),19)

    def test_firma_deterministica(self):
        self.assertEqual(calcola(dati())['fingerprint'],calcola(dati())['fingerprint'])
        d=dati();d['cal']['lega'][2]['m'][0][4]='1-1'
        self.assertNotEqual(calcola(dati())['fingerprint'],calcola(d)['fingerprint'])

    def test_unione_lab_non_attiva_radio_prima_del_rilascio(self):
        sp=importlib.util.spec_from_file_location('prepara_boa',ROOT/'voci-src/prepara_dati.py')
        mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            for v,attivo in [('6.0',False),('6.0.1',False),('6.0.2',True),('6.1',True)]:
                (p/'versioni.json').write_text(json.dumps({'versioni':[{'v':v}]}))
                self.assertEqual(mod.versione_boa(p),attivo)

    def test_inserimento_nel_copione_completo_senza_servizi_vocali(self):
        sys.path.insert(0,str(ROOT/'voci-src'))
        import copione
        base=json.loads((ROOT/'voci-src/dati.json').read_text())
        for n in (17,19):
            d=copy.deepcopy(base);d['aw'][-1]['n']=n;d['giro_di_boa']=calcola(dati(n))
            d['cronache_classifica_attive']=True;d.pop('zona_classifica',None)
            righe=copione.build(d,random.Random(n),{},regole={})
            self.assertTrue(any('Giro di boa' in r[1] for r in righe))
            self.assertTrue(any('A: posizione' in r[1] for r in righe))


if __name__=='__main__':unittest.main(verbosity=2)
