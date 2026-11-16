"""Claude, 16 novembre 2026: voti dei personaggi dell'MVP che arrivano durante la settimana (sql/mvp-personaggi-621.sql).
Solo PostgreSQL locale, mai Supabase."""
import json,os,sys,time
from pathlib import Path
import psycopg
R=Path(__file__).resolve().parents[2]
if os.environ.get('PGHOST') not in ('127.0.0.1','localhost'):raise SystemExit('PGHOST deve essere esplicitamente locale')
NAME='girrr621_pers_'+str(os.getpid())+'_'+str(int(time.time()))
ca=dict(host=os.environ['PGHOST'],port=int(os.environ.get('PGPORT','5432')),user=os.environ.get('PGUSER','postgres'),password=os.environ.get('PGPASSWORD',''),dbname='postgres',autocommit=True)
with psycopg.connect(**ca) as a:a.execute('create database '+NAME)
ca['dbname']=NAME
sys.path.insert(0,str(R/'prove'));from prova_mvp60_db import SETUP
ok=[]
def check(l,x):
 assert x,l;ok.append(l);print(l)
try:
 c=psycopg.connect(**ca);c.execute(SETUP)
 c.execute("create table public.curva_post(id bigint primary key,created timestamptz,body text);create table public.curva_poll(post_id bigint primary key,opts text[]);create table public.curva_vote(post_id bigint,team text,opt integer,primary key(post_id,team));create table public.conf_risposta(team text,giornata int,risposte jsonb,libera text,promessa text,pesa text,esito text,creata timestamptz default now());create table public.conf_dopo(team text,giornata int,risposta text,creata timestamptz default now())")
 for f in ('sondaggio-curva.sql','mvp-tifosi-60.sql','votazioni-62-proposta.sql'):c.execute((R/'sql'/f).read_text())
 v=lambda q,a=():c.execute(q,a).fetchone()[0]
 cand=json.dumps([{'team':'A'},{'team':'B'},{'team':'C'}])
 red=json.dumps([{'autore':'Redazione','scelta':'A','motivo':'Vittoria verificata.'}])
 pers=json.dumps([{'autore':'P%d'%i,'scelta':s,'motivo':'Motivo %d verificato.'%i} for i,s in enumerate(['B','B','C','B','C'],1)])
 def prepara(g):c.execute("select public.mvp_prepara('2026/27',%s,clock_timestamp()+interval '1 day',%s,%s,%s,repeat('a',64))",(g,cand,red,pers))
 prepara(7)  # votazione già aperta prima della modifica
 c.execute((R/'sql'/'mvp-personaggi-621.sql').read_text())
 st=v("select public.mvp_stato('2026/27',7)")['votazione']
 check('Votazione già aperta: restano tutti e 5 i personaggi',len(st['personaggi'])==5 and st['personaggi_totali']==5)
 # Nel test le date vengono spostate indietro: anche l'attivazione va spostata, altrimenti la 8ª risulterebbe «già in corso».
 c.execute("update mvp_private.progressivo set dal=now()-interval '200 hours'")
 c.execute("update mvp_private.giornate set creata=now()-interval '300 hours' where giornata=7")
 check('Votazione aperta prima dell\'attivazione: ancora tutti e 5',len(v("select public.mvp_stato('2026/27',7)")['votazione']['personaggi'])==5)
 prepara(8)
 # nuova votazione: durata 6 «unità» di 10 ore, aperta 25 ore fa -> arrivati i voti a 10 e 20 ore (2 su 5)
 c.execute("update mvp_private.giornate set creata=now()-interval '25 hours',chiude=now()+interval '35 hours' where giornata=8")
 st=v("select public.mvp_stato('2026/27',8)")['votazione']
 check('Nuova votazione: arrivati 2 personaggi su 5',len(st['personaggi'])==2 and st['personaggi_totali']==5 and [p['autore'] for p in st['personaggi']]==['P1','P2'])
 cl={x['team']:x for x in st['classifica']}
 check('Classifica provvisoria: conta solo i voti arrivati',cl['B']['personaggi']==2 and cl['C']['personaggi']==0)
 check('Classifica provvisoria: pesi normalizzati sui voti arrivati (A 50, B 50, C 0)',round(float(cl['A']['total']))==50 and round(float(cl['B']['total']))==50 and round(float(cl['C']['total']))==0)
 c.execute("update mvp_private.giornate set creata=now()-interval '1 hour',chiude=now()+interval '59 hours' where giornata=8")
 st=v("select public.mvp_stato('2026/27',8)")['votazione']
 check('Appena aperta: nessun personaggio ancora, nessun errore di divisione',len(st['personaggi'])==0 and round(float(st['classifica'][0]['total']))==50)
 c.execute("update mvp_private.giornate set creata=now()-interval '61 hours',chiude=now()-interval '1 minute' where giornata=8")
 c.execute("select public.mvp_chiudi('2026/27')")
 fin=v("select risultato from mvp_private.giornate where giornata=8")
 f={x['team']:x for x in fin}
 check('Verdetto alla chiusura: contano tutti e 5 i personaggi',f['B']['personaggi']==3 and f['C']['personaggi']==2)
 check('Verdetto identico alla formula di prima (A 50, B 30, C 20)',[round(float(f[t]['total'])) for t in 'ABC']==[50,30,20])
 st=v("select public.mvp_stato('2026/27',8)")['votazione']
 check('Votazione chiusa: elenco completo dei personaggi',len(st['personaggi'])==5)
 c.execute("set role anon")
 try:c.execute("select * from mvp_private.progressivo");check('Tabella privata non leggibile dal browser',False)
 except psycopg.Error:check('Tabella privata non leggibile dal browser',True)
 c.execute("reset role")
 print(len(ok),'prove riuscite')
finally:
 try:c.close()
 except Exception:pass
 with psycopg.connect(**{**ca,'dbname':'postgres'}) as a:a.execute('drop database '+NAME)
