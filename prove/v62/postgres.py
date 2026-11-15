"""Test su PostgreSQL locale con sessioni distinte; nessuna connessione a Supabase."""
import concurrent.futures as cf,json,os,sys,threading,time
from pathlib import Path
import psycopg
R=Path(__file__).resolve().parents[2]
if os.environ.get('PGHOST') not in ('127.0.0.1','localhost'):raise SystemExit('PGHOST deve essere esplicitamente locale')
NAME='girrr62_test_'+str(os.getpid())+'_'+str(int(time.time()))
connargs=dict(host=os.environ['PGHOST'],port=int(os.environ.get('PGPORT','5432')),user=os.environ.get('PGUSER','postgres'),password=os.environ.get('PGPASSWORD',''),dbname='postgres',autocommit=True)
with psycopg.connect(**connargs) as admin:admin.execute('create database '+NAME)
connargs['dbname']=NAME
sys.path.insert(0,str(R/'prove'));from prova_mvp60_db import SETUP
c=psycopg.connect(**connargs);c.execute(SETUP)
c.execute("create table public.curva_post(id bigint primary key,created timestamptz,body text);create table public.curva_poll(post_id bigint primary key,opts text[]);create table public.curva_vote(post_id bigint,team text,opt integer,primary key(post_id,team));create table public.conf_risposta(team text,giornata int,risposte jsonb,libera text,promessa text,pesa int,esito text,primary key(team,giornata));create table public.conf_dopo(team text,giornata int,risposta jsonb,creata timestamptz default now(),primary key(team,giornata));")
for f in ('sondaggio-curva.sql','mvp-tifosi-60.sql'):c.execute((R/'sql'/f).read_text())
red=json.dumps([{'autore':'Redazione','scelta':'stif dc','motivo':'Vittoria verificata.'}]);bots=json.dumps([{'autore':'Personaggio','scelta':'Oranje VC','motivo':'Vittoria verificata.'}]);cand=json.dumps([{'team':'stif dc'},{'team':'Oranje VC'}]);code='codice-solo-del-test'
c.execute("select public.mvp_prepara('2026/27',7,'2026-11-21T14:00:00Z',%s,%s,%s,repeat('a',64))",(cand,red,bots))
c.execute("insert into sondaggio_private.voti(giornata,team,scelta) values(8,'Oranje VC','A')")
for _ in range(2):
 for f in ('votazioni-62-proposta.sql','finestre-62-proposta.sql'):c.execute((R/'sql'/f).read_text())
report=[]
def check(label,ok):
 assert ok,label
 report.append(label)
def value(sql,args=()):return c.execute(sql,args).fetchone()[0]
for n,offset in ((8,1),(7,-1),(6,-2),(5,-3)):
 c.execute("select public.v62_prepara(%s,'2026/27','sfida',%s,%s,'Sfida',%s,clock_timestamp()-interval '10 days',clock_timestamp()+(%s||' days')::interval)",(f'sfida:2026/27:{n}',str(n),n,'["A","B"]',str(offset)))
check('Voti preesistenti leggibili senza importazioni',value("select public.v62_sondaggi('2026/27','Oranje VC',%s)->'aperti'->0->>'mia_scelta'",(code,))=='A')
bar=threading.Barrier(2)
def voto(scelta,fn='sondaggio'):
 with psycopg.connect(**connargs) as cc:
  cc.execute('set role anon');bar.wait()
  if fn=='mvp':return cc.execute("select public.mvp_vota('Apo team',%s,'2026/27',7,%s)",(code,scelta)).fetchone()[0]
  return cc.execute("select public.v62_vota('sfida:2026/27:8','Apo team',%s,%s)",(code,scelta)).fetchone()[0]
with cf.ThreadPoolExecutor(2) as ex:r=list(ex.map(voto,['A','B']))
check('Due sessioni concorrenti con scelte diverse: un solo voto',sum(x['registrato'] for x in r)==1 and value("select count(*) from sondaggio_private.voti where giornata=8 and team='Apo team'")==1)
check('Risposte concorrenti riportano entrambe la prima scelta',r[0]['mia_scelta']==r[1]['mia_scelta'])
prima=r[0]['mia_scelta'];c.execute("select public.sondaggio_vota('Apo team',%s,8,%s)",(code,'B' if prima=='A' else 'A'))
check('Vecchia RPC conserva la scelta',value("select scelta from sondaggio_private.voti where giornata=8 and team='Apo team'")==prima)
bar=threading.Barrier(2)
with cf.ThreadPoolExecutor(2) as ex:r=list(ex.map(lambda x:voto(x,'mvp'),['stif dc','Oranje VC']))
check('MVP concorrente: una preferenza immutabile',sum(x['registrato'] for x in r)==1 and r[0]['scelta']==r[1]['scelta'])
c.execute("select public.mvp_vota('Apo team',%s,'2026/27',7,null)",(code,))
check('Il ritiro non cancella il primo voto',value("select count(*) from mvp_private.voti where team='Apo team'")==1)
check('Scadenza già annunciata preservata',str(value("select chiude from mvp_private.giornate where giornata=7")).startswith('2026-11-21 14:00:00'))
check('Ultimi due chiusi identici e storico non cancellato',len(value("select public.v62_sondaggi('2026/27')->'chiusi'"))==2 and value('select count(*) from votazioni62_private.sondaggi')==4)
c.execute("insert into public.curva_post values(620001,clock_timestamp()-interval '2 days','Post precedente alle nuove finestre');insert into public.curva_poll values(620001,array['A','B'])")
c.execute("select public.curva_vota('Oranje VC',%s,620001,0)",(code,))
assert c.execute("select votazioni62_private.post_scadenza(created) is null from public.curva_post where id=620001").fetchone()[0]
report.append('Finestre solo future: post precedente senza scadenza inventata o chiusura retroattiva')
c.execute("insert into public.curva_post values(620002,clock_timestamp(),'Post con sondaggio');insert into public.curva_poll values(620002,array['A','B'])")
c.execute("select public.v62_vota('post:2026/27:620002','Oranje VC',%s,'A')",(code,));c.execute("select public.curva_vota('Oranje VC',%s,620002,1)",(code,))
check('Post nuovo: stesso ID e stessi voti senza copia del catalogo',value('select count(*) from public.curva_vote where post_id=620002')==1 and value('select opt from public.curva_vote where post_id=620002')==0)
with psycopg.connect(**connargs) as lock:
 lock.autocommit=False;lock.execute("update votazioni62_private.sondaggi set chiude=clock_timestamp()+interval '.2 seconds' where giornata=8")
 with cf.ThreadPoolExecutor(1) as ex:
  def tardivo():
   try:
    with psycopg.connect(**connargs) as cc:cc.execute("select public.v62_vota('sfida:2026/27:8','stif dc',%s,'A')",(code,))
   except psycopg.Error:return True
   return False
  f=ex.submit(tardivo);time.sleep(.3);lock.commit();check('Scadenza ricontrollata dopo attesa del lock',f.result())
c.execute("select public.v62_finestre_prepara('2026/27','vigilia',8,clock_timestamp()-interval '1 hour',clock_timestamp()+interval '1 hour')")
c.execute("insert into public.conf_risposta(team,giornata,risposte) values('Oranje VC',8,'[]')")
try:c.execute("update public.conf_risposta set risposte='[{}]' where giornata=8");raise AssertionError('Conferenza sovrascritta')
except psycopg.errors.RaiseException:report.append('Conferenza pubblicata immutabile anche sul server')
with psycopg.connect(**connargs) as anon:
 anon.execute('set role anon')
 try:anon.execute('select * from votazioni62_private.sondaggi');raise AssertionError('Accesso diretto consentito')
 except psycopg.errors.InsufficientPrivilege:report.append('Schema privato, RLS e privilegi verificati')
c.close();Path(__file__).with_name('risultati-postgres.json').write_text(json.dumps({'motore':'PostgreSQL 17 nativo locale','databaseIsolato':NAME,'sessioniConcorrenti':2,'produzione':False,'prove':report},ensure_ascii=False,indent=2)+'\n');print('\n'.join(report))
