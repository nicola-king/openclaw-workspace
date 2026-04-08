# 学习笔记：OpenClaw 安装与配置（第四阶段）

> 学习时间：2026-04-06 00:30  
> 来源：小红书 @早晚冰美式 o  
> 主题：n8n + OpenClaw 亚马逊广告自动化 - 第四阶段

---

## 📋 第四阶段：安装 OpenClaw 接入 AI 分析

**目标**：让 n8n 能够调用 OpenClaw 进行 AI 数据分析

---

## 🔧 4.1 安装 OpenClaw

### 安装步骤

#### 第 1 步：下载并安装
```bash
# 回到腾讯云服务器的命令行
curl -fsSL https://get.openclaw.dev | sh
```

#### 第 2 步：启动 OpenClaw
```bash
openclaw start
```

#### 第 3 步：浏览器访问
```
http://你的服务器 IP:18789
```

#### 第 4 步：配置 AI API Key

| 选项 | API Key 格式 | 说明 |
|------|------------|------|
| **用 OpenAI** | `sk-xxx...` | 用 GPT-4 分析数据 |
| **用 Claude** (推荐) | `sk-ant-xxx...` | 对中文理解更好，建议优先选择 |

---

## 🔗 4.2 把 OpenClaw 连接到 n8n

### 连接流程

```
n8n 工作流
    ↓
整理数据的 Code 节点
    ↓
HTTP Request 节点（新增）
    ↓
OpenClaw API（AI 分析）
    ↓
返回建议
```

### HTTP Request 节点配置

**URL**: `http://localhost:18789/api/chat`  
**Method**: `POST`  
**Headers**:
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_OPENCLAW_API_KEY"
}
```

**Body**:
```json
{
  "message": "请分析以下亚马逊广告数据，给出优化建议：\n\nACoS: 45%\n花费：$500\n销售：$1100\n关键词：[关键词 1, 关键词 2, ...]"
}
```

---

## 🎯 太一现状对比

### OpenClaw 安装状态

| 项目 | 教程配置 | 太一现状 |
|------|---------|---------|
| **安装方式** | 腾讯云服务器 | ✅ 已安装（本机） |
| **访问地址** | http://IP:18789 | ✅ 已配置（微信通道） |
| **AI API Key** | OpenAI/Claude | ✅ 百炼/Gemini/本地 |
| **启动状态** | openclaw start | ✅ 运行中 |

**结论**：太一已完全安装并配置 OpenClaw，无需重复安装。

---

## 🛠️ 太一 OpenClaw 配置

### 当前状态

```bash
# 安装位置
~/.openclaw/

# 工作目录
~/.openclaw/workspace/

# 配置文件
~/.openclaw/config.json

# 运行状态
openclaw gateway status  # ✅ 运行中
```

### AI 模型配置

| 模型 | 用途 | 状态 |
|------|------|------|
| **百炼 qwen3.5-plus** | 主力模型 | ✅ 已配置 |
| **Gemini 2.5 Pro** | 长文本分析 | ✅ 可用 |
| **本地模型** | 离线推理 | 🟡 可选 |

### 消息通道

| 通道 | 状态 | 用途 |
|------|------|------|
| **微信** | ✅ 已连接 | 主力通讯 |
| **Telegram** | ✅ 已配置 | 海外/备用 |
| **飞书** | ✅ 已配置 | 文档协作 |

---

## 💡 与 n8n 集成方案

### 方案 A：OpenClaw 独立运行（推荐）

**架构**:
```
Cron 定时任务
    ↓
数据采集 Skill
    ↓
AI 分析（OpenClaw 内置）
    ↓
微信推送
```

**优势**:
- ✅ 无需 n8n（零额外成本）
- ✅ 与现有系统无缝集成
- ✅ 完全可控

**太一已实现**:
- ✅ ROI 周报自动化
- ✅ 热点选题生成
- ✅ 知几-E 模拟盘
- ✅ 三级预警系统

### 方案 B：n8n + OpenClaw 混合

**架构**:
```
n8n（流程编排 + 可视化）
    ↓
OpenClaw（AI 分析）
```

**适用场景**:
- 非技术用户需要可视化界面
- 已有 n8n 工作流需要 AI 增强
- 团队协作需要可视化流程

**太一建议**：无需此方案（已有 OpenClaw 原生能力）

---

## 🔗 OpenClaw API 调用示例

### 如果未来需要 n8n 集成

```python
# OpenClaw API 调用示例
import requests

url = "http://localhost:18789/api/chat"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}

data = {
    "message": "分析以下广告数据：ACoS 45%，花费$500，销售$1100"
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result['reply'])
```

### 太一原生替代方案

```python
# 直接使用 OpenClaw 技能
from skills.amazon-ads.SKILL import AmazonAdsTracker

tracker = AmazonAdsTracker()
analysis = tracker.analyze_and_suggest()
print(analysis)
```

**优势**：无需 HTTP 调用，直接 Python 集成。

---

## 📊 教程完整流程回顾

| 阶段 | 内容 | 太一状态 |
|------|------|---------|
| **第一阶段** | 系统架构介绍 | ✅ 已理解 |
| **第二阶段** | 亚马逊 API 集成 | 🟡 按需开发 |
| **第三阶段** | n8n 工作流配置 | 🟡 无需（用 Cron） |
| **第四阶段** | OpenClaw 安装配置 | ✅ 已完成 |

---

## 🎯 太一行动建议

### 无需行动（已有）
- [x] OpenClaw 安装
- [x] AI API 配置（百炼/Gemini）
- [x] 微信通道连接
- [x] 定时任务系统
- [x] 数据采集 Skills

### 可选优化（按需）
- [ ] OpenClaw Web UI 配置（如需要可视化）
- [ ] API Key 管理优化
- [ ] 多模型路由配置

### 核心建议
**继续使用 OpenClaw 原生方案**，无需 n8n。

**理由**：
1. 功能已覆盖（定时/采集/AI/推送）
2. 零额外成本（无需 n8n 服务器）
3. 与现有系统无缝集成
4. 完全可控（代码级定制）

---

*学习笔记生成：太一 AGI · 2026-04-06 00:31*  
*状态：OpenClaw 已完全配置，无需重复安装*
