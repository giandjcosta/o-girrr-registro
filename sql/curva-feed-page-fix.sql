-- Fix overload curva_feed (errore PGRST203)
-- Dopo curva-feed-page.sql, PostgREST vede DUE funzioni e non sa quale usare
-- quando il client chiama senza p_limit/p_before.
-- Soluzione: resta solo la firma a 4 argomenti (con default).

drop function if exists public.curva_feed(text, text);

-- Assicura i grant sulla firma completa
grant execute on function public.curva_feed(text, text, int, double precision) to anon, authenticated;

notify pgrst, 'reload schema';
