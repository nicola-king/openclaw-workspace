#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一全量智能自动化调用

功能:
1. 调用所有可用的 Scripts
2. 调用所有可用的 Skills
3. 智能错误处理
4. 结果聚合报告
5. 自动重试机制

作者：太一 AGI
创建：2026-04-14
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SCRIPTS_DIR = WORKSPACE / "scripts"
SKILLS_DIR = WORKSPACE / "skills"
LOGS_DIR = WORKSPACE / "logs"
REPORTS_DIR = WORKSPACE / "reports"

# 确保目录存在
LOGS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


@dataclass
class ExecutionResult:
    """执行结果"""
    name: str
    type: str  # script/skill
    success: bool
    duration_seconds: float
    error: Optional[str]
    timestamp: str
    retry_count: int = 0


class TaiyiFullAutoExecutor:
    """太一全量自动执行器"""
    
    def __init__(self, max_retries: int = 2, timeout_seconds: int = 300):
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        self.results: List[ExecutionResult] = []
        self.start_time = datetime.now()
        
        print(f"🚀 太一全量智能自动化调用启动")
        print(f"  最大重试：{max_retries} 次")
        print(f"  超时时间：{timeout_seconds} 秒")
        print(f"  开始时间：{self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def discover_scripts(self) -> List[Path]:
        """发现所有 Scripts"""
        scripts = []
        
        # 排除某些脚本
        exclude_patterns = [
            "test_",
            "__",
            "setup_",
            "config_",
        ]
        
        for script in SCRIPTS_DIR.glob("*.py"):
            # 排除测试和配置文件
            if any(script.name.startswith(p) for p in exclude_patterns):
                continue
            
            scripts.append(script)
        
        return sorted(scripts)
    
    def discover_skills(self) -> List[Path]:
        """发现所有可执行的 Skills"""
        skills = []
        
        # 查找有 main.py 或 run.py 的 Skill 目录
        for skill_dir in SKILLS_DIR.rglob("*"):
            if skill_dir.is_dir():
                # 查找主文件
                for main_file in ["main.py", "run.py", "skill.py"]:
                    main_path = skill_dir / main_file
                    if main_path.exists():
                        skills.append(main_path)
                        break
        
        return sorted(skills)
    
    def execute_script(self, script_path: Path) -> ExecutionResult:
        """执行单个 Script"""
        script_name = script_path.stem
        
        for attempt in range(self.max_retries + 1):
            try:
                start = datetime.now()
                
                # 执行
                result = subprocess.run(
                    ["python3", str(script_path)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds
                )
                
                duration = (datetime.now() - start).total_seconds()
                
                if result.returncode == 0:
                    return ExecutionResult(
                        name=script_name,
                        type="script",
                        success=True,
                        duration_seconds=duration,
                        error=None,
                        timestamp=start.isoformat(),
                        retry_count=attempt
                    )
                else:
                    raise RuntimeError(result.stderr[:500] if result.stderr else "Unknown error")
            
            except Exception as e:
                if attempt < self.max_retries:
                    print(f"  ⚠️ 重试 {attempt + 1}/{self.max_retries}: {script_name}")
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    return ExecutionResult(
                        name=script_name,
                        type="script",
                        success=False,
                        duration_seconds=0,
                        error=str(e)[:500],
                        timestamp=datetime.now().isoformat(),
                        retry_count=attempt
                    )
        
        # 不应该到这里
        return ExecutionResult(
            name=script_name,
            type="script",
            success=False,
            duration_seconds=0,
            error="Unknown error",
            timestamp=datetime.now().isoformat()
        )
    
    def execute_skill(self, skill_path: Path) -> ExecutionResult:
        """执行单个 Skill"""
        skill_name = skill_path.parent.name
        
        # 类似 Script 执行
        return self.execute_script(skill_path)
    
    def execute_all(self, include_scripts: bool = True, include_skills: bool = True):
        """执行所有任务"""
        print(f"\n📦 开始全量执行...")
        
        # 发现任务
        scripts = self.discover_scripts() if include_scripts else []
        skills = self.discover_skills() if include_skills else []
        
        total = len(scripts) + len(skills)
        print(f"  发现 Scripts: {len(scripts)} 个")
        print(f"  发现 Skills: {len(skills)} 个")
        print(f"  总计：{total} 个任务")
        
        # 执行 Scripts
        if include_scripts:
            print(f"\n📝 执行 Scripts...")
            for i, script in enumerate(scripts, 1):
                print(f"  [{i}/{len(scripts)}] {script.name}")
                result = self.execute_script(script)
                self.results.append(result)
                status = "✅" if result.success else "❌"
                print(f"    {status} {result.name} ({result.duration_seconds:.2f}s)")
        
        # 执行 Skills
        if include_skills:
            print(f"\n🎯 执行 Skills...")
            for i, skill in enumerate(skills, 1):
                print(f"  [{i}/{len(skills)}] {skill.parent.name}")
                result = self.execute_skill(skill)
                self.results.append(result)
                status = "✅" if result.success else "❌"
                print(f"    {status} {result.name} ({result.duration_seconds:.2f}s)")
        
        # 汇总
        self._print_summary()
    
    def _print_summary(self):
        """打印汇总"""
        total = len(self.results)
        success = sum(1 for r in self.results if r.success)
        failed = total - success
        total_duration = sum(r.duration_seconds for r in self.results)
        
        end_time = datetime.now()
        total_elapsed = (end_time - self.start_time).total_seconds()
        
        print(f"\n" + "=" * 60)
        print(f"📊 执行汇总")
        print(f"=" * 60)
        print(f"  总任务：{total} 个")
        print(f"  成功：{success} 个 ({success/max(total,1)*100:.1f}%)")
        print(f"  失败：{failed} 个 ({failed/max(total,1)*100:.1f}%)")
        print(f"  总耗时：{total_duration:.2f} 秒")
        print(f"  实际耗时：{total_elapsed:.2f} 秒")
        print(f"  平均耗时：{total_duration/max(total,1):.2f} 秒/任务")
        print(f"=" * 60)
    
    def generate_report(self, output_path: Optional[Path] = None) -> Path:
        """生成执行报告"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = REPORTS_DIR / f"full-auto-execution-report_{timestamp}.md"
        
        # 统计
        total = len(self.results)
        success = sum(1 for r in self.results if r.success)
        failed = total - success
        total_duration = sum(r.duration_seconds for r in self.results)
        
        # 按类型分组
        by_type = {}
        for r in self.results:
            if r.type not in by_type:
                by_type[r.type] = []
            by_type[r.type].append(r)
        
        # 生成报告
        content = f"""# 🚀 太一全量智能自动化调用报告

> **执行时间**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}  
> **完成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **状态**: {'✅ 完成' if success > 0 else '❌ 失败'}

---

## 📊 执行汇总

| 指标 | 数值 |
|------|------|
| **总任务** | {total} 个 |
| **成功** | {success} 个 ({success/max(total,1)*100:.1f}%) |
| **失败** | {failed} 个 ({failed/max(total,1)*100:.1f}%) |
| **总耗时** | {total_duration:.2f} 秒 |
| **实际耗时** | {(datetime.now() - self.start_time).total_seconds():.2f} 秒 |
| **平均耗时** | {total_duration/max(total,1):.2f} 秒/任务 |

---

## 📈 按类型统计

"""
        
        for type_name, results in by_type.items():
            type_success = sum(1 for r in results if r.success)
            content += f"### {type_name.title()}s\n\n"
            content += f"| 指标 | 数值 |\n"
            content += f"|------|------|\n"
            content += f"| 总数 | {len(results)} |\n"
            content += f"| 成功 | {type_success} |\n"
            content += f"| 失败 | {len(results) - type_success} |\n\n"
        
        # 失败任务详情
        failed_results = [r for r in self.results if not r.success]
        if failed_results:
            content += f"""## ❌ 失败任务详情

| 名称 | 类型 | 错误信息 | 重试次数 |
|------|------|---------|---------|
"""
            for r in failed_results[:20]:  # 只显示前 20 个
                error_msg = r.error[:100].replace("|", "/") if r.error else "N/A"
                content += f"| {r.name} | {r.type} | {error_msg} | {r.retry_count} |\n"
        
        # 成功任务列表
        content += f"""
## ✅ 成功任务列表

"""
        success_results = [r for r in self.results if r.success]
        for r in success_results[:50]:  # 只显示前 50 个
            content += f"- ✅ {r.name} ({r.type}, {r.duration_seconds:.2f}s)\n"
        
        if len(success_results) > 50:
            content += f"\n... 还有 {len(success_results) - 50} 个成功任务\n"
        
        content += f"""
---

*太一全量智能自动化调用报告 · 太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # 保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 报告已保存：{output_path}")
        return output_path
    
    def save_json_log(self, output_path: Optional[Path] = None) -> Path:
        """保存 JSON 日志"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = LOGS_DIR / f"full-auto-execution_{timestamp}.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        log_data = {
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "stats": {
                "total": len(self.results),
                "success": sum(1 for r in self.results if r.success),
                "failed": sum(1 for r in self.results if not r.success),
            },
            "results": [asdict(r) for r in self.results]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON 日志已保存：{output_path}")
        return output_path


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 太一全量智能自动化调用")
    print("=" * 60)
    
    # 创建执行器
    executor = TaiyiFullAutoExecutor(
        max_retries=2,
        timeout_seconds=300
    )
    
    # 执行所有
    executor.execute_all(
        include_scripts=True,
        include_skills=True
    )
    
    # 生成报告
    report_path = executor.generate_report()
    
    # 保存 JSON 日志
    json_path = executor.save_json_log()
    
    print(f"\n📁 输出文件:")
    print(f"  报告：{report_path}")
    print(f"  日志：{json_path}")
    
    print(f"\n" + "=" * 60)
    print("✅ 全量执行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
