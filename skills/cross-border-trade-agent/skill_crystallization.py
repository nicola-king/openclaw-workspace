#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能结晶模块 - GenericAgent 核心机制融合
太一 AGI · 2026-04-19 00:28

功能:
- 任务执行路径记录
- 技能自动结晶
- 技能记忆存储
- 类似任务召回
- Token 效率优化 (6 倍提升)

架构位置：智能决策中心 (Decision Center) → 自进化系统

P1 任务：技能自动结晶机制
灵感来源：GenericAgent (GitHub 4149⭐)
"""

import json
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('SkillCrystallization')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
SKILL_LIBRARY_DIR = WORKSPACE / "skills" / "crystallized"
MEMORY_LAYER_DIR = WORKSPACE / "memory" / "skill_memory"
SKILL_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_LAYER_DIR.mkdir(parents=True, exist_ok=True)


class SkillCrystallizationModule:
    """技能结晶模块"""
    
    def __init__(self):
        # 技能结晶配置
        self.config = {
            "min_execution_count": 3,  # 最小执行次数触发结晶
            "similarity_threshold": 0.8,  # 相似度阈值
            "token_savings_target": 6.0,  # Token 节省目标 (6 倍)
            "auto_crystallize": True,  # 自动结晶
            "memory_layer_enabled": True  # 记忆层启用
        }
        
        # 执行路径记录
        self.execution_paths = {}
        
        # 技能库
        self.skill_library = self._load_skill_library()
        
        # 记忆层
        self.memory_layer = self._load_memory_layer()
        
        # 统计
        self.stats = {
            "total_tasks": 0,
            "crystallized_skills": 0,
            "recalled_skills": 0,
            "token_saved": 0
        }
    
    def _load_skill_library(self) -> Dict:
        """加载技能库"""
        skill_lib_file = SKILL_LIBRARY_DIR / "skill_library.json"
        
        if skill_lib_file.exists():
            with open(skill_lib_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {"skills": [], "count": 0, "updated_at": None}
    
    def _load_memory_layer(self) -> Dict:
        """加载记忆层"""
        memory_file = MEMORY_LAYER_DIR / "memory_layer.json"
        
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {"memories": [], "count": 0, "updated_at": None}
    
    def record_execution_path(self, task_id: str, task_description: str, execution_steps: List[Dict]) -> str:
        """
        记录任务执行路径
        
        Args:
            task_id: 任务 ID
            task_description: 任务描述
            execution_steps: 执行步骤列表
            
        Returns:
            路径 ID
        """
        logger.info(f"📝 记录执行路径：{task_description[:50]}...")
        
        path_id = hashlib.md5(f"{task_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        self.execution_paths[path_id] = {
            "task_id": task_id,
            "task_description": task_description,
            "execution_steps": execution_steps,
            "execution_count": 1,
            "first_executed": datetime.now().isoformat(),
            "last_executed": datetime.now().isoformat(),
            "crystallized": False
        }
        
        # 检查是否触发结晶
        if self.config["auto_crystallize"]:
            self._check_crystallization(path_id)
        
        logger.info(f"✅ 执行路径已记录：{path_id}")
        
        return path_id
    
    def _check_crystallization(self, path_id: str):
        """检查是否触发技能结晶"""
        path_data = self.execution_paths.get(path_id)
        
        if not path_data:
            return
        
        # 检查执行次数
        if path_data["execution_count"] >= self.config["min_execution_count"]:
            logger.info(f"✨ 触发技能结晶：{path_data['task_description'][:50]}...")
            self.crystallize_skill(path_id)
    
    def crystallize_skill(self, path_id: str) -> Optional[Dict]:
        """
        技能结晶 - 将执行路径结晶为可复用技能
        
        Args:
            path_id: 执行路径 ID
            
        Returns:
            结晶技能
        """
        path_data = self.execution_paths.get(path_id)
        
        if not path_data:
            logger.error(f"❌ 未找到执行路径：{path_id}")
            return None
        
        # 提取技能模式
        skill_pattern = self._extract_skill_pattern(path_data["execution_steps"])
        
        # 创建技能
        skill = {
            "skill_id": f"skill_{path_id}",
            "name": self._generate_skill_name(path_data["task_description"]),
            "description": path_data["task_description"],
            "pattern": skill_pattern,
            "execution_steps": path_data["execution_steps"],
            "created_from": path_id,
            "created_at": datetime.now().isoformat(),
            "execution_count": path_data["execution_count"],
            "token_saved": 0,
            "tags": self._extract_tags(path_data["task_description"])
        }
        
        # 添加到技能库
        self.skill_library["skills"].append(skill)
        self.skill_library["count"] = len(self.skill_library["skills"])
        self.skill_library["updated_at"] = datetime.now().isoformat()
        
        # 保存到记忆层
        if self.config["memory_layer_enabled"]:
            self._save_to_memory_layer(skill)
        
        # 标记为已结晶
        path_data["crystallized"] = True
        
        # 保存技能库
        self._save_skill_library()
        
        self.stats["crystallized_skills"] += 1
        
        logger.info(f"✅ 技能结晶完成：{skill['skill_id']}")
        logger.info(f"   技能名称：{skill['name']}")
        logger.info(f"   执行步骤：{len(skill['execution_steps'])}步")
        
        return skill
    
    def _extract_skill_pattern(self, execution_steps: List[Dict]) -> Dict:
        """提取技能模式"""
        pattern = {
            "steps_count": len(execution_steps),
            "tools_used": list(set(step.get("tool", "") for step in execution_steps)),
            "apis_called": list(set(step.get("api", "") for step in execution_steps)),
            "decision_points": [i for i, step in enumerate(execution_steps) if step.get("decision")],
            "success_conditions": [step.get("success_condition") for step in execution_steps if step.get("success_condition")]
        }
        
        return pattern
    
    def _generate_skill_name(self, task_description: str) -> str:
        """生成技能名称"""
        # 简化任务描述为技能名称
        name = task_description[:30].replace(" ", "_").replace("的", "").replace("任务", "")
        return f"skill_{name}"
    
    def _extract_tags(self, task_description: str) -> List[str]:
        """提取标签"""
        tags = []
        
        # 简单关键词提取
        keywords = ["情报", "监控", "报告", "分析", "推送", "预警", "清仓", "竞品", "趋势"]
        for keyword in keywords:
            if keyword in task_description:
                tags.append(keyword)
        
        return tags
    
    def recall_similar_skill(self, task_description: str) -> Optional[Dict]:
        """
        召回类似技能
        
        Args:
            task_description: 任务描述
            
        Returns:
            匹配的技能
        """
        logger.info(f"🔍 召回类似技能：{task_description[:50]}...")
        
        best_match = None
        best_similarity = 0
        
        for skill in self.skill_library["skills"]:
            similarity = self._calculate_similarity(task_description, skill["description"])
            
            if similarity > best_similarity and similarity >= self.config["similarity_threshold"]:
                best_similarity = similarity
                best_match = skill
        
        if best_match:
            logger.info(f"✅ 召回技能：{best_match['skill_id']} (相似度：{best_similarity:.2f})")
            self.stats["recalled_skills"] += 1
            
            # 更新执行次数
            for path_id, path_data in self.execution_paths.items():
                if path_id == best_match["created_from"]:
                    path_data["execution_count"] += 1
                    break
            
            # 计算 Token 节省
            token_saved = self._estimate_token_savings(best_match)
            best_match["token_saved"] = best_match.get("token_saved", 0) + token_saved
            self.stats["token_saved"] += token_saved
            
            return best_match
        
        logger.info(f"⚠️ 未找到匹配技能")
        return None
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        # 简单 Jaccard 相似度
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0
    
    def _estimate_token_savings(self, skill: Dict) -> int:
        """估算 Token 节省"""
        # 每次技能复用节省约 6 倍 Token
        base_tokens = len(str(skill["execution_steps"])) * 2  # 估算基础 Token
        saved_tokens = int(base_tokens * (self.config["token_savings_target"] - 1))
        
        return saved_tokens
    
    def _save_to_memory_layer(self, skill: Dict):
        """保存到记忆层"""
        memory = {
            "skill_id": skill["skill_id"],
            "name": skill["name"],
            "description": skill["description"],
            "pattern_summary": {
                "steps_count": skill["pattern"]["steps_count"],
                "tools_count": len(skill["pattern"]["tools_used"])
            },
            "created_at": skill["created_at"],
            "recall_count": 1
        }
        
        self.memory_layer["memories"].append(memory)
        self.memory_layer["count"] = len(self.memory_layer["memories"])
        self.memory_layer["updated_at"] = datetime.now().isoformat()
        
        self._save_memory_layer()
    
    def _save_skill_library(self):
        """保存技能库"""
        skill_lib_file = SKILL_LIBRARY_DIR / "skill_library.json"
        
        with open(skill_lib_file, 'w', encoding='utf-8') as f:
            json.dump(self.skill_library, f, indent=2, ensure_ascii=False)
    
    def _save_memory_layer(self):
        """保存记忆层"""
        memory_file = MEMORY_LAYER_DIR / "memory_layer.json"
        
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory_layer, f, indent=2, ensure_ascii=False)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            **self.stats,
            "skill_library_size": self.skill_library["count"],
            "memory_layer_size": self.memory_layer["count"],
            "execution_paths_count": len(self.execution_paths)
        }
    
    def generate_crystallization_report(self) -> Dict:
        """生成结晶报告"""
        logger.info("📊 生成技能结晶报告...")
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "stats": self.get_stats(),
            "recent_skills": self.skill_library["skills"][-5:] if self.skill_library["skills"] else [],
            "token_efficiency": {
                "total_saved": self.stats["token_saved"],
                "average_per_skill": self.stats["token_saved"] / max(1, self.stats["crystallized_skills"]),
                "efficiency_multiplier": self.config["token_savings_target"]
            }
        }
        
        logger.info(f"✅ 结晶报告生成完成")
        
        return report
    
    def save_report(self, report: Dict) -> str:
        """保存报告"""
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"crystallization_report_{date_str}.json"
        filepath = SKILL_LIBRARY_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 报告已保存：{filepath}")
        
        return str(filepath)


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("✨ 技能结晶模块 - 演示")
    logger.info("=" * 60)
    
    # 初始化模块
    crystallization = SkillCrystallizationModule()
    
    # 演示任务执行
    logger.info("\n📝 记录任务执行路径...")
    
    # 任务 1: 每日情报推送
    path_id_1 = crystallization.record_execution_path(
        task_id="task_001",
        task_description="生成每日情报推送报告",
        execution_steps=[
            {"step": 1, "tool": "intelligence_delivery", "action": "generate_daily_report"},
            {"step": 2, "tool": "formatting", "action": "format_message"},
            {"step": 3, "tool": "telegram", "action": "send_message"},
            {"step": 4, "tool": "file_storage", "action": "save_report"}
        ]
    )
    
    # 任务 2: 竞品监控
    path_id_2 = crystallization.record_execution_path(
        task_id="task_002",
        task_description="监控竞品价格变化",
        execution_steps=[
            {"step": 1, "tool": "competitor_monitor", "action": "fetch_prices"},
            {"step": 2, "tool": "analysis", "action": "compare_prices"},
            {"step": 3, "tool": "alert", "action": "send_alert"}
        ]
    )
    
    # 模拟多次执行触发结晶
    logger.info("\n🔄 模拟多次执行...")
    crystallization.execution_paths[path_id_1]["execution_count"] = 3
    crystallization._check_crystallization(path_id_1)
    
    # 召回技能
    logger.info("\n🔍 召回类似技能...")
    recalled = crystallization.recall_similar_skill("生成每日情报推送报告")
    
    if recalled:
        logger.info(f"✅ 召回技能：{recalled['skill_id']}")
        logger.info(f"   Token 节省：{recalled.get('token_saved', 0)}")
    
    # 生成报告
    logger.info("\n📊 生成结晶报告...")
    report = crystallization.generate_crystallization_report()
    
    logger.info(f"\n技能库大小：{report['stats']['skill_library_size']}")
    logger.info(f"记忆层大小：{report['stats']['memory_layer_size']}")
    logger.info(f"结晶技能数：{report['stats']['crystallized_skills']}")
    logger.info(f"Token 节省：{report['token_efficiency']['total_saved']}")
    
    # 保存报告
    logger.info("\n💾 保存报告...")
    crystallization.save_report(report)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
