"""Accessibility and interaction checks for the walkthrough layer.
Temporary tooling for the walkthrough round.

  py design/_wt-a11y.py [--w 390] [--h 844] [--rm] [--hc] [--ts double]
"""
import argparse, json
from playwright.sync_api import sync_playwright

AP = argparse.ArgumentParser()
AP.add_argument('--w', type=int, default=390)
AP.add_argument('--h', type=int, default=844)
AP.add_argument('--rm', action='store_true')
AP.add_argument('--hc', action='store_true')
AP.add_argument('--ts', default='')
A = AP.parse_args()

HARNESS = open('C:/dev/curb-appeal/design/_wt-measure.js', encoding='utf-8').read()

PROBE = r"""
() => {
  const D = document, out = {};
  const g = id => D.getElementById(id);
  const cs = n => n ? getComputedStyle(n) : null;
  const call = g('wt-call'), fold = g('wt-fold'), ring = g('wt-ring'), line = g('wt-line');
  out.pe = {
    wt: cs(g('wt')).pointerEvents,
    call: cs(call).pointerEvents,
    fold: cs(fold).pointerEvents,
    ring: cs(ring).pointerEvents,
    prog: cs(g('wt-prog')).pointerEvents,
    hud: cs(g('wt-hud')).pointerEvents,
    hudBtn: cs(g('wt-fwd')).pointerEvents
  };
  out.roles = {
    callRole: call.getAttribute('role'), callLive: call.getAttribute('aria-live'),
    foldTag: fold.tagName, foldType: fold.type,
    foldExpanded: fold.getAttribute('aria-expanded'),
    foldName: (fold.textContent || '').trim().slice(0, 90),
    lineInDom: !!line && line.textContent.length > 0,
    lineDisplay: cs(line).display, lineClip: cs(line).clip,
    skipHidden: g('wt-skip').hidden, skipDisabled: g('wt-skip').disabled,
    skipLabel: g('wt-skip').getAttribute('aria-label'),
    foldTabIndex: fold.tabIndex,
    callClass: call.className, callOpacity: cs(call).opacity,
    hudText: g('wt-count').textContent,
    hudBox: (r=>[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)])(g('wt-hud').getBoundingClientRect()),
    backLabel: g('wt-back').getAttribute('aria-label'),
    fwdLabel: g('wt-fwd').getAttribute('aria-label')
  };
  out.motion = {
    rmClass: D.documentElement.classList.contains('rm') || D.body.classList.contains('rm'),
    glowAnim: cs(ring.querySelector('i')).animationName,
    glowDur: cs(ring.querySelector('i')).animationDuration,
    callTrans: cs(call).transitionProperty + ' ' + cs(call).transitionDuration,
    foldTrans: cs(fold).transitionProperty + ' ' + cs(fold).transitionDuration,
    ringTrans: cs(ring).transitionDuration,
    progTrans: cs(g('wt-prog').querySelector('i')).transitionDuration
  };
  out.paint = {
    foldBg: cs(fold).backgroundColor, foldBorder: cs(fold).borderTopWidth + ' ' + cs(fold).borderTopColor,
    titleColor: cs(g('wt-title')).color, lineColor: cs(line).color,
    hcOn: g('phone').classList.contains('hc'),
    tsize: g('phone').dataset.textsize || 'default',
    fs: { title: cs(g('wt-title')).fontSize, line: cs(line).fontSize }
  };
  out.frame = { phone: [g('phone').offsetWidth, g('phone').offsetHeight],
                callBox: (r => [r.x, r.y, r.width, r.height].map(v => +v.toFixed(1)))(fold.getBoundingClientRect()),
                inFrame: (function () { var p = g('phone').getBoundingClientRect(), r = fold.getBoundingClientRect();
                  return r.left >= p.left - 0.5 && r.right <= p.right + 0.5 && r.top >= p.top - 0.5 && r.bottom <= p.bottom + 0.5; })() };
  out.step = window.WT.step();
  return out;
}
"""


def pdown(pg, sel, ptype='touch'):
    pg.evaluate("""([s,t])=>{const n=document.querySelector(s);const r=n.getBoundingClientRect();
      n.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true,pointerId:9,pointerType:t,isPrimary:true,
        clientX:r.left+r.width/2,clientY:r.top+r.height/2,button:0}));}""", [sel, ptype])


def pup(pg, sel, ptype='touch'):
    pg.evaluate("""([s,t])=>{const n=document.querySelector(s);
      n.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,cancelable:true,pointerId:9,pointerType:t,isPrimary:true,button:0}));}""", [sel, ptype])


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={'width': A.w, 'height': A.h},
                        reduced_motion=('reduce' if A.rm else 'no-preference'),
                        device_scale_factor=1)
    pg = ctx.new_page(); pg.set_default_timeout(90000)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:8891/design/demo-app.html')
    pg.wait_for_timeout(1800)
    pg.evaluate(HARNESS)
    pg.evaluate("async()=>{ await window.__M.boot(); }")
    if A.ts:
        pg.evaluate("(t)=>{var b=document.querySelector('[data-tsize=\"'+t+'\"]'); if(b) b.click();}", A.ts)
    if A.hc:
        pg.evaluate("()=>{var t=document.querySelector('[data-pref=\"hc\"]'); if(t) t.click();}")
    R = {'w': A.w, 'h': A.h, 'rm': A.rm, 'hc': A.hc, 'ts': A.ts}

    # ---- step 1, expanded ----
    pg.evaluate("async()=>{ await window.__M.settle(5000); }")
    R['s1_open'] = pg.evaluate(PROBE)
    # ---- the auto fold: is the dwell honoured, and is it honoured under Reduce Motion ----
    d = R['s1_open']['step']['dwell']
    pg.wait_for_timeout(int(d * 0.5))
    R['half_dwell_mini'] = pg.evaluate("()=>document.getElementById('wt-call').classList.contains('mini')")
    pg.wait_for_timeout(int(d * 0.5) + 500)
    R['after_dwell_mini'] = pg.evaluate("()=>document.getElementById('wt-call').classList.contains('mini')")
    R['s1_folded'] = pg.evaluate(PROBE)
    # ---- hover on a pointer device ----
    pg.evaluate("""()=>{const n=document.getElementById('wt-fold');const r=n.getBoundingClientRect();
      n.dispatchEvent(new PointerEvent('pointerenter',{bubbles:false,pointerType:'mouse',clientX:r.left+5,clientY:r.top+5}));}""")
    pg.wait_for_timeout(120)
    R['hover_expanded'] = not pg.evaluate("()=>document.getElementById('wt-call').classList.contains('mini')")
    pg.evaluate("""()=>{const n=document.getElementById('wt-fold');
      n.dispatchEvent(new PointerEvent('pointerleave',{bubbles:false,pointerType:'mouse'}));}""")
    pg.wait_for_timeout(120)
    R['hover_refolded'] = pg.evaluate("()=>document.getElementById('wt-call').classList.contains('mini')")
    # ---- press and hold on a touch device ----
    pdown(pg, '#wt-fold')
    pg.wait_for_timeout(150)
    R['hold_at150_expanded'] = not pg.evaluate("()=>document.getElementById('wt-call').classList.contains('mini')")
    pg.wait_for_timeout(350)
    R['hold_at500_expanded'] = not pg.evaluate("()=>document.getElementById('wt-call').classList.contains('mini')")
    pup(pg, '#wt-fold')
    pg.wait_for_timeout(150)
    R['hold_release_refolded'] = pg.evaluate("()=>document.getElementById('wt-call').classList.contains('mini')")
    # ---- keyboard: focus the chip and press Enter ----
    # past the 300ms window that suppresses the synthetic click after a hold
    pg.wait_for_timeout(600)
    pg.evaluate("()=>document.getElementById('wt-fold').focus()")
    R['focus_is_chip'] = pg.evaluate("()=>document.activeElement && document.activeElement.id")
    R['focus_outline'] = pg.evaluate("()=>{var c=getComputedStyle(document.getElementById('wt-fold'),null);return c.outlineWidth+' '+c.outlineStyle+' '+c.outlineColor;}")
    pg.keyboard.press('Enter')
    pg.wait_for_timeout(150)
    R['enter_expanded'] = not pg.evaluate("()=>document.getElementById('wt-call').classList.contains('mini')")
    pg.keyboard.press('Space')
    pg.wait_for_timeout(150)
    R['space_refolded'] = pg.evaluate("()=>document.getElementById('wt-call').classList.contains('mini')")
    # ---- the branch control: only on the map, never inside a sheet ----
    pg.evaluate("async()=>{var M=window.__M; for(var n=0;n<4;n++){ await M.settle(4000); await M.act(); await M.sleep(500);} }")
    pg.wait_for_timeout(1500)
    R['skip_on_map'] = not pg.evaluate("()=>document.getElementById('wt-skip').hidden")
    pg.evaluate("()=>{document.getElementById('key-toggle').click();}")
    pg.wait_for_timeout(400)
    pg.evaluate("()=>{var c=document.getElementById('key-cta'); if(c) c.click();}")
    pg.wait_for_timeout(700)
    R['sheet_open'] = pg.evaluate("()=>!!document.querySelector('.sheet.on')")
    R['skip_in_sheet'] = not pg.evaluate("()=>document.getElementById('wt-skip').hidden")
    R['skip_label_in_sheet'] = pg.evaluate("()=>document.getElementById('wt-skip').getAttribute('aria-label')")
    R['hud_covers_no_app_control'] = pg.evaluate("""()=>{
      const h=document.getElementById('wt-hud').getBoundingClientRect();
      const bad=[];
      document.querySelectorAll('.screen.active button,.screen.active a,.sheet.on button,#navbar button,.apphead button').forEach(n=>{
        if(n.closest('#wt')) return; const b=n.getBoundingClientRect();
        if(!b.width||!b.height) return;
        const w=Math.min(h.right,b.right)-Math.max(h.left,b.left);
        const v=Math.min(h.bottom,b.bottom)-Math.max(h.top,b.top);
        if(w>0&&v>0) bad.push((n.id||n.className)+' '+Math.round(b.x)+','+Math.round(b.y));
      });
      return bad;
    }""")
    R['ring_targets_skip_ever'] = pg.evaluate("()=>{try{return JSON.stringify(window.WT.step().sel).indexOf('wt-skip')>=0}catch(e){return 'err'}}")
    R['errs'] = errs[:10]
    print(json.dumps(R, indent=1))
    b.close()
