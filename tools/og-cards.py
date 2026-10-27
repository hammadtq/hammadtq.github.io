#!/usr/bin/env python3
"""Render 1200x630 social cards for posts into assets/images/og/.

Usage:
  python3 tools/og-cards.py            # cards for posts that don't have one yet
  python3 tools/og-cards.py --all      # re-render every card, plus og-default
  python3 tools/og-cards.py <post.md>  # one post

Needs a headless Chromium. Set CHROME to its path, or let the script find
Playwright's cached chrome-headless-shell. Network access is used for the
Inter font from Google Fonts.
"""
import glob
import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "images", "og")
PHOTO = os.path.join(ROOT, "assets", "images", "bio-photo.jpg")

CATEGORY_LABELS = {"startups": "Startups", "protocol-notes": "Protocol Notes"}

TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=block" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1200px; height: 630px; overflow: hidden; background: #0f172a; }
.card {
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  font-family: 'Inter', -apple-system, sans-serif;
  padding: 72px 80px 64px; display: flex; flex-direction: column;
}
.card::before { content: ''; position: absolute; top: -220px; right: -180px; width: 640px; height: 640px;
  background: radial-gradient(circle, rgba(59,130,246,.18) 0%, transparent 70%); }
.card::after { content: ''; position: absolute; bottom: -180px; left: -160px; width: 460px; height: 460px;
  background: radial-gradient(circle, rgba(139,92,246,.12) 0%, transparent 70%); }
.grid { position: absolute; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
  background-size: 40px 40px; }
.bar { position: absolute; top: 0; left: 0; right: 0; height: 6px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899); }
.z { position: relative; z-index: 1; }
.meta { display: flex; align-items: center; gap: 16px; font-size: 20px; font-weight: 500; color: #64748b; }
.pill { background: rgba(59,130,246,.2); border: 1px solid rgba(59,130,246,.35); color: #60a5fa;
  padding: 8px 18px; border-radius: 8px; text-transform: uppercase; letter-spacing: .08em; font-size: 16px; font-weight: 700; }
.main { flex: 1; display: flex; flex-direction: column; justify-content: center; }
h1 { color: #fff; font-weight: 800; letter-spacing: -0.025em; line-height: 1.08; font-size: {{TITLE_SIZE}}px;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
p { margin-top: 24px; color: #94a3b8; font-size: 26px; line-height: 1.4; max-width: 1000px;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.foot { display: flex; align-items: center; gap: 18px; }
.foot img { width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 2px solid rgba(255,255,255,.15); }
.name { color: #fff; font-size: 24px; font-weight: 700; }
.site { color: #64748b; font-size: 20px; margin-top: 2px; }
</style></head>
<body><div class="card"><div class="grid"></div><div class="bar"></div>
<div class="z meta">{{META}}</div>
<div class="z main"><h1>{{TITLE}}</h1>{{SUBTITLE}}</div>
<div class="z foot"><img src="{{PHOTO}}"><div><div class="name">Hammad Tariq</div><div class="site">hammadtariq.com</div></div></div>
</div></body></html>"""


def find_chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    hits = sorted(glob.glob(os.path.expanduser(
        "~/Library/Caches/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell")))
    hits += sorted(glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell")))
    if not hits:
        sys.exit("No headless Chromium found; set CHROME=/path/to/chrome")
    return hits[-1]


def front_matter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm = m.group(1) if m else ""

    def field(name):
        f = re.search(r"^%s:\s*(.+)$" % name, fm, re.M)
        return f.group(1).strip().strip('"').strip("'") if f else ""

    cats = re.findall(r"[\w-]+", field("categories"))
    return {"title": field("title"), "summary": field("summary"),
            "category": cats[0] if cats else "", "date": field("date"),
            "og_image": (re.search(r"^\s+og_image:\s*(\S+)", fm, re.M) or [None, ""])[1]}


def slug(path):
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", os.path.basename(path)[:-3]).lower()


def title_size(title):
    n = len(title)
    return 76 if n <= 32 else 64 if n <= 55 else 56 if n <= 80 else 48


def render(chrome, out_png, title, summary="", meta=""):
    page = (TEMPLATE
            .replace("{{TITLE_SIZE}}", str(title_size(title)))
            .replace("{{TITLE}}", html.escape(title))
            .replace("{{SUBTITLE}}", "<p>%s</p>" % html.escape(summary) if summary else "")
            .replace("{{META}}", meta)
            .replace("{{PHOTO}}", "file://" + PHOTO))
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(page)
    try:
        subprocess.run([chrome, "--headless", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--window-size=1200,630", "--virtual-time-budget=8000",
                        "--allow-file-access-from-files", "--screenshot=" + out_png, "file://" + f.name],
                       check=True, capture_output=True)
    finally:
        os.unlink(f.name)


def to_jpeg(png, jpg):
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", png, "--out", jpg],
                   check=True, capture_output=True)
    os.unlink(png)


def main():
    args = sys.argv[1:]
    redo = "--all" in args
    posts = [a for a in args if a.endswith(".md")] or sorted(glob.glob(os.path.join(ROOT, "_posts", "*.md")))
    chrome = find_chrome()
    os.makedirs(OUT, exist_ok=True)

    for post in posts:
        fm = front_matter(post)
        if fm["og_image"] and "/og/" not in fm["og_image"]:
            continue  # post uses its own artwork
        jpg = os.path.join(OUT, slug(post) + ".jpg")
        if os.path.exists(jpg) and not redo and len(args) == 0:
            continue
        label = CATEGORY_LABELS.get(fm["category"], fm["category"].replace("-", " ").title())
        meta = '<span class="pill">%s</span>' % html.escape(label) if label else ""
        png = jpg[:-4] + ".png"
        render(chrome, png, fm["title"], fm["summary"], meta)
        to_jpeg(png, jpg)
        print("wrote", os.path.relpath(jpg, ROOT))

    if redo:
        png = os.path.join(ROOT, "assets", "images", "og-default.png")
        render(chrome, png, "Hammad Tariq",
               "Identity and security infrastructure for AI agents, and HamariHawa, a live map of air pollution over Pakistan and India.",
               '<span class="pill">Cryptography</span><span class="pill">AI</span><span class="pill">Finance</span>')
        print("wrote", os.path.relpath(png, ROOT))


if __name__ == "__main__":
    main()
