# MiroFish Skill — 群体智能预测引擎

> 集成自 666ghj/MiroFish (63,391⭐)
> AGPL-3.0 · https://github.com/666ghj/MiroFish
> 官网: https://mirofish.ai

## 概述

MiroFish 是一款**多 Agent 群体智能预测引擎**。输入种子信息（新闻/政策/金融信号），自动构建高保真并行数字世界，数千个独立人格 Agent 自由交互、社会演化。

| 特性 | 说明 |
|------|------|
| **语言** | Python + Node.js |
| **前端** | React (port 3000) |
| **后端** | Python Flask (port 5001) |
| **部署** | 源码 / Docker |
| **模型** | 兼容 OpenAI SDK 格式（推荐阿里通义 qwen-plus） |
| **记忆** | Zep Cloud（免费额度够用） |

## 工作流

```
种子素材（新闻/报告/小说）
  → Graph Building（实体提取 + 记忆注入 + GraphRAG）
    → Environment Setup（关系提取 + 人格生成 + Agent 配置）
      → Simulation（双平台并行模拟 + 动态时序记忆）
        → Report Generation（ReportAgent 深度交互）
          → Deep Interaction（与模拟世界对话）
```

## 预期用途

在太一系统中，MiroFish 可用于：

1. **跨境贸易舆情预测** — 输入目标市场政策/关税新闻，模拟市场情绪演化
2. **竞品行为推演** — 输入竞品动态，推演其可能的市场策略走向
3. **招投标结果预测** — 输入项目背景/竞标者信息，模拟评标过程
4. **内容创作沙盒** — OERV 叙事剧情推演、公众号选题反响模拟

## 部署（备选）

```bash
# 前提：Node.js 18+ / Python 3.11-3.12 / uv
git clone https://github.com/666ghj/MiroFish.git
cd MiroFish
cp .env.example .env
# 编辑 .env 填入 LLM_API_KEY / ZEP_API_KEY 等
npm run setup:all    # 一键安装全部依赖
npm run dev          # 启动前端+后端
```

| 组件 | 端口 |
|------|------|
| 前端 | http://localhost:3000 |
| 后端 API | http://localhost:5001 |

Docker: `docker compose up -d`

## 环境变量

```env
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus
ZEP_API_KEY=z_xxx
```

## 状态

| 项目 | 状态 |
|------|------|
| 本地部署 | ✅ 已部署 |
| 后端 | ✅ 5001 |
| 前端 | ✅ 3000 |
| ZEP 记忆 | ⚠️ 未配置（功能受限） |
| 与太一集成 | 🟢 已集成

## 关联资源

- **GitHub**: https://github.com/666ghj/MiroFish
- **Live Demo**: https://666ghj.github.io/mirofish-demo/
- **Discord**: http://discord.gg/ePf5aPaHnA
- **X**: https://x.com/mirofish_ai
- **深度文档**: https://deepwiki.com/666ghj/MiroFish
