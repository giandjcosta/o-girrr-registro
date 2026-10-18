-- Quote Derby di Totogirrr (5.0)
-- Regole: +15% su ogni esito delle partite Derby; moltiplicatore +10% sulla schedina che contiene un Derby (si applica sopra);
-- cashback 20% della puntata se la schedina con un Derby perde. Valgono dal giorno in cui nasce il Derby: se nasce a giornata iniziata
-- la quota di quella giornata resta normale. Le schedine già giocate non cambiano mai (quota salvata al momento del gioco).

create table if not exists derby_rivalita(a text not null, b text not null, r numeric not null, primary key(a,b));
alter table derby_rivalita enable row level security;
insert into derby_rivalita(a,b,r)
select least(x,y), greatest(x,y), r from (values
 ('Apo team','WOA',94.3),('Apo team','Real Madrink',60),('WOA','Real Madrink',60),('WOA','Grodah',88.6),('Apo team','The Blue brothers',82.9),
 ('WOA','The Blue brothers',82.9),('Apo team','Grodah',82.9),('Real Madrink','The Blue brothers',54.3),('Grodah','The Blue brothers',80)) v(x,y,r)
on conflict do nothing;

-- Interruttore: finché non si accende (al rilascio) le quote restano quelle di prima
create table if not exists derby_cfg(k text primary key, v boolean not null default false);
alter table derby_cfg enable row level security;
insert into derby_cfg(k,v) values ('quote', false) on conflict do nothing;

create table if not exists derby_attivi(a text not null, b text not null, dal timestamptz not null default now(), primary key(a,b));
alter table derby_attivi enable row level security;

alter table toto_selezioni add column if not exists derby boolean not null default false;

-- Chi è Derby adesso: votato dai più, oppure Sfida accettata con il nome concordato; se i più dicono no non lo è; altrimenti vale la rivalità (>= 50)
create or replace function derby_aggiorna() returns void language plpgsql security definer set search_path to 'public' as $$
begin
  create temp table _d on commit drop as
  with k as (
    select a, b from derby_voto union select a, b from derby_rivalita union select least(da,a), greatest(da,a) from derby_sfida),
  c as (
    select k.a, k.b,
      (select count(*) from derby_voto v where v.a = k.a and v.b = k.b and v.si) si,
      (select count(*) from derby_voto v where v.a = k.a and v.b = k.b and not v.si) no,
      exists(select 1 from derby_sfida s where s.stato = 'accettata' and s.nome_ok and least(s.da,s.a) = k.a and greatest(s.da,s.a) = k.b) sf,
      coalesce((select r.r from derby_rivalita r where r.a = k.a and r.b = k.b), 0) rv
    from k)
  select a, b from c where sf or (case when no > si then false when si > no then true else rv >= 50 end);
  delete from derby_attivi x where not exists(select 1 from _d where _d.a = x.a and _d.b = x.b);
  insert into derby_attivi(a,b) select a,b from _d on conflict do nothing;
  drop table _d;
end $$;

create or replace function derby_trg() returns trigger language plpgsql security definer set search_path to 'public' as $$
begin perform derby_aggiorna(); return null; end $$;
drop trigger if exists derby_voto_trg on derby_voto;
create trigger derby_voto_trg after insert or update or delete on derby_voto for each statement execute function derby_trg();
drop trigger if exists derby_sfida_trg on derby_sfida;
create trigger derby_sfida_trg after insert or update or delete on derby_sfida for each statement execute function derby_trg();

-- Una partita è Derby se la sua coppia era già Derby prima che iniziasse la giornata (la prima partita della giornata)
create or replace function toto_e_derby(p toto_partite) returns boolean language sql stable security definer set search_path to 'public','pg_temp' as $$
  select p.trasf is not null and coalesce((select v from derby_cfg where k = 'quote'), false) and exists(
    select 1 from derby_attivi d
    where d.a = least(p.casa, p.trasf) and d.b = greatest(p.casa, p.trasf)
      and d.dal <= (select min(t.chiude) from toto_partite t where t.comp = p.comp and t.giornata = p.giornata)) $$;

create or replace function toto_quota(p toto_partite, m text) returns numeric language sql stable set search_path to 'public','pg_temp' as $$
  select case when toto_e_derby(p) then round(b * 1.15, 2) else b end
  from (select case m when '1' then p.q1 when 'X' then p.qx when '2' then p.q2 when 'O' then p.qo when 'U' then p.qu
          else (p.extra ->> m)::numeric end b) x $$;

create or replace function toto_gioca(p_team text, p_code text, p_puntata numeric, p_sel jsonb)
returns jsonb language plpgsql security definer set search_path to 'public' as $$
declare cr numeric; n int; q numeric := 1; e jsonb; pa toto_partite%rowtype; qq numeric; sid bigint; visti text[] := '{}'; der boolean; haderby boolean := false;
begin
  perform toto_chk(p_team, p_code);
  if p_puntata is null or p_puntata < 5 then raise exception 'Puntata minima: 5 fantacrediti'; end if;
  if p_puntata <> round(p_puntata,2) then raise exception 'Puntata non valida'; end if;
  n := coalesce(jsonb_array_length(p_sel),0);
  if n < 1 then raise exception 'Scegli almeno un esito'; end if;
  if n > 6 then raise exception 'Massimo 6 partite in una multipla'; end if;
  select crediti into cr from toto_conti where team = p_team for update;
  if p_puntata > cr then raise exception 'Fantacrediti insufficienti'; end if;
  insert into toto_schedine(team, puntata, quota) values (p_team, p_puntata, 1) returning id into sid;
  for e in select * from jsonb_array_elements(p_sel) loop
    select * into pa from toto_partite where id = e->>'p';
    if not found then raise exception 'Partita inesistente'; end if;
    if pa.chiusa or pa.chiude <= now() then raise exception 'Scommesse chiuse per %', trim(pa.casa || ' ' || pa.trasf); end if;
    if pa.id = any(visti) then raise exception 'Due esiti della stessa partita non si possono mettere insieme'; end if;
    visti := visti || pa.id;
    if pa.comp <> 'vinc' and (pa.casa = p_team or pa.trasf = p_team) and p_puntata > 100 then raise exception 'Sulla tua partita puntata massima 100'; end if;
    qq := toto_quota(pa, e->>'m');
    if qq is null then raise exception 'Esito non valido'; end if;
    der := toto_e_derby(pa);
    haderby := haderby or der;
    insert into toto_selezioni(schedina, partita, mercato, quota, derby) values (sid, pa.id, e->>'m', qq, der);
    q := q * qq;
  end loop;
  if haderby then q := q * 1.10; end if;
  q := least(round(q,2), 500);
  update toto_schedine set quota = q where id = sid;
  update toto_conti set crediti = crediti - p_puntata where team = p_team;
  return jsonb_build_object('id', sid, 'quota', q, 'vincita_possibile', round(p_puntata*q,2), 'derby', haderby);
end $$;

create or replace function toto_risolvi(p_id text) returns integer language plpgsql security definer set search_path to 'public' as $$
declare s record; l record; n_v int; n_p int; n_sch int := 0; vin numeric; tr numeric; cd numeric; dp numeric; quota numeric; rest numeric; pay numeric; tot numeric; cb numeric;
begin
  for s in select distinct sc.id, sc.team, sc.puntata, sc.quota from toto_schedine sc join toto_selezioni x on x.schedina = sc.id
           where x.partita = p_id and sc.stato = 'aperta' loop
    select count(*) filter (where esito='v'), count(*) filter (where esito='p') into n_v, n_p from toto_selezioni where schedina = s.id;
    if n_p > 0 then
      update toto_schedine set stato = 'persa' where id = s.id; n_sch := n_sch + 1;
      if exists(select 1 from toto_selezioni where schedina = s.id and derby) then
        cb := round(s.puntata * 0.20, 2);
        update toto_conti set crediti = crediti + cb where team = s.team;
        insert into toto_movimenti(team,tipo,importo,nota) values (s.team,'cashback_derby',cb,'Cashback Derby: 20% della puntata, schedina persa');
      end if;
    elsif n_v = (select count(*) from toto_selezioni where schedina = s.id) then
      vin := round(s.puntata*s.quota,2);
      select debito, debito_p into cd, dp from toto_conti where team = s.team for update;
      tr := least(cd, round(vin*0.4,2));
      quota := least(dp, round(vin*0.25,2)); rest := quota; tot := 0;
      for l in select * from toto_prestiti where debitore = s.team and stato = 'attivo' order by creato for update loop
        exit when rest <= 0;
        pay := least(rest, round(l.importo*l.tasso,2) - l.restituito);
        if pay > 0 then
          update toto_prestiti set restituito = restituito + pay, stato = case when restituito + pay >= round(importo*tasso,2) then 'chiuso' else stato end, aggiornato = now() where id = l.id;
          update toto_conti set crediti = crediti + pay where team = l.creditore;
          insert into toto_movimenti(team,tipo,importo,nota) values
            (l.creditore,'rimborso_ricevuto',pay,'Rimborso automatico da '||s.team||' (25% di una vincita)'),
            (s.team,'rimborso',-pay,'25% della vincita a '||l.creditore||' per il prestito');
          rest := rest - pay; tot := tot + pay;
        end if;
      end loop;
      update toto_schedine set stato = 'vinta', vincita = vin where id = s.id;
      update toto_conti set crediti = crediti + vin - tr - tot, debito = debito - tr, debito_p = greatest(0, debito_p - tot) where team = s.team;
      if tr > 0 then insert into toto_movimenti(team,tipo,importo,nota) values (s.team,'banco',-tr,'40% della vincita trattenuto dal banco per il prestito'); end if;
      n_sch := n_sch + 1;
    end if;
  end loop;
  return n_sch;
end $$;

-- toto_stato: ogni partita dice se è Derby, ogni selezione se lo era quando è stata giocata
do $$
declare d text;
begin
  select pg_get_functiondef(oid) into d from pg_proc where proname = 'toto_stato' and pronamespace = 'public'::regnamespace;
  d := replace(d, 'jsonb_agg(to_jsonb(p) order by p.chiude, p.id)', 'jsonb_agg(to_jsonb(p) || jsonb_build_object(''derby'', toto_e_derby(p)) order by p.chiude, p.id)');
  d := replace(d, '''esito'',x.esito)', '''esito'',x.esito,''derby'',x.derby)');
  if position('toto_e_derby' in d) = 0 or position('x.derby' in d) = 0 then raise exception 'toto_stato non modificata'; end if;
  execute d;
end $$;

select derby_aggiorna();
