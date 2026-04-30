#!/usr/bin/env python3
"""
Heal-State Skill - 自愈汇报模块
"""

from pathlib import Path
from .core import HealState

class HealReporter:
    """自愈汇报生成器"""
    
    def __init__(self):
        self.heal_state = HealState()
    
    def generate_report(self) -> str:
        """生成自愈汇报"""
        state = self.heal_state.get_state()
        intervention = self.heal_state._read_json(self.heal_state.INTERVENTION_FILE)
        
        lines = []
        lines.append("🚑 自愈系统汇报")
        lines.append("")
        
        # 状态
        status_map = {
            "idle": "✅ 正常",
            "checking": "🔍 检查中",
            "healing": "🔧 自愈中",
            "intervention_required": "🚨 需要人工干预"
        }
        status = status_map.get(state.get("status", "idle"), state.get("status"))
        lines.append(f"【系统状态】{status}")
        
        # 统计
        lines.append(f"【连续成功】{state.get('consecutiveSuccesses', 0)} 次")
        lines.append(f"【总失败】{state.get('totalFailures', 0)} 次")
        lines.append(f"【最后检查】{state.get('lastCheck', '从未')}")
        lines.append(f"【最后自愈】{state.get('lastHeal', '从未')}")
        lines.append("")
        
        # 当前问题
        issues = state.get("currentIssues", [])
        if issues:
            lines.append("【当前问题】")
            for issue in issues:
                issue_id = issue.get("id", "unknown")
                attempts = state.get("healAttempts", {}).get(issue_id, 0)
                lines.append(f"  - {issue.get('name', 'Unknown')}: {attempts}次尝试")
        else:
            lines.append("【当前问题】无")
        
        lines.append("")
        
        # 人工干预警告
        if intervention.get("required"):
            lines.append("🚨 人工干预告警！")
            lines.append(f"   原因：{intervention.get('reason', '未知')}")
            lines.append(f"   时间：{intervention.get('triggeredAt', '未知')}")
            lines.append("")
            lines.append("   请 SAYELF 检查并修复后执行：")
            lines.append("   /自愈重置")
        
        # 防死循环状态
        lines.append("")
        lines.append("【防死循环保护】")
        lines.append(f"   单问题最大尝试：{HealState.MAX_RETRY_ATTEMPTS}次")
        lines.append(f"   总失败阈值：{HealState.MAX_TOTAL_FAILURES}次")
        lines.append(f"   自愈冷却时间：{HealState.COOLDOWN_MINUTES}分钟")
        
        return "\n".join(lines)


if __name__ == "__main__":
    reporter = HealReporter()
    print(reporter.generate_report())
