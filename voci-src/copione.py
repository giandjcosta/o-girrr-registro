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
       "The Blue brothers":"Mario e Leanzino","Atletico ma non troppo":"Riccardo","Oranje VC":"Dj Costa","AFA SELECCION":"Maria"}
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
RIDE = ["Ah ah ah, scusate, non ce la faccio!", "Ah ah ah, questa me la segno!", "Ah ah, ma dai!"]
SOSP = ["Eh... che dolore.", "Mamma mia... poveretto.", "Eh... purtroppo il calcio è anche questo."]
STUP = ["Ma davvero?!", "Non ci credo!", "Cosa?! Ma com'è possibile?!"]
COMM = ["Ragazzi, mi emoziono ancora.", "Il calcio è anche questo: i ritorni.", "Non è solo una classifica, è la nostra storia."]
CURVA = ["Chissà cosa staranno scrivendo in Curva i tifosi {t}!", "In Curva, stasera, i tifosi {t} non dormono!", "Diamo un'occhiata alla Curva: i tifosi {t} sono già al lavoro!", "Chissà in Curva cosa ne pensano i tifosi {t}!"]
CONF = ["Chi non crede in noi può restare a casa.", "Siamo pronti, ci vediamo in campo.", "Non siamo qui per fare i turisti.", "Quest'anno non ci ferma nessuno.", "Un punto alla volta, ma tutti insieme."]
# --- numeri del campionato: attacco, difesa e differenza reti dalla classifica vera (gf/gs di ogni squadra)
def numeri(T, n, rng):
    """Una o due curiosità sui gol, solo dalla 3ª giornata (prima i numeri dicono poco). Restituisce battute (voce, testo, tono)."""
    if n < 3 or not T or "gf" not in T[0]: return []
    def capo(k, rev=False):   # chi guida la statistica; None se a pari merito sono più di due
        v = (min if rev else max)(r[k] for r in T); c = [r["t"] for r in T if r[k] == v]
        return (" e ".join(c), v, len(c) > 1) if len(c) <= 2 else None
    for r in T: r["_dr"] = r["gf"] - r["gs"]
    fatti = []
    a = capo("gf")
    if a: fatti.append([("B", f"Il miglior attacco è quello di {a[0]}: {a[1]} gol fatti in {n} giornate{', a pari merito' if a[2] else ''}!", "urlo"),
                        ("G", rng.choice(["Davanti fanno paura!", "Quando partono non li fermi più!", "Altro che catenaccio!"]), None)])
    d = capo("gs", True)
    if d: fatti.append([("B", f"La difesa meno battuta è quella di {d[0]}: solo {d[1]} gol subiti{', a pari merito' if d[2] else ''}.", None),
                        ("G", rng.choice(["Lì dietro non passa nessuno!", "Un muro, signori!", "Le partite si vincono anche così."]), None)])
    w = capo("gs")
    if w and w[1] >= 2 * n: fatti.append([("G", f"E poi c'è la difesa di {w[0]}: {w[1]} gol presi. Qualcuno chiuda la porta!", "sarcasmo")])
    t1 = T[0]
    if a and t1["t"] not in a[0].split(" e ") and t1["gf"] < a[1]:
        fatti.append([("B", f"Curiosità: {t1['t']} comanda la classifica, ma non ha il miglior attacco. Vince con la testa!", None)])
    dr = capo("_dr")
    if dr and dr[1] >= 4: fatti.append([("B", f"La differenza reti migliore è di {dr[0]}: più {dr[1]}!", None)])
    for r in T: r.pop("_dr", None)
    rng.shuffle(fatti)
    return [b for f_ in fatti[:2] for b in f_]
def build(D, rng, mercato, nomi=None, conf=None, curva_=None, regole=None):
    nomi = nomi or {}
    b1 = nomi.get('B', 'Beppe Rovesciata'); g1 = nomi.get('G', 'Luigi Fischietti'); g0 = g1.split()[0]; b0 = b1.split()[0]
    a = D["aw"][-1]; T = D["tab"]; P = D["prob"]; n = a["n"]
    row = {r["t"]: r for r in T}
    def pick(x): return rng.choice(x)
    def curva(t): return ""   # niente frasi inventate sulla Curva: si legge solo un post vero (curva.json)
    def pct(x): return f(round(x))
    L = []
    def add(k, t, st=None): L.append((k, " ".join(t.split()), st))
    # --- apertura alla Caressa e Bergomi: la frase passa da una voce all'altra
    add("B", f"Buongiorno, buonasera e buonanotte a tutti, siete su Radio Girrr, la radio ufficiale della Lega O Fant A Girrr! Oggi siamo qui con {b1}", "urlo")
    add("G", f"e {g1}! Si parte!", "urlo")
    add("B", f"Giornata numero {n}! {g0}, hai già guardato i punteggi?")
    add("G", pick(["Guardati, riguardati e ho pure fatto una scommessa con me stesso. Ho perso.", "Sì, al barbecue con gli amici: più di un arrosto bruciato, ma i punteggi li ho letti tutti!", "Certo, qui in studio, appena usciti. Che serata!", "Sul divano, con una pizza in mano: giornata perfetta.", "Altro che guardati: li ho imparati a memoria!", "Sì, in terrazza con un bel caffè. Tutto liscio, sono pronto!", "Con la famiglia a pranzo: nessuno ha parlato d'altro."]))
    # --- punteggi estremi: a volte si esalta, a volte si prende in giro
    tono = pick(["esalta", "sfotte"])
    mv, fl, mz = a["mvp"], a["flop"], a["maz"]
    if tono == "esalta":
        add("B", f"Il re della giornata è {mv[0]}! {f(mv[1])} punti! Che prestazione!", "urlo")
        add("G", f"{f(mv[1])} punti! {curva(mv[0])}")
    else:
        add("B", f"Il re della giornata è {mv[0]}, con {f(mv[1])} punti.")
        add("G", f"Bravi, eh. Però il vero esame è la prossima settimana. {curva(mv[0])}", "sarcasmo")
    if rng.random() < 0.6:
        add("B", f"Dall'altra parte, il flop: {fl[0]} si ferma a {f(fl[1])} punti.")
        add("G", pick([f"Coraggio, {fl[0]}! Si cade, ci si rialza!", f"{f(fl[1])}. Non infierisco. {curva(fl[0])}", "Qui ci vuole un abbraccio. Sottovoce, eh."]), "sus" if rng.random() < 0.4 else None)
        r_ = rng.random()
        if r_ < 0.4: add("B", pick(RIDE), "ride")
        elif r_ < 0.7: add("G", pick(SOSP), "sospiro")
    if mz[2] >= 8:
        add("B", f"E la sconfitta più pesante è quella di {mz[0]}, battuta da {mz[3]} con {f(mz[2])} punti di scarto! Una mazzata!")
        if rng.random() < 0.6: add("G", pick(["Ahia!", "Questa ha fatto male anche a noi!", "Altro che mazzata: una cassa di birra in testa!"]), "urlo")
        if rng.random() < 0.5: add("B", pick(STUP), "stupore")
    # --- classifica: primi tre, e ogni tanto l'ultimo
    t1, t2, t3 = T[0], T[1], T[2]
    add("B", f"In classifica comanda {t1['t']} con {t1['pts']} punti! Seguono {t2['t']} e {t3['t']}.")
    ns = ANNO_SCORSO.get(t1["t"])
    if ns and ns >= 8: add("G", f"E pensare che l'anno scorso {t1['t']} era {ORD[ns]}. Qui c'è una rinascita!", "urlo")
    elif t1["t"] in STORIE: add("G", pick(STORIE[t1["t"]]), "commosso" if t1["t"] in ("Oranje VC", "Atletico ma non troppo", "Grodah") else None)
    last = T[-1]
    if rng.random() < 0.5 or (last["v"] == 0 and last["g"] >= 3):
        add("B", f"In fondo c'è {last['t']}. Può risalire e sperare di uscire dall'ultima posizione?")
        add("G", pick(["Io dico di sì. Poi però bisogna scrivere la formazione!", "La speranza è l'ultima a morire. Come l'ultimo in classifica!", "Una vittoria e si cambia musica!"]))
    nm = numeri(T, n, rng)
    if nm:
        add("B", rng.choice(["E adesso un po' di numeri!", "Diamo i numeri, in senso buono!", "Due numeri sulla stagione!"]))
        for k, t, st in nm: add(k, t, st)
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
    EXP = (regole or {}).get("aspettative") or {"Oranje VC":4,"Apo team":5,"Grodah":3,"WOA":2,"Real Madrink":3,"stif dc":6,"Mariana Coneja":6,"AFA SELECCION":4,"The Blue brothers":7,"Atletico ma non troppo":8}
    def fid(t): r = row[t]; return max(5, min(98, round(50 + (EXP.get(t, 5) - r["pos"]) * 6 + r["v"] * 8 - r["p"] * 8)))
    basso = min(row, key=fid); alto = max(row, key=fid)
    if fid(basso) <= 30 and rng.random() < 0.7:
        add("B", f"Il presidente di {basso} non è molto contento ultimamente!")
        add("G", "Se continua così si parla di esonero. Sottovoce, eh." if fid(basso) <= 15 else "Servono risultati, e anche in fretta.", "sospiro" if fid(basso) > 15 else "sus")
    elif fid(alto) >= 85 and rng.random() < 0.5:
        add("B", f"Il presidente di {alto} è al settimo cielo!")
        add("G", "Con questi punti ci credo. Contratto a vita!")
    # --- storie degli allenatori, una o due a puntata
    teams_in = [mv[0], fl[0]]
    pool = [t for t in teams_in if t in STORIE and (t != t1["t"])]
    if pool and rng.random() < 0.8:
        t = pick(pool); add("G", pick(STORIE[t]), "commosso" if t in ("Oranje VC", "Atletico ma non troppo", "Grodah") else None)
    # --- inviata
    add("B", "Ora ci colleghiamo con la nostra inviata sul campo! Giulia, a te!", "urlo")
    sup = max(((r["t"], EXP.get(r["t"], 5), r["pos"]) for r in T), key=lambda x: x[1] - x[2])
    add("S", f"Grazie {b0}! Qui è un bel caos! Prima notizia: {sup[0]} sta superando le aspettative! Il presidente la voleva intorno al {ORDM.get(sup[1], str(sup[1]))} posto, e invece oggi è {ORD.get(sup[2], str(sup[2])+'ª')}!", "entusiasmo")
    g = D["cal"][0]["m"]
    # --- conferenze stampa della settimana (solo se qualcuno le ha fatte): le mischiamo in un piccolo riepilogo e le confrontiamo col campo
    cf = (conf or {}).get("squadre") or {}
    if cf:
        pt = {r[0]: r[1] for r in a["rows"]}
        avv = {}
        for x, y in (conf.get("partite") or []): avv[x] = y; avv[y] = x
        info = []
        prom = {}
        pare = set()   # squadre la cui promessa si è chiusa in pareggio (esito "p" dal database)
        for t, ans in cf.items():
            if isinstance(ans, dict) and ans.get("esito") == "p": pare.add(t)
            # formato nuovo: {"toni": [...], "promessa": "frase", "pesa": 1|2}; formato vecchio: solo la lista dei toni
            toni = ans.get("toni") if isinstance(ans, dict) else ans
            if isinstance(ans, dict) and ans.get("promessa"): prom[t] = ans
            if t not in pt or t not in avv or avv[t] not in pt: continue
            tono = min(2, round(sum(toni) / len(toni))); vinta = pt[t] > pt[avv[t]]
            info.append((t, tono, vinta, avv[t]))
        TONO = ["si è presentato come la squadra da battere", "è stato molto umile", "ha lanciato la sfida a tutti"]
        VERO = {(0, True): "{t} aveva parlato da campione e ha vinto. Parole mantenute!", (0, False): "{t} aveva parole forti per niente: si è fermato contro {o}.",
                (1, True): "{t} è stato umile, ma in campo ha dimostrato che la sua squadra può fare molto!", (1, False): "{t} è stato umile e il campo gli ha dato ragione: ha perso contro {o}.",
                (2, True): "{t} ha provocato tutti e poi ha vinto: chi di sfida ferisce...", (2, False): "{t} aveva dichiarato guerra e ha perso la battaglia contro {o}."}
        if info:
            ordine = sorted(info, key=lambda z: (z[0] not in prom, z[1] == 1 and not z[2], not ((z[1] == 0 and not z[2]) or (z[1] == 1 and z[2])), z[0]))
            scelte = ordine[:3]
            elenco = "; ".join(f"{t} {TONO[tn]}" for t, tn, _, _ in scelte)
            add("S", f"Dalla sala stampa, nelle conferenze di questa settimana: {elenco}. Vediamo se il campo ha dato ragione!", "entusiasmo")
            # una promessa fatta in conferenza pesa sulla fiducia della dirigenza: la radio lo racconta
            pr = [x for x in info if x[0] in prom]
            for i, (t, tn, v, o) in enumerate(scelte[:2]):
                if t in prom:
                    pz = prom[t]["promessa"].rstrip(".!? ")
                    fr = (f"{t} aveva promesso: {pz}. Contro {o} è finita in pareggio: parola a metà, e la dirigenza aspetta di vedere di più." if t in pare
                          else f"{t} aveva promesso: {pz}. Parola mantenuta, e la dirigenza apprezza!" if v
                          else f"{t} aveva promesso: {pz}. E ha perso contro {o}: parola tradita, e il presidente ha detto che potevano evitare di essere così sfacciati.")
                    add("G" if i == 0 else "B", fr, None if (v or t in pare) else "sarcasmo")
                else:
                    add("G" if i == 0 else "B", VERO[(tn, v)].format(t=t, o=o), "sarcasmo" if (tn == 0 and not v) else None)
    # --- sfide per il derby lanciate in conferenza (stato: accettata / rifiutata / scaduta / attesa)
    for sd in (conf or {}).get("sfide_derby") or []:
        if sd.get("annunciata"): continue   # già annunciata in una puntata: l'annuncio va in onda una volta sola (il Derby si nomina comunque quando si gioca)
        da, ar, st_ = sd.get("da"), sd.get("a"), sd.get("stato")
        if st_ == "accettata": add("S", f"Notizia dalla sala stampa: {da} ha sfidato {ar}, e la sfida è stata accettata! Nasce {sd.get('nome') or 'un nuovo Derby'}, Derby ufficiale per sempre!", "entusiasmo")
        elif st_ == "rifiutata": add("S", f"{da} aveva sfidato {ar}, ma {ar} ha rifiutato. Niente Derby, solo un po' più di rivalità!", "sarcasmo")
        elif st_ == "scaduta": add("S", f"{da} aveva sfidato {ar}, ma {ar} non ha risposto: la sfida è decaduta. Resta un po' di rivalità!")
    # --- Curva: solo un post vero, se Gianluca ne ha dato uno
    cv = (curva_ or {}).get("post")
    if cv: add("S", f"E dalla Curva: {cv}", "entusiasmo")
    # --- il caso della giornata: una notizia vera da raccontare (curva.json, "caso"), messa a mano come il post
    cs = (curva_ or {}).get("caso")
    if cs:
        add("S", f"E c'è un caso che fa discutere: {cs}", "sus")
        add("B", pick(["Regolamento è regolamento! Ma una protesta così non si sentiva da anni!", "Il regolamento parla chiaro, ma qui la polemica è appena cominciata!"]), "sarcasmo")
    add("S", "Per ora è tutto, restituisco la linea in studio!", "entusiasmo")   # il saluto di Giulia chiude sempre il suo collegamento, dopo Derby, Curva e caso
    if cf or cv or cs: add("G", pick(["Grazie Giulia! Questo è calcio!", "Grazie Giulia, collegamento da Oscar!", "Grazie Giulia! Un'altra settimana di parole, vediamo i fatti."]))
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
    # derby: prima i voti degli amici di Gianluca (regole.json, "derby_amici"); senza voti si calcola dalla storia della lega (derby.py)
    import derby as _d
    cand = [m for m in g if _d.e_derby(m[0], m[1], g, regole)]
    der = max(cand, key=lambda m: _d.intensita(m[0], m[1], regole) + _d.rivalita(m[0], m[1], regole)) if cand else None
    # i Derby nati dalle sfide accettate sono ufficiali: se si giocano alla prossima giornata hanno la precedenza
    uff = [(m, sd) for m in g for sd in ((conf or {}).get("sfide_derby") or []) if sd.get("stato") == "accettata" and {sd.get("da"), sd.get("a")} == {m[0], m[1]}]
    if uff:
        m, sd = uff[0]
        add("B", f"Alla prossima giornata c'è il Derby! {sd.get('nome') or 'Derby'}: {m[0]} contro {m[1]}!", "urlo")
    elif der: add("B", f"Alla prossima giornata c'è il Derby: {der[0]} contro {der[1]}!" + (" Una rivalità storica!" if _d.rivalita(der[0], der[1], regole) >= 70 else ""), "urlo")
    # --- mercato: Ciro c'è solo se ci sono notizie
    notizie = (mercato or {}).get("notizie") or []
    if notizie:
        add("B", "E adesso il mercato! Abbiamo notizie, e per commentarle chiamiamo Ciro Trattativa!", "urlo")
        add("C", "Buongiorno a tutti, qui Ciro Trattativa. Notizie fresche dal mercato!")
        for z in notizie[:3]:
            tx = z["testo"][0].upper() + z["testo"][1:]
            if z["tipo"] == "ufficiale": add("C", f"Ufficiale! {tx}.", "urlo")
            else: add("C", f"Lo dirò sottovoce: semi ufficiale, prendetelo con le pinze! {tx}.", "sus")
        add("G", "Ciro, come sempre, sicurissimo! Al cento per cento.")
    # --- chiusura
    add("B", "Per Radio Girrr, la radio ufficiale della Lega, è tutto! Mettete la formazione, vi vogliamo bene!", "urlo")
    add("G", "Ci sentiamo mercoledì prossimo! Ciao a tutti!", "urlo")
    return L
