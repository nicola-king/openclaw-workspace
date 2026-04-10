#!/usr/bin/env python3
"""
教学方法库

融合各派真谛，根据根器选择方法
直击人心，一语惊醒梦中人

作者：太一 AGI
创建：2026-04-10
"""

from dataclasses import dataclass
from typing import Dict, List
import random


@dataclass
class TeachingMethod:
    """教学方法"""
    name: str
    root_type: str  # 适合根器 (上/中/下/通用)
    style: str  # 风格 (顿悟/渐修/方便)
    description: str
    examples: List[str]
    suitable_scenarios: List[str]


# ═══════════════════════════════════════════════════════════
# 教学方法库
# ═══════════════════════════════════════════════════════════

TEACHING_METHODS: Dict[str, TeachingMethod] = {
    # ───────────────────────────────────────────────────────
    # 上根器 - 顿悟法门
    # ───────────────────────────────────────────────────────
    
    "direct_pointing": TeachingMethod(
        name="直指人心",
        root_type="上",
        style="顿悟",
        description="不立文字，直指人心，见性成佛",
        examples=[
            "佛即心，心即佛。汝今之心，即是佛心。",
            "汝是阿谁？念佛的是谁？",
            "当下即是，拟思即差。",
            "即心即佛，无心是道。",
        ],
        suitable_scenarios=["询问佛性", "寻求开悟", "执著文字"]
    ),
    
    "koan": TeachingMethod(
        name="禅宗公案",
        root_type="上",
        style="顿悟",
        description="以公案起疑情，疑情破则开悟",
        examples=[
            "赵州茶：僧问'如何是佛法大意？'赵州云'吃茶去。'",
            "庭前柏树子：僧问'祖师西来意？'赵州云'庭前柏树子。'",
            "只手之声：参'听只手之声'。",
            "无字公案：参'无'字。",
        ],
        suitable_scenarios=["求佛法大意", "问祖师意", "执著概念"]
    ),
    
    "hua_tou": TeachingMethod(
        name="参话头",
        root_type="上",
        style="顿悟",
        description="参一句话头，疑情成片，桶底脱落",
        examples=[
            "念佛的是谁？",
            "父母未生前，如何是汝本来面目？",
            "万法归一，一归何处？",
            "拖死尸的是谁？",
        ],
        suitable_scenarios=["求开悟", "问本来面目", "寻求解脱"]
    ),
    
    "bang_he": TeachingMethod(
        name="棒喝",
        root_type="上",
        style="顿悟",
        description="当头棒喝，惊醒梦中人",
        examples=[
            "喝！汝还在梦中么？",
            "棒下无生忍，目前不容情！",
            "咄！这钝汉！",
            "汝向外驰求做什么？",
        ],
        suitable_scenarios=["执著深重", "向外驰求", "沉迷不悟"]
    ),
    
    "emptiness_break": TeachingMethod(
        name="破执显空",
        root_type="上",
        style="顿悟",
        description="破除执著，显发空性",
        examples=[
            "凡所有相，皆是虚妄。汝执著什么？",
            "一切有为法，如梦幻泡影。汝当真么？",
            "应无所住而生其心。汝心住何处？",
            "色即是空，空即是色。汝见色不见空？",
        ],
        suitable_scenarios=["执著相", "执著法", "执著空"]
    ),
    
    # ───────────────────────────────────────────────────────
    # 中根器 - 渐修法门
    # ───────────────────────────────────────────────────────
    
    "gradual_cultivation": TeachingMethod(
        name="渐修渐悟",
        root_type="中",
        style="渐修",
        description="循序渐进，由戒生定，由定发慧",
        examples=[
            "先持戒，后修定，后发慧。",
            "诸恶莫作，众善奉行，自净其意。",
            "身是菩提树，心如明镜台。时时勤拂拭，勿使惹尘埃。",
            "从闻思修入三摩地。",
        ],
        suitable_scenarios=["初学者", "求修行方法", "问如何入手"]
    ),
    
    "sutra_study": TeachingMethod(
        name="经典研读",
        root_type="中",
        style="渐修",
        description="研读经典，理解教义，如理思惟",
        examples=[
            "《心经》云：色不异空，空不异色。",
            "《金刚经》云：应无所住而生其心。",
            "《法华经》云：开示悟入佛之知见。",
            "《楞严经》云：一切众生皆具如来智慧德相。",
        ],
        suitable_scenarios=["求教义", "问经典", "寻求理解"]
    ),
    
    "meditation_guide": TeachingMethod(
        name="禅修指导",
        root_type="中",
        style="渐修",
        description="指导禅修方法，培养定力",
        examples=[
            "观呼吸：专注呼吸，出入息分明。",
            "四念处：观身不净，观受是苦，观心无常，观法无我。",
            "默照禅：默默忘言，昭昭现前。",
            "话头禅：提话头，不起第二念。",
        ],
        suitable_scenarios=["求禅修方法", "问如何打坐", "心散乱"]
    ),
    
    "cause_effect": TeachingMethod(
        name="因果开示",
        root_type="中",
        style="渐修",
        description="开示因果道理，止恶行善",
        examples=[
            "善有善报，恶有恶报。",
            "欲知前世因，今生受者是。欲知来世果，今生作者是。",
            "菩萨畏因，众生畏果。",
            "一念嗔心起，百万障门开。",
        ],
        suitable_scenarios=["问命运", "遭遇困境", "造恶业"]
    ),
    
    # ───────────────────────────────────────────────────────
    # 下根器 - 方便法门
    # ───────────────────────────────────────────────────────
    
    "simple_language": TeachingMethod(
        name="大白话",
        root_type="下",
        style="方便",
        description="通俗易懂，用日常语言讲解佛法",
        examples=[
            "佛法很简单，就是做好事，存好心，说好话。",
            "别太执着，放下就轻松了。",
            "人生就像做梦，别太当真。",
            "开心也是一天，不开心也是一天，何不开心点？",
        ],
        suitable_scenarios=["初学者", "文化不高", "问简单问题"]
    ),
    
    "story_telling": TeachingMethod(
        name="故事比喻",
        root_type="下",
        style="方便",
        description="用故事和比喻说明佛法道理",
        examples=[
            "就像一个人背着沉重的包袱，放下就轻松了。",
            "好比水中月，镜中花，看得见摸不着。",
            "如同小孩玩游戏，太认真就输了。",
            "好像做梦，梦里什么都有，醒来什么都没有。",
        ],
        suitable_scenarios=["不理解抽象概念", "需要具体例子", "问深奥问题"]
    ),
    
    "pure_land": TeachingMethod(
        name="念佛往生",
        root_type="下",
        style="方便",
        description="教导念佛往生净土法门",
        examples=[
            "南无阿弥陀佛，念这句佛号就能往生极乐世界。",
            "信愿行三资粮，具足就能往生。",
            "末法众生，唯依念佛得度。",
            "一念相应一念佛，念念相应念念佛。",
        ],
        suitable_scenarios=["求往生", "问净土法门", "年老体弱"]
    ),
    
    "blessing_ritual": TeachingMethod(
        name="拜佛供养",
        root_type="下",
        style="方便",
        description="教导拜佛、供养等仪式修行",
        examples=[
            "每天拜佛，能消业障。",
            "供花供果，培养布施心。",
            "烧香礼拜，表达恭敬心。",
            "念经持咒，能得加持。",
        ],
        suitable_scenarios=["求加持", "问如何供养", "需要仪式感"]
    ),
    
    # ───────────────────────────────────────────────────────
    # 心理学融合 - 现代方便
    # ───────────────────────────────────────────────────────
    
    "freud_analysis": TeachingMethod(
        name="精神分析",
        root_type="中",
        style="现代",
        description="用弗洛伊德精神分析解读佛法",
        examples=[
            "你的本我被贪嗔痴控制，需要超我 (佛性) 来引导。",
            "你的执著来自童年创伤，放下过去，活在当下。",
            "梦境是你潜意识的显现，观梦如观心。",
            "你的我执就是自我，需要超越自我，证得无我。",
        ],
        suitable_scenarios=["有心理学背景", "问心理问题", "现代知识分子"]
    ),
    
    "jung_analysis": TeachingMethod(
        name="荣格心理学",
        root_type="中",
        style="现代",
        description="用荣格分析心理学解读佛法",
        examples=[
            "你的集体无意识就是阿赖耶识，含藏一切种子。",
            "自性化过程就是明心见性的过程。",
            "整合阴影就是转烦恼为菩提。",
            "曼陀罗就是坛城，代表心灵的完整。",
        ],
        suitable_scenarios=["有心理学背景", "问心灵成长", "寻求整合"]
    ),
    
    "existentialism": TeachingMethod(
        name="存在主义",
        root_type="中",
        style="现代",
        description="用存在主义心理学解读佛法",
        examples=[
            "你的存在焦虑就是苦，佛法就是解脱之道。",
            "你有自由选择，但也要承担业力。",
            "生命的意义在于觉悟，而非逃避。",
            "面对死亡，才能体悟无常，珍惜当下。",
        ],
        suitable_scenarios=["问生命意义", "存在焦虑", "现代知识分子"]
    ),
}


# ═══════════════════════════════════════════════════════════
# 核心函数
# ═══════════════════════════════════════════════════════════

def select_method(root_type: str, question: str, user_background: str = None) -> TeachingMethod:
    """
    根据根器和问题选择教学方法
    
    Args:
        root_type: 根器类型 (上/中/下)
        question: 用户问题
        user_background: 用户背景 (如"心理学"/"初学者"等)
    
    Returns:
        最适合的教学方法
    """
    # 筛选适合根器的方法
    suitable_methods = [m for m in TEACHING_METHODS.values() if m.root_type in [root_type, "通用"]]
    
    # 如果有心理学背景，优先心理学方法
    if user_background and "心理学" in user_background:
        psych_methods = [m for m in suitable_methods if "心理学" in m.name or m.style == "现代"]
        if psych_methods:
            return random.choice(psych_methods)
    
    # 根据问题场景匹配
    for method in suitable_methods:
        for scenario in method.suitable_scenarios:
            if scenario in question:
                return method
    
    # 默认返回该根器的第一个方法
    return suitable_methods[0] if suitable_methods else TEACHING_METHODS["simple_language"]


def generate_response(method: TeachingMethod, question: str, dharma_teaching=None) -> str:
    """
    根据教学方法生成回答
    
    Args:
        method: 教学方法
        question: 用户问题
        dharma_teaching: 相关佛法教义
    
    Returns:
        回答内容
    """
    # 选择示例
    example = random.choice(method.examples)
    
    response = f"""
【{method.name}】({method.style})

{example}

"""
    
    # 如果有佛法教义，添加教义内容
    if dharma_teaching:
        response += f"""
📚 佛法开示：

{dharma_teaching.description[:300]}...

核心：{dharma_teaching.core_concept}

"""
    
    response += """
🙏 愿你智悲双修，觉悟成佛。
"""
    
    return response


def main():
    """主函数 - 测试"""
    print("🪷 教学方法库测试")
    print("="*60)
    
    # 统计
    print(f"\n📊 教学方法数量：{len(TEACHING_METHODS)} 个")
    
    # 按根器统计
    by_root = {}
    for method in TEACHING_METHODS.values():
        if method.root_type not in by_root:
            by_root[method.root_type] = 0
        by_root[method.root_type] += 1
    
    print("\n📚 按根器统计:")
    for root, count in by_root.items():
        print(f"   {root}根器：{count} 个方法")
    
    # 测试方法选择
    print("\n1. 方法选择测试...")
    test_cases = [
        ("上", "什么是佛法？", None),
        ("中", "如何修行？", None),
        ("下", "佛法好难懂", None),
        ("中", "我有焦虑问题", "心理学"),
    ]
    
    for root, question, background in test_cases:
        method = select_method(root, question, background)
        print(f"   根器:{root} 问题:'{question[:10]}...' → {method.name}")
    
    # 测试回答生成
    print("\n2. 回答生成测试...")
    method = TEACHING_METHODS["direct_pointing"]
    response = generate_response(method, "什么是佛？")
    print(f"   {response[:200]}...")
    
    print("\n✅ 教学方法库测试完成!")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
