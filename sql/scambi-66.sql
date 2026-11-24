-- Versione 6.6 · Scambi nell'app (Claude, 24 novembre 2026, decisioni di Gianluca).
-- PROPOSTA: non applicata. Si incolla nell'SQL Editor di Supabase solo con il «Vai» di Gianluca.
--
-- Come funziona
-- - Dallo Spogliatoio («Mercato Scambi» › «Valuta uno scambio» › «Effettua lo scambio») un allenatore entrato con il suo codice
--   registra uno scambio già fatto o concordato: solo giocatori delle due rose, stesso numero e stessi ruoli (lo controlla la pagina;
--   il workflow lo ricontrolla sulle rose vere prima di applicarlo), niente crediti.
-- - Lo scambio resta «in attesa» finché arriva UNA conferma, vale la prima:
--     · manuale: l'altra squadra, Gianluca (Oranje VC) o qualsiasi altro allenatore della lega come testimone,
--       ma mai chi l'ha proposto; l'ospite non ha codice e quindi non può confermare;
--     · automatica: l'importazione da Leghe trova le rose già scambiate (workflow, codice di Oranje VC).
-- - L'altra squadra può rifiutarlo, chi l'ha proposto può annullarlo. Dopo 14 giorni senza conferma decade.
-- - Alla conferma il workflow del sito applica lo scambio alle rose (data.json), rifà la classifica delle rose, prepara il post
--   della Lega con il commento di Ciro in Curva e la notizia per Radio e Giornale, poi segna lo scambio come applicato.
-- - Notifiche: nella pagina Notifiche e sul telefono (nuova voce «Scambi», accesa di base).
--
-- Stesso schema del resto: nessun accesso diretto alla tabella, tutto passa da funzioni che controllano il codice squadra (curva_chk).
-- Per tornare indietro (prima di ripristinare le due funzioni delle notifiche, vedi in fondo):
--   drop function public.scambio_proponi(text,text,text,text[],text[],jsonb); drop function public.scambio_rispondi(text,text,bigint,text);
--   drop function public.scambio_stato(text,text); drop function public.scambio_srv_leghe(text,text,bigint);
--   drop function public.scambio_srv_applicato(text,text,bigint,text,text); drop function scambi_private.scadi(); drop table public.scambi;
--   drop schema scambi_private;

create schema if not exists scambi_private;
revoke all on schema scambi_private from public, anon, authenticated;

create table if not exists public.scambi(
  id bigserial primary key,
  da text not null,                       -- chi registra lo scambio
  a text not null,                        -- l'altra squadra
  dai text[] not null,                    -- id dei giocatori che «da» cede
  ricevi text[] not null,                 -- id dei giocatori che «da» riceve da «a»
  nomi jsonb not null default '{}',       -- id -> {"n": nome, "t": squadra di Serie A, "r": ruolo}, solo per mostrarlo
  stato text not null default 'attesa' check (stato in ('attesa','confermato','rifiutato','annullato','scaduto','non_valido')),
  creato timestamptz not null default now(),
  chiuso timestamptz,
  conferma text check (conferma in ('squadra','lega','testimone','leghe')),
  confermato_da text,
  applicato timestamptz,
  esito text,                             -- nota del workflow («Applicato alle rose», «Rose diverse da Leghe», …)
  check (da <> a),
  check (cardinality(dai) between 1 and 5 and cardinality(dai) = cardinality(ricevi))
);
alter table public.scambi enable row level security;
revoke all on public.scambi from public, anon, authenticated;
create index if not exists scambi_stato on public.scambi(stato, creato desc);

-- Gli scambi in attesa da più di 14 giorni decadono
create or replace function scambi_private.scadi() returns void language sql security definer set search_path to 'public' as $$
  update scambi set stato = 'scaduto', chiuso = now() where stato = 'attesa' and creato < now() - interval '14 days';
$$;
revoke all on function scambi_private.scadi() from public, anon, authenticated;

create or replace function public.scambio_proponi(p_team text, p_code text, p_a text, p_dai text[], p_ricevi text[], p_nomi jsonb default '{}')
returns jsonb language plpgsql security definer set search_path to 'public' as $$
declare nid bigint; tutti text[];
begin
  perform curva_chk(p_team, p_code);
  perform scambi_private.scadi();
  if p_a is null or p_a = p_team or not exists (select 1 from curva_lock where team = p_a) then raise exception 'Squadra non valida'; end if;
  if coalesce(cardinality(p_dai),0) = 0 or coalesce(cardinality(p_dai),0) <> coalesce(cardinality(p_ricevi),0) then
    raise exception 'Servono gli stessi giocatori da tutte e due le parti'; end if;
  if cardinality(p_dai) > 5 then raise exception 'Al massimo 5 giocatori per parte'; end if;
  tutti := p_dai || p_ricevi;
  if exists (select 1 from unnest(tutti) x where x !~ '^[0-9]{1,8}$') then raise exception 'Giocatore non valido'; end if;
  if (select count(distinct x) from unnest(tutti) x) <> cardinality(tutti) then raise exception 'Lo stesso giocatore compare due volte'; end if;
  if jsonb_typeof(coalesce(p_nomi,'{}')) <> 'object' or length(coalesce(p_nomi,'{}')::text) > 4000 then raise exception 'Nomi non validi'; end if;
  -- uno stesso giocatore non può stare in due scambi in attesa
  if exists (select 1 from scambi s where s.stato = 'attesa' and (s.dai || s.ricevi) && tutti) then
    raise exception 'Uno di questi giocatori è già in uno scambio in attesa di conferma'; end if;
  if (select count(*) from scambi where da = p_team and creato > now() - interval '1 day') >= 5 then
    raise exception 'Troppi scambi registrati oggi'; end if;
  insert into scambi(da, a, dai, ricevi, nomi)
  values (p_team, p_a, p_dai, p_ricevi,
          coalesce((select jsonb_object_agg(k, jsonb_build_object('n', left(v->>'n',40), 't', left(v->>'t',20), 'r', left(v->>'r',1)))
                      from jsonb_each(coalesce(p_nomi,'{}')) e(k,v) where k = any(tutti) and jsonb_typeof(v) = 'object'), '{}'))
  returning id into nid;
  return jsonb_build_object('id', nid, 'stato', 'attesa');
end $$;

-- p_azione: 'conferma' (l'altra squadra, Oranje VC o un testimone, mai chi l'ha registrato), 'rifiuta' (solo l'altra squadra),
-- 'annulla' (solo chi l'ha registrato). Vale la prima conferma: le altre trovano lo scambio già chiuso.
create or replace function public.scambio_rispondi(p_team text, p_code text, p_id bigint, p_azione text)
returns jsonb language plpgsql security definer set search_path to 'public' as $$
declare r scambi%rowtype; tipo text;
begin
  perform curva_chk(p_team, p_code);
  perform scambi_private.scadi();
  select * into r from scambi where id = p_id for update;
  if not found then raise exception 'Scambio non trovato'; end if;
  if r.stato <> 'attesa' then
    return jsonb_build_object('stato', r.stato, 'gia', true, 'conferma', r.conferma, 'confermato_da', r.confermato_da); end if;
  if p_azione = 'conferma' then
    if p_team = r.da then raise exception 'Lo scambio lo deve confermare un altro allenatore'; end if;
    tipo := case when p_team = r.a then 'squadra' when p_team = 'Oranje VC' then 'lega' else 'testimone' end;
    update scambi set stato = 'confermato', chiuso = now(), conferma = tipo, confermato_da = p_team where id = r.id;
    return jsonb_build_object('stato', 'confermato', 'conferma', tipo);
  elsif p_azione = 'rifiuta' then
    if p_team <> r.a then raise exception 'Può rifiutarlo solo %', r.a; end if;
    update scambi set stato = 'rifiutato', chiuso = now(), confermato_da = p_team where id = r.id;
    return jsonb_build_object('stato', 'rifiutato');
  elsif p_azione = 'annulla' then
    if p_team <> r.da then raise exception 'Può annullarlo solo %', r.da; end if;
    update scambi set stato = 'annullato', chiuso = now(), confermato_da = p_team where id = r.id;
    return jsonb_build_object('stato', 'annullato');
  end if;
  raise exception 'Azione non valida';
end $$;

-- Lettura pubblica (come la Curva): gli ultimi 40 scambi. Con il codice dice anche chi sta guardando.
create or replace function public.scambio_stato(p_team text default null, p_code text default null)
returns jsonb language plpgsql security definer set search_path to 'public' as $$
declare ok boolean := false;
begin
  if p_team is not null then ok := curva_ok(p_team, p_code); end if;
  perform scambi_private.scadi();
  return jsonb_build_object('ok', ok, 'team', case when ok then p_team end,
    'scambi', coalesce((select jsonb_agg(jsonb_build_object('id',id,'da',da,'a',a,'dai',dai,'ricevi',ricevi,'nomi',nomi,'stato',stato,
        'creato',creato,'chiuso',chiuso,'conferma',conferma,'confermato_da',confermato_da,'applicato',applicato,'esito',esito) order by id desc)
      from (select * from scambi order by id desc limit 40) q), '[]'::jsonb));
end $$;

-- Workflow (codice di Oranje VC): conferma automatica quando le rose importate da Leghe sono già scambiate
create or replace function public.scambio_srv_leghe(p_team text, p_code text, p_id bigint)
returns jsonb language plpgsql security definer set search_path to 'public' as $$
declare r scambi%rowtype;
begin
  perform curva_chk(p_team, p_code);
  if p_team <> 'Oranje VC' then raise exception 'Solo Oranje VC'; end if;
  select * into r from scambi where id = p_id for update;
  if not found then raise exception 'Scambio non trovato'; end if;
  if r.stato <> 'attesa' then return jsonb_build_object('stato', r.stato, 'gia', true); end if;
  update scambi set stato = 'confermato', chiuso = now(), conferma = 'leghe', confermato_da = 'Leghe Fantacalcio' where id = r.id;
  return jsonb_build_object('stato', 'confermato', 'conferma', 'leghe');
end $$;

-- Workflow (codice di Oranje VC): lo scambio confermato è stato applicato alle rose del sito (o non si può applicare)
create or replace function public.scambio_srv_applicato(p_team text, p_code text, p_id bigint, p_esito text, p_stato text default null)
returns void language plpgsql security definer set search_path to 'public' as $$
begin
  perform curva_chk(p_team, p_code);
  if p_team <> 'Oranje VC' then raise exception 'Solo Oranje VC'; end if;
  if p_stato is not null and p_stato <> 'non_valido' then raise exception 'Stato non valido'; end if;
  update scambi set applicato = now(), esito = left(p_esito, 200), stato = coalesce(p_stato, stato)
   where id = p_id and stato = 'confermato' and applicato is null;
end $$;

revoke all on function public.scambio_proponi(text,text,text,text[],text[],jsonb), public.scambio_rispondi(text,text,bigint,text),
  public.scambio_stato(text,text), public.scambio_srv_leghe(text,text,bigint), public.scambio_srv_applicato(text,text,bigint,text,text) from public;
grant execute on function public.scambio_proponi(text,text,text,text[],text[],jsonb), public.scambio_rispondi(text,text,bigint,text),
  public.scambio_stato(text,text), public.scambio_srv_leghe(text,text,bigint), public.scambio_srv_applicato(text,text,bigint,text,text) to anon, authenticated;

-- ── Notifiche ─────────────────────────────────────────────────────────────────────────────────────────────────────
-- Sul telefono: nuova voce «scambi» (accesa di base: la funzione push-invia manda ogni categoria che non è spenta).
create or replace function push_private.pulisci_pref(p jsonb)
 returns jsonb language sql immutable set search_path to '' as $function$
  select coalesce(jsonb_object_agg(k, (p->>k)::boolean), '{}'::jsonb)
    from unnest(array['formazione','risultati','giornale','curva','menzioni','applausi','derby','totogirrr','scambi']) k
   where p ? k and jsonb_typeof(p->k) = 'boolean'
$function$;

-- Eventi degli scambi per una squadra: richiesta diretta all'altra squadra, novità per tutti gli altri, esito a chi l'ha registrato.
create or replace function scambi_private.eventi(p_team text)
returns table(chiave text, titolo text, testo text, url text, quando timestamptz)
language sql stable security definer set search_path to 'public' as $$
  with s as (
    -- «Baldanzi e Kean», «Colpani, Adams e Kean»: virgole e l'ultima con «e»
    select x.*, regexp_replace((select string_agg(coalesce(x.nomi->g->>'n', 'Giocatore'), ', ') from unnest(x.dai) g), ', ([^,]*)$', ' e \1') nd,
                regexp_replace((select string_agg(coalesce(x.nomi->g->>'n', 'Giocatore'), ', ') from unnest(x.ricevi) g), ', ([^,]*)$', ' e \1') nr
      from scambi x where x.creato > now() - interval '30 days'
  )
  select 'sc-'||id, da||' ti propone uno scambio', 'Ti offre '||nd||' in cambio di '||nr||' · Tocca a te confermare',
         'index.html?scambio='||id, creato
    from s where a = p_team
  union all
  select 'sc-'||id, 'Richiesta di scambio: '||da||' e '||a, nd||' in cambio di '||nr||' · Puoi confermarlo come testimone',
         'index.html?scambio='||id, creato
    from s where p_team not in (da, a)
  union all
  select 'sc-ok-'||id, 'Scambio ufficiale: '||da||' e '||a, nd||' in cambio di '||nr,
         'index.html?scambio='||id, chiuso
    from s where stato = 'confermato' and chiuso is not null and (p_team <> confermato_da or confermato_da is null)
  union all
  select 'sc-no-'||id, a||' ha rifiutato lo scambio', nd||' in cambio di '||nr, 'index.html?scambio='||id, chiuso
    from s where stato = 'rifiutato' and da = p_team
$$;
revoke all on function scambi_private.eventi(text) from public, anon, authenticated;

-- push_private.eventi: copia della funzione online il 24 novembre 2026, con in fondo gli scambi
create or replace function push_private.eventi(p_team text, p_da timestamp with time zone)
 returns table(chiave text, cat text, titolo text, testo text, url text, quando timestamp with time zone)
 language sql stable security definer set search_path to 'public', 'pg_temp'
as $function$
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
    union all
    select 'men-p'||p.id, 'menzioni', p.team||' ti ha menzionato in un coro', left(p.body,140), 'apri.html?p=curva', p.created
      from curva_post p
     where p.team <> p_team and p.body ~* push_private.menzione(p_team)
    union all
    select 'men-r'||r.id, 'menzioni', r.team||' ti ha menzionato in una risposta', left(r.body,140), 'apri.html?p=curva', r.created
      from curva_reply r
     where r.team <> p_team and r.body ~* push_private.menzione(p_team)
       and not exists (select 1 from curva_post m where r.k = 'p'||m.id and m.team = p_team)
    union all
    select 'men-a'||a.id, 'menzioni',
           case a.h when 'girrr_sport' then 'Girrr Sport' when 'giornale_girrr' then 'Il Giornale' when 'ciro_trattativa' then 'Ciro Trattativa'
                    when 'lega_ofantagirrr' then 'La Lega' else initcap(replace(a.h,'_',' ')) end||' ti ha menzionato',
           left(regexp_replace(a.body, '^\[re:a\d+\]\s*', ''),140), 'apri.html?p=curva', coalesce(a.quando, a.created)
      from curva_adm a
     where a.body ~* push_private.menzione(p_team) and coalesce(a.quando, a.created) <= now()
    union all
    select x.chiave, 'scambi', x.titolo, x.testo, x.url, x.quando from scambi_private.eventi(p_team) x
  ) e(chiave, cat, titolo, testo, url, quando)
  where quando > p_da
$function$;

-- notifiche_stato: copia della funzione online il 24 novembre 2026, con in fondo gli scambi
create or replace function public.notifiche_stato(p_team text, p_code text)
 returns jsonb language plpgsql stable security definer set search_path to 'public', 'pg_temp'
as $function$
declare l notifiche_private.letture; ev jsonb;
begin
  perform curva_chk(p_team, p_code);
  select * into l from notifiche_private.letture where team = p_team;
  with e as (
    select 'risp-'||r.id chiave, 'curva' tipo, '💬' ic, r.team||' ti ha risposto' titolo, left(r.body,140) testo, r.created quando
      from curva_reply r join curva_post p on r.k = 'p'||p.id
     where p.team = p_team and r.team <> p_team
    union all
    select 'app-'||x.k||'-'||count(*), 'curva', '👏',
           case when count(*)=1 then min(x.team)||' ha applaudito il tuo coro' else count(*)||' applausi al tuo coro' end,
           left(max(x.body),140), max(x.created)
      from (select a.k, a.team, a.created, coalesce(p.body, rr.body) body
              from curva_react a
              left join curva_post p on a.k = 'p'||p.id and p.team = p_team
              left join curva_reply rr on a.k = 'r'||rr.id and rr.team = p_team
             where a.kind = 'a' and a.team <> p_team and (p.id is not null or rr.id is not null)) x
     group by x.k
    union all
    select 'sfida-'||s.id, 'derby', '⚔️', s.da||' ti ha sfidato', coalesce(nullif(s.frase_testo,''), 'Nuova sfida Derby')||case when s.stato='attesa' then ' · Tocca a te rispondere' else '' end, s.creata
      from derby_sfida s where s.a = p_team
    union all
    select 'sfida-r-'||s.id, 'derby', '⚔️', s.a||case s.stato when 'accettata' then ' ha accettato la tua sfida' when 'rifiutata' then ' ha rifiutato la tua sfida' else ' ha risposto alla tua sfida' end, coalesce(s.nome,''), s.risposta
      from derby_sfida s where s.da = p_team and s.risposta is not null
    union all
    select 'prest-'||t.id||'-'||t.stato, 'totogirrr', '🤝', 'Richiesta di prestito', case when t.creditore = p_team then t.debitore else t.creditore end||' · '||trim_scale(t.importo)::text||' · Tocca a te rispondere', t.aggiornato
      from toto_prestiti t where t.attesa_di = p_team and t.stato = 'richiesta'
    union all
    select 'mov-'||m.id, 'totogirrr', '🪙', 'Totogirrr: '||case when m.importo >= 0 then '+' else '' end||trim_scale(m.importo)::text,
           coalesce(nullif(m.nota,''), replace(m.tipo,'_',' ')), m.creato
      from toto_movimenti m where m.team = p_team
    union all
    select x.chiave, 'scambi', '🔁', x.titolo, x.testo, x.quando from scambi_private.eventi(p_team) x
  )
  select coalesce(jsonb_agg(jsonb_build_object('chiave',chiave,'tipo',tipo,'ic',ic,'titolo',titolo,'testo',testo,'quando',quando,
           'nuova', quando > coalesce(l.letto_fino, to_timestamp(0))) order by quando desc), '[]'::jsonb)
    into ev
    from (select * from e where quando > now() - interval '30 days' order by quando desc limit 40) z;
  return jsonb_build_object('letto_fino', l.letto_fino, 'chiavi', coalesce(to_jsonb(l.chiavi), '[]'::jsonb), 'eventi', ev);
end $function$;

-- Ritorno indietro delle notifiche: rieseguire le definizioni del 24 novembre 2026 senza le righe «scambi»
-- (sono in questo file: basta togliere l'ultimo «union all» di ognuna e 'scambi' da pulisci_pref).
