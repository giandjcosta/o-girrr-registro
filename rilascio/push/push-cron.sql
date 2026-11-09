-- Notifiche push: giro ogni 5 minuti (dopo il deploy della funzione push-invia)
-- Giro ogni 5 minuti
select cron.unschedule('push-giro') where exists (select 1 from cron.job where jobname = 'push-giro');
select cron.schedule('push-giro', '*/5 * * * *', $c$
  select net.http_post(
    url := 'https://qmjqfgmvimsuxvghetgi.supabase.co/functions/v1/push-invia',
    headers := jsonb_build_object('Content-Type', 'application/json', 'x-girrr-cron', (select cron_token from push_private.cfg where id = 1)),
    body := '{"giro":true}'::jsonb,
    timeout_milliseconds := 30000)
$c$);
