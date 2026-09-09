"""Build the artifact-host wrappers around the CURRENT design/demo-app.html,
using tools/artifact_unwrap.py itself so the thing under test is the thing that
gets published.

Two host skeletons, differing in exactly one line:
  host-vp.html   the host supplies <meta name=viewport content="width=device-width,initial-scale=1">
  host-novp.html the host supplies no viewport meta at all
and one more:
  host-frame.html  an iframe of host-vp at an arbitrary width, which is what a
                   viewer pane does.
"""
import pathlib, sys
sys.path.insert(0, 'C:/dev/curb-appeal/tools')
from artifact_unwrap import unwrap

SP = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
SRC = pathlib.Path('C:/dev/curb-appeal/design/demo-app.html')
inner = unwrap(SRC.read_text(encoding='utf-8'), 'EntryMap Walkthrough')

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
%s<style>
body{margin:0;padding:0;font:14px system-ui;background:#faf9f5}
img{max-width:100%%}
[hidden]{display:none!important}
</style>
</head>
<body>
"""
VP = '<meta name="viewport" content="width=device-width, initial-scale=1">\n'

(SP / 'host-vp.html').write_text(HEAD % VP + inner + '\n</body>\n</html>\n', encoding='utf-8')
(SP / 'host-novp.html').write_text(HEAD % '' + inner + '\n</body>\n</html>\n', encoding='utf-8')
(SP / 'host-frame.html').write_text(
    '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">'
    '<style>html,body{margin:0;padding:0}iframe{display:block;width:100%;height:100vh;border:0}</style>'
    '</head><body><iframe src="host-vp.html"></iframe></body></html>\n', encoding='utf-8')
for n in ('host-vp.html', 'host-novp.html', 'host-frame.html'):
    p = SP / n
    print(n, p.stat().st_size, 'bytes')
