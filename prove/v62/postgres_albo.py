"""Albo 6.2: prove SQL su PostgreSQL LOCALE, mai su Supabase."""
import json
import os
import sys
import time
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parents[2]
if os.environ.get("PGHOST") not in ("127.0.0.1", "localhost"):
    raise SystemExit("PGHOST deve essere esplicitamente locale")

NAME = "girrr62_albo_" + str(os.getpid()) + "_" + str(int(time.time()))
CONN = dict(
    host=os.environ["PGHOST"],
    port=int(os.environ.get("PGPORT", "5432")),
    user=os.environ.get("PGUSER", "postgres"),
    password=os.environ.get("PGPASSWORD", ""),
    dbname="postgres",
    autocommit=True,
)
sys.path.insert(0, str(ROOT / "prove"))
from prova_mvp60_db import SETUP

with psycopg.connect(**CONN) as admin:
    admin.execute("create database " + NAME)

CONN["dbname"] = NAME
verifiche = []


def check(nome, condizione):
    assert condizione, nome
    verifiche.append(nome)


def expect_error(conn, sql, params=()):
    try:
        conn.execute(sql, params)
    except psycopg.Error:
        return True
    return False


try:
    with psycopg.connect(**CONN) as c:
        c.execute(SETUP)
        c.execute(
            "create table public.curva_post(id bigint primary key,created timestamptz,body text);"
            "create table public.curva_poll(post_id bigint primary key,opts text[]);"
            "create table public.curva_vote(post_id bigint,team text,opt integer,primary key(post_id,team));"
            "create table public.conf_risposta(team text,giornata int,risposte jsonb,libera text,promessa text,pesa int,esito text,primary key(team,giornata));"
            "create table public.conf_dopo(team text,giornata int,risposta jsonb,creata timestamptz default now(),primary key(team,giornata));"
        )
        for f in (
            "sondaggio-curva.sql",
            "mvp-tifosi-60.sql",
            "votazioni-62-proposta.sql",
            "finestre-62-proposta.sql",
            "albo-62-proposta.sql",
        ):
            c.execute((ROOT / "sql" / f).read_text(encoding="utf-8"))
        c.execute((ROOT / "sql" / "albo-62-proposta.sql").read_text(encoding="utf-8"))
        check("SQL dell'Albo ripetibile", True)

        def v(q, p=()):
            return c.execute(q, p).fetchone()[0]

        a = v("select public.v62_albo('2026/27')")
        check("Senza giornate complete, partite null e nessun MVP inventato",
              a["partite"] is None and a["mvp"] == [] and a["mvp_classifica"] == []
              and not a["stagione_conclusa"])

        a_opzione = "Grodah – stif dc"
        b_opzione = "Oranje VC – WOA"
        opzioni = json.dumps([a_opzione, b_opzione], ensure_ascii=False)
        c.execute(
            "select public.v62_prepara('sfida:2026/27:8','2026/27','sfida','8',8,'Quale sfida seguire?',%s,"
            "clock_timestamp()-interval '1 hour',clock_timestamp()+interval '1 day')",
            (opzioni,),
        )
        check("Sondaggio aperto senza giuria non produce zero fittizi",
              v("select public.v62_albo('2026/27')->'partite'") is None)
        giuria = [
            {"tipo": "redazione", "autore": "Redazione", "scelta": a_opzione,
             "motivo": "Vera sfida al vertice."},
            {"tipo": "personaggio", "autore": "Nonno Cesare", "scelta": a_opzione,
             "motivo": "Mi interessa lo scontro al vertice."},
            {"tipo": "personaggio", "autore": "Statistico", "scelta": b_opzione,
             "motivo": "Sono numeri da seguire."},
        ]
        dossier = json.dumps(giuria, ensure_ascii=False)
        check("Dossier di giuria senza opzioni vere rifiutato",
              expect_error(c, "select public.v62_giuria_sfide_prepara('2026/27',8,%s)",
                  (json.dumps([dict(giuria[0], scelta="Non esiste"), *giuria[1:]], ensure_ascii=False),)))
        c.execute("select public.v62_giuria_sfide_prepara('2026/27',8,%s)", (dossier,))
        c.execute("select public.v62_giuria_sfide_prepara('2026/27',8,%s)", (dossier,))
        check("Giuria ripetibile senza duplicazioni",
              v("select count(*) from votazioni62_private.giuria_sfide") == 3)
        check("Giuria pubblicata immutabile",
              expect_error(c, "select public.v62_giuria_sfide_prepara('2026/27',8,%s)",
                           (json.dumps([dict(giuria[0], scelta=b_opzione), *giuria[1:]], ensure_ascii=False),)))
        check("Giuria riservata al servizio",
              not v("select has_function_privilege('anon',"
                    "'public.v62_giuria_sfide_prepara(text,integer,jsonb)','execute')"))
        check("Albo leggibile da anon",
              v("select has_function_privilege('anon','public.v62_albo(text)','execute')"))
        check("Tabelle giuria con RLS",
              v("select relrowsecurity from pg_catalog.pg_class where oid="
                "'votazioni62_private.giuria_sfide'::regclass"))
        with psycopg.connect(**CONN) as anon:
            anon.execute("set role anon")
            check("Scritture giuria non eseguibili dal browser",
                  expect_error(anon, "select public.v62_giuria_sfide_prepara('2026/27',8,%s)", (dossier,)))
            check("Accesso diretto ai dati giuria negato",
                  expect_error(anon, "select * from votazioni62_private.giuria_sfide"))
        code = "codice-solo-del-test"
        c.execute("select public.v62_vota('sfida:2026/27:8','Oranje VC',%s,%s)", (code, a_opzione))
        c.execute("select public.v62_vota('sfida:2026/27:8','Apo team',%s,%s)", (code, a_opzione))
        c.execute("update votazioni62_private.sondaggi set chiude=clock_timestamp()-interval '1 minute' where giornata=8")
        a = v("select public.v62_albo('2026/27')")
        check("Voti contati senza doppioni e per opzione reale",
              a["partite"][0]["partita"] == a_opzione and
              a["partite"][0]["voti"] == {
                  "allenatori": 2, "redazione": 1, "personaggi": 1, "totale": 4
              } and a["partite"][1]["voti"]["totale"] == 1)
        check("Nessun inserimento retroattivo di giuria",
              expect_error(c, "select public.v62_giuria_sfide_prepara('2026/27',9,%s)", (dossier,)))
        check("Nessun dato allenatori di altra stagione attribuito",
              v("select public.v62_albo('2027/28')->'partite'") is None)

        red = '[{"autore":"Redazione","scelta":"stif dc","motivo":"Vittoria verificata."}]'
        pers = '[{"autore":"Statistico","scelta":"stif dc","motivo":"Vittoria verificata."}]'
        candidates = '[{"team":"stif dc"},{"team":"Oranje VC"}]'
        for day, team in ((7, "stif dc"), (6, "Oranje VC"), (5, "stif dc")):
            result = json.dumps([{"team": team, "total": 60}], ensure_ascii=False)
            c.execute(
                "insert into mvp_private.giornate(stagione,giornata,chiude,candidati,redazione,personaggi,firma,chiusa,risultato)"
                " values('2026/27',%s,clock_timestamp()-interval '1 day',%s,%s,%s,repeat('a',64),clock_timestamp(),%s)",
                (day, candidates, red, pers, result),
            )
        a = v("select public.v62_albo('2026/27')")
        check("MVP e classifica coerenti con verdetti chiusi",
              len(a["mvp"]) == 3 and a["mvp_classifica"][0] ==
              {"team": "stif dc", "mvp": 2, "giornate": [5, 7]})
        check("Fine stagione non dedotta automaticamente", a["stagione_conclusa"] is False)
        c.execute("select public.v62_albo_finalizza('2026/27',8)")
        c.execute("select public.v62_albo_finalizza('2026/27',8)")
        check("Finalizzazione esplicita e idempotente",
              v("select public.v62_albo('2026/27')->>'stagione_conclusa'") == "true")
        check("Non si cambia una stagione finalizzata",
              expect_error(c, "select public.v62_albo_finalizza('2026/27',7)"))
        check("La finalizzazione non è pubblica",
              not v("select has_function_privilege('anon',"
                    "'public.v62_albo_finalizza(text,integer)','execute')"))
finally:
    with psycopg.connect(**{**CONN, "dbname": "postgres"}) as admin:
        admin.execute("drop database if exists " + NAME + " with (force)")

print("\n".join(verifiche))
print(str(len(verifiche)) + " controlli Albo completati su PostgreSQL locale")
