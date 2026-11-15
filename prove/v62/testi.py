import copy,json,random,sys,unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path[:0]=[str(R/'voci-src'),str(R/'calcoli')]
from mvp_editoriale62 import frase,scegli
from finestre62 import scadenza
import copione
class Test(unittest.TestCase):
 def test_radio(self):
  d=json.loads((R/'voci-src/dati.json').read_text());d['cronache_classifica_attive']=True
  base=copione.build(d,random.Random(7),{});w={'stagione':'2026/27','giornata':4,'chiusa':'2026-11-01T12:00:00Z','risultato':[{'team':'Atletico ma non troppo'}]};d['mvp_tifosi']=w
  dopo=copione.build(d,random.Random(7),{});self.assertEqual(len(dopo),len(base)+1);self.assertEqual(dopo[:-3]+dopo[-2:],base);self.assertEqual(dopo[-3][0],'G');self.assertEqual(dopo[-3][1],'Atletico ma non troppo è l’MVP dei tifosi della 4ª giornata.');self.assertLessEqual(len(dopo[-3][1].split()),15)
  d['mvp_annunciati']=['2026/27:4'];self.assertEqual(copione.build(d,random.Random(7),{}),base)
 def test_stati(self):
  now=datetime(2026,11,15,tzinfo=timezone.utc);w={'stagione':'2026/27','giornata':7,'chiude':'2026-11-21T14:00:00Z','chiusa':None,'classifica':[{'team':'Provvisoria'}]}
  self.assertEqual(frase(w,ora=now),'Per l’MVP della 7ª si vota ancora in Curva.');self.assertIsNone(frase(w,ora=now+timedelta(days=8)));w['chiusa']='2026-11-15T00:00:00Z';self.assertIsNone(frase(w,ora=now));self.assertIsNone(scegli({'votazione':w,'archivio':[]}))
 def test_finestre(self):
  a=datetime(2026,11,15,12,tzinfo=timezone.utc);i=a+timedelta(hours=36)
  self.assertEqual(scadenza('mvp',apertura=a,inizio=i),i);self.assertEqual(scadenza('mvp',apertura=a,inizio=a+timedelta(days=5)),a+timedelta(hours=48));self.assertEqual(scadenza('post',apertura=a),a+timedelta(hours=24));self.assertEqual(scadenza('dopo',apertura=a+timedelta(hours=8),risultati=a),a+timedelta(hours=48));self.assertEqual(scadenza('vigilia',apertura=a,inizio=i),i);self.assertEqual(scadenza('mvp',apertura=a,inizio=i,esistente=a+timedelta(days=6)),a+timedelta(days=6))
 def test_giornale_contenuti(self):
  sys.path.insert(0,str(R/'rilascio/r62/editoriale'))
  from mvp_giornale62 import integra
  now=datetime(2026,11,15,tzinfo=timezone.utc);t={'coro':{'testo':'Originale'},'titolo':'Intatto'}
  w={'stagione':'2026/27','giornata':6,'chiusa':'2026-11-14T00:00:00Z','classifica':[{'team':'Oranje VC'}]}
  dossier={'archivio':[w],'commento':{'squadra':'WOA','testo':'Parole autentiche','post_id':9,'giornata':6,'fonte':'curva','pertinente':True,'squadra_riferita':'Oranje VC'}}
  r=integra(t,dossier,7,now);self.assertEqual(r['coro'],t['coro']);self.assertEqual(r['titolo'],'Intatto');self.assertNotIn('mvp_editoriale',r)
  aperto=json.loads((R/'prove/v62/fixture/mvp-reale.json').read_text());r=integra(t,aperto,7,now);self.assertEqual(len(r['mvp_editoriale']['candidati']),3);self.assertIsNone(r['mvp_editoriale']['verdetto']);self.assertEqual(r['coro'],t['coro'])
 def test_ora_legale(self):
  from zoneinfo import ZoneInfo
  a=datetime(2027,3,27,12,tzinfo=ZoneInfo('Europe/Rome'));fine=scadenza('post',apertura=a);self.assertEqual((fine-a.astimezone(timezone.utc)).total_seconds(),86400)
if __name__=='__main__':unittest.main()
