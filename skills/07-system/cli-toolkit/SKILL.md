---
name: cli-toolkit
version: 1.0.0
description: CLI 工具集 - 云厂商/DevOps/开发工具统一封装
category: cli
tags: ['cli', 'cloud', 'devops', 'aws', 'azure', 'gcp', 'docker', 'k8s', '命令行，云，运维']
author: 太一 AGI
created: 2026-04-07
status: active
priority: P1
---


# CLI Toolkit v1.0 - 统一命令行工具集

> **版本**: 1.0.0 (整合版) | **创建**: 2026-04-07
> **负责 Bot**: 素问 | **状态**: ✅ 已激活

---

## 📋 功能概述

统一 CLI 工具技能，整合云厂商和 DevOps 工具。

**整合内容**:
- ✅ aws-cli → cloud/aws.py
- ✅ azure-cli → cloud/azure.py
- ✅ gcp-cli → cloud/gcp.py
- ✅ docker-ctl → devops/docker.py
- ✅ k8s-deploy → devops/k8s.py

**独立保留**:
- git-integration (Git 专用)
- gemini-cli (Gemini 专用)
- jimeng-cli (即梦专用)

---

## 🏗️ 架构设计

```
cli-toolkit/
├── SKILL.md (主入口)
├── cloud/ (云服务)
│   ├── aws.py (AWS CLI)
│   ├── azure.py (Azure CLI)
│   └── gcp.py (GCP CLI)
├── devops/ (运维工具)
│   ├── docker.py (Docker)
│   └── k8s.py (Kubernetes)
└── wrappers/ (独立 CLI 包装)
    ├── gemini.py → gemini-cli
    └── jimeng.py → jimeng-cli
```

---

## 🚀 使用方式

### Python API

```python
from skills.cli_toolkit import CLIToolkit

# 初始化
cli = CLIToolkit()

# AWS 操作
cli.cloud.aws.run_command('s3 ls')
cli.cloud.aws.ec2.describe_instances()

# Docker 操作
cli.devops.docker.run('ps')
cli.devops.docker.build('.', 'myimage:latest')

# K8s 操作
cli.devops.k8s.run('get pods')
cli.devops.k8s.apply('deployment.yaml')
```

### 命令行

```bash
# AWS
cli aws s3 ls
cli aws ec2 describe-instances

# Docker
cli docker ps
cli docker build -t myimage .

# K8s
cli k8s get pods
cli k8s apply -f deployment.yaml
```

---

## 📊 模块说明

### 1. Cloud Module - 云服务

| 云厂商 | 功能 |
|--------|------|
| **AWS** | EC2/S3/Lambda/RDS 等 |
| **Azure** | VM/Blob/Functions 等 |
| **GCP** | Compute/Storage/Functions 等 |

### 2. DevOps Module - 运维工具

| 工具 | 功能 |
|------|------|
| **Docker** | 容器构建/运行/管理 |
| **Kubernetes** | 集群部署/管理/监控 |

---

## ⚠️ 安全限制

### 需要认证的操作

- ✅ AWS: 需要 AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY
- ✅ Azure: 需要 Azure 登录
- ✅ GCP: 需要 gcloud 认证
- ✅ K8s: 需要 kubeconfig

### 自动执行的操作

- [x] 只读查询 (ls/get/describe)
- [ ] 写操作 (需要确认)
- [ ] 删除操作 (需要确认)

---

## 📋 变更日志

### v1.0.0 (2026-04-07)
- ✅ 整合 5 个 CLI 技能
- ✅ 创建统一架构 cloud/devops
- ✅ 保留独立 CLI 工具

---

*维护：素问 AGI | CLI Toolkit v1.0*
