#!/usr/bin/env python3
"""
Generate book cover v2: Flesh Revelations
Design: 含苞花蕾 + 英文排印 + 暗影张力
"""
import os, shutil, threading, socket, http.server, time, json
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
  background: #060606;
  display: flex; align-items: center; justify-content: center;
  font-family: Georgia, 'Times New Roman', serif;
  overflow: hidden;
}
.cover {
  width: 1620px; height: 2430px;
  position: relative; overflow: hidden;
  background: radial-gradient(ellipse at 50% 65%, #1a0d08 0%, #0d0806 40%, #060404 70%, #000 100%);
}

/* Grain texture */
.cover::before {
  content: '';
  position: absolute; inset: 0;
  background: repeating-conic-gradient(rgba(255,255,255,0.003) 0% 25%, transparent 0% 50%) 0 0 / 4px 4px;
  pointer-events: none; z-index: 5;
}
.cover::after {
  content: '';
  position: absolute; inset: 0;
  box-shadow: inset 0 0 200px rgba(0,0,0,0.6);
  pointer-events: none; z-index: 5;
}

/* Subtle backlight from bottom */
.backlight {
  position: absolute; bottom: -200px; left: 50%; transform: translateX(-50%);
  width: 800px; height: 600px;
  background: radial-gradient(ellipse, rgba(180,100,60,0.08) 0%, transparent 70%);
  z-index: 0;
}

/* ===== FLOWER BUD SVG ===== */
.flower-container {
  position: absolute;
  left: 50%; top: 48%;
  transform: translate(-50%, -55%);
  width: 520px; height: 680px;
  z-index: 2;
}
.flower-bud svg {
  width: 100%; height: 100%;
  display: block;
}

/* Stem reaching down */
.stem-line {
  position: absolute;
  left: 50%; top: 72%;
  width: 2px; height: 180px;
  transform: translateX(-50%);
  background: linear-gradient(to bottom, rgba(140,110,80,0.4), rgba(140,110,80,0.05));
  z-index: 1;
}

/* Subtle leaf */
.leaf {
  position: absolute;
  left: 52%; top: 78%;
  width: 60px; height: 30px;
  border-radius: 0 50% 50% 50%;
  background: rgba(100,120,80,0.12);
  transform: rotate(-15deg);
  z-index: 1;
}
.leaf2 {
  position: absolute;
  left: 44%; top: 82%;
  width: 50px; height: 25px;
  border-radius: 50% 0 50% 50%;
  background: rgba(100,120,80,0.08);
  transform: rotate(20deg);
  z-index: 1;
}

/* ===== TYPOGRAPHY ===== */
.typography {
  position: absolute;
  z-index: 4;
  text-align: center;
  width: 100%;
}

/* Top epigraph */
.epigraph-top {
  top: 80px;
  font-family: 'Georgia', 'Times New Roman', serif;
  font-size: 11px;
  font-style: italic;
  letter-spacing: 4px;
  color: rgba(180, 140, 100, 0.2);
  text-transform: uppercase;
}

/* Title area - BELOW the flower */
.title-area {
  position: absolute;
  bottom: 280px;
  left: 0; right: 0;
  text-align: center;
  z-index: 4;
}

.series-line {
  font-family: 'Arial', 'Helvetica', sans-serif;
  font-size: 9px;
  letter-spacing: 8px;
  text-transform: uppercase;
  color: rgba(180, 140, 100, 0.3);
  font-weight: 400;
  margin-bottom: 16px;
}

.main-title {
  font-family: 'Georgia', 'Times New Roman', serif;
  font-size: 46px;
  font-weight: 400;
  color: #d4c5b0;
  letter-spacing: 6px;
  line-height: 1.2;
  text-transform: uppercase;
}

.subtitle {
  display: block;
  font-family: 'Georgia', 'Times New Roman', serif;
  font-size: 16px;
  font-weight: 300;
  font-style: italic;
  color: rgba(180, 140, 100, 0.5);
  letter-spacing: 5px;
  margin-top: 14px;
}

.title-divider {
  width: 40px;
  height: 1px;
  background: rgba(180, 140, 100, 0.25);
  margin: 22px auto;
}

.tagline-bottom {
  font-family: 'Arial', 'Helvetica', sans-serif;
  font-size: 9px;
  font-weight: 300;
  color: rgba(180, 140, 100, 0.2);
  letter-spacing: 3px;
  line-height: 1.8;
  max-width: 480px;
  margin: 0 auto;
}

.author-line {
  position: absolute;
  bottom: 120px;
  left: 0; right: 0;
  text-align: center;
  z-index: 4;
  font-family: 'Georgia', 'Times New Roman', serif;
  font-size: 11px;
  letter-spacing: 10px;
  color: rgba(180, 140, 100, 0.25);
  text-transform: uppercase;
}

/* Light dust particles */
.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255,200,150,0.04);
  pointer-events: none;
  z-index: 1;
}
.p1 { width: 3px; height: 3px; top: 20%; left: 15%; }
.p2 { width: 2px; height: 2px; top: 30%; right: 20%; }
.p3 { width: 4px; height: 4px; top: 60%; left: 10%; }
.p4 { width: 2px; height: 2px; bottom: 30%; right: 12%; }
.p5 { width: 3px; height: 3px; top: 12%; right: 35%; }
</style>
</head>
<body>
<div class="cover">
  <div class="backlight"></div>

  <!-- Epigraph -->
  <div class="epigraph-top">a literary-philosophical novel</div>

  <!-- Particles -->
  <div class="particle p1"></div>
  <div class="particle p2"></div>
  <div class="particle p3"></div>
  <div class="particle p4"></div>
  <div class="particle p5"></div>

  <!-- Flower bud SVG -->
  <div class="flower-container">
    <div class="flower-bud">
      <svg viewBox="0 0 520 680" xmlns="http://www.w3.org/2000/svg">
        <!-- Stem -->
        <path d="M260 420 Q258 500 260 600" stroke="rgba(140,110,80,0.15)" stroke-width="2.5" fill="none"/>
        
        <!-- Sepal / outer petals (closed bud) -->
        <path d="M260 420 Q220 360 200 380 Q220 340 260 340 Q300 340 320 380 Q300 360 260 420Z" 
              fill="rgba(140,100,80,0.18)" stroke="none"/>
        
        <!-- Left outer petal wrapping -->
        <path d="M260 380 Q200 350 175 320 Q165 290 195 265 Q220 250 245 270 Q255 280 260 300 Q260 340 260 380Z"
              fill="rgba(160,120,90,0.12)" stroke="none"/>
        
        <!-- Right outer petal wrapping -->
        <path d="M260 380 Q320 350 345 320 Q355 290 325 265 Q300 250 275 270 Q265 280 260 300 Q260 340 260 380Z"
              fill="rgba(160,120,90,0.10)" stroke="none"/>
        
        <!-- Main bud body - central closed shape -->
        <path d="M260 360 Q230 310 225 270 Q220 230 235 200 Q250 175 260 170 Q270 175 285 200 Q300 230 295 270 Q290 310 260 360Z"
              fill="rgba(180,140,110,0.06)" stroke="rgba(180,140,110,0.12)" stroke-width="1"/>
        
        <!-- Inner bud highlight -->
        <path d="M260 340 Q245 300 242 270 Q240 240 248 220 Q254 205 260 200 Q266 205 272 220 Q280 240 278 270 Q275 300 260 340Z"
              fill="rgba(200,170,140,0.03)" stroke="none"/>
        
        <!-- Tip of bud (slightly open, hint of what's inside) -->
        <path d="M260 170 Q252 160 250 145 Q248 130 255 120 Q260 115 265 120 Q272 130 270 145 Q268 160 260 170Z"
              fill="rgba(200,160,130,0.05)" stroke="none"/>
        
        <!-- Tiny hint of color peeking through the tip -->
        <ellipse cx="260" cy="125" rx="4" ry="6" fill="rgba(200,100,80,0.06)"/>
        
        <!-- Subtle vein lines on left petal -->
        <path d="M245 270 Q225 240 220 210" stroke="rgba(180,140,110,0.04)" stroke-width="0.5" fill="none"/>
        <path d="M250 300 Q235 270 230 240" stroke="rgba(180,140,110,0.03)" stroke-width="0.5" fill="none"/>
        
        <!-- Subtle vein lines on right petal -->
        <path d="M275 270 Q295 240 300 210" stroke="rgba(180,140,110,0.04)" stroke-width="0.5" fill="none"/>
        <path d="M270 300 Q285 270 290 240" stroke="rgba(180,140,110,0.03)" stroke-width="0.5" fill="none"/>
        
        <!-- Delicate glow at the heart -->
        <ellipse cx="260" cy="250" rx="12" ry="20" fill="rgba(220,180,140,0.02)"/>
      </svg>
    </div>
  </div>
  <div class="stem-line"></div>
  <div class="leaf"></div>
  <div class="leaf2"></div>

  <!-- Title area -->
  <div class="title-area">
    <div class="series-line">a novel of the body and its truths</div>
    <div class="main-title">
      flesh<br>revelations
    </div>
    <span class="subtitle">ten movements of desire</span>
    <div class="title-divider"></div>
    <div class="tagline-bottom">
      the body is not the prison of the soul<br>
      but the only true path to freedom and truth
    </div>
  </div>

  <!-- Author -->
  <div class="author-line">a. n.</div>
</div>
</body>
</html>"""

# Write HTML
html_path = OUTPUT_DIR / "book-cover-v2.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(COVER_HTML)
print(f"[cover v2] HTML: {html_path}")

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
serve_url = f"http://127.0.0.1:{port}/book-cover-v2.html"
print(f"[cover v2] Serving: {serve_url}")

# Render
from playwright.sync_api import sync_playwright
CHROMIUM = shutil.which("chromium-browser") or shutil.which("chromium") or shutil.which("google-chrome")

png_path = OUTPUT_DIR / "Flesh_Revelations_Cover_v2.png"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True, executable_path=CHROMIUM,
        args=["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage",
              "--disable-setuid-sandbox", "--disable-software-rasterizer"],
    )
    page = browser.new_page(viewport={"width": 1800, "height": 2700}, device_scale_factor=2)
    page.goto(serve_url, wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    page.screenshot(path=str(png_path), clip={"x": 0, "y": 0, "width": 1800, "height": 2700})
    browser.close()
    httpd.shutdown()

size_kb = os.path.getsize(png_path) // 1024
print(f"[cover v2] ✅ PNG: {png_path} ({size_kb}KB)")

# Smaller preview
jpg_path = OUTPUT_DIR / "Flesh_Revelations_Cover_v2.jpg"
Image.open(png_path).resize((600, 900), Image.LANCZOS).save(str(jpg_path), "JPEG", quality=85)
print(f"[cover v2] ✅ JPG: {jpg_path}")

print(f"\nCOVER_PATH:{png_path}")
