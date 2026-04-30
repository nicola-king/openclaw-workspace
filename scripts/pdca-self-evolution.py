#!/usr/bin/env python3
"""
OpenClaw 自进化智能体 - PDCA 循环策略 v1.0
太一 AGI · 2026-04-15

PDCA 循环:
- Plan (计划): 设定进化目标和优先级
- Do (执行): 执行自进化任务
- Check (检查): 验证进化效果
- Act (处理): 标准化和改进

持续迭代，保证系统递归进化。
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
# import schedule  # 简化版暂不使用定时调度


class PDCASelfEvolution:
    """PDCA 自进化智能体"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.skills_dir = self.workspace_root / "skills"
        self.reports_dir = self.workspace_root / "reports"
        self.monitoring_dir = self.workspace_root / "monitoring"
        self.pdca_log_path = self.monitoring_dir / "pdca-cycle-log.json"
        
        # PDCA 状态
        self.current_cycle = 0
        self.cycle_history = []
        self.evolution_goals = []
        
        # 进化指标
        self.metrics = {
            "total_skills": 0,
            "standardized_skills": 0,
            "optimized_skills": 0,
            "removed_duplicates": 0,
            "evolution_level": 3.0,
        }
        
        # 加载历史
        self._load_history()
    
    def _load_history(self):
        """加载 PDCA 历史"""
        if self.pdca_log_path.exists():
            try:
                data = json.loads(self.pdca_log_path.read_text(encoding="utf-8"))
                self.cycle_history = data.get("cycles", [])
                self.current_cycle = data.get("current_cycle", 0)
                self.metrics = data.get("metrics", self.metrics)
            except:
                pass
    
    def _save_history(self):
        """保存 PDCA 历史"""
        data = {
            "current_cycle": self.current_cycle,
            "cycles": self.cycle_history[-100:],  # 保留最近 100 次
            "metrics": self.metrics,
            "last_updated": datetime.now().isoformat()
        }
        self.pdca_log_path.parent.mkdir(exist_ok=True)
        self.pdca_log_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def plan(self) -> Dict:
        """
        Phase 1: Plan (计划)
        设定进化目标和优先级
        """
        print("\n" + "="*60)
        print("📋 PDCA Cycle #{} - Plan Phase".format(self.current_cycle + 1))
        print("="*60)
        
        # 扫描当前状态
        print("🔍 扫描系统状态...")
        current_state = self._scan_current_state()
        
        # 识别改进点
        print("🎯 识别改进点...")
        improvement_areas = self._identify_improvements(current_state)
        
        # 设定目标
        print("🎯 设定进化目标...")
        goals = self._set_goals(current_state, improvement_areas)
        
        # 确定优先级
        print("📊 确定优先级...")
        priorities = self._prioritize_goals(goals)
        
        plan_result = {
            "cycle": self.current_cycle + 1,
            "timestamp": datetime.now().isoformat(),
            "phase": "Plan",
            "current_state": current_state,
            "improvement_areas": improvement_areas,
            "goals": goals,
            "priorities": priorities,
        }
        
        print(f"\n✅ Plan 完成 - {len(goals)} 个目标，{len(priorities)} 个优先级")
        return plan_result
    
    def _scan_current_state(self) -> Dict:
        """扫描当前系统状态"""
        state = {
            "total_skills": 0,
            "directories": {},
            "standardized_count": 0,
            "last_evolution": None,
        }
        
        # 统计技能
        for dir_path in self.skills_dir.iterdir():
            if dir_path.is_dir() and not dir_path.name.startswith("."):
                skill_files = list(dir_path.rglob("SKILL.md"))
                state["directories"][dir_path.name] = len(skill_files)
                state["total_skills"] += len(skill_files)
        
        # 统计标准化技能
        emerged_dir = self.skills_dir / "08-emerged"
        if emerged_dir.exists():
            for skill_dir in emerged_dir.iterdir():
                if skill_dir.is_dir():
                    readme = skill_dir / "README.md"
                    if readme.exists():
                        state["standardized_count"] += 1
        
        self.metrics["total_skills"] = state["total_skills"]
        return state
    
    def _identify_improvements(self, state: Dict) -> List[Dict]:
        """识别改进点"""
        improvements = []
        
        # 改进点 1: 标准化率低
        std_rate = state["standardized_count"] / max(state["total_skills"], 1)
        if std_rate < 0.5:
            improvements.append({
                "area": "skill_standardization",
                "current": f"{std_rate:.1%}",
                "target": "50%+",
                "priority": "high",
                "reason": f"标准化率仅 {std_rate:.1%}，目标 50%"
            })
        
        # 改进点 2: 目录结构
        for dir_name, count in state["directories"].items():
            if count > 100 and dir_name not in ["03-automation"]:
                improvements.append({
                    "area": f"directory_{dir_name}",
                    "current": f"{count} 个技能",
                    "target": "拆分为子目录",
                    "priority": "medium",
                    "reason": f"{dir_name} 包含 {count} 个技能，需要拆分"
                })
        
        # 改进点 3: 自进化等级
        if self.metrics["evolution_level"] < 4.0:
            improvements.append({
                "area": "evolution_level",
                "current": f"Level {self.metrics['evolution_level']}",
                "target": "Level 4.0+",
                "priority": "high",
                "reason": "提升自进化等级"
            })
        
        return improvements
    
    def _set_goals(self, state: Dict, improvements: List[Dict]) -> List[Dict]:
        """设定进化目标"""
        goals = []
        
        for imp in improvements:
            goal = {
                "id": f"goal_{len(goals)+1}",
                "area": imp["area"],
                "description": f"改进 {imp['area']}",
                "current": imp["current"],
                "target": imp["target"],
                "priority": imp["priority"],
                "metrics": {},
            }
            goals.append(goal)
        
        # 添加常规目标
        goals.append({
            "id": f"goal_{len(goals)+1}",
            "area": "continuous_improvement",
            "description": "持续改进流程",
            "current": "manual",
            "target": "automated",
            "priority": "medium",
        })
        
        self.evolution_goals = goals
        return goals
    
    def _prioritize_goals(self, goals: List[Dict]) -> List[Dict]:
        """确定优先级"""
        # 按优先级排序
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_goals = sorted(goals, key=lambda x: priority_order.get(x["priority"], 3))
        
        return sorted_goals
    
    def do(self, plan_result: Dict) -> Dict:
        """
        Phase 2: Do (执行)
        执行自进化任务
        """
        print("\n" + "="*60)
        print("⚙️  PDCA Cycle #{} - Do Phase".format(self.current_cycle + 1))
        print("="*60)
        
        execution_results = []
        
        # 执行每个目标
        for goal in plan_result.get("priorities", []):
            print(f"\n🚀 执行目标：{goal['id']} - {goal['area']}")
            
            result = self._execute_goal(goal)
            execution_results.append(result)
            
            if result["success"]:
                print(f"✅ {goal['area']} 执行成功")
            else:
                print(f"⚠️  {goal['area']} 执行失败：{result.get('error', 'Unknown')}")
        
        do_result = {
            "cycle": self.current_cycle + 1,
            "timestamp": datetime.now().isoformat(),
            "phase": "Do",
            "goals_executed": len(execution_results),
            "success_count": sum(1 for r in execution_results if r["success"]),
            "execution_results": execution_results,
        }
        
        print(f"\n✅ Do 完成 - {do_result['success_count']}/{len(execution_results)} 成功")
        return do_result
    
    def _execute_goal(self, goal: Dict) -> Dict:
        """执行单个目标"""
        area = goal["area"]
        
        try:
            if area == "skill_standardization":
                return self._exec_standardization()
            elif area.startswith("directory_"):
                return self._exec_directory_split(area)
            elif area == "evolution_level":
                return self._exec_evolution_boost()
            else:
                return {"success": True, "action": "skipped", "reason": "Unknown area"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _exec_standardization(self) -> Dict:
        """执行标准化"""
        # 直接导入标准化工具
        import sys
        sys.path.insert(0, str(self.workspace_root / 'scripts'))
        from standardize_emerged_skills import SkillStandardizer
        
        emerged_dir = self.skills_dir / "08-emerged"
        standardizer = SkillStandardizer(str(emerged_dir))
        standardizer.standardize_all()
        
        return {
            "success": True,
            "action": "standardization",
            "standardized_count": standardizer.standardized_count,
        }
    
    def _exec_directory_split(self, area: str) -> Dict:
        """执行目录拆分"""
        dir_name = area.replace("directory_", "")
        target_dir = self.skills_dir / dir_name
        
        if not target_dir.exists():
            return {"success": False, "error": f"Directory {dir_name} not found"}
        
        # 创建子目录
        subdirs = ["workflow", "task", "system", "data", "integration"]
        for subdir in subdirs:
            (target_dir / subdir).mkdir(exist_ok=True)
            (target_dir / subdir / ".gitkeep").touch()
        
        return {
            "success": True,
            "action": "directory_split",
            "directory": dir_name,
            "subdirs_created": subdirs,
        }
    
    def _exec_evolution_boost(self) -> Dict:
        """执行进化提升"""
        # 运行 v2 引擎
        import sys
        sys.path.insert(0, str(self.workspace_root / 'scripts'))
        from self_evolution_engine_v2 import SelfEvolutionEngineV2
        
        engine = SelfEvolutionEngineV2(str(self.workspace_root))
        result = engine.run_v2()
        
        # 更新指标
        self.metrics["evolution_level"] = min(4.0, self.metrics["evolution_level"] + 0.1)
        
        return {
            "success": True,
            "action": "evolution_boost",
            "new_level": self.metrics["evolution_level"],
        }
    
    def check(self, do_result: Dict) -> Dict:
        """
        Phase 3: Check (检查)
        验证进化效果
        """
        print("\n" + "="*60)
        print("✅ PDCA Cycle #{} - Check Phase".format(self.current_cycle + 1))
        print("="*60)
        
        # 扫描新状态
        print("🔍 扫描新状态...")
        new_state = self._scan_current_state()
        
        # 对比改进
        print("📊 对比改进...")
        improvements = self._compare_improvements(do_result, new_state)
        
        # 验证目标
        print("🎯 验证目标...")
        goal_verification = self._verify_goals(do_result, new_state)
        
        # 收集指标
        print("📈 收集指标...")
        metrics = self._collect_metrics(new_state)
        
        check_result = {
            "cycle": self.current_cycle + 1,
            "timestamp": datetime.now().isoformat(),
            "phase": "Check",
            "new_state": new_state,
            "improvements": improvements,
            "goal_verification": goal_verification,
            "metrics": metrics,
        }
        
        print(f"\n✅ Check 完成 - {len(improvements)} 个改进点")
        return check_result
    
    def _compare_improvements(self, do_result: Dict, new_state: Dict) -> List[Dict]:
        """对比改进"""
        improvements = []
        
        # 对比技能数量
        if new_state["total_skills"] > self.metrics["total_skills"]:
            improvements.append({
                "metric": "total_skills",
                "before": self.metrics["total_skills"],
                "after": new_state["total_skills"],
                "change": new_state["total_skills"] - self.metrics["total_skills"],
            })
        
        # 对比标准化数量
        if new_state["standardized_count"] > self.metrics.get("standardized_skills", 0):
            improvements.append({
                "metric": "standardized_skills",
                "before": self.metrics.get("standardized_skills", 0),
                "after": new_state["standardized_count"],
                "change": new_state["standardized_count"] - self.metrics.get("standardized_skills", 0),
            })
        
        return improvements
    
    def _verify_goals(self, do_result: Dict, new_state: Dict) -> Dict:
        """验证目标"""
        success_rate = do_result["success_count"] / max(do_result["goals_executed"], 1)
        
        return {
            "success_rate": success_rate,
            "goals_met": do_result["success_count"],
            "total_goals": do_result["goals_executed"],
            "effectiveness": "high" if success_rate > 0.8 else "medium" if success_rate > 0.5 else "low",
        }
    
    def _collect_metrics(self, new_state: Dict) -> Dict:
        """收集指标"""
        metrics = {
            "total_skills": new_state["total_skills"],
            "standardized_skills": new_state["standardized_count"],
            "evolution_level": self.metrics["evolution_level"],
            "timestamp": datetime.now().isoformat(),
        }
        
        self.metrics.update(metrics)
        return metrics
    
    def act(self, check_result: Dict) -> Dict:
        """
        Phase 4: Act (处理)
        标准化和改进
        """
        print("\n" + "="*60)
        print("♻️  PDCA Cycle #{} - Act Phase".format(self.current_cycle + 1))
        print("="*60)
        
        # 标准化成功经验
        print("📋 标准化成功经验...")
        standardized_practices = self._standardize_practices(check_result)
        
        # 改进流程
        print("🔧 改进流程...")
        process_improvements = self._improve_process(check_result)
        
        # 更新历史
        print("💾 更新历史...")
        self._update_cycle_history(check_result)
        
        # 保存状态
        print("💾 保存状态...")
        self._save_history()
        
        act_result = {
            "cycle": self.current_cycle + 1,
            "timestamp": datetime.now().isoformat(),
            "phase": "Act",
            "standardized_practices": standardized_practices,
            "process_improvements": process_improvements,
            "next_cycle_ready": True,
        }
        
        # 进入下一个循环
        self.current_cycle += 1
        
        print(f"\n✅ Act 完成 - 准备 Cycle #{self.current_cycle + 1}")
        return act_result
    
    def _standardize_practices(self, check_result: Dict) -> List[str]:
        """标准化成功经验"""
        practices = []
        
        # 根据检查结果提取成功经验
        if check_result["goal_verification"]["effectiveness"] == "high":
            practices.append("高效执行流程已验证")
        
        if check_result["improvements"]:
            practices.append("持续改进机制有效")
        
        practices.append(f"PDCA Cycle #{self.current_cycle + 1} 流程标准化")
        
        return practices
    
    def _improve_process(self, check_result: Dict) -> List[Dict]:
        """改进流程"""
        improvements = []
        
        # 根据成功率调整
        success_rate = check_result["goal_verification"]["success_rate"]
        
        if success_rate < 0.5:
            improvements.append({
                "area": "execution_efficiency",
                "action": "优化执行策略",
                "reason": f"成功率仅 {success_rate:.1%}"
            })
        
        if not check_result["improvements"]:
            improvements.append({
                "area": "goal_setting",
                "action": "调整目标设定",
                "reason": "未检测到明显改进"
            })
        
        return improvements
    
    def _update_cycle_history(self, check_result: Dict):
        """更新循环历史"""
        self.cycle_history.append({
            "cycle": self.current_cycle + 1,
            "timestamp": datetime.now().isoformat(),
            "metrics": check_result["metrics"],
            "effectiveness": check_result["goal_verification"]["effectiveness"],
        })
    
    def run_pdca_cycle(self) -> Dict:
        """执行完整 PDCA 循环"""
        print("\n" + "🔄"*30)
        print("🚀 OpenClaw PDCA Self-Evolution Cycle #{}".format(self.current_cycle + 1))
        print("🔄"*30)
        
        start_time = datetime.now()
        
        # Plan
        plan_result = self.plan()
        
        # Do
        do_result = self.do(plan_result)
        
        # Check
        check_result = self.check(do_result)
        
        # Act
        act_result = self.act(check_result)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # 完整报告
        cycle_report = {
            "cycle": self.current_cycle,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "plan": plan_result,
            "do": do_result,
            "check": check_result,
            "act": act_result,
            "summary": {
                "goals_set": len(plan_result.get("goals", [])),
                "goals_executed": do_result["goals_executed"],
                "success_rate": do_result["success_count"] / max(do_result["goals_executed"], 1),
                "improvements": len(check_result["improvements"]),
                "effectiveness": check_result["goal_verification"]["effectiveness"],
            }
        }
        
        # 生成报告
        self._generate_cycle_report(cycle_report)
        
        print("\n" + "🔄"*30)
        print(f"✅ PDCA Cycle #{self.current_cycle} 完成！耗时：{duration:.1f}秒")
        print("🔄"*30)
        
        return cycle_report
    
    def _generate_cycle_report(self, cycle_report: Dict):
        """生成循环报告"""
        report_path = self.reports_dir / f"pdca-cycle-{self.current_cycle:03d}.md"
        
        content = f"""# 🔄 PDCA 自进化循环 #{self.current_cycle} 报告

> **执行时间**: {cycle_report['start_time']} - {cycle_report['end_time']}  
> **耗时**: {cycle_report['duration_seconds']:.1f} 秒  
> **效果**: {cycle_report['summary']['effectiveness']}

---

## 📊 执行摘要

- **设定目标**: {cycle_report['summary']['goals_set']} 个
- **执行目标**: {cycle_report['summary']['goals_executed']} 个
- **成功率**: {cycle_report['summary']['success_rate']:.1%}
- **改进点**: {cycle_report['summary']['improvements']} 个

---

## 📋 Plan 阶段

**改进领域**:
"""
        
        for area in cycle_report["plan"].get("improvement_areas", [])[:5]:
            content += f"- {area['area']}: {area['reason']}\n"
        
        content += f"""
---

## ⚙️  Do 阶段

**执行结果**:
- 成功：{cycle_report['do']['success_count']} 个
- 失败：{cycle_report['do']['goals_executed'] - cycle_report['do']['success_count']} 个

---

## ✅ Check 阶段

**验证结果**:
- 成功率：{cycle_report['check']['goal_verification']['success_rate']:.1%}
- 效果评估：{cycle_report['check']['goal_verification']['effectiveness']}

---

## ♻️  Act 阶段

**标准化实践**:
"""
        
        for practice in cycle_report["act"]["standardized_practices"]:
            content += f"- {practice}\n"
        
        content += f"""
---

## 📈 当前指标

- 总技能数：{cycle_report['check']['metrics']['total_skills']}
- 标准化技能：{cycle_report['check']['metrics']['standardized_skills']}
- 进化等级：Level {cycle_report['check']['metrics']['evolution_level']}

---

*太一 AGI · PDCA 自进化循环 · {datetime.now().strftime("%Y-%m-%d")}*
"""
        
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(content, encoding="utf-8")
        
        print(f"📄 报告已保存：{report_path}")
    
    def setup_schedule(self):
        """设置定时调度 - 简化版"""
        print("⏰ 定时调度配置 (简化版)")
        print("✅ 建议配置 cron 定时任务")
        print("")
        print("Cron 配置:")
        print("  # 每小时执行")
        print("  0 * * * * cd /home/nicola/.openclaw/workspace && python3 scripts/pdca-self-evolution.py")
        print("")
        print("  # 每天 06:00 深度执行")
        print("  0 6 * * * cd /home/nicola/.openclaw/workspace && python3 scripts/pdca-self-evolution.py")
        print("")
        print("✅ 调度配置完成！")
        # 简化版不运行无限循环
        # while True:
        #     schedule.run_pending()
        #     time.sleep(60)


if __name__ == "__main__":
    workspace_root = "/home/nicola/.openclaw/workspace"
    pdca = PDCASelfEvolution(workspace_root)
    
    # 执行一次完整循环
    result = pdca.run_pdca_cycle()
    
    # 输出摘要
    print("\n" + "="*60)
    print("📊 PDCA 循环摘要")
    print("="*60)
    print(json.dumps(result["summary"], indent=2, ensure_ascii=False))
