-- O Girrr · Notifiche sul telefono: TUTTO IN UNO da incollare nell'editor SQL di Supabase (progetto qmjqfgmvimsuxvghetgi) e premere Run.
-- Crea solo cose nuove (schema push_private, funzioni push_*, giro ogni 5 minuti). Si può rilanciare senza danni.

-- Notifiche push di O Girrr (Claude, 9 novembre 2026, richiesta di Gianluca).
-- Solo oggetti nuovi: schema push_private, funzioni push_*. Nessuna tabella o funzione esistente cambia.
-- Invio: Edge Function «push-invia», chiamata ogni 5 minuti da pg_cron (pg_net).

create extension if not exists pg_cron with schema pg_catalog;
create extension if not exists pg_net with schema extensions;

create schema if not exists push_private;
revoke all on schema push_private from public, anon, authenticated;

create table if not exists push_private.iscrizioni(
  id bigserial primary key,
  team text not null,
  endpoint text not null unique,
  p256dh text not null,
  auth text not null,
  piattaforma text,
  pref jsonb not null default '{}'::jsonb,
  creata timestamptz not null default now(),
  aggiornata timestamptz not null default now()
);
create index if not exists iscrizioni_team on push_private.iscrizioni(team);

create table if not exists push_private.inviate(
  chiave text not null,
  iscrizione bigint not null references push_private.iscrizioni(id) on delete cascade,
  inviata timestamptz not null default now(),
  primary key (chiave, iscrizione)
);
create index if not exists inviate_quando on push_private.inviate(inviata);

-- Una riga sola: chiavi di firma (VAPID, create dalla funzione al primo giro) e gettone del giro programmato
create table if not exists push_private.cfg(
  id int primary key default 1 check (id = 1),
  vapid_pub text,
  vapid_priv text,
  cron_token text not null default encode(extensions.gen_random_bytes(24), 'hex')
);
insert into push_private.cfg(id) values (1) on conflict do nothing;

alter table push_private.iscrizioni enable row level security;
alter table push_private.inviate enable row level security;
alter table push_private.cfg enable row level security;
revoke all on all tables in schema push_private from public, anon, authenticated;

-- Preferenze: solo le voci conosciute, vero/falso
create or replace function push_private.pulisci_pref(p jsonb) returns jsonb
language sql immutable set search_path = '' as $$
  select coalesce(jsonb_object_agg(k, (p->>k)::boolean), '{}'::jsonb)
    from unnest(array['formazione','risultati','giornale','curva','applausi','derby','totogirrr']) k
   where p ? k and jsonb_typeof(p->k) = 'boolean'
$$;

-- Eventi personali di una squadra (gli stessi della pagina Notifiche, notifiche_stato), con la categoria della notifica
create or replace function push_private.eventi(p_team text, p_da timestamptz)
returns table(chiave text, cat text, titolo text, testo text, url text, quando timestamptz)
language sql stable security definer set search_path = public, pg_temp as $$
  select * from (
    select 'risp-'||r.id, 'curva', r.team||' ti ha risposto', left(r.body,140), 'apri.html?p=curva', r.created
      from curva_reply r join curva_post p on r.k = 'p'||p.id
     where p.team = p_team and r.team <> p_team
    union all
    select 'app-'||x.k||'-'||count(*), 'applausi',
           case when count(*)=1 then min(x.team)||' ha applaudito il tuo coro' else count(*)||' applausi al tuo coro' end,
           left(max(x.body),140), 'apri.html?p=curva', max(x.created)
      from (select a.k, a.team, a.created, coalesce(p.body, rr.body) body
              from curva_react a
              left join curva_post p on a.k = 'p'||p.id and p.team = p_team
              left join curva_reply rr on a.k = 'r'||rr.id and rr.team = p_team
             where a.kind = 'a' and a.team <> p_team and (p.id is not null or rr.id is not null)) x
     group by x.k
    union all
    select 'sfida-'||s.id, 'derby', s.da||' ti ha sfidato',
           coalesce(nullif(s.frase_testo,''), 'Nuova sfida Derby')||case when s.stato='attesa' then ' · Tocca a te rispondere' else '' end,
           'apri.html?p=app&h=sport', s.creata
      from derby_sfida s where s.a = p_team
    union all
    select 'sfida-r-'||s.id, 'derby',
           s.a||case s.stato when 'accettata' then ' ha accettato la tua sfida' when 'rifiutata' then ' ha rifiutato la tua sfida' else ' ha risposto alla tua sfida' end,
           coalesce(nullif(s.nome,''), 'Derby'), 'apri.html?p=app&h=sport', s.risposta
      from derby_sfida s where s.da = p_team and s.risposta is not null
    union all
    select 'prest-'||t.id||'-'||t.stato, 'totogirrr', 'Totogirrr · Richiesta di prestito',
           case when t.creditore = p_team then t.debitore else t.creditore end||' · '||trim_scale(t.importo)::text||' · Tocca a te rispondere',
           'apri.html?p=totogirrr', t.aggiornato
      from toto_prestiti t where t.attesa_di = p_team and t.stato = 'richiesta'
    union all
    select 'mov-'||m.id, 'totogirrr', 'Totogirrr: '||case when m.importo >= 0 then '+' else '' end||trim_scale(m.importo)::text,
           coalesce(nullif(m.nota,''), replace(m.tipo,'_',' ')), 'apri.html?p=totogirrr', m.creato
      from toto_movimenti m where m.team = p_team
  ) e(chiave, cat, titolo, testo, url, quando)
  where quando > p_da
$$;
revoke all on function push_private.eventi(text, timestamptz) from public, anon, authenticated;

-- ===== Funzioni per la pagina (con il codice della squadra, come la Curva) =====

create or replace function public.push_chiave() returns text
language sql stable security definer set search_path = '' as $$ select vapid_pub from push_private.cfg where id = 1 $$;

create or replace function public.push_iscrivi(p_team text, p_code text, p_sub jsonb, p_pref jsonb, p_piattaforma text default null)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare e text := p_sub->>'endpoint'; k1 text := p_sub#>>'{keys,p256dh}'; k2 text := p_sub#>>'{keys,auth}'; r push_private.iscrizioni;
begin
  perform curva_chk(p_team, p_code);
  if e is null or e !~ '^https://' or char_length(e) > 1000 then raise exception 'Iscrizione non valida'; end if;
  if k1 is null or k2 is null or char_length(k1) > 200 or char_length(k2) > 100 then raise exception 'Iscrizione non valida'; end if;
  insert into push_private.iscrizioni(team, endpoint, p256dh, auth, piattaforma, pref)
       values (p_team, e, k1, k2, left(p_piattaforma, 20), push_private.pulisci_pref(coalesce(p_pref, '{}')))
  on conflict (endpoint) do update set team = excluded.team, p256dh = excluded.p256dh, auth = excluded.auth,
       piattaforma = excluded.piattaforma, pref = excluded.pref, aggiornata = now()
  returning * into r;
  -- al massimo 8 telefoni per squadra: si tolgono i più vecchi
  delete from push_private.iscrizioni where team = p_team and id in
    (select id from push_private.iscrizioni where team = p_team order by aggiornata desc offset 8);
  return jsonb_build_object('iscritto', true, 'pref', r.pref);
end $$;

create or replace function public.push_stato(p_team text, p_code text, p_endpoint text)
returns jsonb language plpgsql stable security definer set search_path = public, pg_temp as $$
declare r push_private.iscrizioni;
begin
  perform curva_chk(p_team, p_code);
  select * into r from push_private.iscrizioni where endpoint = p_endpoint and team = p_team;
  return jsonb_build_object('iscritto', r.id is not null, 'pref', coalesce(r.pref, '{}'::jsonb));
end $$;

create or replace function public.push_preferenze(p_team text, p_code text, p_endpoint text, p_pref jsonb)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare r push_private.iscrizioni;
begin
  perform curva_chk(p_team, p_code);
  update push_private.iscrizioni set pref = push_private.pulisci_pref(coalesce(p_pref, '{}')), aggiornata = now()
   where endpoint = p_endpoint and team = p_team returning * into r;
  return jsonb_build_object('iscritto', r.id is not null, 'pref', coalesce(r.pref, '{}'::jsonb));
end $$;

create or replace function public.push_cancella(p_team text, p_code text, p_endpoint text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
begin
  perform curva_chk(p_team, p_code);
  delete from push_private.iscrizioni where endpoint = p_endpoint and team = p_team;
  return jsonb_build_object('iscritto', false);
end $$;

revoke all on function public.push_chiave(), public.push_iscrivi(text,text,jsonb,jsonb,text), public.push_stato(text,text,text),
  public.push_preferenze(text,text,text,jsonb), public.push_cancella(text,text,text) from public;
grant execute on function public.push_chiave(), public.push_iscrivi(text,text,jsonb,jsonb,text), public.push_stato(text,text,text),
  public.push_preferenze(text,text,text,jsonb), public.push_cancella(text,text,text) to anon, authenticated, service_role;

-- ===== Funzioni solo per la funzione di invio (service_role) =====

create or replace function public.push_srv_cfg() returns jsonb
language sql stable security definer set search_path = '' as $$
  select jsonb_build_object('pub', vapid_pub, 'priv', vapid_priv, 'token', cron_token) from push_private.cfg where id = 1
$$;

create or replace function public.push_srv_chiavi(p_pub text, p_priv text) returns void
language sql security definer set search_path = '' as $$
  update push_private.cfg set vapid_pub = p_pub, vapid_priv = p_priv where id = 1 and vapid_pub is null
$$;

-- Tutte le iscrizioni, con le chiavi già inviate negli ultimi 4 giorni e gli eventi personali nuovi
create or replace function public.push_srv_giro() returns jsonb
language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce(jsonb_agg(jsonb_build_object(
    'id', i.id, 'team', i.team, 'endpoint', i.endpoint, 'p256dh', i.p256dh, 'auth', i.auth, 'pref', i.pref, 'creata', i.creata,
    'inviate', coalesce((select jsonb_agg(v.chiave) from push_private.inviate v where v.iscrizione = i.id and v.inviata > now() - interval '4 days'), '[]'::jsonb),
    'eventi', coalesce((select jsonb_agg(to_jsonb(ev) order by ev.quando)
                          from push_private.eventi(i.team, greatest(i.creata, now() - interval '12 hours')) ev
                         where not exists (select 1 from push_private.inviate v where v.iscrizione = i.id and v.chiave = ev.chiave)), '[]'::jsonb)
  )), '[]'::jsonb)
  from push_private.iscrizioni i
$$;

create or replace function public.push_srv_segna(p_inviate jsonb, p_scadute bigint[]) returns void
language plpgsql security definer set search_path = public, pg_temp as $$
begin
  insert into push_private.inviate(chiave, iscrizione)
    select x->>'chiave', (x->>'id')::bigint from jsonb_array_elements(coalesce(p_inviate, '[]'::jsonb)) x
     where exists (select 1 from push_private.iscrizioni i where i.id = (x->>'id')::bigint)
  on conflict do nothing;
  delete from push_private.iscrizioni where id = any(coalesce(p_scadute, '{}'));
  delete from push_private.inviate where inviata < now() - interval '60 days';
end $$;

-- Notifica di prova chiesta dalla pagina: iscrizione della squadra, al massimo una al minuto
create or replace function public.push_srv_prova(p_team text, p_code text, p_endpoint text) returns jsonb
language plpgsql security definer set search_path = public, pg_temp as $$
declare r push_private.iscrizioni; k text := 'prova-'||to_char(now(), 'YYYYMMDDHH24MI');
begin
  if not curva_ok(p_team, p_code) then return null; end if;
  select * into r from push_private.iscrizioni where endpoint = p_endpoint and team = p_team;
  if r.id is null then return null; end if;
  insert into push_private.inviate(chiave, iscrizione) values (k, r.id) on conflict do nothing;
  if not found then return jsonb_build_object('troppe', true); end if;
  return jsonb_build_object('id', r.id, 'endpoint', r.endpoint, 'p256dh', r.p256dh, 'auth', r.auth);
end $$;

revoke all on function public.push_srv_cfg(), public.push_srv_chiavi(text,text), public.push_srv_giro(),
  public.push_srv_segna(jsonb,bigint[]), public.push_srv_prova(text,text,text) from public, anon, authenticated;
grant execute on function public.push_srv_cfg(), public.push_srv_chiavi(text,text), public.push_srv_giro(),
  public.push_srv_segna(jsonb,bigint[]), public.push_srv_prova(text,text,text) to service_role;


-- Notifiche push: giro ogni 5 minuti (dopo il deploy della funzione push-invia)
-- Giro ogni 5 minuti
select cron.unschedule('push-giro') where exists (select 1 from cron.job where jobname = 'push-giro');
select cron.schedule('push-giro', '*/5 * * * *', $c$
  select net.http_post(
    url := 'https://qmjqfgmvimsuxvghetgi.supabase.co/functions/v1/push-invia',
    headers := jsonb_build_object('Content-Type', 'application/json', 'x-girrr-cron', (select cron_token from push_private.cfg where id = 1)),
    body := '{"giro":true}'::jsonb,
    timeout_milliseconds := 30000)
$c$);
