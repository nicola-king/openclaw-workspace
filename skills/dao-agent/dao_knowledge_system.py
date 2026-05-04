#!/usr/bin/env python3
"""
🌿 道家道教底层逻辑知识体系

构建完整的道家道教知识体系：
- 核心概念 (道/德/无/有/自然)
- 宇宙观 (天人合一/阴阳五行)
- 修炼体系 (内丹/外丹/符箓)
- 伦理观 (无为/清静/积德)
- 神仙体系 (三清/四御/神仙)

取其精华，去其糟粕。

作者：太一 AGI
创建：2026-04-11
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class CoreConcept:
    """核心概念"""
    name: str
    category: str  # 核心概念/宇宙观/修炼体系/伦理观/神仙体系
    definition: str  # 定义
    explanation: str  # 详细解释
    source: str  # 来源经典
    modern_application: str  # 现代应用
    essence: bool  # 是否精华


# ═══════════════════════════════════════════════════════════
# 一、核心概念 (道/德/无/有/自然等)
# ═══════════════════════════════════════════════════════════

CORE_CONCEPTS = {
    "dao": CoreConcept(
        name="道",
        category="核心概念",
        definition="宇宙万物的本源和运行规律",
        explanation="""
道是道家哲学的最高范畴：
1. 道是宇宙的本源：道生一，一生二，二生三，三生万物
2. 道是运行的规律：人法地，地法天，天法道，道法自然
3. 道是超越的存在：道可道，非常道
4. 道是无形的：视之不见，听之不闻，搏之不得
""",
        source="道德经",
        modern_application="理解事物的本质规律，顺应自然发展",
        essence=True
    ),
    
    "de": CoreConcept(
        name="德",
        category="核心概念",
        definition="道的体现和功用",
        explanation="""
德是道在具体事物中的体现：
1. 德者，得也：得道之谓德
2. 上德不德：最高的德不表现为德
3. 德畜之：道生之，德畜之
4. 积德：积善之家，必有余庆
""",
        source="道德经",
        modern_application="修养品德，积德行善",
        essence=True
    ),
    
    "wu": CoreConcept(
        name="无",
        category="核心概念",
        definition="道的本体状态",
        explanation="""
无是道的本体状态：
1. 无中生有：天下万物生于有，有生于无
2. 无为：道常无为而无不为
3. 无用之用：人皆知有用之用，而莫知无用之用
4. 虚无：致虚极，守静笃
""",
        source="道德经",
        modern_application="放下执著，保持虚空的心态",
        essence=True
    ),
    
    "you": CoreConcept(
        name="有",
        category="核心概念",
        definition="道的显现状态",
        explanation="""
有是道的显现状态：
1. 有生有：天下万物生于有
2. 有无相生：有无相生，难易相成
3. 有之以为利：有之以为利，无之以为用
4. 有涯：吾生也有涯
""",
        source="道德经",
        modern_application="认识有限，追求无限",
        essence=True
    ),
    
    "ziran": CoreConcept(
        name="自然",
        category="核心概念",
        definition="道的本然状态",
        explanation="""
自然是道的本然状态：
1. 道法自然：人法地，地法天，天法道，道法自然
2. 自然而然：莫之命而常自然
3. 自然无为：辅万物之自然而不敢为
4. 自然本性：任性自然，不假外求
""",
        source="道德经",
        modern_application="顺应自然，不强求，不造作",
        essence=True
    ),
    
    "wuwei": CoreConcept(
        name="无为",
        category="核心概念",
        definition="顺应自然的处世方式",
        explanation="""
无为是道家的核心实践原则：
1. 无为而无不为：道常无为而无不为
2. 无为而治：为无为，则无不治
3. 无为不争：夫唯不争，故无尤
4. 无为自然：我无为而民自化
""",
        source="道德经",
        modern_application="放下控制，让事物自然发展",
        essence=True
    ),
}


# ═══════════════════════════════════════════════════════════
# 二、宇宙观 (天人合一/阴阳五行等)
# ═══════════════════════════════════════════════════════════

COSMOLOGY = {
    "tianrenheyi": CoreConcept(
        name="天人合一",
        category="宇宙观",
        definition="人与天地自然的统一",
        explanation="""
天人合一是道家的核心宇宙观：
1. 天地与我并生：天地与我并生，而万物与我为一
2. 人与天地参：人能参天地之化育
3. 天人感应：天人感应，同类相动
4. 天人相应：人身一小天地
""",
        source="庄子",
        modern_application="与自然和谐相处，保护环境",
        essence=True
    ),
    
    "yinyang": CoreConcept(
        name="阴阳",
        category="宇宙观",
        definition="宇宙万物的两种基本力量",
        explanation="""
阴阳是宇宙的基本法则：
1. 一阴一阳之谓道：阴阳交替运行就是道
2. 阴阳相生：阴阳相生，循环不息
3. 阴阳平衡：阴平阳秘，精神乃治
4. 阴阳转化：重阴必阳，重阳必阴
""",
        source="易经/黄帝内经",
        modern_application="保持身心平衡，理解事物的两面性",
        essence=True
    ),
    
    "wuxing": CoreConcept(
        name="五行",
        category="宇宙观",
        definition="金木水火土五种基本元素",
        explanation="""
五行是构成宇宙的基本元素：
1. 五行相生：金生水，水生木，木生火，火生土，土生金
2. 五行相克：金克木，木克土，土克水，水克火，火克金
3. 五行对应：肝属木，心属火，脾属土，肺属金，肾属水
4. 五行运行：五行运行，化生万物
""",
        source="黄帝内经",
        modern_application="理解事物的相互关系，保持平衡",
        essence=True
    ),
    
    "hundun": CoreConcept(
        name="混沌",
        category="宇宙观",
        definition="宇宙未分化的原始状态",
        explanation="""
混沌是宇宙的原始状态：
1. 有物混成：有物混成，先天地生
2. 混沌未分：混沌未分，阴阳未判
3. 复归混沌：复归于婴儿，复归于无极
4. 混沌之德：混沌氏之术
""",
        source="道德经/庄子",
        modern_application="保持初心，回归本真",
        essence=True
    ),
}


# ═══════════════════════════════════════════════════════════
# 三、修炼体系 (内丹/外丹/符箓等)
# ═══════════════════════════════════════════════════════════

PRACTICE_SYSTEM = {
    "neidan": CoreConcept(
        name="内丹",
        category="修炼体系",
        definition="以自身为炉鼎的修炼方法",
        explanation="""
内丹是道家的核心修炼方法：
1. 炼精化气：将精气转化为真气
2. 炼气化神：将真气转化为元神
3. 炼神还虚：将元神归于虚无
4. 炼虚合道：与道合一
""",
        source="悟真篇/金丹大要",
        modern_application="修身养性，内观自省",
        essence=True
    ),
    
    "jingzuo": CoreConcept(
        name="静坐",
        category="修炼体系",
        definition="静坐冥想的修炼方法",
        explanation="""
静坐是道家的基本修炼方法：
1. 致虚极：致虚极，守静笃
2. 心斋：虚者，心斋也
3. 坐忘：堕肢体，黜聪明，离形去知
4. 守一：抱元守一，神不外驰
""",
        source="道德经/庄子",
        modern_application="冥想静心，减压养身",
        essence=True
    ),
    
    "daoyin": CoreConcept(
        name="导引",
        category="修炼体系",
        definition="导气引体的养生方法",
        explanation="""
导引是道家的养生修炼方法：
1. 导气令和：导气令和，引体令柔
2. 吐纳：吐故纳新
3. 按摩：按摩经络，通行气血
4. 运动：五禽戏/八段锦/太极拳
""",
        source="黄帝内经",
        modern_application="太极拳/气功/瑜伽等身心锻炼",
        essence=True
    ),
    
    "waidan": CoreConcept(
        name="外丹",
        category="修炼体系",
        definition="炼制丹药的修炼方法",
        explanation="""
外丹是道家的炼丹方法：
1. 炼丹术：以金石药物炼制丹药
2. 金丹：服食金丹，以求长生
3. 炉火：炉火纯青
4. 服食：服食丹药
""",
        source="抱朴子",
        modern_application="❌ 炼丹服药不可取，属于糟粕",
        essence=False  # 糟粕
    ),
    
    "fulu": CoreConcept(
        name="符箓",
        category="修炼体系",
        definition="画符念咒的法术",
        explanation="""
符箓是道教的法术：
1. 画符：画符念咒
2. 驱鬼：驱鬼降魔
3. 治病：符水治病
4. 祈福：祈福禳灾
""",
        source="道教法术",
        modern_application="❌ 画符念咒不可取，属于糟粕",
        essence=False  # 糟粕
    ),
}


# ═══════════════════════════════════════════════════════════
# 四、伦理观 (无为/清静/积德等)
# ═══════════════════════════════════════════════════════════

ETHICS = {
    "qingjing": CoreConcept(
        name="清静",
        category="伦理观",
        definition="清心寡欲的处世态度",
        explanation="""
清静是道家的基本伦理：
1. 清静无为：清静为天下正
2. 少私寡欲：见素抱朴，少私寡欲
3. 知足常乐：知足者富
4. 不争：夫唯不争，故无尤
""",
        source="道德经/清静经",
        modern_application="减少欲望，保持内心平静",
        essence=True
    ),
    
    "jide": CoreConcept(
        name="积德",
        category="伦理观",
        definition="积累善行功德",
        explanation="""
积德是道家的伦理实践：
1. 积善成德：积善成德，而神明自得
2. 厚德载物：地势坤，君子以厚德载物
3. 功德：功德无量
4. 阴德：阴德天报之
""",
        source="道德经/太上感应篇",
        modern_application="行善积德，助人为乐",
        essence=True
    ),
    
    "ci": CoreConcept(
        name="慈",
        category="伦理观",
        definition="慈悲爱心",
        explanation="""
慈是道家的三宝之一：
1. 我有三宝：一曰慈，二曰俭，三曰不敢为天下先
2. 慈故能勇：慈故能勇
3. 慈爱：以慈爱之心待人
4. 慈悲：慈悲为怀
""",
        source="道德经",
        modern_application="培养慈悲心，关爱他人",
        essence=True
    ),
    
    "jian": CoreConcept(
        name="俭",
        category="伦理观",
        definition="节俭朴素",
        explanation="""
俭是道家的三宝之一：
1. 俭故能广：俭故能广
2. 节俭：去甚，去奢，去泰
3. 朴素：见素抱朴
4. 知足：知足不辱，知止不殆
""",
        source="道德经",
        modern_application="节俭生活，环保可持续",
        essence=True
    ),
}


# ═══════════════════════════════════════════════════════════
# 五、神仙体系 (三清/四御/神仙等)
# ═══════════════════════════════════════════════════════════

IMMORTAL_SYSTEM = {
    "sanqing": CoreConcept(
        name="三清",
        category="神仙体系",
        definition="道教的最高神",
        explanation="""
三清是道教的最高神：
1. 玉清元始天尊：居于清微天
2. 上清灵宝天尊：居于禹余天
3. 太清道德天尊：居于大赤天 (即老子)
""",
        source="道教神系",
        modern_application="理解道教文化，取其精神内涵",
        essence=True
    ),
    
    "siyu": CoreConcept(
        name="四御",
        category="神仙体系",
        definition="辅佐三清的四位天帝",
        explanation="""
四御是辅佐三清的四位天帝：
1. 玉皇大帝：总执天道
2. 中天紫微北极大帝：协助玉皇执掌天道
3. 勾陈上宫天皇大帝：协助玉皇执掌南北极与天地人三才
4. 承天效法后土皇地祇：执掌阴阳生育、万物之美
""",
        source="道教神系",
        modern_application="理解道教文化，取其精神内涵",
        essence=True
    ),
    
    "shenxian": CoreConcept(
        name="神仙",
        category="神仙体系",
        definition="得道成仙的人",
        explanation="""
神仙是得道成仙的人：
1. 仙人：长生不老，神通广大
2. 真人：修真得道的人
3. 至人：至人无己
4. 神人：神人无功
""",
        source="庄子/列仙传",
        modern_application="追求精神超越，而非物质成仙",
        essence=True
    ),
    
    "chengxian": CoreConcept(
        name="成仙",
        category="神仙体系",
        definition="修炼成仙",
        explanation="""
成仙是道教的终极目标：
1. 肉身成仙：肉身飞升
2. 尸解成仙：尸解成仙
3. 白日飞升：白日飞升
4. 长生不老：长生不老
""",
        source="道教",
        modern_application="❌ 成仙迷信不可取，属于糟粕",
        essence=False  # 糟粕
    ),
}


# ═══════════════════════════════════════════════════════════
# 核心函数
# ═══════════════════════════════════════════════════════════

def get_all_essence_concepts() -> List[CoreConcept]:
    """获取所有精华概念"""
    all_concepts = []
    
    for collection in [CORE_CONCEPTS, COSMOLOGY, PRACTICE_SYSTEM, ETHICS, IMMORTAL_SYSTEM]:
        for concept in collection.values():
            if concept.essence:
                all_concepts.append(concept)
    
    return all_concepts


def get_concept_by_name(name: str) -> CoreConcept:
    """根据名称获取概念"""
    all_collections = [CORE_CONCEPTS, COSMOLOGY, PRACTICE_SYSTEM, ETHICS, IMMORTAL_SYSTEM]
    
    for collection in all_collections:
        for key, concept in collection.items():
            if name in concept.name or name in key:
                return concept
    
    return None


def get_concepts_by_category(category: str) -> List[CoreConcept]:
    """根据类别获取概念"""
    all_concepts = get_all_essence_concepts()
    return [c for c in all_concepts if c.category == category]


def get_statistics() -> Dict:
    """获取统计信息"""
    all_concepts = get_all_essence_concepts()
    
    # 按类别统计
    category_count = {}
    for c in all_concepts:
        if c.category not in category_count:
            category_count[c.category] = 0
        category_count[c.category] += 1
    
    # 统计糟粕
    false_count = sum(1 for c in PRACTICE_SYSTEM.values() if not c.essence)
    false_count += sum(1 for c in IMMORTAL_SYSTEM.values() if not c.essence)
    
    return {
        "total_essence": len(all_concepts),
        "total_false": false_count,
        "by_category": category_count,
    }


def main():
    """主函数 - 测试"""
    print("🌿 道家道教底层逻辑知识体系测试")
    print("="*60)
    
    # 统计
    stats = get_statistics()
    print(f"\n📊 知识体系统计:")
    print(f"   精华概念：{stats['total_essence']} 个")
    print(f"   糟粕概念：{stats['total_false']} 个")
    
    print(f"\n   按类别统计:")
    for category, count in stats['by_category'].items():
        print(f"      {category}: {count} 个")
    
    # 测试查询
    print("\n1. 概念查询测试...")
    test_concepts = ["道", "德", "阴阳", "内丹", "清静"]
    for name in test_concepts:
        concept = get_concept_by_name(name)
        if concept:
            print(f"   '{name}' → {concept.name} ({concept.category})")
    
    # 显示核心概念
    print("\n2. 核心概念展示...")
    dao = get_concept_by_name("道")
    print(f"   {dao.name}: {dao.definition}")
    print(f"   来源：{dao.source}")
    
    print("\n✅ 道家道教底层逻辑知识体系测试完成!")
    print("   取其精华，去其糟粕。")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
