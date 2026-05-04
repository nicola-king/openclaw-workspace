#!/usr/bin/env python3
"""
根器评估系统

通过对话评估用户根器
上根利器/中根器/下根器

作者：太一 AGI
创建：2026-04-10
"""

from dataclasses import dataclass
from typing import Dict, List
import json
from pathlib import Path


@dataclass
class RootAssessment:
    """根器评估结果"""
    root_type: str  # 上/中/下
    confidence: float  # 置信度 (0-1)
    characteristics: List[str]  # 特征描述
    recommended_methods: List[str]  # 推荐方法
    enlightenment_stage: str  # 觉悟阶段 (信/解/行/证)


# ═══════════════════════════════════════════════════════════
# 根器评估标准
# ═══════════════════════════════════════════════════════════

ROOT_INDICATORS = {
    "上": {
        "特征": [
            "悟性高，一点即通",
            "能接受空性直接教导",
            "不执著文字相",
            "有疑情，好参究",
            "能当下承担",
        ],
        "问题示例": [
            "什么是本来面目？",
            "如何是佛法大意？",
            "念佛的是谁？",
            "如何是祖师西来意？",
        ],
        "回答特征": [
            "简洁直接",
            "能理解公案",
            "不执著概念",
        ],
        "推荐方法": ["直指人心", "禅宗公案", "参话头", "棒喝", "破执显空"],
    },
    "中": {
        "特征": [
            "悟性中等，需要循序渐进",
            "能理解理论，需要实践指导",
            "有一定佛学基础",
            "愿意禅修实践",
        ],
        "问题示例": [
            "如何修行？",
            "什么是四圣谛？",
            "如何打坐？",
            "心经讲什么？",
        ],
        "回答特征": [
            "能理解教义",
            "需要具体方法",
            "有修行意愿",
        ],
        "推荐方法": ["渐修渐悟", "经典研读", "禅修指导", "因果开示"],
    },
    "下": {
        "特征": [
            "悟性较低，需要善巧方便",
            "需要具体方法和仪式感",
            "佛学基础薄弱",
            "需要鼓励和安慰",
        ],
        "问题示例": [
            "佛法是什么？",
            "念佛有用吗？",
            "如何消灾？",
            "佛法好难懂",
        ],
        "回答特征": [
            "需要通俗解释",
            "喜欢故事比喻",
            "需要信心建立",
        ],
        "推荐方法": ["大白话", "故事比喻", "念佛往生", "拜佛供养"],
    },
}


# ═══════════════════════════════════════════════════════════
# 评估函数
# ═══════════════════════════════════════════════════════════

def assess_by_question(question: str) -> RootAssessment:
    """
    通过问题评估根器
    
    Args:
        question: 用户问题
    
    Returns:
        根器评估结果
    """
    score = {"上": 0, "中": 0, "下": 0}
    
    # 上根器指标
    upper_keywords = ["本来面目", "佛法大意", "祖师西来意", "是谁", "如何是", "即心即佛"]
    for keyword in upper_keywords:
        if keyword in question:
            score["上"] += 2
    
    # 中根器指标
    middle_keywords = ["如何修行", "四圣谛", "八正道", "打坐", "禅修", "心经", "金刚经"]
    for keyword in middle_keywords:
        if keyword in question:
            score["中"] += 2
    
    # 下根器指标
    lower_keywords = ["佛法是什么", "好难懂", "念佛有用", "消灾", "保佑", "简单"]
    for keyword in lower_keywords:
        if keyword in question:
            score["下"] += 2
    
    # 确定根器
    root_type = max(score, key=score.get)
    confidence = score[root_type] / max(1, sum(score.values()))
    
    return RootAssessment(
        root_type=root_type,
        confidence=min(1.0, confidence),
        characteristics=ROOT_INDICATORS[root_type]["特征"][:3],
        recommended_methods=ROOT_INDICATORS[root_type]["推荐方法"],
        enlightenment_stage="信"  # 初始阶段
    )


def assess_by_dialogue(dialogue_history: List[Dict]) -> RootAssessment:
    """
    通过对话历史评估根器
    
    Args:
        dialogue_history: 对话历史记录
    
    Returns:
        根器评估结果
    """
    if not dialogue_history:
        return assess_by_question("")
    
    score = {"上": 0, "中": 0, "下": 0}
    
    for turn in dialogue_history:
        question = turn.get("question", "")
        answer = turn.get("answer", "")
        user_response = turn.get("user_response", "")
        
        # 评估理解程度
        if "明白了" in user_response or "懂了" in user_response:
            score["中"] += 1
            score["上"] += 1
        elif "不懂" in user_response or "不明白" in user_response:
            score["下"] += 1
        
        # 评估悟性
        if len(question) < 10 and "如何是" in question:
            score["上"] += 2
        elif "为什么" in question:
            score["中"] += 1
        elif "是什么" in question:
            score["下"] += 1
    
    # 确定根器
    root_type = max(score, key=score.get)
    confidence = score[root_type] / max(1, sum(score.values()))
    
    return RootAssessment(
        root_type=root_type,
        confidence=min(1.0, confidence),
        characteristics=ROOT_INDICATORS[root_type]["特征"][:3],
        recommended_methods=ROOT_INDICATORS[root_type]["推荐方法"],
        enlightenment_stage="解"  # 对话后可能进入理解阶段
    )


def update_enlightenment_stage(user_id: str, progress_data: Dict) -> str:
    """
    更新觉悟阶段
    
    Args:
        user_id: 用户 ID
        progress_data: 进度数据
    
    Returns:
        觉悟阶段 (信/解/行/证)
    """
    # 加载用户进度
    user_file = Path(__file__).parent / "users" / f"{user_id}.json"
    
    if user_file.exists():
        with open(user_file, "r", encoding="utf-8") as f:
            user_data = json.load(f)
    else:
        user_data = {"enlightenment_stage": "信", "interactions": 0}
    
    # 更新阶段
    interactions = user_data.get("interactions", 0) + 1
    user_data["interactions"] = interactions
    
    # 根据互动次数和深度更新阶段
    if interactions < 5:
        stage = "信"
    elif interactions < 20:
        stage = "解"
    elif interactions < 50:
        stage = "行"
    else:
        stage = "证"
    
    user_data["enlightenment_stage"] = stage
    
    # 保存
    user_file.parent.mkdir(exist_ok=True)
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)
    
    return stage


def get_user_profile(user_id: str) -> Dict:
    """获取用户档案"""
    user_file = Path(__file__).parent / "users" / f"{user_id}.json"
    
    if user_file.exists():
        with open(user_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    return {
        "user_id": user_id,
        "root_type": None,
        "enlightenment_stage": "信",
        "interactions": 0,
        "dialogue_history": [],
        "breakthroughs": [],
    }


def main():
    """主函数 - 测试"""
    print("🪷 根器评估系统测试")
    print("="*60)
    
    # 测试问题评估
    print("\n1. 问题评估测试...")
    test_questions = [
        "什么是本来面目？",
        "如何修行？",
        "佛法好难懂",
        "念佛的是谁？",
    ]
    
    for question in test_questions:
        assessment = assess_by_question(question)
        print(f"   问题:'{question}' → {assessment.root_type}根器 (置信度:{assessment.confidence:.2f})")
    
    # 测试对话评估
    print("\n2. 对话评估测试...")
    dialogue = [
        {"question": "什么是佛法？", "answer": "...", "user_response": "明白了"},
        {"question": "如何是？", "answer": "...", "user_response": "懂了"},
    ]
    assessment = assess_by_dialogue(dialogue)
    print(f"   对话评估 → {assessment.root_type}根器")
    
    # 测试用户档案
    print("\n3. 用户档案测试...")
    profile = get_user_profile("test_user")
    print(f"   用户档案：{profile}")
    
    print("\n✅ 根器评估系统测试完成!")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
