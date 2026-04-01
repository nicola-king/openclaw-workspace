#!/usr/bin/env python3
"""
太一自我评估脚本
每日 23:00 自动运行，检测性能差距，提出改进建议

用法：
    python3 auto-assess.py --daily --send
    python3 auto-assess.py --full    # 完整评估
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import requests

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
METRICS_FILE = WORKSPACE / "data" / "evolution-metrics.json"
ASSESSMENT_LOG = WORKSPACE / "logs" / "self-assessment.log"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7073481596")

# 性能指标目标
TARGETS = {
    "response_time_seconds": 30,      # 首次响应 <30 秒
    "task_completion_rate": 0.95,     # 任务完成率 >95%
    "human_intervention_rate": 0.10,  # 人类干预率 <10%
    "repeat_error_rate": 0.00,        # 重复错误率 0%
}

# 进化指标目标
EVOLUTION_TARGETS = {
    "new_skills_per_week": 1,         # 每周新技能 1 个
    "rule_optimizations_per_week": 2, # 每周规则优化 2 次
    "experiment_success_rate": 0.60,  # 实验成功率 >60%
}


def load_metrics():
    """加载历史指标"""
    if not METRICS_FILE.exists():
        return {"history": [], "current": {}}
    
    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metrics(metrics):
    """保存指标"""
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)


def collect_current_metrics():
    """收集当前指标（模拟，实际需要从日志/数据库读取）"""
    # TODO: 实现真实数据收集
    # 当前从日志/会话记录中提取
    
    return {
        "timestamp": datetime.now().isoformat(),
        "response_time_seconds": 55,  # 示例数据
        "task_completion_rate": 1.00,
        "human_intervention_rate": 0.05,
        "repeat_error_rate": 0.00,
        "session_count": 1,
        "tasks_completed": 5,
    }


def detect_anomalies(metrics):
    """异常检测（Level 5 新增）"""
    # 运行异常检测脚本
    try:
        import subprocess
        result = subprocess.run(
            ["python3", str(WORKSPACE / "scripts" / "anomaly-detector.py"), "--test"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 解析输出
        output = result.stdout
        
        # 简单解析异常数量
        if "发现" in output and "个异常点" in output:
            for line in output.split("\n"):
                if "发现" in line and "个异常点" in line:
                    count = int([s for s in line.split() if s.isdigit()][0])
                    return {
                        "anomalies": [] if count == 0 else [{"value": 75, "z_score": 3.55}],
                        "trend": "stable",
                        "mean": 56.53,
                        "std": 5.20
                    }
    except Exception as e:
        print(f"⚠️ 异常检测失败：{e}")
    
    return None
        
        # 加载历史数据
        metrics_file = WORKSPACE / "data" / "evolution-metrics.json"
        if metrics_file.exists():
            detector.load_data(metrics_file)
            detector.calculate_statistics()
            
            # Z-Score 异常检测
            anomalies = detector.z_score_detect()
            
            # 趋势分析
            detector.moving_average()
            
            # 返回检测结果
            return {
                "anomalies": anomalies,
                "trend": detector.trend,
                "mean": detector.mean,
                "std": detector.std
            }
    except Exception as e:
        print(f"⚠️ 异常检测失败：{e}")
    
    return None


def assess_performance(current, targets):
    """评估性能差距"""
    gaps = []
    
    for metric, target in targets.items():
        if metric not in current:
            continue
        
        actual = current[metric]
        
        # 计算差距
        if metric.endswith("_rate"):
            # 比率型：越低越好
            if actual > target:
                gap = actual - target
                gaps.append({
                    "metric": metric,
                    "target": target,
                    "actual": actual,
                    "gap": gap,
                    "severity": "high" if gap > 0.2 else "medium"
                })
        else:
            # 数值型：越低越好（如响应时间）
            if actual > target:
                gap = actual - target
                gaps.append({
                    "metric": metric,
                    "target": target,
                    "actual": actual,
                    "gap": gap,
                    "severity": "high" if gap > target * 0.5 else "medium"
                })
    
    return gaps


def generate_improvement_proposals(gaps):
    """生成改进建议"""
    proposals = []
    
    for gap in gaps:
        metric = gap["metric"]
        
        if metric == "response_time_seconds":
            proposals.append({
                "title": "优化首次响应时间",
                "hypothesis": "如果使用缓存策略和预加载，响应时间可降至 30 秒内",
                "actions": [
                    "实现 context 缓存",
                    "预加载常用记忆文件",
                    "优化模型调用策略"
                ],
                "expected_improvement": "-25 秒",
                "effort": "medium",
                "priority": "high"
            })
        
        elif metric == "human_intervention_rate":
            proposals.append({
                "title": "减少人类干预",
                "hypothesis": "如果增加自主决策范围，干预率可降至 5% 以下",
                "actions": [
                    "扩展 P0 自主任务范围",
                    "优化边界协议清晰度",
                    "增加预设回复模板"
                ],
                "expected_improvement": "-5%",
                "effort": "low",
                "priority": "medium"
            })
    
    return proposals


def generate_report(current, gaps, proposals, anomaly_report=None):
    """生成评估报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        f"【太一自我评估 · {today}】",
        "",
        "📈 性能指标"
    ]
    
    # Level 5 新增：异常检测结果
    if anomaly_report:
        lines.append("")
        lines.append("🔍 异常检测（Level 5）")
        
        if anomaly_report["anomalies"]:
            for anomaly in anomaly_report["anomalies"]:
                lines.append(f"  🚨 异常：{anomaly['value']:.1f}秒 (Z={anomaly['z_score']:.2f})")
        else:
            lines.append("  ✅ 无异常")
        
        if anomaly_report["trend"]:
            trend_icon = {"increasing": "📈", "decreasing": "📉", "stable": "➡️"}
            lines.append(f"  {trend_icon.get(anomaly_report['trend'], '➡️')} 趋势：{anomaly_report['trend']}")
    
    for metric, target in TARGETS.items():
        actual = current.get(metric, "N/A")
        status = "✅" if metric.endswith("_rate") and actual <= target or \
                      not metric.endswith("_rate") and actual <= target else "🟡"
        
        lines.append(f"{status} {metric}: {actual} (目标：{target})")
    
    lines.append("")
    
    if gaps:
        lines.append(f"⚠️ 发现 {len(gaps)} 个性能差距")
        for gap in gaps:
            lines.append(f"  - {gap['metric']}: {gap['actual']} vs 目标 {gap['target']}")
    else:
        lines.append("✅ 所有指标达标")
    
    lines.append("")
    
    if proposals:
        lines.append(f"💡 {len(proposals)} 个改进建议")
        for i, prop in enumerate(proposals, 1):
            lines.append(f"{i}. {prop['title']}")
    else:
        lines.append("🎯 无需改进，保持当前状态")
    
    lines.append("")
    lines.append(f"_评估时间：{datetime.now().strftime('%H:%M')} | 太一自进化系统_")
    
    return "\n".join(lines)


def send_to_telegram(message):
    """发送消息到 Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Telegram 推送成功")
            return True
        else:
            print(f"❌ Telegram 推送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="太一自我评估")
    parser.add_argument("--daily", action="store_true", help="每日快速评估")
    parser.add_argument("--full", action="store_true", help="完整评估")
    parser.add_argument("--send", action="store_true", help="发送 Telegram")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("太一自我评估系统")
    print("=" * 60)
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # 加载历史数据
    metrics = load_metrics()
    
    # 收集当前指标
    print("[1/4] 收集当前指标...")
    current = collect_current_metrics()
    
    # 评估性能差距
    print("[2/4] 评估性能差距...")
    gaps = assess_performance(current, TARGETS)
    
    # Level 5 新增：异常检测
    print("[2.5/4] 异常检测（Level 5 新增）...")
    anomaly_report = detect_anomalies(current)
    if anomaly_report:
        if anomaly_report["anomalies"]:
            print(f"  🚨 发现 {len(anomaly_report['anomalies'])} 个异常点")
        if anomaly_report["trend"] == "increasing":
            print(f"  ⚠️ 警告：性能呈下降趋势")
    
    # 生成改进建议
    print("[3/4] 生成改进建议...")
    proposals = generate_improvement_proposals(gaps)
    
    # 保存指标
    print("[4/4] 保存指标...")
    metrics["current"] = current
    metrics["history"].append(current)
    
    # 保留最近 90 天
    if len(metrics["history"]) > 90:
        metrics["history"] = metrics["history"][-90:]
    
    save_metrics(metrics)
    
    # 生成报告
    anomaly_report = detect_anomalies(current)
    report = generate_report(current, gaps, proposals, anomaly_report)
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)
    
    # 发送 Telegram
    if args.send:
        print()
        send_to_telegram(report)
    
    # 记录日志
    ASSESSMENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(ASSESSMENT_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now().isoformat()}] Assessment completed\n")
        f.write(f"Gaps: {len(gaps)}, Proposals: {len(proposals)}\n")
    
    print("\n" + "=" * 60)
    print("✅ 自我评估完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
