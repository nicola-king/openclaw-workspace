---
name: llm-finetune
version: 1.0.0
description: llm-finetune skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# LLM Finetune Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 素问
> **状态**: ✅ 已激活 | **优先级**: P4-01

---

## 📋 功能概述

提供大模型微调能力，支持 LoRA/QLoRA 等高效微调方法。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `llm finetune` | 微调模型 | `llm finetune --model qwen-7b --data dataset.json` |
| `llm prepare-data` | 准备数据 | `llm prepare-data --input raw.json --output train.json` |
| `llm train` | 启动训练 | `llm train --config config.yaml` |
| `llm evaluate` | 评估模型 | `llm evaluate --model checkpoint --data test.json` |
| `llm merge` | 合并适配器 | `llm merge --base model --adapter lora --output merged` |
| `llm convert` | 格式转换 | `llm convert --model pt --format gguf` |

---

## 📝 使用示例

### 示例 1: 准备微调数据

```bash
# 太一，准备微调数据
llm prepare-data --input ./custom-data.json --output ./train-data.json --format alpaca
```

### 示例 2: 启动 LoRA 微调

```bash
# 太一，用 QLoRA 微调 Qwen-7B
llm finetune --model qwen-7b --data ./train-data.json --method qlora --epochs 3
```

### 示例 3: 评估模型

```bash
# 太一，评估微调后的模型
llm evaluate --model ./checkpoint-1000 --data ./test-data.json
```

---

## ⚠️ 资源需求

| 方法 | GPU 内存 | 时间 | 适用场景 |
|------|---------|------|---------|
| Full Finetune | 80GB+ | 数天 | 研究/大规模 |
| LoRA | 24GB+ | 数小时 | 通用 |
| QLoRA | 16GB+ | 数小时 | 消费级 GPU |

---

*创建时间：2026-04-03 09:32 | 素问 | 太一 AGI v5.0*
