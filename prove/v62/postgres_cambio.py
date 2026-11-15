"""Claude, 15 novembre 2026: «Cambia il mio voto» su PostgreSQL locale (mai Supabase).
Un solo voto per squadra; una seconda richiesta normale non cambia nulla; il pulsante sì, finché la votazione è aperta."""
import json,os,sys,time
from pathlib import Path
import psycopg
R=Path(__file__).resolve().parents[2]
if os.environ.get('PGHOST') not in ('127.0.0.1','localhost'):raise SystemExit('PGHOST deve essere esplicitamente locale')
NAME='girrr62_cambio_'+str(os.getpid())+'_'+str(int(time.time()))
ca=dict(host=os.environ['PGHOST'],port=int(os.environ.get('PGPORT','5432')),user=os.environ.get('PGUSER','postgres'),password=os.environ.get('PGPASSWORD',''),dbname='postgres',autocommit=True)
with psycopg.connect(**ca) as a:a.execute('create database '+NAME)
ca['dbname']=NAME
sys.path.insert(0,str(R/'prove'));from prova_mvp60_db import SETUP
c=psycopg.connect(**ca);c.execute(SETUP)
c.execute("create table public.curva_post(id bigint primary key,created timestamptz,body text);create table public.curva_poll(post_id bigint primary key,opts text[]);create table public.curva_vote(post_id bigint,team text,opt integer,primary key(post_id,team));create table public.conf_risposta(team text,giornata int,risposte jsonb,libera text,promessa text,pesa int,esito text,primary key(team,giornata));create table public.conf_dopo(team text,giornata int,risposta jsonb,creata timestamptz default now(),primary key(team,giornata));")
for f in ('sondaggio-curva.sql','mvp-tifosi-60.sql','votazioni-62-proposta.sql','finestre-62-proposta.sql'):c.execute((R/'sql'/f).read_text())
code='codice-solo-del-test';v=lambda q,a=():c.execute(q,a).fetchone()[0];ok=[]
def check(l,x):
 assert x,l;ok.append(l)
c.execute("select public.mvp_prepara('2026/27',7,clock_timestamp()+interval '1 day',%s,%s,%s,repeat('a',64))",(json.dumps([{'team':'stif dc'},{'team':'Oranje VC'}]),json.dumps([{'autore':'Redazione','scelta':'stif dc','motivo':'Vittoria verificata.'}]),json.dumps([{'autore':'Personaggio','scelta':'Oranje VC','motivo':'Vittoria verificata.'}])))
c.execute("select public.v62_prepara('sfida:2026/27:8','2026/27','sfida','8',8,'Sfida','[\"A\",\"B\"]',clock_timestamp()-interval '1 hour',clock_timestamp()+interval '1 day')")
# Sfida
v("select public.v62_vota('sfida:2026/27:8','Apo team',%s,'A')",(code,))
check('Sfida: seconda richiesta normale non cambia',v("select public.v62_vota('sfida:2026/27:8','Apo team',%s,'B')->>'mia_scelta'",(code,))=='A')
check('Sfida: il pulsante cambia il voto',v("select public.v62_vota('sfida:2026/27:8','Apo team',%s,'B',true)->>'mia_scelta'",(code,))=='B')
check('Sfida: resta un solo voto della squadra',v("select count(*) from sondaggio_private.voti where giornata=8 and team='Apo team'")==1)
check('Sfida: Curva e Girrr Sport leggono lo stesso voto',v("select public.v62_sondaggi('2026/27','Apo team',%s)->'aperti'->0->>'mia_scelta'",(code,))=='B')
try:
 c.execute("select public.v62_vota('sfida:2026/27:8','Apo team',%s,'Z',true)",(code,));check('Sfida: scelta non valida rifiutata',False)
except psycopg.Error:check('Sfida: scelta non valida rifiutata anche nel cambio',True)
try:
 c.execute("select public.v62_vota('sfida:2026/27:8','Apo team','codice-sbagliato','A',true)");check('Codice errato',False)
except psycopg.Error:check('Cambio negato con un codice errato',True)
# Post della Curva
c.execute("insert into public.curva_post values(1,clock_timestamp(),'Chi vince?');insert into public.curva_poll values(1,array['Uno','Due'])")
v("select public.v62_vota('post:2026/27:1','Oranje VC',%s,'Uno')",(code,))
v("select public.v62_vota('post:2026/27:1','Oranje VC',%s,'Due')",(code,))
check('Post: seconda richiesta normale non cambia',v("select opt from public.curva_vote where post_id=1 and team='Oranje VC'")==0)
v("select public.v62_vota('post:2026/27:1','Oranje VC',%s,'Due',true)",(code,))
check('Post: il pulsante cambia il voto, una sola riga',v("select opt from public.curva_vote where post_id=1 and team='Oranje VC'")==1 and v("select count(*) from public.curva_vote where post_id=1")==1)
# MVP
v("select public.mvp_vota('Apo team',%s,'2026/27',7,'stif dc')",(code,))
check('MVP: seconda richiesta normale non cambia',v("select public.mvp_vota('Apo team',%s,'2026/27',7,'Oranje VC')->>'scelta'",(code,))=='stif dc')
check('MVP: il pulsante cambia il voto',v("select public.mvp_vota('Apo team',%s,'2026/27',7,'Oranje VC',true)->>'scelta'",(code,))=='Oranje VC')
check('MVP: un solo voto della squadra',v("select count(*) from mvp_private.voti where giornata=7 and team='Apo team'")==1)
# Chiusa
c.execute("update mvp_private.giornate set chiude=clock_timestamp()-interval '1 minute' where giornata=7")
try:
 c.execute("select public.mvp_vota('Apo team',%s,'2026/27',7,'stif dc',true)",(code,));check('MVP chiusa',False)
except psycopg.Error:check('MVP: a votazione chiusa il cambio è rifiutato',True)
c.close()
with psycopg.connect(**{**ca,'dbname':'postgres'}) as a:a.execute('drop database '+NAME)
print('\n'.join(ok));print(len(ok),'prove riuscite')
