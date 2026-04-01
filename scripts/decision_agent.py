#!/usr/bin/env python3
"""
Decision Agent - 情景模式决策引擎
负责：识别 State(64) → 判断 Stage(6) → 调用 Skill(384)
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class DecisionAgent:
    """
    情景模式决策 Agent
    
    核心功能：
    1. 识别用户当前状态（64 之一）
    2. 判断所处阶段（1-6）
    3. 调用对应 Skill（行动指令）
    """
    
    # 状态关键词映射
    STATE_KEYWORDS = {
        "积累未显期": ["努力", "没结果", "没回报", "没效果", "付出", "收获"],
        "启动混乱期": ["刚开始", "一团乱", "头绪", "混乱", "起步"],
        "资源受限期": ["资源", "条件", "不够", "缺钱", "缺人", "缺时间"],
        "关系深化期": ["关系", "深入", "表面", "沟通", "信任"],
        "路径依赖期": ["习惯", "旧模式", "重复", "依赖", "老方法"],
        "突破决策期": ["决定", "选择", "决策", "犹豫", "取舍"],
        "自然演化期": ["顺其自然", "控制", "放手", "等待"],
        "风险重复期": ["重复", "反复", "再次", "又一次", "循环"],
        "主动退出期": ["退出", "放手", "放弃", "离开", "结束"],
        "内部重构期": ["内部", "重构", "调整", "重组", "混乱"],
        "负担削减期": ["负担", "负载", "太累", "压力", " overload"],
        "资源聚合期": ["分散", "整合", "聚合", "协同", "资源"],
        "结构变革期": ["变革", "大调整", "结构", "体系", "系统"],
        "渐进深化期": ["渐进", "逐步", "深入", "慢慢", "快"],
        "影响渗透期": ["影响", "渗透", "扩散", "输出", "持续"],
        "内在校准期": ["方向", "偏离", "校准", "初心", "对齐"],
        
        "路径错配期": ["方向", "不对", "错配", "不适合", "赛道"],
        "过载停滞期": ["太累", "过载", "停滞", "停不下来", "倦怠"],
        "慢速积累期": ["慢", "进展", "积累", "坚持", "放弃"],
        "资源高位期": ["状态好", "高位", "顺利", "怕失去", "飘"],
        "系统修正期": ["微调", "修正", "优化", "迭代", "小问题"],
        "表达失真期": ["沟通", "误解", "表达", "说不清", "理解"],
        "能量压缩期": ["压力", "压缩", "憋", "释放", "出口"],
        "曝光放大期": ["关注", "曝光", "被看到", " spotlight"],
        "力量释放期": ["行动", "释放", "出击", "机会", "发力"],
        "认知分歧期": ["分歧", "不一致", "想法", "共识", "差异"],
        "收益放大期": ["回报", "收益", "收获", "成果", "奖励"],
        "稳态提升期": ["稳定", "上升", "提升", "持续", "节奏"],
        "系统成型期": ["系统", "体系", "成型", "框架", "流程"],
        "依附结构期": ["依靠", "依附", "依赖", "支撑", "独立"],
        "互动增强期": ["互动", "交流", "沟通", "增多", "社交"],
        "细节放大期": ["细节", "完美", "注意", "纠结", "小数点"],
        
        "时机未到期": ["时机", "时候", "等待", "成熟", "早"],
        "关系阻力期": ["阻力", "摩擦", "冲突", "人际", "矛盾"],
        "结构调整期": ["调整", "重组", "结构", "理顺", "混乱"],
        "收缩保护期": ["收缩", "保守", "保护", "防御", "风险"],
        "机会临界期": ["机会", "临界", "来了", "抓住", "判断"],
        "结构剥离期": ["剥离", "舍弃", "断舍离", "删除", "精简"],
        "输入污染期": ["信息", "污染", "太杂", "筛选", "质量"],
        "吸引增强期": ["吸引", "魅力", "关注", "上升", "磁场"],
        "加速增长期": ["加速", "增长", "快速", "爆发", "可持续"],
        "路径受阻期": ["受阻", "路不通", "阻碍", "替代", "新路径"],
        "强制决策期": ["必须", "强制", "决定", "拖延", "紧迫"],
        "限制强化期": ["限制", "约束", "规则", "创新", "框架"],
        "冲击震荡期": ["冲击", "震荡", "外部", "波动", "稳住"],
        "高点不稳期": ["高点", "不稳", "巅峰", "风险", "下滑"],
        "结构分散期": ["分散", "注意力", "聚焦", "多", "核心"],
        "完成收尾期": ["收尾", "完成", "结束", "遗漏", "检查"],
        
        "认知偏差期": ["偏差", "理解", "错误", "认知", "纠正"],
        "上升不稳期": ["不稳", "波动", "上升", "节奏", "稳步"],
        "推进停滞期": ["停滞", "推不动", "卡住", "换方法", "换人"],
        "能量蓄势期": ["蓄势", "准备", "充足", "时机", "行动"],
        "观察判断期": ["观察", "判断", "决策", "信息", "快速"],
        "重启循环期": ["重启", "新的开始", "放下", "过去", "循环"],
        "压力临界期": ["压力", "临界", "极限", "减压", "退出"],
        "稳定结构期": ["稳定", "结构", "平衡", "僵化", "发展"],
        "隐匿保护期": ["隐匿", "隐藏", "低调", "保护", "暴露"],
        "问题释放期": ["问题", "爆发", "释放", "解决", "直面"],
        "干扰入侵期": ["干扰", "入侵", "边界", "外部", "设立"],
        "基础供给期": ["基础", "供给", "需求", "优先", "满足"],
        "强制暂停期": ["暂停", "被迫", "停止", "利用", "反思"],
        "环境流动期": ["环境", "流动", "变化", "适应", "共舞"],
        "规则约束期": ["规则", "约束", "限制", "遵守", "突破"],
        "未完过渡期": ["未完", "过渡", "还没", "继续", "接近"],
    }
    
    # 阶段关键词映射
    STAGE_KEYWORDS = {
        1: ["刚开始", "一开始", "最初", "起步", "开始"],
        2: ["逐渐", "慢慢", "察觉", "意识到", "发现"],
        3: ["怀疑", "质疑", "困惑", "迷茫", "对不对"],
        4: ["尝试", "试试", "调整", "改变", "新方法"],
        5: ["逐步", "适应", "见效", "有效", "新方式"],
        6: ["完成", "进入", "新状态", "转化", "稳定"],
    }
    
    def __init__(self, skills_data_path: str = None):
        """
        初始化 Decision Agent
        
        Args:
            skills_data_path: Skills 数据文件路径
        """
        self.skills_data_path = skills_data_path or "/home/nicola/.openclaw/workspace/data/skills/384-skills-complete.json"
        self.skills = self._load_skills()
    
    def _load_skills(self) -> Dict:
        """加载 Skills 数据库"""
        skills_file = Path(self.skills_data_path)
        
        if not skills_file.exists():
            print(f"⚠️ Skills 文件不存在：{skills_file}")
            return {}
        
        with open(skills_file, 'r', encoding='utf-8') as f:
            skills_list = json.load(f)
        
        # 转换为字典索引
        skills_dict = {}
        for skill in skills_list:
            skill_id = skill['id']
            skills_dict[skill_id] = skill
        
        print(f"✅ 加载 {len(skills_dict)} 个 Skills")
        return skills_dict
    
    def analyze(self, user_input: str) -> Dict:
        """
        分析用户输入，返回 State + Stage + Skill
        
        Args:
            user_input: 用户输入文本
        
        Returns:
            {
                "state": {...},
                "stage": {...},
                "skill": {...},
                "confidence": 0.85
            }
        """
        # Step 1: 识别状态
        state = self._identify_state(user_input)
        
        # Step 2: 判断阶段
        stage = self._identify_stage(user_input)
        
        # Step 3: 调用 Skill
        skill_id = f"{state['id']}-{stage['step']}"
        skill = self.skills.get(skill_id)
        
        # Step 4: 计算置信度
        confidence = self._calculate_confidence(user_input, state, stage)
        
        return {
            "state": state,
            "stage": stage,
            "skill": skill,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
    
    def _identify_state(self, user_input: str) -> Dict:
        """识别用户当前状态"""
        
        scores = {}
        
        for state_name, keywords in self.STATE_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword in user_input.lower():
                    score += 1
            if score > 0:
                scores[state_name] = score
        
        if not scores:
            # 默认返回积累未显期
            return {
                "id": "A01",
                "name": "积累未显期",
                "type": "调整型",
                "theme": "努力还没有看到结果"
            }
        
        # 返回得分最高的状态
        best_state = max(scores, key=scores.get)
        state_id = self._get_state_id(best_state)
        
        return {
            "id": state_id,
            "name": best_state,
            "type": self._get_type_by_id(state_id),
            "theme": self._get_theme(best_state),
            "score": scores[best_state]
        }
    
    def _identify_stage(self, user_input: str) -> Dict:
        """判断用户所处阶段"""
        
        scores = {}
        
        for stage_num, keywords in self.STAGE_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword in user_input.lower():
                    score += 1
            if score > 0:
                scores[stage_num] = score
        
        if not scores:
            # 默认返回第 3 阶段（最常见痛点）
            return {
                "step": 3,
                "name": "开始怀疑路径",
                "score": 0
            }
        
        # 返回得分最高的阶段
        best_stage = max(scores, key=scores.get)
        
        stage_names = {
            1: "刚开始不对劲",
            2: "逐渐察觉问题",
            3: "开始怀疑路径",
            4: "尝试调整方式",
            5: "逐步适应",
            6: "进入新状态"
        }
        
        return {
            "step": best_stage,
            "name": stage_names.get(best_stage, "未知"),
            "score": scores[best_stage]
        }
    
    def _get_state_id(self, state_name: str) -> str:
        """根据状态名称获取 ID"""
        state_mapping = {
            "积累未显期": "A01",
            "启动混乱期": "A05",
            "资源受限期": "A09",
            "关系深化期": "A13",
            "路径依赖期": "A17",
            "突破决策期": "A21",
            "自然演化期": "A25",
            "风险重复期": "A29",
            "主动退出期": "A33",
            "内部重构期": "A37",
            "负担削减期": "A41",
            "资源聚合期": "A45",
            "结构变革期": "A49",
            "渐进深化期": "A53",
            "影响渗透期": "A57",
            "内在校准期": "A61",
            
            "路径错配期": "B02",
            "过载停滞期": "B06",
            "慢速积累期": "B10",
            "资源高位期": "B14",
            "系统修正期": "B18",
            "表达失真期": "B22",
            "能量压缩期": "B26",
            "曝光放大期": "B30",
            "力量释放期": "B34",
            "认知分歧期": "B38",
            "收益放大期": "B42",
            "稳态提升期": "B46",
            "系统成型期": "B50",
            "依附结构期": "B54",
            "互动增强期": "B58",
            "细节放大期": "B62",
            
            "时机未到期": "C03",
            "关系阻力期": "C07",
            "结构调整期": "C11",
            "收缩保护期": "C15",
            "机会临界期": "C19",
            "结构剥离期": "C23",
            "输入污染期": "C27",
            "吸引增强期": "C31",
            "加速增长期": "C35",
            "路径受阻期": "C39",
            "强制决策期": "C43",
            "限制强化期": "C47",
            "冲击震荡期": "C51",
            "高点不稳期": "C55",
            "结构分散期": "C59",
            "完成收尾期": "C63",
            
            "认知偏差期": "D04",
            "上升不稳期": "D08",
            "推进停滞期": "D12",
            "能量蓄势期": "D16",
            "观察判断期": "D20",
            "重启循环期": "D24",
            "压力临界期": "D28",
            "稳定结构期": "D32",
            "隐匿保护期": "D36",
            "问题释放期": "D40",
            "干扰入侵期": "D44",
            "基础供给期": "D48",
            "强制暂停期": "D52",
            "环境流动期": "D56",
            "规则约束期": "D60",
            "未完过渡期": "D64",
        }
        
        return state_mapping.get(state_name, "A01")
    
    def _get_type_by_id(self, state_id: str) -> str:
        """根据 ID 获取类型"""
        if state_id.startswith("A"):
            return "调整型"
        elif state_id.startswith("B"):
            return "过渡型"
        elif state_id.startswith("C"):
            return "观察型"
        elif state_id.startswith("D"):
            return "决策型"
        return "未知"
    
    def _get_theme(self, state_name: str) -> str:
        """获取状态主题"""
        themes = {
            "积累未显期": "努力还没有看到结果",
            "启动混乱期": "刚开始一团乱",
            "路径错配期": "方向不对",
            "时机未到期": "还没到时候",
            "认知偏差期": "理解有误",
        }
        return themes.get(state_name, "未知主题")
    
    def _calculate_confidence(self, user_input: str, state: Dict, stage: Dict) -> float:
        """计算匹配置信度"""
        
        # 基础置信度
        base_confidence = 0.5
        
        # 状态匹配加分
        state_score = state.get('score', 0)
        state_bonus = min(state_score * 0.1, 0.3)
        
        # 阶段匹配加分
        stage_score = stage.get('score', 0)
        stage_bonus = min(stage_score * 0.1, 0.2)
        
        confidence = base_confidence + state_bonus + stage_bonus
        
        return min(confidence, 0.99)
    
    def format_output(self, result: Dict) -> str:
        """格式化输出结果"""
        
        state = result['state']
        stage = result['stage']
        skill = result['skill']
        confidence = result['confidence']
        
        output = []
        output.append("╔══════════════════════════════════════════════════════════╗")
        output.append("║  情景模式 · 决策报告                                      ║")
        output.append("╚═══════════════════════════════════════════════════════════╝")
        output.append("")
        output.append(f"📍 你当前的位置")
        output.append(f"   情景：{state['name']}")
        output.append(f"   类型：{state['type']}")
        output.append(f"   阶段：Step {stage['step']}/6 ({stage['name']})")
        output.append(f"   置信度：{confidence:.0%}")
        output.append("")
        
        if skill:
            output.append(f"💡 最优动作：{skill['decision']}")
            output.append("")
            output.append(f"🎯 具体行动：")
            for i, action in enumerate(skill['action'], 1):
                output.append(f"   {i}. {action}")
            output.append("")
            output.append(f"⚠️ 避免：")
            for avoid in skill['avoid']:
                output.append(f"   - {avoid}")
            output.append("")
            output.append(f"🧠 心理学解读：")
            output.append(f"   阿德勒：{skill['psychology']['adler']}")
            output.append(f"   荣格：{skill['psychology']['jung']}")
            output.append(f"   弗洛伊德：{skill['psychology']['freud']}")
        else:
            output.append("⚠️ 暂未找到对应 Skill，正在生成中...")
        
        output.append("")
        output.append("═══════════════════════════════════════════════════════════")
        
        return "\n".join(output)


def main():
    """主函数 - 测试 Decision Agent"""
    
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Decision Agent 测试                                      ║")
    print("║  情景模式决策引擎                                         ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    # 创建 Agent
    agent = DecisionAgent()
    
    # 测试用例
    test_cases = [
        "我最近很努力但没结果",
        "刚开始做一团乱，不知道从哪开始",
        "方向好像不对，越努力越焦虑",
        "时机还没到，但我不想浪费时间",
        "理解可能有偏差，结果一直不对",
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"【测试 {i}】")
        print(f"输入：{test_input}")
        print()
        
        result = agent.analyze(test_input)
        output = agent.format_output(result)
        print(output)
        print()
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()
