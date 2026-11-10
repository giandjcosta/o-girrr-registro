-- Notifiche sul telefono · Menzioni in Curva (Claude, 10 novembre 2026, richiesta di Gianluca: «servirebbe la notifica push
-- quando qualcuno ti tagga, almeno come opzione attivabile o meno»).
-- DA APPLICARE SOLO CON IL «VAI» DI GIANLUCA SUL DATABASE (progetto qmjqfgmvimsuxvghetgi).
-- Cosa cambia: solo lo schema push_private (le notifiche push). Nessuna tabella nuova, nessun dato cambiato.
--   1. push_private.menzione(team): il tag della squadra come nella Curva («Oranje VC» -> @oranje_vc), riconosciuto
--      solo se è intero (non dentro @oranje_vc2) e non preceduto da una lettera (le email non contano).
--   2. push_private.pulisci_pref: accetta la nuova preferenza «menzioni» (vero/falso).
--   3. push_private.eventi: la stessa di prima (rilascio/push/da-incollare.sql) più le menzioni, categoria «menzioni».
-- La funzione «push-invia» non cambia: manda una categoria se la preferenza non è falsa, quindi le menzioni partono accese
-- e si spengono con l'interruttore «Menzioni» nella pagina Notifiche (push.js).
-- Per tornare indietro: rieseguire le due funzioni di rilascio/push/da-incollare.sql (righe di pulisci_pref ed eventi)
-- e cancellare push_private.menzione.

create or replace function push_private.menzione(p_team text) returns text
language sql immutable set search_path = '' as $$
  select '(^|[^a-z0-9_@])@' || trim(both '_' from regexp_replace(lower(p_team), '[^a-z0-9]+', '_', 'g')) || '([^a-z0-9_]|$)'
$$;
revoke all on function push_private.menzione(text) from public, anon, authenticated;

create or replace function push_private.pulisci_pref(p jsonb) returns jsonb
language sql immutable set search_path = '' as $$
  select coalesce(jsonb_object_agg(k, (p->>k)::boolean), '{}'::jsonb)
    from unnest(array['formazione','risultati','giornale','curva','menzioni','applausi','derby','totogirrr']) k
   where p ? k and jsonb_typeof(p->k) = 'boolean'
$$;

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
    union all
    -- 5.7: menzioni in Curva (cori, risposte e post ufficiali come Girrr Sport). Le risposte ai tuoi cori sono già «ti ha risposto».
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
  ) e(chiave, cat, titolo, testo, url, quando)
  where quando > p_da
$$;
revoke all on function push_private.eventi(text, timestamptz) from public, anon, authenticated;
