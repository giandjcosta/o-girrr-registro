-- O Girrr 6.2 · Albo › Record (SOLO PROPOSTA, non applicare a Supabase).
-- Dipende da votazioni-62-proposta.sql e mvp-tifosi-60.sql.
-- Non ricostruire voti di giuria per le stagioni senza una fonte editoriale verificata.
begin;

create table if not exists votazioni62_private.giuria_sfide (
 stagione text not null check(stagione ~ '^[0-9]{4}/[0-9]{2}$'),
 giornata integer not null check(giornata between 1 and 60),
 tipo text not null check(tipo in ('redazione','personaggio')),
 autore text not null check(length(btrim(autore)) between 2 and 100),
 scelta text not null check(length(btrim(scelta)) between 1 and 120),
 motivo text not null check(length(btrim(motivo)) between 10 and 600),
 primary key(stagione,giornata,tipo,autore)
);
alter table votazioni62_private.giuria_sfide enable row level security;
revoke all on votazioni62_private.giuria_sfide from public,anon,authenticated;

-- L'ultima giornata vera va confermata dal servizio, non dedotta dai voti.
create table if not exists votazioni62_private.albo_finali (
 stagione text primary key,
 ultima_giornata integer not null check(ultima_giornata between 1 and 60),
 conclusa timestamptz not null default clock_timestamp()
);
alter table votazioni62_private.albo_finali enable row level security;
revoke all on votazioni62_private.albo_finali from public,anon,authenticated;

-- Fonte: preferenze reali inviate dalla redazione in un solo dossier firmato.
-- Il servizio deve prepararle prima della chiusura del sondaggio della giornata.
-- Niente auto-generazione di voti, niente aggiornamento successivo delle preferenze.
create or replace function public.v62_giuria_sfide_prepara(
 p_stagione text,p_giornata integer,p_voti jsonb
) returns void language plpgsql security definer set search_path='' as $$
declare s votazioni62_private.sondaggi;
begin
 if p_stagione !~ '^[0-9]{4}/[0-9]{2}$' or p_giornata not between 1 and 60
    or jsonb_typeof(p_voti) is distinct from 'array'
    or jsonb_array_length(p_voti) not between 2 and 110
 then raise exception 'Dossier della giuria non valido'; end if;
 select * into s from votazioni62_private.sondaggi
 where stagione=p_stagione and origine='sfida' and giornata=p_giornata
 for update;
 if not found then raise exception 'Sondaggio della giornata non inizializzato'; end if;
 if exists(
  select 1 from pg_catalog.jsonb_array_elements(p_voti) e
  where e->>'tipo' not in ('redazione','personaggio')
     or nullif(btrim(e->>'autore'),'') is null
     or length(btrim(e->>'autore')) not between 2 and 100
     or not(s.scelte ? (e->>'scelta'))
     or length(btrim(e->>'motivo')) not between 10 and 600
 ) or (
  select count(*) from pg_catalog.jsonb_array_elements(p_voti) e
 ) <> (
  select count(distinct (e->>'tipo',e->>'autore')) from pg_catalog.jsonb_array_elements(p_voti) e
 ) or not exists(
  select 1 from pg_catalog.jsonb_array_elements(p_voti) e where e->>'tipo'='redazione'
 ) or not exists(
  select 1 from pg_catalog.jsonb_array_elements(p_voti) e where e->>'tipo'='personaggio'
 ) then raise exception 'Preferenze di giuria incomplete o non valide'; end if;
 if exists(select 1 from votazioni62_private.giuria_sfide
           where stagione=p_stagione and giornata=p_giornata) then
  if (select count(*) from votazioni62_private.giuria_sfide
      where stagione=p_stagione and giornata=p_giornata)=jsonb_array_length(p_voti)
     and not exists(
       select 1 from pg_catalog.jsonb_array_elements(p_voti) e
       where not exists (
        select 1 from votazioni62_private.giuria_sfide v
        where v.stagione=p_stagione and v.giornata=p_giornata
          and v.tipo=e->>'tipo' and v.autore=e->>'autore'
          and v.scelta=e->>'scelta' and v.motivo=e->>'motivo'
       )
     ) then return; end if;
  raise exception 'Giuria già pubblicata: scelte immutabili';
 end if;
 if s.chiuso is not null or s.aperto is null or clock_timestamp()>=s.chiude
 then raise exception 'Giuria non pubblicabile retroattivamente'; end if;
 insert into votazioni62_private.giuria_sfide(stagione,giornata,tipo,autore,scelta,motivo)
 select p_stagione,p_giornata,e->>'tipo',e->>'autore',e->>'scelta',e->>'motivo'
 from pg_catalog.jsonb_array_elements(p_voti) e;
end $$;

create or replace function public.v62_albo_finalizza(p_stagione text,p_ultima_giornata integer)
returns void language plpgsql security definer set search_path='' as $$
declare precedente integer;
begin
 if p_stagione !~ '^[0-9]{4}/[0-9]{2}$' or p_ultima_giornata not between 1 and 60
 then raise exception 'Stagione o giornata finale non valida'; end if;
 select ultima_giornata into precedente from votazioni62_private.albo_finali
 where stagione=p_stagione for update;
 if found then
  if precedente<>p_ultima_giornata then raise exception 'Fine stagione già certificata'; end if;
  return;
 end if;
 if not exists(select 1 from votazioni62_private.sondaggi
               where stagione=p_stagione and origine='sfida' and giornata=p_ultima_giornata)
 then raise exception 'Ultima giornata non registrata nel catalogo'; end if;
 if exists(select 1 from votazioni62_private.sondaggi
   where stagione=p_stagione and origine='sfida' and
         (giornata>p_ultima_giornata or clock_timestamp()<chiude))
 then raise exception 'Il calendario o le votazioni non sono concluse'; end if;
 if exists(select 1 from mvp_private.giornate
   where stagione=p_stagione and (giornata>p_ultima_giornata or chiusa is null))
 then raise exception 'Verdetti MVP ancora aperti'; end if;
 insert into votazioni62_private.albo_finali(stagione,ultima_giornata)
 values(p_stagione,p_ultima_giornata) on conflict do nothing;
end $$;

-- Contratto richiesto dall'Albo di Claude:
-- {stagione,mvp:[{giornata,team,chiusa}],
--  mvp_classifica:[{team,mvp,giornate}],
--  partite:[{id,giornata,partita,voti:{allenatori,redazione,personaggi,totale}}]|null,
--  stagione_conclusa:boolean}
--
-- I voti allenatori della vecchia tabella hanno soltanto (giornata,team).
-- Per non attribuire voti storici alla stagione sbagliata, questa fonte è
-- certificabile solo per 2026/27, finché non esiste la migrazione stagionale.
-- Le giornate senza un dossier di entrambe le giurie NON diventano zeri fittizi.
create or replace function public.v62_albo(p_stagione text)
returns jsonb language sql stable security definer set search_path='' as $$
 with vincitori as (
  select g.giornata,g.risultato->0->>'team' as team,g.chiusa
  from mvp_private.giornate g
  where g.stagione=p_stagione and g.chiusa is not null
    and g.risultato is not null and g.risultato->0->>'team' is not null
 ),
 classifica as (
  select team,count(*)::integer mvp,
    pg_catalog.jsonb_agg(giornata order by giornata) giornate,
    max(giornata) ultima
  from vincitori group by team
 ),
 completati as (
  select s.id,s.stagione,s.giornata,s.scelte
  from votazioni62_private.sondaggi s
  where s.stagione=p_stagione and s.origine='sfida'
    and s.aperto is not null and s.chiude<=clock_timestamp()
 ),
 scelte as (
  select s.id,s.stagione,s.giornata,o.scelta,o.posizione,
  (select count(*)::integer from sondaggio_private.voti v
   where v.giornata=s.giornata and v.scelta=o.scelta) allenatori,
  (select count(*)::integer from votazioni62_private.giuria_sfide v
   where v.stagione=s.stagione and v.giornata=s.giornata
     and v.tipo='redazione' and v.scelta=o.scelta) redazione,
  (select count(*)::integer from votazioni62_private.giuria_sfide v
   where v.stagione=s.stagione and v.giornata=s.giornata
     and v.tipo='personaggio' and v.scelta=o.scelta) personaggi
  from completati s cross join lateral
  pg_catalog.jsonb_array_elements_text(s.scelte) with ordinality o(scelta,posizione)
 ),
 conteggi as (
  select *,allenatori+redazione+personaggi as totale from scelte
 )
 select pg_catalog.jsonb_build_object(
  'stagione',p_stagione,
  'mvp',coalesce((select pg_catalog.jsonb_agg(
    pg_catalog.jsonb_build_object('giornata',giornata,'team',team,'chiusa',chiusa)
    order by giornata) from vincitori),'[]'::jsonb),
  'mvp_classifica',coalesce((select pg_catalog.jsonb_agg(
    pg_catalog.jsonb_build_object('team',team,'mvp',mvp,'giornate',giornate)
    order by mvp desc,ultima desc,team) from classifica),'[]'::jsonb),
  'partite',case
    when p_stagione<>'2026/27' or not exists(select 1 from completati)
      or exists (
        select 1 from completati s where
        not exists (select 1 from votazioni62_private.giuria_sfide v
                    where v.stagione=s.stagione and v.giornata=s.giornata and v.tipo='redazione')
        or not exists (select 1 from votazioni62_private.giuria_sfide v
                       where v.stagione=s.stagione and v.giornata=s.giornata and v.tipo='personaggio')
      ) then null::jsonb
    else (select coalesce(pg_catalog.jsonb_agg(
       pg_catalog.jsonb_build_object(
        'id',id,'giornata',giornata,'partita',scelta,
        'voti',pg_catalog.jsonb_build_object('allenatori',allenatori,
                   'redazione',redazione,'personaggi',personaggi,'totale',totale))
       order by totale desc,giornata desc,posizione),'[]'::jsonb)
       from conteggi)
    end,
  'stagione_conclusa',exists(
   select 1 from votazioni62_private.albo_finali f where f.stagione=p_stagione)
 )
$$;

revoke all on function public.v62_giuria_sfide_prepara(text,integer,jsonb),
 public.v62_albo_finalizza(text,integer),public.v62_albo(text) from public,anon,authenticated;
grant execute on function public.v62_giuria_sfide_prepara(text,integer,jsonb),
 public.v62_albo_finalizza(text,integer) to service_role;
grant execute on function public.v62_albo(text) to anon,authenticated,service_role;
commit;
