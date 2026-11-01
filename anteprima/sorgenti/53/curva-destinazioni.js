/* Ponte di sola navigazione, incluso nella chiusura della Curva dalla build. */
window.OGCurva55={
 get:function(){return {ready:!!D&&NET!==null,posts:POSTS,replies:S.replies||[],more:FEED_MORE}},
 open:function(pk,rid){
  var p=POSTS.find(function(p){return p.k===pk});if(!p)return false;
  if(rid&&!(p.r||[]).some(function(r){return r.real&&String(r.id)===String(rid)}))return false;
  vprof=p.a;vista='u';edit=false;ptab='cori';open[pk]=true;render();
  return !!document.querySelector(rid?'[data-risposta="'+rid+'"]':'article.post[data-k="'+pk+'"]');
 },
 older:function(){
  if(!S.posts.length)return Promise.resolve(false);
  var oldest=Math.min.apply(null,S.posts.map(function(p){return p.ts}));
  return rpc('curva_feed',{p_team:me,p_code:me?code:null,p_limit:150,p_before:oldest}).then(function(f){
   if(!f||!Array.isArray(f.posts))throw Error('Archivio non disponibile');
   var seen={},added=0;S.posts.forEach(function(p){seen[p.id]=1});
   f.posts.forEach(function(p){if(!seen[p.id]){S.posts.push(p);seen[p.id]=1;added++}});
   var rr={};(S.replies||[]).forEach(function(r){rr[r.id]=1});
   (f.replies||[]).forEach(function(r){if(!rr[r.id]){S.replies.push(r);rr[r.id]=1}});
   FEED_MORE=f.posts.length===150&&added>0;render();return added>0;
  });
 }
};
