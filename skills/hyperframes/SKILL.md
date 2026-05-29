---
name: hyperframes
version: 1.0.0
description: 太一 HyperFrames 集成 — HTML→视频渲染引擎（HeyGen 开源，Apache 2.0）
category: creativity
tags: ['hyperframes', 'video', 'animation', 'html-to-video', 'heygen', 'oerv', 'content-pipeline']
author: 太一 AGI
created: 2026-05-29
status: active
trigger: 当需要生成视频/动画/短视频/产品演示/OERV视频版时，自动识别并路由到 HyperFrames
---

# 🎬 HyperFrames — 太一视频渲染引擎

> 基于 HeyGen HyperFrames (⭐22K) · Apache 2.0
> Write HTML. Render video. Built for agents.

---

## 🧠 智能调度规则

太一系统自动识别以下场景，决策"静态 HTML" vs "动态视频"：

### 使用场景 → 自动匹配

| 场景 | 输出 | 路由 | 说明 |
|------|------|------|------|
| **OERV 公众号文章** | 图文 | art-agent HTML | 静态发布 |
| **OERV 视频版** | MP4 | hyperframes | 叙事→视频自动转 |
| **产品演示/发布** | MP4 | hyperframes | GSAP 动画+配音 |
| **数据可视化简报** | MP4 | hyperframes | 图表动效+旁白 |
| **小红书/短视频** | MP4 | hyperframes | 竖屏+快节奏 |
| **日报/月报** | 图文 | html-anything | 静态 PDF |
| **品牌宣传片** | MP4 | hyperframes | 多场景+转场动画 |
| **GitHub PR walkthrough** | MP4 | hyperframes | 代码 diff + 配音 |
| **网页→视频** | MP4 | hyperframes | URL → 短视频 |

### 自动识别特征

```
用户说"做成视频" / "短视频" / "动效" / "动画" / "宣传片"
  → 自动路由到 HyperFrames

用户说"生成报告" / "写文章" / "排版" / "卡片"
  → 走 art-agent / html-anything 静态路由

OERV 分发时自动判断：
  - 有 "video" / "mp4" 标记 → hyperframes
  - 有 "wechat" / "article" 标记 → art-agent HTML
  - 未指定 → 默认生成 HTML，额外提供视频版
```

---

## 🔌 调用方式

### 一键命令

```
/视频 "产品介绍" --duration 15 --size 1080x1920
/视频 "数据周报" --template data-chart
/oerv-video "闪念内容"     # OERV 全链路 → 视频版
```

### Python API

```python
from skills.hyperframes.hyperframes import render, info

# 从 HTML 文件渲染视频
result = render("/path/to/composition.html")

# 从模板+内容生成
result = render(
    content="产品功能介绍文字...",
    template="product-launch",
    duration=10,
    size="1920x1080",
    output="/tmp/output.mp4",
)

# 信息
info()
# → {version, available, ffmpeg, node}
```

### CLI

```bash
python -m skills.hyperframes.hyperframes render <html_path>
python -m skills.hyperframes.hyperframes template <template_name> <content>
python -m skills.hyperframes.hyperframes check
```

---

## 📦 安装

```bash
# 依赖: Node.js 22+ (系统已安装), FFmpeg (系统已安装 8.0.1)

# HyperFrames 通过 npx 自动拉取，无需全局安装
npx hyperframes --version
```

---

## 🏗 与 OERV 叙事引擎集成

```
OERV 叙事 → 搜索配图 → art-agent 排版
    │
    ├─ 图文版 → HTML/PDF（现有链路）
    │
    └─ 视频版 → HyperFrames（新增链路）
         │
         ├─ 叙事文本 → HTML composition
         ├─ 配图/素材 → 嵌入 video/img 标签
         ├─ GSAP 动画 → fade/slide/scale
         └─ npx hyperframes render → MP4
```

---

## 📊 规格

| 项目 | 值 |
|------|-----|
| 许可 | Apache 2.0 |
| 引擎 | 无头 Chrome + FFmpeg |
| 输入 | HTML + CSS + JavaScript (GSAP/Three.js/Anime.js) |
| 输出 | MP4 (H.264) |
| 最大分辨率 | 任意（常见 1920×1080 / 1080×1920） |
| 帧率 | 30fps (默认) |
| 音频 | 支持多音轨混音 |
| 安装 | npx 零安装 |

---

## 📁 文件结构

```
skills/hyperframes/
├── SKILL.md            ← 本文档
└── hyperframes.py      ← 核心封装
```

---

## 🔗 相关资源

- GitHub: https://github.com/heygen-com/hyperframes
- 官方文档: https://hyperframes.heygen.com/introduction
- 在线 Playground: https://www.hyperframes.dev/
- 组件目录: https://hyperframes.heygen.com/catalog/blocks/data-chart
- 展示案例: https://hyperframes.heygen.com/showcase
- NPM: https://www.npmjs.com/package/hyperframes
