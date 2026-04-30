#!/usr/bin/env python3
"""
预测性维护模块
太一 AGI · 2026-04-17

功能：
- 基于历史数据预测潜在问题
- 计算脚本风险评分
- 生成预防性维护建议
- 提前干预避免问题发生
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
QUALITY_LOG = WORKSPACE / "monitoring" / "task-quality-log.json"
REPORTS_DIR = WORKSPACE / "skills" / "08-monitoring" / "quality-monitor-agent" / "reports"


def load_quality_logs(days=7):
    """加载最近 N 天的质量日志"""
    if not QUALITY_LOG.exists():
        return []
    
    with open(QUALITY_LOG, "r", encoding="utf-8") as f:
        logs = json.load(f)
    
    cutoff = datetime.now() - timedelta(days=days)
    recent_logs = []
    for log in logs:
        try:
            log_time = datetime.fromisoformat(log["timestamp"])
            if log_time >= cutoff:
                recent_logs.append(log)
        except:
            continue
    
    return recent_logs


def calculate_risk_score(script_name, logs):
    """
    计算脚本风险评分
    
    风险评分 = (
        问题频率 × 0.4 +      # 过去 7 天问题次数
        修复失败率 × 0.3 +    # 修复失败占比
        时间规律性 × 0.2 +    # 是否在固定时间出问题
        影响范围 × 0.1        # 影响的任务数量
    )
    """
    # 筛选该脚本的日志
    script_logs = [l for l in logs if l.get("script") == script_name]
    
    if not script_logs:
        return 0.0, {"status": "no_issues"}
    
    # 1. 问题频率（0-100 分）
    issue_count = len(script_logs)
    frequency_score = min(100, issue_count * 10)  # 每出现 1 次 +10 分，最高 100
    
    # 2. 修复失败率（0-100 分）
    total_fixes = sum(1 for l in script_logs if "auto_fix" in l)
    failed_fixes = sum(1 for l in script_logs if l.get("auto_fix", {}).get("status") in ["fix_failed", "fix_error"])
    fix_failure_rate = (failed_fixes / total_fixes * 100) if total_fixes > 0 else 0
    fix_failure_score = fix_failure_rate
    
    # 3. 时间规律性（0-100 分）
    # 检查是否在固定小时出问题
    hour_counts = defaultdict(int)
    for log in script_logs:
        try:
            hour = datetime.fromisoformat(log["timestamp"]).hour
            hour_counts[hour] += 1
        except:
            continue
    
    if hour_counts:
        max_hour_count = max(hour_counts.values())
        # 如果某个时间段问题集中，规律性得分高
        time_pattern_score = (max_hour_count / len(script_logs)) * 100
    else:
        time_pattern_score = 0
    
    # 4. 影响范围（0-100 分）
    # 检查缺失文件数量
    missing_files = set()
    for log in script_logs:
        for f in log.get("files_missing", []):
            missing_files.add(f)
    impact_score = min(100, len(missing_files) * 20)  # 每个缺失文件 +20 分
    
    # 计算总分
    total_score = (
        frequency_score * 0.4 +
        fix_failure_score * 0.3 +
        time_pattern_score * 0.2 +
        impact_score * 0.1
    )
    
    risk_details = {
        "issue_count": issue_count,
        "frequency_score": frequency_score,
        "fix_failure_rate": fix_failure_rate,
        "fix_failure_score": fix_failure_score,
        "time_pattern_score": time_pattern_score,
        "missing_files_count": len(missing_files),
        "impact_score": impact_score,
        "peak_hours": sorted(hour_counts.keys(), key=lambda h: hour_counts[h], reverse=True)[:3],
    }
    
    return total_score, risk_details


def get_risk_level(score):
    """根据评分获取风险等级"""
    if score <= 20:
        return "🟢", "低风险"
    elif score <= 50:
        return "🟡", "中风险"
    elif score <= 80:
        return "🟠", "高风险"
    else:
        return "🔴", "极高风险"


def generate_maintenance_recommendations(script_name, score, details):
    """生成维护建议"""
    recommendations = []
    
    emoji, level = get_risk_level(score)
    
    # 高频问题
    if details.get("issue_count", 0) >= 3:
        recommendations.append(
            f"🔍 **深入检查 {script_name}** - 过去 7 天出现 {details['issue_count']} 次问题，建议检查脚本逻辑和依赖"
        )
    
    # 修复失败率高
    if details.get("fix_failure_rate", 0) > 50:
        recommendations.append(
            f"🔧 **优化自动修复** - {script_name} 修复失败率 {details['fix_failure_rate']:.0f}%，建议检查修复脚本或增加重试机制"
        )
    
    # 时间规律性
    if details.get("peak_hours"):
        peak_hour = details["peak_hours"][0]
        recommendations.append(
            f"⏰ **关注高峰时段** - {script_name} 常在 {peak_hour:02d}:00 左右出问题，建议在该时段前进行预防性检查"
        )
    
    # 影响范围大
    if details.get("missing_files_count", 0) >= 3:
        recommendations.append(
            f"📁 **检查输出文件** - {script_name} 影响 {details['missing_files_count']} 个输出文件，建议检查文件路径和权限"
        )
    
    if not recommendations:
        recommendations.append(f"✅ {script_name} 运行稳定，无需特别维护")
    
    return recommendations


def generate_predictive_report(logs):
    """生成预测性维护报告"""
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 获取所有脚本
    scripts = set(l.get("script") for l in logs if l.get("script"))
    
    # 计算每个脚本的风险评分
    risk_assessment = []
    for script in scripts:
        score, details = calculate_risk_score(script, logs)
        emoji, level = get_risk_level(score)
        risk_assessment.append({
            "script": script,
            "score": score,
            "level": level,
            "emoji": emoji,
            "details": details,
            "recommendations": generate_maintenance_recommendations(script, score, details)
        })
    
    # 按风险评分排序
    risk_assessment.sort(key=lambda x: x["score"], reverse=True)
    
    # 生成报告
    report = f"""# 预测性维护报告

生成时间：{today}
统计周期：过去 7 天
数据来源：monitoring/task-quality-log.json

---

## 📊 总体风险概览

| 风险等级 | 脚本数量 | 占比 |
|------|--------|------|
| 🔴 极高风险 | {sum(1 for r in risk_assessment if r['score'] > 80)} | {sum(1 for r in risk_assessment if r['score'] > 80)*100//len(risk_assessment) if risk_assessment else 0}% |
| 🟠 高风险 | {sum(1 for r in risk_assessment if 50 < r['score'] <= 80)} | {sum(1 for r in risk_assessment if 50 < r['score'] <= 80)*100//len(risk_assessment) if risk_assessment else 0}% |
| 🟡 中风险 | {sum(1 for r in risk_assessment if 20 < r['score'] <= 50)} | {sum(1 for r in risk_assessment if 20 < r['score'] <= 50)*100//len(risk_assessment) if risk_assessment else 0}% |
| 🟢 低风险 | {sum(1 for r in risk_assessment if r['score'] <= 20)} | {sum(1 for r in risk_assessment if r['score'] <= 20)*100//len(risk_assessment) if risk_assessment else 0}% |

---

## 🎯 脚本风险评估

"""
    
    for assessment in risk_assessment:
        report += f"""### {assessment['emoji']} {assessment['script']} · 风险评分：{assessment['score']:.1f} ({assessment['level']})

**详细指标**:
- 问题次数：{assessment['details'].get('issue_count', 0)}
- 修复失败率：{assessment['details'].get('fix_failure_rate', 0):.1f}%
- 影响文件数：{assessment['details'].get('missing_files_count', 0)}
- 高峰时段：{assessment['details'].get('peak_hours', [])}

**维护建议**:
"""
        for rec in assessment["recommendations"]:
            report += f"\n- {rec}"
        report += "\n"
    
    # 总体建议
    high_risk_scripts = [r for r in risk_assessment if r["score"] > 50]
    
    report += f"""
---

## 💡 总体维护建议

"""
    
    if high_risk_scripts:
        report += "**优先处理以下高风险脚本**:\n\n"
        for script in high_risk_scripts[:3]:
            report += f"1. {script['emoji']} {script['script']} - 风险评分 {script['score']:.1f}\n"
    else:
        report += "✅ 所有脚本风险可控，继续正常监控即可\n"
    
    report += f"""
---

## 📈 趋势预测

基于过去 7 天数据分析：

"""
    
    # 趋势预测
    if len(logs) > 10:
        report += "- 📊 数据量充足，预测可信度高\n"
    else:
        report += "- ⚠️  数据量较少，预测仅供参考\n"
    
    if high_risk_scripts:
        report +=(f"- ⚠️  预计未来 7 天可能出现 {len(high_risk_scripts)} 个脚本问题\n")
        report +=("- 建议提前进行预防性维护\n")
    else:
        report +=("- ✅ 预计未来 7 天系统稳定，无重大风险\n")
    
    report += f"""
---

## 📝 原始数据

- 日志总数：{len(logs)} 条
- 涉及脚本：{len(scripts)} 个
- 分析脚本：skills/08-monitoring/quality-monitor-agent/src/predictive_maintenance.py

---

*太一 AGI · 预测性维护系统 · 自动生成*
"""
    
    return report, risk_assessment


def main():
    """主函数"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔮 开始预测性维护分析...")
    
    # 加载最近 7 天数据
    print("  📁 加载最近 7 天质量日志...")
    logs = load_quality_logs(days=7)
    print(f"  找到 {len(logs)} 条记录")
    
    if not logs:
        print("  ℹ️  无质量问题记录，系统运行良好 ✅")
        return 0
    
    # 生成预测性维护报告
    print("  📊 生成预测性维护报告...")
    report, risk_assessment = generate_predictive_report(logs)
    
    # 保存报告
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORTS_DIR / f"predictive-maintenance-{datetime.now().strftime('%Y%m%d')}.md"
    report_file.write_text(report, encoding='utf-8')
    print(f"  ✅ 报告已保存：{report_file}")
    
    # 打印高风险脚本
    high_risk = [r for r in risk_assessment if r["score"] > 50]
    if high_risk:
        print(f"\n⚠️  发现 {len(high_risk)} 个高风险脚本:")
        for script in high_risk[:3]:
            print(f"  {script['emoji']} {script['script']} - 风险评分 {script['score']:.1f}")
    else:
        print(f"\n✅ 所有脚本风险可控")
    
    print(f"\n✅ 预测性维护分析完成！")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
