-- PROPOSTA NON APPLICATA: finestre condivise per aperture future.
begin;
create table if not exists votazioni62_private.finestre(
 stagione text not null,tipo text not null check(tipo in ('vigilia','dopo')),
 giornata integer not null check(giornata between 1 and 60),aperto timestamptz not null,chiude timestamptz not null,
 check(chiude>aperto),primary key(stagione,tipo,giornata)
);
alter table votazioni62_private.finestre enable row level security;
revoke all on votazioni62_private.finestre from public,anon,authenticated;
create or replace function public.v62_finestre_prepara(p_stagione text,p_tipo text,p_giornata integer,p_aperto timestamptz,p_chiude timestamptz)
returns void language plpgsql security definer set search_path='' as $$
begin
 if p_tipo='dopo' and p_chiude is distinct from p_aperto+interval '48 hours' then raise exception 'Dopo partita: 48 ore dai risultati pubblicati'; end if;
 insert into votazioni62_private.finestre values(p_stagione,p_tipo,p_giornata,p_aperto,p_chiude) on conflict do nothing;
 -- Non riavviare la finestra e non ritoccare scadenze annunciate.
end $$;
create or replace function public.v62_finestre(p_stagione text)
returns jsonb language sql stable security definer set search_path='' as $$
 select jsonb_build_object('server_ora',clock_timestamp(),'prima_giornata',(select min(giornata) from votazioni62_private.finestre where stagione=p_stagione),
 'finestre',coalesce((select jsonb_agg(to_jsonb(f) order by giornata,tipo) from votazioni62_private.finestre f where stagione=p_stagione),'[]'::jsonb))
$$;
create or replace function votazioni62_private.controlla_conferenza()
returns trigger language plpgsql security definer set search_path='' as $$
declare f record; v_tipo text; prima integer;
begin
 v_tipo=case when tg_table_name='conf_dopo' then 'dopo' else 'vigilia' end;
 if tg_op='UPDATE' then
  if v_tipo='vigilia' and (to_jsonb(new)->'risposte',to_jsonb(new)->'libera',to_jsonb(new)->'promessa',to_jsonb(new)->'pesa') is distinct from (to_jsonb(old)->'risposte',to_jsonb(old)->'libera',to_jsonb(old)->'promessa',to_jsonb(old)->'pesa') then raise exception 'Conferenza già pubblicata: le parole restano quelle'; end if;
  return new;
 end if;
 select min(giornata) into prima from votazioni62_private.finestre;
 -- Le giornate precedenti all’attivazione conservano le regole già annunciate.
 if prima is not null and new.giornata<prima then return new; end if;
 select * into f from votazioni62_private.finestre where giornata=new.giornata and finestre.tipo=v_tipo order by stagione desc limit 1 for key share;
 if not found then raise exception 'Finestra non ancora disponibile'; end if;
 if clock_timestamp()<f.aperto or clock_timestamp()>=f.chiude then raise exception 'Conferenza fuori dalla finestra di partecipazione'; end if;
 return new;
end $$;
-- Tavole esistenti, non vengono ricreate o svuotate.
do $$ begin
 if not exists(select 1 from pg_trigger where tgname='conf_finestre62') then create trigger conf_finestre62 before insert or update on public.conf_risposta for each row execute function votazioni62_private.controlla_conferenza(); end if;
 if not exists(select 1 from pg_trigger where tgname='dopo_finestre62') then create trigger dopo_finestre62 before insert or update on public.conf_dopo for each row execute function votazioni62_private.controlla_conferenza(); end if;
end $$;
revoke all on function public.v62_finestre(text),public.v62_finestre_prepara(text,text,integer,timestamptz,timestamptz),votazioni62_private.controlla_conferenza() from public,anon,authenticated;
grant execute on function public.v62_finestre(text) to anon,authenticated,service_role;
grant execute on function public.v62_finestre_prepara(text,text,integer,timestamptz,timestamptz) to service_role;
commit;
