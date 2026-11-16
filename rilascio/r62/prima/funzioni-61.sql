-- Definizioni in uso PRIMA della 6.2 (lette da Supabase il 16 novembre 2026, sola lettura, da Claude).
-- Servono SOLO per tornare indietro: riapplicarle ripristina il comportamento 6.1 delle quattro funzioni.
-- Conteggi al momento della lettura: sondaggio_private.voti 6ª 1, 7ª 2, 8ª 2; mvp_private.voti 2026/27:7 2;
-- curva_vote 0; conf_risposta 8; conf_dopo 1. MVP 7ª: chiude 2026-11-21 15:00 Europe/Rome, non chiusa.
-- Privilegi originali: curva_vota, sondaggio_vota e mvp_vota eseguibili da anon, authenticated, service_role;
-- mvp_prepara solo da service_role.
-- Per tornare indietro con la 6.2 già applicata: prima
--   drop function if exists public.mvp_vota(text,text,text,integer,text,boolean);
--   drop trigger if exists conf_finestre62 on public.conf_risposta; drop trigger if exists dopo_finestre62 on public.conf_dopo;
-- poi le definizioni qui sotto e i grant in fondo. Nessun voto, catalogo o verdetto va cancellato.

CREATE OR REPLACE FUNCTION public.curva_vota(p_team text, p_code text, p_post bigint, p_opt integer)
 RETURNS void
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
declare po curva_poll; t timestamptz;
begin perform curva_chk(p_team,p_code);
 select * into po from curva_poll where post_id=p_post;
 if po.post_id is null then raise exception 'Sondaggio non trovato'; end if;
 select created into t from curva_post where id=p_post;
 if t<now()-interval '24 hours' then raise exception 'Il sondaggio è chiuso'; end if;
 if p_opt<0 or p_opt>=array_length(po.opts,1) then raise exception 'Risposta non valida'; end if;
 insert into curva_vote(post_id,team,opt) values(p_post,p_team,p_opt) on conflict (post_id,team) do nothing;
end $function$;

CREATE OR REPLACE FUNCTION public.mvp_prepara(p_stagione text, p_giornata integer, p_chiude timestamp with time zone, p_candidati jsonb, p_redazione jsonb, p_personaggi jsonb, p_firma text)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
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
end $function$;

CREATE OR REPLACE FUNCTION public.mvp_vota(p_team text, p_code text, p_stagione text, p_giornata integer, p_scelta text DEFAULT NULL::text)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
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
end $function$;

CREATE OR REPLACE FUNCTION public.sondaggio_vota(p_team text, p_code text, p_giornata integer, p_scelta text)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'pg_temp'
AS $function$
begin
  perform curva_chk(p_team, p_code);
  if p_scelta is null or char_length(trim(p_scelta)) = 0 or char_length(p_scelta) > 120 then raise exception 'Scelta non valida'; end if;
  insert into sondaggio_private.voti(giornata, team, scelta) values (p_giornata, p_team, trim(p_scelta))
  on conflict (giornata, team) do update set scelta = excluded.scelta, aggiornato = now();
  return public.sondaggio_stato(p_giornata);
end $function$;

revoke all on function public.curva_vota(text,text,bigint,integer),public.sondaggio_vota(text,text,integer,text),public.mvp_vota(text,text,text,integer,text),public.mvp_prepara(text,integer,timestamptz,jsonb,jsonb,jsonb,text) from public;
grant execute on function public.curva_vota(text,text,bigint,integer),public.sondaggio_vota(text,text,integer,text),public.mvp_vota(text,text,text,integer,text) to anon,authenticated,service_role;
grant execute on function public.mvp_prepara(text,integer,timestamptz,jsonb,jsonb,jsonb,text) to service_role;
