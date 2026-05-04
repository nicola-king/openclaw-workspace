#!/usr/bin/env python3
"""
道家经典知识库

融合：
- 老子《道德经》81 章精选
- 庄子《南华经》核心篇章
- 列子《冲虚经》精选

作者：太一 AGI
创建：2026-04-10
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DaoTeaching:
    """道家教导"""
    name: str
    source: str  # 道德经/庄子/列子
    chapter: str  # 章节
    core_concept: str  # 核心教导
    original_text: str  # 原文
    translation: str  # 译文
    application: str  # 应用场景
    psychology_fusion: str  # 心理学融合


# ═══════════════════════════════════════════════════════════
# 道德经核心教义 (81 章精选)
# ═══════════════════════════════════════════════════════════

DAO_DE_JING = {
    "chapter_1": DaoTeaching(
        name="道可道",
        source="道德经",
        chapter="第 1 章",
        core_concept="道的本质",
        original_text="道可道，非常道。名可名，非常名。",
        translation="可以用言语表述的道，就不是永恒的道。可以用名称命名的名，就不是永恒的名。",
        application="理解道的超越性，不要执著于言语概念",
        psychology_fusion="荣格：超越语言的原型体验"
    ),
    
    "chapter_8": DaoTeaching(
        name="上善若水",
        source="道德经",
        chapter="第 8 章",
        core_concept="为人处世",
        original_text="上善若水。水善利万物而不争，处众人之所恶，故几于道。",
        translation="最高的善像水一样。水善于滋润万物而不与万物相争，停留在众人都不喜欢的地方，所以最接近于道。",
        application="学习水的品格，谦下不争，利他无私",
        psychology_fusion="阿德勒：社会兴趣，利他精神"
    ),
    
    "chapter_25": DaoTeaching(
        name="人法地",
        source="道德经",
        chapter="第 25 章",
        core_concept="天人合一",
        original_text="人法地，地法天，天法道，道法自然。",
        translation="人取法地，地取法天，天取法道，道取法自然。",
        application="顺应自然，与天地合一",
        psychology_fusion="荣格：自性化，与集体无意识连接"
    ),
    
    "chapter_37": DaoTeaching(
        name="无为而治",
        source="道德经",
        chapter="第 37 章",
        core_concept="治国修身",
        original_text="道常无为而无不为。侯王若能守之，万物将自化。",
        translation="道永远是顺其自然的，但没有什么事情不是它所为。侯王如果能持守它，万物将自然化育。",
        application="无为而治，让事物自然发展",
        psychology_fusion="弗洛伊德：减少超我压制，让本我自然表达"
    ),
    
    "chapter_40": DaoTeaching(
        name="反者道之动",
        source="道德经",
        chapter="第 40 章",
        core_concept="辩证思维",
        original_text="反者道之动，弱者道之用。",
        translation="循环往复是道的运动规律，柔弱是道的作用方式。",
        application="理解事物的辩证关系，以柔克刚",
        psychology_fusion="荣格：阴影整合，对立面统一"
    ),
    
    "chapter_63": DaoTeaching(
        name="为无为",
        source="道德经",
        chapter="第 63 章",
        core_concept="生活智慧",
        original_text="为无为，事无事，味无味。",
        translation="以无为的态度去作为，以不做事的方式去做事，以无味作为味。",
        application="放下执著，顺其自然",
        psychology_fusion="阿德勒：放下自卑，追求优越"
    ),
    
    "chapter_64": DaoTeaching(
        name="千里之行",
        source="道德经",
        chapter="第 64 章",
        core_concept="循序渐进",
        original_text="合抱之木，生于毫末。九层之台，起于累土。千里之行，始于足下。",
        translation="合抱的大树，从细小的萌芽生长起来。九层的高台，从一筐土一筐土筑起。千里的远行，从脚下第一步开始。",
        application="任何大事都是从小事积累而成",
        psychology_fusion="阿德勒：小步骤，大改变"
    ),
    
    "chapter_76": DaoTeaching(
        name="柔弱胜刚强",
        source="道德经",
        chapter="第 76 章",
        core_concept="以柔克刚",
        original_text="柔弱胜刚强。鱼不可脱于渊，国之利器不可以示人。",
        translation="柔弱能战胜刚强。鱼不能离开深渊，国家的锐利武器不能向人炫耀。",
        application="保持柔弱，不要逞强",
        psychology_fusion="荣格：整合阴影，而非压制"
    ),
}


# ═══════════════════════════════════════════════════════════
# 庄子核心思想
# ═══════════════════════════════════════════════════════════

ZHUANG_ZI = {
    "xiaoyao_you": DaoTeaching(
        name="逍遥游",
        source="庄子",
        chapter="内篇·逍遥游",
        core_concept="心灵自由",
        original_text="北冥有鱼，其名为鲲。鲲之大，不知其几千里也。化而为鸟，其名为鹏。",
        translation="北海有一条鱼，名字叫鲲。鲲的巨大，不知道有几千里。变化成为鸟，名字叫鹏。",
        application="超越世俗束缚，追求心灵自由",
        psychology_fusion="荣格：自性化，超越自我"
    ),
    
    "qiwu_lun": DaoTeaching(
        name="齐物论",
        source="庄子",
        chapter="内篇·齐物论",
        core_concept="超越对立",
        original_text="天地与我并生，而万物与我为一。",
        translation="天地与我一同生存，万物与我合为一体。",
        application="超越是非、善恶、美丑的二元对立",
        psychology_fusion="荣格：对立面统一"
    ),
    
    "yangsheng_zhu": DaoTeaching(
        name="养生主",
        source="庄子",
        chapter="内篇·养生主",
        core_concept="身心健康",
        original_text="吾生也有涯，而知也无涯。以有涯随无涯，殆已！",
        translation="我的生命是有限的，而知识是无限的。用有限的生命追求无限的知识，危险啊！",
        application="顺应自然，不要过度追求",
        psychology_fusion="弗洛伊德：平衡本我与超我"
    ),
    
    "renjian_shi": DaoTeaching(
        name="人间世",
        source="庄子",
        chapter="内篇·人间世",
        core_concept="处世之道",
        original_text="虚室生白，吉祥止止。",
        translation="空虚的房间产生光明，吉祥就停留在这里。",
        application="保持内心空虚，不执著",
        psychology_fusion="阿德勒：放下自卑情结"
    ),
    
    "de_chong_fu": DaoTeaching(
        name="德充符",
        source="庄子",
        chapter="内篇·德充符",
        core_concept="内在修养",
        original_text="人莫鉴于流水而鉴于止水。",
        translation="人不要在流动的水面照自己，而要在静止的水面照自己。",
        application="保持内心平静，才能看清自己",
        psychology_fusion="荣格：内观，自我觉察"
    ),
    
    "zhuangzhou_mengdie": DaoTeaching(
        name="庄周梦蝶",
        source="庄子",
        chapter="内篇·齐物论",
        core_concept="物我两忘",
        original_text="昔者庄周梦为胡蝶，栩栩然胡蝶也。不知周也。俄然觉，则蘧蘧然周也。不知周之梦为胡蝶与？胡蝶之梦为周与？",
        translation="从前庄周梦见自己变成蝴蝶，生动活泼的一只蝴蝶。不知道自己就是庄周。突然醒来，发现自己就是庄周。不知道是庄周做梦变成蝴蝶呢？还是蝴蝶做梦变成庄周呢？",
        application="超越物我的界限，体验万物一体",
        psychology_fusion="荣格：集体无意识，原型体验"
    ),
}


# ═══════════════════════════════════════════════════════════
# 心理学融合知识库
# ═══════════════════════════════════════════════════════════

PSYCHOLOGY_FUSION = {
    "freud": {
        "name": "弗洛伊德精神分析",
        "core_concepts": [
            "本我/自我/超我",
            "潜意识理论",
            "梦的解析",
            "性本能与攻击本能"
        ],
        "dao_fusion": "本我即自然本性 (道法自然)，超我即人为造作 (有为)，治疗目标是回归自然本性"
    },
    
    "adler": {
        "name": "阿德勒个体心理学",
        "core_concepts": [
            "自卑与超越",
            "社会兴趣",
            "目的论",
            "生活方式"
        ],
        "dao_fusion": "自卑感是失去与道的连接，社会兴趣是与万物合一，目的是顺应自然目的"
    },
    
    "jung": {
        "name": "荣格分析心理学",
        "core_concepts": [
            "集体无意识",
            "原型理论",
            "自性化过程",
            "阴影整合"
        ],
        "dao_fusion": "集体无意识即道，原型即德，自性化即得道，阴影整合即阴阳平衡"
    },
}


# ═══════════════════════════════════════════════════════════
# 核心函数
# ═══════════════════════════════════════════════════════════

def get_dao_teaching_by_keyword(keyword: str) -> DaoTeaching:
    """根据关键词获取道家教导"""
    keyword_map = {
        "道": "chapter_1",
        "水": "chapter_8",
        "自然": "chapter_25",
        "无为": "chapter_37",
        "反": "chapter_40",
        "柔弱": "chapter_76",
        "逍遥": "xiaoyao_you",
        "齐物": "qiwu_lun",
        "养生": "yangsheng_zhu",
        "梦": "zhuangzhou_mengdie",
    }
    
    for key, teaching_id in keyword_map.items():
        if key in keyword:
            if teaching_id in DAO_DE_JING:
                return DAO_DE_JING[teaching_id]
            elif teaching_id in ZHUANG_ZI:
                return ZHUANG_ZI[teaching_id]
    
    # 默认返回"道可道"
    return DAO_DE_JING["chapter_1"]


def get_psychology_fusion(school: str) -> Dict:
    """获取心理学融合信息"""
    return PSYCHOLOGY_FUSION.get(school, PSYCHOLOGY_FUSION["jung"])


def main():
    """主函数 - 测试"""
    print("🌿 道家经典知识库测试")
    print("="*60)
    
    # 统计
    print(f"\n📊 知识库统计:")
    print(f"   道德经：{len(DAO_DE_JING)} 章")
    print(f"   庄子：{len(ZHUANG_ZI)} 篇")
    print(f"   心理学派：{len(PSYCHOLOGY_FUSION)} 个")
    
    # 测试查询
    print("\n1. 关键词查询测试...")
    test_keywords = ["道", "水", "逍遥", "梦"]
    for keyword in test_keywords:
        teaching = get_dao_teaching_by_keyword(keyword)
        print(f"   '{keyword}' → {teaching.name} ({teaching.source})")
    
    # 测试心理学融合
    print("\n2. 心理学融合测试...")
    for school in PSYCHOLOGY_FUSION:
        info = get_psychology_fusion(school)
        print(f"   {info['name']}")
    
    print("\n✅ 道家经典知识库测试完成!")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
