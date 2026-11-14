/* O Girrr · Giro di boa 6.0.2. Pagina e album leggono il calcolo del workflow.
   Qui si impaginano fatti già calcolati: nessuna classifica ricostruita nel browser. */
(function () {
  'use strict';
  if (window.GirrrBoa) return;
  const script = document.currentScript;
  const ROOT = new URL('./', script.src).href;
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
  function scheda(s) {
    return `<h3>${E(nome(s.squadra))}</h3><div class="gb-fatti">${sezioni(s).map(([a,b])=>`<div><h4>${a}</h4><p>${E(b)}</p></div>`).join('')}</div>
      <details open><summary>Andamento in classifica</summary>${andamento(s)}</details>
      <details><summary>Tutte le partite di Campionato</summary><ul>${s.partite.map(p=>`<li>${E(match(p))} · ${p.casa?'In casa':'In trasferta'}</li>`).join('')}</ul></details>
      <details><summary>Risultati dei Derby</summary><p>${E(s.derby.criterio)}</p><ul>${s.derby.disponibile ? s.derby.partite.map(p=>`<li>${E(p.nome_derby)} · ${E(match(p))}</li>`).join('') || '<li>Nessun Derby giocato</li>' : '<li>'+ND+'</li>'}</ul></details>
      <details><summary>Percorso in Champions Cup</summary><ul>${s.coppa.partite.map(p=>`<li>${E(match(p))} · ${E(p.gruppo)}</li>`).join('') || '<li>Nessuna partita nel periodo</li>'}</ul></details>
      <details><summary>Le conferenze</summary><ul>${s.promesse.disponibile ? s.promesse.partite.map(p=>`<li>${p.giornata}ª giornata: ${E(p.promessa)} · ${{v:'Mantenuta',s:'Pari',p:'Tradita'}[p.esito]||'Da valutare'}</li>`).join('') || '<li>Nessuna promessa conservata nel periodo</li>' : '<li>'+ND+'</li>'}</ul></details>
      <details><summary>I numeri</summary><p>Totale: ${N(s.numeri.totali)} Fantapunti · Media: ${N(s.numeri.media)} Fantapunti<br>Sul filo: scarto in Fantapunti non superiore a ${N(s.numeri.soglia_sul_filo_fantapunti)}, con un gol di differenza.</p><ul>${s.sul_filo.map(p=>`<li>${E(match(p))} · ${N(p.fantapunti)} contro ${N(p.fantapunti_avversario)} Fantapunti</li>`).join('') || '<li>Nessuna partita entro la soglia</li>'}</ul></details>`;
  }
  function lega(p) {
    const c = p.campionato;
    return `<h3>Il campionato</h3><p class="gb-lead">${c.campione_inverno ? 'Campione d’inverno: ' : 'In vetta: '}${E(nome(c.campione_inverno||c.capolista))}</p><p>${c.partite} partite · ${c.gol} gol del risultato</p><div class="gb-classifica">${p.classifica.map(r=>`<div><b>${r.posizione}.</b><span>${E(nome(r.squadra))}</span><strong>${r.punti}<small> punti</small></strong><small>${r.gol_fatti} GF / ${r.gol_subiti} GS</small></div>`).join('')}</div><p>Miglior attacco: ${E(c.miglior_attacco.map(nome).join(', '))}<br>Miglior difesa: ${E(c.miglior_difesa.map(nome).join(', '))}</p><p>Sopra le attese: ${E(c.sopra_le_attese.map(nome).join(', ')||'Nessuna squadra di almeno due posizioni')}<br>Sotto le attese: ${E(c.sotto_le_attese.map(nome).join(', ')||'Nessuna squadra di almeno due posizioni')}</p><div class="gb-tutte">${p.classifica.map(r=>`<details><summary>${E(nome(r.squadra))} · ${r.posizione}ª · ${r.punti} punti</summary>${scheda(p.squadre[r.squadra])}</details>`).join('')}</div>`;
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
      host.innerHTML=`<header><small class="gb-versione">6.0.2 · Giro di boa</small><h2 data-gb-tit></h2><p>La tua squadra o tutto il campionato. Gli stessi fatti nelle immagini e in Radio.</p></header><div class="gb-controlli"><label>Contenuto<select data-gb-ambito><option value="squadra">La squadra</option><option value="lega">Tutto il campionato</option></select></label><label data-gb-scelta>Squadra<select data-gb-squadra>${j.periodi.finora.classifica.map(r=>`<option value="${E(r.squadra)}"${r.squadra===team?' selected':''}>${E(nome(r.squadra))}</option>`).join('')}</select></label><label>Periodo<select data-gb-periodo>${opzioni(j)}</select></label></div><button type="button" class="gb-bottone" data-gb-album>Prepara le tre foto</button><div data-gb-contenuto></div><p class="gb-fonte">Dopo l’ultima giornata pubblicata. Posizione e punti sono quelli in classifica; i bilanci riguardano il periodo scelto. A pari punti valgono le regole del Tabellone. La zona retrocessione corrisponde all’ultimo posto.</p>`;
      const q = s=>host.querySelector(s);
      const precedente=scelte.get(team);
      if(precedente){for(const [sel,val] of Object.entries(precedente)){const el=q(sel);if([...el.options].some(o=>o.value===val))el.value=val;}}
      function aggiorna() {
        const k=q('[data-gb-periodo]').value,p=periodo(j,k),t=q('[data-gb-squadra]').value,all=q('[data-gb-ambito]').value==='lega';
        q('[data-gb-tit]').textContent=titolo(j,k);q('[data-gb-scelta]').hidden=all;
        q('[data-gb-contenuto]').innerHTML=all?lega(p):scheda(p.squadre[t]);
        scelte.set(team,{'[data-gb-periodo]':k,'[data-gb-squadra]':t,'[data-gb-ambito]':all?'lega':'squadra'});
      }
      host.querySelectorAll('select').forEach(s=>s.addEventListener('change',aggiorna));aggiorna();
      q('[data-gb-album]').onclick=()=>apri({j,root,squadra:q('[data-gb-squadra]').value,ambito:q('[data-gb-ambito]').value,k:q('[data-gb-periodo]').value});
      host.dataset.pronto='1';
    } catch(e) { host.innerHTML=`<p role="status">${E(e.message)}</p><button type="button" class="gb-bottone">Riprova</button>`;host.querySelector('button').onclick=()=>monta(host,team,root); }
  }
  function righeAlbum(j, k, ambito, team) {
    const p=periodo(j,k),s=p.squadre[team],c=p.campionato;
    if (ambito==='lega') {
      const tavola=[['La corsa',`${c.campione_inverno?'Campione d’inverno':'Capolista'}: ${nome(c.campione_inverno||c.capolista)}`],...p.classifica.map(r=>[`${r.posizione}. ${nome(r.squadra)}`,`${r.punti} punti · ${r.gol_fatti} gol fatti · ${r.gol_subiti} subiti`]),['I primati',`Attacco: ${c.miglior_attacco.map(nome).join(', ')}. Difesa: ${c.miglior_difesa.map(nome).join(', ')}.`]];
      const storie=p.classifica.map(r=>{const t=p.squadre[r.squadra];return [nome(r.squadra),`${B(t.bilancio)}. ${t.dirigenza.giudizio}; attesa ${t.dirigenza.attesa??ND}ª. Fiducia: ${N(t.dirigenza.fiducia)}. Champions Cup: ${t.coppa.qualificazione}. Derby: ${t.derby.disponibile?t.derby.giocate+' giocati':ND}. MVP: ${t.mvp.disponibile?t.mvp.ricevuti:ND}.`];});
      return [{tit:'La classifica',righe:tavola},{tit:'Cinque storie',righe:storie.slice(0,5)},{tit:'Altre cinque storie',righe:storie.slice(5)}];
    }
    if (!s) throw new Error('Squadra non disponibile nel bilancio');
    const all=sezioni(s);
    return [
      {tit:'La stagione',righe:all.slice(0,12)},
      {tit:'Le storie',righe:[...all.slice(12),['Derby, risultati',s.derby.disponibile?s.derby.partite.slice(0,3).map(match).join('; ') + (s.derby.partite.length>3?' · Tutti i risultati nella scheda':'')||'Nessun Derby giocato':ND],['I numeri',`${N(s.numeri.totali)} Fantapunti totali · ${N(s.numeri.media)} Fantapunti di media · Soglia sul filo: ${N(s.numeri.soglia_sul_filo_fantapunti)} Fantapunti`]]},
      {tit:'Partita per partita',righe:s.partite.map(p=>[`${p.giornata}ª · ${p.casa?'Casa':'Trasferta'} · ${p.gol_fatti}-${p.gol_subiti} (${p.esito})`,nome(p.avversario)])}
    ];
  }
  function linee(ctx, s, max) {
    const words=text(s).split(/\s+/),out=[];let line='';
    words.forEach(w=>{if(ctx.measureText((line?line+' ':'')+w).width>max&&line){out.push(line);line=w;}else line+=(line?' ':'')+w;});if(line)out.push(line);return out;
  }
  async function album(j,{k='finora',ambito='squadra',squadra,stadio=/\/stadio\//.test(location.pathname)||document.documentElement.dataset.skin==='stadio'}={}) {
    if(document.fonts?.ready) await document.fonts.ready;
    const pagine=righeAlbum(j,k,ambito,squadra),files=[];
    for(let idx=0;idx<pagine.length;idx++) {
      const page=pagine[idx],cv=document.createElement('canvas');cv.width=1080;cv.height=1350;
      const ctx=cv.getContext('2d'),accent=stadio?'#ffd166':'#d62839',colonna=page.righe.length>14;
      const g=ctx.createLinearGradient(0,0,700,1350);g.addColorStop(0,'#2c3f7c');g.addColorStop(1,'#141d3d');ctx.fillStyle=g;ctx.fillRect(0,0,1080,1350);
      ctx.fillStyle=accent;ctx.beginPath();if(stadio&&ctx.roundRect)ctx.roundRect(0,0,12,1350,[0,12,12,0]);else ctx.rect(0,0,16,1350);ctx.fill();
      ctx.textBaseline='top';ctx.fillStyle='#bfe3ff';ctx.font='800 24px Inter, system-ui';ctx.fillText('O FANT A GIRRR · '+j.stagione.toUpperCase(),60,45);
      ctx.fillStyle='#fbf6ec';let ts=44;const title=titolo(j,k);while(ts>28){ctx.font=`900 ${ts}px Inter, system-ui`;if(ctx.measureText(title).width<=960)break;ts-=2;}ctx.fillText(title,60,90);
      ctx.font=stadio?'42px Lobster, cursive':'900 36px Inter, system-ui';ctx.fillStyle='#ffd166';
      const top=ambito==='lega'?'Tutto il campionato':nome(squadra);ctx.fillText(top,60,155,960);
      ctx.font='700 26px Inter, system-ui';ctx.fillStyle='#bfe3ff';ctx.fillText(page.tit+' · '+(idx+1)+'/3',60,213);
      const rows=page.righe,cols=colonna?[rows.slice(0,Math.ceil(rows.length/2)),rows.slice(Math.ceil(rows.length/2))]:[rows],width=colonna?450:960;
      for(let ci=0;ci<cols.length;ci++) {
        let size=colonna?30:38,measure=[];
        for(;size>=20;size--) {
          measure=cols[ci].map(([a,b])=>{ctx.font=`800 ${size}px Inter, system-ui`;const aa=linee(ctx,a,width-36);ctx.font=`600 ${size}px Inter, system-ui`;return {a:aa,b:linee(ctx,b,width-36)};});
          if(measure.reduce((v,r)=>v+(colonna?4:18)+(r.a.length+r.b.length)*(size+6),0)<=1010)break;
        }
        if(size<20)throw new Error('I contenuti dell’album richiedono una revisione di impaginazione');
        let y=270;const x=60+ci*510;
        measure.forEach(r=>{ctx.fillStyle=accent;ctx.fillRect(x,y,stadio?6:8,Math.max(48,(r.a.length+r.b.length)*(size+6)));ctx.fillStyle='#ffd166';ctx.font=`800 ${size}px Inter, system-ui`;r.a.forEach(v=>{ctx.fillText(v,x+20,y,width-24);y+=size+6;});ctx.fillStyle='#fbf6ec';ctx.font=`600 ${size}px Inter, system-ui`;r.b.forEach(v=>{ctx.fillText(v,x+20,y,width-24);y+=size+6;});y+=colonna?4:18;});
      }
      ctx.fillStyle='#bfe3ff';ctx.font='600 20px Inter, system-ui';ctx.fillText('Campionato · Giornate '+periodo(j,k).dalla_giornata+'–'+periodo(j,k).alla_giornata+' · Risultati ufficiali',60,1304);
      const blob=await new Promise(ok=>cv.toBlob(ok,'image/png'));if(!blob)throw new Error('Impossibile preparare la foto');
      const slug=(ambito==='lega'?'campionato':squadra).toLowerCase().replace(/[^a-z0-9]+/g,'-');
      files.push({file:new File([blob],`o-girrr-${slug}-${k}-${idx+1}.png`,{type:'image/png'}),url:URL.createObjectURL(blob),canvas:cv});
    }
    return files;
  }
  async function apri(o={}) {
    stile();const focus=document.activeElement,d=document.createElement('dialog');d.className='gb gb-dialogo'+(/\/stadio\//.test(location.pathname)?' gb-stadio':'');d.setAttribute('aria-label','Condividi il bilancio');
    d.innerHTML='<button class="gb-bottone gb-chiudi" type="button">Chiudi ×</button><h2>Le tre foto per il gruppo</h2><p role="status">Preparo l’album…</p>';document.body.append(d);d.showModal();
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
        area.querySelector('.gb-album').innerHTML=files.map((v,i)=>`<figure><a href="${v.url}" target="_blank" rel="noopener" aria-label="Apri grande la foto ${i+1}"><img src="${v.url}" alt="Foto ${i+1} di 3 del bilancio"></a><figcaption>Foto ${i+1} di 3</figcaption><a class="gb-bottone" href="${v.url}" download="${v.file.name}">Scarica foto ${i+1}</a></figure>`).join('');
        status.textContent='Tre foto insieme, senza testo aggiunto.';
        const condivisibili=files.map(v=>v.file);
        if(navigator.share&&navigator.canShare?.({files:condivisibili})) {
          const b=document.createElement('button');b.type='button';b.className='gb-bottone';b.textContent='Condividi le tre foto';b.dataset.gbInvia='1';az.append(b);
          b.onclick=()=>navigator.share({files:condivisibili}).catch(e=>{if(e.name!=='AbortError')status.textContent='Condivisione non riuscita. Puoi scaricare le foto.';});
        } else status.textContent='Tre foto pronte. Su questo browser puoi scaricarle una per una.';
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
