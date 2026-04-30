#!/usr/bin/env python3
"""
Mind Model Extractor - 心智模型提取

灵感：女娲 Skill
作者：太一 AGI
创建：2026-04-09
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
USER_MODEL_FILE = WORKSPACE / "memory/user-model.json"

# 预定义心智模型库
MIND_MODEL_LIBRARY = {
    "第一性原理": {
        "keywords": ["物理极限", "基本原理", "抛开", "最优解", "本质"],
        "description": "从基本原理推导，不依赖类比"
    },
    "逆向思维": {
        "keywords": ["反过来", "逆向", "如果...会怎样", "反面"],
        "description": "从对立面思考问题"
    },
    "二阶思维": {
        "keywords": ["然后呢", "接下来", "长期影响", "连锁反应"],
        "description": "考虑后果的后果"
    },
    "概率思维": {
        "keywords": ["概率", "期望值", "胜率", "风险收益比"],
        "description": "用概率和期望值做决策"
    },
    "机会成本": {
        "keywords": ["代价", "放弃", " alternative", "其他选择"],
        "description": "考虑放弃的选项价值"
    },
    "复利思维": {
        "keywords": ["复利", "积累", "长期", "滚雪球"],
        "description": "选择有复利效应的赛道"
    },
    "能力圈": {
        "keywords": ["懂", "不懂", "能力范围", "边界"],
        "description": "只做自己理解的事"
    },
    "边际思维": {
        "keywords": ["边际", "额外", "增量"],
        "description": "考虑边际成本和边际收益"
    }
}


@dataclass
class MindModel:
    """心智模型"""
    name: str
    description: str
    examples: List[str]
    frequency: float
    confidence: float


@dataclass
class DecisionHeuristic:
    """决策启发式"""
    name: str
    rule: str
    examples: List[str]
    confidence: float


@dataclass
class ExpressionDNA:
    """表达 DNA"""
    style: str
    avg_length: float
    common_phrases: List[str]
    tone: str
    emoji_usage: Dict[str, int]


class MindModelExtractor:
    """心智模型提取器"""
    
    def __init__(self):
        self.models = []
        self.heuristics = []
        self.dna = None
    
    def extract_mind_models(self, conversations: List[Dict]) -> List[MindModel]:
        """
        从对话中提取心智模型
        
        Args:
            conversations: 对话历史
        
        Returns:
            心智模型列表
        """
        model_counts = {name: 0 for name in MIND_MODEL_LIBRARY.keys()}
        model_examples = {name: [] for name in MIND_MODEL_LIBRARY.keys()}
        
        # 扫描对话
        for conv in conversations:
            user_message = conv.get("user", "")
            
            # 匹配心智模型
            for model_name, model_info in MIND_MODEL_LIBRARY.items():
                if any(kw in user_message for kw in model_info["keywords"]):
                    model_counts[model_name] += 1
                    if len(model_examples[model_name]) < 3:
                        model_examples[model_name].append(user_message[:100])
        
        # 转换为 MindModel 对象
        total = sum(model_counts.values()) or 1
        for model_name, count in model_counts.items():
            if count >= 2:  # 至少出现 2 次
                self.models.append(MindModel(
                    name=model_name,
                    description=MIND_MODEL_LIBRARY[model_name]["description"],
                    examples=model_examples[model_name],
                    frequency=count / total,
                    confidence=min(0.5 + count * 0.1, 0.95)
                ))
        
        # 按频率排序
        self.models.sort(key=lambda m: m.frequency, reverse=True)
        
        return self.models
    
    def extract_heuristics(self, decisions: List[Dict]) -> List[DecisionHeuristic]:
        """
        从决策历史中提取启发式
        
        Args:
            decisions: 决策历史
        
        Returns:
            决策启发式列表
        """
        # 简化实现：识别常见决策模式
        patterns = {
            "成本优先": ["便宜", "成本", "预算", "省钱"],
            "质量优先": ["质量", "稳定", "可靠", "最好"],
            "速度优先": ["快", "立即", "马上", "尽快"],
            "风险规避": ["风险", "安全", "稳妥", "保守"]
        }
        
        heuristic_counts = {name: 0 for name in patterns.keys()}
        heuristic_examples = {name: [] for name in patterns.keys()}
        
        for decision in decisions:
            text = decision.get("text", "") + " " + decision.get("reason", "")
            
            for name, keywords in patterns.items():
                if any(kw in text for kw in keywords):
                    heuristic_counts[name] += 1
                    if len(heuristic_examples[name]) < 3:
                        heuristic_examples[name].append(text[:100])
        
        # 转换为对象
        total = sum(heuristic_counts.values()) or 1
        for name, count in heuristic_counts.items():
            if count >= 2:
                self.heuristics.append(DecisionHeuristic(
                    name=name,
                    rule=f"在决策时优先考虑{name.lower()}",
                    examples=heuristic_examples[name],
                    confidence=min(0.5 + count * 0.1, 0.95)
                ))
        
        self.heuristics.sort(key=lambda h: h.confidence, reverse=True)
        
        return self.heuristics
    
    def analyze_expression_dna(self, messages: List[str]) -> ExpressionDNA:
        """
        分析表达 DNA
        
        Args:
            messages: 消息列表
        
        Returns:
            ExpressionDNA 对象
        """
        if not messages:
            return ExpressionDNA(
                style="unknown",
                avg_length=0,
                common_phrases=[],
                tone="neutral",
                emoji_usage={}
            )
        
        # 计算平均长度
        avg_length = sum(len(m) for m in messages) / len(messages)
        
        # 提取常用短语
        word_freq = {}
        for msg in messages:
            words = re.findall(r'[\w]+', msg)
            for word in words:
                if len(word) > 2:
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        common_phrases = sorted(word_freq.keys(), key=lambda w: -word_freq[w])[:10]
        
        # 分析语气
        if avg_length < 30:
            tone = "简洁"
        elif avg_length < 100:
            tone = "中等"
        else:
            tone = "详细"
        
        # 表情符号使用
        emoji_usage = {}
        for msg in messages:
            for char in msg:
                if ord(char) > 12700:  # emoji 范围
                    emoji_usage[char] = emoji_usage.get(char, 0) + 1
        
        # 风格判断
        if avg_length < 50 and len(emoji_usage) > 3:
            style = "极简 + 表情丰富"
        elif avg_length < 50:
            style = "极简黑客风"
        elif avg_length < 100:
            style = "标准"
        else:
            style = "详细"
        
        self.dna = ExpressionDNA(
            style=style,
            avg_length=avg_length,
            common_phrases=common_phrases,
            tone=tone,
            emoji_usage=emoji_usage
        )
        
        return self.dna
    
    def generate_profile(self) -> Dict:
        """生成用户心智档案"""
        return {
            "mind_models": [asdict(m) for m in self.models],
            "decision_heuristics": [asdict(h) for h in self.heuristics],
            "expression_dna": asdict(self.dna) if self.dna else None,
            "generated_at": datetime.now().isoformat()
        }
    
    def save_to_user_model(self):
        """保存到用户模型"""
        profile = self.generate_profile()
        
        if USER_MODEL_FILE.exists():
            with open(USER_MODEL_FILE, "r", encoding="utf-8") as f:
                user_model = json.load(f)
        else:
            user_model = {}
        
        # 更新
        user_model["mind_models"] = profile["mind_models"]
        user_model["decision_heuristics"] = profile["decision_heuristics"]
        user_model["expression_dna"] = profile["expression_dna"]
        
        # 保存
        USER_MODEL_FILE.parent.mkdir(exist_ok=True)
        with open(USER_MODEL_FILE, "w", encoding="utf-8") as f:
            json.dump(user_model, f, indent=2, ensure_ascii=False)
        
        return True


def main():
    """测试"""
    extractor = MindModelExtractor()
    
    print("🧠 心智模型提取器测试")
    print()
    
    # 测试对话
    conversations = [
        {"user": "这个事的物理极限是什么？"},
        {"user": "抛开现有方案，最优解是什么？"},
        {"user": "反过来会怎样？"},
        {"user": "然后呢？接下来会发生什么？"},
        {"user": "概率有多大？期望值呢？"}
    ]
    
    models = extractor.extract_mind_models(conversations)
    print(f"识别心智模型：{len(models)} 个")
    for m in models:
        print(f"  - {m.name} (频率：{m.frequency:.2f})")
    
    print()
    
    # 测试表达 DNA
    messages = ["✅ 好的", "🚀 开始执行", "SAYELF，已完成"]
    dna = extractor.analyze_expression_dna(messages)
    print(f"表达 DNA: {dna.style}, {dna.tone}")


if __name__ == "__main__":
    main()
