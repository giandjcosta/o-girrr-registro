"""Scrive il copione della puntata: rubriche con condizioni, toni che cambiano, storie vere della lega."""
import json, random, pathlib
R = pathlib.Path(__file__).parent
def f(x):
    x = float(x); return str(int(x)) if x == int(x) else str(x).replace(".", ",")
NUM = ["zero","uno","due","tre","quattro","cinque","sei","sette","otto","nove","dieci"]
ORDM = {1:"primo",2:"secondo",3:"terzo",4:"quarto",5:"quinto",6:"sesto",7:"settimo",8:"ottavo",9:"nono",10:"decimo"}
ORD = {1:"prima",2:"seconda",3:"terza",4:"quarta",5:"quinta",6:"sesta",7:"settima",8:"ottava",9:"nona",10:"decima"}
# chi c'è dietro ogni squadra (da confermare) e come stava l'anno scorso (Gioberti Cup 2025/26)
CHI = {"Apo team":"Apo","WOA":"Ser","Grodah":"RikyArma","Real Madrink":"AndrewTT","stif dc":"Stifson","Mariana Coneja":"Mark Lenders",
       "The Blue brothers":"Mario e Leanzino","Atletico ma non troppo":"Riccardo","Oranje VC":"Dj Costa"}
ANNO_SCORSO = {"WOA":1,"Grodah":2,"stif dc":4,"Mariana Coneja":5,"Real Madrink":6,"Apo team":10}
STORIE = {
 "Apo team": ["Apo ha vinto due titoli di fila, nel 2021/22 e nel 2022/23, ed è l'unico ad esserci riuscito!", "Apo è passato da campione per due anni a ultimo per due anni di fila. Una montagna russa!"],
 "WOA": ["Ser in cinque stagioni non ha mai cambiato né squadra né nome: la WOA è una certezza!", "Ser l'anno scorso ha vinto la Gioberti Cup con dieci punti sul secondo!"],
 "Grodah": ["RikyArma, dall'ultimo posto del 2022/23 alla Coppa Campioni dell'anno scorso: roba da film!"],
 "stif dc": ["Stifson è arrivato nel 2024/25 ed è stato subito secondo, a tre punti dal campione!"],
 "Real Madrink": ["AndrewTT ha due podi in cinque anni, ma ancora nessun titolo. Sarà l'anno buono?"],
 "The Blue brothers": ["Mario ha cambiato nome quattro volte: Gingleton, Barny, Pep Mariola e adesso Mario!", "Leanzino ha vinto il titolo 2023/24 per appena due punti, e adesso gioca in coppia con Mario!"],
 "Atletico ma non troppo": ["Riccardo è sparito per due stagioni ed è tornato con l'Atletico Ma Non Troppo!"],
 "Oranje VC": ["Dj Costa è tornato dopo quattro stagioni di assenza!"],
 "Mariana Coneja": ["Mark Lenders l'anno scorso ha chiuso quinto. Quest'anno vuole di più!"],
}
CURVA = ["Chissà cosa staranno scrivendo in Curva i tifosi {t}!", "In Curva, stasera, i tifosi {t} non dormono!", "Diamo un'occhiata alla Curva: i tifosi {t} sono già al lavoro!", "Chissà in Curva cosa ne pensano i tifosi {t}!"]
CONF = ["Chi non crede in noi può restare a casa.", "Siamo pronti, ci vediamo in campo.", "Non siamo qui per fare i turisti.", "Quest'anno non ci ferma nessuno.", "Un punto alla volta, ma tutti insieme."]
def build(D, rng, mercato, nomi=None):
    nomi = nomi or {}
    b1 = nomi.get('B', 'Beppe Rovesciata'); g1 = nomi.get('G', 'Steve Offside'); g0 = g1.split()[0]; b0 = b1.split()[0]
    a = D["aw"][-1]; T = D["tab"]; P = D["prob"]; n = a["n"]
    row = {r["t"]: r for r in T}
    def pick(x): return rng.choice(x)
    def curva(t): return pick(CURVA).format(t="di " + t)
    def pct(x): return f(round(x))
    L = []
    def add(k, t, st=None): L.append((k, t, st))
    # --- apertura alla Caressa e Bergomi: la frase passa da una voce all'altra
    add("B", f"Buongiorno, buonasera e buonanotte a tutti, siete su Radio Girrr! Oggi siamo qui con {b1}", "urlo")
    add("G", f"e {g1}! Si parte!", "urlo")
    add("B", f"Giornata numero {n}! {g0}, hai già guardato i punteggi?")
    add("G", pick(["Guardati, riguardati e ho pure fatto una scommessa con me stesso. Ho perso.", "Sì, con una tazza di tè in mano, come ogni buon britannico. E mi sono rovinato la colazione.", "Altro che guardati: li ho imparati a memoria!"]))
    # --- punteggi estremi: a volte si esalta, a volte si prende in giro
    tono = pick(["esalta", "sfotte"])
    mv, fl, mz = a["mvp"], a["flop"], a["maz"]
    if tono == "esalta":
        add("B", f"Il re della giornata è {mv[0]}! {f(mv[1])} punti! Che prestazione!", "urlo")
        add("G", f"{f(mv[1])} punti! {curva(mv[0])}")
    else:
        add("B", f"Il re della giornata è {mv[0]}, con {f(mv[1])} punti.")
        add("G", f"Bravi, eh. Però il vero esame è la prossima settimana. {curva(mv[0])}")
    if rng.random() < 0.6:
        add("B", f"Dall'altra parte, il flop: {fl[0]} si ferma a {f(fl[1])} punti.")
        add("G", pick([f"Coraggio, {fl[0]}! Si cade, ci si rialza!", f"{f(fl[1])}. Non infierisco. {curva(fl[0])}", "Qui ci vuole un abbraccio. Sottovoce, eh."]), "sus" if rng.random() < 0.4 else None)
    if mz[2] >= 8:
        add("B", f"E la sconfitta più pesante è quella di {mz[0]}, battuta da {mz[3]} con {f(mz[2])} punti di scarto! Una mazzata!")
        if rng.random() < 0.6: add("G", pick(["Ahia!", "Questa ha fatto male anche a noi!", "Altro che mazzata: una cassa di birra in testa!"]), "urlo")
    # --- classifica: primi tre, e ogni tanto l'ultimo
    t1, t2, t3 = T[0], T[1], T[2]
    add("B", f"In classifica comanda {t1['t']} con {t1['pts']} punti! Seguono {t2['t']} e {t3['t']}.")
    ns = ANNO_SCORSO.get(t1["t"])
    if ns and ns >= 8: add("G", f"E pensare che l'anno scorso {t1['t']} era {ORD[ns]}. Qui c'è una rinascita!", "urlo")
    elif t1["t"] in STORIE: add("G", pick(STORIE[t1["t"]]))
    last = T[-1]
    if rng.random() < 0.5 or (last["v"] == 0 and last["g"] >= 3):
        add("B", f"In fondo c'è {last['t']}. Può risalire e sperare di uscire dall'ultima posizione?")
        add("G", pick(["Io dico di sì. Poi però bisogna scrivere la formazione!", "La speranza è l'ultima a morire. Come l'ultimo in classifica!", "Una vittoria e si cambia musica!"]))
    # --- percentuali solo nei momenti buoni
    gap = t1["pts"] - t2["pts"]
    quarto = T[3]["pts"] if len(T) > 3 else None
    metà = n in (18, 19, 20)
    if gap >= 9:
        add("B", f"{t1['t']} ha {gap} punti sul secondo! Secondo i nostri calcoli ha il {pct(P[t1['t']]['s'][-1])} per cento di vincere lo scudetto!", "urlo")
    elif len(T) > 3 and T[2]["pts"] - T[3]["pts"] >= 9:
        add("B", f"{t3['t']} ha {T[2]['pts'] - T[3]['pts']} punti sul quarto: il podio sembra già quasi chiuso!")
    elif metà:
        fav = max(P, key=lambda t: P[t]["s"][-1])
        add("B", f"A metà campionato il nostro modello dice che il favorito è {fav}, con il {pct(P[fav]['s'][-1])} per cento di scudetto!")
    elif last["v"] == 0 and last["g"] >= 3:
        add("G", f"{last['t']} non vince da {last['g']} partite. Il nostro modello la dà ultima nel {pct(P[last['t']]['u'][-1])} per cento dei casi!")
    # --- presidente
    EXP = {"Oranje VC":4,"Apo team":5,"Grodah":3,"WOA":2,"Real Madrink":3,"stif dc":6,"Mariana Coneja":6,"AFA SELECCION":4,"The Blue brothers":7,"Atletico ma non troppo":8}
    def fid(t): r = row[t]; return max(5, min(98, round(50 + (EXP.get(t, 5) - r["pos"]) * 6 + r["v"] * 8 - r["p"] * 8)))
    basso = min(row, key=fid); alto = max(row, key=fid)
    if fid(basso) <= 30 and rng.random() < 0.7:
        add("B", f"Il presidente di {basso} non è molto contento ultimamente!")
        add("G", "Se continua così si parla di esonero. Sottovoce, eh." if fid(basso) <= 15 else "Servono risultati, e anche in fretta.", "sus")
    elif fid(alto) >= 85 and rng.random() < 0.5:
        add("B", f"Il presidente di {alto} è al settimo cielo!")
        add("G", "Con questi punti ci credo. Contratto a vita!")
    # --- storie degli allenatori, una o due a puntata
    teams_in = [mv[0], fl[0]]
    pool = [t for t in teams_in if t in STORIE and (t != t1["t"])]
    if pool and rng.random() < 0.8:
        t = pick(pool); add("G", pick(STORIE[t]))
    # --- inviata
    add("B", "Ora ci colleghiamo con la nostra inviata sul campo! Giulia, a te!", "urlo")
    sup = max(((r["t"], EXP.get(r["t"], 5), r["pos"]) for r in T), key=lambda x: x[1] - x[2])
    add("S", f"Grazie {b0}! Qui è un bel caos! Prima notizia: {sup[0]} sta superando le aspettative! Il presidente la voleva intorno al {ORDM.get(sup[1], str(sup[1]))} posto, e invece oggi è {ORD.get(sup[2], str(sup[2])+'ª')}!", "urlo")
    g = D["cal"][0]["m"]; conf = next(((m[0], m[1]) for m in g if "Oranje VC" in m), (g[0][0], g[0][1]))
    add("S", f"Dalla sala stampa, alla vigilia di {conf[0]} contro {conf[1]}, l'allenatore dice: «{pick(CONF)}» Per ora è tutto, restituisco la linea in studio!")
    add("G", pick(["Grazie Giulia! Un allenatore, una frase e mezza lega è già in fermento.", "Grazie Giulia! Questo è calcio!", "Grazie Giulia, collegamento da Oscar!"]))
    # --- coppa: storie vere, nessun giro di parole
    cup = D["cup"][-1] if D.get("cup") else None
    if cup:
        add("B", f"Passiamo alla Champions Cup, la coppa della nostra lega! Si è chiusa la giornata {cup['n']}!", "urlo")
        for i, m in enumerate(sorted(cup["m"], key=lambda m: -abs(m[2]-m[3]))[:2]):
            x, y = m[1], m[4]; ga, gb = (int(z) for z in m[5].split("-"))
            if ga == gb: fr = f"{x} e {y} si dividono la posta: finisce {NUM[ga]} a {NUM[gb]}."
            else:
                w, l, gw, gl = (x, y, ga, gb) if ga > gb else (y, x, gb, ga)
                fr = f"Vittoria di {w} contro {l}: {NUM[gw]} a {NUM[gl]}."
            add("B" if i == 0 else "G", fr)
            if l == "Grodah" if ga != gb else False: add("G", "Cade la campionessa in carica! L'anno scorso la Coppa Campioni era sua!", "urlo")
    # --- derby
    DER = [("Grodah","WOA"),("stif dc","Real Madrink"),("Oranje VC","AFA SELECCION"),("Apo team","The Blue brothers"),("Mariana Coneja","Atletico ma non troppo")]
    der = next((m for m in g if any({x.lower(), y.lower()} == {m[0].lower(), m[1].lower()} for x, y in DER)), None)
    if der: add("B", f"Alla prossima giornata c'è il derby: {der[0]} contro {der[1]}!", "urlo")
    # --- mercato: Ciro c'è solo se ci sono notizie
    notizie = (mercato or {}).get("notizie") or []
    if notizie:
        add("B", "E adesso il mercato! Abbiamo notizie, e per commentarle chiamiamo Ciro Trattativa!", "urlo")
        add("C", "Buongiorno a tutti, qui Ciro Trattativa. Lo dirò sottovoce: notizie fresche dal mercato!", "sus")
        for z in notizie[:3]:
            pref = "Ufficiale!" if z["tipo"] == "ufficiale" else "Semi ufficiale: prendetelo con le pinze!"
            add("C", f"{pref} {z['testo'][0].upper() + z['testo'][1:]}.")
        add("G", "Ciro, come sempre, sicurissimo! Al cento per cento.")
    # --- chiusura
    add("B", "Per Radio Girrr è tutto! Mettete la formazione, vi vogliamo bene!", "urlo")
    add("G", "Ci sentiamo mercoledì prossimo! Ciao a tutti!", "urlo")
    return L
