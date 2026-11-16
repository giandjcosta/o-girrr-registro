-- 6.2.1 · MVP dei tifosi: i voti dei personaggi arrivano uno alla volta durante la settimana (Claude, 16 novembre 2026, richiesta di Gianluca).
-- La redazione vota all'apertura. Il voto del personaggio n-esimo (su N) arriva a creata + n/(N+1) della durata della votazione,
-- quindi l'ultimo arriva prima della chiusura. La classifica provvisoria conta solo i voti arrivati; alla chiusura
-- (mvp_chiudi) sono arrivati tutti, quindi il verdetto è identico a prima. Vale solo per le votazioni aperte DOPO
-- l'applicazione (giornate.creata >= progressivo_dal): una votazione già in corso non cambia.
-- Dipende da mvp-tifosi-60.sql. Applicare solo con il «Vai» di Gianluca.
begin;
create table if not exists mvp_private.progressivo(id boolean primary key default true check(id),dal timestamptz not null);
insert into mvp_private.progressivo values(true,clock_timestamp()) on conflict do nothing;
alter table mvp_private.progressivo enable row level security;
revoke all on mvp_private.progressivo from public,anon,authenticated;

-- Voti dei personaggi già arrivati (tutti per le votazioni chiuse o precedenti all'attivazione).
create or replace function mvp_private.personaggi_arrivati(p_stagione text,p_giornata integer)
returns jsonb language sql stable set search_path='' as $$
 select coalesce((
  select jsonb_agg(r order by ord)
  from mvp_private.giornate w
  cross join lateral jsonb_array_elements(w.personaggi) with ordinality a(r,ord)
  where w.stagione=p_stagione and w.giornata=p_giornata
    and (w.chiusa is not null
      or w.creata<(select dal from mvp_private.progressivo where id)
      or now()>=w.creata+(w.chiude-w.creata)*ord/(jsonb_array_length(w.personaggi)+1))
 ),'[]'::jsonb)
$$;

create or replace function mvp_private.classifica(p_stagione text,p_giornata integer)
returns jsonb language sql stable set search_path='' as $function$
 with w as (select * from mvp_private.giornate where stagione=p_stagione and giornata=p_giornata),
 pa as (select mvp_private.personaggi_arrivati(p_stagione,p_giornata) p),
 h as (select count(*)::numeric n from mvp_private.voti where stagione=p_stagione and giornata=p_giornata),
 conteggi as (
 select c,
  (select count(*) from jsonb_array_elements(w.redazione) r where r->>'scelta'=c->>'team')::numeric red,
  (select count(*) from jsonb_array_elements(pa.p) r where r->>'scelta'=c->>'team')::numeric bot,
  (select count(*) from mvp_private.voti v where v.stagione=p_stagione and v.giornata=p_giornata and v.scelta=c->>'team')::numeric umani,
  h.n nh,jsonb_array_length(w.redazione)::numeric nr,jsonb_array_length(pa.p)::numeric nb
 from w cross join pa cross join h cross join lateral jsonb_array_elements(w.candidati) c),
 punti as (select *,100*((case when nh>0 then .4 else .5 end)*red/nr+(case when nb>0 then (case when nh>0 then .4 else .5 end)*bot/nb else 0 end)+(case when nh>0 then .2*umani/nh else 0 end)) totale from conteggi)
 select coalesce(jsonb_agg(c || jsonb_build_object('red',red,'personaggi',bot,'umani',umani,'total',totale,'humanCount',nh) order by totale desc,red desc,lower(c->>'team'),c->>'team'),'[]'::jsonb) from punti
$function$;

-- Come prima, ma «personaggi» elenca solo i voti arrivati e «personaggi_totali» dice quanti sono in tutto.
create or replace function public.mvp_stato(p_stagione text,p_giornata integer default null)
returns jsonb language sql stable security definer set search_path='' as $function$
 with w as (select * from mvp_private.giornate where stagione=p_stagione and (p_giornata is null or giornata=p_giornata) order by giornata desc limit 1)
 select jsonb_build_object('votazione',
 (select jsonb_build_object('stagione',stagione,'giornata',giornata,'chiude',chiude,'chiusa',chiusa,'redazione',redazione,
   'personaggi',mvp_private.personaggi_arrivati(stagione,giornata),'personaggi_totali',jsonb_array_length(personaggi),
   'classifica',coalesce(risultato,mvp_private.classifica(stagione,giornata)),'firma',firma) from w),
 'archivio',coalesce((select jsonb_agg(jsonb_build_object('stagione',stagione,'giornata',giornata,'chiusa',chiusa,'classifica',risultato,'redazione',redazione) order by giornata desc) from mvp_private.giornate where stagione=p_stagione and chiusa is not null),'[]'::jsonb))
$function$;

revoke all on all functions in schema mvp_private from public,anon,authenticated;
commit;
