#!/usr/bin/env python3
"""Build the GitHub Pages site in docs/ from the app sources.

Each app lives in <app>/index.html as a page fragment (the same file is published
as a Claude artifact, which adds its own document skeleton). This script wraps every
fragment in a full HTML document: everything above the `<!-- body -->` marker goes
into <head>, the rest into <body>. home/ becomes the site root.
"""
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "docs"
DOMAIN = "maxpog.com"
MARKER = "<!-- body -->"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px/1.4 system-ui,-apple-system,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>
"""


def wrap(src: pathlib.Path) -> str:
    text = src.read_text(encoding="utf-8")
    if MARKER not in text:
        raise SystemExit(f"{src}: missing {MARKER} marker")
    head, body = text.split(MARKER, 1)
    head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    return f"{HEAD}{head.strip()}\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n"


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for src in sorted(ROOT.glob("*/index.html")):
        app = src.parent.name
        if app == "docs":
            continue
        dest = OUT / "index.html" if app == "home" else OUT / app / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(wrap(src), encoding="utf-8")
        print("built", dest.relative_to(ROOT))
        for asset in src.parent.iterdir():
            if asset.is_file() and asset.name != "index.html" and not asset.name.startswith("."):
                shutil.copy(asset, dest.parent / asset.name)
    shutil.copy(ROOT / "nonstop" / "favicon.svg", OUT / "favicon.svg")
    (OUT / "CNAME").write_text(DOMAIN + "\n")
    (OUT / ".nojekyll").write_text("")


if __name__ == "__main__":
    main()
