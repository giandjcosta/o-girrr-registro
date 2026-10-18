-- Conferenze stampa pubblicate dalle squadre, con le risposte: serve al post "Conferenza pre partita" della Curva.
-- Sola lettura, come conf_promesse (che restituisce solo le conferenze con una promessa e senza le risposte).
create or replace function public.conf_pubbliche()
returns json
language sql
stable
security definer
set search_path to 'public'
as $function$
  select coalesce(json_agg(json_build_object('team',team,'giornata',giornata,'risposte',risposte,'libera',libera,'promessa',promessa,'pesa',pesa) order by giornata desc, team), '[]'::json)
  from conf_risposta;
$function$;
grant execute on function public.conf_pubbliche() to anon, authenticated;
