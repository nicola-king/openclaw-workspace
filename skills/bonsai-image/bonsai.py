"""
太一 Bonsai Image 4B 引擎 · Taiyi Bonsai Image Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
基于 PrismML Bonsai Image 4B (1-bit / ternary diffusion)
Apache 2.0 · 本地运行 · 零成本 · 隐私全保

能力:
  generate()      智能图生（自动检测硬件 + 选择最优变体）
  smart_route()   检测硬件能力 → 返回推荐方案
  check_hardware() 打印系统诊断
  info()          模型信息
"""

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

SKILL_DIR = Path(__file__).parent
MODELS_DIR = SKILL_DIR / "models"
OUTPUT_DIR = SKILL_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

VERSION = "1.0.0"

# =====================================================================
# 使用场景 → 参数映射（智能匹配核心）
# =====================================================================

SCENE_MAP = {
    "oerv_narrative": {
        "variant": "ternary",
        "size": (832, 1248),
        "style": "literary, ink-wash, poetic, atmospheric",
        "desc": "OERV 叙事插画 — 文学性、水墨感、意境",
    },
    "daily_cover": {
        "variant": "ternary",
        "size": (1024, 1024),
        "style": "data-journalism, clean, modern, minimalist",
        "desc": "日报封面 — 数据新闻风、干净简洁",
    },
    "xiaohongshu_card": {
        "variant": "binary",
        "size": (704, 1408),
        "style": "xiaohongshu-style, warm, bright, trendy",
        "desc": "小红书卡片背景 — 明亮温暖、时尚",
    },
    "wechat_article": {
        "variant": "ternary",
        "size": (1248, 832),
        "style": "cinematic, storytelling, evocative",
        "desc": "公众号文章配图 — 故事感、电影感",
    },
    "brand_poster": {
        "variant": "ternary",
        "size": (1408, 704),
        "style": "brand, premium, sophisticated, clean",
        "desc": "品牌海报 — 高级感、品牌调性",
    },
    "quick_preview": {
        "variant": "binary",
        "size": (512, 512),
        "style": "",
        "desc": "快速预览 — 概念迭代不纠结质量",
    },
}

SIZE_MAP = {
    "512": (512, 512),
    "1024": (1024, 1024),
    "square": (512, 512),
    "landscape": (1248, 832),
    "portrait": (832, 1248),
    "wide": (1408, 704),
    "tall": (704, 1408),
    "card": (704, 1408),
}

# =====================================================================
# 硬件检测
# =====================================================================

def _has_nvidia_gpu() -> bool:
    """检查是否有 NVIDIA GPU"""
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                          capture_output=True, text=True, timeout=5)
        return r.returncode == 0 and "NVIDIA" in r.stdout
    except: return False

def _has_apple_silicon() -> bool:
    """检查 Apple Silicon"""
    if platform.system() != "Darwin":
        return False
    try:
        r = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                          capture_output=True, text=True, timeout=3)
        return "Apple" in r.stdout
    except: return False

def _has_pytorch() -> bool:
    """检查 PyTorch 是否可用"""
    try:
        import torch
        return True
    except ImportError:
        return False

def _has_mlx() -> bool:
    """检查 MLX 是否可用 (macOS)"""
    try:
        import mlx.core
        return True
    except ImportError:
        return False

def _model_downloaded() -> bool:
    """检查模型是否已下载"""
    # 检查各种可能的模型路径
    model_paths = [
        MODELS_DIR / "bonsai" / "bonsai-image-4B-ternary-gemlite",
        MODELS_DIR / "bonsai" / "bonsai-image-4B-ternary-mlx",
        MODELS_DIR / "bonsai" / "bonsai-image-4B-binary-gemlite",
        MODELS_DIR / "bonsai" / "bonsai-image-4B-binary-mlx",
        Path("/tmp/bonsai-demo/models"),
    ]
    for p in model_paths:
        if p.exists() and any(p.iterdir()):
            return True
    return False

# =====================================================================
# 智能路由
# =====================================================================

def smart_route() -> Dict:
    """
    检测系统能力 → 返回推荐方案

    返回:
      {
        hardware: "nvidia" | "apple-silicon" | "cpu" | "none",
        pytorch: bool,
        mlx: bool (macOS only),
        model_available: bool,
        recommended: "local" | "cpu" | "unavailable",
        note: str
      }
    """
    has_nvidia = _has_nvidia_gpu()
    has_apple = _has_apple_silicon()
    has_torch = _has_pytorch()
    has_mlx = _has_mlx()
    model_ok = _model_downloaded()

    if has_nvidia:
        return {
            "hardware": "nvidia",
            "pytorch": has_torch,
            "mlx": False,
            "model_available": model_ok,
            "recommended": "local",
            "note": "✅ NVIDIA GPU 可用 — 推荐本地 Bonsai (gemlite+HQQ)"
        }

    if has_apple and has_mlx:
        return {
            "hardware": "apple-silicon",
            "pytorch": has_torch,
            "mlx": True,
            "model_available": model_ok,
            "recommended": "local",
            "note": "✅ Apple Silicon + MLX 可用 — 推荐本地 Bonsai (MLX)"
        }

    if has_torch:
        return {
            "hardware": "cpu",
            "pytorch": True,
            "mlx": False,
            "model_available": model_ok,
            "recommended": "cpu",
            "note": "⚠️ CPU-only — 可用但慢 (~30-60s/张)。有 GPU 建议用 Googe Colab / cloud"
        }

    return {
        "hardware": "none",
        "pytorch": False,
        "mlx": False,
        "model_available": model_ok,
        "recommended": "unavailable",
        "note": "❌ 无 PyTorch 且无 GPU — 本地 Bonsai 不可用。安装: pip install torch"
    }

# =====================================================================
# 图像生成（核心）
# =====================================================================

def generate(prompt: str,
             size: Union[str, Tuple[int, int]] = "square",
             variant: str = "auto",
             scene: str = None,
             style: str = None,
             output: str = None,
             force_local: bool = False,
             seed: int = None) -> Dict:
    """
    智能图像生成 — 自动检测硬件 + 选择最优变体

    参数:
      prompt: 提示词 (可以包含 style 描述)
      size: "square"/"landscape"/"portrait"/"wide"/"tall"/"card"/"512"/"1024" 或 (w,h) 元组
      variant: "auto"/"ternary"/"binary" (auto=硬件决定)
      scene: 场景名 → 自动匹配 size/variant/style (见 SCENE_MAP)
      style: 额外风格提示词
      output: 输出路径 (默认 auto)
      force_local: 强制本地生成 (即使硬件不支持也尝试)
      seed: 随机种子 (固定结果)

    返回:
      {status, path, size, variant, hardware, time_ms, note}
    """
    route = smart_route()
    t0 = time.time()

    # === 场景匹配 ===
    if scene and scene in SCENE_MAP:
        scene_cfg = SCENE_MAP[scene]
        variant = scene_cfg["variant"]
        if isinstance(size, str) and size in ["square", "1024"]:
            size = scene_cfg["size"]
        if not style:
            style = scene_cfg.get("style", "")

    # === 尺寸解析 ===
    if isinstance(size, str):
        size = SIZE_MAP.get(size.lower(), SIZE_MAP["square"])

    variant = variant if variant != "auto" else (
        "binary" if route["hardware"] == "cpu" else "ternary"
    )

    # === 提示词处理 ===
    full_prompt = prompt
    if style:
        full_prompt = f"{prompt}, {style}"

    # === 硬件检查 ===
    if route["recommended"] == "unavailable" and not force_local:
        elapsed = int((time.time() - t0) * 1000)
        return {
            "status": "unavailable",
            "prompt": prompt,
            "size": size,
            "variant": variant,
            "time_ms": elapsed,
            "note": route["note"],
            "hardware": route["hardware"],
            "solution": "安装 PyTorch (pip install torch) 或用 WebGPU Demo: https://huggingface.co/spaces/webml-community/bonsai-image-webgpu",
        }

    # === 生成（走 Bonsai pipeline） ===
    output_path = output or str(OUTPUT_DIR / f"bonsai_{int(time.time())}.png")

    # TODO: 实际调用 Bonsai inference
    # 当模型下载+GPU就绪后:
    #   run subprocess with generate.sh
    # 目前返回 placeholder

    elapsed = int((time.time() - t0) * 1000)
    return {
        "status": "pending_model_download",
        "prompt": full_prompt,
        "size": size,
        "variant": variant,
        "scene": scene,
        "hardware": route["hardware"],
        "time_ms": elapsed,
        "output": output_path,
        "note": "模型未下载。请先运行: cd skills/bonsai-image && bash scripts/setup.sh",
        "download_cmd": "git clone https://github.com/PrismML-Eng/Bonsai-Image-Demo.git /tmp/bonsai-demo && cd /tmp/bonsai-demo && ./setup.sh && ./scripts/download_model.sh ternary",
    }

# =====================================================================
# 信息 / 诊断
# =====================================================================

def check_hardware() -> str:
    """打印硬件诊断"""
    route = smart_route()
    lines = [
        f"🌲 Bonsai Image {VERSION}",
        f"═══════════════════",
        f"OS: {platform.system()} {platform.machine()}",
        f"PyTorch: {'✅' if route['pytorch'] else '❌'} {'(' + __import__('torch').__version__ + ')' if route['pytorch'] else ''}",
        f"MLX: {'✅' if route['mlx'] else '❌'}",
        f"NVIDIA GPU: {'✅' if route['hardware'] == 'nvidia' else '❌'}",
        f"Apple Silicon: {'✅' if route['hardware'] == 'apple-silicon' else '❌'}",
        f"Model Downloaded: {'✅' if route['model_available'] else '❌'}",
        f"",
        f"Recommended: {route['recommended']}",
        f"Note: {route['note']}",
    ]
    return "\n".join(lines)

def info() -> str:
    """模型信息"""
    return json.dumps({
        "model": "Bonsai Image 4B",
        "source": "PrismML",
        "license": "Apache 2.0",
        "variants": {
            "ternary": {"size_gb": 1.21, "bits": 1.58, "compression": "6.4×"},
            "binary": {"size_gb": 0.93, "bits": 1.0, "compression": "8.3×"},
        },
        "capabilities": list(SCENE_MAP.keys()),
        "hardware_required": "NVIDIA GPU / Apple Silicon / CPU (slow)",
        "url_github": "https://github.com/PrismML-Eng/Bonsai-Image-Demo",
        "url_huggingface": "https://huggingface.co/collections/prism-ml/bonsai-image",
        "url_webgpu_demo": "https://huggingface.co/spaces/webml-community/bonsai-image-webgpu",
    }, indent=2)

# =====================================================================
# CLI
# =====================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"🌲 Bonsai Image {VERSION}")
        print()
        print("用法:")
        print("  python -m skills.bonsai_image.bonsai check       硬件诊断")
        print("  python -m skills.bonsai_image.bonsai info        模型信息")
        print("  python -m skills.bonsai_image.bonsai gen <提示>   生成图像")
        print()
        print("场景预设:")
        for k, v in SCENE_MAP.items():
            print(f"  {k:20s} {v['desc']} ({v['size'][0]}×{v['size'][1]})")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "check":
        print(check_hardware())

    elif cmd == "info":
        print(info())

    elif cmd == "gen":
        prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "a beautiful landscape"
        r = generate(prompt)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    elif cmd == "scene" and len(sys.argv) > 2:
        scene_name = sys.argv[2]
        prompt = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "default scene"
        r = generate(prompt, scene=scene_name)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
