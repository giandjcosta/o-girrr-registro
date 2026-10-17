-- Versione 5.0 · derby, sfide e conferenza stampa (Supabase).
-- Stesso schema di Curva: nessun accesso diretto alle tabelle, tutto passa dalle funzioni che controllano il codice squadra.
-- Non tocca le tabelle esistenti. È sicuro rieseguirlo. Già applicato al database della lega e provato con una prova annullata (nessun dato scritto).

create table if not exists derby_sfida(
  id bigserial primary key,
  stagione text not null,
  da text not null,
  a text not null,
  frase int not null check (frase between 0 and 2),
  nome text check (nome is null or char_length(nome) between 3 and 40),
  nome_ok boolean not null default false,
  stato text not null default 'attesa' check (stato in ('attesa','accettata','rifiutata','scaduta')),
  creata timestamptz not null default now(),
  risposta timestamptz,
  check (da <> a)
);
create index if not exists derby_sfida_s on derby_sfida(stagione, da);

create table if not exists derby_voto(
  a text not null,
  b text not null,
  team text not null,
  si boolean not null,
  creato timestamptz not null default now(),
  primary key (a, b, team),
  check (a < b)
);

create table if not exists conf_risposta(
  team text not null,
  giornata int not null check (giornata between 1 and 60),
  risposte jsonb not null,
  libera text check (libera is null or char_length(libera) <= 80),
  promessa text check (promessa is null or char_length(promessa) <= 80),
  pesa int not null default 1 check (pesa between 0 and 3),
  esito text check (esito is null or esito in ('v','p','s')),
  creata timestamptz not null default now(),
  primary key (team, giornata)
);

alter table derby_sfida enable row level security;
alter table derby_voto enable row level security;
alter table conf_risposta enable row level security;
revoke all on derby_sfida, derby_voto, conf_risposta from anon, authenticated;
revoke all on sequence derby_sfida_id_seq from anon, authenticated;

-- Le sfide senza risposta decadono dopo tre giorni
create or replace function derby_scadi() returns void language sql security definer set search_path=public as $$
  update derby_sfida set stato='scaduta', risposta=now() where stato='attesa' and creata < now() - interval '3 days';
$$;

-- Lancia una sfida: una alla volta, al massimo due a stagione per squadra
create or replace function derby_sfida_lancia(p_team text, p_code text, p_rival text, p_frase int, p_nome text default null, p_stagione text default '2026/27')
returns bigint language plpgsql security definer set search_path=public as $$
declare i bigint; nm text:=nullif(btrim(coalesce(p_nome,'')),'');
begin
  perform curva_chk(p_team, p_code);
  perform derby_scadi();
  if p_rival = p_team then raise exception 'Non puoi sfidare te stesso'; end if;
  if not exists(select 1 from curva_lock where team = p_rival) then raise exception 'Squadra non valida'; end if;
  if p_frase not between 0 and 2 then raise exception 'Frase non valida'; end if;
  if nm is not null and char_length(nm) not between 3 and 40 then raise exception 'Il nome deve avere da 3 a 40 caratteri'; end if;
  if exists(select 1 from derby_sfida where da = p_team and stato = 'attesa') then raise exception 'Hai già una sfida in attesa'; end if;
  if (select count(*) from derby_sfida where da = p_team and stagione = p_stagione) >= 2 then raise exception 'Hai usato le due sfide di questa stagione'; end if;
  insert into derby_sfida(stagione, da, a, frase, nome) values(p_stagione, p_team, p_rival, p_frase, nm) returning id into i;
  return i;
end $$;

-- Il rivale risponde: accetta (e conferma o cambia il nome) oppure rifiuta
create or replace function derby_sfida_rispondi(p_team text, p_code text, p_id bigint, p_azione text, p_nome text default null)
returns void language plpgsql security definer set search_path=public as $$
declare r derby_sfida; nm text:=nullif(btrim(coalesce(p_nome,'')),'');
begin
  perform curva_chk(p_team, p_code);
  perform derby_scadi();
  select * into r from derby_sfida where id = p_id and a = p_team and stato = 'attesa';
  if not found then raise exception 'Nessuna sfida da rispondere'; end if;
  if p_azione = 'accetta' then
    if nm is not null and char_length(nm) not between 3 and 40 then raise exception 'Il nome deve avere da 3 a 40 caratteri'; end if;
    update derby_sfida set stato = 'accettata', risposta = now(), nome = coalesce(nm, nome), nome_ok = (coalesce(nm, nome) is not null) where id = p_id;
  elsif p_azione = 'rifiuta' then
    update derby_sfida set stato = 'rifiutata', risposta = now() where id = p_id;
  else
    raise exception 'Azione non valida';
  end if;
end $$;

-- Chi ha lanciato la sfida può proporre o cambiare il nome finché il rivale non risponde
create or replace function derby_sfida_nome(p_team text, p_code text, p_id bigint, p_nome text)
returns void language plpgsql security definer set search_path=public as $$
declare nm text:=btrim(coalesce(p_nome,''));
begin
  perform curva_chk(p_team, p_code);
  if char_length(nm) not between 3 and 40 then raise exception 'Il nome deve avere da 3 a 40 caratteri'; end if;
  update derby_sfida set nome = nm where id = p_id and da = p_team and stato = 'attesa';
  if not found then raise exception 'Sfida non trovata o già chiusa'; end if;
end $$;

-- Un amico dice se una coppia è un derby (vale il suo voto, cambiabile)
create or replace function derby_vota(p_team text, p_code text, p_a text, p_b text, p_si boolean)
returns void language plpgsql security definer set search_path=public as $$
declare x text:=least(p_a, p_b); y text:=greatest(p_a, p_b);
begin
  perform curva_chk(p_team, p_code);
  if p_a = p_b then raise exception 'Coppia non valida'; end if;
  if not exists(select 1 from curva_lock where team = p_a) or not exists(select 1 from curva_lock where team = p_b) then raise exception 'Squadra non valida'; end if;
  insert into derby_voto(a, b, team, si) values(x, y, p_team, p_si)
  on conflict (a, b, team) do update set si = excluded.si, creato = now();
end $$;

-- Lettura libera, come il feed di Curva: sfide recenti e voti. Con il codice giusto torna anche la conferenza della squadra.
create or replace function derby_stato(p_team text default null, p_code text default null)
returns json language plpgsql security definer set search_path=public as $$
declare ok boolean:=p_team is not null and curva_ok(p_team, p_code); res json;
begin
  perform derby_scadi();
  select json_build_object(
    'ok', ok,
    'sfide', coalesce((select json_agg(json_build_object('id',id,'stagione',stagione,'da',da,'a',a,'frase',frase,'nome',nome,'nome_ok',nome_ok,'stato',stato,'ts',extract(epoch from creata)*1000,'risp',extract(epoch from risposta)*1000) order by creata desc)
      from (select * from derby_sfida order by creata desc limit 60) q), '[]'::json),
    'voti', coalesce((select json_agg(json_build_object('a',a,'b',b,'si',n_si,'no',n_no)) from
      (select a, b, count(*) filter (where si) n_si, count(*) filter (where not si) n_no from derby_voto group by a, b) v), '[]'::json),
    'miei', case when ok then coalesce((select json_agg(json_build_object('a',a,'b',b,'si',si)) from derby_voto where team = p_team), '[]'::json) else '[]'::json end,
    'conf', case when ok then coalesce((select json_agg(json_build_object('giornata',giornata,'risposte',risposte,'libera',libera,'promessa',promessa,'pesa',pesa,'esito',esito) order by giornata) from conf_risposta where team = p_team), '[]'::json) else '[]'::json end
  ) into res;
  return res;
end $$;

-- Conferenza stampa: tre risposte tra quelle proposte e una libera (massimo 80 caratteri). Non si cambia dopo l'esito.
create or replace function conf_salva(p_team text, p_code text, p_giornata int, p_risposte jsonb, p_libera text default null, p_promessa text default null, p_pesa int default 1)
returns void language plpgsql security definer set search_path=public as $$
declare lb text:=nullif(btrim(coalesce(p_libera,'')),''); pr text:=nullif(btrim(coalesce(p_promessa,'')),'');
begin
  perform curva_chk(p_team, p_code);
  if jsonb_typeof(p_risposte) <> 'array' or jsonb_array_length(p_risposte) > 4 then raise exception 'Risposte non valide'; end if;
  if lb is not null and char_length(lb) > 80 then raise exception 'La risposta libera può avere al massimo 80 caratteri'; end if;
  if pr is not null and char_length(pr) > 80 then raise exception 'La promessa può avere al massimo 80 caratteri'; end if;
  if exists(select 1 from conf_risposta where team = p_team and giornata = p_giornata and esito is not null) then raise exception 'Conferenza già chiusa'; end if;
  insert into conf_risposta(team, giornata, risposte, libera, promessa, pesa) values(p_team, p_giornata, p_risposte, lb, pr, greatest(0, least(3, coalesce(p_pesa,1))))
  on conflict (team, giornata) do update set risposte = excluded.risposte, libera = excluded.libera, promessa = excluded.promessa, pesa = excluded.pesa;
end $$;

-- Solo Oranje VC (o lo script della giornata, con il suo codice) registra l'esito di una promessa: v mantenuta, p pareggio, s tradita
create or replace function conf_risolvi(p_team text, p_code text, p_target text, p_giornata int, p_esito text)
returns void language plpgsql security definer set search_path=public as $$
begin
  perform curva_chk(p_team, p_code);
  if p_team <> 'Oranje VC' then raise exception 'Solo Oranje VC'; end if;
  if p_esito not in ('v','p','s') then raise exception 'Esito non valido'; end if;
  update conf_risposta set esito = p_esito where team = p_target and giornata = p_giornata;
  if not found then raise exception 'Conferenza non trovata'; end if;
end $$;

-- Panoramica per tutti delle promesse con il loro esito (senza le risposte intere)
create or replace function conf_promesse() returns json language sql stable security definer set search_path=public as $$
  select coalesce(json_agg(json_build_object('team',team,'giornata',giornata,'promessa',promessa,'pesa',pesa,'esito',esito) order by giornata desc), '[]'::json)
  from conf_risposta where promessa is not null;
$$;
