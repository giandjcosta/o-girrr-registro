// O Girrr · Invio delle notifiche push (Claude, 9 novembre 2026).
// Edge Function «push-invia» su Supabase. Tre usi:
//   {chiave:true}                       -> chiave pubblica per iscriversi (la crea al primo uso)
//   {prova:true, team, code, endpoint}  -> notifica di prova a quel telefono (una al minuto)
//   {giro:true} + intestazione x-girrr-cron -> giro programmato ogni 5 minuti (pg_cron)
// Le chiavi di firma e il gettone del giro stanno nello schema privato push_private: nessun segreto nel codice.
import webpush from "npm:web-push@3.6.7";

const DB = Deno.env.get("SUPABASE_URL")!;
const SR = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const SITO = "https://giandjcosta.github.io/o-fant-a-girrr/";
const LEGHE = "https://leghe.fantacalcio.it/";
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type, apikey, authorization, x-client-info",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const ORA = 3600_000, MIN = 60_000;
const GIORNI: Record<string, string> = { lun: "lunedì", mar: "martedì", mer: "mercoledì", gio: "giovedì", ven: "venerdì", sab: "sabato", dom: "domenica" };

type Evento = { chiave: string; cat: string; titolo: string; testo: string; url: string; quando: string; generale?: boolean; perSquadra?: (t: string) => { titolo: string; testo: string } | null };

function risposta(o: unknown, stato = 200) {
  return new Response(JSON.stringify(o), { status: stato, headers: { ...CORS, "Content-Type": "application/json" } });
}
async function rpc(nome: string, corpo: Record<string, unknown> = {}) {
  const r = await fetch(`${DB}/rest/v1/rpc/${nome}`, {
    method: "POST",
    headers: { apikey: SR, Authorization: `Bearer ${SR}`, "Content-Type": "application/json" },
    body: JSON.stringify(corpo),
  });
  const t = await r.text();
  if (!r.ok) throw new Error(`${nome}: ${r.status} ${t.slice(0, 200)}`);
  return t ? JSON.parse(t) : null;
}
async function json(u: string) {
  try { const r = await fetch(u + "?t=" + Date.now(), { headers: { "Cache-Control": "no-cache" } }); return r.ok ? await r.json() : null; } catch { return null; }
}

// ---------- Ora italiana ----------
function offsetRoma(ms: number) {
  const p = new Intl.DateTimeFormat("en-US", { timeZone: "Europe/Rome", timeZoneName: "shortOffset" }).formatToParts(new Date(ms));
  const m = /GMT([+-]\d+)/.exec(p.find((x) => x.type === "timeZoneName")?.value || "");
  return m ? +m[1] : 1;
}
function daRoma(y: number, mo: number, d: number, h: number, mi: number) {
  const t = Date.UTC(y, mo - 1, d, h, mi);
  return t - offsetRoma(t) * ORA;
}
function hmRoma(ms: number) {
  const d = new Date(ms + offsetRoma(ms) * ORA);
  return { h: d.getUTCHours(), m: d.getUTCMinutes(), testo: String(d.getUTCHours()).padStart(2, "0") + ":" + String(d.getUTCMinutes()).padStart(2, "0") };
}
/** Di notte (23:00-7:30) si tiene tutto per la mattina, tranne la formazione */
export function notte(ms: number) { const { h, m } = hmRoma(ms); return h >= 23 || h < 7 || (h === 7 && m < 30); }

// ---------- Eventi della lega, uguali per tutti (dati pubblici del sito) ----------
// deno-lint-ignore no-explicit-any
export function eventiGenerali(d: any, indice: any[] | null, ora: number): Evento[] {
  const ev: Evento[] = [];
  if (d) {
    // Formazione: la giornata comincia con la prima partita di Serie A della prossima giornata (fx[nx], ora italiana)
    const nx = d.nx, fx = (d.fx || {})[nx] || [];
    const base = new Date(d.cal?.date || d.updated || ora);
    let primo: { t: number; casa: string; ospite: string; g: string } | null = null;
    for (const [casa, ospite, quando] of fx) {
      const m = /(\w+)\s+(\d{1,2})\/(\d{1,2})\s+(\d{1,2}):(\d{2})/.exec(String(quando || ""));
      if (!m) continue;
      let y = base.getUTCFullYear();
      if (+m[3] < base.getUTCMonth() + 1 - 6) y++;
      const t = daRoma(y, +m[3], +m[2], +m[4], +m[5]);
      if (!primo || t < primo.t) primo = { t, casa, ospite, g: GIORNI[m[1].toLowerCase()] || m[1] };
    }
    if (primo) {
      const resta = primo.t - ora;
      const gir = (d.cal?.lega || []).find((g: { sa: number }) => g.sa === nx);
      const art = (n: number) => (n === 8 || n === 11 || String(n).startsWith("8") ? "L'" : "La ");
      const nome = gir ? `${art(gir.n)}${gir.n}ª giornata` : `${art(nx)}${nx}ª giornata di Serie A`;
      const testo = `${nome} comincia ${primo.g} alle ${hmRoma(primo.t).testo} con ${primo.casa}–${primo.ospite}. Schiera la formazione su Leghe.`;
      const quando = new Date(ora).toISOString();
      if (resta > 0 && resta <= 60 * MIN + 2 * MIN) {
        const min = Math.max(5, Math.round(resta / MIN / 5) * 5);
        ev.push({ chiave: `form1-${nx}`, cat: "formazione", titolo: `Formazione: ${min >= 60 ? "manca 1 ora" : "mancano " + min + " minuti"}`, testo, url: LEGHE, quando, generale: true });
      } else if (resta > 62 * MIN && resta <= 3 * ORA + 2 * MIN) {
        const h = Math.round(resta / ORA);
        ev.push({ chiave: `form3-${nx}`, cat: "formazione", titolo: `Formazione: mancano ${h} ${h === 1 ? "ora" : "ore"}`, testo, url: LEGHE, quando, generale: true });
      }
    }
    // Risultati: escono un'ora dopo il più tardivo fra voti completi e calcolo su Leghe (come pub.js del sito)
    const V = d.votiTs || {}, C = d.calcTs || {};
    for (const g of d.cal?.lega || []) {
      const v = V[g.sa], c = C[g.sa];
      if (!v && !c) continue;
      const pub = Math.max(v ? Date.parse(v) : 0, c ? Date.parse(c) : 0) + ORA;
      if (ora < pub || ora - pub > 12 * ORA) continue;
      const coppa = (d.cal?.cup || []).find((x: { sa: number }) => x.sa === g.sa);
      ev.push({
        chiave: `ris-${g.sa}`, cat: "risultati", titolo: `Risultati della ${g.n}ª giornata`,
        testo: "Risultati e classifica sono online.", url: "apri.html?p=tabellone", quando: new Date(pub).toISOString(), generale: true,
        perSquadra: (t: string) => {
          const righe: string[] = [];
          const m = (g.m || []).find((x: unknown[]) => x[0] === t || x[3] === t);
          const k = coppa && (coppa.m || []).find((x: unknown[]) => x[1] === t || x[4] === t);
          const uguale = m && k && m[0] === k[1] && m[3] === k[4] && m[4] === k[5];
          if (m) righe.push(`${uguale ? "Campionato e Champions Cup" : "Campionato"}: ${m[0]}–${m[3]} ${m[4]}`);
          if (k && !uguale) righe.push(`Champions Cup: ${k[1]}–${k[4]} ${k[5]}`);
          return righe.length ? { titolo: `Risultati della ${g.n}ª giornata`, testo: righe.join(" · ") } : null;
        },
      });
    }
  }
  // Giornale: all'ora di uscita del numero
  for (const x of indice || []) {
    const pub = x && x.pub ? Date.parse(x.pub) : NaN;
    if (!(pub <= ora) || ora - pub > 12 * ORA) continue;
    ev.push({ chiave: `gio-${x.n}`, cat: "giornale", titolo: `È uscito il Giornale n° ${x.n}`, testo: String(x.titolone || "").slice(0, 160), url: "apri.html?p=giornale", quando: new Date(pub).toISOString(), generale: true });
  }
  return ev;
}

// ---------- Invio ----------
async function chiavi() {
  let c = await rpc("push_srv_cfg");
  if (!c?.pub) {
    const k = webpush.generateVAPIDKeys();
    await rpc("push_srv_chiavi", { p_pub: k.publicKey, p_priv: k.privateKey });
    c = await rpc("push_srv_cfg");
  }
  webpush.setVapidDetails(SITO, c.pub, c.priv);
  return c;
}
// Nomi mostrati (Claude, 9 novembre 2026, 5.6.2): la chiave resta «The Blue brothers», nelle notifiche si legge il nome ufficiale. Stessa tabella di nomi.js.
const NOMI: [string, string][] = [["Blue brothers", "Blues Brothers"], ["Blue Brothers", "Blues Brothers"], ["BLUE BROTHERS", "BLUES BROTHERS"], ["blue brothers", "blues brothers"]];
const nomeMostrato = (s: string) => NOMI.reduce((x, [a, b]) => x.split(a).join(b), String(s || ""));
// deno-lint-ignore no-explicit-any
async function manda(s: any, dati: { titolo: string; testo: string; url: string; tag: string }, ttl: number, urgente: boolean) {
  try {
    dati = { ...dati, titolo: nomeMostrato(dati.titolo), testo: nomeMostrato(dati.testo) };
    await webpush.sendNotification({ endpoint: s.endpoint, keys: { p256dh: s.p256dh, auth: s.auth } }, JSON.stringify(dati), { TTL: ttl, urgency: urgente ? "high" : "normal" });
    return "ok";
  } catch (e) {
    const st = (e as { statusCode?: number }).statusCode;
    return st === 404 || st === 410 ? "scaduta" : "errore " + (st || (e as Error).message);
  }
}

async function giro() {
  const ora = Date.now();
  const [iscr, d, indice] = await Promise.all([rpc("push_srv_giro"), json(SITO + "data.json"), json(SITO + "riepiloghi/indice.json")]);
  const generali = eventiGenerali(d, indice, ora);
  const zitto = notte(ora);
  const inviate: { chiave: string; id: number }[] = [], scadute: number[] = [];
  let mandate = 0, errori = 0;
  for (const s of iscr || []) {
    const pref = s.pref || {}, gia = new Set<string>(s.inviate || []);
    const tutti: Evento[] = [...generali, ...(s.eventi || [])];
    let qui = 0;
    for (const e of tutti) {
      if (qui >= 4) break; // non più di 4 notifiche per telefono a giro: le altre al giro dopo
      if (gia.has(e.chiave)) continue;
      const voluto = e.cat === "applausi" ? pref.applausi === true : pref[e.cat] !== false;
      if (!voluto) continue;
      if (zitto && e.cat !== "formazione") continue;
      // Uscite di prima dell'iscrizione: non si mandano (tranne la formazione, che guarda avanti)
      if (e.generale && e.cat !== "formazione" && Date.parse(e.quando) < Date.parse(s.creata)) { inviate.push({ chiave: e.chiave, id: s.id }); continue; }
      const p = e.perSquadra ? e.perSquadra(s.team) : null;
      const esito = await manda(s, { titolo: p?.titolo || e.titolo, testo: p?.testo || e.testo, url: e.url, tag: e.chiave }, e.cat === "formazione" ? ORA : 12 * ORA, e.cat === "formazione");
      if (esito === "scaduta") { scadute.push(s.id); break; }
      if (esito === "ok") { inviate.push({ chiave: e.chiave, id: s.id }); mandate++; qui++; } else errori++;
    }
  }
  if (inviate.length || scadute.length) await rpc("push_srv_segna", { p_inviate: inviate, p_scadute: scadute });
  return { iscrizioni: (iscr || []).length, generali: generali.map((e) => e.chiave), mandate, errori, scadute: scadute.length, notte: zitto };
}

if (import.meta.main !== false) Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return risposta({ errore: "Solo POST" }, 405);
  // deno-lint-ignore no-explicit-any
  let b: any = {};
  try { b = await req.json(); } catch { /* corpo vuoto */ }
  try {
    const c = await chiavi();
    if (b.chiave) return risposta({ pub: c.pub });
    if (b.prova) {
      const s = await rpc("push_srv_prova", { p_team: String(b.team || ""), p_code: String(b.code || ""), p_endpoint: String(b.endpoint || "") });
      if (!s) return risposta({ errore: "Telefono non iscritto o codice non valido" }, 403);
      if (s.troppe) return risposta({ errore: "Aspetta un minuto prima di un'altra prova" }, 429);
      const esito = await manda(s, { titolo: "O Girrr", testo: "Le notifiche funzionano: da ora gli avvisi arrivano qui.", url: "apri.html?p=notifiche", tag: "prova" }, 600, true);
      if (esito === "scaduta") await rpc("push_srv_segna", { p_inviate: [], p_scadute: [s.id] });
      return risposta({ esito });
    }
    if (b.giro) {
      if (!c.token || req.headers.get("x-girrr-cron") !== c.token) return risposta({ errore: "Non autorizzato" }, 401);
      return risposta(await giro());
    }
    return risposta({ errore: "Richiesta sconosciuta" }, 400);
  } catch (e) {
    console.error(e);
    return risposta({ errore: "Errore interno" }, 500);
  }
});
