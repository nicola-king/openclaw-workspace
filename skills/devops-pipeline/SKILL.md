---
name: devops-pipeline
version: 1.0.0
description: 太一 DevOps 管道引擎 — 参考 Microsoft CI/CD 模式（Symphony/ResourceModules/Azure DevOps）
category: infrastructure
tags: ['devops', 'cicd', 'pipeline', 'github-actions', 'azure-devops', 'iac', 'automation']
author: 太一 AGI
created: 2026-05-29
status: active
trigger: 当需要 CI/CD 管道/自动化部署/发布/质量门禁时自动路由
---

# 🔧 DevOps Pipeline 引擎

> 参考模式：Microsoft Symphony (IaC CI/CD) · Azure/ResourceModules (模块化CI平台) · Azure DevOps Python API (编程化DevOps)

---

## 🧠 智能调度规则

| 用户说 | 路由 | 输出 |
|--------|------|------|
| "配置 CI/CD" | pipeline:generate | GitHub Actions / Azure Pipeline YAML |
| "发布/部署" | pipeline:deploy | 执行发布管道 |
| "质量门禁" | pipeline:gate | 代码扫描+测试+门禁检查 |
| "管道状态" | pipeline:status | 当前管道健康报告 |
| "产线这个模块" | pipeline:module | 模块化 CI 管道模板 |

---

## 📦 集成内容

### 管道模板（3 层架构，参考 ResourceModules）

```
L1: 基础设施管道 (IaC)
  ├─ 代码验证 + Lint + 安全扫描
  ├─ 多环境部署 (dev → staging → prod)
  └─ 不可变部署 (immutable)

L2: 应用管道 (太一技能/Agent)
  ├─ 构建 → 测试 → 打包 → 发布
  ├─ AI 生成代码质量门禁
  └─ 自动版本号 + CHANGELOG

L3: 内容管道 (OERV/公众号)
  ├─ 叙事 → 搜索 → 制作 → 审核 → 发布
  ├─ 多平台分发 (公众号/小红书/视频号)
  └─ 定时发布 + 自动排期
```

### 当前已集成的 DevOps 设施

| 设施 | 状态 | 说明 |
|------|------|------|
| Git 自动备份 | ✅ | 每日 03:00 cron |
| 系统自检 | ✅ | SRE 自修复 |
| 健康检查 | ✅ | API 保活 |
| 管道监控 | ⏳ | 本模块新增 |
| 发布管道 | ⏳ | 本模块新增 |

---

## 🔌 调用方式

```python
from skills.devops_pipeline.pipeline import (
    generate_pipeline,     # 生成 CI/CD YAML
    check_health,          # 管道健康检查
    gate_check,            # 质量门禁
    deploy,                # 执行部署
    status,                # 管道状态报告
)
```

## 📁 文件结构

```
skills/devops-pipeline/
├── SKILL.md          ← 本文档
└── pipeline.py       ← 核心引擎
```
