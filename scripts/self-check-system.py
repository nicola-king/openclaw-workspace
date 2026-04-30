#!/usr/bin/env python3
"""
太一体系自检系统 - 全面健康检查

作者：太一 AGI
创建：2026-04-09
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
REPORTS_DIR = WORKSPACE / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


@dataclass
class CheckResult:
    """检查结果"""
    name: str
    status: str  # ok/warning/error
    details: str
    timestamp: str


class SelfCheckSystem:
    """自检系统"""
    
    def __init__(self):
        self.results = []
        self.warnings = []
        self.errors = []
    
    def check_agents(self) -> CheckResult:
        """检查 Agent 状态"""
        agents_dir = WORKSPACE / "agents"
        if not agents_dir.exists():
            return CheckResult(
                name="Agent 状态",
                status="error",
                details="agents 目录不存在",
                timestamp=datetime.now().isoformat()
            )
        
        agent_dirs = [d for d in agents_dir.iterdir() if d.is_dir()]
        count = len(agent_dirs)
        
        if count >= 4:
            status = "ok"
        elif count >= 1:
            status = "warning"
        else:
            status = "error"
        
        return CheckResult(
            name="Agent 状态",
            status=status,
            details=f"{count} 个 Agent: {[d.name for d in agent_dirs]}",
            timestamp=datetime.now().isoformat()
        )
    
    def check_skills(self) -> CheckResult:
        """检查 Skill 状态"""
        skills_dir = WORKSPACE / "skills"
        if not skills_dir.exists():
            return CheckResult(
                name="Skill 状态",
                status="error",
                details="skills 目录不存在",
                timestamp=datetime.now().isoformat()
            )
        
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        count = len(skill_dirs)
        
        if count >= 50:
            status = "ok"
        elif count >= 10:
            status = "warning"
        else:
            status = "error"
        
        return CheckResult(
            name="Skill 状态",
            status=status,
            details=f"{count} 个技能",
            timestamp=datetime.now().isoformat()
        )
    
    def check_crontab(self) -> CheckResult:
        """检查定时任务"""
        try:
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return CheckResult(
                    name="定时任务",
                    status="error",
                    details="Crontab 未安装",
                    timestamp=datetime.now().isoformat()
                )
            
            # 计算有效任务数
            lines = result.stdout.strip().split("\n")
            task_count = len([l for l in lines if l.strip() and not l.strip().startswith("#")])
            
            status = "ok" if task_count >= 10 else "warning"
            
            return CheckResult(
                name="定时任务",
                status=status,
                details=f"{task_count} 个定时任务",
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            return CheckResult(
                name="定时任务",
                status="error",
                details=str(e),
                timestamp=datetime.now().isoformat()
            )
    
    def check_dashboard(self, port: int, name: str) -> CheckResult:
        """检查 Dashboard 服务"""
        import urllib.request
        import urllib.error
        
        try:
            response = urllib.request.urlopen(f"http://localhost:{port}", timeout=5)
            status_code = response.getcode()
            
            if status_code == 200:
                return CheckResult(
                    name=f"{name} ({port})",
                    status="ok",
                    details=f"HTTP {status_code}",
                    timestamp=datetime.now().isoformat()
                )
            else:
                return CheckResult(
                    name=f"{name} ({port})",
                    status="warning",
                    details=f"HTTP {status_code}",
                    timestamp=datetime.now().isoformat()
                )
        except Exception as e:
            return CheckResult(
                name=f"{name} ({port})",
                status="error",
                details=str(e),
                timestamp=datetime.now().isoformat()
            )
    
    def check_gateway(self) -> CheckResult:
        """检查 Gateway 状态"""
        try:
            result = subprocess.run(
                ["systemctl", "--user", "status", "openclaw-gateway.service", "-n", "2", "--no-pager"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            output = result.stdout
            
            if "active (running)" in output:
                return CheckResult(
                    name="Gateway",
                    status="ok",
                    details="运行中",
                    timestamp=datetime.now().isoformat()
                )
            elif "inactive" in output or "failed" in output:
                return CheckResult(
                    name="Gateway",
                    status="error",
                    details="未运行或失败",
                    timestamp=datetime.now().isoformat()
                )
            else:
                return CheckResult(
                    name="Gateway",
                    status="warning",
                    details="状态未知",
                    timestamp=datetime.now().isoformat()
                )
        except Exception as e:
            return CheckResult(
                name="Gateway",
                status="error",
                details=str(e),
                timestamp=datetime.now().isoformat()
            )
    
    def check_git(self) -> CheckResult:
        """检查 Git 状态"""
        try:
            # 检查变更
            result = subprocess.run(
                ["git", "status", "-s"],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=WORKSPACE
            )
            
            changes = len([l for l in result.stdout.strip().split("\n") if l.strip()])
            
            if changes == 0:
                status = "ok"
                details = "工作区干净"
            elif changes < 10:
                status = "warning"
                details = f"{changes} 个未提交变更"
            else:
                status = "error"
                details = f"{changes} 个未提交变更 (过多)"
            
            return CheckResult(
                name="Git 状态",
                status=status,
                details=details,
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            return CheckResult(
                name="Git 状态",
                status="error",
                details=str(e),
                timestamp=datetime.now().isoformat()
            )
    
    def check_error_logs(self) -> CheckResult:
        """检查错误日志"""
        error_metrics = WORKSPACE / "logs" / "error_metrics.json"
        
        if not error_metrics.exists():
            return CheckResult(
                name="错误日志",
                status="ok",
                details="无错误记录",
                timestamp=datetime.now().isoformat()
            )
        
        try:
            with open(error_metrics, "r", encoding="utf-8") as f:
                metrics = json.load(f)
            
            total_errors = metrics.get("total_errors", 0)
            recurrence_rate = metrics.get("recurrence_rate", 0)
            
            if total_errors == 0:
                status = "ok"
                details = "无错误"
            elif recurrence_rate < 0.1:
                status = "ok"
                details = f"{total_errors} 个错误，重复率 {recurrence_rate:.1%}"
            elif recurrence_rate < 0.3:
                status = "warning"
                details = f"{total_errors} 个错误，重复率 {recurrence_rate:.1%} (偏高)"
            else:
                status = "error"
                details = f"{total_errors} 个错误，重复率 {recurrence_rate:.1%} (过高)"
            
            return CheckResult(
                name="错误日志",
                status=status,
                details=details,
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            return CheckResult(
                name="错误日志",
                status="error",
                details=str(e),
                timestamp=datetime.now().isoformat()
            )
    
    def check_core_files(self) -> CheckResult:
        """检查核心文件"""
        core_files = [
            WORKSPACE / "memory" / "user-model.json",
            WORKSPACE / "HEARTBEAT.md",
            WORKSPACE / "SOUL.md"
        ]
        
        missing = []
        for f in core_files:
            if not f.exists():
                missing.append(str(f))
        
        if missing:
            return CheckResult(
                name="核心文件",
                status="error",
                details=f"缺失：{missing}",
                timestamp=datetime.now().isoformat()
            )
        else:
            return CheckResult(
                name="核心文件",
                status="ok",
                details="全部存在",
                timestamp=datetime.now().isoformat()
            )
    
    def run_full_check(self) -> Dict:
        """运行全面自检"""
        print("🔍 太一体系自检系统")
        print("=" * 50)
        print()
        
        # 运行所有检查
        checks = [
            self.check_agents(),
            self.check_skills(),
            self.check_crontab(),
            self.check_dashboard(3000, "Bot Dashboard"),
            self.check_dashboard(8080, "ROI Dashboard"),
            self.check_dashboard(18789, "Gateway"),
            self.check_gateway(),
            self.check_git(),
            self.check_error_logs(),
            self.check_core_files()
        ]
        
        # 收集结果
        self.results = checks
        self.warnings = [r for r in checks if r.status == "warning"]
        self.errors = [r for r in checks if r.status == "error"]
        
        # 打印结果
        for result in checks:
            icon = "✅" if result.status == "ok" else "⚠️" if result.status == "warning" else "❌"
            print(f"{icon} {result.name}: {result.details}")
        
        print()
        print("=" * 50)
        print(f"总计：{len(checks)} 项检查")
        print(f"✅ 正常：{len(checks) - len(self.warnings) - len(self.errors)} 项")
        print(f"⚠️ 警告：{len(self.warnings)} 项")
        print(f"❌ 错误：{len(self.errors)} 项")
        print()
        
        # 生成报告
        report = self.generate_report()
        print(report)
        
        # 保存报告
        self.save_report(report)
        
        return {
            "total": len(checks),
            "ok": len(checks) - len(self.warnings) - len(self.errors),
            "warnings": len(self.warnings),
            "errors": len(self.errors),
            "results": [asdict(r) for r in checks]
        }
    
    def generate_report(self) -> str:
        """生成报告"""
        report = f"""# 太一体系自检报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 总体状态

- 检查项目：{len(self.results)} 项
- ✅ 正常：{len(self.results) - len(self.warnings) - len(self.errors)} 项
- ⚠️ 警告：{len(self.warnings)} 项
- ❌ 错误：{len(self.errors)} 项

## 检查结果

| 项目 | 状态 | 详情 |
|------|------|------|
"""
        for r in self.results:
            icon = "✅" if r.status == "ok" else "⚠️" if r.status == "warning" else "❌"
            report += f"| {r.name} | {icon} {r.status} | {r.details} |\n"
        
        if self.warnings or self.errors:
            report += """
## 需要关注

"""
            if self.warnings:
                report += "### 警告\n\n"
                for w in self.warnings:
                    report += f"- {w.name}: {w.details}\n"
            
            if self.errors:
                report += "\n### 错误\n\n"
                for e in self.errors:
                    report += f"- {e.name}: {e.details}\n"
        
        return report
    
    def save_report(self, report: str):
        """保存报告"""
        report_file = REPORTS_DIR / f"self-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"📄 报告已保存：{report_file}")


def main():
    """主函数"""
    checker = SelfCheckSystem()
    result = checker.run_full_check()
    
    # 返回状态码
    if result["errors"] > 0:
        sys.exit(1)
    elif result["warnings"] > 0:
        sys.exit(0)  # 警告不退出
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
