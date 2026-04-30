---
name: gmgn-auto-config
version: 1.0.0
description: 自动化配置 GMGN 钱包和交易参数
category: auto-generated
tags: ['GMGN', '配置', '交易', '自动化']
author: 太一 AGI (Auto-Generated)
created: 2026-04-09
---

# GMGN Auto Config Skill

> 版本：v1.0 | 创建：2026-04-09 | 优先级：P2  
> 来源：从 3+ 次 GMGN 配置任务中自动提取

---

## 🎯 职责

自动化配置 GMGN 钱包和交易参数，包括：
- 配置 Solana/Base 钱包地址
- 设置交易参数（滑点/金额）
- 配置 API Key
- 测试连接
- 保存配置到 TOOLS.md

---

## 🔍 触发条件

- 用户提及：GMGN 配置
- 用户提及：钱包配置
- 用户提及：交易设置

---

## 🛠️ 执行流程

1. **读取配置模板**
   - 读取 `skills/gmgn/config-template.md`
   - 提取配置项

2. **生成钱包地址**
   - Solana 地址生成
   - Base 地址生成
   - 保存到 TOOLS.md

3. **配置交易参数**
   - 滑点设置（默认 1%）
   - 单笔金额设置
   - 每日限额设置

4. **配置 API Key**
   - GMGN Bot API Key
   - 测试连接
   - 保存配置

5. **验证配置**
   - 钱包余额查询
   - API 连接测试
   - 返回配置摘要

---

## 📁 相关文件

- `TOOLS.md` - 配置存储
- `skills/gmgn/SKILL.md` - GMGN 技能
- `skills/gmgn/config-template.md` - 配置模板

---

## 📋 使用示例

```
# 示例 1: 基础配置
太一，配置 GMGN 钱包

# 示例 2: 指定参数
太一，配置 GMGN，滑点 0.5%，单笔 100U

# 示例 3: 测试连接
太一，测试 GMGN API 连接
```

---

## 🔧 配置模板

```json
{
  "gmgn": {
    "solana_wallet": "自动生成",
    "base_wallet": "自动生成",
    "slippage": "1%",
    "amount_per_trade": "100U",
    "daily_limit": "1000U",
    "api_key": "用户输入"
  }
}
```

---

## ✅ 质量检查

- [x] 命名规范检查
- [x] 元数据完整检查
- [x] 触发条件清晰检查
- [x] 步骤可执行检查
- [x] 无硬编码检查
- [x] 有使用示例检查
- [ ] 有错误处理检查

---

*本技能由太一自动生成，经 SAYELF 确认后激活。*
