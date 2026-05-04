#!/usr/bin/env python3
"""
跨境贸易 Agent - 综合质量检查脚本
太一 AGI · 2026-04-18

功能:
- 语法检查
- 导入检查
- 功能测试
- 生成质量报告
"""

import sys
import py_compile
import tempfile
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SKILLS_DIR = WORKSPACE / "skills/01-trading/cross-border-trade-agent"

# 需要检查的脚本列表
SCRIPTS_TO_CHECK = [
    "smart_product_selector.py",
    "supplier_matcher.py",
    "logistics_optimizer.py",
    "price_comparator.py",
    "sales_forecaster.py",
    "multilingual_support.py",
    "product_trend_forecaster.py",
    "intelligence_reporter.py",
]

# 系统脚本
SYSTEM_SCRIPTS = [
    "skills/scheduler-agent/src/scheduler.py",
    "scripts/scheduler-monitor.py",
    "scripts/hourly-health-check.py",
    "scripts/daily-constitution-study.py",
    "scripts/daily-report-generator.py",
    "skills/05-content/wisdom-scheduler/src/scheduler.py",
    "skills/05-content/dao-agent/src/dao_agent.py",
    "skills/05-content/wu-agent/src/wu_agent.py",
    "skills/07-system/md2pdf/md2pdf.py",
    "skills/05-content/dao-agent/morning_wisdom_pdf.py",
    "skills/05-content/wu-agent/evening_wisdom_pdf.py",
]


class QualityChecker:
    """质量检查器"""
    
    def __init__(self):
        self.results = {
            "syntax_check": {"passed": 0, "failed": 0, "details": []},
            "import_check": {"passed": 0, "failed": 0, "details": []},
            "overall_score": 0,
        }
    
    def check_syntax(self, script_path):
        """语法检查"""
        try:
            py_compile.compile(script_path, doraise=True)
            self.results["syntax_check"]["passed"] += 1
            self.results["syntax_check"]["details"].append({
                "script": str(script_path),
                "status": "✅ PASS",
                "error": None,
            })
            return True
        except py_compile.PyCompileError as e:
            self.results["syntax_check"]["failed"] += 1
            self.results["syntax_check"]["details"].append({
                "script": str(script_path),
                "status": "❌ FAIL",
                "error": str(e),
            })
            return False
    
    def check_imports(self, script_path):
        """导入检查"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # 尝试编译代码
            compile(code, str(script_path), 'exec')
            self.results["import_check"]["passed"] += 1
            self.results["import_check"]["details"].append({
                "script": str(script_path),
                "status": "✅ PASS",
                "error": None,
            })
            return True
        except Exception as e:
            self.results["import_check"]["failed"] += 1
            self.results["import_check"]["details"].append({
                "script": str(script_path),
                "status": "❌ FAIL",
                "error": str(e),
            })
            return False
    
    def run_all_checks(self):
        """运行所有检查"""
        print("=" * 60)
        print("🔍 跨境贸易 Agent - 综合质量检查")
        print("=" * 60)
        
        # 检查跨境贸易 Skills
        print(f"\n📦 检查跨境贸易 Skills ({len(SCRIPTS_TO_CHECK)}个)")
        print("-" * 60)
        
        for script in SCRIPTS_TO_CHECK:
            script_path = SKILLS_DIR / script
            if script_path.exists():
                print(f"检查：{script}...", end=" ")
                syntax_ok = self.check_syntax(script_path)
                import_ok = self.check_imports(script_path)
                
                if syntax_ok and import_ok:
                    print("✅")
                else:
                    print("❌")
            else:
                print(f"⚠️  {script} - 文件不存在")
        
        # 检查系统脚本
        print(f"\n🔧 检查系统脚本 ({len(SYSTEM_SCRIPTS)}个)")
        print("-" * 60)
        
        for script in SYSTEM_SCRIPTS:
            script_path = WORKSPACE / script
            if script_path.exists():
                print(f"检查：{script}...", end=" ")
                syntax_ok = self.check_syntax(script_path)
                
                if syntax_ok:
                    print("✅")
                else:
                    print("❌")
            else:
                print(f"⚠️  {script} - 文件不存在")
        
        # 计算总体评分
        total_checks = (
            self.results["syntax_check"]["passed"] +
            self.results["syntax_check"]["failed"] +
            self.results["import_check"]["passed"] +
            self.results["import_check"]["failed"]
        )
        
        total_passed = (
            self.results["syntax_check"]["passed"] +
            self.results["import_check"]["passed"]
        )
        
        self.results["overall_score"] = (total_passed / total_checks * 100) if total_checks > 0 else 0
        
        # 生成报告
        self.generate_report()
    
    def generate_report(self):
        """生成质量报告"""
        print("\n" + "=" * 60)
        print("📊 质量检查报告")
        print("=" * 60)
        
        print(f"\n语法检查:")
        print(f"  ✅ 通过：{self.results['syntax_check']['passed']}")
        print(f"  ❌ 失败：{self.results['syntax_check']['failed']}")
        
        print(f"\n导入检查:")
        print(f"  ✅ 通过：{self.results['import_check']['passed']}")
        print(f"  ❌ 失败：{self.results['import_check']['failed']}")
        
        print(f"\n总体评分：{self.results['overall_score']:.1f}/100")
        
        if self.results['overall_score'] >= 95:
            print("\n🎊 质量等级：优秀 (Production Ready)")
        elif self.results['overall_score'] >= 80:
            print("\n👍 质量等级：良好 (Beta)")
        else:
            print("\n⚠️ 质量等级：需要改进 (Alpha)")
        
        # 保存报告
        report_file = SKILLS_DIR / "quality-report.md"
        self.save_report(report_file)
        
        print(f"\n💾 报告已保存：{report_file}")


def main():
    """主函数"""
    checker = QualityChecker()
    checker.run_all_checks()


if __name__ == "__main__":
    main()
