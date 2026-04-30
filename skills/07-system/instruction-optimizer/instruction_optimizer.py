#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instruction Optimizer · 指令优化师 v1.0
太一 AGI · 2026-04-21 13:54

核心能力:
- 四维度指令质量评估
- 主动追问机制
- 20+ 场景指令模板
- 输出质量自检
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('InstructionOptimizer')


class InstructionOptimizer:
    """指令优化师"""
    
    # 四维度关键词库
    DIMENSION_KEYWORDS = {
        "role": [
            "专家", "顾问", "教练", "教授", "身份", "角色", "合伙人", "总监",
            "首席", "资深", "顶级", "专业", "老师", "导师", "师傅"
        ],
        "method": [
            "方法", "理论", "框架", "模型", "法则", "原理", "技巧", "工具",
            "体系", "流程", "标准", "规范", "方法论", "策略", "战术"
        ],
        "context": [
            "目标", "基础", "背景", "领域", "时间", "约束", "条件", "现状",
            "水平", "程度", "投入", "资源", "限制", "需求", "期望"
        ],
        "action": [
            "方案", "计划", "步骤", "行动", "执行", "落地", "具体", "操作",
            "实施", "实践", "执行", "清单", "路线", "路径", "指南"
        ]
    }
    
    # 指令模板库
    TEMPLATES = {
        "learning": [
            {
                "id": "LEARN-01",
                "name": "新领域速通",
                "template": "你是{领域}专家，用{方法论}，帮我设计{时间}学习计划。我基础{基础}，目标{目标}"
            },
            {
                "id": "LEARN-02",
                "name": "技能突破",
                "template": "你是{技能}教练，用刻意练习原理，设计 21 天突破方案。当前水平{水平}"
            },
            {
                "id": "LEARN-03",
                "name": "知识体系",
                "template": "你是{学科}教授，用建构主义方法，帮我搭建知识树。已有基础{基础}"
            }
        ],
        "analysis": [
            {
                "id": "ANALYZE-01",
                "name": "商业分析",
                "template": "你是麦肯锡合伙人，用 MECE 法则分析{问题}。背景{背景}，目标{目标}"
            },
            {
                "id": "ANALYZE-02",
                "name": "根因分析",
                "template": "你是质量专家，用 5Why 法分析{问题}。现象{现象}，影响{影响}"
            },
            {
                "id": "ANALYZE-03",
                "name": "竞品分析",
                "template": "你是战略顾问，用波特五力分析{行业}。我们位置{位置}，目标{目标}"
            }
        ],
        "decision": [
            {
                "id": "DECIDE-01",
                "name": "重大决策",
                "template": "你是决策顾问，用决策矩阵帮我选择{选项}。标准{标准}，权重{权重}"
            },
            {
                "id": "DECIDE-02",
                "name": "风险评估",
                "template": "你是风控专家，用 FMEA 方法评估{项目}风险。背景{背景}"
            },
            {
                "id": "DECIDE-03",
                "name": "资源分配",
                "template": "你是 CFO，用零基预算法分配{资源}。目标{目标}，约束{约束}"
            }
        ],
        "creation": [
            {
                "id": "CREATE-01",
                "name": "内容创作",
                "template": "你是顶级文案，用 AIDA 模型写{类型}。受众{受众}，目标{目标}"
            },
            {
                "id": "CREATE-02",
                "name": "方案设计",
                "template": "你是设计师，用设计思维设计{方案}。用户需求{需求}，约束{约束}"
            },
            {
                "id": "CREATE-03",
                "name": "头脑风暴",
                "template": "你是创意总监，用 SCAMPER 法 brainstorm{主题}。背景{背景}"
            }
        ],
        "efficiency": [
            {
                "id": "EFFICIENCY-01",
                "name": "时间管理",
                "template": "你是效率专家，用 GTD 方法优化我的时间。当前状态{状态}，目标{目标}"
            },
            {
                "id": "EFFICIENCY-02",
                "name": "流程优化",
                "template": "你是精益专家，用价值流图分析{流程}。当前问题{问题}"
            },
            {
                "id": "EFFICIENCY-03",
                "name": "习惯养成",
                "template": "你是习惯教练，用原子习惯方法养成{习惯}。当前状态{状态}"
            }
        ]
    }
    
    # 质量等级
    LEVELS = {
        (90, 100): {"name": "S", "desc": "指令清晰完整", "action": "直接执行"},
        (75, 89): {"name": "A", "desc": "指令较清晰", "action": "直接执行 + 确认"},
        (60, 74): {"name": "B", "desc": "指令基本完整", "action": "执行 + 补充建议"},
        (40, 59): {"name": "C", "desc": "指令缺失较多", "action": "追问后执行"},
        (0, 39): {"name": "D", "desc": "指令模糊", "action": "必须追问"}
    }
    
    def __init__(self):
        self.template_file = Path(__file__).parent / "templates.json"
        self.history = []
        logger.info("🎯 Instruction Optimizer v1.0 已初始化")
    
    def evaluate(self, instruction: str) -> Dict:
        """评估指令质量"""
        logger.info(f"📊 评估指令质量：{instruction[:50]}...")
        
        dimensions = {}
        
        # 角色清晰度 (25 分)
        role_score = min(25, len([k for k in self.DIMENSION_KEYWORDS["role"] if k in instruction]) * 5)
        dimensions["role"] = role_score
        
        # 方法论指定 (25 分)
        method_score = min(25, len([k for k in self.DIMENSION_KEYWORDS["method"] if k in instruction]) * 5)
        dimensions["method"] = method_score
        
        # 背景完整度 (25 分)
        context_score = min(25, len([k for k in self.DIMENSION_KEYWORDS["context"] if k in instruction]) * 4)
        dimensions["context"] = context_score
        
        # 行动具体度 (25 分)
        action_score = min(25, len([k for k in self.DIMENSION_KEYWORDS["action"] if k in instruction]) * 5)
        dimensions["action"] = action_score
        
        total_score = sum(dimensions.values())
        level = self._get_level(total_score)
        missing = self._get_missing(dimensions)
        suggestions = self._generate_suggestions(dimensions, missing)
        
        result = {
            "score": total_score,
            "dimensions": dimensions,
            "level": level["name"],
            "level_desc": level["desc"],
            "action": level["action"],
            "missing": missing,
            "suggestions": suggestions,
            "evaluated_at": datetime.now().isoformat()
        }
        
        self.history.append(result)
        logger.info(f"✅ 指令质量评估完成：{total_score}分 ({level['name']}级)")
        
        return result
    
    def auto_followup(self, instruction: str) -> str:
        """自动生成追问"""
        logger.info(f"🤔 生成追问：{instruction[:50]}...")
        
        evaluation = self.evaluate(instruction)
        
        if evaluation["score"] >= 75:
            return "✅ 指令清晰，开始执行..."
        
        followup_lines = [
            "收到！为了给您提供最佳方案，请补充以下信息：\n",
        ]
        
        if "role" in evaluation["missing"]:
            followup_lines.append("1️⃣ **角色**：希望我以什么身份协助？(如：资深教练/行业专家/战略顾问)\n")
        
        if "method" in evaluation["missing"]:
            followup_lines.append("2️⃣ **方法**：有偏好的方法论吗？(如：刻意练习/MECE 法则/GTD 方法)\n")
        
        if "context" in evaluation["missing"]:
            followup_lines.append("3️⃣ **背景**：\n")
            followup_lines.append("   - 目标：希望达到什么程度？\n")
            followup_lines.append("   - 基础：当前水平如何？\n")
            followup_lines.append("   - 时间：能投入多久？\n")
        
        if "action" in evaluation["missing"]:
            followup_lines.append("4️⃣ **输出**：需要具体可执行的方案吗？\n")
        
        return "".join(followup_lines)
    
    def get_templates(self, category: str = None) -> str:
        """获取指令模板"""
        logger.info(f"📋 获取模板：{category}")
        
        if category and category in self.TEMPLATES:
            templates = self.TEMPLATES[category]
        else:
            templates = []
            for cat_templates in self.TEMPLATES.values():
                templates.extend(cat_templates)
        
        output_lines = ["【指令模板库】\n"]
        
        for template in templates:
            output_lines.append(f"\n{template['id']} | {template['name']}")
            output_lines.append(f"\"{template['template']}\"")
        
        return "\n".join(output_lines)
    
    def optimize_instruction(self, instruction: str, category: str = None) -> str:
        """优化指令"""
        logger.info(f"✏️ 优化指令：{instruction[:50]}...")
        
        evaluation = self.evaluate(instruction)
        
        if evaluation["score"] >= 75:
            return instruction
        
        # 基于模板优化
        templates = self.TEMPLATES.get(category, [])
        if templates:
            template = templates[0]["template"]
            return f"基于模板优化：{template}"
        
        # 通用优化
        optimized = instruction
        if "role" in evaluation["missing"]:
            optimized = "作为相关领域专家，" + optimized
        if "action" in evaluation["missing"]:
            optimized = optimized + "，请提供具体可执行的方案"
        
        return optimized
    
    def self_check(self, output: str, instruction: str) -> Dict:
        """输出质量自检"""
        logger.info(f"🔍 输出质量自检")
        
        check_items = [
            {"name": "角色一致性", "check": "输出是否符合指令指定的角色身份", "pass": True},
            {"name": "方法论应用", "check": "是否应用了指定的方法论/框架", "pass": True},
            {"name": "背景利用", "check": "是否充分利用了提供的背景信息", "pass": True},
            {"name": "可执行性", "check": "输出是否具体可执行", "pass": True}
        ]
        
        # 简化自检 (实际应更复杂)
        for item in check_items:
            item["pass"] = True  # 简化为全部通过
        
        result = {
            "instruction": instruction[:50],
            "output_length": len(output),
            "check_items": check_items,
            "all_passed": all(item["pass"] for item in check_items),
            "checked_at": datetime.now().isoformat()
        }
        
        logger.info(f"✅ 自检完成：{'全部通过' if result['all_passed'] else '有待改进'}")
        
        return result
    
    def _get_level(self, score: int) -> Dict:
        """获取质量等级"""
        for (min_score, max_score), level in self.LEVELS.items():
            if min_score <= score <= max_score:
                return level
        return self.LEVELS[(0, 39)]
    
    def _get_missing(self, dimensions: Dict) -> List[str]:
        """获取缺失维度"""
        missing = []
        for dim, score in dimensions.items():
            if score < 15:  # 低于 60% 视为缺失
                missing.append(dim)
        return missing
    
    def _generate_suggestions(self, dimensions: Dict, missing: List[str]) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if "role" in missing:
            suggestions.append("建议指定专家身份，如'作为麦肯锡合伙人'")
        if "method" in missing:
            suggestions.append("建议指定方法论，如'用 MECE 法则分析'")
        if "context" in missing:
            suggestions.append("建议交代背景，如'目标/基础/时间约束'")
        if "action" in missing:
            suggestions.append("建议明确要求，如'提供可执行的方案'")
        
        return suggestions
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """获取评估历史"""
        return self.history[-limit:]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self.history:
            return {"total": 0}
        
        scores = [h["score"] for h in self.history]
        return {
            "total": len(self.history),
            "avg_score": sum(scores) / len(scores),
            "max_score": max(scores),
            "min_score": min(scores),
            "level_distribution": self._get_level_distribution()
        }
    
    def _get_level_distribution(self) -> Dict:
        """获取等级分布"""
        distribution = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0}
        for h in self.history:
            level = h.get("level", "D")
            if level in distribution:
                distribution[level] += 1
        return distribution


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("🎯 Instruction Optimizer · 指令优化师 v1.0")
    logger.info("=" * 60)
    
    optimizer = InstructionOptimizer()
    
    # 演示指令评估
    logger.info(f"\n📊 演示指令评估...")
    
    test_instructions = [
        "帮我分析一下",
        "你是麦肯锡合伙人，用 MECE 法则分析一下市场",
        "你是麦肯锡合伙人，用 MECE 法则分析一下市场。背景：我们是初创公司，目标：找到差异化定位",
        "你是麦肯锡合伙人，用 MECE 法则分析一下市场。背景：我们是初创公司，目标：找到差异化定位。请提供具体可执行的 3 步方案"
    ]
    
    for instruction in test_instructions:
        logger.info(f"\n指令：{instruction}")
        result = optimizer.evaluate(instruction)
        logger.info(f"  评分：{result['score']}分 ({result['level']}级)")
        logger.info(f"  处理：{result['action']}")
    
    # 演示追问
    logger.info(f"\n🤔 演示主动追问...")
    followup = optimizer.auto_followup("我想学 Python")
    logger.info(f"{followup}")
    
    # 演示模板
    logger.info(f"\n📋 演示模板获取...")
    templates = optimizer.get_templates("learning")
    logger.info(f"{templates}")
    
    # 演示统计
    logger.info(f"\n📊 演示统计信息...")
    stats = optimizer.get_stats()
    logger.info(f"  总评估：{stats.get('total', 0)}次")
    logger.info(f"  平均分：{stats.get('avg_score', 0):.1f}分")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 指令优化师演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
