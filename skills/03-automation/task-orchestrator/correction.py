#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction Mechanism - 纠偏机制
检测异常并自动/手动介入处理
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

AGENTS_DIR = Path.home() / ".openclaw" / "agents"
WORKSPACE = Path.home() / ".openclaw" / "workspace"
CORRECTION_LOG = WORKSPACE / "reports" / "correction-log.json"

class CorrectionMechanism:
    """纠偏机制"""
    
    def __init__(self):
        self.agents_dir = AGENTS_DIR
        self.correction_log = self._load_log()
    
    def _load_log(self) -> List[Dict]:
        """加载纠偏日志"""
        if CORRECTION_LOG.exists():
            return json.loads(CORRECTION_LOG.read_text(encoding='utf-8'))
        return []
    
    def _save_log(self):
        """保存纠偏日志"""
        CORRECTION_LOG.parent.mkdir(parents=True, exist_ok=True)
        CORRECTION_LOG.write_text(json.dumps(self.correction_log, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def detect_anomalies(self) -> List[Dict]:
        """
        检测异常
        
        异常类型:
        - 未确认：分发后 10 分钟未确认
        - 进度滞后：落后计划 30 分钟/1 小时/2 小时
        - 阻塞：Bot 上报阻塞
        - 超时：超过截止时间
        """
        anomalies = []
        now = datetime.now()
        
        for bot_dir in self.agents_dir.iterdir():
            if not bot_dir.is_dir():
                continue
            
            bot = bot_dir.name
            inbox = bot_dir / "inbox"
            outbox = bot_dir / "outbox"
            
            # 检查未确认任务
            if inbox.exists():
                for task_file in inbox.glob("TASK-DISPATCH-*.md"):
                    created = datetime.fromtimestamp(task_file.stat().st_mtime)
                    elapsed = (now - created).seconds / 60  # 分钟
                    
                    if elapsed > 10:
                        # 检查是否有确认回复
                        has_confirmation = False
                        if outbox.exists():
                            for report_file in outbox.glob("*.md"):
                                content = report_file.read_text(encoding='utf-8')
                                if task_file.stem in content:
                                    has_confirmation = True
                                    break
                        
                        if not has_confirmation:
                            anomalies.append({
                                "type": "no_confirmation",
                                "severity": "P1",
                                "bot": bot,
                                "task_id": task_file.stem,
                                "elapsed_minutes": elapsed,
                                "detected_at": now.isoformat(),
                                "action": "notify_taiyi"
                            })
            
            # 检查阻塞任务
            if outbox.exists():
                for report_file in outbox.glob("BLOCKED-*.md"):
                    content = report_file.read_text(encoding='utf-8')
                    anomalies.append({
                        "type": "blocked",
                        "severity": "P0",
                        "bot": bot,
                        "task_id": report_file.stem,
                        "description": self._extract_blocker(content),
                        "detected_at": now.isoformat(),
                        "action": "taiyi_intervene"
                    })
        
        return anomalies
    
    def _extract_blocker(self, content: str) -> str:
        """从阻塞报告中提取阻塞原因"""
        import re
        match = re.search(r'阻塞 [：:]\s*(.+?)(?:\n|$)', content)
        return match.group(1).strip() if match else "未知原因"
    
    def handle_anomaly(self, anomaly: Dict) -> Dict:
        """
        处理异常
        
        处理策略:
        - P0: 立即太一介入
        - P1: 15 分钟内太一协调
        - P2: 自动处理
        """
        severity = anomaly.get("severity", "P2")
        anomaly_type = anomaly.get("type")
        
        result = {
            "anomaly": anomaly,
            "handled": False,
            "action_taken": None,
            "timestamp": datetime.now().isoformat()
        }
        
        if severity == "P0":
            # 立即介入
            result["action_taken"] = "taiyi_immediate_intervention"
            result["handled"] = True
            self._notify_taiyi(anomaly, urgent=True)
        
        elif severity == "P1":
            # 15 分钟内协调
            result["action_taken"] = "taiyi_coordination_scheduled"
            result["handled"] = True
            self._notify_taiyi(anomaly, urgent=False)
        
        elif severity == "P2":
            # 自动处理
            if anomaly_type == "no_confirmation":
                result["action_taken"] = "auto_reminder_sent"
                result["handled"] = True
                self._send_auto_reminder(anomaly)
        
        # 记录日志
        self.correction_log.append(result)
        self._save_log()
        
        return result
    
    def _notify_taiyi(self, anomaly: Dict, urgent: bool = False):
        """通知太一"""
        alert_file = self.agents_dir / "taiyi" / "inbox" / f"ALERT-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        
        urgency = "🔴 紧急" if urgent else "🟡 注意"
        content = f"""# {urgency} 纠偏告警

**类型**: {anomaly['type']}
**Bot**: {anomaly['bot']}
**任务**: {anomaly['task_id']}
**发现时间**: {anomaly['detected_at']}
**严重级别**: {anomaly['severity']}

---

## 建议处理

{self._get_suggested_action(anomaly)}

---

*Correction Mechanism v1.0 | 太一 AGI*
"""
        alert_file.parent.mkdir(parents=True, exist_ok=True)
        alert_file.write_text(content, encoding='utf-8')
    
    def _get_suggested_action(self, anomaly: Dict) -> str:
        """获取建议处理动作"""
        actions = {
            "no_confirmation": "1. 检查 Bot 是否在线\n2. 重新分发任务\n3. 调整任务分配",
            "blocked": "1. 了解阻塞原因\n2. 协调资源解决\n3. 必要时重新分配",
            "overdue": "1. 评估剩余工作量\n2. 调整截止时间或增援\n3. 记录经验教训"
        }
        return actions.get(anomaly['type'], "1. 调查原因\n2. 制定解决方案\n3. 执行并跟踪")
    
    def _send_auto_reminder(self, anomaly: Dict):
        """发送自动提醒"""
        bot = anomaly['bot']
        reminder_file = self.agents_dir / bot / "inbox" / f"REMINDER-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        
        content = f"""# ⏰ 任务确认提醒

**任务**: {anomaly['task_id']}
**分发时间**: 约{anomaly['elapsed_minutes']:.0f}分钟前

---

请确认是否收到任务委派单，如未收到请@太一！

---

*自动提醒 | Task Orchestrator v1.0*
"""
        reminder_file.parent.mkdir(parents=True, exist_ok=True)
        reminder_file.write_text(content, encoding='utf-8')
    
    def generate_correction_report(self) -> str:
        """生成纠偏报告"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        report_file = WORKSPACE / "reports" / f"correction-report-{timestamp}.md"
        
        anomalies = self.detect_anomalies()
        
        content = f"""# 纠偏机制报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')} | **Correction Mechanism v1.0**

---

## 📊 异常检测

**当前异常数**: {len(anomalies)}

| 严重级别 | 数量 | 处理状态 |
|---------|------|---------|
"""
        
        by_severity = {}
        for a in anomalies:
            sev = a.get('severity', 'P2')
            by_severity[sev] = by_severity.get(sev, 0) + 1
        
        for sev in ['P0', 'P1', 'P2']:
            count = by_severity.get(sev, 0)
            content += f"| {sev} | {count} | {'🟡 待处理' if count > 0 else '✅'} |\n"
        
        content += f"""
---

## 📋 历史纠偏记录

**总记录数**: {len(self.correction_log)}

"""
        
        if self.correction_log:
            content += "| 时间 | 类型 | Bot | 处理动作 |\n|------|------|-----|----------|\n"
            for record in self.correction_log[-10:]:  # 最近 10 条
                a = record['anomaly']
                content += f"| {record['timestamp'][:16]} | {a['type']} | {a['bot']} | {record['action_taken']} |\n"
        else:
            content += "*暂无纠偏记录*\n"
        
        content += f"""
---

*Correction Mechanism v1.0 | 太一 AGI*
"""
        
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(content, encoding='utf-8')
        
        return str(report_file)


def main():
    """主函数"""
    import sys
    
    correction = CorrectionMechanism()
    
    if len(sys.argv) < 2:
        command = "detect"
    else:
        command = sys.argv[1]
    
    if command == "detect":
        anomalies = correction.detect_anomalies()
        if anomalies:
            print(f"⚠️ 发现 {len(anomalies)} 个异常:")
            for a in anomalies:
                severity_emoji = {"P0": "🔴", "P1": "🟡", "P2": "🔵"}.get(a['severity'], "⚪")
                print(f"  {severity_emoji} [{a['severity']}] {a['type']} - {a['bot']}/{a['task_id']}")
        else:
            print("✅ 无异常")
    
    elif command == "handle":
        anomalies = correction.detect_anomalies()
        for a in anomalies:
            result = correction.handle_anomaly(a)
            print(f"{'✅' if result['handled'] else '⏳'} 处理 {a['type']}: {a['action_taken']}")
        if not anomalies:
            print("✅ 无需处理")
    
    elif command == "report":
        report = correction.generate_correction_report()
        print(f"✅ 纠偏报告已生成：{report}")
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
