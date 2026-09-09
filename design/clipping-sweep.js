/* ============================================================================
   THE CLIPPING SWEEP, WITH ITS BLIND SPOTS WRITTEN DOWN.
   Round 14 (frontdoor #458). Paste into the console with a screen active, or
   drive it over every screen x text step x contrast mode x frame from a driver.

   WHY IT EXISTS AS A FILE. Round 11 ran 1,300 screen-scans and reported ZERO
   clipped text nodes. The result was true and the conclusion was wrong: it
   compared each element's own scrollWidth to its own clientWidth, which can only
   see an element clipping ITSELF. The capture coach fitted its own box perfectly
   and was cut 25.1px each side by its PARENT, on every frame, at the 200% text
   step, for three rounds. A sweep whose blind spot is unrecorded gets cited as
   evidence of something it cannot establish, so the method and its limits live
   here rather than in a round report.

   THE METHOD. For every element in the active screen that carries a non-empty
   direct text child and is visible:
     - the OLD statistic is still reported (selfX / selfY), so the two methods can
       be compared on the same node;
     - and per axis, walk the ancestors to the FIRST one whose overflow is not
       `visible`:
         auto | scroll  -> the content is reachable by scrolling. NOT a clip.
         hidden | clip  -> the content is unreachable. A clip, measured against
                           that ancestor's PADDING box, in px on each side.
     Walking past a scroller would report every below-the-fold row in the app as
     clipped; not walking at all is Round 11's bug. Stopping at the first
     non-visible overflow is the only rule that does neither.

   WHAT IT STILL CANNOT SEE, stated so the next round does not have to find out:
     1. GRAPHICS. It looks at text nodes. An <svg> or an <img> clipped by an
        ancestor is invisible to it. Round 14 found the welcome wordmark clipped
        14.2-72.7px at the bottom by .wl-hero at the large text steps -- BY HAND,
        while investigating the .wl-tag finding this sweep did report. A graphic
        sweep is a separate tool and does not exist yet.
     2. TIMING. Anything painted behind a transition or a setTimeout is measured
        in whatever state it is in when the sweep runs. The capture coach swaps
        its text on a 160ms timer and is opacity:0 until then; at a 60ms settle
        this sweep reported nothing at all on that screen. 320ms is the settle
        that finds it. A sweep with the wrong settle reports a clean build.
     3. TRANSFORMS AND STICKY. getBoundingClientRect is post-transform on both the
        node and the clipper, which is right for a translation and wrong for a
        rotation. Nothing in this build rotates a clipper.
     4. It says nothing about whether a clipped node MATTERS. .sr-only is a
        deliberate 1px clip and is flagged and labelled, not excluded.
   ========================================================================== */
(function(){
  const TOL = 0.5;
  const phone = document.getElementById('phone');
  const out = [];
  const root = document.querySelector('.screen.active');
  if(!root) return out;

  function cname(el){
    const c = el.className;
    const s = (c && c.baseVal!==undefined) ? c.baseVal : (''+(c||''));
    return (el.id?'#'+el.id:'') + (s.trim()? '.'+s.trim().split(/\s+/).join('.') : '');
  }
  function ownText(el){
    let t='';
    for(const n of el.childNodes) if(n.nodeType===3) t += n.nodeValue;
    return t.replace(/\s+/g,' ').trim();
  }
  function isSrOnly(el){
    for(let n=el; n && n!==phone; n=n.parentElement)
      if(n.classList && n.classList.contains('sr-only')) return true;
    return false;
  }
  function clippers(el){
    const res = {x:null, y:null};
    for(let n=el.parentElement; n; n=n.parentElement){
      const cs = getComputedStyle(n);
      if(res.x===null && cs.overflowX!=='visible')
        res.x = (cs.overflowX==='hidden'||cs.overflowX==='clip') ? n : false;
      if(res.y===null && cs.overflowY!=='visible')
        res.y = (cs.overflowY==='hidden'||cs.overflowY==='clip') ? n : false;
      if(res.x!==null && res.y!==null) break;
      if(n===document.documentElement) break;
    }
    return {x: res.x||null, y: res.y||null};
  }
  function padBox(n){
    const r = n.getBoundingClientRect();
    const cs = getComputedStyle(n);
    return {left:  r.left  + (parseFloat(cs.borderLeftWidth)||0),
            right: r.right - (parseFloat(cs.borderRightWidth)||0),
            top:   r.top   + (parseFloat(cs.borderTopWidth)||0),
            bottom:r.bottom- (parseFloat(cs.borderBottomWidth)||0)};
  }

  root.querySelectorAll('*').forEach(el=>{
    if(el.tagName==='SCRIPT'||el.tagName==='STYLE') return;
    const txt = ownText(el);
    if(!txt) return;
    if(el.checkVisibility && !el.checkVisibility({checkOpacity:true, contentVisibilityAuto:true, visibilityProperty:true})) return;
    const r = el.getBoundingClientRect();
    if(r.width < 0.5 && r.height < 0.5) return;

    const rec = {screen: root.id, sel: cname(el), tag: el.tagName.toLowerCase(),
                 text: txt.slice(0,60), srOnly: isSrOnly(el),
                 w:+r.width.toFixed(1), h:+r.height.toFixed(1),
                 selfX:+(el.scrollWidth - el.clientWidth).toFixed(1),
                 selfY:+(el.scrollHeight - el.clientHeight).toFixed(1),
                 cutL:0,cutR:0,cutT:0,cutB:0,byX:null,byY:null};
    const c = clippers(el);
    if(c.x){ const b=padBox(c.x);
      rec.cutL=+Math.max(0,b.left-r.left).toFixed(1);
      rec.cutR=+Math.max(0,r.right-b.right).toFixed(1);
      if(rec.cutL>TOL||rec.cutR>TOL) rec.byX=cname(c.x); }
    if(c.y){ const b=padBox(c.y);
      rec.cutT=+Math.max(0,b.top-r.top).toFixed(1);
      rec.cutB=+Math.max(0,r.bottom-b.bottom).toFixed(1);
      if(rec.cutT>TOL||rec.cutB>TOL) rec.byY=cname(c.y); }
    const anc = !!(rec.byX||rec.byY);
    const slf = rec.selfX>TOL || rec.selfY>TOL;
    if(anc||slf){ rec.kindAnc=anc; rec.kindSelf=slf; out.push(rec); }
  });
  return out;
})()
