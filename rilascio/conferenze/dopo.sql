-- Conferenza del dopo partita (Claude, 10 novembre 2026, richiesta di Gianluca: «la conferenza dopo partita la metterei sotto
-- conferenza stampa»). DA APPLICARE SOLO CON IL «VAI» DI GIANLUCA SUL DATABASE (progetto qmjqfgmvimsuxvghetgi).
-- Solo oggetti nuovi: tabella conf_dopo e funzioni conf_dopo_salva e conf_dopo_pubbliche. Niente di esistente cambia.
-- Una risposta per squadra e giornata, che poi non si cambia più (come la conferenza della vigilia, bloccata nella pagina).
-- Il controllo del codice squadra è curva_chk, lo stesso della Curva e delle notifiche.
-- Per tornare indietro: drop function conf_dopo_salva(text,text,int,jsonb); drop function conf_dopo_pubbliche(); drop table conf_dopo;

create table if not exists public.conf_dopo(
  team text not null,
  giornata int not null check (giornata between 1 and 60),
  risposta jsonb not null,
  creata timestamptz not null default now(),
  primary key (team, giornata)
);
alter table public.conf_dopo enable row level security;
revoke all on public.conf_dopo from public, anon, authenticated;

create or replace function public.conf_dopo_salva(p_team text, p_code text, p_giornata int, p_risposta jsonb)
returns void language plpgsql security definer set search_path = public, pg_temp as $$
declare t text := btrim(coalesce(p_risposta->>'t', '')); a text := p_risposta->>'a'; k int;
begin
  perform curva_chk(p_team, p_code);
  if p_giornata is null or p_giornata < 1 or p_giornata > 60 then raise exception 'Giornata non valida'; end if;
  if char_length(t) < 1 or char_length(t) > 80 then raise exception 'La risposta deve avere da 1 a 80 caratteri'; end if;
  if a is null or a not in ('0', '1', '2', 'free') then raise exception 'Risposta non valida'; end if;
  k := case when (p_risposta->>'k') ~ '^[0-2]$' then (p_risposta->>'k')::int else 1 end;
  insert into conf_dopo(team, giornata, risposta) values (p_team, p_giornata, jsonb_build_object('a', a, 't', t, 'k', k))
    on conflict (team, giornata) do nothing;
  if not found then raise exception 'La conferenza del dopo partita è già pubblicata'; end if;
end $$;

create or replace function public.conf_dopo_pubbliche()
returns jsonb language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce(jsonb_agg(jsonb_build_object('team', team, 'giornata', giornata, 'risposta', risposta, 'creata', creata)
                            order by giornata, team), '[]'::jsonb)
    from conf_dopo
$$;

revoke all on function public.conf_dopo_salva(text, text, int, jsonb), public.conf_dopo_pubbliche() from public;
grant execute on function public.conf_dopo_salva(text, text, int, jsonb), public.conf_dopo_pubbliche() to anon, authenticated, service_role;
