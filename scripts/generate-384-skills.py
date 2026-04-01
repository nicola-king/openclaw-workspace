#!/usr/bin/env python3
"""
384 Skills 批量生成脚本
64 状态 × 6 阶段 = 384 Skills
"""

import json
from pathlib import Path
from datetime import datetime

# 64 状态定义
STATES = {
    "调整型": [
        {"id": "A01", "name": "积累未显期", "theme": "努力还没有看到结果"},
        {"id": "A05", "name": "启动混乱期", "theme": "刚开始一团乱"},
        {"id": "A09", "name": "资源受限期", "theme": "条件不够"},
        {"id": "A13", "name": "关系深化期", "theme": "关系需要深入"},
        {"id": "A17", "name": "路径依赖期", "theme": "习惯旧模式"},
        {"id": "A21", "name": "突破决策期", "theme": "需要做决定"},
        {"id": "A25", "name": "自然演化期", "theme": "顺其自然"},
        {"id": "A29", "name": "风险重复期", "theme": "类似问题反复出现"},
        {"id": "A33", "name": "主动退出期", "theme": "需要放手"},
        {"id": "A37", "name": "内部重构期", "theme": "内部需要调整"},
        {"id": "A41", "name": "负担削减期", "theme": "负载过重"},
        {"id": "A45", "name": "资源聚合期", "theme": "需要整合"},
        {"id": "A49", "name": "结构变革期", "theme": "需要大调整"},
        {"id": "A53", "name": "渐进深化期", "theme": "逐步深入"},
        {"id": "A57", "name": "影响渗透期", "theme": "影响力扩散"},
        {"id": "A61", "name": "内在校准期", "theme": "需要调整方向"},
    ],
    "过渡型": [
        {"id": "B02", "name": "路径错配期", "theme": "方向不对"},
        {"id": "B06", "name": "过载停滞期", "theme": "太累了"},
        {"id": "B10", "name": "慢速积累期", "theme": "进展慢"},
        {"id": "B14", "name": "资源高位期", "theme": "状态不错"},
        {"id": "B18", "name": "系统修正期", "theme": "需要微调"},
        {"id": "B22", "name": "表达失真期", "theme": "沟通有问题"},
        {"id": "B26", "name": "能量压缩期", "theme": "压力大"},
        {"id": "B30", "name": "曝光放大期", "theme": "被关注"},
        {"id": "B34", "name": "力量释放期", "theme": "可以行动了"},
        {"id": "B38", "name": "认知分歧期", "theme": "想法不一致"},
        {"id": "B42", "name": "收益放大期", "theme": "回报来了"},
        {"id": "B46", "name": "稳态提升期", "theme": "稳定上升"},
        {"id": "B50", "name": "系统成型期", "theme": "体系建立"},
        {"id": "B54", "name": "依附结构期", "theme": "需要依靠"},
        {"id": "B58", "name": "互动增强期", "theme": "交流增多"},
        {"id": "B62", "name": "细节放大期", "theme": "注意细节"},
    ],
    "观察型": [
        {"id": "C03", "name": "时机未到期", "theme": "还没到时候"},
        {"id": "C07", "name": "关系阻力期", "theme": "人际摩擦"},
        {"id": "C11", "name": "结构调整期", "theme": "需要重组"},
        {"id": "C15", "name": "收缩保护期", "theme": "需要保守"},
        {"id": "C19", "name": "机会临界期", "theme": "机会来了"},
        {"id": "C23", "name": "结构剥离期", "theme": "需要舍弃"},
        {"id": "C27", "name": "输入污染期", "theme": "信息太杂"},
        {"id": "C31", "name": "吸引增强期", "theme": "吸引力上升"},
        {"id": "C35", "name": "加速增长期", "theme": "快速增长"},
        {"id": "C39", "name": "路径受阻期", "theme": "路不通"},
        {"id": "C43", "name": "强制决策期", "theme": "必须决定"},
        {"id": "C47", "name": "限制强化期", "theme": "约束变多"},
        {"id": "C51", "name": "冲击震荡期", "theme": "外部冲击"},
        {"id": "C55", "name": "高点不稳期", "theme": "巅峰风险"},
        {"id": "C59", "name": "结构分散期", "theme": "注意力分散"},
        {"id": "C63", "name": "完成收尾期", "theme": "快结束了"},
    ],
    "决策型": [
        {"id": "D04", "name": "认知偏差期", "theme": "理解有误"},
        {"id": "D08", "name": "上升不稳期", "theme": "波动大"},
        {"id": "D12", "name": "推进停滞期", "theme": "推不动"},
        {"id": "D16", "name": "能量蓄势期", "theme": "准备充足"},
        {"id": "D20", "name": "观察判断期", "theme": "需要判断"},
        {"id": "D24", "name": "重启循环期", "theme": "新的开始"},
        {"id": "D28", "name": "压力临界期", "theme": "快到极限"},
        {"id": "D32", "name": "稳定结构期", "theme": "稳定状态"},
        {"id": "D36", "name": "隐匿保护期", "theme": "需要隐藏"},
        {"id": "D40", "name": "问题释放期", "theme": "问题爆发"},
        {"id": "D44", "name": "干扰入侵期", "theme": "外部干扰"},
        {"id": "D48", "name": "基础供给期", "theme": "基础需求"},
        {"id": "D52", "name": "强制暂停期", "theme": "被迫停止"},
        {"id": "D56", "name": "环境流动期", "theme": "环境变化"},
        {"id": "D60", "name": "规则约束期", "theme": "有规则限制"},
        {"id": "D64", "name": "未完过渡期", "theme": "还没结束"},
    ],
}

# 6 阶段定义
STAGES = [
    {"step": 1, "name": "刚开始不对劲", "decision_template": "接受现状，基础准备"},
    {"step": 2, "name": "逐渐察觉问题", "decision_template": "检查问题，收集信息"},
    {"step": 3, "name": "开始怀疑路径", "decision_template": "停止当前，重新评估"},
    {"step": 4, "name": "尝试调整方式", "decision_template": "小步试错，快速迭代"},
    {"step": 5, "name": "逐步适应", "decision_template": "强化有效，固化新法"},
    {"step": 6, "name": "进入新状态", "decision_template": "庆祝成果，开启新循环"},
]

# 心理学解读模板
PSYCHOLOGY_TEMPLATES = {
    "adler": [
        "你的目标导向是{goal}，而非{real_goal}。问：你想证明给谁看？",
        "你在追求{pursue}而非{real_pursue}。这服务于你的生活方式。",
        "你的行为服务于{purpose}。停下来问：这真的是我想要的吗？",
    ],
    "jung": [
        "潜意识在重复'{pattern}'的原型。觉察它，才能超越它。",
        "你在无意识中扮演{archetype}角色。意识到这一点，就有选择权。",
        "这是{shadow}阴影的投射。你不愿承认的部分，会以这种方式出现。",
    ],
    "freud": [
        "防御机制：{defense}。你在用{behavior}逃避{fear}。",
        "你在用{behavior}保护自我免受{threat}。但这让你无法真正解决问题。",
        "这是{mechanism}在起作用。觉察它，才有选择是否继续的自由。",
    ],
}


def generate_skill(state: dict, stage: dict) -> dict:
    """生成单个 Skill"""
    
    skill_id = f"{state['id']}-{stage['step']}"
    
    # 生成情境描述
    situation = f"在{state['name']}，你{stage['name']}。{state['theme']}。"
    
    # 生成核心问题
    core_problem = f"{state['theme']} + {stage['name']}导致的行为模式固化"
    
    # 生成行动建议
    actions = generate_actions(state, stage)
    
    # 生成避免事项
    avoids = generate_avoids(state, stage)
    
    # 生成心理学解读
    psychology = generate_psychology(state, stage)
    
    return {
        "id": skill_id,
        "state_id": state["id"],
        "state_name": state["name"],
        "stage": stage["step"],
        "stage_name": stage["name"],
        "type": get_type_by_id(state["id"]),
        "theme": state["theme"],
        
        "situation": situation,
        "core_problem": core_problem,
        "decision": stage["decision_template"],
        
        "action": actions,
        "avoid": avoids,
        
        "psychology": psychology,
        
        "metadata": {
            "quality_score": 45,
            "status": "published",
            "price_tier": "premium",
            "created_at": datetime.now().isoformat(),
            "version": "1.0"
        }
    }


def get_type_by_id(state_id: str) -> str:
    """根据状态 ID 获取类型"""
    if state_id.startswith("A"):
        return "调整型"
    elif state_id.startswith("B"):
        return "过渡型"
    elif state_id.startswith("C"):
        return "观察型"
    elif state_id.startswith("D"):
        return "决策型"
    return "未知"


def generate_actions(state: dict, stage: dict) -> list:
    """生成行动建议"""
    
    base_actions = {
        1: ["接受当前状态", "记录每天进展", "设定合理期望"],
        2: ["列出所有相关因素", "逐一验证假设", "找信任的人聊聊"],
        3: ["暂停当前投入 48 小时", "写下核心问题", "寻求外部反馈"],
        4: ["尝试 1 个新方法", "设定实验期", "快速验证效果"],
        5: ["强化有效方法", "固化新流程", "删除旧方法"],
        6: ["庆祝成果", "复盘经验", "开启新循环"],
    }
    
    return base_actions.get(stage["step"], ["具体行动待补充"])


def generate_avoids(state: dict, stage: dict) -> list:
    """生成避免事项"""
    
    base_avoids = {
        1: ["急于求成", "与他人比较"],
        2: ["情绪化决策", "逃避问题"],
        3: ["继续加倍努力", "用忙碌逃避质疑"],
        4: ["期待立竿见影", "频繁更换方法"],
        5: ["回到旧模式", "自我怀疑"],
        6: ["骄傲自满", "停止学习"],
    }
    
    return base_avoids.get(stage["step"], ["避免事项待补充"])


def generate_psychology(state: dict, stage: dict) -> dict:
    """生成心理学解读"""
    
    return {
        "adler": f"你的目标导向是证明自己，而非解决问题。问：你想证明给谁看？",
        "jung": f"潜意识在重复'努力=正确'的原型。觉察它，才能超越它。",
        "freud": f"防御机制：用忙碌逃避方向质疑。你在用努力逃避'可能选错了'的恐惧。",
    }


def generate_all_skills():
    """生成全部 384 Skills"""
    
    all_skills = []
    
    for type_name, states in STATES.items():
        print(f"📦 生成{type_name}...")
        
        for state in states:
            for stage in STAGES:
                skill = generate_skill(state, stage)
                all_skills.append(skill)
    
    return all_skills


def save_skills(skills: list, output_path: str):
    """保存 Skills 到文件"""
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(skills, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 保存 {len(skills)} 个 Skills 到 {output_file}")


def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  384 Skills 批量生成                                      ║")
    print("║  64 状态 × 6 阶段 = 384 Skills                              ║")
    print("╚═══════════════════════════════════════════════════════════")
    print()
    
    # 生成全部 Skills
    skills = generate_all_skills()
    
    # 保存
    output_path = "/home/nicola/.openclaw/workspace/data/skills/384-skills-complete.json"
    save_skills(skills, output_path)
    
    # 统计
    print()
    print("📊 生成统计:")
    print(f"  总计：{len(skills)} 个 Skills")
    
    by_type = {}
    for skill in skills:
        t = skill["type"]
        by_type[t] = by_type.get(t, 0) + 1
    
    for t, count in by_type.items():
        print(f"  {t}: {count} 个")
    
    print()
    print("✅ 384 Skills 生成完成")


if __name__ == "__main__":
    main()
