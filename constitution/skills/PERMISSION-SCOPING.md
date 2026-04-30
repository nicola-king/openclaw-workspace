# 动态权限授予协议

> 版本：1.0 | 创建时间：2026-04-04 | 层级：Tier 2
> 触发：能力涌现 (Agent Skills 架构学习)

---

## 📋 核心原则

**最小权限 · 按需授予 · 任务回收 · 审计追踪**

---

## 🔐 权限模型

### 权限分级
| 等级 | 权限 | 用途 | 审批 |
|------|------|------|------|
| **L1** | `web_fetch`, `web_search`, `file_read` | 只读操作 | 自动 |
| **L2** | `message`, `canvas`, `file_write`, `image_generate` | 写入/交互 | 自动 |
| **L3** | `exec`, `file_delete` | 系统/删除 | 需 SAYELF 批准 |

### 权限作用域
| 作用域 | 范围 | 示例 |
|--------|------|------|
| `session` | 当前会话 | 消息发送 |
| `workspace` | workspace 目录 | 文件读写 |
| `system` | 系统级 | shell 执行 |
| `network` | 网络访问 | 网页抓取 |

---

## 🔄 权限生命周期

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  REQUEST │ ──→ │   GRANT  │ ──→ │   USE    │
│  请求    │     │  授予    │     │  使用    │
└──────────┘     └──────────┘     └──────────┘
                                          │
                                          ↓
┌──────────┐     ┌──────────┐     ┌──────────┐
│  AUDIT   │ ←── │  REVOKE  │ ←── │  EXPIRE  │
│  审计    │     │  回收    │     │  过期    │
└──────────┘     └──────────┘     └──────────┘
```

---

## ⚡ 权限请求

### 请求格式
```python
class PermissionRequest:
    def __init__(self, skill, permissions, reason, scope="session"):
        self.skill = skill          # 技能名称
        self.permissions = permissions  # 请求权限列表
        self.reason = reason        # 请求原因
        self.scope = scope          # 作用域
        self.timestamp = datetime.now()
        self.status = "pending"     # pending/granted/denied
        self.expires_at = None      # 过期时间
        self.granted_by = None      # 授予人
```

### 请求流程
```python
def request_permissions(skill, permissions, reason):
    # 1. 检查技能元数据
    skill_meta = get_skill_metadata(skill)
    if not skill_meta:
        return False, "技能不存在"
    
    # 2. 验证权限声明
    declared_perms = skill_meta.get("permissions", [])
    for perm in permissions:
        if perm not in declared_perms:
            return False, f"权限 {perm} 未在技能元数据中声明"
    
    # 3. 检查权限等级
    for perm in permissions:
        level = get_permission_level(perm)
        if level == 3:
            # L3 权限需 SAYELF 批准
            return request_sayelf_approval(skill, permissions, reason)
    
    # 4. 自动授予 L1/L2 权限
    grant_permissions(skill, permissions, reason)
    return True, "权限已授予"
```

---

## ✅ 权限授予

### 授予策略
| 条件 | 策略 | 过期时间 |
|------|------|---------|
| L1 权限 | 自动授予 | Session 结束 |
| L2 权限 | 自动授予 | 30 分钟 |
| L3 权限 | SAYELF 批准 | 10 分钟 |
| 高风险操作 | 逐次批准 | 单次使用 |

### 授予记录
```json
{
  "grant_id": "grant-20260404-083800-001",
  "skill": "browser-automation",
  "permissions": ["exec", "canvas"],
  "reason": "执行 Playwright 浏览器自动化",
  "scope": "workspace",
  "granted_at": "2026-04-04T08:38:00+08:00",
  "granted_by": "taiyi",
  "expires_at": "2026-04-04T08:48:00+08:00",
  "status": "active"
}
```

### 权限令牌
```python
class PermissionToken:
    def __init__(self, grant_id, permissions, expires_at):
        self.grant_id = grant_id
        self.permissions = set(permissions)
        self.expires_at = expires_at
        self.used_count = 0
        self.max_uses = None  # None=无限
    
    def is_valid(self, permission):
        """检查权限是否有效"""
        if datetime.now() > self.expires_at:
            return False, "权限已过期"
        if permission not in self.permissions:
            return False, f"权限 {permission} 未授予"
        if self.max_uses and self.used_count >= self.max_uses:
            return False, "权限使用次数已耗尽"
        return True, "有效"
    
    def use(self, permission):
        """使用权限"""
        valid, reason = self.is_valid(permission)
        if valid:
            self.used_count += 1
        return valid, reason
```

---

## 🎯 权限使用

### 使用前检查
```python
def check_permission_before_use(skill, permission, action):
    """使用权限前检查"""
    token = get_active_token(skill)
    
    if not token:
        log_audit_event("permission_denied", {
            "skill": skill,
            "permission": permission,
            "action": action,
            "reason": "无有效令牌"
        })
        return False, "无有效权限令牌"
    
    valid, reason = token.is_valid(permission)
    if not valid:
        log_audit_event("permission_denied", {
            "skill": skill,
            "permission": permission,
            "action": action,
            "reason": reason
        })
        return False, reason
    
    # 记录使用
    token.use(permission)
    log_audit_event("permission_used", {
        "skill": skill,
        "permission": permission,
        "action": action,
        "grant_id": token.grant_id
    })
    
    return True, "权限验证通过"
```

### 高风险操作拦截
```python
HIGH_RISK_COMMANDS = [
    "rm -rf", "dd", "mkfs", "chmod 777",
    "curl | bash", "wget | bash",
    "sudo", "su", "passwd"
]

def intercept_high_risk_exec(command):
    """拦截高风险命令"""
    for pattern in HIGH_RISK_COMMANDS:
        if pattern in command:
            log_audit_event("high_risk_intercepted", {
                "command": command,
                "pattern": pattern
            })
            return False, f"高风险命令被拦截：{pattern}"
    
    # 需要 SAYELF 批准
    return request_sayelf_approval("exec", command)
```

---

## 💨 权限回收

### 回收触发条件
| 条件 | 动作 |
|------|------|
| 令牌过期 | 自动回收 |
| 任务完成 | 自动回收 |
| Session 结束 | 回收所有 |
| 异常检测 | 立即回收 + 告警 |
| 用户请求 | 立即回收 |

### 回收流程
```python
def revoke_permissions(skill, reason="task_completed"):
    """回收技能权限"""
    token = get_active_token(skill)
    if not token:
        return
    
    # 1. 记录回收
    log_audit_event("permission_revoked", {
        "skill": skill,
        "grant_id": token.grant_id,
        "reason": reason,
        "used_count": token.used_count
    })
    
    # 2. 撤销令牌
    token.permissions = set()
    token.expires_at = datetime.now()
    
    # 3. 清理状态
    remove_active_token(skill)
    
    # 4. 通知技能
    if hasattr(skill, 'on_permissions_revoked'):
        skill.on_permissions_revoked()
```

---

## 📊 审计追踪

### 审计事件类型
| 事件 | 触发条件 | 记录内容 |
|------|---------|---------|
| `permission_requested` | 请求权限 | skill, permissions, reason |
| `permission_granted` | 授予权限 | grant_id, permissions, expires |
| `permission_used` | 使用权限 | skill, permission, action |
| `permission_denied` | 拒绝权限 | skill, permission, reason |
| `permission_revoked` | 回收权限 | skill, grant_id, reason |
| `high_risk_intercepted` | 高风险拦截 | command, pattern |
| `sayelf_approval_required` | 需 SAYELF 批准 | skill, permissions, action |

### 审计日志格式
```json
{
  "timestamp": "2026-04-04T08:38:00+08:00",
  "event": "permission_used",
  "skill": "browser-automation",
  "permission": "exec",
  "action": "playwright run",
  "grant_id": "grant-20260404-083800-001",
  "session_id": "agent:main:wechat:direct",
  "user": "SAYELF"
}
```

### 审计日志存储
```
workspace/
└── logs/
    └── audit/
        ├── 2026-04/
        │   ├── 04/
        │   │   ├── permission-20260404.log
        │   │   └── high-risk-20260404.log
        │   └── ...
        └── ...
```

---

## 🔧 工具脚本

### 权限管理 CLI
```bash
#!/bin/bash
# scripts/permission-manager.sh

case "$1" in
  list)
    # 列出当前授予的权限
    python scripts/permission_manager.py list
    ;;
  grant)
    # 手动授予权限
    python scripts/permission_manager.py grant "$2" "$3"
    ;;
  revoke)
    # 回收权限
    python scripts/permission_manager.py revoke "$2"
    ;;
  audit)
    # 查看审计日志
    python scripts/permission_manager.py audit "$2"
    ;;
  stats)
    # 显示统计
    python scripts/permission_manager.py stats
    ;;
  *)
    echo "Usage: $0 {list|grant|revoke|audit|stats}"
    exit 1
    ;;
esac
```

### Python 管理器
```python
#!/usr/bin/env python3
# scripts/permission_manager.py

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

STATE_FILE = Path("/tmp/permission-state.json")
AUDIT_LOG_DIR = Path("/home/nicola/.openclaw/workspace/logs/audit")

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"grants": [], "tokens": {}}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def list_grants():
    """列出当前授予的权限"""
    state = load_state()
    active_grants = [g for g in state["grants"] if g["status"] == "active"]
    
    print(f"活跃授权：{len(active_grants)}")
    for grant in active_grants:
        expires = grant.get("expires_at", "never")
        print(f"  - {grant['skill']}: {', '.join(grant['permissions'])}")
        print(f"    过期：{expires}")
        print(f"    使用：{grant.get('used_count', 0)} 次")

def audit_log(skill=None, date=None):
    """查看审计日志"""
    if date is None:
        date = datetime.now().strftime("%Y-%m/%d")
    
    log_file = AUDIT_LOG_DIR / date / f"permission-{datetime.now().strftime('%Y%m%d')}.log"
    
    if not log_file.exists():
        print("无审计日志")
        return
    
    content = log_file.read_text()
    if skill:
        content = "\n".join([l for l in content.split("\n") if skill in l])
    
    print(content)

def stats():
    """显示权限统计"""
    state = load_state()
    
    total_grants = len(state["grants"])
    active_grants = len([g for g in state["grants"] if g["status"] == "active"])
    
    print(f"总授权数：{total_grants}")
    print(f"活跃授权：{active_grants}")
    print(f"已回收：{total_grants - active_grants}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python permission_manager.py {list|audit|stats}")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "list":
        list_grants()
    elif cmd == "audit":
        audit_log(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "stats":
        stats()
    else:
        print(f"Unknown command: {cmd}")
```

---

## 📈 监控指标

| 指标 | 目标 | 告警 |
|------|------|------|
| 活跃授权数 | <20 | >50 |
| L3 权限请求 | <10/小时 | >30/小时 |
| 权限拒绝率 | <5% | >20% |
| 高风险拦截 | 0 | >5/小时 |
| 过期未回收 | 0 | >10 |

---

## 🔗 相关文件

| 文件 | 用途 |
|------|------|
| `constitution/skills/PERMISSION-SCOPING.md` | 本文件 |
| `constitution/skills/SKILL-LIFECYCLE.md` | 生命周期管理 |
| `constitution/skills/SKILL-METADATA.md` | 技能元数据标准 |
| `scripts/permission-manager.sh` | CLI 工具 |
| `scripts/permission_manager.py` | Python 管理器 |

---

*创建时间：2026-04-04 | 太一 AGI · 能力涌现*
