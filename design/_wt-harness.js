/* TEMPORARY measurement harness -- not part of the app or the walkthrough layer.
   Served alongside demo-app.html during a round and deleted before the round lands. */
window.__H={
 sleep:function(ms){return new Promise(function(r){setTimeout(r,ms)})},
 rb:function(e){ if(!e) return null; var r=e.getBoundingClientRect(); if(!r.width||!r.height) return null;
   return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2)}; },
 ov:function(a,b){ if(!a||!b) return 0; var w=Math.max(0,Math.min(a.r,b.r)-Math.max(a.x,b.x)); var h=Math.max(0,Math.min(a.b,b.b)-Math.max(a.y,b.y)); return +(w*h).toFixed(0); },
 settle:async function(ms){ var H=this,t=Date.now(),last='',n=0;
   while(Date.now()-t<ms){ var on=document.getElementById('wt-ring').classList.contains('on');
     var st=document.getElementById('wt-call').getAttribute('style')||'';
     if(on&&st===last){ if(++n>=3) return true; } else n=0;
     last=st; await H.sleep(90); }
   return false; },
 snap:function(tag){ var H=this, D=document, st=window.WT.step();
   var call=H.rb(D.getElementById('wt-call')), ring=H.rb(D.getElementById('wt-ring'));
   var p=D.getElementById('phone').getBoundingClientRect();
   var f={x:p.left,y:p.top,r:p.right,b:p.bottom};
   var clip=call? +(Math.max(f.x-call.x,0)+Math.max(call.r-f.r,0)+Math.max(f.y-call.y,0)+Math.max(call.b-f.b,0)).toFixed(2):0;
   var ringOn=D.getElementById('wt-ring').classList.contains('on');
   var tgtNode=st.sel?D.querySelector(st.sel):null;
   var content=[];
   D.querySelectorAll('.sheet.on').forEach(function(sh){
     sh.querySelectorAll('.sheet-scroll > *').forEach(function(n){
       if(tgtNode&&(n===tgtNode||n.contains(tgtNode))) return;
       var b=H.rb(n); if(!b) return; var o=H.ov(call,b);
       if(o>0) content.push({sel:sh.id+' .'+(n.className||n.tagName),t:(n.textContent||'').trim().replace(/\s+/g,' ').slice(0,30),ov:o,frac:+(o/(b.w*b.h)).toFixed(3)});
     });});
   var rec={tag:tag,sel:st.sel,scr:(D.querySelector('.screen.active')||{}).id,title:D.getElementById('wt-title').textContent,
     call:call?[call.x,call.y,call.w,call.h]:null, ring:ring?[ring.x,ring.y,ring.w,ring.h]:null, ringOn:ringOn,
     clip:clip, ringOv:ringOn?H.ov(call,ring):0, navOv:H.ov(call,H.rb(D.querySelector('#navbar'))),
     arrow:getComputedStyle(D.getElementById('wt-arrow')).display, cls:D.getElementById('wt-call').className, content:content};
   window.__rec.push(rec);
   try{ var L=JSON.parse(sessionStorage.getItem('__wtlog')||'[]'); L.push(rec); sessionStorage.setItem('__wtlog',JSON.stringify(L)); }catch(e){}
   return rec; },
 click:function(s){ var e=document.querySelector(s); if(e){e.click();return true;} return false; },
 key:function(){ var s=window.WT.step(); return s.step+'.'+s.target; },
 waitStep:async function(from,ms){ var H=this,t=Date.now(); while(Date.now()-t<ms){ if(H.key()!==from) return true; await H.sleep(70);} return false; },
 /* advance the route by one stop, doing whatever that stop needs */
 act:async function(){ var H=this,s=window.WT.step();
   if(s.step===10){ await H.sleep(9200); return; }
   if(s.step===2&&s.target===1){ H.click('#ob-persona-grid .persona'); await H.sleep(400); return; }
   if((s.step===4&&s.target===2)||(s.step===5&&s.target===1)){ H.click('#card-grip'); await H.sleep(700); return; }
   if(s.sel) H.click(s.sel); await H.sleep(600); },
 run:async function(stops){ var H=this,out=[];
   for(var n=0;n<stops;n++){
     var k=H.key(); await H.settle(4000); out.push(H.snap(k));
     try{sessionStorage.setItem('__wtat',k)}catch(e){}
     await H.act(); var moved=await H.waitStep(k,8000);
     if(!moved){ out.push({tag:'STUCK '+k}); break; }
     var s=window.WT.step(); if(s.step===12&&s.target===2){ await H.settle(4000); out.push(H.snap('12.2')); break; }
   }
   return out; },
 nocam:function(){ try{ if(navigator.mediaDevices) navigator.mediaDevices.getUserMedia=function(){return Promise.reject(new Error('harness: denied'))}; }catch(e){}
   try{ Object.defineProperty(navigator,'mediaDevices',{configurable:true,value:{getUserMedia:function(){return Promise.reject(new Error('harness: denied'))},enumerateDevices:function(){return Promise.resolve([])}}}); }catch(e){} },
 boot:async function(){ var H=this; H.nocam();
   if((document.querySelector('.screen.active')||{}).id==='splash'){ document.getElementById('splash').click(); await H.sleep(1400); }
   window.__rec=[]; return (document.querySelector('.screen.active')||{}).id; }
};
window.__rec=[];

/* ---- synthesized finger, for the drag/fold checks ---- */
window.__G={
  pe:function(t,x,y,id){ return new PointerEvent(t,{pointerId:id||7,pointerType:'touch',isPrimary:true,
      bubbles:true,cancelable:true,clientX:x,clientY:y,button:0,buttons:(t==='pointerup')?0:1}); },
  /* grab the card at (fx,fy) inside it and finish at +dx,+dy, in n steps */
  drag:async function(dx,dy,n){ var c=document.getElementById('wt-call'), r=c.getBoundingClientRect();
    var sx=r.left+Math.min(40,r.width/2), sy=r.top+Math.min(20,r.height/2); n=n||6;
    c.dispatchEvent(this.pe('pointerdown',sx,sy));
    for(var k=1;k<=n;k++){ c.dispatchEvent(this.pe('pointermove',sx+dx*k/n,sy+dy*k/n)); await window.__H.sleep(16); }
    c.dispatchEvent(this.pe('pointerup',sx+dx,sy+dy));
    await window.__H.sleep(120); },
  tap:async function(jitter){ var c=document.getElementById('wt-call'), r=c.getBoundingClientRect();
    var sx=r.left+r.width/2, sy=r.top+r.height/2; jitter=jitter||0;
    c.dispatchEvent(this.pe('pointerdown',sx,sy));
    c.dispatchEvent(this.pe('pointermove',sx+jitter,sy+jitter));
    c.dispatchEvent(this.pe('pointerup',sx+jitter,sy+jitter));
    await window.__H.sleep(120); },
  state:function(){ var c=document.getElementById('wt-call');
    return {box:window.WT.box(), cls:c.className, step:window.WT.step(),
            arrow:getComputedStyle(document.getElementById('wt-arrow')).display,
            arrowLeft:document.getElementById('wt-arrow').style.left,
            ring:document.getElementById('wt-ring').style.cssText}; }
};
