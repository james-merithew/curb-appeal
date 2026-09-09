"""Unwrap a standalone prototype page for the Artifact wrapper.

The Artifact host supplies its own `<!doctype html><head>...</head><body>` and
places the file's content inside that body. Publishing a complete document there
nests one inside another, so this strips the outer wrapper and hands over exactly
what belongs inside it: the head's contents (minus the two metas the host already
supplies) followed by the body's contents.

Run it, then publish the file it writes -- never the source page directly.

    py tools/artifact_unwrap.py design/demo-app.html <out.html> "EntryMap Walkthrough"

The title is rewritten because the host reads the <title> tag and the tag always
wins over the tool's own `title` parameter.
"""
import sys
import pathlib

# Only the charset is stripped. The viewport meta is KEPT: a walkthrough round measured
# what happens when the host does not supply one -- a 980px layout viewport, the desktop
# phone-mock drawn 155 device pixels wide, and a page that scrolls. A duplicate viewport
# meta is harmless; a missing one is the whole of "there shouldn't be a scroll".
HOST_SUPPLIES = (
    '<meta charset="utf-8">',
)


def unwrap(src_text: str, title: str | None) -> str:
    head = src_text[src_text.index("<head>") + len("<head>"): src_text.index("</head>")]
    body = src_text[src_text.index("<body>") + len("<body>"): src_text.rindex("</body>")]
    for tag in HOST_SUPPLIES:
        head = head.replace(tag, "")
    if title:
        start = head.index("<title>")
        end = head.index("</title>") + len("</title>")
        head = head[:start] + f"<title>{title}</title>" + head[end:]
    return head.strip() + "\n" + body.strip() + "\n"


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    src = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    title = sys.argv[3] if len(sys.argv) > 3 else None

    text = unwrap(src.read_text(encoding="utf-8"), title)
    out.write_text(text, encoding="utf-8")

    # A real nested document tag would break the page; the same characters inside a
    # comment or a string are fine, so report the count rather than refusing.
    bare = sum(text.count(t) for t in ("<!DOCTYPE", "<html ", "</html>", "<head>", "</head>", "<body>", "</body>"))
    non_ascii = sum(1 for ch in text if ord(ch) > 0x7E)
    print(f"{out}  {out.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"  document tags found (comments included): {bare}")
    print(f"  non-ASCII characters: {non_ascii}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
