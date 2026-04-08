---
name: terraform-apply
version: 1.0.0
description: terraform-apply skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Terraform Apply Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 素问
> **状态**: ✅ 已激活 | **优先级**: P1-02

---

## 📋 功能概述

提供基础设施即代码（IaC）能力，支持 Terraform 创建/更新/销毁云资源。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `terraform init` | 初始化 | `terraform init` |
| `terraform plan` | 执行计划 | `terraform plan -out=tfplan` |
| `terraform apply` | 应用变更 | `terraform apply tfplan` |
| `terraform destroy` | 销毁资源 | `terraform destroy` |
| `terraform state` | 状态管理 | `terraform state list` |
| `terraform output` | 输出值 | `terraform output` |
| `terraform import` | 导入资源 | `terraform import aws_instance.foo i-123456` |
| `terraform fmt` | 格式化 | `terraform fmt -recursive` |
| `terraform validate` | 验证 | `terraform validate` |
| `terraform workspace` | 工作区 | `terraform workspace new prod` |

---

## 📝 使用示例

### 示例 1: 初始化并应用

```bash
# 太一，初始化并应用 Terraform 配置
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

### 示例 2: 销毁资源

```bash
# 太一，销毁所有 Terraform 管理的资源
terraform destroy
```

**太一响应**:
```
⚠️ 此操作将销毁所有资源:
- aws_instance.web (i-0abc123)
- aws_s3_bucket.data
- aws_rds_cluster.db

确认执行？[y/N]
```

---

## ⚠️ 安全限制

### 自动执行的操作
- [x] `terraform init/plan/validate/fmt`
- [x] `terraform output/state list`
- [x] `terraform apply` (非生产工作区)

### 需要确认的操作
- [ ] `terraform apply` (生产工作区)
- [ ] `terraform destroy`
- [ ] `terraform state rm`

---

*创建时间：2026-04-03 09:17 | 素问 | 太一 AGI v5.0*
