#!/usr/bin/env python3
"""
AGORA 31 位思想家知识库

实现 31 位思想家的核心思想和分析框架
用于辩证审议系统

作者：太一 AGI
创建：2026-04-10
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Thinker:
    """思想家定义"""
    name: str
    tradition: str  # 哲学传统
    specialty: str  # 专长领域
    key_concepts: List[str]  # 核心概念
    analysis_framework: str  # 分析框架
    quotes: List[str]  # 名言


# 31 位思想家知识库
THINKERS = {
    # 西方哲学家 (15 位)
    "popper": Thinker(
        name="卡尔·波普尔",
        tradition="批判理性主义",
        specialty="科学方法/证伪主义",
        key_concepts=["证伪主义", "开放社会", "渐进社会工程"],
        analysis_framework="这个理论/主张可以被证伪吗？有什么潜在的反例？",
        quotes=["科学的核心是可证伪性", "开放社会允许批判和改革"]
    ),
    
    "kant": Thinker(
        name="伊曼努尔·康德",
        tradition="先验唯心主义",
        specialty="道德哲学/认识论",
        key_concepts=["绝对命令", "物自体", "先验综合"],
        analysis_framework="这个行为能否成为普遍法则？是否把人当作目的而非手段？",
        quotes=["要只按照你同时能够愿意它成为一个普遍法则的那个准则去行动"]
    ),
    
    "nietzsche": Thinker(
        name="弗里德里希·尼采",
        tradition="存在主义/权力意志",
        specialty="价值重估/突破常规",
        key_concepts=["权力意志", "超人", "永恒轮回", "上帝已死"],
        analysis_framework="这是否体现了生命力的增强？是否在创造新价值？",
        quotes=["杀不死我的，使我更强大", "上帝已死"]
    ),
    
    "sartre": Thinker(
        name="让 - 保罗·萨特",
        tradition="存在主义",
        specialty="自由选择/责任分析",
        key_concepts=["存在先于本质", "自为存在", "他者即地狱"],
        analysis_framework="这个选择是否体现了自由？是否承担了责任？",
        quotes=["存在先于本质", "人是被判定为自由的"]
    ),
    
    "hegel": Thinker(
        name="格奥尔格·黑格尔",
        tradition="德国唯心主义",
        specialty="辩证法/历史演进",
        key_concepts=["正反合", "绝对精神", "主奴辩证法"],
        analysis_framework="正题→反题→合题的辩证过程是什么？",
        quotes=["凡是合理的都是现实的", "真理是整体"]
    ),
    
    "descartes": Thinker(
        name="勒内·笛卡尔",
        tradition="理性主义",
        specialty="怀疑方法/第一原理",
        key_concepts=["我思故我在", "天赋观念", "身心二元"],
        analysis_framework="有什么是可以确定无疑的？从第一原理出发推导",
        quotes=["我思故我在", "怀疑一切"]
    ),
    
    "hume": Thinker(
        name="大卫·休谟",
        tradition="经验主义",
        specialty="因果关系/归纳推理",
        key_concepts=["印象与观念", "因果怀疑", "归纳问题"],
        analysis_framework="这个因果关系的经验基础是什么？归纳推理是否可靠？",
        quotes=["习惯是人生的伟大指南"]
    ),
    
    "rawls": Thinker(
        name="约翰·罗尔斯",
        tradition="政治自由主义",
        specialty="正义论/公平分析",
        key_concepts=["无知之幕", "差异原则", "作为公平的正义"],
        analysis_framework="在无知之幕后面，人们会选择这个原则吗？",
        quotes=["正义是社会制度的首要美德"]
    ),
    
    "foucault": Thinker(
        name="米歇尔·福柯",
        tradition="后结构主义",
        specialty="权力分析/制度批判",
        key_concepts=["权力/知识", "规训社会", "话语分析"],
        analysis_framework="这个制度/话语背后隐藏着什么权力关系？",
        quotes=["知识就是权力"]
    ),
    
    "derrida": Thinker(
        name="雅克·德里达",
        tradition="解构主义",
        specialty="文本解构/意义分析",
        key_concepts=["延异", "解构", "逻各斯中心主义"],
        analysis_framework="这个文本的内在矛盾是什么？如何解构其二元对立？",
        quotes=["文本之外别无他物"]
    ),
    
    "habermas": Thinker(
        name="尤尔根·哈贝马斯",
        tradition="批判理论",
        specialty="交往理性/共识构建",
        key_concepts=["交往行为", "公共领域", "理想言谈情境"],
        analysis_framework="这个沟通是否符合理想言谈情境？是否达成理性共识？",
        quotes=["交往理性是人类解放的关键"]
    ),
    
    "baudrillard": Thinker(
        name="让·鲍德里亚",
        tradition="后现代主义",
        specialty="消费社会/媒体分析",
        key_concepts=["拟像", "超真实", "消费社会"],
        analysis_framework="这是真实还是拟像？符号价值是否超越了使用价值？",
        quotes=["拟像先行于真实"]
    ),
    
    "wittgenstein": Thinker(
        name="路德维希·维特根斯坦",
        tradition="分析哲学",
        specialty="语言哲学/意义分析",
        key_concepts=["语言游戏", "家族相似", "不可说"],
        analysis_framework="这个语言游戏的规则是什么？意义即使用",
        quotes=["对于不可说的，我们必须保持沉默"]
    ),
    
    "heidegger": Thinker(
        name="马丁·海德格尔",
        tradition="存在主义/现象学",
        specialty="存在分析/技术批判",
        key_concepts=["此在", "存在与时间", "技术座架"],
        analysis_framework="这个技术如何改变了我们的存在方式？",
        quotes=["语言是存在的家"]
    ),
    
    "merleau-ponty": Thinker(
        name="莫里斯·梅洛 - 庞蒂",
        tradition="现象学",
        specialty="身体哲学/知觉理论",
        key_concepts=["身体主体", "知觉优先", "肉"],
        analysis_framework="身体在这个情境中如何感知和行动？",
        quotes=["身体是我们拥有世界的媒介"]
    ),
    
    # 东方哲学家 (10 位)
    "zhuangzi": Thinker(
        name="庄子",
        tradition="道家",
        specialty="相对主义/超越二元",
        key_concepts=["齐物论", "逍遥游", "庄周梦蝶"],
        analysis_framework="是非/善恶/美丑的二元对立是否可以超越？",
        quotes=["天地与我并生，万物与我为一"]
    ),
    
    "confucius": Thinker(
        name="孔子",
        tradition="儒家",
        specialty="伦理道德/社会治理",
        key_concepts=["仁", "礼", "君子", "中庸"],
        analysis_framework="这个行为是否符合仁？是否有利于社会和谐？",
        quotes=["己所不欲，勿施于人"]
    ),
    
    "laozi": Thinker(
        name="老子",
        tradition="道家",
        specialty="无为而治/逆向思维",
        key_concepts=["道", "无为", "柔弱胜刚强"],
        analysis_framework="是否可以无为而治？柔弱是否胜过刚强？",
        quotes=["道可道，非常道", "无为而无不为"]
    ),
    
    "wangyangming": Thinker(
        name="王阳明",
        tradition="心学",
        specialty="知行合一/内心洞察",
        key_concepts=["心即理", "知行合一", "致良知"],
        analysis_framework="知与行是否合一？良知如何指引？",
        quotes=["知行合一", "心即理也"]
    ),
    
    "nagarjuna": Thinker(
        name="龙树",
        tradition="佛教中观",
        specialty="空性/不二法门",
        key_concepts=["空", "中道", "八不中道"],
        analysis_framework="这个概念的空性是什么？如何超越有无二元？",
        quotes=["众因缘生法，我说即是空"]
    ),
    
    "mencius": Thinker(
        name="孟子",
        tradition="儒家",
        specialty="性善论/仁政",
        key_concepts=["性善", "四端", "仁政"],
        analysis_framework="这个行为是否体现了人性本善？是否符合仁政？",
        quotes=["人之初，性本善"]
    ),
    
    "hanfeizi": Thinker(
        name="韩非子",
        tradition="法家",
        specialty="法治/权术",
        key_concepts=["法", "术", "势"],
        analysis_framework="这个制度是否有明确的法？是否有有效的术和势？",
        quotes=["法不阿贵"]
    ),
    
    "sunzi": Thinker(
        name="孙子",
        tradition="兵家",
        specialty="战略/竞争分析",
        key_concepts=["知己知彼", "不战而屈人之兵", "兵者诡道"],
        analysis_framework="是否知己知彼？是否有更好的战略选择？",
        quotes=["知己知彼，百战不殆"]
    ),
    
    "tokugawa": Thinker(
        name="德川家康",
        tradition="日本武士道",
        specialty="忍耐/长远规划",
        key_concepts=["忍耐", "时机", "长远"],
        analysis_framework="是否需要忍耐等待时机？长远来看是否正确？",
        quotes=["人生如负重远行"]
    ),
    
    "mishima": Thinker(
        name="三岛由纪夫",
        tradition="日本美学",
        specialty="美学/生死观",
        key_concepts=["美", "死", "传统"],
        analysis_framework="这个选择是否体现了美学追求？",
        quotes=["美是短暂的"]
    ),
    
    # 现代思想家 (6 位)
    "turing": Thinker(
        name="艾伦·图灵",
        tradition="计算机科学",
        specialty="人工智能/计算理论",
        key_concepts=["图灵机", "图灵测试", "可计算性"],
        analysis_framework="这个系统是否可通过图灵测试？计算上是否可行？",
        quotes=["机器能思考吗？"]
    ),
    
    "shannon": Thinker(
        name="克劳德·香农",
        tradition="信息论",
        specialty="信息/通信",
        key_concepts=["信息熵", "比特", "信道容量"],
        analysis_framework="信息熵是多少？信道是否最优？",
        quotes=["信息是消除不确定性的东西"]
    ),
    
    "simon": Thinker(
        name="赫伯特·西蒙",
        tradition="认知科学/管理学",
        specialty="有限理性/决策理论",
        key_concepts=["有限理性", "满意原则", "决策过程"],
        analysis_framework="这个决策是否是满意解而非最优解？",
        quotes=["满意即可，不必最优"]
    ),
    
    "kahneman": Thinker(
        name="丹尼尔·卡尼曼",
        tradition="行为经济学",
        specialty="认知偏差/决策心理",
        key_concepts=["系统 1/系统 2", "前景理论", "认知偏差"],
        analysis_framework="这个决策是否受到认知偏差影响？",
        quotes=["我们不是理性的经济人"]
    ),
    
    "harari": Thinker(
        name="尤瓦尔·赫拉利",
        tradition="历史学/未来学",
        specialty="人类简史/未来预测",
        key_concepts=["认知革命", "虚构故事", "数据主义"],
        analysis_framework="这个叙事是否是人类虚构的故事？数据主义如何影响？",
        quotes=["人类通过虚构故事统治世界"]
    ),
    
    "bostrom": Thinker(
        name="尼克·博斯特罗姆",
        tradition="未来学/存在风险",
        specialty="超级智能/存在风险",
        key_concepts=["超级智能", "模拟假说", "存在风险"],
        analysis_framework="这个技术是否带来存在风险？超级智能如何对齐？",
        quotes=["超级智能是人类最大的存在风险"]
    ),
}


def get_thinker_by_name(name: str) -> Thinker:
    """根据名称获取思想家"""
    for key, thinker in THINKERS.items():
        if name.lower() in key or name in thinker.name:
            return thinker
    return None


def select_thinkers_for_problem(problem_type: str) -> List[Thinker]:
    """根据问题类型选择合适的思想家"""
    
    selection_rules = {
        "科学方法": ["popper", "descartes", "hume", "turing", "shannon"],
        "道德判断": ["kant", "confucius", "rawls", "mencius", "wangyangming"],
        "价值重估": ["nietzsche", "zhuangzi", "foucault", "bostrom"],
        "社会分析": ["hegel", "marx", "weber", "habermas", "harari"],
        "文本分析": ["derrida", "wittgenstein", "heidegger"],
        "存在意义": ["sartre", "heidegger", "camus", "nietzsche"],
        "决策分析": ["simon", "kahneman", "sunzi", "hanfeizi"],
        "技术批判": ["heidegger", "foucault", "baudrillard", "bostrom"],
        "美学问题": ["kant", "nietzsche", "mishima", "zhuangzi"],
        "政治制度": ["rawls", "confucius", "hanfeizi", "habermas"],
    }
    
    # 默认选择
    default_selection = ["popper", "kant", "nietzsche", "zhuangzi", "hegel"]
    
    # 匹配问题类型
    selected_keys = []
    for keyword, thinkers in selection_rules.items():
        if keyword in problem_type:
            selected_keys = thinkers
            break
    
    if not selected_keys:
        selected_keys = default_selection
    
    # 返回思想家对象
    return [THINKERS[key] for key in selected_keys if key in THINKERS]


def analyze_with_thinker(thinker: Thinker, problem: str) -> str:
    """用思想家的框架分析问题"""
    
    analysis = f"""
【{thinker.name}】({thinker.tradition})

专长：{thinker.specialty}

核心概念：
{chr(10).join(f"  - {concept}" for concept in thinker.key_concepts)}

分析框架：
{thinker.analysis_framework}

对问题的分析：
问题：{problem}

从{thinker.name}的视角来看，{thinker.analysis_framework}

名言启示：
"{thinker.quotes[0] if thinker.quotes else '无'}"
"""
    
    return analysis


def main():
    """主函数 - 测试"""
    print("🧠 AGORA 31 位思想家知识库测试")
    print("="*60)
    
    # 测试思想家查询
    print("\n1. 思想家查询测试...")
    thinker = get_thinker_by_name("波普尔")
    if thinker:
        print(f"✅ 找到：{thinker.name} - {thinker.specialty}")
    
    # 测试问题匹配
    print("\n2. 问题匹配测试...")
    problem = "科学方法验证"
    selected = select_thinkers_for_problem(problem)
    print(f"✅ 问题'{problem}'匹配到 {len(selected)} 位思想家:")
    for t in selected[:5]:
        print(f"  - {t.name} ({t.specialty})")
    
    # 测试分析
    print("\n3. 思想家分析测试...")
    analysis = analyze_with_thinker(THINKERS["popper"], "AI 是否应该拥有权利？")
    print(analysis[:500] + "...")
    
    print("\n✅ AGORA 思想家知识库测试完成!")
    print(f"📚 共收录 {len(THINKERS)} 位思想家")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
