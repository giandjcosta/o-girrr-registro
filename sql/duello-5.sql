-- Versione 5.0 · Sfide 1 contro 1 di Totogirrr (Supabase).
-- Chi lancia sceglie un avversario e una posta (da 10 a 200 fantacrediti, e mai più di quello che hanno entrambi in quel momento).
-- Se l'altro accetta, nella giornata scelta vince chi fa più punti e prende le due poste; pareggio: ognuno riprende la sua.
-- I fantacrediti sono quelli veri di toto_conti: la posta di chi lancia è bloccata subito, quella di chi accetta all'accettazione.
-- Se la sfida non viene accettata prima dell'inizio della giornata (o entro 3 giorni), decade e la posta torna indietro.
-- Stesso schema del resto: nessun accesso diretto alle tabelle, tutto passa da funzioni che controllano il codice squadra (toto_chk).

create table if not exists toto_duelli(
  id bigserial primary key,
  giornata int not null,
  da text not null,
  a text not null,
  posta numeric not null check (posta between 10 and 200 and posta = round(posta)),
  stato text not null default 'attesa' check (stato in ('attesa','accettato','rifiutato','scaduto','chiuso')),
  creato timestamptz not null default now(),
  risposto timestamptz,
  pa numeric, pb numeric,
  vincitore text,
  check (da <> a)
);
alter table toto_duelli enable row level security;

-- Inizio della giornata di campionato (la prima partita che chiude le scommesse)
create or replace function duello_inizio(p_g int) returns timestamptz language sql stable security definer set search_path to 'public' as $$
  select min(chiude) from toto_partite where comp = 'lega' and giornata = p_g;
$$;
-- Prossima giornata di campionato non ancora iniziata
create or replace function duello_prossima() returns int language sql stable security definer set search_path to 'public' as $$
  select giornata from toto_partite where comp = 'lega' group by giornata having min(chiude) > now() order by giornata limit 1;
$$;

-- Le sfide non accettate in tempo decadono e la posta torna a chi l'aveva messa
create or replace function duello_scadi() returns void language plpgsql security definer set search_path to 'public' as $$
declare r toto_duelli%rowtype;
begin
  for r in select * from toto_duelli where stato = 'attesa'
           and (creato < now() - interval '3 days' or coalesce(duello_inizio(giornata), now()) <= now()) for update loop
    update toto_conti set crediti = crediti + r.posta where team = r.da;
    insert into toto_movimenti(team,tipo,importo,nota) values (r.da,'duello_rimborso',r.posta,'Sfida a '||r.a||' scaduta: posta restituita');
    update toto_duelli set stato = 'scaduto', risposto = now() where id = r.id;
  end loop;
end $$;

create or replace function duello_lancia(p_team text, p_code text, p_rival text, p_posta numeric, p_giornata int default null) returns jsonb
language plpgsql security definer set search_path to 'public' as $$
declare g int; cr numeric; cr2 numeric; nid bigint;
begin
  perform toto_chk(p_team, p_code);
  perform duello_scadi();
  if p_rival = p_team then raise exception 'Non puoi sfidare te stesso'; end if;
  select crediti into cr2 from toto_conti where team = p_rival;
  if not found then raise exception 'Quella squadra non ha ancora un conto Totogirrr'; end if;
  g := coalesce(p_giornata, duello_prossima());
  if g is null or coalesce(duello_inizio(g), now()) <= now() then raise exception 'Quella giornata è già iniziata'; end if;
  if p_posta is null or p_posta <> round(p_posta) or p_posta < 10 then raise exception 'Posta minima: 10 fantacrediti'; end if;
  if p_posta > 200 then raise exception 'Posta massima: 200 fantacrediti'; end if;
  select crediti into cr from toto_conti where team = p_team for update;
  if p_posta > cr then raise exception 'Non hai abbastanza fantacrediti'; end if;
  if p_posta > cr2 then raise exception 'Il tuo avversario ha solo % fantacrediti: abbassa la posta', cr2; end if;
  if exists (select 1 from toto_duelli where giornata = g and stato in ('attesa','accettato') and ((da = p_team and a = p_rival) or (da = p_rival and a = p_team))) then
    raise exception 'C''è già una sfida tra voi due per questa giornata'; end if;
  if (select count(*) from toto_duelli where da = p_team and giornata = g and stato in ('attesa','accettato')) >= 3 then
    raise exception 'Hai già tre sfide per questa giornata'; end if;
  update toto_conti set crediti = crediti - p_posta where team = p_team;
  insert into toto_duelli(giornata, da, a, posta) values (g, p_team, p_rival, p_posta) returning id into nid;
  insert into toto_movimenti(team,tipo,importo,nota) values (p_team,'duello_posta',-p_posta,'Sfida a '||p_rival||' per la giornata '||g);
  return jsonb_build_object('id', nid, 'giornata', g);
end $$;

create or replace function duello_rispondi(p_team text, p_code text, p_id bigint, p_azione text) returns jsonb
language plpgsql security definer set search_path to 'public' as $$
declare r toto_duelli%rowtype; cr numeric;
begin
  perform toto_chk(p_team, p_code);
  perform duello_scadi();
  select * into r from toto_duelli where id = p_id for update;
  if not found or r.a <> p_team or r.stato <> 'attesa' then raise exception 'Nessuna sfida a cui rispondere'; end if;
  if p_azione = 'rifiuta' then
    update toto_conti set crediti = crediti + r.posta where team = r.da;
    insert into toto_movimenti(team,tipo,importo,nota) values (r.da,'duello_rimborso',r.posta,r.a||' ha rifiutato la sfida: posta restituita');
    update toto_duelli set stato = 'rifiutato', risposto = now() where id = r.id;
    return jsonb_build_object('stato','rifiutato');
  elsif p_azione = 'accetta' then
    select crediti into cr from toto_conti where team = p_team for update;
    if cr < r.posta then raise exception 'Non hai abbastanza fantacrediti per accettare (servono %)', r.posta; end if;
    update toto_conti set crediti = crediti - r.posta where team = p_team;
    insert into toto_movimenti(team,tipo,importo,nota) values (p_team,'duello_posta',-r.posta,'Sfida di '||r.da||' per la giornata '||r.giornata);
    update toto_duelli set stato = 'accettato', risposto = now() where id = r.id;
    return jsonb_build_object('stato','accettato');
  end if;
  raise exception 'Azione non valida';
end $$;

-- Lettura: le sfide recenti (di tutti, come in Curva) e, per ognuno, quanti fantacrediti ha adesso (serve a calcolare la posta massima)
create or replace function duello_stato(p_team text default null, p_code text default null) returns jsonb
language plpgsql security definer set search_path to 'public' as $$
declare ok boolean := false;
begin
  if p_team is not null then
    begin perform toto_chk(p_team, p_code); ok := true; exception when others then ok := false; end;
  end if;
  perform duello_scadi();
  return jsonb_build_object(
    'ok', ok,
    'prossima', duello_prossima(),
    'inizio', (select duello_inizio(duello_prossima())),
    'crediti', coalesce((select jsonb_object_agg(team, crediti) from toto_conti), '{}'::jsonb),
    'duelli', coalesce((select jsonb_agg(jsonb_build_object('id',id,'giornata',giornata,'da',da,'a',a,'posta',posta,'stato',stato,
        'ts',extract(epoch from creato)*1000,'pa',pa,'pb',pb,'vincitore',vincitore) order by id desc)
      from (select * from toto_duelli order by id desc limit 60) q), '[]'::jsonb));
end $$;

-- Chiusura (solo Oranje VC, cioè il workflow dei calcoli): p_punti = {"squadra": punti della giornata, ...}
create or replace function duello_chiudi(p_team text, p_code text, p_giornata int, p_punti jsonb) returns int
language plpgsql security definer set search_path to 'public' as $$
declare r toto_duelli%rowtype; x numeric; y numeric; n int := 0;
begin
  perform curva_chk(p_team, p_code);
  if p_team <> 'Oranje VC' then raise exception 'Solo Oranje VC'; end if;
  for r in select * from toto_duelli where giornata = p_giornata and stato = 'accettato' for update loop
    x := (p_punti ->> r.da)::numeric; y := (p_punti ->> r.a)::numeric;
    if x is null or y is null then continue; end if;
    if x > y then
      update toto_conti set crediti = crediti + 2*r.posta where team = r.da;
      insert into toto_movimenti(team,tipo,importo,nota) values (r.da,'duello_vincita',2*r.posta,'Sfida vinta contro '||r.a||' ('||x||' a '||y||')');
    elsif y > x then
      update toto_conti set crediti = crediti + 2*r.posta where team = r.a;
      insert into toto_movimenti(team,tipo,importo,nota) values (r.a,'duello_vincita',2*r.posta,'Sfida vinta contro '||r.da||' ('||y||' a '||x||')');
    else
      update toto_conti set crediti = crediti + r.posta where team in (r.da, r.a);
      insert into toto_movimenti(team,tipo,importo,nota) values (r.da,'duello_rimborso',r.posta,'Sfida pari con '||r.a||': posta restituita'),(r.a,'duello_rimborso',r.posta,'Sfida pari con '||r.da||': posta restituita');
    end if;
    update toto_duelli set stato = 'chiuso', pa = x, pb = y, vincitore = case when x > y then r.da when y > x then r.a end, risposto = now() where id = r.id;
    n := n + 1;
  end loop;
  return n;
end $$;
