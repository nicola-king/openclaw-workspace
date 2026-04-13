#!/usr/bin/env python3
"""
Heal-State Skill - 自愈状态管理与防死循环机制
版本：v1.0 | 创建：2026-04-01
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any

class HealState:
    """自愈状态管理器"""
    
    STATE_FILE = Path("/tmp/heal-state.json")
    HISTORY_FILE = Path("/tmp/heal-history.json")
    INTERVENTION_FILE = Path("/tmp/heal-intervention-required.json")
    
    # 防死循环阈值
    MAX_RETRY_ATTEMPTS = 3  # 单问题最大自愈次数
    MAX_TOTAL_FAILURES = 5  # 总失败次数阈值
    COOLDOWN_MINUTES = 10   # 自愈间隔（分钟）
    INTERVENTION_WINDOW = 60  # 统计窗口（分钟）
    
    def __init__(self):
        self._ensure_files()
    
    def _ensure_files(self):
        """确保状态文件存在"""
        for f in [self.STATE_FILE, self.HISTORY_FILE, self.INTERVENTION_FILE]:
            if not f.exists():
                f.parent.mkdir(parents=True, exist_ok=True)
                self._write_json(f, self._default_for(f))
    
    def _default_for(self, path: Path) -> dict:
        """返回文件的默认结构"""
        if path == self.STATE_FILE:
            return {
                "lastCheck": None,
                "lastHeal": None,
                "status": "idle",  # idle, checking, healing, intervention_required
                "currentIssues": [],
                "healAttempts": {},  # issue_id -> count
                "totalFailures": 0,
                "consecutiveSuccesses": 0,
                "lastIntervention": None
            }
        elif path == self.HISTORY_FILE:
            return {"entries": []}
        elif path == self.INTERVENTION_FILE:
            return {
                "required": False,
                "reason": None,
                "triggeredAt": None,
                "issues": []
            }
        return {}
    
    def _read_json(self, path: Path) -> dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return self._default_for(path)
    
    def _write_json(self, path: Path, data: dict):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_state(self) -> dict:
        """获取当前状态"""
        return self._read_json(self.STATE_FILE)
    
    def update_state(self, **kwargs):
        """更新状态"""
        state = self.get_state()
        for key, value in kwargs.items():
            if key in state:
                state[key] = value
        state["lastCheck"] = datetime.now(timezone.utc).isoformat()
        self._write_json(self.STATE_FILE, state)
    
    def start_check(self):
        """开始检查"""
        self.update_state(status="checking")
    
    def start_heal(self, issue_id: str):
        """开始自愈"""
        state = self.get_state()
        state["status"] = "healing"
        state["lastHeal"] = datetime.now(timezone.utc).isoformat()
        
        # 计数自愈尝试
        if issue_id not in state["healAttempts"]:
            state["healAttempts"][issue_id] = 0
        state["healAttempts"][issue_id] += 1
        
        self._write_json(self.STATE_FILE, state)
    
    def record_success(self, issue_id: str):
        """记录自愈成功"""
        state = self.get_state()
        state["consecutiveSuccesses"] += 1
        state["totalFailures"] = max(0, state["totalFailures"] - 1)
        
        # 清理已成功的尝试计数
        if issue_id in state["healAttempts"]:
            del state["healAttempts"][issue_id]
        
        self._write_json(self.STATE_FILE, state)
        self._log_history(issue_id, "success")
    
    def record_failure(self, issue_id: str, reason: str):
        """记录自愈失败"""
        state = self.get_state()
        state["consecutiveSuccesses"] = 0
        state["totalFailures"] += 1
        
        self._write_json(self.STATE_FILE, state)
        self._log_history(issue_id, "failure", reason)
        
        # 检查是否需要人工干预
        self._check_intervention_needed(issue_id, reason)
    
    def _log_history(self, issue_id: str, result: str, reason: str = ""):
        """记录历史"""
        history = self._read_json(self.HISTORY_FILE)
        history["entries"].append({
            "issueId": issue_id,
            "result": result,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        # 保留最近 100 条
        history["entries"] = history["entries"][-100:]
        self._write_json(self.HISTORY_FILE, history)
    
    def _check_intervention_needed(self, issue_id: str, reason: str):
        """检查是否需要人工干预"""
        state = self.get_state()
        intervention = self._read_json(self.INTERVENTION_FILE)
        
        # 条件 1: 单问题自愈次数超限
        attempts = state["healAttempts"].get(issue_id, 0)
        if attempts >= self.MAX_RETRY_ATTEMPTS:
            intervention["required"] = True
            intervention["reason"] = f"单问题自愈次数超限 ({attempts}/{self.MAX_RETRY_ATTEMPTS})"
            intervention["triggeredAt"] = datetime.now(timezone.utc).isoformat()
            intervention["issues"].append({
                "id": issue_id,
                "attempts": attempts,
                "reason": reason
            })
        
        # 条件 2: 总失败次数超限
        if state["totalFailures"] >= self.MAX_TOTAL_FAILURES:
            intervention["required"] = True
            intervention["reason"] = f"总失败次数超限 ({state['totalFailures']}/{self.MAX_TOTAL_FAILURES})"
            intervention["triggeredAt"] = datetime.now(timezone.utc).isoformat()
        
        self._write_json(self.INTERVENTION_FILE, intervention)
        
        if intervention["required"]:
            state["status"] = "intervention_required"
            state["lastIntervention"] = datetime.now(timezone.utc).isoformat()
            self._write_json(self.STATE_FILE, state)
    
    def needs_intervention(self) -> tuple[bool, Optional[dict]]:
        """检查是否需要人工干预"""
        intervention = self._read_json(self.INTERVENTION_FILE)
        return intervention["required"], intervention if intervention["required"] else None
    
    def reset_intervention(self):
        """重置人工干预状态（人工修复后调用）"""
        state = self.get_state()
        state["healAttempts"] = {}
        state["totalFailures"] = 0
        state["status"] = "idle"
        self._write_json(self.STATE_FILE, state)
        
        self._write_json(self.INTERVENTION_FILE, {
            "required": False,
            "reason": None,
            "triggeredAt": None,
            "issues": []
        })
    
    def can_heal(self, issue_id: str) -> tuple[bool, str]:
        """检查是否可以自愈（防死循环）"""
        state = self.get_state()
        
        # 检查是否需要人工干预
        if state["status"] == "intervention_required":
            return False, "需要人工干预"
        
        # 检查自愈次数
        attempts = state["healAttempts"].get(issue_id, 0)
        if attempts >= self.MAX_RETRY_ATTEMPTS:
            return False, f"自愈次数超限 ({attempts}/{self.MAX_RETRY_ATTEMPTS})"
        
        # 检查冷却时间
        if state["lastHeal"]:
            last_heal = datetime.fromisoformat(state["lastHeal"].replace('Z', '+00:00'))
            cooldown = datetime.now(timezone.utc) - last_heal
            if cooldown.total_seconds() < self.COOLDOWN_MINUTES * 60:
                remaining = self.COOLDOWN_MINUTES - cooldown.total_seconds() / 60
                return False, f"冷却中 ({remaining:.1f}分钟)"
        
        return True, "可以自愈"
    
    def get_summary(self) -> str:
        """获取状态摘要"""
        state = self.get_state()
        intervention = self._read_json(self.INTERVENTION_FILE)
        
        lines = []
        lines.append("🚑 自愈系统状态")
        lines.append("")
        lines.append(f"【状态】{self._translate_status(state['status'])}")
        lines.append(f"【最后检查】{state['lastCheck'] or '从未'}")
        lines.append(f"【最后自愈】{state['lastHeal'] or '从未'}")
        lines.append("")
        
        if state["currentIssues"]:
            lines.append("【当前问题】")
            for issue in state["currentIssues"]:
                attempts = state["healAttempts"].get(issue.get('id', 'unknown'), 0)
                lines.append(f"  - {issue.get('name', 'Unknown')} (尝试：{attempts}次)")
        else:
            lines.append("【当前问题】无")
        
        lines.append("")
        lines.append(f"【连续成功】{state['consecutiveSuccesses']} 次")
        lines.append(f"【总失败】{state['totalFailures']} 次")
        
        if intervention["required"]:
            lines.append("")
            lines.append("🚨 需要人工干预！")
            lines.append(f"   原因：{intervention['reason']}")
            lines.append(f"   时间：{intervention['triggeredAt']}")
        
        return "\n".join(lines)
    
    def _translate_status(self, status: str) -> str:
        """翻译状态"""
        mapping = {
            "idle": "空闲",
            "checking": "检查中",
            "healing": "自愈中",
            "intervention_required": "需要人工干预"
        }
        return mapping.get(status, status)


# 便捷函数
def get_state() -> dict:
    """获取状态"""
    return HealState().get_state()

def needs_intervention() -> tuple[bool, Optional[dict]]:
    """检查是否需要人工干预"""
    return HealState().needs_intervention()

def get_summary() -> str:
    """获取摘要"""
    return HealState().get_summary()

if __name__ == "__main__":
    # 测试
    heal = HealState()
    print(heal.get_summary())
