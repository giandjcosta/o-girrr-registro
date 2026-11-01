-- Notifiche personali della Lega (1° novembre 2026, «vai» di Gianluca).
-- Solo oggetti nuovi: schema privato notifiche_private, tabella letture, funzioni notifiche_stato e notifiche_segna_lette.
-- Le notifiche personali si calcolano dalle tabelle esistenti (Curva, Derby, Totogirrr): nessun dato duplicato.
-- Per tornare indietro: drop function public.notifiche_stato(text,text); drop function public.notifiche_segna_lette(text,text,text[]); drop schema notifiche_private cascade;

create schema if not exists notifiche_private;
revoke all on schema notifiche_private from public, anon, authenticated;

create table if not exists notifiche_private.letture(
  team text primary key,
  letto_fino timestamptz not null default to_timestamp(0),
  chiavi text[] not null default '{}',
  aggiornato timestamptz not null default now()
);
alter table notifiche_private.letture enable row level security;
revoke all on notifiche_private.letture from public, anon, authenticated;

create or replace function public.notifiche_stato(p_team text, p_code text)
returns jsonb language plpgsql stable security definer set search_path = public, pg_temp as $f$
declare l notifiche_private.letture; ev jsonb;
begin
  perform curva_chk(p_team, p_code);
  select * into l from notifiche_private.letture where team = p_team;
  with e as (
    -- risposte ai miei post in Curva
    select 'risp-'||r.id chiave, 'curva' tipo, '💬' ic, r.team||' ti ha risposto' titolo, left(r.body,140) testo, r.created quando
      from curva_reply r join curva_post p on r.k = 'p'||p.id
     where p.team = p_team and r.team <> p_team
    union all
    -- applausi ai miei post e alle mie risposte (uno per post, con il numero)
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
    -- sfide Derby ricevute
    select 'sfida-'||s.id, 'derby', '⚔️', s.da||' ti ha sfidato', coalesce(nullif(s.frase_testo,''), 'Nuova sfida Derby')||case when s.stato='attesa' then ' · Tocca a te rispondere' else '' end, s.creata
      from derby_sfida s where s.a = p_team
    union all
    -- risposte alle mie sfide
    select 'sfida-r-'||s.id, 'derby', '⚔️', s.a||case s.stato when 'accettata' then ' ha accettato la tua sfida' when 'rifiutata' then ' ha rifiutato la tua sfida' else ' ha risposto alla tua sfida' end, coalesce(s.nome,''), s.risposta
      from derby_sfida s where s.da = p_team and s.risposta is not null
    union all
    -- prestiti che aspettano una mia risposta
    select 'prest-'||t.id||'-'||t.stato, 'totogirrr', '🤝', 'Richiesta di prestito', case when t.creditore = p_team then t.debitore else t.creditore end||' · '||trim_scale(t.importo)::text||' · Tocca a te rispondere', t.aggiornato
      from toto_prestiti t where t.attesa_di = p_team and t.stato = 'richiesta'
    union all
    -- movimenti del Totogirrr
    select 'mov-'||m.id, 'totogirrr', '🪙', 'Totogirrr: '||case when m.importo >= 0 then '+' else '' end||trim_scale(m.importo)::text,
           coalesce(nullif(m.nota,''), replace(m.tipo,'_',' ')), m.creato
      from toto_movimenti m where m.team = p_team
  )
  select coalesce(jsonb_agg(jsonb_build_object('chiave',chiave,'tipo',tipo,'ic',ic,'titolo',titolo,'testo',testo,'quando',quando,
           'nuova', quando > coalesce(l.letto_fino, to_timestamp(0))) order by quando desc), '[]'::jsonb)
    into ev
    from (select * from e where quando > now() - interval '30 days' order by quando desc limit 40) z;
  return jsonb_build_object('letto_fino', l.letto_fino, 'chiavi', coalesce(to_jsonb(l.chiavi), '[]'::jsonb), 'eventi', ev);
end $f$;

create or replace function public.notifiche_segna_lette(p_team text, p_code text, p_chiavi text[] default '{}')
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $f$
declare k text[];
begin
  perform curva_chk(p_team, p_code);
  if coalesce(array_length(p_chiavi,1),0) > 100 then raise exception 'Troppe notifiche in una volta'; end if;
  if exists(select 1 from unnest(coalesce(p_chiavi,'{}')) c where char_length(c) > 80) then raise exception 'Chiave non valida'; end if;
  insert into notifiche_private.letture(team, letto_fino, chiavi, aggiornato)
       values (p_team, now(), coalesce(p_chiavi,'{}'), now())
  on conflict (team) do update set letto_fino = now(), aggiornato = now(),
       chiavi = (select coalesce(array_agg(c), '{}') from (select distinct c from unnest(notifiche_private.letture.chiavi || coalesce(excluded.chiavi,'{}')) c order by c desc limit 200) s)
  returning chiavi into k;
  return jsonb_build_object('letto_fino', now(), 'chiavi', to_jsonb(k));
end $f$;

revoke all on function public.notifiche_stato(text,text) from public;
revoke all on function public.notifiche_segna_lette(text,text,text[]) from public;
grant execute on function public.notifiche_stato(text,text) to anon, authenticated;
grant execute on function public.notifiche_segna_lette(text,text,text[]) to anon, authenticated;
