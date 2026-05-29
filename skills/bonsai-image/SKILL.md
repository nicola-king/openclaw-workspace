---
name: bonsai-image
version: 1.0.0
description: 太一 Bonsai Image 4B 集成 — 本地图生（1-bit/ternary 量化扩散模型）PrismML Apache 2.0
category: creativity
tags: ['bonsai', 'image-generation', 'local-ai', 'diffusion', 'art-agent', 'prismml', '1-bit', 'ternary']
author: 太一 AGI
created: 2026-05-29
status: active
trigger: 当需要生成图像/插图/封面/卡片时，自动识别硬件能力并路由到本地 Bonsai 或云端 API
---

# 🌲 Bonsai Image 4B — 太一本地图生引擎

> 基于 PrismML Bonsai Image 4B (1-bit / ternary)
> Apache 2.0 开源 · 本地运行 · 零成本 · 隐私全保

---

## 🧠 智能调度规则

太一系统自动识别以下条件，决策"本地 Bonsai" vs "云端 API"：

### 硬件检测
```
NVIDIA GPU / Apple Silicon → ✅ 本地 Bonsai（优先）
CPU-only                   → ⚠️ 可用但慢（4B 参数 CPU 推理 ≈ 30-60s/张）
无 PyTorch / 无加速库      → ⚡ 自动降级到云端/fallback
```

### 使用场景 → 自动匹配参数

| 场景 | 模型变体 | 分辨率 | 风格提示 | 优先级 |
|------|---------|--------|---------|-------|
| OERV 叙事插画 | ternary | 832×1248 | 文学性、水墨感、意境 | ⭐⭐⭐ |
| 日报封面图 | ternary | 1024×1024 | 数据新闻风、干净简洁 | ⭐⭐⭐ |
| 小红书卡片背景 | binary | 704×1408 | 小红书风格、明亮温暖 | ⭐⭐ |
| 公众号文章配图 | ternary | 1248×832 | 故事感、电影感 | ⭐⭐⭐ |
| 品牌素材/海报 | ternary | 1408×704 | 品牌调性、高级感 | ⭐⭐ |
| 快速预览/概念 | binary | 512×512 | 快速迭代 | ⭐ |

---

## 🔌 调用方式

### 一键命令

```
/图 一只在月光下飞翔的白鹿
/图 --style 水墨 --size 832x1248 雨中樱花
/图 --fast 概念设计草图 未来城市
/图 --card 小红书 极简主义家居
```

### Python API

```python
from skills.bonsai_image.bonsai import generate, smart_route

# 智能路由（自动检测硬件）
result = generate("月光下的一只白鹿", size=(832, 1248))

# 强制本地 Bonsai
result = generate("雨中樱花", force_local=True)

# 指定风格参数
result = generate("极简主义家居",
    style="minimalist", size=(1024, 1024),
    variant="ternary"  # ternary or binary
)

# 获取路由状态
status = smart_route()
# → {"hardware": "cpu", "available": True, "recommended": "cpu"}
```

### 命令行

```bash
# 检查硬件兼容性
python -m skills.bonsai_image check

# 生成图像
python -m skills.bonsai_image gen "月光飞鹿" --size 832x1248 --output /tmp/output.png

# 信息
python -m skills.bonsai_image info
```

---

## 📦 安装 & 下载模型

```bash
# 1. 克隆 demo 仓库获取设置脚本
git clone https://github.com/PrismML-Eng/Bonsai-Image-Demo.git /tmp/bonsai-demo

# 2. 安装依赖
cd /tmp/bonsai-demo && ./setup.sh

# 3. 下载模型权重（ternary 1.21GB / binary 0.93GB）
./scripts/download_model.sh ternary   # 或 binary

# 4. 软链接到太一 workspace
ln -sf /tmp/bonsai-demo/models ~/.openclaw/workspace/skills/bonsai-image/models/bonsai
```

**系统要求：**
- macOS: Apple Silicon (M1+) + MLX
- Linux: NVIDIA GPU + CUDA + gemlite/HQQ （或 CPU-only PyTorch，较慢）
- Windows: NVIDIA GPU + triton-windows
- 内存: ≥8GB
- 存储: ~2GB (模型权重)

---

## 🎨 与 art-agent 集成

Bonsai Image 已注册到 art-agent 的智能调度引擎：

```
art-agent 收到"生成配图"
  │
  ├─ → 检查 hardware.available
  │
  ├─ ✅ GPU/Metal → bonsai-image (本地)
  │     ├─ OERV 叙事 → 832×1248 ternary
  │     ├─ 日报封面 → 1024×1024 ternary
  │     └─ 小红书卡 → 704×1408 binary
  │
  └─ ❌ CPU-only → 告知"本地Bonsai慢, 是否继续?"
        └─ 用户确认 → CPU 推理 (30-60s)
        └─ 用户拒绝 → 用云端 API 生成
```

---

## 📊 模型规格

| 指标 | Binary (1-bit) | Ternary (1.58-bit) |
|------|:-:|:-:|
| 模型大小 | **0.93 GB** | **1.21 GB** |
| 压缩比 vs FP16 | 8.3× | 6.4× |
| 质量保留 | up to 95% | up to 95% |
| M4 Pro 512×512 | ~6s | ~6s |
| iPhone 17 Pro Max | ~9.4s | ~9.4s |
| CPU (本机 Intel N150) | ~30-60s | ~30-60s |
| 许可 | Apache 2.0 | Apache 2.0 |

---

## 📁 文件结构

```
skills/bonsai-image/
├── SKILL.md              ← 本文档
├── bonsai.py             ← 核心封装（generate/smart_route）
├── scripts/
│   └── setup.sh          ← 一键安装脚本
└── models/               ← 模型权重 (下载后)
    └── bonsai/
```

---

## 🔗 相关资源

- PrismML 官网: https://prismml.com
- GitHub: https://github.com/PrismML-Eng/Bonsai-Image-Demo
- HuggingFace: https://huggingface.co/collections/prism-ml/bonsai-image
- WebGPU Demo: https://huggingface.co/spaces/webml-community/bonsai-image-webgpu
- iOS App: https://apps.apple.com/us/app/bonsai-studio-by-prismml/id6767042620
- 白皮书: https://github.com/PrismML-Eng/Bonsai-Image-Demo/blob/main/bonsai-image-4b-whitepaper.pdf
