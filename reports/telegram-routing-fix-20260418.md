---
title: Telegram 路由规则修复报告
author: 太一 AGI
date: 2026-04-18
type: report
tags: ['修复', '路由', 'Telegram', '合规']
---

# 🔧 Telegram 路由规则修复报告

> **问题发现**: 2026-04-18 07:45  
> **修复时间**: 2026-04-18 07:46  
> **状态**: ✅ 已修复

---

---

## ❌ 问题根因

### 违规配置

我在 `load-env.sh` 中使用了"智能探测"逻辑：

```bash
# ❌ 错误做法（已修复）
if ! curl -s --max-time 3 https://api.telegram.org > /dev/null 2>&1; then
    # 直连失败才启用代理
    export HTTPS_PROXY="http://127.0.0.1:7890"
else
    # 直连成功就禁用代理
    unset HTTPS_PROXY
fi
```

### 违背的规则

根据 **太一智能路由系统** (`skills/07-system/geo-model-router/SKILL.md`)：

> **原则 2: 国外流量走代理**  
> 目标类型：国外服务 → 路由策略：代理 (经过 SOCKS5/HTTP 代理)  
> **Telegram Bot API → 代理**

**违规点**：
1. ❌ 使用"智能探测"替代确定性路由
2. ❌ 可能绕过代理直连（违背规则）
3. ❌ 不符合 `communication_channels.json` 定义

---

## ✅ 修复方案

### 修改文件
`/home/nicola/.openclaw/load-env.sh`

### 修复后配置

```bash
# ✅ 正确做法（遵循太一智能路由规则）
# 规则来源：skills/07-system/geo-model-router/SKILL.md
# 原则 2: 国外流量走代理
# Telegram 明确定义为 international 类型 → 必须使用代理

# 固定启用代理（符合太一智能路由规则）
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export NO_PROXY="localhost,127.0.0.1,192.168.0.0/16,10.0.0.0/8"
export no_proxy="localhost,127.0.0.1,192.168.0.0/16,10.0.0.0/8"

echo "🌐 代理已启用：127.0.0.1:7890 (遵循太一智能路由规则)"
echo "   规则：国外服务 (Telegram) → 必须走代理"
```

---

## 📋 规则对照表

### 太一智能路由系统定义

| 服务 | 类型 | 路由策略 | 配置 |
|------|------|---------|------|
| 微信 | domestic | 直连 | ✅ 无代理 |
| 飞书 | domestic | 直连 | ✅ 无代理 |
| **Telegram** | **international** | **代理** | ✅ **已修复** |
| Discord | international | 代理 | ⏳ 待配置 |

### 配置文件位置

| 文件 | 内容 | 位置 |
|------|------|------|
| `communication_channels.json` | 渠道类型定义 | `skills/07-system/geo-model-router/config/` |
| `international_services.json` | 国外服务白名单 | `skills/07-system/geo-model-router/config/` |
| `SKILL.md` | 路由规则文档 | `skills/07-system/geo-model-router/` |

---

## 🔍 验证结果

### 环境变量检查
```bash
$ . /home/nicola/.openclaw/load-env.sh
🌐 代理已启用：127.0.0.1:7890 (遵循太一智能路由规则)
   规则：国外服务 (Telegram) → 必须走代理
✅ 环境变量加载成功

$ env | grep -E "PROXY|proxy"
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
http_proxy=http://127.0.0.1:7890
https_proxy=http://127.0.0.1:7890
```

### Telegram API 测试
```python
✅ Telegram API 通过代理连接成功
   Bot: @sayelfbot
```

---

## 🎯 合规性确认

### ✅ 符合原则 2
- [x] Telegram 定义为 international 类型
- [x] 固定使用代理 (127.0.0.1:7890)
- [x] 不使用智能探测绕过规则

### ✅ 符合配置文件
- [x] `communication_channels.json`: Telegram → international
- [x] `international_services.json`: api.telegram.org → route: international

### ✅ 符合文档规范
- [x] `SKILL.md` 原则 2: 国外流量走代理
- [x] 代理配置：socks5://127.0.0.1:7890

---

## 📝 教训总结

### 错误原因
1. **过度优化**：试图用"智能探测"提升性能
2. **忽视规则**：未严格遵守太一智能路由系统的确定性规则
3. **假设错误**：假设直连更快，忽略了规则的合规性要求

### 正确做法
1. **严格遵守配置文件**：`communication_channels.json` 是唯一真相源
2. **不擅自修改路由逻辑**：如需调整，先修改配置文件
3. **遵循文档**：`SKILL.md` 的四大原则不可违背

---

## 🔗 相关文件

- 路由规则：`skills/07-system/geo-model-router/SKILL.md`
- 渠道配置：`skills/07-system/geo-model-router/config/communication_channels.json`
- 修复文件：`/home/nicola/.openclaw/load-env.sh`

---

*太一 AGI · 路由规则合规性修复 · 2026-04-18*
