-- Versione 5.0 · il nome del Derby si concorda a più giri.
-- Chi lancia la sfida può proporre un nome. Quando il rivale accetta la sfida, il nome non è ancora deciso:
-- ognuno può accettare il nome proposto dall'altro oppure scrivere il proprio, finché uno dei due accetta.
-- Non cancella né cambia dati esistenti (le tabelle sono vuote). È sicuro rieseguirlo.

alter table derby_sfida add column if not exists nome_da text;

-- Lancia: ricorda chi ha proposto il nome e non permette una sfida tra due squadre che sono già un Derby
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
  if exists(select 1 from derby_sfida where ((da = p_team and a = p_rival) or (da = p_rival and a = p_team)) and stato = 'accettata' and nome_ok) then raise exception 'È già un Derby'; end if;
  if (select count(*) from derby_sfida where da = p_team and stagione = p_stagione) >= 2 then raise exception 'Hai usato le due sfide di questa stagione'; end if;
  insert into derby_sfida(stagione, da, a, frase, nome, nome_da) values(p_stagione, p_team, p_rival, p_frase, nm, case when nm is not null then p_team end) returning id into i;
  return i;
end $$;

-- Risposta alla sfida: accetta o rifiuta. Accettare NON chiude il nome: se si scrive un nome, resta una proposta da confermare.
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
    update derby_sfida set stato = 'accettata', risposta = now(), nome_ok = false,
      nome = coalesce(nm, nome), nome_da = case when nm is not null then p_team else nome_da end where id = p_id;
  elsif p_azione = 'rifiuta' then
    update derby_sfida set stato = 'rifiutata', risposta = now() where id = p_id;
  else
    raise exception 'Azione non valida';
  end if;
end $$;

-- Proposta o controproposta del nome (a sfida accettata): vale se l'ultima proposta non è tua
create or replace function derby_nome_proponi(p_team text, p_code text, p_id bigint, p_nome text)
returns void language plpgsql security definer set search_path=public as $$
declare r derby_sfida; nm text:=btrim(coalesce(p_nome,''));
begin
  perform curva_chk(p_team, p_code);
  if char_length(nm) not between 3 and 40 then raise exception 'Il nome deve avere da 3 a 40 caratteri'; end if;
  select * into r from derby_sfida where id = p_id and stato = 'accettata' and not nome_ok and (da = p_team or a = p_team);
  if not found then raise exception 'Sfida non trovata o nome già concordato'; end if;
  if r.nome_da = p_team then raise exception 'Hai già proposto un nome: aspetta la risposta'; end if;
  update derby_sfida set nome = nm, nome_da = p_team where id = p_id;
end $$;

-- Accetta il nome proposto dall'altra squadra: da qui il Derby è ufficiale
create or replace function derby_nome_accetta(p_team text, p_code text, p_id bigint)
returns void language plpgsql security definer set search_path=public as $$
declare r derby_sfida;
begin
  perform curva_chk(p_team, p_code);
  select * into r from derby_sfida where id = p_id and stato = 'accettata' and not nome_ok and (da = p_team or a = p_team);
  if not found then raise exception 'Sfida non trovata o nome già concordato'; end if;
  if r.nome is null then raise exception 'Nessun nome da accettare'; end if;
  if r.nome_da = p_team then raise exception 'Il nome lo hai proposto tu: deve accettarlo l''altra squadra'; end if;
  update derby_sfida set nome_ok = true where id = p_id;
end $$;

-- Lettura libera: ora ogni sfida dice anche chi ha proposto l'ultimo nome
create or replace function derby_stato(p_team text default null, p_code text default null)
returns json language plpgsql security definer set search_path=public as $$
declare ok boolean:=p_team is not null and curva_ok(p_team, p_code); res json;
begin
  perform derby_scadi();
  select json_build_object(
    'ok', ok,
    'sfide', coalesce((select json_agg(json_build_object('id',id,'stagione',stagione,'da',da,'a',a,'frase',frase,'nome',nome,'nome_da',nome_da,'nome_ok',nome_ok,'stato',stato,'ts',extract(epoch from creata)*1000,'risp',extract(epoch from risposta)*1000) order by creata desc)
      from (select * from derby_sfida order by creata desc limit 60) q), '[]'::json),
    'voti', coalesce((select json_agg(json_build_object('a',a,'b',b,'si',n_si,'no',n_no)) from
      (select a, b, count(*) filter (where si) n_si, count(*) filter (where not si) n_no from derby_voto group by a, b) v), '[]'::json),
    'miei', case when ok then coalesce((select json_agg(json_build_object('a',a,'b',b,'si',si)) from derby_voto where team = p_team), '[]'::json) else '[]'::json end,
    'conf', case when ok then coalesce((select json_agg(json_build_object('giornata',giornata,'risposte',risposte,'libera',libera,'promessa',promessa,'pesa',pesa,'esito',esito) order by giornata) from conf_risposta where team = p_team), '[]'::json) else '[]'::json end
  ) into res;
  return res;
end $$;
