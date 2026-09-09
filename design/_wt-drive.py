"""Drives design/demo-app.html through the walkthrough and prints the per-step
coverage table. Temporary tooling for the walkthrough round.

  py design/_wt-drive.py [--w 390] [--h 844] [--rm] [--hc] [--ts larger]
                         [--branch A|B|C] [--out run.json]

Needs a server on 127.0.0.1:8891 rooted at the repo (py -m http.server 8891).
Playwright, not the Browser pane: the pane's rAF stops the moment it is not the
fronted view, and this layer's whole tracking loop is rAF.
"""
import argparse, json, time
from playwright.sync_api import sync_playwright

AP = argparse.ArgumentParser()
AP.add_argument('--w', type=int, default=390)
AP.add_argument('--h', type=int, default=844)
AP.add_argument('--rm', action='store_true')
AP.add_argument('--hc', action='store_true')
AP.add_argument('--ts', default='')
AP.add_argument('--branch', default='')
AP.add_argument('--chapter', type=int, default=0)
AP.add_argument('--out', default='wtrun.json')
AP.add_argument('--url', default='http://127.0.0.1:8891/design/demo-app.html')
A = AP.parse_args()

HARNESS = open('C:/dev/curb-appeal/design/_wt-measure.js', encoding='utf-8').read()

CFG = """
(function(){
  var M = window.__M;
  /* keyed by TITLE, not by step number, so inserting a step does not silently
     retarget an action at the wrong stop -- which it did once, and the run stalled
     with the press-and-hold aimed at the locate button. */
  M.ACTS = {
    'Grouped places': 'hold',
    'It reads the photo': 'wait',
    'In your words': async function(m){ await m.type('#correct-note','The side door has a bell now.'); }
  };
})();
"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={'width': A.w, 'height': A.h},
                        reduced_motion=('reduce' if A.rm else 'no-preference'),
                        device_scale_factor=1)
    pg = ctx.new_page()
    pg.set_default_timeout(300000)
    errs = []
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
    pg.goto(A.url)
    pg.wait_for_timeout(1800)
    pg.evaluate(HARNESS)
    pg.evaluate(CFG)
    pg.evaluate("async()=>{ await window.__M.boot(); }")
    if A.ts:
        pg.evaluate("(t)=>{ var b=document.querySelector('[data-tsize=\"'+t+'\"]'); if(b) b.click(); }", A.ts)
    if A.hc:
        pg.evaluate("()=>{ var t=document.querySelector('[data-pref=\"hc\"]'); if(t) t.click(); }")
    if A.chapter:
        pg.evaluate("(n)=>{ window.WT.chapter(n); }", A.chapter)
        pg.wait_for_timeout(900)
        pg.evaluate("()=>{ window.__rows=[]; }")
    t0 = time.time()
    pg.evaluate("async()=>{ await window.__M.run(120); }")
    t1 = time.time()
    rows = pg.evaluate("window.__rows")
    wall = pg.evaluate("window.__wall")
    scrolled = pg.evaluate("window.__scrolled||[]")
    json.dump({'w': A.w, 'h': A.h, 'rm': A.rm, 'hc': A.hc, 'ts': A.ts, 'branch': A.branch, 'chapter': A.chapter,
               'wall_ms': wall, 'scrolled': scrolled, 'py_s': round(t1 - t0, 1), 'errs': errs[:25], 'rows': rows},
              open(A.out, 'w', encoding='ascii'), indent=1)
    print('rows', len(rows), 'wall_ms', wall, 'errs', len(errs))
    for e in errs[:8]:
        print('  ', e[:160])
    b.close()
