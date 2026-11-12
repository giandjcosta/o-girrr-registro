#!/usr/bin/env python3
"""Curva: nuovi personaggi, più frasi e immagini nuove (Claude, 12 novembre 2026). Prototipo per il Lab.

Decisioni di Gianluca (12 novembre): i 12 account proposti (La Suocera Tifosa diventa La Prof di Matematica, perché
«La Suocera» c'è già), Pizzeria Fuorigioco non verificata, Radio Girrr e Il VAR del Girrr verificati; più frasi per ogni
personaggio, anche provocatorie; immagini disegnate dalla pagina con dati veri (lavagna del bar con i risultati, altre
foto d'epoca e altre), senza servizi a pagamento.

I cori della Curva sono calcolati dalla data (stessa data, stessi cori per tutti). Per non cambiare i giorni passati,
tutto il nuovo entra dal giorno TAGLIO_N in poi, come le frasi NUOVE dal 2 novembre. Nel Lab TAGLIO_N è oggi;
al rilascio va messo il giorno del rilascio.

Uso: python3 rilascio/curva-os/banca.py CARTELLA_DEL_SITO
Scrive rilascio/curva-os/pagine/girrr/curva-banca.js e rilascio/curva-os/pagine/stadio/girrr/curva-banca.js.
I nomi, le biografie e i colori dei nuovi account e i disegni delle immagini nuove sono in applica.py (curva.html).
"""
import os
import sys

BLOCCO = r'''
/* ===== Nuovi personaggi, frasi e immagini (Claude, 12 novembre 2026) =====
   Entrano dal giorno TAGLIO_N in poi: i giorni passati restano uguali. Le immagini nuove si disegnano in curva.html (MEMEPLUS). */
var TAGLIO_N=Math.floor(Date.UTC(2026,10,12)/864e5);
var PERS_N={
 rodrigo_saudade:{
  gen:["Ragazzi, o fantacalcio italiano é uma loucura. Ma eu adoro. {#}","Qui in Italia il caffè è perfetto e il fantacalcio è un dramma. No Brasil é o contrário.","Ho spiegato il modulo a mia madre a Rio. Ha detto: muito complicado, ma tifo pela {top}."],
  ri:["Que golaço, {vinc}! {sc} contro {perd}: isso é futebol, gente! ⚽","{perd} perde {sc}. Calma, amigos: anche il Brasil ha perso, una volta. Ou duas.","{vinc} vince {sc} e io ballo samba in salotto. I vicini meno."],
  cl:["{top} in testa. Tem ginga, tem alegria. Gli altri? Saudade.","{sq} al {pos}° posto. Meu Deus, la difesa. Ma o ataque é bonito.","{sq} al {pos}° posto: mais samba e meno tattica, por favor."],
  pm:["{sq} gioca bonito ma non segna. Brasileiro demais, poco italiano."],
  mk:["{gio} a {sq}? Bom jogador. Non è Ronaldinho, ma chi lo è?"],
  al:["{all}, amigo: più fantasia, menos panchina. Joga bonito!"],
  so:["Sorpresa {sq}? No Brasil diciamo: o futebol é uma caixinha de surpresas."]},
 klaus_puenktlich:{
  gen:["Formazione consegnata alle 14:59. Ordnung muss sein. {#}","In Germania la formazione si fa il lunedì. Qui il sabato alle 14:58. Unglaublich.","Ho fatto un foglio di calcolo per il fantacalcio. Poi un foglio per il foglio. Alles klar."],
  ri:["{vinc} batte {perd} {sc}. Risultato corretto, efficiente. Wunderbar.","{sc} per {vinc}. Previsto nel mio modello alla seconda cifra decimale. Natürlich.","{perd} perde {sc}. Troppo Chaos, troppo poco Ordnung."],
  cl:["Classifica controllata: {top} primo. Tutto in ordine. Gut.","{sq} al {pos}° posto. Non è una tragedia, è un dato. Ich bin ruhig.","{sq} al {pos}° posto. Serve Disziplin, non speranza."],
  pm:["{sq}: buona organizzazione, poca precisione. Note: sieben su zehn."],
  al:["{all} cambia modulo ogni settimana. In Germania lo chiamiamo: nein."],
  mk:["Acquistare {gio}? Prima un'analisi costi e benefici. Poi forse. Vielleicht."],
  so:["Sorpresa {sq}? Le sorprese sono solo dati non ancora capiti."]},
 elpibe_rosario:{
  gen:["El fútbol es pasión, hermano. Il fantacalcio è pasión con la calcolatrice. {#}","Da noi a Rosario si gioca per strada. Qui si gioca sul divano. ¡Igual de bueno!","Ho messo il capitano col cuore, non con la testa. Como siempre."],
  ri:["¡Qué partido! {vinc} vince {sc} con garra. Esto es fútbol, hermano.","{perd} perde {sc}. Ma non mollare: el que abandona no tiene premio.","{vinc} {sc}: golazo de media cancha, almeno nella mia testa."],
  cl:["{top} primero. Ma il campionato è lungo, como un tango.","{sq} al {pos}° posto. Serve più garra, menos excusas.","{sq} al {pos}° posto: ¡vamos, que se puede!"],
  pm:["{sq} ha giocato con el corazón. Le gambe sono arrivate dopo."],
  al:["{all} es un poeta. Un poeta che fa formazioni strane, pero poeta."],
  mk:["{gio} a {sq}? Si tiene garra, bienvenido."],
  so:["¿Sorpresa {sq}? En el fútbol todo puede pasar. Anche questo."]},
 mister_tea:{
  gen:["Lovely stuff. Il fantacalcio è come il cricket: nessuno lo capisce davvero. {#}","Tea at five, formazione alle sei. Very civilised.","Da noi la domenica c'è il pub. Qui il gruppo WhatsApp. Same thing, really."],
  ri:["{vinc} {sc} su {perd}. Proper football. Jolly good.","{perd} perde {sc}. Not cricket, ma succede.","{sc} per {vinc}. I say, che pomeriggio."],
  cl:["{top} on top. Rather impressive, I must admit.","{sq} al {pos}° posto. Keep calm and fanta on.","{sq} al {pos}° posto. Oh dear."],
  pm:["{sq} today: brilliant, then terrible, then brilliant. Very British."],
  al:["{all}, old chap: meno rotazioni, più tea."],
  mk:["{gio} a {sq}? A bargain, if you ask me. Nobody did."],
  so:["Sorpresa {sq}? Quite the turn-up for the books."]},
 jp_chic:{
  gen:["Il fantacalcio è come la moda: tutto torna. Anche il 3-5-2. Voilà. {#}","Je suis désolé, ma la mia formazione era troppo elegante per vincere.","Un caffè, un croissant, una formazione sbagliata. C'est la vie."],
  ri:["{vinc} vince {sc}. C'est magnifique. Ma il centrocampo, oh là là.","{perd} perde {sc}. Pas de panique: domani si ricomincia, avec style.","{sc} per {vinc}. Très chic."],
  cl:["{top} en tête. Bravo, ma senza eleganza.","{sq} al {pos}° posto. Il y a du travail, mes amis.","{sq} al {pos}° posto. Un disastro, voilà."],
  pm:["{sq} ha giocato con la grazia di un elefante in un atelier."],
  al:["{all}: più fantasia, moins de confusion. Merci."],
  mk:["{gio} a {sq}? Un acquisto di stile. Il rendimento è un'altra storia."],
  so:["Sorpresa {sq}? Comme d'habitude."]},
 mamma_del_portiere:{
  gen:["Il portiere non sbaglia mai: sbaglia la difesa davanti. Ve lo dico da mamma. {#}","Mio figlio para tutto, anche i rimproveri del mister.","Ho fatto la lasagna per tutta la squadra. Un clean sheet si festeggia."],
  ri:["{perd} perde {sc}. La colpa? La difesa. Il portiere era perfetto.","{vinc} vince {sc}. Grazie al portiere, ovviamente. Chi altro?","{sc}: e io dico sempre che il portiere è il più bravo."],
  cl:["{sq} al {pos}° posto. Con un portiere così dovreste essere primi.","{top} in testa: ha un portiere che mangia bene, si vede."],
  pm:["{sq}: il portiere ha salvato la partita. Gli altri hanno solo corso."],
  al:["{all}, il portiere non si tocca. Se no vengo io in panchina."],
  so:["Sorpresa {sq}? Io no, il portiere ve l'avevo detto."]},
 meteo_girrr:{
  gen:["Previsioni per il weekend: pioggia di gol a nord, nebbia in difesa al centro. {#}","Allerta gialla per i fantallenatori che non hanno ancora fatto la formazione.","Temperatura del gruppo WhatsApp: in aumento verso sera."],
  ri:["Bollettino: su {vinc} splende il sole, su {perd} temporale dopo il {sc}.","{sc}: era prevista nebbia, invece è arrivata la grandine di gol.","{perd} esce dal {sc} con il cielo coperto. Schiarite attese la prossima settimana."],
  cl:["In testa alta pressione su {top}. Bassa pressione in fondo alla classifica.","{sq} al {pos}° posto: variabile, con possibili rovesci."],
  pm:["Su {sq} oggi venti forti da destra. La difesa è volata via."],
  al:["Perturbazione in arrivo sulla panchina di {all}. Portate l'ombrello."],
  so:["Sorpresa {sq}: nessun modello l'aveva prevista. Nemmeno il mio."]},
 ultra_da_divano:{
  gen:["Coro dal divano: FORZA! (Poi ho chiesto la pizza.) {#}","Ho cantato per novanta minuti. Il gatto è scappato al quarto d'ora.","Sciarpa al collo, telecomando in mano. Il vero ultrà non si alza mai."],
  ri:["{vinc} {sc}! Ho urlato così forte che il vicino ha battuto sul muro. Ricambiato.","{perd} perde {sc}. Ho lanciato il cuscino. Il cuscino sta bene.","{sc} per {vinc}: coreografia dal divano riuscita, coperta rossa e popcorn."],
  cl:["{top} primo! Stasera fumogeno di candele profumate.","{sq} al {pos}° posto. Il divano non abbandona mai."],
  pm:["{sq} oggi meritava i fischi. Fischiati. Dal divano."],
  al:["{all} fuori! Poi dentro. Poi vediamo. Il divano decide."],
  so:["Sorpresa {sq}! Ho rovesciato le patatine."]},
 pentito_del_fanta:{
  gen:["Confesso: anche questa settimana ho tolto quello che poi ha segnato. {#}","Mi pento della formazione di domenica. E di quella di prima. E di quella prima ancora.","Non lo faccio più. Lo dico ogni lunedì."],
  ri:["{vinc} vince {sc}. Avevo pensato di metterlo, poi ho cambiato idea. Classico.","{perd} perde {sc}. Io c'ero, in panchina. Con il mio rimorso.","{sc}: lo sapevo. Non l'ho fatto. Mi pento."],
  cl:["{sq} al {pos}° posto. Con le formazioni giuste sarebbe primo. Mea culpa.","{top} in testa. Io in testa ho solo rimpianti."],
  pm:["{sq}: tre scelte, tre errori. Una costanza che fa paura."],
  al:["{all}, ti capisco: anche io cambio idea alle 14:59."],
  mk:["Ho venduto {gio} una settimana fa. Ovviamente ora segna."],
  so:["Sorpresa {sq}? La sorpresa vera è che io abbia indovinato qualcosa."]},
 prof_di_mate:{
  gen:["Esercizio per casa: se ogni domenica sbagli un capitano, quanti capitani sbagli in un anno? {#}","Nel gruppo WhatsApp ho contato 47 «ma dai». Media alta, deviazione standard altissima.","Il fantacalcio è statistica con le emozioni. Io porto la statistica."],
  ri:["{vinc}–{perd} {sc}: risultato corretto. Il procedimento di {perd}, invece, da rivedere.","{sc} per {vinc}. Voto al compito: otto. Ordine e precisione.","{perd} perde {sc}. Insufficiente, ma recuperabile."],
  cl:["{top} primo: dimostrazione ben fatta. {sq} al {pos}°: rivedere le ipotesi.","Classifica corretta a matita: {sq} al {pos}° posto. Bisogna studiare di più."],
  pm:["{sq}: tanta fantasia, pochi calcoli. Si vede."],
  al:["{all}: il modulo non è un'opinione. Ripassiamo i numeri."],
  so:["Sorpresa {sq}? Era nell'intervallo di confidenza. Al limite."]},
 bomber99:{
  gen:["raga ma il fanta e tipo il gioco ma piu stressante {#}","domenica ho urlato cosi tanto che mia nonna ha chiesto se avevamo vinto lo scudetto","chi mi spiega il modificatore della difesa senza farmi addormentare"],
  ri:["{vinc} {sc} ez","{perd} ha perso {sc} ahahah gg","{sc} raga {vinc} e in fiamme 🔥🔥"],
  cl:["{top} primo pazzesco","{sq} {pos}° bro che succede"],
  pm:["{sq} oggi lag totale"],
  al:["{all} cambia formazione ogni volta tipo che e una skin"],
  so:["{sq} plot twist assurdo"]},
 utente84629:{
  gen:["Ok.","Interessante.","Seguo.","Ah."],
  ri:["{sc}. Giusto.","{vinc}. Bene.","{perd}. Peccato."],
  cl:["{top} primo. Ci sta.","{sq} al {pos}°. Vedremo."],
  pm:["{sq}. Mah."],
  so:["Questa non me l'aspettavo."]},
 pizzeria_fuorigioco:{
  gen:["Stasera la Pizza Capolista è dedicata a {top}. Mozzarella, pomodoro e un po' di invidia. {#}","Da noi il forno è sempre caldo, come il gruppo della lega la domenica sera.","Prenotate il tavolo per la prossima giornata: il dolce lo offre la casa a chi vince."],
  ri:["{vinc} vince {sc}: pizza Margherita offerta dallo chef (al vincitore, non al gruppo).","{perd} perde {sc}. Consolatevi con una diavola: piccante come la sconfitta.","{sc} per {vinc}. Festeggiamo con una calzone, chiusa come la sua difesa."],
  cl:["Nuova pizza della settimana: la «{top}», in cima alla classifica e al menù.","{sq} al {pos}° posto? Abbiamo la pizza giusta: la Quattro Stagioni, per ricominciare."],
  pm:["{sq} oggi: tanta farina, poco lievito."],
  al:["{all}, passa in pizzeria: una buona pizza schiarisce le idee sulla formazione."]},
 radio_girrr:{
  gen:["Radio Girrr: le voci della lega, dopo ogni giornata. {#}","Siamo in onda con il commento della giornata. Volume su.","In studio si parla di Derby, classifica e del prossimo turno."],
  ri:["In onda: {vinc} batte {perd} {sc}. Il commento completo nella puntata della giornata.","{vinc} {sc} su {perd}: ne parliamo nella puntata di oggi.","Radio Girrr: {sc} per {vinc}. Le reazioni degli allenatori in onda."],
  cl:["Radio Girrr: {top} guida la classifica. Il punto completo in onda.","{sq} al {pos}° posto: in puntata le prospettive per il prossimo turno."],
  pm:["Stasera in onda: la giornata di {sq} e il resto della lega."],
  al:["In studio si discute delle scelte di {all}. Chiamate in diretta (nel gruppo)."]},
 var_girrr:{
  gen:["Il VAR del Girrr rivede gli episodi della giornata. Si decide al monitor. {#}","Check in corso. Nessuno tocchi il telecomando.","Episodio rivisto tre volte, da tre angolazioni. Decisione confermata."],
  ri:["Check VAR su {vinc}–{perd} {sc}: risultato confermato.","{sc} per {vinc}. Revisione completata, si riparte.","Rivisto l'episodio decisivo di {perd}. La Moviola completa su Girrr Sport."],
  cl:["Classifica verificata al monitor: {top} in testa. Decisione confermata.","{sq} al {pos}° posto. Nessun intervento necessario."],
  pm:["Su {sq} c'è un episodio da rivedere. Lo trovate nella Moviola."],
  al:["Il VAR non entra nelle scelte di {all}. Per fortuna di tutti."]}
};
var NUOVI=Object.keys(PERS_N);
NUOVI.forEach(function(a){PERS[a]=PERS_N[a]});
/* Più frasi per i personaggi di sempre (anche qualcuna provocatoria) */
var NUOVE2={
 nonno_cesare:{gen:["Ai miei tempi la formazione si consegnava a voce. E il mister se la ricordava."],ri:["{vinc} {sc}. Bella partita. Ai miei tempi però si esultava meno e si vinceva di più."]},
 tifoso_arrabbiato:{cl:["{sq} al {pos}° posto. Cambiate nome, colori e modulo. Non la posizione: quella cambiatela due volte."],ri:["{perd} perde {sc}. Io ho già scritto la lettera di protesta. A chi? A tutti."]},
 il_complottista:{cl:["{top} in testa da settimane. Coincidenze? Io tengo un quaderno."],gen:["Perché il calendario mette sempre certe partite di sabato? Rifletteteci. {#}"]},
 il_romantico_del_pallone:{gen:["Il fantacalcio ci ricorda che anche un panchinaro può cambiare una domenica."],ri:["{vinc} {sc}: c'è ancora poesia, nel calcio."]},
 ing_stadi:{gen:["Ho misurato la panchina di {sq}: è lunga 6 metri. Le idee del mister, meno."]},
 il_super_tifoso:{ri:["Sapevo che {vinc} avrebbe vinto {sc}. Lo sapevo da sempre. Da stamattina."]},
 il_barista:{gen:["Al bancone si accettano pronostici, lamentele e caffè. In quest'ordine. {#}"],cl:["{top} in testa: oggi caffè offerto ai tifosi. Domani si vedrà."]},
 il_mago_cabala:{gen:["Le stelle dicono: capitano scelto di mercoledì porta fortuna. Il giovedì no."]},
 la_suocera:{gen:["Mio genero passa la domenica col fantacalcio. Almeno così non tocca il telecomando."]},
 il_tassista:{gen:["Il cliente di stamattina tifava {top}. Gli ho fatto lo sconto. Per pietà verso gli altri."]},
 fidanzata_stufa:{gen:["Ha detto «solo cinque minuti per la formazione». Era giovedì."]},
 americano_spaesato:{gen:["Still don't understand the modificatore. But I love the drama. {#}"]},
 mister_divano:{al:["{all}, quel cambio al 60° lo avrei fatto al 59°. Dettagli che fanno campionati."]},
 radio_spogliatoio:{gen:["Dallo spogliatoio: c'è chi canta sotto la doccia e chi ripensa al capitano sbagliato."]},
 mamma_di_capitan:{gen:["Mio figlio è capitano solo quando sbaglia gli altri. Ve lo segnalo."]},
 ex_ds_provincia:{mk:["{gio} a {sq}? Ai miei tempi un affare così si chiudeva in trattoria."]},
 var_parlante:{gen:["Io parlo, il VAR del Girrr decide. Ognuno il suo mestiere."]},
 fc27_ratings:{gen:["Aggiornamento in arrivo: overall in salita per chi ha segnato, in discesa per chi ha parlato troppo."]},
 il_cugino_del_dt:{mk:["Mio cugino dice che {gio} è già d'accordo con {sq}. Mio cugino dice tante cose."]},
 telecronista_stanco:{ri:["{vinc} {sc} su {perd}. Lo dico con l'entusiasmo che mi resta. Poco."]},
 gufo_professionista:{cl:["{top} in testa? Uh uh. Il campionato è lungo, le mie ali pure."]},
 il_filosofo_del_pallone:{gen:["Il pareggio è il modo che ha il calcio di dirci che abbiamo ragione entrambi. O torto."]},
 bomber_da_bar:{gen:["Al bar ho segnato 300 gol. Tutti di testa, tutti in fuorigioco."]},
 statistico_folle:{cl:["{sq} al {pos}° posto: ho fatto 10.000 simulazioni. In 9.999 avevo dimenticato il caffè."]},
 arbitro_in_pensione:{gen:["Fischiavo meno di voi nel gruppo WhatsApp. E avevo il fischietto."]}
};
var MA_N=["Cambia il nome di {sq}, non la posizione: {pos}° resta {pos}°. {#}","{all}, ottimo lavoro. Ma i risultati li fa {sq} da sola?","Se {sq} fosse una pizza, sarebbe una margherita: buona, ma nessuno la ordina per festeggiare."];
var MAD_N=["Cambia il nome di {sq}, non la posizione. {#}","{all}: due allenatori, un solo divano, nessuna idea condivisa.","Per {sq} serviva un rinforzo. Hanno preso un altro allenatore."];
/* Immagini nuove per i personaggi (disegnate dalla pagina, con i dati veri della lega) */
var IMGPER_N={il_barista:[['lavagna_ris','ri,cl,gen,pm']],nonno_cesare:[['epoca2','*']],rodrigo_saudade:[['cartolina','*']],klaus_puenktlich:[['tabelle','*']],
 meteo_girrr:[['meteo','*']],pizzeria_fuorigioco:[['pizza','*']],radio_girrr:[['onda','*']],var_girrr:[['var','*']],prof_di_mate:[['quaderno','*']],ultra_da_divano:[['coreo','*']]};
/* Utenti qualunque nuovi, con nomi un po' a caso */
var COMUNI_N=[['gianfra_77','Gianfra77','s'],['la_vale_tifa','LaValeTifa','g'],['tommy.ultras','tommy.ultras','a'],['sere_fanta','Sere_Fanta','i'],['pippo_sabato','PippoSabato','s'],['mr_contropiede','Mr Contropiede','c'],['luca_95','luca_95','p'],['zio_franco','ZioFranco','g']];
function comuneG(r,g){return g>=TAGLIO_N?pick(r,COMUNI.concat(COMUNI_N)):comune(r)}
/* Dati veri per le immagini nuove: risultati dell'ultima giornata, prime della classifica, prossimo turno */
function cxPiu(cx,ST){try{if(ST.ult){cx.g=ST.ult.n;cx.ris=ST.ult.m.map(function(m){return [m[0],m[3],m[4]]})}if(ST.cls)cx.cls=ST.cls.slice(0,6).map(function(t){return [t.n,t.pt]});if(ST.next){cx.gn=ST.next.n;cx.prox=ST.next.m.map(function(m){return [m[0],m[3]]})}}catch(e){}}
'''

SOSTITUZIONI = [
    ("var ordine=shuffle(r,AUTORI);", "var ordine=shuffle(r,g>=TAGLIO_N?AUTORI.concat(NUOVI):AUTORI);"),
    ("if(g>=TAGLIO_G&&NUOVE[a]&&NUOVE[a][cat])lis=lis.concat(NUOVE[a][cat]);",
     "if(g>=TAGLIO_G&&NUOVE[a]&&NUOVE[a][cat])lis=lis.concat(NUOVE[a][cat]);if(g>=TAGLIO_N&&NUOVE2[a]&&NUOVE2[a][cat])lis=lis.concat(NUOVE2[a][cat]);"),
    ("lis=du?MAD:MA;ix=Math.floor(rm()*lis.length)",
     "lis=du?(g>=TAGLIO_N?MAD.concat(MAD_N):MAD):(g>=TAGLIO_N?MA.concat(MA_N):MA);ix=Math.floor(rm()*lis.length)"),
    ("po.cx={sq:c.sq,sq2:c.sq2,gio:c.gio,pt:c.pt};\n  if(IMGPER[a]&&ri()<0.6){var iml=IMGPER[a],",
     "po.cx={sq:c.sq,sq2:c.sq2,gio:c.gio,pt:c.pt};if(g>=TAGLIO_N){cxPiu(po.cx,ST);po.cx.vinc=c.vinc;po.cx.perd=c.perd;po.cx.sc=c.sc}\n  var iml0=(IMGPER[a]||[]).concat(g>=TAGLIO_N&&IMGPER_N[a]?IMGPER_N[a]:[]);\n  if(iml0.length&&ri()<0.6){var iml=iml0,"),
    ("cu=comune(rc),fc=rc()<0.12", "cu=comuneG(rc,g),fc=rc()<0.12"),
    ("window.CVB={MISTER:MISTER,COMUNI:COMUNI,", "window.CVB={MISTER:MISTER,COMUNI:COMUNI,COMUNI_N:COMUNI_N,NUOVI:NUOVI,"),
]


def applica(t):
    for a, b in SOSTITUZIONI:
        n = t.count(a)
        assert n == 1, 'trovato %d volte: %s' % (n, a[:70])
        t = t.replace(a, b)
    k = 'window.CVB={'
    assert t.count(k) == 1
    return t.replace(k, BLOCCO.strip() + '\n' + k)


if __name__ == '__main__':
    sito = sys.argv[1]
    qui = os.path.dirname(os.path.abspath(__file__))
    for rel in ('girrr/curva-banca.js', 'stadio/girrr/curva-banca.js'):
        t = open(os.path.join(sito, rel), encoding='utf-8').read()
        out = os.path.join(qui, 'pagine', rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(applica(t))
        print('scritto', out)
