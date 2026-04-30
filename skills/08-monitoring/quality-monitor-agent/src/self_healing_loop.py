#!/usr/bin/env python3
"""
自愈闭环模块
太一 AGI · 2026-04-17

功能：
- 完整的自愈闭环流程：检测→修复→验证→学习→预防
- 自愈效果评估
- 自愈历史追踪
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SELF_HEAL_LOG = WORKSPACE / "monitoring" / "self-heal-log.json"


class SelfHealingLoop:
    """自愈闭环管理器"""
    
    def __init__(self):
        self.script_paths = {
            "daily-report-generator.py": "scripts/daily-report-generator.py",
            "daily-constitution-study.py": "scripts/daily-constitution-study.py",
            "hourly-health-check.py": "scripts/hourly-health-check.py",
            "yijing-daily-study.py": "skills/07-system/suwen/yijing-daily-study.py",
            "xianqin-daily-study.py": "skills/07-system/suwen/xianqin-daily-study.py",
            "weather-forecast.py": "skills/07-system/suwen/weather-forecast.py",
        }
    
    def detect(self, issue: Dict) -> bool:
        """
        步骤 1：检测问题
        
        Returns:
            bool: 是否检测到问题
        """
        print(f"  🔍 [检测] 检查问题：{issue.get('script', 'unknown')}")
        
        # 检查文件是否缺失
        files_missing = issue.get("files_missing", [])
        if files_missing:
            print(f"    ✅ 确认缺失文件：{len(files_missing)} 个")
            return True
        
        print(f"    ℹ️  无缺失文件")
        return False
    
    def fix(self, issue: Dict) -> Dict:
        """
        步骤 2：自动修复
        
        Returns:
            Dict: 修复结果
        """
        script_name = issue.get("script", "unknown")
        
        print(f"  🔧 [修复] 尝试修复：{script_name}")
        
        if script_name not in self.script_paths:
            print(f"    ⚠️  脚本路径未配置")
            return {"status": "no_config", "error": "脚本路径未配置"}
        
        script_path = WORKSPACE / self.script_paths[script_name]
        
        if not script_path.exists():
            print(f"    ⚠️  脚本文件不存在：{script_path}")
            return {"status": "not_found", "error": f"脚本不存在：{script_path}"}
        
        try:
            result = subprocess.run(
                ["python3", str(script_path)],
                cwd=str(WORKSPACE),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"    ✅ 修复成功")
                return {"status": "fixed", "output": result.stdout[:200]}
            else:
                print(f"    ⚠️  修复失败：{result.stderr[:100]}")
                return {"status": "fix_failed", "error": result.stderr[:100]}
        
        except Exception as e:
            print(f"    ⚠️  修复异常：{str(e)}")
            return {"status": "fix_error", "error": str(e)}
    
    def verify(self, issue: Dict, fix_result: Dict) -> Dict:
        """
        步骤 3：验证修复
        
        Returns:
            Dict: 验证结果
        """
        print(f"  ✅ [验证] 检查修复结果...")
        
        if fix_result.get("status") != "fixed":
            print(f"    ⚠️  修复失败，跳过验证")
            return {"status": "skip", "reason": "修复失败"}
        
        # 检查文件是否已创建
        files_missing = issue.get("files_missing", [])
        files_created = []
        files_still_missing = []
        
        for file_pattern in files_missing:
            # 替换占位符
            today = datetime.now().strftime("%Y-%m-%d")
            today_nodash = datetime.now().strftime("%Y%m%d")
            today_hour = datetime.now().strftime("%Y%m%d-%H%M")
            
            filename = file_pattern.format(
                today=today,
                today_nodash=today_nodash,
                today_hour=today_hour
            )
            file_path = WORKSPACE / filename
            
            if file_path.exists() and file_path.stat().st_size > 50:
                files_created.append(filename)
            else:
                files_still_missing.append(filename)
        
        if files_created:
            print(f"    ✅ 文件已创建：{len(files_created)} 个")
        
        if files_still_missing:
            print(f"    ⚠️  文件仍缺失：{len(files_still_missing)} 个")
        
        return {
            "status": "verified" if not files_still_missing else "partial",
            "files_created": files_created,
            "files_still_missing": files_still_missing
        }
    
    def learn(self, issue: Dict, fix_result: Dict, verify_result: Dict):
        """
        步骤 4：学习记录
        
        将自愈过程记录到日志，用于后续分析
        """
        print(f"  🧠 [学习] 记录自愈过程...")
        
        # 加载现有日志
        heal_log = []
        if SELF_HEAL_LOG.exists():
            try:
                with open(SELF_HEAL_LOG, "r", encoding="utf-8") as f:
                    heal_log = json.load(f)
            except:
                heal_log = []
        
        # 添加新记录
        record = {
            "timestamp": datetime.now().isoformat(),
            "issue": issue,
            "fix_result": fix_result,
            "verify_result": verify_result,
            "success": fix_result.get("status") == "fixed" and verify_result.get("status") == "verified"
        }
        heal_log.append(record)
        
        # 保留最近 100 条
        heal_log = heal_log[-100:]
        
        # 保存日志
        SELF_HEAL_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(SELF_HEAL_LOG, "w", encoding="utf-8") as f:
            json.dump(heal_log, f, indent=2, ensure_ascii=False)
        
        print(f"    ✅ 已记录到 self-heal-log.json")
    
    def prevent(self, heal_log: List[Dict]) -> List[str]:
        """
        步骤 5：预防建议
        
        基于自愈历史生成预防性建议
        
        Returns:
            List[str]: 预防建议列表
        """
        print(f"  🛡️  [预防] 生成预防建议...")
        
        recommendations = []
        
        # 分析自愈成功率
        total = len(heal_log)
        success = sum(1 for r in heal_log if r.get("success", False))
        
        if total > 0:
            success_rate = success / total * 100
            if success_rate < 80:
                recommendations.append(
                    f"🔧 自愈成功率 {success_rate:.0f}%，建议优化自动修复脚本"
                )
        
        # 分析高频问题脚本
        script_counts = {}
        for record in heal_log:
            script = record.get("issue", {}).get("script", "unknown")
            script_counts[script] = script_counts.get(script, 0) + 1
        
        for script, count in script_counts.items():
            if count >= 3:
                recommendations.append(
                    f"🔍 {script} 自愈 {count} 次，建议深入检查根本原因"
                )
        
        if not recommendations:
            recommendations.append("✅ 自愈系统运行良好，无需特别预防措施")
        
        for rec in recommendations:
            print(f"    {rec}")
        
        return recommendations
    
    def execute(self, issue: Dict) -> Dict:
        """
        执行完整自愈闭环
        
        流程：检测→修复→验证→学习→预防
        
        Args:
            issue: 问题描述
        
        Returns:
            Dict: 自愈结果
        """
        print(f"\n🔄 开始自愈闭环流程...")
        
        # 步骤 1：检测
        detected = self.detect(issue)
        if not detected:
            return {"status": "no_issue", "message": "未检测到问题"}
        
        # 步骤 2：修复
        fix_result = self.fix(issue)
        
        # 步骤 3：验证
        verify_result = self.verify(issue, fix_result)
        
        # 步骤 4：学习
        self.learn(issue, fix_result, verify_result)
        
        # 步骤 5：预防
        heal_log = []
        if SELF_HEAL_LOG.exists():
            with open(SELF_HEAL_LOG, "r", encoding="utf-8") as f:
                heal_log = json.load(f)
        prevent_recommendations = self.prevent(heal_log)
        
        # 汇总结果
        success = fix_result.get("status") == "fixed" and verify_result.get("status") == "verified"
        
        result = {
            "status": "success" if success else "partial",
            "detected": detected,
            "fix_result": fix_result,
            "verify_result": verify_result,
            "prevent_recommendations": prevent_recommendations,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n✅ 自愈闭环完成：{'成功' if success else '部分成功'}")
        
        return result


def main():
    """主函数 - 演示自愈闭环流程"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔄 自愈闭环系统已就绪")
    print("\n用法:")
    print("  # 作为模块导入")
    print("  from self_healing_loop import SelfHealingLoop")
    print("  loop = SelfHealingLoop()")
    print("  result = loop.execute(issue)")
    print("\n自愈流程：检测 → 修复 → 验证 → 学习 → 预防")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
