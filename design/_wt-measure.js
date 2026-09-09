/* TEMPORARY measurement harness for the walkthrough round -- not part of the three
   appended blocks and not loaded by demo-app.html. It is injected by
   design/_wt-drive.py.

   It exists to answer the one question the pass before this one never measured:
   "does the callout cover the thing this step is about" -- per step, printed.
   Everything else it records (rendered line count, ring shape and mode, fold
   decision, dock position, per-stop elapsed time) is there so that no claim in
   the round report has to be estimated. */
window.__M = {
  sleep: function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); },

  rb: function (e) {
    if (!e) return null; var r = e.getBoundingClientRect();
    if (!r.width || !r.height) return null;
    return { x: +r.left.toFixed(1), y: +r.top.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1), r: +r.right.toFixed(1), b: +r.bottom.toFixed(1) };
  },
  ov: function (a, b) {
    if (!a || !b) return 0;
    var w = Math.max(0, Math.min(a.r, b.r) - Math.max(a.x, b.x));
    var h = Math.max(0, Math.min(a.b, b.b) - Math.max(a.y, b.y));
    return Math.round(w * h);
  },
  vis: function (n) {
    if (!n || !n.getClientRects().length) return false;
    var cs = getComputedStyle(n);
    if (cs.visibility === 'hidden' || cs.opacity === '0' || cs.display === 'none') return false;
    return true;
  },
  /* the union of every match of a (possibly comma-separated) selector: the same
     region the layer itself treats as "what this step is about" */
  unionOf: function (sel) {
    var M = this, out = null;
    if (!sel) return null;
    document.querySelectorAll(sel).forEach(function (n) {
      if (!M.vis(n)) return;
      var b = M.rb(n); if (!b) return;
      out = out ? { x: Math.min(out.x, b.x), y: Math.min(out.y, b.y), r: Math.max(out.r, b.r), b: Math.max(out.b, b.b) } : { x: b.x, y: b.y, r: b.r, b: b.b };
    });
    if (!out) return null;
    out.w = +(out.r - out.x).toFixed(1); out.h = +(out.b - out.y).toFixed(1);
    return out;
  },
  surfaces: function () {
    var out = [], a = document.querySelector('.screen.active');
    if (a) out.push(a);
    document.querySelectorAll('.sheet.on').forEach(function (s) { out.push(s); });
    return out;
  },
  /* every app element the callout's box overlaps that has its own text or is a
     control, with the fraction of it covered. Nothing inside #wt counts. */
  covered: function (callBox) {
    var M = this, out = [];
    if (!callBox) return out;
    M.surfaces().forEach(function (surf) {
      surf.querySelectorAll('*').forEach(function (n) {
        if (n.closest('#wt')) return;
        var b = M.rb(n); if (!b) return;
        var o = M.ov(callBox, b); if (o <= 0) return;
        var txt = (n.textContent || '').trim().replace(/\s+/g, ' ');
        var isLeafText = txt && n.children.length === 0;
        var isCtl = /^(BUTTON|A|INPUT|IMG|CANVAS|SVG)$/.test(n.tagName);
        if (!isLeafText && !isCtl) return;
        if (!M.vis(n)) return;
        out.push({
          sel: (n.id ? '#' + n.id : n.tagName.toLowerCase() + (n.className && typeof n.className === 'string' ? '.' + n.className.trim().split(/\s+/).join('.') : '')),
          t: txt.slice(0, 40), ov: o, frac: +(o / (b.w * b.h)).toFixed(2)
        });
      });
    });
    out.sort(function (p, q) { return q.frac - p.frac; });
    return out.slice(0, 6);
  },
  /* how many rendered lines the step's line is running to. THE measurement behind
     "one short line": the per-callout cap is only real if this is 1. */
  lines: function () {
    var el = document.getElementById('wt-line');
    if (!el || !el.textContent) return 0;
    /* measured UNFOLDED even when the stop folded itself: .mini clips #wt-line to
       1px, and "how many lines does this line run to" is a property of the copy,
       not of the fold decision. The classes are put straight back in the same
       synchronous block, so nothing is painted in between. */
    var call = document.getElementById('wt-call');
    var wasMini = call.classList.contains('mini');
    var wasSil = call.classList.contains('silent');
    if (wasMini) call.classList.remove('mini');
    if (wasSil) call.classList.remove('silent');
    var cs = getComputedStyle(el);
    var lh = parseFloat(cs.lineHeight);
    if (!lh || isNaN(lh)) lh = parseFloat(cs.fontSize) * 1.4;
    var n = Math.round(el.getBoundingClientRect().height / lh);
    var w = Math.round(el.getBoundingClientRect().width);
    if (wasMini) call.classList.add('mini');
    if (wasSil) call.classList.add('silent');
    this.lastLineW = w;
    return n;
  },
  key: function () { var s = window.WT.step(); return (s.branch || '') + s.step; },
  isFin: function () {
    var f = document.getElementById('wt-fwd');
    return !!f && /Close the walkthrough/.test(f.getAttribute('aria-label') || '');
  },
  snap: function (tag, phase) {
    var M = this, D = document;
    var st = window.WT.step();
    var callEl = D.getElementById('wt-call'), ringEl = D.getElementById('wt-ring');
    var foldEl = D.getElementById('wt-fold');
    var call = M.rb(foldEl), ring = M.rb(ringEl);
    var mini = /\bmini\b/.test(callEl.className);
    var subj = M.unionOf(st.subj);
    var tgt = st.sel ? M.unionOf(st.sel) : null;
    var subjOv = M.ov(call, subj);
    return {
      tag: tag, phase: phase, step: st.step, of: st.of, branch: st.branch,
      ch: st.ch, chName: st.chName, pos: st.pos, chTotal: st.chTotal,
      silent: st.silent, pre: st.pre, nar: st.nar, narOf: st.narOf,
      hudChap: (document.getElementById('wt-count')||{}).textContent,
      foldTab: document.getElementById('wt-fold').tabIndex,
      wtHidden: document.getElementById('wt').hidden,
      scr: (D.querySelector('.screen.active') || {}).id,
      sel: st.sel, subj: st.subj, dwell: st.dwell,
      title: D.getElementById('wt-title').textContent,
      line: D.getElementById('wt-line').textContent,
      chars: D.getElementById('wt-line').textContent.length,
      lines: M.lines(), lineW: M.lastLineW,
      callClass: callEl.className,
      callOn: callEl.classList.contains('on'), mini: mini,
      expanded: foldEl.getAttribute('aria-expanded'),
      call: call ? [call.x, call.y, call.w, call.h] : null,
      ringOn: ringEl.classList.contains('on'),
      ringIn: ringEl.classList.contains('in'),
      ringOnFill: ringEl.classList.contains('onfill'),
      ringShadow: ringEl.classList.contains('on') ? getComputedStyle(ringEl).boxShadow : null,
      ring: ring ? [ring.x, ring.y, ring.w, ring.h] : null,
      radius: ringEl.classList.contains('on') ? getComputedStyle(ringEl).borderRadius : null,
      ink: ringEl.style.getPropertyValue('--wt-ink') || null,
      scale: callEl.style.getPropertyValue('--wt-scale') || '1',
      arrow: getComputedStyle(D.getElementById('wt-arrow')).display,
      tgtOv: M.ov(call, tgt),
      subjBox: subj ? [subj.x, subj.y, subj.w, subj.h] : null,
      subjOv: subjOv,
      subjFrac: subj ? +(subjOv / (subj.w * subj.h)).toFixed(3) : 0,
      covers: mini ? M.covered(call) : M.covered(call)
    };
  },
  ACTS: {}, NORING: {},
  /* settled = the ring is on (or the stop declares none) and the callout's own
     style and class string have been identical for three samples. The same
     discipline the layer uses, so nothing is sampled mid-transition. */
  settle: async function (ms) {
    var M = this, t = Date.now(), last = '', n = 0;
    var noRing = !!(M.NORING && M.NORING[M.key()]) || window.WT.step().ring === false;
    var sil = !!window.WT.step().silent;
    while (Date.now() - t < ms) {
      var c = document.getElementById('wt-call'), r = document.getElementById('wt-ring');
      var ringOn = r.classList.contains('on');
      var st = (c.getAttribute('style') || '') + '|' + c.className + '|' + (r.getAttribute('style') || '') + '|' + ringOn;
      var ok = sil ? ringOn : (c.classList.contains('on') && (ringOn || noRing));
      if (st === last && ok) { if (++n >= 3) return true; } else n = 0;
      last = st; await M.sleep(60);
    }
    return false;
  },
  click: function (s) { var e = document.querySelector(s); if (e) { e.click(); return true; } return false; },
  /* the press-and-hold the numbered disc answers. Dispatched as a real pointer
     sequence on #pins, which is where the app delegates from. */
  hold: async function (s) {
    var n = document.querySelector(s); if (!n) return false;
    var r = n.getBoundingClientRect();
    var o = { bubbles: true, cancelable: true, composed: true, pointerId: 7, pointerType: 'touch', isPrimary: true, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2 };
    n.dispatchEvent(new PointerEvent('pointerdown', o));
    await this.sleep(700);
    return true;
  },
  release: function () {
    var o = { bubbles: true, cancelable: true, composed: true, pointerId: 7, pointerType: 'touch', isPrimary: true };
    var n = document.getElementById('pins');
    if (n) n.dispatchEvent(new PointerEvent('pointerup', o));
  },
  type: async function (s, txt) {
    var n = document.querySelector(s); if (!n) return false;
    n.focus(); n.value = txt;
    n.dispatchEvent(new Event('input', { bubbles: true }));
    await this.sleep(250); return true;
  },
  /* the two stops whose control is genuinely below the fold on a 390x844 frame
     (My Business on screen-profile, Suggest a correction at the bottom of a full
     card). The presenter scrolls; the harness has to as well, or the row it
     records is the layer's scroll hint rather than the step's own line. */
  reveal: async function () {
    var M = this, st = window.WT.step();
    if (!st.sel) return false;
    var n = document.querySelector(st.sel);
    if (!n) return false;
    var phone = document.getElementById('phone');
    var wt = document.getElementById('wt');
    var frame = wt.getBoundingClientRect();
    var b = n.getBoundingClientRect();
    if (b.top - frame.top >= 46 && b.bottom - frame.top <= frame.height) return false;
    /* NOT scrollIntoView. It walks every scrollable ancestor including #phone,
       which is overflow:hidden and is the app's own frame -- scrolling it slides
       the whole app inside its bezel, which no user can do and which put the
       walkthrough's frame 253px out of register with the app in an earlier run
       of this harness. Only the nearest scroller INSIDE the phone moves. */
    var sc = n.parentElement;
    while (sc && sc !== phone) {
      var ov = getComputedStyle(sc).overflowY;
      if ((ov === 'auto' || ov === 'scroll') && sc.scrollHeight > sc.clientHeight + 1) break;
      sc = sc.parentElement;
    }
    if (!sc || sc === phone) return false;
    var sb = sc.getBoundingClientRect();
    sc.scrollTop += (b.top - sb.top) - (sb.height / 2 - b.height / 2);
    if (phone.scrollTop) phone.scrollTop = 0;
    await M.sleep(500);
    return true;
  },
  act: async function () {
    var M = this, st = window.WT.step(), a = M.ACTS[M.key()] || M.ACTS[st.title];
    if (a === 'wait') { await M.sleep(9800); return; }
    if (a === 'hold') { await M.hold(st.sel); return; }
    if (typeof a === 'function') { await a(M); return; }
    if (st.sel) M.click(st.sel);
    await M.sleep(150);
  },
  waitKey: async function (from, ms) {
    var M = this, t = Date.now();
    while (Date.now() - t < ms) { if (M.key() !== from) return true; await M.sleep(60); }
    return false;
  },
  nocam: function () {
    var deny = function () { return Promise.reject(new Error('harness: denied')); };
    try { Object.defineProperty(navigator, 'mediaDevices', { configurable: true, value: { getUserMedia: deny, enumerateDevices: function () { return Promise.resolve([]); } } }); } catch (e) { }
  },
  boot: async function () {
    var M = this; M.nocam();
    var sp = document.getElementById('ob-splash');
    if (sp && sp.classList.contains('active')) { sp.click(); await M.sleep(1400); }
    window.__rows = []; window.__scrolled = [];
    return (document.querySelector('.screen.active') || {}).id;
  },

  /* ONE STOP, TWO SAMPLES.
     A: the moment the geometry has settled -- the callout as it opens, which is
        where "does it cover the subject" is decided.
     B: dwell + 500ms later -- the folded chip, which is where the dock is
        measured and where the auto-fold is confirmed to have happened.
     BEAT is the presenter's beat before he taps: the runtime this reports is
     therefore the layer's own pace plus one fixed human beat per stop, stated
     rather than assumed. */
  BEAT: 900,
  run: async function (maxStops) {
    var M = this, t0 = Date.now();
    for (var n = 0; n < (maxStops || 60); n++) {
      var k = M.key(), s0 = Date.now(), sil = !!window.WT.step().silent;
      await M.settle(5000);
      if (await M.reveal()) { window.__scrolled = (window.__scrolled || []).concat([k]); await M.settle(4000); }
      var a = M.snap(k, sil ? 'S' : 'A'); a.tSettle = Date.now() - s0;
      window.__rows.push(a);
      if (!sil) {
        var d = window.WT.step().dwell;
        await M.sleep(d + 150);
        var b = M.snap(k, 'B'); window.__rows.push(b);
        await M.sleep(M.BEAT);
      } else {
        await M.sleep(250);
      }
      await M.act();
      var moved = await M.waitKey(k, 9000);
      a.tStop = Date.now() - s0;
      if (!moved) {
        if (M.isFin()) { await M.settle(2500); window.__rows.push(M.snap('FINISH', 'A')); break; }
        window.__rows.push({ tag: 'STUCK ' + k, phase: 'X', scr: (document.querySelector('.screen.active') || {}).id, sel: window.WT.step().sel });
        break;
      }
      if (M.isFin()) { await M.settle(2500); window.__rows.push(M.snap('FINISH', 'A')); break; }
    }
    window.__wall = Date.now() - t0;
    return window.__rows.length;
  }
};
window.__rows = [];
