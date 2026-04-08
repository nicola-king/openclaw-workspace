#!/usr/bin/env python3
"""
Heal-State Skill - 自愈成果汇报
每次自愈完成后生成详细汇报
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))

from core import HealState

class HealResultReporter:
    """自愈成果汇报生成器"""
    
    def __init__(self):
        self.heal_state = HealState()
    
    def generate_result_report(self, issue_id: str, action: str, success: bool, details: dict = None) -> str:
        """
        生成单次自愈成果汇报
        
        Args:
            issue_id: 问题 ID
            action: 自愈动作
            success: 是否成功
            details: 详细信息
        """
        state = self.heal_state.get_state()
        attempts = state.get("healAttempts", {}).get(issue_id, 0)
        
        lines = []
        
        # 标题
        if success:
            lines.append("✅ 自愈成功！")
        else:
            lines.append("❌ 自愈失败")
        
        lines.append("")
        
        # 问题信息
        lines.append(f"【问题】{issue_id}")
        lines.append(f"【动作】{action}")
        lines.append(f"【尝试次数】{attempts}次")
        lines.append(f"【结果】{'成功' if success else '失败'}")
        
        if details:
            lines.append("")
            lines.append("【详情】")
            for key, value in details.items():
                lines.append(f"  {key}: {value}")
        
        lines.append("")
        
        # 统计信息
        lines.append("【统计】")
        lines.append(f"  连续成功：{state.get('consecutiveSuccesses', 0)} 次")
        lines.append(f"  总失败：{state.get('totalFailures', 0)} 次")
        
        # 警告
        intervention_needed, intervention = self.heal_state.needs_intervention()
        if intervention_needed:
            lines.append("")
            lines.append("🚨 需要人工干预！")
            lines.append(f"   原因：{intervention.get('reason', '未知')}")
            lines.append(f"   请 SAYELF 检查并修复后发送：/自愈重置")
        
        return "\n".join(lines)
    
    def generate_periodic_report(self) -> str:
        """生成周期性汇报（10 分钟）"""
        state = self.heal_state.get_state()
        history = self.heal_state._read_json(self.heal_state.HISTORY_FILE)
        
        lines = []
        lines.append("🚑 自愈系统周期汇报")
        lines.append("")
        
        # 状态
        status_map = {
            "idle": "✅ 正常",
            "checking": "🔍 检查中",
            "healing": "🔧 自愈中",
            "intervention_required": "🚨 需要人工干预"
        }
        lines.append(f"【系统状态】{status_map.get(state.get('status', 'idle'), '未知')}")
        
        # 本次周期统计
        entries = history.get("entries", [])
        recent = [e for e in entries if self._is_recent(e.get("timestamp", ""))]
        
        successes = sum(1 for e in recent if e.get("result") == "success")
        failures = sum(1 for e in recent if e.get("result") == "failure")
        
        lines.append(f"【本次周期】{len(recent)} 次自愈")
        lines.append(f"  ✅ 成功：{successes}")
        lines.append(f"  ❌ 失败：{failures}")
        
        lines.append("")
        
        # 最近自愈记录
        if recent:
            lines.append("【最近自愈】")
            for entry in recent[-5:]:  # 最近 5 次
                timestamp = entry.get("timestamp", "")[:16].replace("T", " ")
                result = "✅" if entry.get("result") == "success" else "❌"
                issue = entry.get("issueId", "unknown")
                lines.append(f"  {result} {timestamp} - {issue}")
        
        lines.append("")
        
        # 防死循环状态
        lines.append("【防死循环保护】")
        lines.append(f"  单问题最大尝试：{HealState.MAX_RETRY_ATTEMPTS}次")
        lines.append(f"  总失败阈值：{HealState.MAX_TOTAL_FAILURES}次")
        lines.append(f"  冷却时间：{HealState.COOLDOWN_MINUTES}分钟")
        
        # 人工干预检查
        intervention_needed, intervention = self.heal_state.needs_intervention()
        if intervention_needed:
            lines.append("")
            lines.append("🚨 人工干预警告！")
            lines.append(f"   原因：{intervention.get('reason', '未知')}")
            lines.append(f"   时间：{intervention.get('triggeredAt', '未知')}")
            lines.append("")
            lines.append("   请 SAYELF 立即检查并发送：/自愈重置")
        
        return "\n".join(lines)
    
    def _is_recent(self, timestamp: str) -> bool:
        """检查是否为最近 10 分钟内的记录"""
        if not timestamp:
            return False
        try:
            ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            return (now - ts).total_seconds() < 600  # 10 分钟
        except:
            return False


def generate_result_report(issue_id: str, action: str, success: bool, details: dict = None):
    """生成自愈成果汇报"""
    reporter = HealResultReporter()
    report = reporter.generate_result_report(issue_id, action, success, details or {})
    print(report)
    return report

def generate_periodic_report():
    """生成周期汇报"""
    reporter = HealResultReporter()
    report = reporter.generate_periodic_report()
    print(report)
    return report

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "periodic":
        generate_periodic_report()
    else:
        # 测试
        generate_result_report(
            issue_id="gateway_down",
            action="重启 Gateway",
            success=True,
            details={"耗时": "3 秒", "PID": "223263"}
        )
