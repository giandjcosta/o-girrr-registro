"""Claude, 24 novembre 2026: prove di sql/scambi-66.sql (scambi nell'app, 6.6).
Solo PostgreSQL locale, mai Supabase: crea un database usa e getta con le tabelle minime della Curva, dei Derby e del Totogirrr.
Uso: sudo -u postgres python3 prove/v66/prova_scambi_sql.py   (oppure PGHOST=127.0.0.1 con un utente che può creare database)"""
import json, os, subprocess, sys, time
from pathlib import Path
R = Path(__file__).resolve().parents[2]
if os.environ.get('PGHOST') not in (None, '', '127.0.0.1', 'localhost'): raise SystemExit('PGHOST deve essere locale')
DB = 'girrr66_scambi_%d_%d' % (os.getpid(), int(time.time()))
def psql(sql, db=DB, ok=True):
    p = subprocess.run(['psql', '-X', '-q', '-t', '-A', '-v', 'ON_ERROR_STOP=1', '-d', db, '-c', sql], capture_output=True, text=True)
    if ok and p.returncode: raise SystemExit('ERRORE SQL: ' + p.stderr)
    return p
SETUP = r"""
do $$ begin if not exists (select 1 from pg_roles where rolname='anon') then create role anon; end if;
 if not exists (select 1 from pg_roles where rolname='authenticated') then create role authenticated; end if; end $$;
create extension if not exists pgcrypto;
create table curva_lock(team text primary key, h text);
create function curva_hash(t text) returns text language sql immutable as $$ select md5(t) $$;
create function curva_ok(p_team text, p_code text) returns boolean language sql stable security definer set search_path to 'public' as $$
 select exists(select 1 from curva_lock where team=p_team and h=curva_hash(p_team||'|'||upper(coalesce(p_code,'')))) $$;
create function curva_chk(p_team text, p_code text) returns void language plpgsql security definer set search_path to 'public' as $$
 begin if not curva_ok(p_team,p_code) then raise exception 'Codice non valido'; end if; end $$;
insert into curva_lock select t, md5(t||'|'||upper(c)) from (values ('Oranje VC','oo'),('Real Madrink','rr'),('The Blue brothers','bb'),('Apo team','aa')) v(t,c);
create table curva_post(id bigint primary key, team text, body text, created timestamptz default now());
create table curva_reply(id bigint primary key, k text, team text, body text, created timestamptz default now());
create table curva_react(k text, team text, kind text, created timestamptz default now());
create table curva_adm(id bigint primary key, h text, body text, quando timestamptz, created timestamptz default now());
create table derby_sfida(id bigint primary key, da text, a text, stato text, frase_testo text, nome text, creata timestamptz, risposta timestamptz);
create table toto_prestiti(id bigint primary key, creditore text, debitore text, importo numeric, stato text, attesa_di text, aggiornato timestamptz);
create table toto_movimenti(id bigint primary key, team text, tipo text, importo numeric, nota text, creato timestamptz);
create schema push_private; create schema notifiche_private;
create function push_private.menzione(t text) returns text language sql immutable as $$ select '@'||replace(lower(t),' ','_') $$;
create table notifiche_private.letture(team text primary key, letto_fino timestamptz, chiavi text[] default '{}', aggiornato timestamptz);
"""
ok = []
def check(l, x):
    if not x: raise SystemExit('FALLITA: ' + l)
    ok.append(l); print('ok ·', l)
def q(sql):  # prima riga, prima colonna, come JSON se serve
    out = psql(sql).stdout.strip()
    try: return json.loads(out)
    except Exception: return out
def err(sql):
    p = psql(sql, ok=False); return p.stderr if p.returncode else ''
subprocess.run(['psql', '-X', '-q', '-d', 'postgres', '-c', 'create database ' + DB], check=True)
try:
    psql(SETUP)
    psql((R / 'sql' / 'scambi-66.sql').read_text())
    check('Lo script si applica una seconda volta senza errori', psql((R / 'sql' / 'scambi-66.sql').read_text()).returncode == 0)
    nomi = json.dumps({'1': {'n': 'Baldanzi', 't': 'Roma', 'r': 'C'}, '2': {'n': 'Kean', 't': 'Fiorentina', 'r': 'A'},
                       '3': {'n': 'Colpani', 't': 'Fiorentina', 'r': 'C'}, '4': {'n': 'Adams', 't': 'Torino', 'r': 'A'}})
    P = "select public.scambio_proponi('%s','%s','%s',array[%s]::text[],array[%s]::text[],'%s')"
    check('Codice sbagliato: rifiutato', 'Codice non valido' in err(P % ('The Blue brothers', 'xx', 'Real Madrink', "'1','2'", "'3','4'", nomi)))
    check('Numero diverso di giocatori: rifiutato', 'stessi giocatori' in err(P % ('The Blue brothers', 'bb', 'Real Madrink', "'1','2'", "'3'", nomi)))
    check('Con sé stessi: rifiutato', 'Squadra non valida' in err(P % ('The Blue brothers', 'bb', 'The Blue brothers', "'1'", "'3'", nomi)))
    check('Squadra inesistente: rifiutata', 'Squadra non valida' in err(P % ('The Blue brothers', 'bb', 'Nessuno', "'1'", "'3'", nomi)))
    check('Giocatore ripetuto: rifiutato', 'due volte' in err(P % ('The Blue brothers', 'bb', 'Real Madrink', "'1','1'", "'3','4'", nomi)))
    check('Id non numerico: rifiutato', 'non valido' in err(P % ('The Blue brothers', 'bb', 'Real Madrink', "'x'", "'3'", nomi)))
    r = q(P % ('The Blue brothers', 'bb', 'Real Madrink', "'1','2'", "'3','4'", nomi))
    sid = r['id']; check('Scambio registrato in attesa', r['stato'] == 'attesa')
    check('Stesso giocatore in un altro scambio in attesa: rifiutato', 'già in uno scambio' in err(P % ('Apo team', 'aa', 'Real Madrink', "'9'", "'3'", nomi)))
    st = q("select public.scambio_stato()")
    check('Lettura pubblica senza codice: c\'è lo scambio, ok=false', st['ok'] is False and st['scambi'][0]['id'] == sid and st['scambi'][0]['nomi']['1']['n'] == 'Baldanzi')
    check('Lettura con codice sbagliato: ok=false, niente squadra', q("select public.scambio_stato('Apo team','zz')")['ok'] is False)
    R_ = "select public.scambio_rispondi('%s','%s',%d,'%s')"
    check('Chi l\'ha proposto non può confermarlo', 'un altro allenatore' in err(R_ % ('The Blue brothers', 'bb', sid, 'conferma')))
    check('Un testimone non può rifiutarlo', 'Può rifiutarlo solo' in err(R_ % ('Apo team', 'aa', sid, 'rifiuta')))
    check('Solo chi l\'ha proposto può annullarlo', 'Può annullarlo solo' in err(R_ % ('Real Madrink', 'rr', sid, 'annulla')))
    check('Azione sconosciuta: rifiutata', 'Azione non valida' in err(R_ % ('Real Madrink', 'rr', sid, 'boh')))
    # notifiche prima della conferma
    n_real = q("select public.notifiche_stato('Real Madrink','rr')")['eventi']
    check('Notifica diretta all\'altra squadra', any(e['titolo'] == 'The Blue brothers ti propone uno scambio' and e['testo'] == 'Ti offre Baldanzi e Kean in cambio di Colpani e Adams · Tocca a te confermare' for e in n_real))
    n_apo = q("select public.notifiche_stato('Apo team','aa')")['eventi']
    check('Notifica a tutti gli altri come testimoni', any(e['titolo'].startswith('Richiesta di scambio') and e['tipo'] == 'scambi' for e in n_apo))
    check('Chi propone non riceve la propria richiesta', not q("select public.notifiche_stato('The Blue brothers','bb')")['eventi'])
    pe = q("select json_agg(e) from push_private.eventi('Real Madrink', now()-interval '1 hour') e")
    check('Push: categoria «scambi» con link alla richiesta', pe and pe[0]['cat'] == 'scambi' and pe[0]['url'] == 'index.html?scambio=%d' % sid)
    check('Preferenze del telefono: «scambi» accettata', q("select push_private.pulisci_pref('{\"scambi\":false,\"x\":true}')") == {'scambi': False})
    # conferma del testimone: vale la prima
    r = q(R_ % ('Apo team', 'aa', sid, 'conferma'))
    check('Il testimone conferma', r['stato'] == 'confermato' and r['conferma'] == 'testimone')
    r = q(R_ % ('Real Madrink', 'rr', sid, 'conferma'))
    check('Vale la prima conferma: la seconda trova lo scambio già chiuso', r.get('gia') is True and r['confermato_da'] == 'Apo team')
    check('Dopo la conferma il rifiuto non cambia niente', q(R_ % ('Real Madrink', 'rr', sid, 'rifiuta')).get('gia') is True)
    n_blue = q("select public.notifiche_stato('The Blue brothers','bb')")['eventi']
    check('Notifica «Scambio ufficiale» a chi l\'aveva proposto', any(e['titolo'] == 'Scambio ufficiale: The Blue brothers e Real Madrink' for e in n_blue))
    check('Il testimone che ha confermato non riceve «Scambio ufficiale»', not any(e['titolo'].startswith('Scambio ufficiale') for e in q("select public.notifiche_stato('Apo team','aa')")['eventi']))
    # workflow: applicato
    check('Applicato: solo Oranje VC', 'Solo Oranje VC' in err("select public.scambio_srv_applicato('Apo team','aa',%d,'x')" % sid))
    psql("select public.scambio_srv_applicato('Oranje VC','oo',%d,'Applicato alle rose')" % sid)
    s0 = q("select public.scambio_stato()")['scambi'][0]
    check('Segnato come applicato', s0['applicato'] and s0['esito'] == 'Applicato alle rose' and s0['stato'] == 'confermato')
    # conferma di Gianluca (lega), rifiuto, annullamento, conferma da Leghe
    a = q(P % ('Real Madrink', 'rr', 'Apo team', "'11'", "'12'", '{}'))['id']
    check('Oranje VC conferma come Lega', q(R_ % ('Oranje VC', 'oo', a, 'conferma'))['conferma'] == 'lega')
    b = q(P % ('Real Madrink', 'rr', 'Apo team', "'13'", "'14'", '{}'))['id']
    check('L\'altra squadra rifiuta', q(R_ % ('Apo team', 'aa', b, 'rifiuta'))['stato'] == 'rifiutato')
    check('Notifica del rifiuto a chi l\'aveva proposto', any(e['titolo'] == 'Apo team ha rifiutato lo scambio' for e in q("select public.notifiche_stato('Real Madrink','rr')")['eventi']))
    c = q(P % ('Real Madrink', 'rr', 'Apo team', "'15'", "'16'", '{}'))['id']
    check('Chi l\'ha proposto annulla', q(R_ % ('Real Madrink', 'rr', c, 'annulla'))['stato'] == 'annullato')
    d = q(P % ('Real Madrink', 'rr', 'Apo team', "'17'", "'18'", '{}'))['id']
    check('Conferma da Leghe: solo Oranje VC', 'Solo Oranje VC' in err("select public.scambio_srv_leghe('Apo team','aa',%d)" % d))
    check('Conferma automatica da Leghe', q("select public.scambio_srv_leghe('Oranje VC','oo',%d)" % d)['conferma'] == 'leghe')
    psql("select public.scambio_srv_applicato('Oranje VC','oo',%d,'Rose diverse','non_valido')" % d)
    check('Il workflow può segnare uno scambio non valido', q("select public.scambio_stato()")['scambi'][0]['stato'] == 'non_valido')
    e = q(P % ('Real Madrink', 'rr', 'Apo team', "'19'", "'20'", '{}'))['id']
    psql("update scambi set creato = now() - interval '15 days' where id = %d" % e)
    check('Dopo 14 giorni senza conferma decade', [s for s in q("select public.scambio_stato()")['scambi'] if s['id'] == e][0]['stato'] == 'scaduto')
    nid = q("select public.scambio_proponi('Apo team','aa','Oranje VC',array['31']::text[],array['32']::text[],jsonb_build_object('31',jsonb_build_object('n',repeat('x',90)),'99',jsonb_build_object('n','Intruso')))")['id']
    sn = [s for s in q("select public.scambio_stato()")['scambi'] if s['id'] == nid][0]['nomi']
    check('Nomi lunghi tagliati a 40 caratteri, ignorati quelli fuori dallo scambio', len(sn['31']['n']) == 40 and '99' not in sn)
    check('Tabella non leggibile da anon', 'permission denied' in subprocess.run(['psql', '-X', '-d', DB, '-c', 'set role anon; select * from public.scambi'], capture_output=True, text=True).stderr)
    print('\nTutte le %d prove superate.' % len(ok))
finally:
    subprocess.run(['psql', '-X', '-q', '-d', 'postgres', '-c', 'drop database if exists ' + DB])
