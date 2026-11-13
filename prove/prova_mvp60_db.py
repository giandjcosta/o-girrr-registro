"""Prova lo schema soltanto su Postgres locale o su un contenitore di test esplicito."""
import argparse
import os
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SETUP="""
do $$ begin
 if not exists(select 1 from pg_roles where rolname='anon') then create role anon; end if;
 if not exists(select 1 from pg_roles where rolname='authenticated') then create role authenticated; end if;
 if not exists(select 1 from pg_roles where rolname='service_role') then create role service_role; end if;
end $$;
create or replace function public.curva_chk(team text,code text) returns void language plpgsql as $$
begin if team not in ('Oranje VC','stif dc','Apo team') or code is distinct from 'codice-solo-del-test' then raise exception 'Codice non valido'; end if; end $$;
create table if not exists public.derby_sfida(stagione text,da text,a text,nome text,nome_ok boolean,stato text,creata timestamptz);
create or replace view public.derby_attivi as select 'Oranje VC'::text a,'Apo team'::text b,now() dal;
"""
TESTS=r"""
begin;
set local role service_role;
select public.mvp_prepara('2026/27',7,now()+interval '1 hour',
'[{"team":"stif dc","gf":2,"gs":1},{"team":"Oranje VC","gf":2,"gs":1},{"team":"Mariana Coneja","gf":3,"gs":2}]',
'[{"autore":"Redazione","scelta":"stif dc","motivo":"Vittoria in trasferta sulla Grodah."}]',
'[{"autore":"Nonno Cesare","scelta":"Oranje VC","motivo":"Vittoria e due gol in trasferta."},{"autore":"Statistico","scelta":"Mariana Coneja","motivo":"Tre gol alla Apo team."}]',repeat('a',64));
reset role;
do $$ declare j jsonb; begin
 j=public.mvp_stato('2026/27');
 assert j->'votazione'->'classifica'->0->>'team'='stif dc';
 assert (j->'votazione'->'classifica'->0->>'total')::numeric=50;
 assert jsonb_array_length(j->'archivio')=0;
 assert not has_function_privilege('anon','public.mvp_prepara(text,integer,timestamptz,jsonb,jsonb,jsonb,text)','execute');
 assert not has_function_privilege('anon','public.mvp_chiudi(text)','execute');
 assert (select bool_and(relrowsecurity) from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='mvp_private' and c.relkind='r');
end $$;
set local role anon;
do $$ begin
 begin perform public.mvp_vota('Oranje VC','sbagliato','2026/27',7,'stif dc');raise exception 'AUTORIZZAZIONE MANCANTE';exception when raise_exception then assert sqlerrm='Codice non valido';end;
 begin perform 1 from mvp_private.voti;raise exception 'ACCESSO DIRETTO CONSENTITO';exception when insufficient_privilege then null;end;
 begin perform public.mvp_chiudi('2026/27');raise exception 'CHIUSURA PUBBLICA';exception when insufficient_privilege then null;end;
 begin perform public.mvp_vota('Oranje VC','codice-solo-del-test','2026/27',7,'Inesistente');raise exception 'CANDIDATO INESISTENTE';exception when raise_exception then assert sqlerrm='Candidatura non valida';end;
end $$;
select public.mvp_vota('Oranje VC','codice-solo-del-test','2026/27',7,'Oranje VC');
do $$ declare j jsonb;begin
 j=public.mvp_stato('2026/27');
 assert (select sum((x->>'total')::numeric) from jsonb_array_elements(j->'votazione'->'classifica') x)=100;
 assert (j->'votazione'->'classifica'->0->>'humanCount')::int=1;
 assert public.mvp_mio('Oranje VC','codice-solo-del-test','2026/27',7)->>'scelta'='Oranje VC';
 begin perform public.mvp_mio('Apo team','sbagliato','2026/27',7);raise exception 'VOTO ALTRUI';exception when raise_exception then assert sqlerrm='Codice non valido';end;
end $$;
select public.mvp_vota('Oranje VC','codice-solo-del-test','2026/27',7,'stif dc');
do $$ begin assert public.mvp_mio('Oranje VC','codice-solo-del-test','2026/27',7)->>'scelta'='stif dc';end $$;
select public.mvp_vota('Oranje VC','codice-solo-del-test','2026/27',7,null);
do $$ begin assert public.mvp_mio('Oranje VC','codice-solo-del-test','2026/27',7)->>'scelta' is null;end $$;
reset role;
-- La scadenza si controlla dopo il lock, con l'orologio reale, anche in una transazione lunga.
update mvp_private.giornate set chiude=clock_timestamp()+interval '0.02 seconds' where giornata=7;
select pg_sleep(0.03);
set local role anon;
do $$ begin
 begin perform public.mvp_vota('Oranje VC','codice-solo-del-test','2026/27',7,'stif dc');raise exception 'VOTO TARDIVO';exception when raise_exception then assert sqlerrm='Votazione conclusa';end;
end $$;
reset role;
set local role service_role;
select public.mvp_chiudi('2026/27');
select public.mvp_chiudi('2026/27');
reset role;
do $$ declare j jsonb;begin
 j=public.mvp_stato('2026/27');
 assert jsonb_array_length(j->'archivio')=1;
 assert j->'archivio'->0->'classifica'->0->>'team'='stif dc';
 assert (j->'archivio'->0->'classifica'->0->>'total')::numeric=50;
 assert (select count(*) from mvp_private.voti)=0;
 begin perform public.mvp_prepara('2026/27',6,now()-interval '1 day',
 '[{"team":"stif dc"}]','[{"autore":"R","scelta":"stif dc","motivo":"Vittoria."}]','[{"autore":"B","scelta":"stif dc","motivo":"Vittoria."}]',repeat('a',64));raise exception 'PREMIO RETROATTIVO';exception when raise_exception then assert sqlerrm='Non si apre retroattivamente una votazione scaduta';end;
 begin perform public.mvp_prepara('2026/27',8,now()+interval '1 day',null,'[]','[]',repeat('a',64));raise exception 'GIURIA NULL';exception when raise_exception then assert sqlerrm='Giurie e candidature non valide';end;
 assert jsonb_array_length(public.mvp_derby('2026/27')->'coppie')=1;
end $$;
rollback;
select 'PASS - Autenticazione, isolamento, voto/cambio/ritiro, pesi, scadenza, chiusura senza allenatori, archivio e Derby';
"""


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--docker');a=p.parse_args()
    if a.docker:
        if not a.docker.startswith('girrr-'):raise SystemExit('Usare un contenitore esplicitamente dedicato ai test Girrr')
        cmd=['docker','--host=unix:///var/run/docker.sock','exec','-i',a.docker,'psql','-U','postgres','-v','ON_ERROR_STOP=1','-q']
    else:
        if os.environ.get('PGHOST') not in ('localhost','127.0.0.1'):raise SystemExit('Questa prova accetta soltanto PGHOST locale')
        cmd=['psql','-v','ON_ERROR_STOP=1','-q']
    schema=(ROOT/'sql/mvp-tifosi-60.sql').read_text()
    result=subprocess.run(cmd,input=SETUP+schema+schema+TESTS,text=True,capture_output=True)
    if result.returncode:
        print(result.stderr);raise SystemExit(result.returncode)
    print('PASS · Schema eseguito due volte; autenticazione, RLS, giurie, voto, ritiro, scadenza, chiusura e archivio verificati su Postgres reale locale.')


if __name__=='__main__':main()
