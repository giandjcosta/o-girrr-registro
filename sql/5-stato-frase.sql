-- derby_stato restituisce anche il testo vero della frase scelta (frase_testo), come le altre colonne della sfida.
create or replace function public.derby_stato(p_team text default null, p_code text default null)
returns json
language plpgsql
security definer
set search_path to 'public'
as $function$
declare ok boolean:=p_team is not null and curva_ok(p_team, p_code); res json;
begin
  perform derby_scadi();
  select json_build_object(
    'ok', ok,
    'sfide', coalesce((select json_agg(json_build_object('id',id,'stagione',stagione,'da',da,'a',a,'frase',frase,'frase_testo',frase_testo,'nome',nome,'nome_da',nome_da,'nome_ok',nome_ok,'stato',stato,'ts',extract(epoch from creata)*1000,'risp',extract(epoch from risposta)*1000) order by creata desc)
      from (select * from derby_sfida order by creata desc limit 60) q), '[]'::json),
    'voti', coalesce((select json_agg(json_build_object('a',a,'b',b,'si',n_si,'no',n_no)) from
      (select a, b, count(*) filter (where si) n_si, count(*) filter (where not si) n_no from derby_voto group by a, b) v), '[]'::json),
    'miei', case when ok then coalesce((select json_agg(json_build_object('a',a,'b',b,'si',si)) from derby_voto where team = p_team), '[]'::json) else '[]'::json end,
    'conf', case when ok then coalesce((select json_agg(json_build_object('giornata',giornata,'risposte',risposte,'libera',libera,'promessa',promessa,'pesa',pesa,'esito',esito) order by giornata) from conf_risposta where team = p_team), '[]'::json) else '[]'::json end
  ) into res;
  return res;
end $function$;
