-- BOZZA 6.2: solo preparazione. Non eseguire sul progetto della Lega senza Vai.
-- Dipende da sondaggio-curva.sql e mvp-tifosi-60.sql già esistenti.
-- curva_chk è l'autenticazione a codice della Lega: non si usa auth.uid(),
-- perché gli allenatori non sono utenti Supabase Auth.
begin;
create schema if not exists votazioni62_private;
revoke all on schema votazioni62_private from public,anon,authenticated;
-- Un solo istante di attivazione: le finestre dei post valgono per nuove aperture.
create table if not exists votazioni62_private.attivazione(id boolean primary key default true check(id),post_dal timestamptz not null);
insert into votazioni62_private.attivazione values(true,clock_timestamp()) on conflict do nothing;
alter table votazioni62_private.attivazione enable row level security;
revoke all on votazioni62_private.attivazione from public,anon,authenticated;
create or replace function votazioni62_private.post_scadenza(p_creato timestamptz)
returns timestamptz language sql stable set search_path='' as $$
 select case when p_creato>=post_dal then p_creato+interval '24 hours' else null end from votazioni62_private.attivazione where id
$$;
create table if not exists votazioni62_private.sondaggi (
 id text primary key,
 stagione text not null,
 origine text not null check(origine in ('sfida','post')),
 fonte text not null,
 giornata integer not null check(giornata between 1 and 60),
 titolo text not null,
 scelte jsonb not null check(jsonb_typeof(scelte)='array' and jsonb_array_length(scelte)>1),
 aperto timestamptz,
 chiude timestamptz not null check((aperto is null or chiude>aperto)),
 chiuso timestamptz,
 unique(stagione,origine,fonte)
);
create index if not exists sondaggi62_stagione_chiude on votazioni62_private.sondaggi(stagione,chiude desc,id);
alter table votazioni62_private.sondaggi enable row level security;
revoke all on all tables in schema votazioni62_private from public,anon,authenticated;

-- Catalogo unico. La chiusura effettiva dipende anche dall'orologio del server,
-- senza aspettare il prossimo passaggio dell'automazione. Nessuna cancellazione.
create or replace function public.v62_sondaggi(p_stagione text,p_team text default null,p_code text default null)
returns jsonb language plpgsql security definer set search_path='' as $$
begin
 if p_team is not null then perform public.curva_chk(p_team,p_code); end if;
 if p_stagione !~ '^\d{4}/\d{2}$' then raise exception 'Stagione non valida'; end if;
 return (with catalogo as (
 select id,stagione,origine,fonte,giornata,titolo,scelte,aperto,chiude,chiuso from votazioni62_private.sondaggi where stagione=p_stagione
 union all
 select 'post:'||p_stagione||':'||po.post_id::text,p_stagione,'post',po.post_id::text,null::integer,left(p.body,160),to_jsonb(po.opts),p.created,votazioni62_private.post_scadenza(p.created),null::timestamptz
 from public.curva_poll po join public.curva_post p on p.id=po.post_id
 where p.created>=(make_date(left(p_stagione,4)::int,7,1)::timestamp at time zone 'Europe/Rome') and p.created<(make_date(left(p_stagione,4)::int+1,7,1)::timestamp at time zone 'Europe/Rome')
 and not exists(select 1 from votazioni62_private.sondaggi s where s.stagione=p_stagione and s.origine='post' and s.fonte=po.post_id::text)
 ),righe as (
 select s.*,s.chiuso is not null or coalesce(clock_timestamp()>=s.chiude,false) as concluso,
 jsonb_build_object('id',s.id,'giornata',s.giornata,'titolo',s.titolo,'origine',s.origine,'fonte',s.fonte,'scelte',s.scelte,
 'aperto',s.aperto,'chiude',s.chiude,'commenti',case when s.origine='sfida' then public.sondaggio_stato(s.giornata)->'commenti' else '[]'::jsonb end,'chiuso',s.chiuso is not null or coalesce(clock_timestamp()>=s.chiude,false),
 'mia_scelta',case when s.origine='post' then (select po.opts[v.opt+1] from public.curva_vote v join public.curva_poll po on po.post_id=v.post_id where v.post_id=s.fonte::bigint and v.team=p_team) else (select v.scelta from sondaggio_private.voti v where v.giornata=s.giornata and v.team=p_team) end,
 'conteggi',case when s.origine='post' then coalesce((select jsonb_object_agg(scelta,n) from (select po.opts[v.opt+1] scelta,count(*) n from public.curva_vote v join public.curva_poll po on po.post_id=v.post_id where v.post_id=s.fonte::bigint group by po.opts[v.opt+1]) z),'{}'::jsonb) else coalesce((select jsonb_object_agg(scelta,n) from (select scelta,count(*) n from sondaggio_private.voti where giornata=s.giornata group by scelta) z),'{}'::jsonb) end) as dati
 from catalogo s where (s.aperto is null or s.aperto<=clock_timestamp()))
 select jsonb_build_object('server_ora',clock_timestamp(),'aperti',coalesce((select jsonb_agg(dati order by aperto desc,id) from righe where not concluso),'[]'::jsonb),
 'chiusi',coalesce((select jsonb_agg(dati order by chiude desc,id) from (select * from righe where concluso order by chiude desc,id limit 2) z),'[]'::jsonb)));
end $$;

-- Claude, 15 novembre 2026 (Gianluca): un solo voto, condiviso fra Curva e Girrr Sport. Una seconda richiesta
-- normale non lo cambia («Hai già votato»); lo cambia solo il pulsante «Cambia il mio voto» (p_cambia=true),
-- finché la votazione è aperta e con una scelta valida. Il voto resta uno per squadra.
create or replace function votazioni62_private.cambia_post(p_team text,p_post bigint,p_opt integer)
returns void language plpgsql security definer set search_path='' as $$
declare op text[]; t timestamptz;
begin
 select po.opts,p.created into op,t from public.curva_poll po join public.curva_post p on p.id=po.post_id where po.post_id=p_post for update of po;
 if not found then raise exception 'Sondaggio non trovato'; end if;
 if clock_timestamp()>=votazioni62_private.post_scadenza(t) then raise exception 'Il sondaggio è chiuso'; end if;
 if p_opt is null or p_opt<0 or p_opt>=array_length(op,1) then raise exception 'Risposta non valida'; end if;
 insert into public.curva_vote(post_id,team,opt) values(p_post,p_team,p_opt) on conflict(post_id,team) do update set opt=excluded.opt;
end $$;
drop function if exists public.v62_vota(text,text,text,text);
create or replace function public.v62_vota(p_id text,p_team text,p_code text,p_scelta text,p_cambia boolean default false)
returns jsonb language plpgsql security definer set search_path='' as $$
declare s votazioni62_private.sondaggi; precedente text; op text[]; prima timestamptz; fonte_id bigint; scelta_indice integer;
begin
 perform public.curva_chk(p_team,p_code);
 select * into s from votazioni62_private.sondaggi where id=p_id for update;
 if not found then
  if p_id !~ '^post:[0-9]{4}/[0-9]{2}:[0-9]+$' then raise exception 'Sondaggio non disponibile'; end if;
  fonte_id=split_part(p_id,':',3)::bigint;
  select po.opts,p.created into op,prima from public.curva_poll po join public.curva_post p on p.id=po.post_id where po.post_id=fonte_id;
  if not found or extract(year from prima at time zone 'Europe/Rome')::int-(case when extract(month from prima at time zone 'Europe/Rome')<7 then 1 else 0 end)<>substring(p_id from 6 for 4)::int then raise exception 'Fonte non valida'; end if;
  scelta_indice=array_position(op,p_scelta)-1;
  if coalesce(p_cambia,false) then perform votazioni62_private.cambia_post(p_team,fonte_id,scelta_indice); else perform public.curva_vota(p_team,p_code,fonte_id,scelta_indice); end if;
  select op[v.opt+1] into precedente from public.curva_vote v where post_id=fonte_id and team=p_team;
  return jsonb_build_object('mia_scelta',precedente,'stato','registrato');
 end if;
 if s.origine='post' then
  scelta_indice=(select ord::int-1 from jsonb_array_elements_text(s.scelte) with ordinality a(scelta,ord) where scelta=p_scelta);
  if coalesce(p_cambia,false) then perform votazioni62_private.cambia_post(p_team,s.fonte::bigint,scelta_indice); else perform public.curva_vota(p_team,p_code,s.fonte::bigint,scelta_indice); end if;
  select po.opts[v.opt+1] into precedente from public.curva_vote v join public.curva_poll po on po.post_id=v.post_id where v.post_id=s.fonte::bigint and v.team=p_team;
  return jsonb_build_object('mia_scelta',precedente,'stato','registrato');
 end if;
 select scelta into precedente from sondaggio_private.voti where giornata=s.giornata and team=p_team;
 if found and not coalesce(p_cambia,false) then return jsonb_build_object('registrato',false,'mia_scelta',precedente,'stato','gia_votato'); end if;
 if s.chiuso is not null or coalesce(clock_timestamp()>=s.chiude,false) or clock_timestamp()<s.aperto then raise exception 'Votazione non aperta'; end if;
 if p_scelta is null or not s.scelte ? p_scelta then raise exception 'Scelta non valida'; end if;
 if s.origine='sfida' then
  if precedente is not null then update sondaggio_private.voti set scelta=p_scelta where giornata=s.giornata and team=p_team;
  else insert into sondaggio_private.voti(giornata,team,scelta) values(s.giornata,p_team,p_scelta) on conflict do nothing; end if;
 end if;
 return jsonb_build_object('registrato',true,'mia_scelta',p_scelta,'stato','registrato');
end $$;

-- La vecchia RPC deve rispettare lo stesso primo voto: niente percorso alternativo.
-- Il caricamento del catalogo per la stagione corrente va completato e confrontato
-- con i voti precedenti PRIMA di attivare la 6.2. Nessuna importazione automatica.
create or replace function public.sondaggio_vota(p_team text,p_code text,p_giornata int,p_scelta text)
returns jsonb language plpgsql security definer set search_path='' as $$
declare sid text; risultato jsonb;
begin
 perform public.curva_chk(p_team,p_code);
 select id into sid from votazioni62_private.sondaggi where origine='sfida' and giornata=p_giornata order by aperto desc limit 1;
 if sid is null then raise exception 'Catalogo 6.2 non pronto: voto sospeso'; end if;
 risultato=public.v62_vota(sid,p_team,p_code,p_scelta);
 -- Compatibilità con i client precedenti: specchio, mai sovrascrittura.
 insert into sondaggio_private.voti(giornata,team,scelta) values(p_giornata,p_team,risultato->>'mia_scelta') on conflict do nothing;
 return public.sondaggio_stato(p_giornata)||risultato;
end $$;

drop function if exists public.mvp_vota(text,text,text,integer,text);
create or replace function public.mvp_vota(p_team text,p_code text,p_stagione text,p_giornata integer,p_scelta text default null,p_cambia boolean default false)
returns jsonb language plpgsql security definer set search_path='' as $$
declare w mvp_private.giornate; precedente text;
begin
 perform public.curva_chk(p_team,p_code);
 select * into w from mvp_private.giornate where stagione=p_stagione and giornata=p_giornata for update;
 if not found then raise exception 'Votazione non disponibile'; end if;
 select scelta into precedente from mvp_private.voti where stagione=p_stagione and giornata=p_giornata and team=p_team;
 if found and not coalesce(p_cambia,false) then return public.mvp_stato(p_stagione,p_giornata)||jsonb_build_object('scelta',precedente,'registrato',false); end if;
 if w.chiusa is not null or clock_timestamp()>=w.chiude then raise exception 'Votazione conclusa'; end if;
 if p_scelta is null or not exists(select 1 from jsonb_array_elements(w.candidati) c where c->>'team'=p_scelta) then raise exception 'Candidatura non valida'; end if;
 if precedente is not null then update mvp_private.voti set scelta=p_scelta where stagione=p_stagione and giornata=p_giornata and team=p_team;
 else insert into mvp_private.voti(stagione,giornata,team,scelta) values(p_stagione,p_giornata,p_team,p_scelta); end if;
 return public.mvp_stato(p_stagione,p_giornata)||jsonb_build_object('scelta',p_scelta,'registrato',true);
end $$;

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
  if w.chiude is distinct from p_chiude then raise exception 'Scadenza già annunciata: non si modifica'; end if;
  if w.firma=p_firma and w.candidati=p_candidati and w.redazione=p_redazione and w.personaggi=p_personaggi and w.chiude=p_chiude then return public.mvp_stato(p_stagione,p_giornata); end if;
  if w.chiusa is not null or clock_timestamp()>=w.chiude then raise exception 'Verdetto conservato: revisione esplicita necessaria'; end if;
  if exists(select 1 from mvp_private.voti where stagione=p_stagione and giornata=p_giornata) then raise exception 'Votazione iniziata: revisione esplicita necessaria'; end if;
 end if;
 if not found and p_chiude>clock_timestamp()+interval '48 hours' then raise exception 'MVP: al massimo 48 ore dalla prima apertura'; end if;
 if p_chiude is null or p_chiude<=clock_timestamp() then raise exception 'Non si apre retroattivamente una votazione scaduta'; end if;
 insert into mvp_private.giornate(stagione,giornata,chiude,candidati,redazione,personaggi,firma)
 values(p_stagione,p_giornata,p_chiude,p_candidati,p_redazione,p_personaggi,p_firma)
 on conflict(stagione,giornata) do update set chiude=excluded.chiude,candidati=excluded.candidati,redazione=excluded.redazione,personaggi=excluded.personaggi,firma=excluded.firma;
 return public.mvp_stato(p_stagione,p_giornata);
end $f$;


-- Una registrazione ripetuta non cambia mai prima apertura e scadenza.
create or replace function public.v62_prepara(p_id text,p_stagione text,p_origine text,p_fonte text,p_giornata int,p_titolo text,p_scelte jsonb,p_aperto timestamptz,p_chiude timestamptz)
returns void language plpgsql security definer set search_path='' as $$
declare op text[]; prima timestamptz;
begin
 if p_id is distinct from p_origine||':'||p_stagione||':'||p_fonte then raise exception 'Identificativo della fonte non valido'; end if;
 if p_origine='sfida' and p_fonte is distinct from p_giornata::text then raise exception 'Giornata della fonte non valida'; end if;
 if p_origine='post' then
  select po.opts,p.created into op,prima from public.curva_poll po join public.curva_post p on p.id=po.post_id where po.post_id=p_fonte::bigint;
  if not found or to_jsonb(op) is distinct from p_scelte or prima is distinct from p_aperto then raise exception 'Il post deve conservare opzioni e prima apertura originali'; end if;
 end if;
 if p_origine='post' and p_chiude is distinct from p_aperto+interval '24 hours' then raise exception 'Il sondaggio nel post dura 24 ore dalla prima apertura'; end if;
 if p_id is null or (p_aperto is null and p_chiude>clock_timestamp()) or p_chiude is null or p_chiude<=p_aperto or p_aperto>clock_timestamp() then raise exception 'Apertura non valida'; end if;
 if exists(select 1 from jsonb_array_elements(p_scelte) s where jsonb_typeof(s)<>'string' or length(s#>>'{}') not between 1 and 120) or (select count(distinct s) from jsonb_array_elements(p_scelte) s)<>jsonb_array_length(p_scelte) then raise exception 'Scelte non valide'; end if;
 insert into votazioni62_private.sondaggi values(p_id,p_stagione,p_origine,p_fonte,p_giornata,p_titolo,p_scelte,p_aperto,p_chiude,null) on conflict do nothing;
 if not exists(select 1 from votazioni62_private.sondaggi where id=p_id and stagione=p_stagione and origine=p_origine and fonte=p_fonte and giornata=p_giornata and titolo=p_titolo and scelte=p_scelte and aperto is not distinct from p_aperto and chiude=p_chiude) then raise exception 'Votazione esistente: dati e scadenza conservati'; end if;
end $$;

-- I sondaggi dei post restano la stessa entità e gli stessi voti di curva_poll/curva_vote.
create or replace function public.curva_vota(p_team text,p_code text,p_post bigint,p_opt integer)
returns void language plpgsql security definer set search_path='' as $$
declare op text[]; t timestamptz;
begin
 perform public.curva_chk(p_team,p_code);
 select po.opts,p.created into op,t from public.curva_poll po join public.curva_post p on p.id=po.post_id where po.post_id=p_post for update of po;
 if not found then raise exception 'Sondaggio non trovato'; end if;
 if exists(select 1 from public.curva_vote where post_id=p_post and team=p_team) then return; end if;
 if clock_timestamp()>=votazioni62_private.post_scadenza(t) then raise exception 'Il sondaggio è chiuso'; end if;
 if p_opt is null or p_opt<0 or p_opt>=array_length(op,1) then raise exception 'Risposta non valida'; end if;
 insert into public.curva_vote(post_id,team,opt) values(p_post,p_team,p_opt) on conflict(post_id,team) do nothing;
end $$;
revoke all on function public.curva_vota(text,text,bigint,integer) from public;
grant execute on function public.curva_vota(text,text,bigint,integer) to anon,authenticated,service_role;


-- Lettura riservata al servizio per non ricominciare aperture già registrate.
create or replace function public.v62_catalogo_server(p_stagione text)
returns jsonb language sql stable security definer set search_path='' as $$
 select coalesce(jsonb_agg(to_jsonb(s) order by giornata),'[]'::jsonb) from votazioni62_private.sondaggi s where stagione=p_stagione
$$;
revoke all on function public.v62_catalogo_server(text) from public,anon,authenticated;
grant execute on function public.v62_catalogo_server(text) to service_role;

revoke all on all functions in schema votazioni62_private from public,anon,authenticated;
revoke all on function public.v62_sondaggi(text,text,text),public.v62_vota(text,text,text,text,boolean),public.v62_prepara(text,text,text,text,int,text,jsonb,timestamptz,timestamptz) from public,anon,authenticated;
grant execute on function public.v62_sondaggi(text,text,text),public.v62_vota(text,text,text,text,boolean) to anon,authenticated,service_role;
grant execute on function public.v62_prepara(text,text,text,text,int,text,jsonb,timestamptz,timestamptz) to service_role;
revoke all on function public.mvp_vota(text,text,text,integer,text,boolean) from public;
grant execute on function public.mvp_vota(text,text,text,integer,text,boolean) to anon,authenticated,service_role;
commit;
