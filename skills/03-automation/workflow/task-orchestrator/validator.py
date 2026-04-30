#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validator - 成果验收器
验证 Bot 交付成果是否符合验收标准
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WORKSPACE = Path.home() / ".openclaw" / "workspace"
AGENTS_DIR = Path.home() / ".openclaw" / "agents"

class TaskValidator:
    """成果验收器"""
    
    def __init__(self):
        self.workspace = WORKSPACE
        self.agents_dir = AGENTS_DIR
    
    def validate(self, bot: str, task_id: str) -> Dict:
        """
        验收任务成果
        
        Args:
            bot: Bot 名称
            task_id: 任务 ID
            
        Returns:
            验收报告
        """
        outbox_dir = self.agents_dir / bot / "outbox"
        
        # 查找验收报告
        report_file = None
        for f in outbox_dir.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            if task_id in content:
                report_file = f
                break
        
        if not report_file:
            return {
                "task_id": task_id,
                "bot": bot,
                "status": "not_found",
                "message": "未找到交付报告"
            }
        
        content = report_file.read_text(encoding='utf-8')
        
        # 验收检查
        checks = {
            "completeness": self._check_completeness(content),
            "timeliness": self._check_timeliness(report_file),
            "documentation": self._check_documentation(content),
            "quality": self._check_quality(content)
        }
        
        # 计算总分
        score = sum(checks.values()) / len(checks)
        
        result = {
            "task_id": task_id,
            "bot": bot,
            "status": "passed" if score >= 0.8 else "needs_improvement" if score >= 0.5 else "failed",
            "score": score,
            "checks": checks,
            "report_file": str(report_file),
            "validated_at": datetime.now().isoformat()
        }
        
        return result
    
    def _check_completeness(self, content: str) -> bool:
        """检查完整性"""
        # 检查是否包含必要部分
        required = ["任务", "状态", "产出"]
        return all(kw in content for kw in required)
    
    def _check_timeliness(self, report_file: Path) -> bool:
        """检查时效性"""
        # 简化：假设在 24 小时内完成
        created = datetime.fromtimestamp(report_file.stat().st_mtime)
        elapsed = (datetime.now() - created).seconds / 3600
        return elapsed < 24
    
    def _check_documentation(self, content: str) -> bool:
        """检查文档化"""
        # 检查是否有文件列表或代码块
        has_files = "文件" in content or "产出" in content
        has_code = "```" in content
        return has_files or has_code
    
    def _check_quality(self, content: str) -> bool:
        """检查质量"""
        # 简化：检查是否有完成标记
        return "✅" in content or "完成" in content
    
    def generate_validation_report(self, validation_result: Dict) -> str:
        """生成验收报告"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        report_file = WORKSPACE / "reports" / f"validation-{validation_result['task_id']}-{timestamp}.md"
        
        status_emoji = {"passed": "✅", "needs_improvement": "🟡", "failed": "🔴", "not_found": "⚪"}.get(validation_result['status'], "⚪")
        
        content = f"""# 任务验收报告

> **验收时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')} | **Validator v1.0**

---

## 📋 任务信息

| 项目 | 内容 |
|------|------|
| **任务 ID** | {validation_result['task_id']} |
| **负责 Bot** | {validation_result['bot']} |
| **验收状态** | {status_emoji} {validation_result['status']} |
| **得分** | {validation_result.get('score', 0):.1%} |

---

## ✅ 验收检查

| 检查项 | 结果 |
|--------|------|
| 完整性 | {'✅' if validation_result.get('checks', {}).get('completeness') else '❌'} |
| 时效性 | {'✅' if validation_result.get('checks', {}).get('timeliness') else '❌'} |
| 文档化 | {'✅' if validation_result.get('checks', {}).get('documentation') else '❌'} |
| 质量 | {'✅' if validation_result.get('checks', {}).get('quality') else '❌'} |

---

## 📁 交付物

**报告位置**: `{validation_result.get('report_file', 'N/A')}`

---

## 🎯 建议

{self._get_suggestions(validation_result)}

---

*Validator v1.0 | 太一 AGI*
"""
        
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(content, encoding='utf-8')
        
        return str(report_file)
    
    def _get_suggestions(self, result: Dict) -> str:
        """获取建议"""
        if result['status'] == 'passed':
            return "✅ 验收通过，无需改进"
        elif result['status'] == 'needs_improvement':
            return "🟡 建议补充文档或优化质量"
        else:
            return "🔴 需要返工或重新交付"


def main():
    """主函数"""
    import sys
    
    validator = TaskValidator()
    
    if len(sys.argv) < 3:
        print("用法：python3 validator.py validate <bot> <task_id>")
        print("      python3 validator.py report <bot> <task_id>")
        sys.exit(1)
    
    command = sys.argv[1]
    bot = sys.argv[2]
    task_id = sys.argv[3] if len(sys.argv) > 3 else "TASK-DEMO"
    
    if command == "validate":
        result = validator.validate(bot, task_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "report":
        result = validator.validate(bot, task_id)
        report = validator.generate_validation_report(result)
        print(f"✅ 验收报告已生成：{report}")
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
