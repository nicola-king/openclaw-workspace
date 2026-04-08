---
name: npm-audit
version: 1.0.0
description: npm-audit skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# NPM Audit Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 素问
> **状态**: ✅ 已激活 | **优先级**: P0-02

---

## 📋 功能概述

提供 Node.js 项目依赖安全审计能力，包括漏洞扫描、安全报告、自动修复建议。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `npm audit` | 安全审计 | `npm audit` |
| `npm audit --json` | JSON 格式报告 | `npm audit --json` |
| `npm audit fix` | 自动修复 | `npm audit fix` |
| `npm audit fix --force` | 强制修复 | `npm audit fix --force` |
| `npm outdated` | 检查过期包 | `npm outdated` |
| `npm ls` | 依赖树 | `npm ls --depth=0` |

---

## 🔧 工具实现

### NPM Audit 命令封装

```bash
# 基础审计
npm audit [--json] [--production]

# 自动修复
npm audit fix [--force] [--dry-run]

# 详细报告
npm audit --audit-level=<low|moderate|high|critical>

# 检查过期
npm outdated [--long]

# 依赖树
npm ls [--depth=<n>] [--prod]
```

### 安全级别定义

| 级别 | 说明 | 自动修复 |
|------|------|---------|
| `low` | 低风险 | ✅ 自动 |
| `moderate` | 中风险 | ✅ 自动 |
| `high` | 高风险 | ⚠️ 需确认 |
| `critical` | 严重风险 | ❌ 需人工审查 |

---

## 📊 审计报告格式

### 文本格式

```
                       === npm audit security report ===

# Run  npm install --save-dev npm@latest  to update npm.

                        # of vulnerabilities found

  low       2
  moderate  5
  high      1
  critical  0

  To address issues that do not require attention, run:
    npm audit fix

  To address all issues possible (including breaking changes), run:
    npm audit fix --force

  Some issues need review, and may require listening
  to a different package with a similar name.
```

### JSON 格式

```json
{
  "actions": [
    {
      "action": "update",
      "resolves": [
        {
          "id": 1234,
          "path": "lodash",
          "dev": false,
          "optional": false,
          "bundled": false
        }
      ],
      "module": "lodash",
      "target": "4.17.21",
      "url": "https://github.com/lodash/lodash/issues/..."
    }
  ],
  "advisories": {
    "1234": {
      "findings": [...],
      "id": 1234,
      "created": "2024-01-01T00:00:00.000Z",
      "updated": "2024-01-01T00:00:00.000Z",
      "deleted": null,
      "title": "Prototype Pollution in lodash",
      "found_by": {...},
      "reported_by": {...},
      "module_name": "lodash",
      "cves": ["CVE-2021-23337"],
      "vulnerable_versions": "<4.17.21",
      "patched_versions": ">=4.17.21",
      "overview": "...",
      "recommendation": "Update to version 4.17.21 or higher",
      "references": [...],
      "access": "public",
      "severity": "high",
      "cwe": "CWE-1321",
      "metadata": {...},
      "url": "https://github.com/advisories/..."
    }
  },
  "muted": [],
  "metadata": {
    "vulnerabilities": {
      "info": 0,
      "low": 2,
      "moderate": 5,
      "high": 1,
      "critical": 0
    },
    "dependencies": {
      "prod": 150,
      "dev": 50,
      "optional": 10,
      "peer": 5,
      "total": 215
    }
  }
}
```

---

## 📝 使用示例

### 示例 1: 基础安全审计

```bash
# 太一，扫描当前项目的安全漏洞
npm audit
```

**输出**:
```
found 8 vulnerabilities (2 low, 5 moderate, 1 high)
```

### 示例 2: 自动修复低风险漏洞

```bash
# 太一，自动修复所有低风险和中风险漏洞
npm audit fix
```

**输出**:
```
fixed 7 of 8 vulnerabilities
```

### 示例 3: 生成 JSON 报告

```bash
# 太一，生成 JSON 格式的安全报告
npm audit --json > audit-report.json
```

### 示例 4: 检查过期依赖

```bash
# 太一，检查哪些依赖需要更新
npm outdated
```

**输出**:
```
Package    Current   Wanted   Latest  Location
lodash     4.17.15  4.17.21  4.17.21  project
axios      0.21.0   0.27.0   1.4.0    project
```

### 示例 5: 高风险漏洞处理

```bash
# 太一，发现高风险漏洞，需要人工审查
npm audit --audit-level=high
```

**太一响应**:
```
⚠️ 发现 1 个高风险漏洞:

Package: lodash
Version: <4.17.21
CVE: CVE-2021-23337
Severity: HIGH

建议:
1. 升级到 4.17.21 或更高版本
2. 运行: npm install lodash@latest
3. 测试确认无破坏性变更

是否执行修复？[y/N]
```

---

## 🔄 自动化工作流

### CI/CD 集成

```yaml
# .github/workflows/security-audit.yml
name: Security Audit

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # 每日执行

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run security audit
        run: npm audit --audit-level=high
      
      - name: Upload audit report
        if: always()
        run: npm audit --json > audit-report.json
      
      - uses: actions/upload-artifact@v3
        with:
          name: audit-report
          path: audit-report.json
```

### 定时扫描脚本

```bash
#!/bin/bash
# scripts/daily-audit.sh

PROJECTS=(
  "/home/nicola/.openclaw/workspace"
  "/home/nicola/projects/project-a"
  "/home/nicola/projects/project-b"
)

for project in "${PROJECTS[@]}"; do
  echo "=== Auditing: $project ==="
  cd "$project"
  
  if [ -f "package.json" ]; then
    npm audit --json > "/tmp/audit-$(basename $project)-$(date +%Y%m%d).json"
    
    # 检查严重漏洞
    critical=$(npm audit --json | jq '.metadata.vulnerabilities.critical')
    if [ "$critical" -gt 0 ]; then
      echo "🚨 CRITICAL: $project has $critical critical vulnerabilities!"
      # 发送通知
    fi
  fi
done
```

---

## ⚠️ 安全限制

### 自动执行的操作
- [x] `npm audit` (扫描)
- [x] `npm audit fix` (低风险/中风险)
- [x] `npm outdated` (检查)
- [x] `npm ls` (依赖树)

### 需要确认的操作
- [ ] `npm audit fix --force` (可能引入破坏性变更)
- [ ] 删除 node_modules
- [ ] 全局安装包卸载

---

## 🔍 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `npm ERR! code EAUDIT` | 审计服务不可用 | 检查网络连接 |
| `npm ERR! code ERESOLVE` | 依赖冲突 | 使用 `--legacy-peer-deps` |
| `no lockfile found` | 缺少 package-lock.json | 运行 `npm install` |
| `npm not found` | 未安装 Node.js | 安装 Node.js |

---

## 🧪 测试用例

```bash
# 测试 1: 创建测试项目
mkdir -p /tmp/npm-audit-test
cd /tmp/npm-audit-test
npm init -y

# 测试 2: 安装已知有漏洞的旧版本
npm install lodash@4.17.15

# 测试 3: 运行审计
npm audit

# 测试 4: 自动修复
npm audit fix

# 测试 5: 验证修复
npm audit

# 清理
cd /
rm -rf /tmp/npm-audit-test
```

---

## 📚 相关文档

- [NPM Audit 官方文档](https://docs.npmjs.com/cli/commands/npm-audit)
- [Node.js Security Best Practices](https://nodejs.org/en/security/)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)

---

*创建时间：2026-04-03 09:12 | 素问 | 太一 AGI v5.0*
