#!/usr/bin/env python3
# scripts/permission-tool-integration.py
# 用途：权限管理集成到工具调用链的示例代码

import json
from pathlib import Path
from datetime import datetime, timedelta

STATE_FILE = Path("/tmp/permission-tool-state.json")
AUDIT_LOG_FILE = Path("/home/nicola/.openclaw/workspace/logs/audit/permission-audit.log")

class PermissionManager:
    """权限管理器 - 集成到工具调用链"""
    
    # 权限分级
    L1_PERMISSIONS = {"web_fetch", "web_search", "file_read"}
    L2_PERMISSIONS = {"message", "canvas", "file_write", "image_generate"}
    L3_PERMISSIONS = {"exec", "file_delete"}
    
    # 高风险命令模式
    HIGH_RISK_PATTERNS = [
        "rm -rf", "dd", "mkfs", "chmod 777",
        "curl | bash", "wget | bash",
        "sudo", "su", "passwd"
    ]
    
    def __init__(self):
        self.state = self._load_state()
        self.active_tokens = {}
    
    def _load_state(self):
        """加载状态"""
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
        return {"grants": [], "tokens": {}}
    
    def _save_state(self):
        """保存状态"""
        STATE_FILE.write_text(json.dumps(self.state, indent=2, ensure_ascii=False))
    
    def _log_audit(self, event, data):
        """记录审计日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            **data
        }
        
        # 确保目录存在
        AUDIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(AUDIT_LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        print(f"📝 审计：{event} - {data.get('skill', 'unknown')}")
    
    def get_permission_level(self, permission):
        """获取权限等级"""
        if permission in self.L1_PERMISSIONS:
            return 1
        elif permission in self.L2_PERMISSIONS:
            return 2
        elif permission in self.L3_PERMISSIONS:
            return 3
        return 3  # 默认高权限
    
    def request_permission(self, skill, permissions, reason, scope="session"):
        """
        请求权限
        
        Args:
            skill: 技能名称
            permissions: 请求的权限列表
            reason: 请求原因
            scope: 作用域 (session/workspace/system)
        
        Returns:
            (granted, message, token_id)
        """
        print(f"🔑 权限请求：{skill} 请求 {permissions}")
        print(f"   原因：{reason}")
        
        # 检查最高权限等级
        max_level = max(self.get_permission_level(p) for p in permissions)
        
        if max_level == 3:
            # L3 权限需 SAYELF 批准
            self._log_audit("sayelf_approval_required", {
                "skill": skill,
                "permissions": permissions,
                "reason": reason,
                "level": "L3"
            })
            
            # 模拟 SAYELF 批准 (实际需用户交互)
            print(f"⚠️  L3 权限需 SAYELF 批准")
            print(f"   命令：/approve {skill} {permissions}")
            
            # 这里简化为自动批准 (实际应等待用户确认)
            granted = True
            granted_by = "taiyi_auto"
        else:
            # L1/L2 自动授予
            granted = True
            granted_by = "auto"
        
        if not granted:
            self._log_audit("permission_denied", {
                "skill": skill,
                "permissions": permissions,
                "reason": "L3 requires approval"
            })
            return False, "需 SAYELF 批准", None
        
        # 生成授权令牌
        token_id = f"token-{datetime.now().strftime('%Y%m%d%H%M%S')}-{skill}"
        expires_at = (datetime.now() + timedelta(minutes=10 if max_level == 3 else 30)).isoformat()
        
        token = {
            "token_id": token_id,
            "skill": skill,
            "permissions": permissions,
            "scope": scope,
            "granted_at": datetime.now().isoformat(),
            "expires_at": expires_at,
            "granted_by": granted_by,
            "used_count": 0,
            "max_uses": None
        }
        
        self.active_tokens[skill] = token
        self.state["grants"].append(token)
        self._save_state()
        
        self._log_audit("permission_granted", {
            "skill": skill,
            "permissions": permissions,
            "token_id": token_id,
            "expires_at": expires_at
        })
        
        print(f"✅ 权限已授予：{token_id}")
        print(f"   过期：{expires_at}")
        return True, "权限已授予", token_id
    
    def check_permission(self, skill, permission, action=None):
        """
        检查权限 (工具调用前检查)
        
        Args:
            skill: 技能名称
            permission: 请求的权限
            action: 具体动作 (如 exec 的命令)
        
        Returns:
            (allowed, message)
        """
        # 检查是否有活跃令牌
        if skill not in self.active_tokens:
            self._log_audit("permission_denied", {
                "skill": skill,
                "permission": permission,
                "reason": "no_active_token"
            })
            return False, f"技能 {skill} 无活跃权限令牌"
        
        token = self.active_tokens[skill]
        
        # 检查过期
        expires_at = datetime.fromisoformat(token["expires_at"])
        if datetime.now() > expires_at:
            self._log_audit("permission_denied", {
                "skill": skill,
                "permission": permission,
                "reason": "token_expired"
            })
            return False, f"权限令牌已过期 ({expires_at})"
        
        # 检查权限是否在令牌中
        if permission not in token["permissions"]:
            self._log_audit("permission_denied", {
                "skill": skill,
                "permission": permission,
                "reason": "permission_not_in_token"
            })
            return False, f"权限 {permission} 未授予"
        
        # 检查高风险命令
        if permission == "exec" and action:
            for pattern in self.HIGH_RISK_PATTERNS:
                if pattern in action:
                    self._log_audit("high_risk_intercepted", {
                        "skill": skill,
                        "permission": permission,
                        "action": action,
                        "pattern": pattern
                    })
                    return False, f"高风险命令被拦截：{pattern}"
        
        # 更新使用计数
        token["used_count"] += 1
        
        self._log_audit("permission_used", {
            "skill": skill,
            "permission": permission,
            "action": action,
            "token_id": token["token_id"],
            "used_count": token["used_count"]
        })
        
        return True, "权限验证通过"
    
    def revoke_permission(self, skill, reason="task_completed"):
        """回收权限"""
        if skill not in self.active_tokens:
            return
        
        token = self.active_tokens[skill]
        
        self._log_audit("permission_revoked", {
            "skill": skill,
            "token_id": token["token_id"],
            "reason": reason,
            "used_count": token["used_count"]
        })
        
        # 标记为已回收
        token["revoked"] = True
        token["revoked_at"] = datetime.now().isoformat()
        
        del self.active_tokens[skill]
        self._save_state()
        
        print(f"💨 权限已回收：{skill} ({reason})")
    
    def list_active_permissions(self):
        """列出活跃权限"""
        print("\n活跃权限:")
        print("-" * 40)
        
        if not self.active_tokens:
            print("  无活跃权限")
            return
        
        for skill, token in self.active_tokens.items():
            expires = token["expires_at"]
            used = token["used_count"]
            perms = ", ".join(token["permissions"])
            print(f"  {skill}:")
            print(f"    权限：{perms}")
            print(f"    过期：{expires}")
            print(f"    使用：{used} 次")


# 工具调用链集成示例
class ToolChainWithPermission:
    """带权限管理的工具调用链"""
    
    def __init__(self):
        self.perm_manager = PermissionManager()
    
    def call_tool(self, tool_name, skill, **kwargs):
        """
        调用工具 (带权限检查)
        
        使用方式:
            chain = ToolChainWithPermission()
            
            # 先请求权限
            chain.perm_manager.request_permission(
                skill="browser-automation",
                permissions=["exec", "canvas"],
                reason="执行浏览器自动化测试"
            )
            
            # 调用工具 (自动检查权限)
            chain.call_tool("exec", "browser-automation", command="playwright run")
        """
        # 映射工具到权限
        tool_to_permission = {
            "exec": "exec",
            "web_fetch": "web_fetch",
            "web_search": "web_search",
            "canvas": "canvas",
            "message": "message",
            "file_read": "file_read",
            "file_write": "file_write",
            "file_delete": "file_delete",
            "image_generate": "image_generate"
        }
        
        required_permission = tool_to_permission.get(tool_name)
        if not required_permission:
            return False, f"未知工具：{tool_name}"
        
        # 检查权限
        action = kwargs.get("command") if tool_name == "exec" else None
        allowed, message = self.perm_manager.check_permission(
            skill, required_permission, action
        )
        
        if not allowed:
            print(f"❌ 工具调用被拒绝：{tool_name}")
            print(f"   原因：{message}")
            return False, message
        
        # 权限验证通过，执行工具调用
        print(f"✅ 工具调用：{tool_name} (技能：{skill})")
        print(f"   参数：{kwargs}")
        
        # 这里模拟工具执行 (实际应调用真实工具)
        # result = actual_tool_call(tool_name, **kwargs)
        
        return True, "工具调用成功"


def demo():
    """演示权限管理集成"""
    print("=" * 60)
    print("权限管理集成到工具调用链 - 演示")
    print("=" * 60)
    print()
    
    # 创建工具链
    chain = ToolChainWithPermission()
    
    # 场景 1: 请求 L1/L2 权限 (自动授予)
    print("[场景 1] 请求 L1/L2 权限 (自动授予)")
    print("-" * 40)
    chain.perm_manager.request_permission(
        skill="browser-automation",
        permissions=["web_fetch", "canvas"],
        reason="浏览器自动化测试"
    )
    print()
    
    # 场景 2: 工具调用 (权限验证通过)
    print("[场景 2] 工具调用 (权限验证通过)")
    print("-" * 40)
    chain.call_tool("web_fetch", "browser-automation", url="https://example.com")
    chain.call_tool("canvas", "browser-automation", action="navigate")
    print()
    
    # 场景 3: 请求 L3 权限 (需批准)
    print("[场景 3] 请求 L3 权限 (需 SAYELF 批准)")
    print("-" * 40)
    chain.perm_manager.request_permission(
        skill="browser-automation",
        permissions=["exec"],
        reason="执行 Playwright 命令"
    )
    print()
    
    # 场景 4: 工具调用 (高风险命令拦截)
    print("[场景 4] 工具调用 (高风险命令拦截)")
    print("-" * 40)
    allowed, msg = chain.call_tool("exec", "browser-automation", command="rm -rf /tmp")
    print(f"   结果：{'允许' if allowed else '拒绝'} - {msg}")
    print()
    
    # 场景 5: 正常 exec 调用
    print("[场景 5] 工具调用 (正常 exec)")
    print("-" * 40)
    chain.call_tool("exec", "browser-automation", command="playwright run test.js")
    print()
    
    # 场景 6: 列出活跃权限
    print("[场景 6] 列出活跃权限")
    print("-" * 40)
    chain.perm_manager.list_active_permissions()
    print()
    
    # 场景 7: 回收权限
    print("[场景 7] 回收权限 (任务完成)")
    print("-" * 40)
    chain.perm_manager.revoke_permission("browser-automation", "task_completed")
    print()
    
    # 场景 8: 权限回收后调用
    print("[场景 8] 权限回收后调用 (应被拒绝)")
    print("-" * 40)
    allowed, msg = chain.call_tool("web_fetch", "browser-automation", url="https://example.com")
    print(f"   结果：{'允许' if allowed else '拒绝'} - {msg}")
    print()
    
    print("=" * 60)
    print("✅ 演示完成")
    print("=" * 60)


if __name__ == "__main__":
    demo()
