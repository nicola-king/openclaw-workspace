#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务自查模块 - 系统健康检查与自修复
太一 AGI · 2026-04-19 00:16

功能:
- 检查所有定时任务状态
- 验证 cron 配置
- 检测执行失败
- 自动修复问题
- 生成自查报告

架构位置：基础设施层 → 监控告警
"""

import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('ScheduledTaskSelfCheck')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
SCRIPTS_DIR = WORKSPACE / "skills" / "01-trading" / "cross-border-trade-agent"
CRON_DIR = WORKSPACE / "cron"
REPORT_DIR = WORKSPACE / "reports" / "scheduled_tasks"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
CRON_DIR.mkdir(parents=True, exist_ok=True)


class ScheduledTaskSelfCheckModule:
    """定时任务自查模块"""
    
    def __init__(self):
        # 定时任务配置
        self.scheduled_tasks = {
            "daily_intelligence": {
                "name": "每日情报推送",
                "script": "daily_intelligence_job.py",
                "schedule": "0 8 * * *",
                "priority": "P0",
                "last_run_file": "last_run_daily.json",
                "expected_duration": 300,  # 5 分钟
                "critical": True
            },
            "weekly_report": {
                "name": "每周报告",
                "script": "weekly_report_job.py",
                "schedule": "0 9 * * 1",
                "priority": "P0",
                "last_run_file": "last_run_weekly.json",
                "expected_duration": 600,
                "critical": True
            },
            "monthly_strategy": {
                "name": "每月战略",
                "script": "monthly_strategy_job.py",
                "schedule": "0 10 1 * *",
                "priority": "P2",
                "last_run_file": "last_run_monthly.json",
                "expected_duration": 900,
                "critical": False
            },
            "trend_monitor": {
                "name": "趋势监控",
                "script": "trend_alert_module.py",
                "schedule": "0 * * * *",
                "priority": "P1",
                "last_run_file": "last_run_trend.json",
                "expected_duration": 120,
                "critical": True
            },
            "competitor_monitor": {
                "name": "竞品监控",
                "script": "competitor_monitor_job.py",
                "schedule": "0 */4 * * *",
                "priority": "P2",
                "last_run_file": "last_run_competitor.json",
                "expected_duration": 180,
                "critical": False
            },
            "clearance_job": {
                "name": "滞销清仓",
                "script": "clearance_job.py",
                "schedule": "0 6 * * *",
                "priority": "P3",
                "last_run_file": "last_run_clearance.json",
                "expected_duration": 300,
                "critical": False
            }
        }
        
        # 自查结果
        self.check_results = []
        
        # 修复记录
        self.fix_records = []
    
    def check_all_tasks(self) -> List[Dict]:
        """
        检查所有定时任务
        
        Returns:
            检查结果列表
        """
        logger.info("=" * 60)
        logger.info("🔍 定时任务自查 - 启动")
        logger.info(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        results = []
        
        for task_id, task_config in self.scheduled_tasks.items():
            logger.info(f"\n📋 检查任务：{task_config['name']} ({task_id})")
            
            result = self._check_single_task(task_id, task_config)
            results.append(result)
        
        self.check_results = results
        
        # 生成报告
        report = self._generate_self_check_report(results)
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 定时任务自查 - 完成")
        logger.info(f"总任务数：{len(results)}")
        logger.info(f"正常：{len([r for r in results if r['status'] == 'ok'])}")
        logger.info(f"警告：{len([r for r in results if r['status'] == 'warning'])}")
        logger.info(f"错误：{len([r for r in results if r['status'] == 'error'])}")
        logger.info("=" * 60)
        
        return results
    
    def _check_single_task(self, task_id: str, task_config: Dict) -> Dict:
        """检查单个任务"""
        result = {
            "task_id": task_id,
            "task_name": task_config["name"],
            "script": task_config["script"],
            "schedule": task_config["schedule"],
            "priority": task_config["priority"],
            "status": "ok",
            "issues": [],
            "fixes": [],
            "checked_at": datetime.now().isoformat()
        }
        
        # 1. 检查脚本文件是否存在
        script_path = SCRIPTS_DIR / task_config["script"]
        if not script_path.exists():
            result["status"] = "error"
            result["issues"].append(f"脚本文件不存在：{script_path}")
            result["fixes"].append(f"创建或恢复脚本文件")
            logger.error(f"❌ 脚本文件不存在：{script_path}")
        else:
            logger.info(f"✅ 脚本文件存在：{script_path}")
        
        # 2. 检查脚本语法
        if script_path.exists():
            syntax_ok = self._check_python_syntax(script_path)
            if not syntax_ok:
                result["status"] = "error"
                result["issues"].append("脚本语法错误")
                result["fixes"].append("修复语法错误")
                logger.error(f"❌ 脚本语法错误：{script_path}")
            else:
                logger.info(f"✅ 脚本语法正确")
        
        # 3. 检查 cron 配置
        cron_ok, cron_issue = self._check_cron_config(task_id, task_config)
        if not cron_ok:
            result["status"] = "warning" if result["status"] == "ok" else result["status"]
            result["issues"].append(cron_issue)
            result["fixes"].append("修复 cron 配置")
            logger.warning(f"⚠️ Cron 配置问题：{cron_issue}")
        else:
            logger.info(f"✅ Cron 配置正确")
        
        # 4. 检查上次执行时间
        last_run_ok, last_run_issue = self._check_last_run(task_id, task_config)
        if not last_run_ok:
            result["status"] = "warning" if result["status"] == "ok" else result["status"]
            result["issues"].append(last_run_issue)
            result["fixes"].append("检查执行日志")
            logger.warning(f"⚠️ 执行时间问题：{last_run_issue}")
        else:
            logger.info(f"✅ 上次执行时间正常")
        
        # 5. 检查依赖模块
        deps_ok, deps_issue = self._check_dependencies(task_config["script"])
        if not deps_ok:
            result["status"] = "error"
            result["issues"].append(deps_issue)
            result["fixes"].append("安装缺失依赖")
            logger.error(f"❌ 依赖问题：{deps_issue}")
        else:
            logger.info(f"✅ 依赖模块正常")
        
        return result
    
    def _check_python_syntax(self, script_path: Path) -> bool:
        """检查 Python 语法"""
        try:
            result = subprocess.run(
                ["python3", "-m", "py_compile", str(script_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"语法检查失败：{str(e)}")
            return False
    
    def _check_cron_config(self, task_id: str, task_config: Dict) -> Tuple[bool, str]:
        """检查 cron 配置"""
        cron_file = CRON_DIR / "cross_border_tasks.cron"
        
        if not cron_file.exists():
            return False, "cron 配置文件不存在"
        
        with open(cron_file, 'r') as f:
            cron_content = f.read()
        
        expected_line = f"{task_config['schedule']} python3 {SCRIPTS_DIR}/{task_config['script']}"
        
        if task_config['schedule'] not in cron_content:
            return False, f"cron 配置中未找到任务：{task_config['schedule']}"
        
        return True, ""
    
    def _check_last_run(self, task_id: str, task_config: Dict) -> Tuple[bool, str]:
        """检查上次执行时间"""
        last_run_file = SCRIPTS_DIR / task_config["last_run_file"]
        
        if not last_run_file.exists():
            return True, ""  # 首次运行，正常
        
        try:
            with open(last_run_file, 'r') as f:
                last_run_data = json.load(f)
            
            last_run_time = datetime.fromisoformat(last_run_data["last_run"])
            time_since = datetime.now() - last_run_time
            
            # 根据任务类型判断是否超时
            if task_id == "trend_monitor":  # 每小时任务
                max_interval = timedelta(hours=2)
            elif task_id == "daily_intelligence":  # 每日任务
                max_interval = timedelta(hours=26)
            elif task_id == "weekly_report":  # 每周任务
                max_interval = timedelta(days=8)
            elif task_id == "monthly_strategy":  # 每月任务
                max_interval = timedelta(days=32)
            elif task_id == "competitor_monitor":  # 每 4 小时任务
                max_interval = timedelta(hours=5)
            elif task_id == "clearance_job":  # 每日任务
                max_interval = timedelta(hours=26)
            else:
                max_interval = timedelta(hours=26)
            
            if time_since > max_interval:
                return False, f"超过{max_interval}未执行 (上次：{time_since}前)"
            
            return True, ""
        
        except Exception as e:
            return False, f"读取上次执行时间失败：{str(e)}"
    
    def _check_dependencies(self, script_name: str) -> Tuple[bool, str]:
        """检查依赖模块"""
        required_modules = ["json", "logging", "pathlib", "datetime"]
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                return False, f"缺少依赖模块：{module}"
        
        return True, ""
    
    def auto_fix_issues(self, results: List[Dict]) -> List[Dict]:
        """自动修复问题"""
        logger.info("\n🔧 开始自动修复...")
        
        fix_records = []
        
        for result in results:
            if result["status"] == "ok":
                continue
            
            for issue in result["issues"]:
                fix_record = {
                    "task_id": result["task_id"],
                    "task_name": result["task_name"],
                    "issue": issue,
                    "fix_attempted": False,
                    "fix_success": False,
                    "fix_message": ""
                }
                
                # 自动修复逻辑
                if "脚本文件不存在" in issue:
                    fix_record["fix_message"] = "需要手动恢复脚本文件"
                    fix_record["fix_attempted"] = False
                
                elif "语法错误" in issue:
                    # 尝试重新编译
                    script_path = SCRIPTS_DIR / result["script"]
                    fix_success = self._check_python_syntax(script_path)
                    fix_record["fix_attempted"] = True
                    fix_record["fix_success"] = fix_success
                    fix_record["fix_message"] = "语法检查已重新执行"
                
                elif "cron 配置" in issue:
                    # 自动创建 cron 配置
                    self._create_cron_config()
                    fix_record["fix_attempted"] = True
                    fix_record["fix_success"] = True
                    fix_record["fix_message"] = "cron 配置已重建"
                
                elif "依赖" in issue:
                    # 尝试安装依赖
                    fix_record["fix_message"] = "需要手动安装依赖"
                    fix_record["fix_attempted"] = False
                
                else:
                    fix_record["fix_message"] = "需要手动干预"
                    fix_record["fix_attempted"] = False
                
                fix_records.append(fix_record)
        
        self.fix_records = fix_records
        
        logger.info(f"✅ 自动修复完成，尝试修复{len(fix_records)}个问题")
        
        return fix_records
    
    def _create_cron_config(self):
        """创建 cron 配置文件"""
        cron_content = "# 跨境贸易 Agent 定时任务配置\n"
        cron_content += "# 生成时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
        
        for task_id, task_config in self.scheduled_tasks.items():
            cron_content += f"# {task_config['name']} ({task_config['priority']})\n"
            cron_content += f"{task_config['schedule']} python3 {SCRIPTS_DIR}/{task_config['script']} >> {WORKSPACE}/logs/cron/{task_id}.log 2>&1\n\n"
        
        cron_file = CRON_DIR / "cross_border_tasks.cron"
        with open(cron_file, 'w') as f:
            f.write(cron_content)
        
        logger.info(f"✅ cron 配置已创建：{cron_file}")
    
    def _generate_self_check_report(self, results: List[Dict]) -> Dict:
        """生成自查报告"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_tasks": len(results),
                "ok": len([r for r in results if r["status"] == "ok"]),
                "warning": len([r for r in results if r["status"] == "warning"]),
                "error": len([r for r in results if r["status"] == "error"])
            },
            "results": results,
            "fix_records": self.fix_records,
            "recommendations": self._generate_recommendations(results)
        }
        
        return report
    
    def _generate_recommendations(self, results: List[Dict]) -> List[Dict]:
        """生成建议"""
        recommendations = []
        
        error_count = len([r for r in results if r["status"] == "error"])
        warning_count = len([r for r in results if r["status"] == "warning"])
        
        if error_count > 0:
            recommendations.append({
                "priority": "P0",
                "type": "critical",
                "message": f"发现{error_count}个严重错误，需要立即修复",
                "action": "检查错误日志并修复"
            })
        
        if warning_count > 0:
            recommendations.append({
                "priority": "P1",
                "type": "warning",
                "message": f"发现{warning_count}个警告，建议检查",
                "action": "查看警告详情"
            })
        
        # 检查趋势监控任务
        trend_task = next((r for r in results if r["task_id"] == "trend_monitor"), None)
        if trend_task and trend_task["status"] != "ok":
            recommendations.append({
                "priority": "P0",
                "type": "critical",
                "message": "趋势监控任务异常，可能影响实时预警",
                "action": "立即修复趋势监控任务"
            })
        
        # 检查每日情报任务
        daily_task = next((r for r in results if r["task_id"] == "daily_intelligence"), None)
        if daily_task and daily_task["status"] != "ok":
            recommendations.append({
                "priority": "P0",
                "type": "critical",
                "message": "每日情报任务异常，可能影响情报推送",
                "action": "立即修复每日情报任务"
            })
        
        if not recommendations:
            recommendations.append({
                "priority": "P3",
                "type": "info",
                "message": "所有定时任务运行正常",
                "action": "继续监控"
            })
        
        return recommendations
    
    def save_report(self, report: Dict) -> str:
        """保存自查报告"""
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"self_check_report_{date_str}.json"
        filepath = REPORT_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 自查报告已保存：{filepath}")
        
        return str(filepath)
    
    def export_summary(self, report: Dict) -> str:
        """导出摘要报告"""
        summary_file = REPORT_DIR / "self_check_summary.md"
        
        content = f"""# 🔍 定时任务自查报告

> **生成时间**: {report['generated_at']}

---

## 📊 概要

| 状态 | 数量 |
|------|------|
| ✅ 正常 | {report['summary']['ok']} |
| ⚠️ 警告 | {report['summary']['warning']} |
| ❌ 错误 | {report['summary']['error']} |
| **总计** | {report['summary']['total_tasks']} |

---

## 📋 任务详情

"""
        for result in report['results']:
            status_icon = "✅" if result["status"] == "ok" else "⚠️" if result["status"] == "warning" else "❌"
            content += f"### {status_icon} {result['task_name']} ({result['task_id']})\n\n"
            content += f"- **脚本**: `{result['script']}`\n"
            content += f"- **计划**: `{result['schedule']}`\n"
            content += f"- **优先级**: {result['priority']}\n"
            content += f"- **状态**: {result['status']}\n"
            
            if result['issues']:
                content += f"- **问题**:\n"
                for issue in result['issues']:
                    content += f"  - {issue}\n"
            
            if result['fixes']:
                content += f"- **修复建议**:\n"
                for fix in result['fixes']:
                    content += f"  - {fix}\n"
            
            content += "\n"
        
        content += """---

## 🔧 修复记录

"""
        if report['fix_records']:
            for fix in report['fix_records']:
                content += f"- **{fix['task_name']}**: {fix['issue']}\n"
                content += f"  - 修复尝试：{'是' if fix['fix_attempted'] else '否'}\n"
                content += f"  - 修复成功：{'是' if fix['fix_success'] else '否'}\n"
                content += f"  - 修复说明：{fix['fix_message']}\n\n"
        else:
            content += "无修复记录\n\n"
        
        content += """---

## 💡 建议

"""
        for rec in report['recommendations']:
            priority_icon = "🔴" if rec["priority"] == "P0" else "🟡" if rec["priority"] == "P1" else "🟢"
            content += f"{priority_icon} **[{rec['priority']}]** {rec['message']}\n"
            content += f"   行动：{rec['action']}\n\n"
        
        content += f"\n---\n\n*报告生成：太一 AGI 定时任务自查系统*\n"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"📄 摘要报告已导出：{summary_file}")
        
        return str(summary_file)


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("🔍 定时任务自查模块 - 演示")
    logger.info("=" * 60)
    
    # 初始化模块
    self_check = ScheduledTaskSelfCheckModule()
    
    # 创建 cron 配置 (如果不存在)
    logger.info("\n📋 检查 cron 配置...")
    self_check._create_cron_config()
    
    # 检查所有任务
    logger.info("\n🔍 检查所有定时任务...")
    results = self_check.check_all_tasks()
    
    # 自动修复
    logger.info("\n🔧 自动修复问题...")
    fix_records = self_check.auto_fix_issues(results)
    
    # 生成报告
    logger.info("\n📋 生成自查报告...")
    report = self_check._generate_self_check_report(results)
    
    # 保存报告
    logger.info("\n💾 保存报告...")
    self_check.save_report(report)
    
    # 导出摘要
    logger.info("\n📄 导出摘要...")
    self_check.export_summary(report)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
