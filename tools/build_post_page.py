#!/usr/bin/env python3
"""Wrap a self-contained post fragment (meta+title+style+body, no doctype)
into a full Field Notes page with site chrome and analytics.

Usage: build_post_page.py <master.html> <out_dir_under_posts>
Example: build_post_page.py ~/conamur/learning-on-the-job.html learning-on-the-job
"""
import re, sys, pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent

ANALYTICS = """<script>
  if (location.hostname === 'curiouseralice.github.io') {
    var gc = document.createElement('script');
    gc.async = true;
    gc.src = 'https://gc.zgo.at/count.js';
    gc.setAttribute('data-goatcounter', 'https://curiouseralice.goatcounter.com/count');
    document.head.appendChild(gc);
  }
</script>"""

CHROME_CSS = """
  /* --- site chrome --- */
  .site-top { max-width: 42.5rem; margin: 0 auto; padding-top: 1.5rem; font-family: var(--mono); font-size: 0.78rem; }
  .site-top a { color: var(--muted); border-bottom: none; }
  .site-top a:hover { color: var(--link); }
  footer.site-foot { max-width: 42.5rem; margin: -2.5rem auto 0; padding: 1.4rem 0 2.6rem; border-top: 1px solid var(--line); font-family: var(--mono); font-size: 0.72rem; color: var(--faint); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; }
  footer.site-foot a { color: var(--muted); border-bottom-color: var(--line); }
"""

def build(master: pathlib.Path, slug: str, description: str = "") -> pathlib.Path:
    src = master.read_text(encoding="utf-8")
    style_start = src.find("<style>")
    style_end = src.find("</style>")
    main_css = src[style_start + len("<style>"):style_end]
    body = src[style_end + len("</style>"):].strip()
    title = re.search(r"<title>(.*?)</title>", src).group(1)
    desc = description or title

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Field Notes</title>
<meta name="description" content="{desc}">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
<style>{main_css}{CHROME_CSS}</style>
</head>
<body>
<nav class="site-top"><a href="../../">&larr; Field Notes</a></nav>
{body}
<footer class="site-foot">
  <span>&copy; 2026 Alice Xu</span>
  <span><a href="../../">Field Notes</a> &middot; built by hand</span>
</footer>
{ANALYTICS}
</body>
</html>
"""
    out = SITE / "posts" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out

if __name__ == "__main__":
    master = pathlib.Path(sys.argv[1]).expanduser()
    slug = sys.argv[2]
    desc = sys.argv[3] if len(sys.argv) > 3 else ""
    out = build(master, slug, desc)
    print("wrote", out, out.stat().st_size, "bytes")
