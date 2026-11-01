-- Sondaggio della Curva 5.5 (1° novembre 2026, «vai» di Gianluca).
-- Solo oggetti nuovi: schema privato sondaggio_private (voti e commenti) e tre funzioni pubbliche.
-- Vota e commenta solo chi entra con la propria squadra (stesso controllo della Curva: curva_chk); i risultati li vedono tutti.
-- Per tornare indietro:
--   drop function public.sondaggio_stato(int); drop function public.sondaggio_vota(text,text,int,text);
--   drop function public.sondaggio_commenta(text,text,int,text); drop schema sondaggio_private cascade;

create schema if not exists sondaggio_private;
revoke all on schema sondaggio_private from public, anon, authenticated;

create table if not exists sondaggio_private.voti(
  giornata int not null check (giornata between 1 and 60),
  team text not null,
  scelta text not null check (char_length(scelta) between 1 and 120),
  aggiornato timestamptz not null default now(),
  primary key (giornata, team)
);
create table if not exists sondaggio_private.commenti(
  id bigserial primary key,
  giornata int not null check (giornata between 1 and 60),
  team text not null,
  testo text not null check (char_length(testo) between 1 and 280),
  creato timestamptz not null default now()
);
create index if not exists commenti_giornata on sondaggio_private.commenti(giornata, creato desc);
alter table sondaggio_private.voti enable row level security;
alter table sondaggio_private.commenti enable row level security;
revoke all on sondaggio_private.voti, sondaggio_private.commenti from public, anon, authenticated;

-- Lettura pubblica: voti per partita e ultimi 50 commenti della giornata
create or replace function public.sondaggio_stato(p_giornata int)
returns jsonb language sql stable security definer set search_path = public, pg_temp as $f$
  select jsonb_build_object(
    'voti', coalesce((select jsonb_agg(jsonb_build_object('scelta', scelta, 'n', n)) from
               (select scelta, count(*) n from sondaggio_private.voti where giornata = p_giornata group by scelta) v), '[]'::jsonb),
    'commenti', coalesce((select jsonb_agg(jsonb_build_object('team', team, 'testo', testo, 'creato', creato) order by creato) from
               (select team, testo, creato from sondaggio_private.commenti where giornata = p_giornata order by creato desc limit 50) c), '[]'::jsonb))
$f$;

-- Un voto per squadra e giornata; votando di nuovo si cambia la scelta
create or replace function public.sondaggio_vota(p_team text, p_code text, p_giornata int, p_scelta text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $f$
begin
  perform curva_chk(p_team, p_code);
  if p_scelta is null or char_length(trim(p_scelta)) = 0 or char_length(p_scelta) > 120 then raise exception 'Scelta non valida'; end if;
  insert into sondaggio_private.voti(giornata, team, scelta) values (p_giornata, p_team, trim(p_scelta))
  on conflict (giornata, team) do update set scelta = excluded.scelta, aggiornato = now();
  return public.sondaggio_stato(p_giornata);
end $f$;

-- Commenti: al massimo 10 per squadra e giornata
create or replace function public.sondaggio_commenta(p_team text, p_code text, p_giornata int, p_testo text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $f$
begin
  perform curva_chk(p_team, p_code);
  if p_testo is null or char_length(trim(p_testo)) = 0 or char_length(p_testo) > 280 then raise exception 'Commento non valido'; end if;
  if (select count(*) from sondaggio_private.commenti where giornata = p_giornata and team = p_team) >= 10 then raise exception 'Troppi commenti'; end if;
  insert into sondaggio_private.commenti(giornata, team, testo) values (p_giornata, p_team, trim(p_testo));
  return public.sondaggio_stato(p_giornata);
end $f$;

revoke all on function public.sondaggio_stato(int), public.sondaggio_vota(text,text,int,text), public.sondaggio_commenta(text,text,int,text) from public;
grant execute on function public.sondaggio_stato(int), public.sondaggio_vota(text,text,int,text), public.sondaggio_commenta(text,text,int,text) to anon, authenticated;
