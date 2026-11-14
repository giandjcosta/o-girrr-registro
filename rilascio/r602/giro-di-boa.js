/* O Girrr · Giro di boa 6.0.2. Pagina e album leggono il calcolo del workflow.
   Qui si impaginano fatti già calcolati: nessuna classifica ricostruita nel browser. */
(function () {
  'use strict';
  if (window.GirrrBoa) return;
  const script = document.currentScript;
  const ROOT = new URL('./', script.src).href;
  const viste = new Map();
  const scelte = new Map(); // Conserva la scelta anche se Carriera si ridisegna dopo una lettura.
  const ND = 'Dato non conservato', E = s => String(s == null ? ND : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const N = v => v == null ? ND : Number(v).toLocaleString('it-IT', { maximumFractionDigits: 3 });
  const nome = t => t === 'The Blue brothers' ? 'The Blues Brothers' : t;
  const text = s => String(s).replace(/·\s*(\p{Ll})/gu, (_, c) => '· ' + c.toUpperCase());
  const pl = (n,uno,tanti) => `${n} ${n===1?uno:tanti}`;
  const B = b => `${pl(b.vittorie,'vittoria','vittorie')} · ${pl(b.pareggi,'pareggio','pareggi')} · ${pl(b.sconfitte,'sconfitta','sconfitte')}`;
  const match = p => `${p.giornata}ª: ${nome(p.squadra_casa)} ${p.risultato} ${nome(p.squadra_trasferta)}`;
  const serie = s => s.partite ? `${pl(s.partite,'partita','partite')} (${s.dalla===s.alla?'alla '+s.dalla+'ª':'dalla '+s.dalla+'ª alla '+s.alla+'ª'})` : 'Nessuna';
  const record = r => r ? match(r.partita) + (r.ex_aequo.length ? ` · Altre ${r.ex_aequo.length} a pari merito` : '') : 'Nessuna';
  function titolo(j, k) { return k === 'ritorno' ? `Il ritorno dopo la ${j.periodi[k].alla_giornata}ª giornata` : j.ultima_pubblicata >= 17 ? (k === 'andata' ? 'Giro di boa · Girone d’andata' : 'Giro di boa · Fino ad ora') : `Il punto dopo la ${j.ultima_pubblicata}ª giornata`; }
  function periodo(j, k) { return j.periodi[k] || j.periodi.finora; }
  async function carica(root = ROOT) {
    const r = await fetch(/\.json$/.test(root) ? root : new URL('girrr/dati/giro-di-boa.json', root), {cache:'no-cache'});
    if (!r.ok) throw new Error('Il bilancio non è disponibile adesso. Riprova più tardi.');
    const j = await r.json();
    if (j.schema !== 1 || !j.periodi?.finora || !j.ultima_pubblicata) throw new Error('Nessuna giornata pubblicata per il bilancio.');
    return j;
  }
  function sezioni(s) {
    const f = s.dirigenza, c = s.coppa, d = s.derby, p = s.promesse;
    return [
      ['Classifica', `${s.posizione}ª posizione · ${s.punti_classifica} punti in classifica · ${s.distacco_vetta} punti dalla vetta`],
      ['Zona retrocessione', s.in_zona_retrocessione ? `Ultimo posto · ${s.distacco_penultimo} punti dal penultimo` : `${s.margine_ultimo_posto} punti di margine sull’ultimo posto`],
      ['Bilancio', `${s.bilancio.giocate} partite · ${B(s.bilancio)} · ${s.bilancio.punti} punti nel periodo`],
      ['In casa', `${s.casa.giocate} partite · ${B(s.casa)} · ${s.casa.punti} punti`],
      ['In trasferta', `${s.trasferta.giocate} partite · ${B(s.trasferta)} · ${s.trasferta.punti} punti`],
      ['Gol del risultato', `${s.bilancio.gol_fatti} fatti · ${s.bilancio.gol_subiti} subiti · Differenza reti ${s.differenza_reti > 0 ? '+' : ''}${s.differenza_reti}`],
      ['Vittoria più larga', record(s.vittoria_piu_larga)], ['Sconfitta più pesante', record(s.sconfitta_piu_pesante)],
      ['Serie di vittorie', serie(s.serie.vittorie)], ['Imbattibilità', serie(s.serie.imbattibilita)],
      ['Digiuno di vittorie', serie(s.serie.senza_vittorie)], ['Digiuno di gol', serie(s.serie.senza_gol)],
      ['Presidente', `${f.giudizio} · Attesa ${f.attesa == null ? ND : f.attesa + 'ª'} · Fascia ${f.fascia} · ${f.obiettivo}`],
      ['Fiducia', `${f.fiducia == null ? ND : N(f.fiducia) + ' su 100'} · Scostamento dall’attesa: ${f.scostamento_posizioni == null ? ND : (f.scostamento_posizioni > 0 ? '+' : '') + f.scostamento_posizioni + ' posizioni'}`],
      ['Derby', d.disponibile ? `${d.giocate} giocati · ${B(d)}` : ND],
      ['Champions Cup', `${c.gironi.length ? 'Girone ' + c.gironi.join(', ') : ND} · ${c.punti_girone == null ? ND : c.punti_girone + ' punti nel girone'} · ${c.qualificazione} · Nel periodo: ${B(c)}`],
      ['Promesse in conferenza', p.disponibile ? `${p.mantenute} mantenute · ${p.pari} pari · ${p.tradite} tradite · ${p.da_valutare} da valutare` : ND],
      ['MVP dei tifosi', s.mvp.disponibile ? `${s.mvp.ricevuti} ricevuti${s.mvp.giornate.length ? ' · Giornate ' + s.mvp.giornate.join(', ') : ''}` : ND],
      ['Partite sul filo', `${s.sul_filo.length} partite decise sul filo · Un gol di differenza`]
    ].map(([a,b]) => [a,text(b)]);
  }
  function andamento(s) {
    if (!s.andamento.length) return '<p>' + ND + '</p>';
    const a = s.andamento, x = i => 32 + i * 636 / Math.max(1,a.length-1), y = p => 22 + (p-1)*18;
    return `<svg class="gb-grafico" viewBox="0 0 700 210" role="img" aria-label="Posizione giornata per giornata"><path d="${a.map((v,i)=>(i?'L':'M')+x(i)+' '+y(v.posizione)).join(' ')}" fill="none" stroke="currentColor" stroke-width="4"/>${a.map((v,i)=>`<circle cx="${x(i)}" cy="${y(v.posizione)}" r="5"/><title>${v.giornata}ª giornata: ${v.posizione}ª posizione</title>`).join('')}</svg><div class="gb-storia">${a.map(v=>`<span><small>${v.giornata}ª giornata</small><b>${v.posizione}ª</b></span>`).join('')}</div>`;
  }
  function dettagli(s) {
    return `<h3>${E(nome(s.squadra))}</h3><div class="gb-fatti">${sezioni(s).map(([a,b])=>`<div><h4>${a}</h4><p>${E(b)}</p></div>`).join('')}</div>
      <details><summary>Andamento in classifica</summary>${andamento(s)}</details>
      <details><summary>Tutte le partite di Campionato</summary><ul>${s.partite.map(p=>`<li>${E(match(p))} · ${p.casa?'In casa':'In trasferta'}</li>`).join('')}</ul></details>
      <details><summary>Risultati dei Derby</summary><p>${E(s.derby.criterio)}</p><ul>${s.derby.disponibile ? s.derby.partite.map(p=>`<li>${E(p.nome_derby)} · ${E(match(p))}</li>`).join('') || '<li>Nessun Derby giocato</li>' : '<li>'+ND+'</li>'}</ul></details>
      <details><summary>Percorso in Champions Cup</summary><ul>${s.coppa.partite.map(p=>`<li>${E(match(p))} · ${E(p.gruppo)}</li>`).join('') || '<li>Nessuna partita nel periodo</li>'}</ul></details>
      <details><summary>Le conferenze</summary><ul>${s.promesse.disponibile ? s.promesse.partite.map(p=>`<li>${p.giornata}ª giornata: ${E(p.promessa)} · ${{v:'Mantenuta',s:'Pari',p:'Tradita'}[p.esito]||'Da valutare'}</li>`).join('') || '<li>Nessuna promessa conservata nel periodo</li>' : '<li>'+ND+'</li>'}</ul></details>
      <details><summary>I numeri</summary><p>Totale: ${N(s.numeri.totali)} Fantapunti · Media: ${N(s.numeri.media)} Fantapunti<br>Sul filo: scarto in Fantapunti non superiore a ${N(s.numeri.soglia_sul_filo_fantapunti)}, con un gol di differenza.</p><ul>${s.sul_filo.map(p=>`<li>${E(match(p))} · ${N(p.fantapunti)} contro ${N(p.fantapunti_avversario)} Fantapunti</li>`).join('') || '<li>Nessuna partita entro la soglia</li>'}</ul></details>`;
  }
  const COLORI={V:'#61dbb2',N:'#c2cede',P:'#ff7b85'};
  const ESITI={V:'Vittoria',N:'Pareggio',P:'Sconfitta'};
  function pallini(partite,limite=5) {
    return `<div class="gb-forma" aria-label="Ultimi risultati">${partite.slice(-limite).map(m=>`<span class="gb-esito gb-${m.esito}" title="${E(match(m))}" aria-label="${E(match(m))} · ${ESITI[m.esito]}">${m.esito}</span>`).join('')}</div>`;
  }
  const legenda=()=>'<p class="gb-legenda"><span class="gb-V">V</span> Vittoria <span class="gb-N">N</span> Pareggio <span class="gb-P">P</span> Sconfitta</p>';
  function traccia(s) {
    if(!s.andamento.length)return '<p>'+ND+'</p>';
    const a=s.andamento,x=i=>36+i*628/Math.max(1,a.length-1),y=n=>24+(n-1)*15.5;
    return `<svg class="gb-grafico" viewBox="0 0 700 205" role="img" aria-label="Posizione dalla ${a[0].giornata}ª alla ${a.at(-1).giornata}ª giornata. ${a.map(v=>v.giornata+'ª: '+v.posizione+'ª').join('; ')}"><line x1="36" x2="664" y1="24" y2="24" stroke="#ffffff25"/><line x1="36" x2="664" y1="163.5" y2="163.5" stroke="#ffffff25"/><text x="2" y="29" fill="#bfe3ff" font-size="15">1ª</text><text x="0" y="169" fill="#bfe3ff" font-size="15">10ª</text><path d="${a.map((v,i)=>(i?'L':'M')+x(i)+' '+y(v.posizione)).join(' ')}" fill="none" stroke="#bfe3ff" stroke-width="3"/>${a.map((v,i)=>`<circle cx="${x(i)}" cy="${y(v.posizione)}" r="${a.length>17?4:7}" style="fill:${COLORI[s.partite.find(m=>m.giornata===v.giornata)?.esito]||'#ffd166'}"><title>${v.giornata}ª giornata · ${v.posizione}ª posizione</title></circle>`).join('')}<text x="36" y="197" fill="#bfe3ff" font-size="15">${a[0].giornata}ª giornata</text><text x="664" y="197" text-anchor="end" fill="#bfe3ff" font-size="15">${a.at(-1).giornata}ª giornata</text></svg>`;
  }
  function voceHTML(v,curva=false) {
    return v?`<blockquote class="gb-voce ${curva?'gb-curva':''}"><small>${curva?'Dalla Curva':'Girrr Sport · Redazione'}</small>${v.titolo?'<h4>'+E(v.titolo)+'</h4>':''}<p>«${E(v.testo)}»</p><cite>${E(nome(v.autore))}${v.giornata?' · '+v.giornata+'ª giornata':v.data?' · '+new Date(v.data).toLocaleDateString('it-IT',{day:'numeric',month:'long',timeZone:'Europe/Rome'}):''}</cite></blockquote>`:`<p class="gb-assente">${ND}</p>`;
  }
  function vociSquadra(s) {
    const v=s.voci||{};
    return `<div class="gb-voci">${voceHTML(v.redazione)}${voceHTML(v.curva?.[0],true)}</div><div class="gb-mini"><div><small>Derby</small><strong>${s.derby.disponibile?s.derby.giocate:ND}</strong><span>Giocati nel periodo</span></div><div><small>Champions Cup</small><strong>${s.coppa.punti_girone??'—'}</strong><span>Punti nel girone</span></div><div><small>Fiducia del presidente</small><strong>${s.dirigenza.fiducia??'—'}<small>/100</small></strong><span>${E(s.dirigenza.giudizio)}</span></div></div>`;
  }
  function tavole(prima,seconda) {
    return `<div class="gb-viste" aria-label="Le due pagine del bilancio"><button type="button" data-gb-vista="0" aria-pressed="true">1 · Colpo d’occhio</button><button type="button" data-gb-vista="1" aria-pressed="false">2 · Voci e bilancio</button></div><section class="gb-tavola" data-gb-pagina="0">${prima}</section><section class="gb-tavola" data-gb-pagina="1" hidden>${seconda}</section>`;
  }
  function scheda(s) {
    const kpi=`<div class="gb-kpi"><div><strong>${s.posizione}<small>ª</small></strong><span>Posizione</span></div><div><strong>${s.punti_classifica}</strong><span>Punti in classifica</span></div><div><strong>${s.bilancio.gol_fatti}<small> : ${s.bilancio.gol_subiti}</small></strong><span>Gol fatti : Subiti</span></div></div>`;
    const casa=[['In casa',s.casa],['In trasferta',s.trasferta]].map(([n,b])=>`<div><span>${n}</span><strong>${b.punti} punti</strong><div class="gb-barra"><i style="width:${b.giocate?100*b.punti/(3*b.giocate):0}%"></i></div><small>${b.giocate} partite</small></div>`).join('');
    return `<h3>${E(nome(s.squadra))}</h3>${tavole(kpi+`<div class="gb-riquadro"><h4>La corsa in classifica</h4>${traccia(s)}${legenda()}</div><div class="gb-riquadro"><h4>Le ultime partite</h4>${pallini(s.partite,7)}<p class="gb-bilancio"><b>${s.bilancio.vittorie}</b> Vittorie <b>${s.bilancio.pareggi}</b> Pareggi <b>${s.bilancio.sconfitte}</b> Sconfitte</p></div><div class="gb-casa">${casa}</div>`,vociSquadra(s))}<details class="gb-dati"><summary>Tutti i dati della squadra</summary>${dettagli(s)}</details>`;
  }
  function lega(p) {
    const c=p.campionato,prima=`<div class="gb-leader"><small>${c.campione_inverno?'Campione d’inverno':'In vetta'}</small><strong>${E(nome(c.campione_inverno||c.capolista))}</strong><span>${c.partite} partite · ${c.gol} gol nel periodo</span></div><div class="gb-classifica">${p.classifica.map(r=>`<div><b>${r.posizione}.</b><span>${E(nome(r.squadra))}<i class="gb-barra"><i style="width:${100*r.punti/Math.max(1,p.classifica[0].punti)}%"></i></i></span><strong>${r.punti}<small> punti</small></strong>${pallini(p.squadre[r.squadra].partite)}</div>`).join('')}</div>${legenda()}`;
    const v=p.voci||{},red=(v.redazione||[]).find(v=>v.squadra===c.capolista)||(v.redazione||[])[0];
    const seconda=`<div class="gb-voci">${voceHTML(red)}${voceHTML(v.curva?.[0],true)}</div><div class="gb-primati"><div><small>Miglior attacco</small><strong>${E(c.miglior_attacco.map(nome).join(', '))}</strong></div><div><small>Miglior difesa</small><strong>${E(c.miglior_difesa.map(nome).join(', '))}</strong></div></div>`;
    return `<h3>Il campionato</h3>${tavole(prima,seconda)}<div class="gb-tutte"><h4>Il dossier di ogni squadra</h4>${p.classifica.map(r=>`<details><summary>${E(nome(r.squadra))} · ${r.posizione}ª · ${r.punti} punti</summary>${dettagli(p.squadre[r.squadra])}</details>`).join('')}</div>`;
  }
  function stile() {
    if (document.getElementById('gb-stile')) return;
    const l = document.createElement('link'); l.id='gb-stile';l.rel='stylesheet';l.href=new URL('giro-di-boa.css',ROOT);document.head.append(l);
  }
  function opzioni(j) { return Object.keys(j.periodi).map(k=>`<option value="${k}"${k==='andata'?' selected':''}>${k==='andata'?'Girone d’andata':k==='ritorno'?'Girone di ritorno':'Fino ad ora'}</option>`).join(''); }
  async function monta(host, team, root = ROOT) {
    stile();host.classList.add('gb');host.classList.toggle('gb-stadio', /\/stadio\//.test(location.pathname));host.innerHTML='<p role="status">Preparo il bilancio…</p>';
    try {
      const j = await carica(root);
      if (!host.isConnected) return;
      host.innerHTML=`<header><small class="gb-versione">6.0.2 · Giro di boa</small><h2 data-gb-tit></h2><p>La tua squadra o tutto il campionato. Gli stessi fatti nelle immagini e in Radio.</p></header><div class="gb-controlli"><label>Contenuto<select data-gb-ambito><option value="squadra">La squadra</option><option value="lega">Tutto il campionato</option></select></label><label data-gb-scelta>Squadra<select data-gb-squadra>${j.periodi.finora.classifica.map(r=>`<option value="${E(r.squadra)}"${r.squadra===team?' selected':''}>${E(nome(r.squadra))}</option>`).join('')}</select></label><label>Periodo<select data-gb-periodo>${opzioni(j)}</select></label></div><button type="button" class="gb-bottone" data-gb-album>Prepara le due foto</button><div data-gb-contenuto></div><p class="gb-fonte">Dopo l’ultima giornata pubblicata. Posizione e punti sono quelli in classifica; i bilanci riguardano il periodo scelto. A pari punti valgono le regole del Tabellone. La zona retrocessione corrisponde all’ultimo posto.</p>`;
      const q = s=>host.querySelector(s);
      const precedente=scelte.get(team);
      if(precedente){for(const [sel,val] of Object.entries(precedente)){const el=q(sel);if([...el.options].some(o=>o.value===val))el.value=val;}}
      function aggiorna() {
        const k=q('[data-gb-periodo]').value,p=periodo(j,k),t=q('[data-gb-squadra]').value,all=q('[data-gb-ambito]').value==='lega';
        q('[data-gb-tit]').textContent=titolo(j,k);q('[data-gb-scelta]').hidden=all;
        q('[data-gb-contenuto]').innerHTML=all?lega(p):scheda(p.squadre[t]);
        const vista=viste.get(team)||'0';q('[data-gb-vista="'+vista+'"]')?.click();
        scelte.set(team,{'[data-gb-periodo]':k,'[data-gb-squadra]':t,'[data-gb-ambito]':all?'lega':'squadra'});
      }
      host.addEventListener('click',e=>{const b=e.target.closest('[data-gb-vista]');if(!b)return;const scope=b.closest('[data-gb-contenuto]');viste.set(team,b.dataset.gbVista);scope.querySelectorAll('[data-gb-vista]').forEach(v=>v.setAttribute('aria-pressed',String(v===b)));scope.querySelectorAll('[data-gb-pagina]').forEach(v=>v.hidden=v.dataset.gbPagina!==b.dataset.gbVista);});
      host.querySelectorAll('select').forEach(s=>s.addEventListener('change',aggiorna));aggiorna();
      q('[data-gb-album]').onclick=()=>apri({j,root,squadra:q('[data-gb-squadra]').value,ambito:q('[data-gb-ambito]').value,k:q('[data-gb-periodo]').value});
      host.dataset.pronto='1';
    } catch(e) { host.innerHTML=`<p role="status">${E(e.message)}</p><button type="button" class="gb-bottone">Riprova</button>`;host.querySelector('button').onclick=()=>monta(host,team,root); }
  }
  function linee(ctx, s, max) {
    const words=text(s).split(/\s+/),out=[];let line='';
    words.forEach(w=>{if(ctx.measureText((line?line+' ':'')+w).width>max&&line){out.push(line);line=w;}else line+=(line?' ':'')+w;});if(line)out.push(line);return out;
  }
  async function album(j,{k='finora',ambito='squadra',squadra,stadio=/\/stadio\//.test(location.pathname)||document.documentElement.dataset.skin==='stadio'}={}) {
    if(document.fonts?.ready)await document.fonts.ready;
    const p=periodo(j,k),s=p.squadre[squadra],c=p.campionato,files=[];
    if(ambito!=='lega'&&!s)throw Error('Squadra non disponibile nel bilancio');
    for(let idx=0;idx<2;idx++){
      const cv=document.createElement('canvas');cv.width=1080;cv.height=1350;
      const ctx=cv.getContext('2d'),accent=stadio?'#ffd166':'#ef5263',ink='#fbf6ec',mute='#b8cae6';
      const grad=ctx.createLinearGradient(0,0,1080,1350);grad.addColorStop(0,stadio?'#163d47':'#253b70');grad.addColorStop(1,'#111d35');ctx.fillStyle=grad;ctx.fillRect(0,0,1080,1350);
      // Motivo da campo, volutamente tenue dietro ai contenuti.
      ctx.strokeStyle='#ffffff08';ctx.lineWidth=2;ctx.strokeRect(780,60,240,220);ctx.beginPath();ctx.arc(900,170,55,0,Math.PI*2);ctx.stroke();
      function txt(t,x,y,size=28,col=ink,weight=600,max=960){ctx.textBaseline='top';ctx.fillStyle=col;ctx.font=`${weight} ${size}px Inter,system-ui,sans-serif`;ctx.fillText(text(t),x,y,max);}
      function wrap(t,x,y,width,size=30,col=ink,limit=8){ctx.font=`600 ${size}px Inter,system-ui,sans-serif`;const a=linee(ctx,t,width);if(a.length>limit)throw Error('Testo troppo lungo per la tavola');a.forEach((l,i)=>txt(l,x,y+i*(size+12),size,col,600,width));return y+a.length*(size+12);}
      function box(x,y,w,h){ctx.fillStyle='#ffffff0a';ctx.beginPath();if(ctx.roundRect)ctx.roundRect(x,y,w,h,stadio?24:[5,20,20,5]);else ctx.rect(x,y,w,h);ctx.fill();ctx.fillStyle=accent;ctx.fillRect(x,y,stadio?6:8,h);}
      function dot(es,x,y,r=20){ctx.fillStyle=COLORI[es];ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.textAlign='center';txt(es,x,y-r+5,r+3,'#11243a',900,r*2);ctx.textAlign='left';}
      function legend(y){[['V','Vittoria'],['N','Pareggio'],['P','Sconfitta']].forEach(([es,n],i)=>{dot(es,80+i*310,y+16,16);txt(n,110+i*310,y,23,mute);});}
      function quote(v,y,curva=false){box(60,y,960,curva?315:355);txt(curva?'DALLA CURVA':'GIRRR SPORT · REDAZIONE',90,y+25,23,accent,800);let at=y+70;
        if(v){if(v.titolo)at=wrap(v.titolo,90,at,900,29,ink,3)+12;at=wrap('«'+v.testo+'»',90,at,900,31,ink,6);txt(nome(v.autore)+(v.giornata?' · '+v.giornata+'ª giornata':v.data?' · '+new Date(v.data).toLocaleDateString('it-IT',{day:'numeric',month:'long',timeZone:'Europe/Rome'}):''),90,y+(curva?266:305),23,mute,600,890);}else txt(ND,90,at,31,mute);}
      txt('O FANT A GIRRR',60,44,24,accent,900);ctx.textAlign='right';txt(j.stagione,1020,44,24,mute,700);ctx.textAlign='left';
      txt(titolo(j,k),60,98,30,mute,700);
      const team=ambito==='lega'?'Tutto il campionato':nome(squadra);
      let titleSize=stadio?52:48,lines;do{ctx.font=stadio?titleSize+'px Lobster,cursive':'900 '+titleSize+'px Inter,system-ui';lines=linee(ctx,team,960);if(lines.length<=2)break;titleSize-=2;}while(titleSize>=28);if(lines.length>2)throw Error('Nome della squadra troppo lungo');ctx.fillStyle=ink;ctx.textBaseline='top';lines.forEach((v,i)=>ctx.fillText(v,60,152+i*53,960));
      txt(idx===0?'01 / IL COLPO D’OCCHIO':'02 / VOCI E BILANCIO',60,266,23,accent,800);
      if(idx===0&&ambito==='squadra'){
        [[s.posizione+'ª','Posizione'],[String(s.punti_classifica),'Punti in classifica'],[s.bilancio.gol_fatti+' : '+s.bilancio.gol_subiti,'Gol fatti : Subiti']].forEach(([v,n],i)=>{box(60+i*330,320,300,165);txt(v,84+i*330,340,v.length>5?63:85,ink,900,252);txt(n,84+i*330,442,21,mute,700,255);});
        txt('LA CORSA IN CLASSIFICA',60,532,23,mute,800);
        const a=s.andamento,x=i=>105+i*875/Math.max(1,a.length-1),y=pos=>605+(pos-1)*18;
        [1,5,10].forEach(pos=>{ctx.strokeStyle='#ffffff14';ctx.beginPath();ctx.moveTo(105,y(pos));ctx.lineTo(980,y(pos));ctx.stroke();txt(pos+'ª',60,y(pos)-12,20,mute);});
        ctx.beginPath();a.forEach((v,i)=>{if(i)ctx.lineTo(x(i),y(v.posizione));else ctx.moveTo(x(i),y(v.posizione));});ctx.strokeStyle='#c0dbed';ctx.lineWidth=4;ctx.stroke();
        a.forEach((v,i)=>{ctx.fillStyle=COLORI[s.partite.find(m=>m.giornata===v.giornata)?.esito]||accent;ctx.beginPath();ctx.arc(x(i),y(v.posizione),a.length>17?6:10,0,Math.PI*2);ctx.fill();});
        txt(a[0]?.giornata+'ª giornata',105,795,21,mute);ctx.textAlign='right';txt(a.at(-1)?.giornata+'ª giornata',980,795,21,mute);ctx.textAlign='left';
        txt('LE ULTIME CINQUE',60,858,23,mute,800);
        const recent=s.partite.slice(-5),ww=960/recent.length;
        recent.forEach((m,i)=>{const xx=60+i*ww;dot(m.esito,xx+24,933,23);txt(m.gol_fatti+'–'+m.gol_subiti,xx+60,910,38,ink,900,ww-64);txt(m.giornata+'ª · '+(m.casa?'Casa':'Fuori'),xx,976,20,mute,600,ww-12);});
        legend(1030);
        [['IN CASA',s.casa],['IN TRASFERTA',s.trasferta]].forEach(([n,b],i)=>{const xx=60+i*500;txt(n,xx,1110,22,mute,800);txt(b.punti+' punti',xx,1149,40,ink,800);txt(b.giocate+' partite',xx+230,1164,22,mute);ctx.fillStyle='#ffffff14';ctx.fillRect(xx,1215,460,10);ctx.fillStyle=accent;ctx.fillRect(xx,1215,b.giocate?460*b.punti/(3*b.giocate):0,10);});
      }else if(idx===0){
        box(60,320,960,100);txt(c.campione_inverno?'CAMPIONE D’INVERNO':'IN VETTA',85,340,20,accent,800);txt(nome(c.campione_inverno||c.capolista),85,372,31,ink,900,900);
        txt('SQUADRA',105,449,20,mute,800);txt('PUNTI',740,449,20,mute,800);txt('ULTIME 5',865,449,20,mute,800);
        p.classifica.forEach((r,i)=>{const yy=494+i*67;txt(r.posizione+'.',60,yy,26,mute,800);txt(nome(r.squadra),105,yy,28,ink,800,590);txt(r.punti,755,yy,30,ink,900,70);ctx.fillStyle='#ffffff12';ctx.fillRect(105,yy+40,585,4);ctx.fillStyle=accent;ctx.fillRect(105,yy+40,585*r.punti/Math.max(1,p.classifica[0].punti),4);p.squadre[r.squadra].partite.slice(-5).forEach((m,i)=>dot(m.esito,867+i*33,yy+15,13));});
        legend(1200);
      }else{
        const v=ambito==='lega'?p.voci||{}:s.voci||{},red=ambito==='lega'?(v.redazione||[]).find(v=>v.squadra===c.capolista)||(v.redazione||[])[0]:v.redazione;
        quote(red,320);quote(v.curva?.[0],710,true);
        if(ambito==='lega'){
          [['MIGLIOR ATTACCO',c.miglior_attacco],['MIGLIOR DIFESA',c.miglior_difesa]].forEach(([n,tt],i)=>{txt(n,60+i*500,1080,21,accent,800);wrap(tt.map(nome).join(', '),60+i*500,1122,450,27,ink,4);});
        }else{
          [['DERBY',s.derby.disponibile?s.derby.giocate:'—','Giocati'],['CHAMPIONS CUP',s.coppa.punti_girone??'—','Punti nel girone'],['FIDUCIA',s.dirigenza.fiducia??'—','Su 100']].forEach(([n,val,unita],i)=>{txt(n,60+i*330,1080,21,accent,800);txt(val,60+i*330,1122,64,ink,900);txt(unita,60+i*330,1201,22,mute);});
        }
      }
      ctx.strokeStyle='#ffffff25';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(60,1275);ctx.lineTo(1020,1275);ctx.stroke();txt('Campionato · Giornate '+p.dalla_giornata+'–'+p.alla_giornata,60,1300,21,mute);ctx.textAlign='right';txt((idx+1)+' / 2',1020,1300,21,mute);ctx.textAlign='left';
      const blob=await new Promise(ok=>cv.toBlob(ok,'image/png'));if(!blob)throw Error('Impossibile preparare la foto');
      const slug=(ambito==='lega'?'campionato':squadra).toLowerCase().replace(/[^a-z0-9]+/g,'-');files.push({file:new File([blob],`o-girrr-${slug}-${k}-${idx+1}.png`,{type:'image/png'}),url:URL.createObjectURL(blob),canvas:cv});
    }
    return files;
  }
  async function apri(o={}) {
    stile();const focus=document.activeElement,d=document.createElement('dialog');d.className='gb gb-dialogo'+(/\/stadio\//.test(location.pathname)?' gb-stadio':'');d.setAttribute('aria-label','Condividi il bilancio');
    d.innerHTML='<button class="gb-bottone gb-chiudi" type="button">Chiudi ×</button><h2>Le due foto per il gruppo</h2><p role="status">Preparo l’album…</p>';document.body.append(d);d.showModal();
    let files=[];const clean=()=>{files.forEach(v=>URL.revokeObjectURL(v.url));d.remove();focus?.focus();};d.addEventListener('close',clean);d.querySelector('button').onclick=()=>d.close();
    try {
      const j=o.j||await carica(o.root||ROOT),k=o.k||(j.periodi.andata?'andata':'finora'),sq=o.squadra||j.periodi.finora.classifica[0].squadra;
      const area=document.createElement('div');area.innerHTML=`<div class="gb-controlli"><label>Contenuto<select data-gb-a><option value="squadra">La squadra</option><option value="lega">Tutto il campionato</option></select></label><label>Periodo<select data-gb-k>${opzioni(j)}</select></label></div><div class="gb-album"></div><div class="gb-azioni"></div>`;d.append(area);area.querySelector('[data-gb-a]').value=o.ambito||'squadra';area.querySelector('[data-gb-k]').value=k;
      let seq=0;
      async function aggiorna() {
        const current=++seq,status=d.querySelector('[role=status]'),az=area.querySelector('.gb-azioni');az.innerHTML='';status.textContent='Preparo l’album…';
        const nuovi=await album(j,{k:area.querySelector('[data-gb-k]').value,ambito:area.querySelector('[data-gb-a]').value,squadra:sq});
        if(!d.isConnected||current!==seq){nuovi.forEach(v=>URL.revokeObjectURL(v.url));return;}
        files.forEach(v=>URL.revokeObjectURL(v.url));files=nuovi;
        area.querySelector('.gb-album').innerHTML=files.map((v,i)=>`<figure><a href="${v.url}" target="_blank" rel="noopener" aria-label="Apri grande la foto ${i+1}"><img src="${v.url}" alt="Foto ${i+1} di 2 del bilancio"></a><figcaption>Foto ${i+1} di 2</figcaption><a class="gb-bottone" href="${v.url}" download="${v.file.name}">Scarica foto ${i+1}</a></figure>`).join('');
        status.textContent='Due foto insieme, senza testo aggiunto.';
        const condivisibili=files.map(v=>v.file);
        if(navigator.share&&navigator.canShare?.({files:condivisibili})) {
          const b=document.createElement('button');b.type='button';b.className='gb-bottone';b.textContent='Condividi le due foto';b.dataset.gbInvia='1';az.append(b);
          b.onclick=()=>navigator.share({files:condivisibili}).catch(e=>{if(e.name!=='AbortError')status.textContent='Condivisione non riuscita. Puoi scaricare le foto.';});
        } else status.textContent='Due foto pronte. Su questo browser puoi scaricarle una per una.';
      }
      area.querySelectorAll('select').forEach(s=>s.onchange=()=>aggiorna().catch(e=>{d.querySelector('[role=status]').textContent=e.message;}));await aggiorna();
    }catch(e){if(d.isConnected)d.querySelector('[role=status]').textContent=e.message;}
  }
  window.GirrrBoa={carica,titolo,periodo,sezioni,scheda,lega,album,apri,monta};
  window.GirrrGiroDiBoa=t=>'<section class="gb" data-gb-host data-gb-team="'+E(t)+'"><p role="status">Preparo il bilancio…</p></section>';
  const mount=()=>document.querySelectorAll('[data-gb-host]:not([data-gb-montato])').forEach(h=>{h.dataset.gbMontato='1';monta(h,h.dataset.gbTeam);});
  new MutationObserver(mount).observe(document.documentElement,{childList:true,subtree:true});mount();
  if (new URLSearchParams(location.search).get('boa')==='1') document.querySelector('[data-ctab=boa]')?.click();
})();
