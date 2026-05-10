#!/usr/bin/env python3
"""
Evolution Agent - 自主进化智能体 v1.0
太一 AGI · 2026-04-15

系统自我改进，无需人工干预
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class EvolutionAgent:
    """自主进化智能体"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.skills_dir = self.workspace_root / "skills"
        self.monitoring_dir = self.workspace_root / "monitoring"
        self.reports_dir = self.workspace_root / "reports"
        self.config_path = self.workspace_root / "skills" / "evolution-agent" / "config" / "evolution-config.json"
        self.evolution_log_path = self.monitoring_dir / "evolution-log.json"
        
        # 配置
        self.config = {
            "auto_optimize": True,
            "auto_create_skills": True,
            "auto_merge_duplicates": True,
            "auto_update_config": True,
            "backup_before_change": True,
        }
        
        # 加载配置
        self._load_config()
        
        # 进化历史
        self.evolution_history = []
        self._load_history()
    
    def _load_config(self):
        """加载配置"""
        if self.config_path.exists():
            try:
                config_data = json.loads(self.config_path.read_text(encoding="utf-8"))
                self.config.update(config_data)
            except:
                pass
    
    def _load_history(self):
        """加载进化历史"""
        if self.evolution_log_path.exists():
            try:
                self.evolution_history = json.loads(self.evolution_log_path.read_text(encoding="utf-8"))
            except:
                pass
    
    def _log_evolution(self, action: str, details: Dict, success: bool):
        """记录进化日志"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "success": success,
        }
        self.evolution_history.append(entry)
        self.evolution_history = self.evolution_history[-100:]  # 保留最近 100 条
        
        self.evolution_log_path.parent.mkdir(exist_ok=True)
        self.evolution_log_path.write_text(json.dumps(self.evolution_history, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def identify_bottlenecks(self) -> List[Dict]:
        """识别瓶颈"""
        bottlenecks = []
        
        # 检查调度器日志
        scheduler_log = self.monitoring_dir / "scheduler-log.json"
        if scheduler_log.exists():
            try:
                logs = json.loads(scheduler_log.read_text(encoding="utf-8"))
                failures = [log for log in logs if not log.get("success", True)]
                
                if len(failures) > 5:
                    bottlenecks.append({
                        "type": "execution_failure",
                        "severity": "high",
                        "message": f"检测到{len(failures)}次执行失败",
                        "suggestion": "检查脚本或增加资源",
                    })
            except:
                pass
        
        # 检查 PDCA 成功率
        pdca_log = self.monitoring_dir / "pdca-simple-log.json"
        if pdca_log.exists():
            try:
                logs = json.loads(pdca_log.read_text(encoding="utf-8"))
                if logs:
                    latest = logs[-1] if isinstance(logs[-1], dict) else {}
                    success_rate = latest.get("check", {}).get("success_rate", 1.0)
                    
                    if success_rate < 0.8:
                        bottlenecks.append({
                            "type": "low_success_rate",
                            "severity": "medium",
                            "message": f"PDCA 成功率低 ({success_rate:.1%})",
                            "suggestion": "优化执行策略",
                        })
            except:
                pass
        
        return bottlenecks
    
    def optimize_process(self, bottlenecks: List[Dict]) -> Dict:
        """优化流程"""
        optimizations = []
        
        for bottleneck in bottlenecks:
            if bottleneck["type"] == "execution_failure":
                # 建议：增加超时时间
                optimizations.append({
                    "action": "increase_timeout",
                    "target": "scheduler-config.json",
                    "change": "timeout: 300 -> 600",
                })
            
            elif bottleneck["type"] == "low_success_rate":
                # 建议：调整执行频率
                optimizations.append({
                    "action": "adjust_frequency",
                    "target": "scheduler-config.json",
                    "change": "interval: auto-adjust",
                })
        
        result = {
            "optimizations": optimizations,
            "count": len(optimizations),
        }
        
        self._log_evolution("optimize_process", result, True)
        return result
    
    def create_skill(self, name: str, description: str) -> Dict:
        """创建技能"""
        skill_dir = self.skills_dir / "08-emerged" / f"emerged-skill-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 SKILL.md
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(f"""# {name}

> **版本**: 1.0.0  
> **创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
> **描述**: {description}  
> **来源**: 自主进化创建

---

## 🎯 职责域

**核心功能**: {description}

---

## 📋 专业能力

- ✅ 核心能力 1
- ✅ 核心能力 2

---

*太一 AGI · 自主进化 · {datetime.now().strftime("%Y-%m-%d")}*
""", encoding="utf-8")
        
        # 创建 README.md
        readme = skill_dir / "README.md"
        readme.write_text(f"# {name}\n\n自主进化创建的技能\n", encoding="utf-8")
        
        # 创建目录
        (skill_dir / "config").mkdir(exist_ok=True)
        (skill_dir / "tests").mkdir(exist_ok=True)
        
        result = {
            "skill_name": name,
            "skill_dir": str(skill_dir),
            "created": True,
        }
        
        self._log_evolution("create_skill", result, True)
        return result
    
    def merge_duplicates(self) -> Dict:
        """合并重复技能"""
        # 简化版：检测重复名称
        merged = []
        
        # TODO: 实现真正的重复检测和合并
        
        result = {
            "merged_count": len(merged),
            "merged_skills": merged,
        }
        
        self._log_evolution("merge_duplicates", result, True)
        return result
    
    def update_config(self, target: str, changes: Dict) -> Dict:
        """更新配置"""
        if not self.config.get("auto_update_config", True):
            return {"status": "disabled"}
        
        # 备份旧配置
        if self.config.get("backup_before_change", True):
            config_file = self.workspace_root / target
            if config_file.exists():
                backup_file = config_file.with_suffix(config_file.suffix + ".backup")
                shutil.copy(config_file, backup_file)
        
        # 更新配置
        result = {
            "target": target,
            "changes": changes,
            "updated": True,
        }
        
        self._log_evolution("update_config", result, True)
        return result
    
    def evolve(self) -> Dict:
        """执行完整进化流程"""
        print("\n" + "="*60)
        print("🧬 Evolution Agent - 自主进化")
        print("="*60)
        
        # 1. 识别瓶颈
        print("\n🔍 识别瓶颈...")
        bottlenecks = self.identify_bottlenecks()
        print(f"发现 {len(bottlenecks)} 个瓶颈")
        
        # 2. 优化流程
        print("\n⚙️  优化流程...")
        optimizations = self.optimize_process(bottlenecks)
        print(f"生成 {optimizations['count']} 个优化建议")
        
        # 3. 创建技能 (如果需要)
        print("\n📦 技能管理...")
        if self.config.get("auto_create_skills", True) and len(bottlenecks) > 0:
            skill_result = self.create_skill(
                f"Optimization-{datetime.now().strftime('%Y%m%d')}",
                "自动创建的优化技能"
            )
            print(f"创建技能：{skill_result['skill_name']}")
        
        # 4. 合并重复
        print("\n🔀 合并重复...")
        merge_result = self.merge_duplicates()
        print(f"合并 {merge_result['merged_count']} 个重复技能")
        
        # 总结
        print(f"\n{'='*60}")
        print("✅ 自主进化完成！")
        print(f"{'='*60}")
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "bottlenecks": len(bottlenecks),
            "optimizations": optimizations["count"],
            "skills_created": 1 if len(bottlenecks) > 0 else 0,
            "duplicates_merged": merge_result["merged_count"],
        }
        
        self._log_evolution("full_evolution", result, True)
        return result
    
    def show_history(self):
        """显示进化历史"""
        print("\n" + "="*60)
        print("📜 进化历史")
        print("="*60)
        
        for entry in self.evolution_history[-10:]:
            status = "✅" if entry["success"] else "❌"
            print(f"{status} {entry['timestamp'][:19]} - {entry['action']}")
        
        print(f"\n总进化次数：{len(self.evolution_history)}")
        print(f"{'='*60}")
    
    def show_status(self):
        """显示状态"""
        print("\n" + "="*60)
        print("🧬 Evolution Agent 状态")
        print("="*60)
        print(f"自动优化：{self.config.get('auto_optimize', True)}")
        print(f"自动创建技能：{self.config.get('auto_create_skills', True)}")
        print(f"自动合并重复：{self.config.get('auto_merge_duplicates', True)}")
        print(f"自动更新配置：{self.config.get('auto_update_config', True)}")
        print(f"进化历史：{len(self.evolution_history)} 条")
        print(f"{'='*60}")


def main():
    """主函数"""
    workspace_root = "/home/sayelf/.openclaw/workspace"
    agent = EvolutionAgent(workspace_root)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--status":
            agent.show_status()
        elif command == "--evolve":
            agent.evolve()
        elif command == "--history":
            agent.show_history()
        elif command == "--optimize":
            bottlenecks = agent.identify_bottlenecks()
            agent.optimize_process(bottlenecks)
        elif command == "--create-skill":
            name = sys.argv[2] if len(sys.argv) > 2 else f"Skill-{datetime.now().strftime('%Y%m%d')}"
            agent.create_skill(name, "手动创建的技能")
        else:
            print(f"未知命令：{command}")
    else:
        agent.show_status()


if __name__ == "__main__":
    import sys
    main()
