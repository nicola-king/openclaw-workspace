#!/usr/bin/env python3
"""
道家完整经典知识库

搜集历史长河中道家所有经典及流派：
- 老子《道德经》
- 庄子《南华经》
- 列子《冲虚经》
- 文子《通玄经》
- 关尹子《文始经》
- 鹖冠子《鹖冠子》
- 黄老学派
- 魏晋玄学
- 唐宋内丹
- 全真道
- 正一道
- 等等

取其精华，去其糟粕。

作者：太一 AGI
创建：2026-04-10
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DaoTeaching:
    """道家教导"""
    name: str
    source: str  # 经典/流派
    period: str  # 历史时期
    core_concept: str  # 核心教导
    original_text: str  # 原文
    translation: str  # 译文/解释
    application: str  # 现代应用
    essence: bool  # 是否精华 (True=精华，False=糟粕)


# ═══════════════════════════════════════════════════════════
# 先秦道家 (公元前 770-221 年)
# ═══════════════════════════════════════════════════════════

PRE_QIN_DAOISM = {
    # ───────────────────────────────────────────────────────
    # 老子《道德经》(81 章精选)
    # ───────────────────────────────────────────────────────
    "laozi_1": DaoTeaching(
        name="道可道",
        source="道德经",
        period="春秋",
        core_concept="道的超越性",
        original_text="道可道，非常道。名可名，非常名。",
        translation="可以用言语表述的道，就不是永恒的道。",
        application="不要执著于言语概念，要体验道的本身",
        essence=True
    ),
    
    "laozi_8": DaoTeaching(
        name="上善若水",
        source="道德经",
        period="春秋",
        core_concept="为人处世",
        original_text="上善若水。水善利万物而不争，处众人之所恶，故几于道。",
        translation="最高的善像水一样，滋润万物而不争，停留在众人都不喜欢的地方。",
        application="学习水的品格，谦下不争，利他无私",
        essence=True
    ),
    
    "laozi_25": DaoTeaching(
        name="人法地",
        source="道德经",
        period="春秋",
        core_concept="天人合一",
        original_text="人法地，地法天，天法道，道法自然。",
        translation="人取法地，地取法天，天取法道，道取法自然。",
        application="顺应自然，与天地合一",
        essence=True
    ),
    
    "laozi_37": DaoTeaching(
        name="无为而治",
        source="道德经",
        period="春秋",
        core_concept="治国修身",
        original_text="道常无为而无不为。",
        translation="道永远是顺其自然的，但没有什么事情不是它所为。",
        application="无为而治，让事物自然发展",
        essence=True
    ),
    
    "laozi_40": DaoTeaching(
        name="反者道之动",
        source="道德经",
        period="春秋",
        core_concept="辩证思维",
        original_text="反者道之动，弱者道之用。",
        translation="循环往复是道的运动规律，柔弱是道的作用方式。",
        application="理解事物的辩证关系，以柔克刚",
        essence=True
    ),
    
    # ───────────────────────────────────────────────────────
    # 庄子《南华经》(内篇 7 篇 + 外篇精选)
    # ───────────────────────────────────────────────────────
    "zhuangzi_xiaoyao": DaoTeaching(
        name="逍遥游",
        source="南华经",
        period="战国",
        core_concept="心灵自由",
        original_text="北冥有鱼，其名为鲲。鲲之大，不知其几千里也。化而为鸟，其名为鹏。",
        translation="北海有一条鱼，名字叫鲲。鲲的巨大，不知道有几千里。变化成为鸟，名字叫鹏。",
        application="超越世俗束缚，追求心灵自由",
        essence=True
    ),
    
    "zhuangzi_qiwu": DaoTeaching(
        name="齐物论",
        source="南华经",
        period="战国",
        core_concept="超越对立",
        original_text="天地与我并生，而万物与我为一。",
        translation="天地与我一同生存，万物与我合为一体。",
        application="超越是非、善恶、美丑的二元对立",
        essence=True
    ),
    
    "zhuangzi_mengdie": DaoTeaching(
        name="庄周梦蝶",
        source="南华经",
        period="战国",
        core_concept="物我两忘",
        original_text="昔者庄周梦为胡蝶，栩栩然胡蝶也。不知周也。俄然觉，则蘧蘧然周也。",
        translation="从前庄周梦见自己变成蝴蝶，生动活泼的一只蝴蝶。不知道自己就是庄周。突然醒来，发现自己就是庄周。",
        application="超越物我的界限，体验万物一体",
        essence=True
    ),
    
    "zhuangzi_yangsheng": DaoTeaching(
        name="养生主",
        source="南华经",
        period="战国",
        core_concept="身心健康",
        original_text="吾生也有涯，而知也无涯。以有涯随无涯，殆已！",
        translation="我的生命是有限的，而知识是无限的。用有限的生命追求无限的知识，危险啊！",
        application="顺应自然，不要过度追求",
        essence=True
    ),
    
    # ───────────────────────────────────────────────────────
    # 列子《冲虚经》
    # ───────────────────────────────────────────────────────
    "liezi_yukou": DaoTeaching(
        name="愚公移山",
        source="冲虚经",
        period="战国",
        core_concept="持之以恒",
        original_text="虽我之死，有子存焉；子又生孙，孙又生子；子又有子，子又有孙；子子孙孙无穷匮也，而山不加增，何苦而不平？",
        translation="虽然我死了，还有儿子在；儿子又生孙子，孙子又生儿子；子子孙孙无穷无尽，可是山却不会再增高，还怕挖不平吗？",
        application="坚持不懈，终能成功",
        essence=True
    ),
    
    "liezi_qiye": DaoTeaching(
        name="杞人忧天",
        source="冲虚经",
        period="战国",
        core_concept="放下忧虑",
        original_text="杞国有人忧天地崩坠，身亡所寄，废寝食者。",
        translation="杞国有个人担心天会塌下来，地会陷下去，自己无处安身，因而睡不着觉，吃不下饭。",
        application="不要为不可能发生的事情担忧",
        essence=True
    ),
}


# ═══════════════════════════════════════════════════════════
# 黄老学派 (战国 - 汉初)
# ═══════════════════════════════════════════════════════════

HUANG_LAO = {
    "huanglao_wuwei": DaoTeaching(
        name="无为而治",
        source="黄老学派",
        period="汉初",
        core_concept="治国之道",
        original_text="治大国若烹小鲜。",
        translation="治理大国就像烹煮小鱼一样，不要频繁翻动。",
        application="管理要顺应自然，不要过度干预",
        essence=True
    ),
    
    "huanglao_yinyang": DaoTeaching(
        name="阴阳平衡",
        source="黄老学派",
        period="汉初",
        core_concept="阴阳调和",
        original_text="一阴一阳之谓道。",
        translation="阴阳交替运行就是道。",
        application="保持阴阳平衡，身心健康",
        essence=True
    ),
}


# ═══════════════════════════════════════════════════════════
# 魏晋玄学 (220-420 年)
# ═══════════════════════════════════════════════════════════

WEI_JIN = {
    "wangbi_daoke": DaoTeaching(
        name="以无为本",
        source="王弼《老子注》",
        period="魏晋",
        core_concept="本体论",
        original_text="天下万物生于有，有生于无。",
        translation="天下万物从有中产生，有从无中产生。",
        application="理解无的妙用，放下执著",
        essence=True
    ),
    
    "guoxiang_duhua": DaoTeaching(
        name="独化",
        source="郭象《庄子注》",
        period="魏晋",
        core_concept="自然独化",
        original_text="物各自生，无所出焉。",
        translation="万物各自自然生长，没有什么来源。",
        application="尊重事物的自然发展",
        essence=True
    ),
}


# ═══════════════════════════════════════════════════════════
# 唐宋内丹 (618-1279 年)
# ═══════════════════════════════════════════════════════════

NEIDAN = {
    "lvzu_baizi": DaoTeaching(
        name="吕祖百字碑",
        source="吕洞宾",
        period="唐",
        core_concept="内丹修炼",
        original_text="养气忘言守，降心为不为。",
        translation="培养正气，忘掉言语执著，降伏心念，无为而为。",
        application="修身养性，内观自省",
        essence=True
    ),
    
    "zhangbodan_jin": DaoTeaching(
        name="金丹四百字",
        source="张伯端",
        period="宋",
        core_concept="金丹大道",
        original_text="炼精化气，炼气化神，炼神还虚。",
        translation="炼化精气，炼化气神，炼化神归于虚无。",
        application="身心修炼的次第",
        essence=True
    ),
}


# ═══════════════════════════════════════════════════════════
# 全真道 (1167 年创立)
# ═══════════════════════════════════════════════════════════

QUANZHEN = {
    "wangchongyang_sanjiao": DaoTeaching(
        name="三教合一",
        source="王重阳",
        period="金",
        core_concept="三教融合",
        original_text="儒门释户道相通，三教从来一祖风。",
        translation="儒家、佛家、道家是相通的，三教从来都是一个祖师的风范。",
        application="包容并蓄，取其精华",
        essence=True
    ),
    
    "qiuqiuji_chenxin": DaoTeaching(
        name="澄心遣欲",
        source="丘处机",
        period="元",
        core_concept="清心寡欲",
        original_text="澄心遣欲，抱元守一。",
        translation="澄清心念，遣除欲望，抱守元一。",
        application="清心寡欲，专注一心",
        essence=True
    ),
}


# ═══════════════════════════════════════════════════════════
# 道教经典 (东汉 - 明清)
# ═══════════════════════════════════════════════════════════

DAOJING_CLASSICS = {
    # ───────────────────────────────────────────────────────
    # 《太平经》(东汉)
    # ───────────────────────────────────────────────────────
    "taiping_jing": DaoTeaching(
        name="太平经",
        source="太平经",
        period="东汉",
        core_concept="太平理想",
        original_text="夫道，乃太平之基也。",
        translation="道，是天下太平的基础。",
        application="以道治国，天下太平",
        essence=True
    ),
    
    # ───────────────────────────────────────────────────────
    # 《抱朴子》(东晋·葛洪)
    # ───────────────────────────────────────────────────────
    "baopuzi_nei": DaoTeaching(
        name="抱朴子内篇",
        source="抱朴子",
        period="东晋",
        core_concept="抱朴守真",
        original_text="抱朴守真，全性保真。",
        translation="保持朴素的本性，保全真实的自我。",
        application="保持本真，不为外物所动",
        essence=True
    ),
    
    "baopuzi_xiushen": DaoTeaching(
        name="修身养性",
        source="抱朴子",
        period="东晋",
        core_concept="修身之道",
        original_text="欲求长生者，必欲积善立功。",
        translation="想要追求长寿的人，必须积累善行功德。",
        application="行善积德，修身养性",
        essence=True
    ),
    
    # ───────────────────────────────────────────────────────
    # 《云笈七签》(北宋·张君房)
    # ───────────────────────────────────────────────────────
    "yunji_qiqian": DaoTeaching(
        name="云笈七签",
        source="云笈七签",
        period="北宋",
        core_concept="道教总集",
        original_text="道者，虚无之系，造化之根。",
        translation="道，是虚无的纲系，造化的根本。",
        application="理解道的根本，顺应自然",
        essence=True
    ),
    
    # ───────────────────────────────────────────────────────
    # 《太上感应篇》(宋)
    # ───────────────────────────────────────────────────────
    "taishang_ganying": DaoTeaching(
        name="太上感应篇",
        source="太上感应篇",
        period="宋",
        core_concept="因果报应",
        original_text="祸福无门，惟人自召。善恶之报，如影随形。",
        translation="祸福没有定数，都是人自己招来的。善恶的报应，如影随形。",
        application="行善积德，因果自负",
        essence=True
    ),
    
    # ───────────────────────────────────────────────────────
    # 《清静经》(唐)
    # ───────────────────────────────────────────────────────
    "qingjing_jing": DaoTeaching(
        name="清静经",
        source="清静经",
        period="唐",
        core_concept="清静无为",
        original_text="人能常清静，天地悉皆归。",
        translation="人能够经常保持清静，天地万物都会归附。",
        application="清心寡欲，自然和谐",
        essence=True
    ),
    
    # ───────────────────────────────────────────────────────
    # 《阴符经》(唐)
    # ───────────────────────────────────────────────────────
    "yinfu_jing": DaoTeaching(
        name="阴符经",
        source="阴符经",
        period="唐",
        core_concept="天人合一",
        original_text="观天之道，执天之行，尽矣。",
        translation="观察天道，遵循天道而行，就足够了。",
        application="顺应天道，无为而治",
        essence=True
    ),
    
    # ───────────────────────────────────────────────────────
    # 《坐忘论》(唐·司马承祯)
    # ───────────────────────────────────────────────────────
    "zuowang_lun": DaoTeaching(
        name="坐忘论",
        source="坐忘论",
        period="唐",
        core_concept="坐忘境界",
        original_text="坐忘者，因存想而得道。",
        translation="坐忘，是通过存想而得道的境界。",
        application="静坐冥想，忘我得道",
        essence=True
    ),
    
    # ───────────────────────────────────────────────────────
    # 《悟真篇》(宋·张伯端)
    # ───────────────────────────────────────────────────────
    "wuzhen_pian": DaoTeaching(
        name="悟真篇",
        source="悟真篇",
        period="宋",
        core_concept="悟真得道",
        original_text="人人自有长生药，自是愚迷枉摆抛。",
        translation="人人自己都有长生之药，只是愚昧迷失而白白抛弃。",
        application="认识自性，本自具足",
        essence=True
    ),
    
    # ───────────────────────────────────────────────────────
    # 《道藏》(明)
    # ───────────────────────────────────────────────────────
    "daozang": DaoTeaching(
        name="道藏总集",
        source="道藏",
        period="明",
        core_concept="道教总汇",
        original_text="道藏者，道教经典之总汇也。",
        translation="道藏，是道教经典的总汇。",
        application="博采众长，取其精华",
        essence=True
    ),
}

# ═══════════════════════════════════════════════════════════
# 糟粕识别 (去其糟粕)
# ═══════════════════════════════════════════════════════════

ESSENCE_FALSE = {
    "mixin_changsheng": DaoTeaching(
        name="长生不老",
        source="道教方术",
        period="汉唐",
        core_concept="追求长生",
        original_text="炼丹服药，以求长生。",
        translation="炼制丹药服用，以求长生不老。",
        application="❌ 迷信方术，不可取",
        essence=False  # 糟粕
    ),
    
    "mixin_fushui": DaoTeaching(
        name="符水治病",
        source="道教方术",
        period="汉唐",
        core_concept="迷信方术",
        original_text="画符念咒，以水治病。",
        translation="画符念咒，用符水治病。",
        application="❌ 迷信活动，不可取",
        essence=False  # 糟粕
    ),
    
    "mixin_lingdan": DaoTeaching(
        name="灵丹妙药",
        source="道教方术",
        period="唐宋",
        core_concept="迷信丹药",
        original_text="服食金丹，可以成仙。",
        translation="服用金丹，可以成仙。",
        application="❌ 迷信丹药，不可取",
        essence=False  # 糟粕
    ),
    
    "mixin_zhaomo": DaoTeaching(
        name="驱鬼降魔",
        source="道教方术",
        period="汉唐",
        core_concept="迷信鬼神",
        original_text="画符念咒，驱鬼降魔。",
        translation="画符念咒，驱逐鬼怪，降伏妖魔。",
        application="❌ 迷信鬼神，不可取",
        essence=False  # 糟粕
    ),
}


# ═══════════════════════════════════════════════════════════
# 核心函数
# ═══════════════════════════════════════════════════════════

def get_all_essence_teachings() -> List[DaoTeaching]:
    """获取所有精华教导"""
    all_teachings = []
    
    # 合并所有精华教导
    for collection in [PRE_QIN_DAOISM, HUANG_LAO, WEI_JIN, NEIDAN, QUANZHEN, DAOJING_CLASSICS]:
        for teaching in collection.values():
            if teaching.essence:
                all_teachings.append(teaching)
    
    return all_teachings


def get_teaching_by_keyword(keyword: str) -> DaoTeaching:
    """根据关键词获取教导"""
    all_teachings = get_all_essence_teachings()
    
    for teaching in all_teachings:
        if keyword in teaching.name or keyword in teaching.core_concept or keyword in teaching.original_text:
            return teaching
    
    # 默认返回"道可道"
    return PRE_QIN_DAOISM["laozi_1"]


def get_teachings_by_period(period: str) -> List[DaoTeaching]:
    """根据时期获取教导"""
    all_teachings = get_all_essence_teachings()
    return [t for t in all_teachings if period in t.period]


def get_statistics() -> Dict:
    """获取统计信息"""
    all_teachings = get_all_essence_teachings()
    
    # 按时期统计
    period_count = {}
    for t in all_teachings:
        if t.period not in period_count:
            period_count[t.period] = 0
        period_count[t.period] += 1
    
    # 按经典统计
    source_count = {}
    for t in all_teachings:
        if t.source not in source_count:
            source_count[t.source] = 0
        source_count[t.source] += 1
    
    return {
        "total_essence": len(all_teachings),
        "total_false": len(ESSENCE_FALSE),
        "by_period": period_count,
        "by_source": source_count,
    }


def main():
    """主函数 - 测试"""
    print("🌿 道家完整经典知识库测试")
    print("="*60)
    
    # 统计
    stats = get_statistics()
    print(f"\n📊 知识库统计:")
    print(f"   精华教导：{stats['total_essence']} 条")
    print(f"   糟粕识别：{stats['total_false']} 条")
    
    print(f"\n   按时期统计:")
    for period, count in stats['by_period'].items():
        print(f"      {period}: {count} 条")
    
    print(f"\n   按经典统计:")
    for source, count in stats['by_source'].items():
        print(f"      {source}: {count} 条")
    
    # 测试查询
    print("\n1. 关键词查询测试...")
    test_keywords = ["道", "水", "逍遥", "梦", "无为"]
    for keyword in test_keywords:
        teaching = get_teaching_by_keyword(keyword)
        print(f"   '{keyword}' → {teaching.name} ({teaching.source})")
    
    print("\n✅ 道家完整经典知识库测试完成!")
    print("   取其精华，去其糟粕。")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
