---
name: google-agents-cli
description: 融合 Google 官方 CLI 工具到太一系统。包括：google/agents-cli（2604⭐，Gemini Agent 构建/评估/部署）和 googleworkspace/cli（26607⭐，Gmail/Drive/Calendar/Sheets/Docs/Chat 统一访问）。自动识别用户意图路由到对应工具。
---

# Google Agents CLI — 太一融合层

融合两个 Google 官方 CLI 工具。

## 已装载能力

### ① google/agents-cli（2604⭐）
Google 官方 Agent 构建 CLI — 在 Gemini Enterprise Agent Platform 上构建/评估/部署 Agent。

| 能力 | 命令 | 说明 |
|:----:|:----:|------|
| 项目脚手架 | `agents-cli scaffold <name>` | 创建新 Agent 项目 |
| 评估 | `agents-cli eval run` | 运行 Agent 评估 |
| 部署 | `agents-cli deploy` | 部署到 Cloud Run/GKE |
| 可观测 | `agents-cli observability` | 监控和日志 |
| 发布 | `agents-cli publish` | 注册到 Gemini Enterprise |

### ② googleworkspace/cli（26607⭐）
Google Workspace 统一 CLI — 一个命令访问所有 Google 服务。

| 服务 | 命令前缀 | 用途 |
|:----:|:--------:|------|
| **Gmail** | `gws gmail` | 邮件收发、搜索、管理 |
| **Drive** | `gws drive` | 文件管理、搜索、上传 |
| **Calendar** | `gws calendar` | 日程管理、会议 |
| **Sheets** | `gws sheets` | 电子表格读写 |
| **Docs** | `gws docs` | 文档创建/编辑 |
| **Chat** | `gws chat` | 聊天消息 |
| **Admin** | `gws admin` | 管理控制台 |

## 自动触发规则

| 用户意图 | 路由到 | 调用方式 |
|---------|--------|---------|
| "建一个Agent/部署Agent" | `agents-cli scaffold/eval/deploy` | Gemini CLI 代理 |
| "查/发邮件" | `gws gmail` | 太一 → gws |
| "查Drive/找文件" | `gws drive list` | 太一 → gws |
| "看日程/安排会议" | `gws calendar` | 太一 → gws |
| "读/写Sheet" | `gws sheets` | 太一 → gws |
| "创建文档" | `gws docs` | 太一 → gws |

## 安装状态

| 工具 | 版本 | 状态 | 认证 |
|:----:|:----:|:----:|:----:|
| agents-cli | v0.2.0 | ✅ 已安装 | ❌ 需 gcloud SDK |
| gws | v0.22.5 | ✅ 已安装 | ❌ 需 OAuth 配置 |

## 配置认证

### gws OAuth
```bash
gws auth login
# 浏览器打开 → 授权 → 完成
```

### agents-cli GCP
```bash
gcloud auth login
# 或设置 GOOGLE_CLOUD_PROJECT
```
