#!/usr/bin/env python3
"""
Honest Boundary - 诚实边界检查

灵感：女娲 Skill
作者：太一 AGI
创建：2026-04-09
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# 预定义能力限制
CAPABILITY_LIMITS = {
    "real_time_data": "无法访问实时数据 (除非调用 API)",
    "physical_tasks": "无法执行需要物理交互的任务",
    "future_prediction": "无法准确预测未来事件",
    "private_data": "无法访问私有数据库",
    "paid_content": "无法访问付费内容"
}

# 需要人工介入的场景
HUMAN_INTERVENTION = {
    "financial_transfer": "涉及资金转账的决策",
    "legal_advice": "法律建议",
    "medical_advice": "医疗建议",
    "creative_final": "创造性工作最终审核"
}


@dataclass
class BoundaryCheck:
    """边界检查结果"""
    can_handle: bool
    reason: str
    suggestion: Optional[str]
    confidence: float
    requires_human: bool


class BoundaryChecker:
    """边界检查器"""
    
    def __init__(self, bot_id: str):
        self.bot_id = bot_id
        self.knowledge_cutoff = datetime.now().strftime("%Y-%m-%d")
    
    def can_handle(self, task: str) -> BoundaryCheck:
        """
        检查任务是否在能力范围内
        
        Args:
            task: 任务描述
        
        Returns:
            BoundaryCheck: 检查结果
        """
        task_lower = task.lower()
        
        # 检查能力限制
        for limit_key, limit_desc in CAPABILITY_LIMITS.items():
            if limit_key in task_lower:
                return BoundaryCheck(
                    can_handle=False,
                    reason=limit_desc,
                    suggestion="建议使用专用工具或 API",
                    confidence=0.95,
                    requires_human=False
                )
        
        # 检查需要人工介入的场景
        for intervention_key, intervention_desc in HUMAN_INTERVENTION.items():
            if intervention_key in task_lower:
                return BoundaryCheck(
                    can_handle=False,
                    reason=intervention_desc,
                    suggestion="需要人工审核和确认",
                    confidence=0.99,
                    requires_human=True
                )
        
        # 默认可以处理
        return BoundaryCheck(
            can_handle=True,
            reason="在能力范围内",
            suggestion=None,
            confidence=0.8,
            requires_human=False
        )
    
    def express_uncertainty(self, confidence: float, context: str = "") -> Dict:
        """
        表达不确定性
        
        Args:
            confidence: 置信度 (0-1)
            context: 上下文
        
        Returns:
            不确定性表达
        """
        if confidence >= 0.9:
            level = "高"
            phrase = "可以确定"
        elif confidence >= 0.7:
            level = "中"
            phrase = "较大概率"
        elif confidence >= 0.5:
            level = "低"
            phrase = "可能"
        else:
            level = "极低"
            phrase = "不确定"
        
        return {
            "confidence": confidence,
            "level": level,
            "phrase": phrase,
            "disclaimer": f"此回答置信度{level}，{context}" if context else "",
            "alternatives": self._get_alternatives(confidence)
        }
    
    def _get_alternatives(self, confidence: float) -> List[str]:
        """获取替代建议"""
        if confidence < 0.5:
            return [
                "建议咨询专业人士",
                "需要更多信息才能准确判断",
                "此问题存在多种可能性"
            ]
        elif confidence < 0.7:
            return [
                "建议结合其他信息源验证",
                "此回答仅供参考"
            ]
        else:
            return []
    
    def generate_boundary_section(self) -> str:
        """生成边界声明 section"""
        section = """## ⚠️ 能力限制

**做不到的事**:
"""
        for key, desc in CAPABILITY_LIMITS.items():
            section += f"- ❌ {desc}\n"
        
        section += "\n**需要人工介入**:\n"
        for key, desc in HUMAN_INTERVENTION.items():
            section += f"- 🟡 {desc}\n"
        
        section += f"\n**信息获取限制**:\n"
        section += f"- 🔒 知识截止：{self.knowledge_cutoff}\n"
        
        return section


def main():
    """测试"""
    checker = BoundaryChecker("taiyi")
    
    print("🎯 诚实边界检查器测试")
    print()
    
    # 测试任务检查
    tasks = [
        "预测明天股价",
        "执行银行转账",
        "分析当前市场趋势",
        "提供医疗建议"
    ]
    
    for task in tasks:
        result = checker.can_handle(task)
        status = "✅" if result.can_handle else "❌"
        print(f"{status} {task}: {result.reason}")
    
    print()
    
    # 测试不确定性表达
    print("不确定性表达测试:")
    for conf in [0.95, 0.75, 0.55, 0.35]:
        expr = checker.express_uncertainty(conf, "市场预测")
        print(f"  置信度{conf:.2f}: {expr['phrase']} ({expr['level']})")


if __name__ == "__main__":
    main()
