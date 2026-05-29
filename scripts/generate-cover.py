#!/usr/bin/env python3
"""
Generate book cover: Flesh Revelations: Ten Movements of Desire
Renders HTML → PNG via Playwright + local HTTP server
"""
import json, os, sys, shutil, threading, socket, http.server, time
from pathlib import Path
from PIL import Image

WORKSPACE = Path.home() / ".openclaw" / "workspace"
OUTPUT_DIR = WORKSPACE / "exports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COVER_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1800px; height: 2700px;
  background: #0a0a0a;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Times New Roman', 'Noto Serif SC', serif;
  overflow: hidden;
}
.cover {
  width: 1620px; height: 2430px;
  background: linear-gradient(145deg, #0d0d0d 0%, #1a1410 30%, #1a0d0a 60%, #0d0a08 100%);
  position: relative; overflow: hidden;
}
.cover::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.005) 2px, rgba(255,255,255,0.005) 4px);
  pointer-events: none;
}
.cover::after {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  box-shadow: inset 0 0 120px rgba(0,0,0,0.5);
  pointer-events: none;
}
.chinese-strip {
  position: absolute; right: 60px; top: 0; bottom: 0;
  writing-mode: vertical-rl;
  font-family: 'Noto Serif SC', 'SimSun', 'STSong', serif;
  font-size: 18px; letter-spacing: 12px;
  color: rgba(180, 140, 100, 0.12);
  padding: 100px 0; line-height: 2.2; text-orientation: upright;
}
.ornament {
  position: absolute; left: 80px; top: 240px;
  width: 1px; height: 300px;
  background: linear-gradient(to bottom, transparent, rgba(180,140,100,0.4), transparent);
}
.ornament-bottom {
  position: absolute; left: 80px; bottom: 320px;
  width: 1px; height: 300px;
  background: linear-gradient(to bottom, transparent, rgba(180,140,100,0.4), transparent);
}
.divider {
  position: absolute; left: 120px; right: 100px; height: 1px;
  background: linear-gradient(to right, transparent 0%, rgba(180,140,100,0.3) 30%, rgba(180,140,100,0.3) 70%, transparent 100%);
}
.divider-top { top: 580px; }
.divider-bottom { bottom: 580px; }
.dots {
  position: absolute; right: 120px; top: 50%; transform: translateY(-50%);
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; opacity: 0.06;
}
.dot { width: 4px; height: 4px; border-radius: 50%; background: #b48c64; }
.content {
  position: absolute; left: 120px; top: 50%; transform: translateY(-54%); max-width: 1000px;
}
.series {
  font-family: 'Arial', 'Helvetica', sans-serif;
  font-size: 10px; letter-spacing: 6px; text-transform: uppercase;
  color: rgba(180, 140, 100, 0.5); margin-bottom: 30px; font-weight: 300;
}
h1 {
  font-family: 'Times New Roman', 'Georgia', serif;
  font-size: 54px; font-weight: 300;
  color: #e8d5c0; line-height: 1.15; letter-spacing: 2px;
}
h1 .subtitle {
  display: block; font-size: 24px; font-weight: 300; font-style: italic;
  color: rgba(180, 140, 100, 0.7); margin-top: 18px; letter-spacing: 4px;
}
.tagline {
  font-family: 'Arial', 'Helvetica', sans-serif;
  font-size: 11px; font-weight: 200;
  color: rgba(180, 140, 100, 0.45); letter-spacing: 3px; text-transform: uppercase;
  margin-top: 36px; line-height: 1.6; max-width: 500px;
}
.author {
  position: absolute; bottom: 180px; left: 120px;
  font-family: 'Times New Roman', 'Georgia', serif;
  font-size: 16px; font-weight: 300;
  color: rgba(180, 140, 100, 0.6); letter-spacing: 8px; text-transform: uppercase;
}
.zh-title {
  position: absolute; left: 120px; top: 790px;
  font-family: 'Noto Serif SC', 'SimSun', serif;
  font-size: 14px; font-weight: 200; color: rgba(180, 140, 100, 0.2); letter-spacing: 6px;
}
.epigraph {
  position: absolute; right: 100px; bottom: 240px; max-width: 340px; text-align: right;
  font-family: 'Times New Roman', 'Georgia', serif;
  font-size: 13px; font-style: italic; font-weight: 300;
  color: rgba(180, 140, 100, 0.2); line-height: 1.6;
}
.accent-line {
  position: absolute; left: 120px; right: 120px; bottom: 360px; height: 1px;
  background: linear-gradient(to right, rgba(180,140,100,0.15), rgba(180,140,100,0.05));
}
</style>
</head>
<body>
<div class="cover">
  <div class="chinese-strip">肉体启示录 欲望的十种运动 存在主义的东方之路 身体的现象学 自由的真实路径</div>
  <div class="ornament"></div><div class="ornament-bottom"></div>
  <div class="divider divider-top"></div><div class="divider divider-bottom"></div>
  <div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
  <div class="content">
    <div class="series">A Literary-Philosophical Novel</div>
    <h1>Flesh Revelations<span class="subtitle">Ten Movements of Desire</span></h1>
    <div class="tagline">The body is not the prison of the soul<br>but the only true path to freedom and truth</div>
  </div>
  <div class="author">— A. N. —</div>
  <div class="zh-title">肉体·欲望·自由</div>
  <div class="epigraph">"Primitive, honest, and viscerally human stories<br>elevated into philosophical and poetic revelation."</div>
  <div class="accent-line"></div>
</div>
</body>
</html>"""

# Write HTML
html_path = OUTPUT_DIR / "book-cover.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(COVER_HTML)
print(f"[cover] HTML written: {html_path}")

# Start local HTTP server
def find_free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

port = find_free_port()
os.chdir(str(OUTPUT_DIR))
httpd = http.server.HTTPServer(("127.0.0.1", port), http.server.SimpleHTTPRequestHandler)
thread = threading.Thread(target=httpd.serve_forever, daemon=True)
thread.start()
time.sleep(0.3)
serve_url = f"http://127.0.0.1:{port}/book-cover.html"
print(f"[cover] Serving at {serve_url}")

# Render with Playwright
CHROMIUM = shutil.which("chromium-browser") or shutil.which("chromium") or shutil.which("google-chrome")
if not CHROMIUM:
    print("[cover] ❌ No Chromium found")
    sys.exit(1)
print(f"[cover] Using Chromium: {CHROMIUM}")

png_path = OUTPUT_DIR / "Flesh_Revelations_Cover.png"

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path=CHROMIUM,
        args=["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage",
              "--disable-setuid-sandbox", "--disable-software-rasterizer",
              "--disable-features=VizDisplayCompositor"],
    )
    context = browser.new_context(
        viewport={"width": 1800, "height": 2700},
        device_scale_factor=2,
        locale="en-US",
    )
    page = context.new_page()
    page.goto(serve_url, wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    page.screenshot(path=str(png_path), clip={"x": 0, "y": 0, "width": 1800, "height": 2700})
    browser.close()
    httpd.shutdown()

size_kb = os.path.getsize(png_path) // 1024
print(f"[cover] ✅ PNG: {png_path} ({size_kb}KB)")

# Smaller preview
jpg_path = OUTPUT_DIR / "Flesh_Revelations_Cover.jpg"
img = Image.open(png_path)
img.resize((600, 900), Image.LANCZOS).save(str(jpg_path), "JPEG", quality=85)
print(f"[cover] ✅ JPG preview: {jpg_path}")

print(f"\nCOVER_PATH:{png_path}")
