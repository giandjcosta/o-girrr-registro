// Attende soltanto un server locale; non invia scritture.
(async()=>{const url=process.argv[2];if(!['127.0.0.1','localhost'].includes(new URL(url).hostname))throw Error('Solo server locale');for(let i=0;i<120;i++){try{if((await fetch(url)).ok)return}catch(e){}await new Promise(r=>setTimeout(r,250))}throw Error('Il server locale non è pronto')})().catch(e=>{console.error(e);process.exit(1)});
