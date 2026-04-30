---
name: issue-pitfalls-record
version: 1.0.0
description: 踩坑记录 Skill - 系统问题与解决方案知识库
category: system
tags: ['issues', 'pitfalls', 'troubleshooting', 'knowledge-base']
author: 太一 AGI
created: 2026-04-12
status: active
priority: P1
---

# 📝 踩坑记录 Skill - 系统问题与解决方案知识库

> **版本**: v1.0.0 | **创建**: 2026-04-12  
> **定位**: 系统问题与解决方案知识库  
> **优先级**: P1  
> **融合**: Core Guardian Agent v2.0

---

## 🎯 Skill 定位

**核心职责**:
```
✅ 记录系统问题和解决方案
✅ 建立知识库供查询
✅ 自动归类问题类型
✅ 提供解决方案建议
✅ 与 Core Guardian Agent 融合
```

**问题分类**:
```
P0 - 紧急问题：Gateway 停止/Ubuntu 故障
P1 - 重要问题：性能超标/资源不足
P2 - 警告问题：轻微异常/潜在风险
P3 - 提示问题：运行状态/配置变更
```

---

## 📁 文件结构

```
skills/07-system/issue-pitfalls-record/
├── SKILL.md (本文档)
├── issues/
│   ├── P0/ (紧急问题)
│   ├── P1/ (重要问题)
│   ├── P2/ (警告问题)
│   └── P3/ (提示问题)
├── solutions/
│   ├── gateway/ (Gateway 相关)
│   ├── ubuntu/ (Ubuntu 系统相关)
│   ├── taiyi/ (太一系统相关)
│   └── other/ (其他问题)
├── knowledge_base.json (知识库)
└── api.py (API 接口)
```

---

## 🔧 核心功能

### 1. 问题记录

**记录格式**:
```json
{
  "issue_id": "ISSUE-20260412-001",
  "timestamp": "2026-04-12T22:38:00",
  "severity": "P1",
  "category": "gateway",
  "title": "Gateway 端口未监听",
  "description": "Gateway 进程运行但端口 18789 未监听",
  "root_cause": "端口被占用",
  "solution": "重启 Gateway 服务",
  "status": "resolved",
  "resolved_at": "2026-04-12T22:40:00",
  "tags": ["gateway", "port", "network"],
  "related_files": ["/etc/systemd/system/openclaw-gateway.service"]
}
```

---

### 2. 解决方案库

**解决方案格式**:
```json
{
  "solution_id": "SOL-GATEWAY-001",
  "category": "gateway",
  "problem": "Gateway 端口未监听",
  "steps": [
    "1. 检查 Gateway 进程：pgrep -f openclaw-gateway",
    "2. 检查端口占用：netstat -tln | grep 18789",
    "3. 重启 Gateway: systemctl restart openclaw-gateway",
    "4. 验证恢复：netstat -tln | grep 18789"
  ],
  "commands": [
    "pgrep -f openclaw-gateway",
    "netstat -tln | grep 18789",
    "systemctl restart openclaw-gateway"
  ],
  "success_rate": 0.95,
  "avg_time_minutes": 2,
  "last_used": "2026-04-12T22:40:00"
}
```

---

### 3. 知识库查询

**查询接口**:
```python
# 按问题 ID 查询
GET /api/issues/{issue_id}

# 按分类查询
GET /api/issues?category=gateway

# 按严重程度查询
GET /api/issues?severity=P1

# 搜索解决方案
GET /api/solutions/search?q=Gateway 端口

# 获取统计信息
GET /api/stats
```

---

### 4. 与 Core Guardian Agent 融合

**融合方式**:
```python
# Core Guardian Agent 检测到问题时自动记录
if metrics.gateway_running and not metrics.gateway_port_ok:
    # 记录问题
    issue = Issue(
        severity='P1',
        category='gateway',
        title='Gateway 端口未监听',
        description=f'Gateway 进程运行 (PID: {metrics.gateway_pid}) 但端口未监听'
    )
    issue_pitfalls_record.add_issue(issue)
    
    # 查询解决方案
    solution = issue_pitfalls_record.search_solution('Gateway 端口未监听')
    if solution:
        execute_solution(solution)
```

---

## 📊 知识库统计

| 指标 | 数值 | 说明 |
|------|------|------|
| **问题总数** | 0 个 | 新建 |
| **已解决问题** | 0 个 | - |
| **未解决问题** | 0 个 | - |
| **解决方案数** | 0 个 | 新建 |
| **平均解决时间** | 0 分钟 | - |
| **解决成功率** | 0% | - |

---

## 🔗 相关链接

**Core Guardian Agent 融合**:
```
skills/07-system/core-guardian-agent/core_guardian_agent_v2.py
```

**问题记录目录**:
```
skills/07-system/issue-pitfalls-record/issues/
```

**解决方案目录**:
```
skills/07-system/issue-pitfalls-record/solutions/
```

**知识库文件**:
```
skills/07-system/issue-pitfalls-record/knowledge_base.json
```

---

**📝 踩坑记录 Skill 已创建！准备融合到 Core Guardian Agent！**

**太一 AGI · 2026-04-12 22:38**
