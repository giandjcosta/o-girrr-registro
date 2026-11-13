-- Installazione MVP dei tifosi 6.0. Preparata e provata localmente, NON applicata alla lega.
-- Autenticazione compatibile con la Curva: curva_chk(team, code). Nessun codice salvato nei voti.
-- Schema privato, RLS e nessun accesso diretto. Le giurie automatiche sono pubbliche;
-- i voti individuali degli allenatori si leggono soltanto con il codice della propria squadra.
begin;
create schema if not exists mvp_private;
revoke all on schema mvp_private from public, anon, authenticated;
create table if not exists mvp_private.giornate(
 stagione text not null check (stagione ~ '^\d{4}/\d{2}$'),
 giornata integer not null check (giornata between 1 and 60),
 chiude timestamptz not null,
 candidati jsonb not null,
 redazione jsonb not null,
 personaggi jsonb not null,
 firma text not null,
 creata timestamptz not null default clock_timestamp(),
 chiusa timestamptz,
 risultato jsonb,
 primary key(stagione,giornata)
);
create table if not exists mvp_private.voti(
 stagione text not null,
 giornata integer not null,
 team text not null,
 scelta text not null,
 aggiornato timestamptz not null default clock_timestamp(),
 primary key(stagione,giornata,team),
 foreign key(stagione,giornata) references mvp_private.giornate(stagione,giornata)
);
alter table mvp_private.giornate enable row level security;
alter table mvp_private.voti enable row level security;
revoke all on all tables in schema mvp_private from public,anon,authenticated;

create or replace function mvp_private.classifica(p_stagione text,p_giornata integer)
returns jsonb language sql stable security invoker set search_path='' as $f$
 with w as (select * from mvp_private.giornate where stagione=p_stagione and giornata=p_giornata),
 h as (select count(*)::numeric n from mvp_private.voti where stagione=p_stagione and giornata=p_giornata),
 conteggi as (
 select c,
  (select count(*) from jsonb_array_elements(w.redazione) r where r->>'scelta'=c->>'team')::numeric red,
  (select count(*) from jsonb_array_elements(w.personaggi) r where r->>'scelta'=c->>'team')::numeric bot,
  (select count(*) from mvp_private.voti v where v.stagione=p_stagione and v.giornata=p_giornata and v.scelta=c->>'team')::numeric umani,
  h.n nh,jsonb_array_length(w.redazione)::numeric nr,jsonb_array_length(w.personaggi)::numeric nb
 from w cross join h cross join lateral jsonb_array_elements(w.candidati) c),
 punti as (select *,100*((case when nh>0 then .4 else .5 end)*red/nr+(case when nh>0 then .4 else .5 end)*bot/nb+(case when nh>0 then .2*umani/nh else 0 end)) totale from conteggi)
 select coalesce(jsonb_agg(c || jsonb_build_object('red',red,'personaggi',bot,'umani',umani,'total',totale,'humanCount',nh) order by totale desc,red desc,lower(c->>'team'),c->>'team'),'[]'::jsonb) from punti
 $f$;

create or replace function public.mvp_stato(p_stagione text,p_giornata integer default null)
returns jsonb language sql stable security definer set search_path='' as $f$
 with w as (select * from mvp_private.giornate where stagione=p_stagione and (p_giornata is null or giornata=p_giornata) order by giornata desc limit 1)
 select jsonb_build_object('votazione',
 (select jsonb_build_object('stagione',stagione,'giornata',giornata,'chiude',chiude,'chiusa',chiusa,'redazione',redazione,'personaggi',personaggi,
 'classifica',coalesce(risultato,mvp_private.classifica(stagione,giornata)),'firma',firma) from w),
 'archivio',coalesce((select jsonb_agg(jsonb_build_object('stagione',stagione,'giornata',giornata,'chiusa',chiusa,'classifica',risultato,'redazione',redazione) order by giornata desc) from mvp_private.giornate where stagione=p_stagione and chiusa is not null),'[]'::jsonb))
 $f$;

create or replace function public.mvp_mio(p_team text,p_code text,p_stagione text,p_giornata integer)
returns jsonb language plpgsql security definer set search_path='' as $f$
begin
 perform public.curva_chk(p_team,p_code);
 return jsonb_build_object('scelta',(select scelta from mvp_private.voti where stagione=p_stagione and giornata=p_giornata and team=p_team));
end $f$;

create or replace function public.mvp_vota(p_team text,p_code text,p_stagione text,p_giornata integer,p_scelta text default null)
returns jsonb language plpgsql security definer set search_path='' as $f$
declare w mvp_private.giornate;
begin
 perform public.curva_chk(p_team,p_code);
 select * into w from mvp_private.giornate where stagione=p_stagione and giornata=p_giornata for update;
 if not found then raise exception 'Votazione non disponibile'; end if;
 if w.chiusa is not null or clock_timestamp()>=w.chiude then raise exception 'Votazione conclusa'; end if;
 if p_scelta is null then
  delete from mvp_private.voti where stagione=p_stagione and giornata=p_giornata and team=p_team;
 else
  if not exists(select 1 from jsonb_array_elements(w.candidati) c where c->>'team'=p_scelta) then raise exception 'Candidatura non valida'; end if;
  insert into mvp_private.voti(stagione,giornata,team,scelta) values(p_stagione,p_giornata,p_team,p_scelta)
  on conflict(stagione,giornata,team) do update set scelta=excluded.scelta,aggiornato=clock_timestamp();
 end if;
 return public.mvp_stato(p_stagione,p_giornata)||jsonb_build_object('scelta',p_scelta);
end $f$;

-- Solo il servizio server può aprire e chiudere una votazione.
create or replace function public.mvp_prepara(p_stagione text,p_giornata integer,p_chiude timestamptz,p_candidati jsonb,p_redazione jsonb,p_personaggi jsonb,p_firma text)
returns jsonb language plpgsql security definer set search_path='' as $f$
declare w mvp_private.giornate;j jsonb;
begin
 if jsonb_typeof(p_candidati) is distinct from 'array' or jsonb_typeof(p_redazione) is distinct from 'array' or jsonb_typeof(p_personaggi) is distinct from 'array' then raise exception 'Giurie e candidature non valide'; end if;
 if jsonb_array_length(p_candidati) not between 1 and 3 or jsonb_array_length(p_redazione) not between 1 and 10 or jsonb_array_length(p_personaggi) not between 1 and 100 then raise exception 'Numero di candidature o voti non valido'; end if;
 if exists(select 1 from jsonb_array_elements(p_candidati) c where nullif(btrim(c->>'team'),'') is null or length(c->>'team')>120) or (select count(distinct c->>'team') from jsonb_array_elements(p_candidati) c)<>jsonb_array_length(p_candidati) then raise exception 'Candidature duplicate o non valide'; end if;
 foreach j in array array[p_redazione,p_personaggi] loop
  if exists(select 1 from jsonb_array_elements(j) r where nullif(btrim(r->>'autore'),'') is null or nullif(btrim(r->>'motivo'),'') is null or length(r->>'motivo')>600 or not exists(select 1 from jsonb_array_elements(p_candidati) c where c->>'team'=r->>'scelta')) then raise exception 'Preferenza di giuria non valida'; end if;
  if (select count(distinct r->>'autore') from jsonb_array_elements(j) r)<>jsonb_array_length(j) then raise exception 'Un solo voto per membro della giuria'; end if;
 end loop;
 if p_firma is null or p_firma !~ '^[a-f0-9]{64}$' then raise exception 'Impronta dei fatti non valida'; end if;
 -- Il lock per stagione/giornata rende atomica anche la prima creazione concorrente.
 perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended(p_stagione||':'||p_giornata::text,0));
 select * into w from mvp_private.giornate where stagione=p_stagione and giornata=p_giornata for update;
 if found then
  if w.firma=p_firma and w.candidati=p_candidati and w.redazione=p_redazione and w.personaggi=p_personaggi and w.chiude=p_chiude then return public.mvp_stato(p_stagione,p_giornata); end if;
  if w.chiusa is not null or clock_timestamp()>=w.chiude then raise exception 'Verdetto conservato: revisione esplicita necessaria'; end if;
  if exists(select 1 from mvp_private.voti where stagione=p_stagione and giornata=p_giornata) then raise exception 'Votazione iniziata: revisione esplicita necessaria'; end if;
 end if;
 if p_chiude is null or p_chiude<=clock_timestamp() then raise exception 'Non si apre retroattivamente una votazione scaduta'; end if;
 insert into mvp_private.giornate(stagione,giornata,chiude,candidati,redazione,personaggi,firma)
 values(p_stagione,p_giornata,p_chiude,p_candidati,p_redazione,p_personaggi,p_firma)
 on conflict(stagione,giornata) do update set chiude=excluded.chiude,candidati=excluded.candidati,redazione=excluded.redazione,personaggi=excluded.personaggi,firma=excluded.firma;
 return public.mvp_stato(p_stagione,p_giornata);
end $f$;

-- Il registro ufficiale, senza chiamare derby_stato (che fa anche scadere le sfide).
create or replace function public.mvp_derby(p_stagione text)
returns jsonb language sql stable security definer set search_path='' as $f$
 select jsonb_build_object('stagione',p_stagione,'verificato',current_timestamp,
 'coppie',coalesce(jsonb_agg(jsonb_build_object('a',d.a,'b',d.b,'dal',d.dal,'n',coalesce(
 (select s.nome from public.derby_sfida s where s.stagione=p_stagione and s.stato='accettata' and s.nome_ok and ((s.da=d.a and s.a=d.b) or (s.da=d.b and s.a=d.a)) order by s.creata desc limit 1),'Derby'))),'[]'::jsonb))
 from public.derby_attivi d
 $f$;

create or replace function public.mvp_chiudi(p_stagione text)
returns jsonb language plpgsql security definer set search_path='' as $f$
declare w record;ris jsonb;
begin
 for w in select stagione,giornata from mvp_private.giornate where stagione=p_stagione and chiusa is null and chiude<=clock_timestamp() for update skip locked loop
  ris=mvp_private.classifica(w.stagione,w.giornata);
  update mvp_private.giornate set chiusa=clock_timestamp(),risultato=ris where stagione=w.stagione and giornata=w.giornata;
 end loop;
 return public.mvp_stato(p_stagione,null);
end $f$;

revoke all on all functions in schema mvp_private from public,anon,authenticated;
revoke all on function public.mvp_stato(text,integer),public.mvp_mio(text,text,text,integer),public.mvp_vota(text,text,text,integer,text),public.mvp_prepara(text,integer,timestamptz,jsonb,jsonb,jsonb,text),public.mvp_chiudi(text),public.mvp_derby(text) from public,anon,authenticated;
grant execute on function public.mvp_stato(text,integer),public.mvp_mio(text,text,text,integer),public.mvp_vota(text,text,text,integer,text),public.mvp_derby(text) to anon,authenticated,service_role;
grant execute on function public.mvp_prepara(text,integer,timestamptz,jsonb,jsonb,jsonb,text),public.mvp_chiudi(text) to service_role;
commit;
