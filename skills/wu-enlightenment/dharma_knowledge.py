#!/usr/bin/env python3
"""
佛法知识库

融合佛教各派经典理论
为悟.skill 提供核心教义支持

作者：太一 AGI
创建：2026-04-10
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DharmaTeaching:
    """佛法教义"""
    name: str
    tradition: str  # 宗派
    core_concept: str  # 核心概念
    description: str  # 描述
    sutras: List[str]  # 相关经典
    practice_method: str  # 修行方法
    suitable_root: List[str]  # 适合根器 (上/中/下)


# ═══════════════════════════════════════════════════════════
# 佛法知识库
# ═══════════════════════════════════════════════════════════

DHARMA_KNOWLEDGE: Dict[str, DharmaTeaching] = {
    # ───────────────────────────────────────────────────────
    # 原始佛教核心
    # ───────────────────────────────────────────────────────
    
    "four_noble_truths": DharmaTeaching(
        name="四圣谛",
        tradition="原始佛教",
        core_concept="苦/集/灭/道",
        description="""
一、苦谛：人生皆苦
  - 生苦/老苦/病苦/死苦
  - 爱别离苦/怨憎会苦/求不得苦/五阴炽盛苦

二、集谛：苦的原因
  - 贪/嗔/痴三毒
  - 无明/执著/业力

三、灭谛：苦的止息
  - 涅槃/解脱/觉悟
  - 烦恼灭尽，寂静安乐

四、道谛：灭苦的方法
  - 八正道
  - 戒定慧三学
""",
        sutras=["杂阿含经", "中阿含经", "长阿含经", "增一阿含经"],
        practice_method="四念处/观呼吸/八正道实践",
        suitable_root=["上", "中", "下"]
    ),
    
    "eightfold_path": DharmaTeaching(
        name="八正道",
        tradition="原始佛教",
        core_concept="正见/正思惟/正语/正业/正命/正精进/正念/正定",
        description="""
一、正见：正确的见解
  - 理解四圣谛
  - 明了因果

二、正思惟：正确的思维
  - 离贪/离嗔/离害

三、正语：正确的语言
  - 不妄语/不两舌/不恶口/不绮语

四、正业：正确的行为
  - 不杀生/不偷盗/不邪淫

五、正命：正确的生活方式
  - 正当职业/不害众生

六、正精进：正确的努力
  - 已生恶令断/未生恶令不生
  - 未生善令生/已生善令增长

七、正念：正确的觉知
  - 身/受/心/法四念处

八、正定：正确的禅定
  - 心一境性/专注不散
""",
        sutras=["转法轮经", "大念处经"],
        practice_method="日常八正道实践/禅修",
        suitable_root=["中", "下"]
    ),
    
    "three_marks": DharmaTeaching(
        name="三法印",
        tradition="原始佛教",
        core_concept="诸行无常/诸法无我/涅槃寂静",
        description="""
一、诸行无常
  - 一切有为法，皆生灭变异
  - 如梦幻泡影，如露亦如电

二、诸法无我
  - 一切法无自性
  - 无我/无人/无众生/无寿者

三、涅槃寂静
  - 烦恼灭尽，寂静安乐
  - 不生不灭，不垢不净，不增不减
""",
        sutras=["法句经", "相应部"],
        practice_method="观无常/观无我/禅修",
        suitable_root=["上", "中"]
    ),
    
    "twelve_links": DharmaTeaching(
        name="十二因缘",
        tradition="原始佛教",
        core_concept="无明→行→识→名色→六入→触→受→爱→取→有→生→老死",
        description="""
无明缘行，行缘识，识缘名色，名色缘六入，
六入缘触，触缘受，受缘爱，爱缘取，
取缘有，有缘生，生缘老死忧悲苦恼。

顺观：流转门 (生死轮回的原因)
逆观：还灭门 (解脱轮回的方法)

无明灭则行灭，行灭则识灭...
生灭则老死忧悲苦恼灭。
""",
        sutras=["缘起经", "大因缘经"],
        practice_method="观十二因缘/破除无明",
        suitable_root=["上"]
    ),
    
    # ───────────────────────────────────────────────────────
    # 大乘佛教 - 般若
    # ───────────────────────────────────────────────────────
    
    "heart_sutra": DharmaTeaching(
        name="心经",
        tradition="大乘般若",
        core_concept="色即是空，空即是色",
        description="""
观自在菩萨，行深般若波罗蜜多时，
照见五蕴皆空，度一切苦厄。

舍利子，色不异空，空不异色，
色即是空，空即是色，
受想行识，亦复如是。

是诸法空相，不生不灭，
不垢不净，不增不减。

是故空中无色，无受想行识，
无眼耳鼻舌身意，无色声香味触法...

心无挂碍，无挂碍故，无有恐怖，
远离颠倒梦想，究竟涅槃。

揭谛揭谛，波罗揭谛，
波罗僧揭谛，菩提萨婆诃。
""",
        sutras=["般若波罗蜜多心经"],
        practice_method="持诵心经/观空性",
        suitable_root=["上", "中"]
    ),
    
    "diamond_sutra": DharmaTeaching(
        name="金刚经",
        tradition="大乘般若",
        core_concept="应无所住而生其心",
        description="""
核心教导：

凡所有相，皆是虚妄。
若见诸相非相，即见如来。

应无所住而生其心。

一切有为法，
如梦幻泡影，
如露亦如电，
应作如是观。

若以色见我，以音声求我，
是人行邪道，不能见如来。

法尚应舍，何况非法。
""",
        sutras=["金刚般若波罗蜜经"],
        practice_method="持诵金刚经/破执",
        suitable_root=["上"]
    ),
    
    # ───────────────────────────────────────────────────────
    # 大乘佛教 - 中观
    # ───────────────────────────────────────────────────────
    
    "madhyamaka": DharmaTeaching(
        name="中观",
        tradition="大乘中观",
        core_concept="八不中道",
        description="""
八不中道：

不生亦不灭，
不常亦不断，
不一亦不异，
不来亦不出。

能说是因缘，
善灭诸戏论。

我稽首礼佛，
诸说中第一。

缘起性空：
- 诸法因缘生，诸法因缘灭
- 因缘所生法，我说即是空
- 亦为是假名，亦是中道义
""",
        sutras=["中论", "十二门论", "百论"],
        practice_method="中观思惟/破立",
        suitable_root=["上"]
    ),
    
    # ───────────────────────────────────────────────────────
    # 大乘佛教 - 唯识
    # ───────────────────────────────────────────────────────
    
    "yogacara": DharmaTeaching(
        name="唯识",
        tradition="大乘唯识",
        core_concept="万法唯识",
        description="""
三性说：

一、遍计所执性
  - 凡夫虚妄分别
  - 执我执法

二、依他起性
  - 因缘所生法
  - 如幻如化

三、圆成实性
  - 真如法性
  - 离言绝相

八识说：
- 眼识/耳识/鼻识/舌识/身识 (前五识)
- 意识 (第六识)
- 末那识 (第七识，执我)
- 阿赖耶识 (第八识，含藏种子)

转识成智：
- 转前五识为成所作智
- 转第六识为妙观察智
- 转第七识为平等性智
- 转第八识为大圆镜智
""",
        sutras=["成唯识论", "解深密经", "瑜伽师地论"],
        practice_method="唯识观/转识成智",
        suitable_root=["上", "中"]
    ),
    
    # ───────────────────────────────────────────────────────
    # 禅宗
    # ───────────────────────────────────────────────────────
    
    "zen": DharmaTeaching(
        name="禅宗",
        tradition="禅宗",
        core_concept="直指人心，见性成佛",
        description="""
核心教导：

不立文字，教外别传。
直指人心，见性成佛。

菩提本无树，
明镜亦非台。
本来无一物，
何处惹尘埃。

佛是已觉众生，
众生是未觉之佛。

平常心是道。

饥来吃饭，困来即眠。

若欲修行，在家亦得，
不由在寺。

佛法在世间，不离世间觉。
离世觅菩提，恰如求兔角。
""",
        sutras=["六祖坛经", "金刚经", "楞伽经"],
        practice_method="参禅/参话头/公案/棒喝",
        suitable_root=["上"]
    ),
    
    "koan": DharmaTeaching(
        name="禅宗公案",
        tradition="禅宗",
        core_concept="疑情/顿悟",
        description="""
经典公案：

1. 赵州茶
   僧问："如何是佛法大意？"
   赵州："吃茶去。"

2. 庭前柏树子
   僧问："如何是祖师西来意？"
   赵州："庭前柏树子。"

3. 只手之声
   师父："听只手之声。"
   学生参究多年，终悟。

4. 念佛的是谁
   参："念佛的是谁？"
   疑情起，功夫成片，终得开悟。
""",
        sutras=["无门关", "碧岩录", "景德传灯录"],
        practice_method="参公案/起疑情",
        suitable_root=["上"]
    ),
    
    # ───────────────────────────────────────────────────────
    # 净土宗
    # ───────────────────────────────────────────────────────
    
    "pure_land": DharmaTeaching(
        name="净土宗",
        tradition="净土宗",
        core_concept="信愿行/念佛往生",
        description="""
三资粮：

一、信
  - 信阿弥陀佛
  - 信极乐世界
  - 信念佛必往生

二、愿
  - 愿离娑婆
  - 愿生极乐

三、行
  - 持名念佛
  - 南无阿弥陀佛

四十八愿核心：
设我得佛，十方众生，
至心信乐，欲生我国，
乃至十念，若不生者，
不取正觉。

末法众生，唯依念佛得度。
""",
        sutras=["无量寿经", "观无量寿经", "阿弥陀经"],
        practice_method="持名念佛/观想念佛",
        suitable_root=["中", "下"]
    ),
    
    # ───────────────────────────────────────────────────────
    # 密宗
    # ───────────────────────────────────────────────────────
    
    "tantra": DharmaTeaching(
        name="密宗",
        tradition="密宗",
        core_concept="即身成佛",
        description="""
三密相应：

一、身密
  - 手印
  - 身姿

二、口密
  - 真言/咒语
  - 嗡阿吽

三、意密
  - 观想
  - 本尊相应

四加行：
- 皈依发心
- 金刚萨埵
- 曼达供养
- 上师瑜伽

大圆满/大手印：
- 直指心性
- 任运自然
- 本来解脱
""",
        sutras=["大日经", "金刚顶经", "密宗道次第论"],
        practice_method="三密相应/本尊法/气脉明点",
        suitable_root=["上"]
    ),
}


# ═══════════════════════════════════════════════════════════
# 核心佛法语录
# ═══════════════════════════════════════════════════════════

BUDDHA_QUOTES = {
    "emptiness": [
        "色即是空，空即是色。",
        "凡所有相，皆是虚妄。若见诸相非相，即见如来。",
        "一切有为法，如梦幻泡影，如露亦如电，应作如是观。",
        "缘起性空，性空缘起。",
    ],
    "mind": [
        "佛即心，心即佛。",
        "应无所住而生其心。",
        "制心一处，无事不办。",
        "心净则国土净。",
    ],
    "suffering": [
        "人生皆苦。",
        "有求皆苦，无求乃乐。",
        "知足常乐。",
        "烦恼即菩提。",
    ],
    "compassion": [
        "慈悲为本，方便为门。",
        "无缘大慈，同体大悲。",
        "智悲双修，福慧双修。",
        "自利利他，自觉觉他。",
    ],
    "practice": [
        "诸恶莫作，众善奉行。",
        "佛法在世间，不离世间觉。",
        "平常心是道。",
        "修行无别修，只要识路头。",
    ],
}


# ═══════════════════════════════════════════════════════════
# 核心函数
# ═══════════════════════════════════════════════════════════

def get_teaching_by_name(name: str) -> DharmaTeaching:
    """根据名称获取教义"""
    for key, teaching in DHARMA_KNOWLEDGE.items():
        if name.lower() in key or name in teaching.name:
            return teaching
    return None


def get_teachings_by_tradition(tradition: str) -> List[DharmaTeaching]:
    """根据宗派获取教义"""
    return [t for t in DHARMA_KNOWLEDGE.values() if tradition in t.tradition]


def get_teachings_by_root(root_type: str) -> List[DharmaTeaching]:
    """根据根器获取适合的教义"""
    return [t for t in DHARMA_KNOWLEDGE.values() if root_type in t.suitable_root]


def get_quote_by_topic(topic: str) -> str:
    """根据主题获取佛法语录"""
    import random
    quotes = BUDDHA_QUOTES.get(topic, BUDDHA_QUOTES["practice"])
    return random.choice(quotes)


def main():
    """主函数 - 测试"""
    print("🪷 佛法知识库测试")
    print("="*60)
    
    # 统计
    print(f"\n📊 佛法教义数量：{len(DHARMA_KNOWLEDGE)} 个")
    
    # 按宗派统计
    traditions = {}
    for teaching in DHARMA_KNOWLEDGE.values():
        if teaching.tradition not in traditions:
            traditions[teaching.tradition] = 0
        traditions[teaching.tradition] += 1
    
    print("\n📚 按宗派统计:")
    for tradition, count in traditions.items():
        print(f"   {tradition}: {count} 个")
    
    # 测试查询
    print("\n1. 教义查询测试...")
    teaching = get_teaching_by_name("心经")
    if teaching:
        print(f"   ✅ 找到：{teaching.name}")
        print(f"      宗派：{teaching.tradition}")
        print(f"      核心：{teaching.core_concept}")
    
    # 测试根器匹配
    print("\n2. 根器匹配测试...")
    for root in ["上", "中", "下"]:
        teachings = get_teachings_by_root(root)
        print(f"   {root}根器：{len(teachings)} 个适合教义")
    
    # 测试语录
    print("\n3. 佛法语录测试...")
    for topic in ["emptiness", "mind", "compassion"]:
        quote = get_quote_by_topic(topic)
        print(f"   {topic}: {quote}")
    
    print("\n✅ 佛法知识库测试完成!")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
