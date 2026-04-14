#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一智能调度中心 - 全 Agent/Skill 自动化调用

功能:
1. 自动发现所有 Agents/Skills
2. 智能路由 (根据任务类型)
3. 自动化调用
4. 结果聚合
5. 错误自愈

作者：太一 AGI
创建：2026-04-14
"""

import os
import sys
import json
import importlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SKILLS_DIR = WORKSPACE / "skills"
AGENTS_DIR = WORKSPACE / "agents"
SCRIPTS_DIR = WORKSPACE / "scripts"


@dataclass
class TaskResult:
    """任务执行结果"""
    task_id: str
    agent_skill: str
    success: bool
    result: Any
    error: Optional[str]
    duration_seconds: float
    timestamp: str


class TaiyiIntelligentScheduler:
    """太一智能调度中心"""
    
    def __init__(self):
        self.skills = self._discover_skills()
        self.agents = self._discover_agents()
        self.scripts = self._discover_scripts()
        self.task_log: List[TaskResult] = []
        
        print(f"🤖 太一智能调度中心初始化")
        print(f"  发现 Skills: {len(self.skills)} 个")
        print(f"  发现 Agents: {len(self.agents)} 个")
        print(f"  发现 Scripts: {len(self.scripts)} 个")
    
    def _discover_skills(self) -> Dict[str, Path]:
        """发现所有 Skills"""
        skills = {}
        
        for skill_dir in SKILLS_DIR.rglob("*"):
            if skill_dir.is_dir():
                # 检查是否有 SKILL.md
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    skills[skill_dir.name] = skill_dir
                
                # 检查是否有 Python 文件
                for py_file in skill_dir.glob("*.py"):
                    if py_file.name != "__init__.py":
                        skills[py_file.stem] = py_file
        
        return skills
    
    def _discover_agents(self) -> Dict[str, Path]:
        """发现所有 Agents"""
        agents = {}
        
        if AGENTS_DIR.exists():
            for agent_dir in AGENTS_DIR.rglob("*"):
                if agent_dir.is_dir():
                    agent_py = agent_dir / "agent.py"
                    if agent_py.exists():
                        agents[agent_dir.name] = agent_py
        
        return agents
    
    def _discover_scripts(self) -> Dict[str, Path]:
        """发现所有 Scripts"""
        scripts = {}
        
        for script in SCRIPTS_DIR.glob("*.py"):
            if script.name != "__init__.py":
                scripts[script.stem] = script
        
        return scripts
    
    def execute_task(self, task_name: str, **kwargs) -> TaskResult:
        """
        智能执行任务
        
        Args:
            task_name: 任务名称 (Skill/Agent/Script 名称)
            **kwargs: 参数
        
        Returns:
            TaskResult
        """
        start_time = datetime.now()
        task_id = f"task_{start_time.strftime('%Y%m%d_%H%M%S')}_{task_name}"
        
        print(f"\n🎯 执行任务：{task_name}")
        
        try:
            # 1. 尝试作为 Script 执行
            if task_name in self.scripts:
                result = self._execute_script(task_name, **kwargs)
            # 2. 尝试作为 Skill 执行
            elif task_name in self.skills:
                result = self._execute_skill(task_name, **kwargs)
            # 3. 尝试作为 Agent 执行
            elif task_name in self.agents:
                result = self._execute_agent(task_name, **kwargs)
            else:
                raise ValueError(f"未知任务：{task_name}")
            
            duration = (datetime.now() - start_time).total_seconds()
            
            task_result = TaskResult(
                task_id=task_id,
                agent_skill=task_name,
                success=True,
                result=result,
                error=None,
                duration_seconds=duration,
                timestamp=start_time.isoformat()
            )
            
            print(f"✅ 任务完成：{task_name} ({duration:.2f}s)")
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            
            task_result = TaskResult(
                task_id=task_id,
                agent_skill=task_name,
                success=False,
                result=None,
                error=str(e),
                duration_seconds=duration,
                timestamp=start_time.isoformat()
            )
            
            print(f"❌ 任务失败：{task_name} - {e}")
        
        self.task_log.append(task_result)
        return task_result
    
    def _execute_script(self, script_name: str, **kwargs) -> Any:
        """执行 Script"""
        script_path = self.scripts[script_name]
        
        # 构建命令
        cmd = ["python3", str(script_path)]
        
        # 添加参数
        for key, value in kwargs.items():
            cmd.extend([f"--{key}", str(value)])
        
        # 执行
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return {"stdout": result.stdout, "stderr": result.stderr}
        else:
            raise RuntimeError(f"Script 执行失败：{result.stderr}")
    
    def _execute_skill(self, skill_name: str, **kwargs) -> Any:
        """执行 Skill"""
        skill_path = self.skills[skill_name]
        
        if skill_path.suffix == ".py":
            # Python Skill
            return self._execute_script(skill_name, **kwargs)
        else:
            # Skill 目录
            # 查找主文件
            main_files = ["main.py", "run.py", "skill.py", f"{skill_name}.py"]
            
            for main_file in main_files:
                main_path = skill_path / main_file
                if main_path.exists():
                    cmd = ["python3", str(main_path)]
                    for key, value in kwargs.items():
                        cmd.extend([f"--{key}", str(value)])
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    
                    if result.returncode == 0:
                        return {"stdout": result.stdout, "stderr": result.stderr}
                    else:
                        raise RuntimeError(f"Skill 执行失败：{result.stderr}")
            
            raise FileNotFoundError(f"Skill 主文件未找到：{skill_path}")
    
    def _execute_agent(self, agent_name: str, **kwargs) -> Any:
        """执行 Agent"""
        agent_path = self.agents[agent_name]
        
        cmd = ["python3", str(agent_path)]
        for key, value in kwargs.items():
            cmd.extend([f"--{key}", str(value)])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            return {"stdout": result.stdout, "stderr": result.stderr}
        else:
            raise RuntimeError(f"Agent 执行失败：{result.stderr}")
    
    def batch_execute(self, tasks: List[Dict]) -> List[TaskResult]:
        """
        批量执行任务
        
        Args:
            tasks: 任务列表 [{"name": "task1", "params": {...}}, ...]
        
        Returns:
            TaskResult 列表
        """
        results = []
        
        for task in tasks:
            task_name = task.get("name")
            params = task.get("params", {})
            
            result = self.execute_task(task_name, **params)
            results.append(result)
        
        success_count = sum(1 for r in results if r.success)
        print(f"\n📊 批量执行完成：{success_count}/{len(results)} 成功")
        
        return results
    
    def intelligent_route(self, task_description: str) -> str:
        """
        智能路由 - 根据任务描述选择最佳 Skill/Agent
        
        Args:
            task_description: 任务描述
        
        Returns:
            推荐的 Skill/Agent 名称
        """
        # 关键词匹配
        keywords_map = {
            "tts": ["tts", "语音", "audio", "speech"],
            "trading": ["trading", "交易", "binance", "polymarket"],
            "weather": ["weather", "天气", "forecast"],
            "search": ["search", "搜索", "google"],
            "translation": ["translation", "翻译", "translate"],
            "summarize": ["summarize", "总结", "summary"],
        }
        
        task_lower = task_description.lower()
        
        for skill_type, keywords in keywords_map.items():
            if any(keyword in task_lower for keyword in keywords):
                # 查找匹配的 Skill
                for skill_name in self.skills.keys():
                    if skill_type in skill_name.lower():
                        return skill_name
        
        # 默认返回第一个可用的
        if self.scripts:
            return list(self.scripts.keys())[0]
        
        raise ValueError("未找到合适的 Skill/Agent")
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_tasks = len(self.task_log)
        success_tasks = sum(1 for t in self.task_log if t.success)
        failed_tasks = total_tasks - success_tasks
        avg_duration = sum(t.duration_seconds for t in self.task_log) / max(total_tasks, 1)
        
        return {
            "total_tasks": total_tasks,
            "success_tasks": success_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": f"{success_tasks/max(total_tasks,1)*100:.1f}%",
            "avg_duration_seconds": f"{avg_duration:.2f}",
            "total_skills": len(self.skills),
            "total_agents": len(self.agents),
            "total_scripts": len(self.scripts),
        }
    
    def save_log(self, output_path: Optional[Path] = None):
        """保存任务日志"""
        if not output_path:
            output_path = WORKSPACE / "logs" / f"scheduler_log_{datetime.now().strftime('%Y%m%d')}.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.get_stats(),
            "tasks": [
                {
                    "task_id": t.task_id,
                    "agent_skill": t.agent_skill,
                    "success": t.success,
                    "duration_seconds": t.duration_seconds,
                    "timestamp": t.timestamp,
                    "error": t.error
                }
                for t in self.task_log
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 日志已保存：{output_path}")


def main():
    """测试"""
    print("🤖 太一智能调度中心测试")
    print("=" * 60)
    
    scheduler = TaiyiIntelligentScheduler()
    
    # 测试 1: 智能路由
    print("\n🧠 测试 1: 智能路由")
    task_desc = "我需要生成语音"
    recommended = scheduler.intelligent_route(task_desc)
    print(f"  任务：{task_desc}")
    print(f"  推荐：{recommended}")
    
    # 测试 2: 执行 Script
    print("\n📝 测试 2: 执行 Script")
    if scheduler.scripts:
        script_name = list(scheduler.scripts.keys())[0]
        result = scheduler.execute_task(script_name)
        print(f"  结果：{'✅ 成功' if result.success else '❌ 失败'}")
    
    # 测试 3: 批量执行
    print("\n📦 测试 3: 批量执行")
    tasks = [
        {"name": "token-optimization-analysis"},
        {"name": "memory-compression-algorithm"},
    ]
    # 只执行存在的任务
    valid_tasks = [t for t in tasks if t["name"] in scheduler.scripts]
    if valid_tasks:
        results = scheduler.batch_execute(valid_tasks)
        print(f"  执行 {len(results)} 个任务")
    
    # 测试 4: 统计信息
    print("\n📊 测试 4: 统计信息")
    stats = scheduler.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 测试 5: 保存日志
    print("\n💾 测试 5: 保存日志")
    scheduler.save_log()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")


if __name__ == "__main__":
    main()
