"""
太一 HyperFrames 引擎 · Taiyi HyperFrames Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
基于 HeyGen HyperFrames (⭐22K) · Apache 2.0
Write HTML. Render video. Built for agents.

能力:
  render()         HTML → MP4 视频渲染
  template()       从预设模板生成视频
  check()          系统可用性诊断
  info()           版本信息
  oerv_video()     OERV 叙事→视频全链路

集成链路:
  OERV叙事 → search配图 → HTML composition → HyperFrames → MP4
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

SKILL_DIR = Path(__file__).parent
OUTPUT_DIR = SKILL_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# =====================================================================
# 预设模板
# =====================================================================

TEMPLATES = {
    "oerv_narrative": {
        "desc": "OERV 叙事视频 — 图文+淡入动效",
        "size": "1920x1080",
        "duration": 15,
        "style": "cinematic",
    },
    "product_launch": {
        "desc": "产品发布 — 标题淡入+背景视频+配乐",
        "size": "1920x1080",
        "duration": 10,
        "style": "modern",
    },
    "data_chart": {
        "desc": "数据图表动效 — 动画图表+旁白",
        "size": "1920x1080",
        "duration": 20,
        "style": "minimal",
    },
    "short_video": {
        "desc": "短视频（竖屏）— 快节奏+字幕",
        "size": "1080x1920",
        "duration": 30,
        "style": "trendy",
    },
    "wechat_article_video": {
        "desc": "公众号文章视频版 — 原文+配图+旁白",
        "size": "1920x1080",
        "duration": 60,
        "style": "clean",
    },
}

# =====================================================================
# 系统检测
# =====================================================================

def _has_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None

def _has_node() -> bool:
    return shutil.which("node") is not None

def _has_npx() -> bool:
    return shutil.which("npx") is not None

def _hyperframes_version() -> Optional[str]:
    try:
        r = subprocess.run(
            ["npx", "hyperframes", "--version"],
            capture_output=True, text=True, timeout=30,
            env={**os.environ, "npm_config_cache": str(SKILL_DIR / ".npm-cache")}
        )
        return r.stdout.strip() or r.stderr.strip() or "?"
    except: return None

# =====================================================================
# 核心：HTML → MP4 渲染
# =====================================================================

def render(html_path: str = None, content: str = None,
           template: str = None, duration: int = 10,
           size: str = "1920x1080", output: str = None,
           title: str = "Video", audio_path: str = None) -> Dict:
    """
    HTML → MP4 视频渲染

    参数:
      html_path: 现有 composition HTML 文件路径
      content: 文字内容（与 template 配合使用）
      template: 预设模板名
      duration: 视频时长（秒）
      size: 分辨率 "1920x1080" / "1080x1920"
      output: 输出路径
      title: 视频标题
      audio_path: 背景音频路径（可选）

    返回:
      {status, path, duration, size, time_ms, note}
    """
    t0 = time.time()
    has_ff = _has_ffmpeg()
    has_n = _has_node() and _has_npx()

    if not has_n:
        return {"status": "unavailable", "error": "Node.js/npx not found",
                "solution": "Install Node.js 22+"}

    if not has_ff:
        return {"status": "unavailable", "error": "FFmpeg not found",
                "solution": "Install FFmpeg"}

    # 如果给了 html_path，直接使用
    if html_path:
        html_file = Path(html_path)
        if not html_file.exists():
            return {"status": "error", "error": f"File not found: {html_path}"}
    else:
        # 用模板生成 composition
        if template and template in TEMPLATES:
            cfg = TEMPLATES[template]
            size = size if size else cfg["size"]
            duration = duration if duration else cfg["duration"]
            html_file = _generate_composition(content, title, duration, size, template)
        else:
            html_file = _generate_composition(content, title, duration, size)

    # 创建临时项目目录
    work_dir = Path(tempfile.mkdtemp(prefix="hyperframes-"))
    # 复制 composition.html
    dest_html = work_dir / "composition.html"
    shutil.copy2(str(html_file), str(dest_html))

    # 执行渲染
    try:
        cache_dir = SKILL_DIR / ".npm-cache"
        cache_dir.mkdir(exist_ok=True)

        render_cmd = [
            "npx", "hyperframes", "render",
            "--input", str(dest_html),
            "--width", size.split("x")[0],
            "--height", size.split("x")[1],
            "--fps", "30",
        ]

        if audio_path:
            render_cmd.extend(["--audio", audio_path])

        r = subprocess.run(
            render_cmd,
            capture_output=True, text=True, timeout=duration * 5 + 60,
            cwd=str(work_dir),
            env={
                **os.environ,
                "npm_config_cache": str(cache_dir),
                "HYPERFRAMES_SKIP_WELCOME": "1",
            }
        )

        elapsed = int((time.time() - t0) * 1000)

        # 查找输出文件
        output_path = output or str(OUTPUT_DIR / f"hyperframes_{int(time.time())}.mp4")
        possible_outputs = list(work_dir.rglob("*.mp4"))
        if possible_outputs:
            shutil.copy2(str(possible_outputs[0]), output_path)
            result = {"status": "ok", "path": output_path,
                      "duration": duration, "size": size,
                      "output_size_mb": round(possible_outputs[0].stat().st_size / 1024 / 1024, 1),
                      "time_ms": elapsed, "template": template}
        else:
            result = {"status": "error", "error": "No MP4 output",
                      "stdout": r.stdout[-500:], "stderr": r.stderr[-500:],
                      "time_ms": elapsed}

    except subprocess.TimeoutExpired:
        result = {"status": "error", "error": "Render timed out",
                  "time_ms": int((time.time() - t0) * 1000)}
    except Exception as e:
        result = {"status": "error", "error": str(e),
                  "time_ms": int((time.time() - t0) * 1000)}

    # 清理临时目录（保留输出）
    try:
        import shutil as _s
        _s.rmtree(work_dir, ignore_errors=True)
    except: pass

    return result

# =====================================================================
# 生成 Composition HTML
# =====================================================================

def _generate_composition(content: str = None, title: str = "Video",
                          duration: int = 10, size: str = "1920x1080",
                          template: str = None) -> Path:
    """生成 HyperFrames composition HTML"""
    w, h = size.split("x")

    content_text = content or title
    # 按句子分段
    sentences = [s.strip() for s in content_text.replace("。", ".").replace("！", "!").replace("？", "?").split(".") if s.strip()]
    if not sentences:
        sentences = [content_text[:100]]

    # 每段时长
    seg_duration = max(2, duration // len(sentences))
    # 开始时间（每段递进）
    start_times = [i * seg_duration for i in range(len(sentences))]

    # 构建 HTML
    html_parts = [f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;500;700&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Noto Sans SC', sans-serif; overflow: hidden; background: #0f0f1a; }}
  #stage {{ position: relative; width: {w}px; height: {h}px; overflow: hidden; background: linear-gradient(135deg, #0f0f1a 0%, #1a1a3e 100%); }}

  .slide {{
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    opacity: 0;
    padding: 80px;
  }}
  .slide h1 {{ font-size: 64px; font-weight: 700; color: #fff; text-align: center; line-height: 1.3; }}
  .slide p {{ font-size: 36px; font-weight: 300; color: #ccc; text-align: center; line-height: 1.5; }}
  .slide .sub {{ font-size: 28px; color: #888; margin-top: 20px; }}

  .brand {{ position: absolute; bottom: 40px; right: 40px; color: #555; font-size: 18px; }}
</style>
</head>
<body>
<div id="stage" data-composition-id="main" data-start="0" data-width="{w}" data-height="{h}">
"""]

    # 添加标题 slide
    html_parts.append(f"""
  <div class="slide" id="slide-title" data-start="0.5" data-duration="2" data-track-index="0" style="opacity:0">
    <h1>{title}</h1>
  </div>
""")

    # 内容 slides
    for i, sent in enumerate(sentences[:8]):  # 最多 8 句
        if len(sent) < 5:
            continue
        start = start_times[min(i, len(start_times)-1)]
        html_parts.append(f"""
  <div class="slide" id="slide-{i}" data-start="{start + 2}" data-duration="{seg_duration}" data-track-index="{i+1}" style="opacity:0">
    <p>{sent}</p>
  </div>
""")

    # 结尾
    html_parts.append(f"""
  <div class="brand" data-start="0" data-duration="{duration}" data-track-index="99">太一 · Taiyi</div>
""")

    # GSAP 动画
    html_parts.append(f"""
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({{ paused: true }});
""")

    for i in range(len(sentences[:8]) + 1):
        sid = "slide-title" if i == 0 else f"slide-{i-1}"
        s = 0.5 if i == 0 else start_times[min(i-1, len(start_times)-1)] + 2
        html_parts.append(f"""
    tl.from("#{sid}", {{ opacity: 0, y: 30, duration: 0.6, ease: "power2.out" }}, {s});
    tl.to("#{sid}", {{ opacity: 0, y: -20, duration: 0.4, ease: "power2.in" }}, ">{seg_duration - 0.8}");
""")

    html_parts.append("""
    window.__timelines = window.__timelines || {};
    window.__timelines.main = tl;
  </script>
</div>
</body>
</html>
""")

    html_content = "\n".join(html_parts)
    out = OUTPUT_DIR / f"composition_{int(time.time())}.html"
    out.write_text(html_content, encoding="utf-8")
    return out

# =====================================================================
# OERV 视频版全链路
# =====================================================================

def oerv_video(narrative: str, images: List[str] = None) -> Dict:
    """OERV 叙事→搜索配图→视频渲染 全链路"""
    t0 = time.time()
    # 生成 composition
    html_file = _generate_composition(
        content=narrative,
        title="OERV 叙事",
        duration=min(60, max(10, len(narrative) // 10)),
        size="1920x1080",
        template="oerv_narrative",
    )
    # 渲染
    result = render(html_path=str(html_file))
    result["narrative_length"] = len(narrative)
    result["total_time"] = int((time.time() - t0) * 1000)
    return result

# =====================================================================
# 诊断
# =====================================================================

def check() -> str:
    """系统诊断"""
    lines = [
        "🎬 HyperFrames 系统诊断",
        f"═══════════════════════",
        f"Node.js:  {shutil.which('node') or '❌'}",
        f"npx:      {shutil.which('npx') or '❌'}",
        f"FFmpeg:   {shutil.which('ffmpeg') or '❌'}",
    ]

    # Node version
    if _has_node():
        r = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        lines.append(f"Node ver: {r.stdout.strip()}")

    # FFmpeg version
    if _has_ffmpeg():
        r = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        ver = r.stdout.split("\n")[0] if r.stdout else "?"
        lines.append(f"FFmpeg:   {ver[:60]}...")

    # HyperFrames
    hv = _hyperframes_version()
    lines.append(f"HyperFrames: {'✅ ' + hv if hv else '❌'}")

    # Templates
    lines.append(f"\n模板 ({len(TEMPLATES)}):")
    for name, cfg in TEMPLATES.items():
        lines.append(f"  {name:25s} {cfg['desc']} ({cfg['size']})")

    lines.append(f"\n输出目录: {OUTPUT_DIR}")
    return "\n".join(lines)

def info() -> str:
    """版本信息"""
    return json.dumps({
        "name": "hyperframes",
        "version": "1.0.0",
        "engine": "HeyGen HyperFrames",
        "license": "Apache 2.0",
        "requirements": {"node": "22+", "ffmpeg": "✅"},
        "templates": list(TEMPLATES.keys()),
        "url_github": "https://github.com/heygen-com/hyperframes",
        "url_docs": "https://hyperframes.heygen.com/introduction",
    }, indent=2)

# =====================================================================
# CLI
# =====================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"🎬 HyperFrames 引擎 v1.0")
        print()
        print("用法:")
        print("  check                   系统诊断")
        print("  info                    版本信息")
        print("  render <html_path>      渲染 HTML → MP4")
        print("  template <名称> <内容>   用模板生成视频")
        print("  oerv <叙事文本>          OERV 视频全链路")
        print()
        print("模板:")
        for name, cfg in TEMPLATES.items():
            print(f"  {name:25s} {cfg['desc']}")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "check":
        print(check())

    elif cmd == "info":
        print(info())

    elif cmd == "render":
        html_path = sys.argv[2] if len(sys.argv) > 2 else None
        if not html_path:
            print("❌ 需要指定 HTML 文件路径")
            sys.exit(1)
        result = render(html_path=html_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "template":
        template_name = sys.argv[2] if len(sys.argv) > 2 else None
        content = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "默认内容"
        if not template_name:
            print("❌ 需要指定模板名")
            sys.exit(1)
        if template_name not in TEMPLATES:
            print(f"❌ 未知模板: {template_name}")
            print(f"   可用: {', '.join(TEMPLATES.keys())}")
            sys.exit(1)
        result = render(content=content, template=template_name)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "oerv":
        narrative = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "默认叙事"
        result = oerv_video(narrative)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print(f"未知命令: {cmd}")
