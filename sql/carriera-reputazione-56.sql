-- Carriera: malus degli sponsor mancati (Gianluca, 2 novembre 2026, «vai» esplicito)
-- Un obiettivo di sponsor mancato vale −1 di reputazione per sempre, senza crediti e non riscattabile.
-- Lo registra il workflow dei premi (premi-giornata.yml) con carriera_registra_server, come i premi.
-- Migrazione: carriera_reputazione_56

alter table career_private.reward_events drop constraint reward_events_reputation_check;
alter table career_private.reward_events add constraint reward_events_reputation_check
  check (reputation in (-1,1,2,3));
alter table career_private.reward_events drop constraint reward_events_status_check;
alter table career_private.reward_events add constraint reward_events_status_check
  check (status in ('pending','claimed','malus'));
alter table career_private.reward_events add constraint reward_events_malus_check
  check ((reputation < 0) = (status = 'malus') and (reputation > 0 or (credits = 0 and kind = 'sponsor')));

create or replace function public.carriera_registra_server(p_season text, p_manager text, p_team text, p_objective text, p_sponsor text, p_kind text, p_rep integer, p_credits numeric, p_proof jsonb)
 returns text
 language plpgsql
 security definer
 set search_path to ''
as $function$
declare v_count integer;
begin
 if current_setting('request.jwt.claim.role',true) <> 'service_role' then
  raise exception 'Restricted service role';
 end if;
 if p_season<>'2026/27' or p_kind not in ('presidente','sponsor') or
   p_credits not in (0,50,75,100,125) or p_rep not in (-1,1,2,3) or
   (p_rep<0 and (p_credits<>0 or p_kind<>'sponsor')) or
   p_proof->>'source'<>'official_github_data_json' then
  raise exception 'Invalid verified reward';
 end if;
 insert into career_private.reward_events(season,manager_key,team,objective_key,sponsor,kind,reputation,credits,proof,status)
 values(p_season,p_manager,p_team,p_objective,p_sponsor,p_kind,p_rep,p_credits,p_proof,case when p_rep<0 then 'malus' else 'pending' end)
 on conflict do nothing;
 get diagnostics v_count=row_count;
 return case when v_count=1 then 'created' else 'duplicate' end;
end $function$;

-- carriera_riscatta resta com'era: riscatta solo lo stato 'pending', quindi un malus non si riscatta.
-- carriera_stato e carriera_reputazione_pubblica sommano già la colonna reputation (i malus contano −1).

-- PER TORNARE INDIETRO (solo se non ci sono righe con status 'malus'):
-- alter table career_private.reward_events drop constraint reward_events_malus_check;
-- alter table career_private.reward_events drop constraint reward_events_status_check;
-- alter table career_private.reward_events add constraint reward_events_status_check check (status in ('pending','claimed'));
-- alter table career_private.reward_events drop constraint reward_events_reputation_check;
-- alter table career_private.reward_events add constraint reward_events_reputation_check check (reputation >= 1 and reputation <= 3);
-- e ricreare carriera_registra_server con  p_rep not in (1,2,3)  e senza la colonna status nell'insert.
