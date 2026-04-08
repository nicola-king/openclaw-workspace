#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一美学评分系统 - 原型实现

功能:
- 图片美学评分 (6 维度)
- 改进建议生成
- 评分报告输出

创建：2026-04-06 10:23
依据：constitution/directives/AESTHETIC-PERCEPTION.md
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class AestheticScorer:
    """美学评分器 - 原型版"""
    
    def __init__(self):
        """初始化评分器"""
        self.dimensions = [
            'color',      # 色彩
            'composition', # 构图
            'style',      # 风格
            'culture',    # 文化
            'emotion',    # 情感
            'originality' # 原创
        ]
        
        self.weights = {
            'color': 0.20,
            'composition': 0.20,
            'style': 0.15,
            'culture': 0.15,
            'emotion': 0.20,
            'originality': 0.10
        }
    
    def evaluate(self, image_path: str, manual_scores: Dict = None) -> Dict:
        """
        评估图片美学
        
        Args:
            image_path: 图片路径
            manual_scores: 手动评分 (原型阶段使用)
            
        Returns:
            {
                'overall': float,
                'color': float,
                'composition': float,
                'style': float,
                'culture': float,
                'emotion': float,
                'originality': float,
                'suggestions': List[str],
                'level': str
            }
        """
        # 原型阶段：使用手动评分
        if manual_scores:
            scores = manual_scores
        else:
            # TODO: 集成 AI 模型自动评分
            scores = self._auto_evaluate(image_path)
        
        # 计算加权总分
        overall = sum(
            scores[dim] * self.weights[dim]
            for dim in self.dimensions
        )
        
        # 生成改进建议
        suggestions = self._generate_suggestions(scores)
        
        # 确定等级
        level = self._get_level(overall)
        
        return {
            'overall': round(overall, 1),
            'color': scores['color'],
            'composition': scores['composition'],
            'style': scores['style'],
            'culture': scores['culture'],
            'emotion': scores['emotion'],
            'originality': scores['originality'],
            'suggestions': suggestions,
            'level': level,
            'timestamp': datetime.now().isoformat()
        }
    
    def _auto_evaluate(self, image_path: str) -> Dict:
        """
        自动评分 (待实现)
        
        TODO: 集成以下模型:
        - 色彩分析：OpenCV + 色彩理论
        - 构图分析：深度学习 ( saliency detection)
        - 风格识别：CNN 分类器 (100+ 风格)
        - 文化符号：知识图谱查询
        - 情感分析：多模态模型
        - 原创性：与数据库对比
        """
        # 临时返回默认分数
        return {
            'color': 5,
            'composition': 5,
            'style': 5,
            'culture': 5,
            'emotion': 5,
            'originality': 5
        }
    
    def _generate_suggestions(self, scores: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 找出低分维度
        weak_dims = [
            (dim, score) for dim, score in scores.items()
            if score < 6
        ]
        
        # 按分数排序
        weak_dims.sort(key=lambda x: x[1])
        
        # 生成建议
        suggestion_templates = {
            'color': [
                "调整配色方案，尝试互补色或类似色",
                "降低/提高饱和度以增强视觉冲击",
                "注意色彩情感与主题匹配"
            ],
            'composition': [
                "使用三分法重新构图",
                "增加画面层次感 (前景/中景/背景)",
                "强化视觉焦点，减少干扰元素"
            ],
            'style': [
                "统一风格元素，避免混搭冲突",
                "强化风格特征 (如赛博朋克的霓虹灯)",
                "参考同类风格优秀作品"
            ],
            'culture': [
                "深化文化符号理解，避免浅层使用",
                "研究符号的历史/情感含义",
                "注意文化背景的准确性"
            ],
            'emotion': [
                "增强情感叙事，让画面讲故事",
                "使用色彩/构图传达特定情绪",
                "添加能引发共鸣的元素"
            ],
            'originality': [
                "尝试新颖的元素组合",
                "避免模板化，加入个人风格",
                "从不同领域汲取灵感"
            ]
        }
        
        # 为每个弱项生成 1-2 条建议
        for dim, score in weak_dims[:3]:  # 最多 3 个弱项
            if dim in suggestion_templates:
                suggestions.append(suggestion_templates[dim][0])
                if score < 4:
                    suggestions.append(suggestion_templates[dim][1])
        
        return suggestions
    
    def _get_level(self, score: float) -> str:
        """根据分数确定等级"""
        if score >= 9:
            return "杰作 (Masterpiece)"
        elif score >= 7:
            return "优秀 (Excellent)"
        elif score >= 5:
            return "良好 (Good)"
        elif score >= 3:
            return "一般 (Fair)"
        else:
            return "较差 (Poor)"
    
    def generate_report(self, scores: Dict, output_path: str = None) -> str:
        """
        生成评分报告
        
        Args:
            scores: evaluate() 返回的评分字典
            output_path: 输出文件路径 (可选)
            
        Returns:
            Markdown 格式报告
        """
        report = f"""# 🎨 美学评分报告

**评分时间**: {scores['timestamp']}  
**整体评分**: **{scores['overall']}/10** ⭐⭐⭐⭐

---

## 📊 维度分析

| 维度 | 评分 | 权重 | 加权分 |
|------|------|------|--------|
| 色彩 | {scores['color']}/10 | 20% | {scores['color'] * 0.20:.1f} |
| 构图 | {scores['composition']}/10 | 20% | {scores['composition'] * 0.20:.1f} |
| 风格 | {scores['style']}/10 | 15% | {scores['style'] * 0.15:.1f} |
| 文化 | {scores['culture']}/10 | 15% | {scores['culture'] * 0.15:.1f} |
| 情感 | {scores['emotion']}/10 | 20% | {scores['emotion'] * 0.20:.1f} |
| 原创 | {scores['originality']}/10 | 10% | {scores['originality'] * 0.10:.1f} |

---

## 🏆 等级：**{scores['level']}**

---

## 💡 改进建议

"""
        for i, suggestion in enumerate(scores['suggestions'], 1):
            report += f"{i}. {suggestion}\n"
        
        if not scores['suggestions']:
            report += "✨ 各方面表现均衡，无需特别改进\n"
        
        report += f"\n---\n\n*报告生成：太一 AGI 美学评分系统 v1.0*\n"
        
        # 保存到文件
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 报告已保存：{output_path}")
        
        return report


def main():
    """测试评分器"""
    scorer = AestheticScorer()
    
    # 测试用例：重庆涂鸦
    test_scores = {
        'color': 8,
        'composition': 7,
        'style': 8,
        'culture': 7,
        'emotion': 7,
        'originality': 8
    }
    
    result = scorer.evaluate("./graffiti.jpg", manual_scores=test_scores)
    
    print("\n" + "="*50)
    print("🎨 太一美学评分系统 - 测试结果")
    print("="*50)
    print(f"整体评分：{result['overall']}/10 - {result['level']}")
    print("\n维度分析:")
    for dim in scorer.dimensions:
        print(f"  {dim}: {result[dim]}/10")
    print("\n改进建议:")
    for i, suggestion in enumerate(result['suggestions'], 1):
        print(f"  {i}. {suggestion}")
    print("="*50)
    
    # 生成报告
    report = scorer.generate_report(result, "./reports/aesthetic-test-report.md")
    print(f"\n📄 完整报告：./reports/aesthetic-test-report.md")


if __name__ == '__main__':
    main()
