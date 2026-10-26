-- PROPOSTA 5.2 — NON APPLICARE IN PRODUZIONE prima della verifica di identity e scheduler.
-- Registrazione atomica/idempotente per premi Carriera verificati lato server.
-- Non pubblicare un endpoint che possa chiamare questa funzione dal client.
create schema if not exists private;
revoke all on schema private from public, anon, authenticated;

create table if not exists private.carriera_premi (
  stagione text not null,
  allenatore_id text not null,
  squadra text not null,
  obiettivo_key text not null,
  tipo text not null check (tipo in ('presidente','sponsor')),
  reputazione integer not null check (reputazione between 1 and 3),
  fantacrediti numeric(10,2) not null default 0 check (fantacrediti between 0 and 125),
  prova jsonb not null,
  verificato_il timestamptz not null default now(),
  primary key (stagione,allenatore_id,obiettivo_key),
  check (tipo='sponsor' or fantacrediti=0),
  check (length(trim(allenatore_id))>0),
  check (length(trim(obiettivo_key))>0)
);
revoke all on private.carriera_premi from public, anon, authenticated;

-- Chiave allenatore_id immutabile, indipendente dalla squadra.
-- Il caller deve verificare l'esito ufficiale alla giornata/termine dell'obiettivo
-- PRIMA di chiamare la funzione; non fidarsi dei valori del browser.
create or replace function private.registra_premio_carriera(
  p_stagione text, p_allenatore_id text, p_squadra text,
  p_obiettivo_key text, p_tipo text, p_reputazione integer,
  p_fantacrediti numeric, p_prova jsonb
) returns boolean
language plpgsql security definer set search_path = ''
as $$
declare v_added boolean;
begin
  insert into private.carriera_premi(
    stagione,allenatore_id,squadra,obiettivo_key,tipo,reputazione,fantacrediti,prova)
  values (p_stagione,p_allenatore_id,p_squadra,p_obiettivo_key,
          p_tipo,p_reputazione,p_fantacrediti,p_prova)
  on conflict (stagione,allenatore_id,obiettivo_key) do nothing;
  v_added=found;
  if not v_added then return false; end if;
  if p_fantacrediti > 0 then
    update public.toto_conti set crediti=crediti+p_fantacrediti
      where team=p_squadra;
    if not found then
      raise exception 'Conto Totogirrr inesistente per squadra %', p_squadra;
    end if;
    insert into public.toto_movimenti(team,tipo,importo,nota)
      values (p_squadra,'premio_sponsor',p_fantacrediti,
        'Carriera '||p_stagione||' · '||p_obiettivo_key);
  end if;
  return true;
end;
$$;
revoke all on function private.registra_premio_carriera(text,text,text,text,text,integer,numeric,jsonb)
  from public,anon,authenticated;
-- Invocare esclusivamente come ruolo amministratore/server dopo validazione.
-- Non assegnare GRANT EXECUTE a ruoli browser.
-- Test in transazione con ROLLBACK e verifica eventi doppio inserimento prima del release.
