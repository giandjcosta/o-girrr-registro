-- BOZZA. Non applicata a nessun database. Serve a ragionare sui dati prima di costruire.

create table leghe (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,            -- es. 'o-fant-a-girrr'
  nome text not null,
  stagione text not null,
  config jsonb not null default '{}',   -- colori, moduli attivi, regole
  creata_il timestamptz not null default now()
);

create table iscrizioni (
  lega_id uuid references leghe(id) on delete cascade,
  utente_id uuid references auth.users(id) on delete cascade,
  ruolo text not null check (ruolo in ('proprietario','allenatore','ospite')),
  squadra text,                         -- solo per gli allenatori
  primary key (lega_id, utente_id)
);

create table inviti (
  codice text primary key,
  lega_id uuid references leghe(id) on delete cascade,
  ruolo text not null default 'ospite',
  scade_il timestamptz
);

create table post (
  id bigint generated always as identity primary key,
  lega_id uuid references leghe(id) on delete cascade,
  autore text not null,                 -- account della lega o della squadra
  testo text not null check (char_length(testo) <= 500),
  creato_il timestamptz not null default now(),
  nascosto boolean not null default false
);

create table segnalazioni (
  id bigint generated always as identity primary key,
  post_id bigint references post(id) on delete cascade,
  da uuid references auth.users(id),
  motivo text,
  creata_il timestamptz not null default now()
);

-- Permessi (idea): chi è iscritto a una lega vede i suoi dati; la Curva globale mostra solo i post non nascosti.
alter table leghe enable row level security;
alter table iscrizioni enable row level security;
alter table post enable row level security;
-- create policy ... (da scrivere e testare in una fase dedicata)
