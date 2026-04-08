#!/usr/bin/env python3
"""
模型使用追踪器 - 每 5 分钟自动更新
追踪大模型使用额度，智能分流，成本优化

用法：
    python3 model-usage-tracker.py [--model MODEL] [--tokens N] [--task-type TYPE]
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = Path('/home/nicola/.openclaw/workspace')
MEMORY_DIR = WORKSPACE / 'memory'
USAGE_FILE = MEMORY_DIR / f'model-usage-{datetime.now().strftime("%Y-%m-%d")}.md'
QUOTA_FILE = MEMORY_DIR / 'model-quota-status.json'

# 模型成本 (¥/K tokens)
COST_RATES = {
    'local': 0.0,           # 本地模型免费
    'qwen-plus': 0.09,      # 百炼 qwen3.5-plus
    'gemini': 0.07,         # Gemini 订阅价
    'coder': 0.12           # qwen3-coder-plus
}

# 配额限制
QUOTAS = {
    'qwen-plus': {'daily': 100, 'weekly': 700, 'monthly': 3000},
    'gemini': {'daily': 1000},
    'coder': {'daily': 100}
}

# 告警阈值
ALERT_THRESHOLDS = {
    'warning': 0.90,    # 90% 告警
    'critical': 0.98,   # 98% 紧急
    'exhausted': 1.00   # 100% 耗尽
}


def ensure_memory_dir():
    """确保 memory 目录存在"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def load_today_usage():
    """读取今日使用统计"""
    if not USAGE_FILE.exists():
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'models': {},
            'total_cost': 0.0,
            'total_tasks': 0,
            'total_tokens': 0
        }
    
    try:
        # 尝试读取 JSON 部分
        with open(USAGE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找 JSON 块
            if '```json' in content:
                json_start = content.find('```json') + 7
                json_end = content.find('```', json_start)
                json_str = content[json_start:json_end].strip()
                return json.loads(json_str)
    except:
        pass
    
    return {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'models': {},
        'total_cost': 0.0,
        'total_tasks': 0,
        'total_tokens': 0
    }


def save_usage(stats):
    """保存使用统计"""
    ensure_memory_dir()
    
    # 生成 Markdown 报告
    markdown = generate_markdown_report(stats)
    
    with open(USAGE_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    # 同时保存 JSON 用于程序读取
    json_file = USAGE_FILE.with_suffix('.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)


def generate_markdown_report(stats):
    """生成 Markdown 格式报告"""
    date = stats.get('date', datetime.now().strftime('%Y-%m-%d'))
    models = stats.get('models', {})
    total_cost = stats.get('total_cost', 0)
    total_tasks = stats.get('total_tasks', 0)
    total_tokens = stats.get('total_tokens', 0)
    
    # 计算本地化率
    local_calls = models.get('local', {}).get('calls', 0)
    localization_rate = (local_calls / total_tasks * 100) if total_tasks > 0 else 0
    
    # 计算配额使用率
    qwen_usage = models.get('qwen-plus', {}).get('calls', 0)
    gemini_usage = models.get('gemini', {}).get('calls', 0)
    coder_usage = models.get('coder', {}).get('calls', 0)
    
    qwen_rate = qwen_usage / QUOTAS['qwen-plus']['daily'] * 100
    gemini_rate = gemini_usage / QUOTAS['gemini']['daily'] * 100
    coder_rate = coder_usage / QUOTAS['coder']['daily'] * 100
    
    # 生成告警
    alerts = []
    if qwen_rate >= 98:
        alerts.append(f'🚨 百炼配额紧急：{qwen_usage}/{QUOTAS["qwen-plus"]["daily"]} ({qwen_rate:.1f}%)')
    elif qwen_rate >= 90:
        alerts.append(f'⚠️ 百炼配额告警：{qwen_usage}/{QUOTAS["qwen-plus"]["daily"]} ({qwen_rate:.1f}%)')
    
    if gemini_rate >= 98:
        alerts.append(f'🚨 Gemini 配额紧急：{gemini_usage}/{QUOTAS["gemini"]["daily"]} ({gemini_rate:.1f}%)')
    elif gemini_rate >= 90:
        alerts.append(f'⚠️ Gemini 配额告警：{gemini_usage}/{QUOTAS["gemini"]["daily"]} ({gemini_rate:.1f}%)')
    
    if not alerts:
        alerts.append('✅ 无告警')
    
    avg_cost = f"¥{(total_cost/total_tasks):.3f}" if total_tasks > 0 else "N/A"
    
    markdown = f"""# 模型使用统计 · {date}

> 最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 自动追踪 (每 5 分钟)

---

## 📊 今日使用 (实时更新)

| 模型 | 调用次数 | Token 数 | 估算成本 | 配额剩余 | 使用率 |
|------|---------|---------|---------|---------|--------|
| Qwen 2.5 7B (本地) | {models.get('local', {}).get('calls', 0)} | {models.get('local', {}).get('tokens', 0):,} | ¥{models.get('local', {}).get('cost', 0):.2f} | ∞ | - |
| qwen3.5-plus | {models.get('qwen-plus', {}).get('calls', 0)} | {models.get('qwen-plus', {}).get('tokens', 0):,} | ¥{models.get('qwen-plus', {}).get('cost', 0):.2f} | {QUOTAS['qwen-plus']['daily'] - qwen_usage}/{QUOTAS['qwen-plus']['daily']} | {qwen_rate:.1f}% |
| Gemini 2.5 Pro | {models.get('gemini', {}).get('calls', 0)} | {models.get('gemini', {}).get('tokens', 0):,} | ¥{models.get('gemini', {}).get('cost', 0):.2f} | {QUOTAS['gemini']['daily'] - gemini_usage}/{QUOTAS['gemini']['daily']} | {gemini_rate:.1f}% |
| qwen3-coder-plus | {models.get('coder', {}).get('calls', 0)} | {models.get('coder', {}).get('tokens', 0):,} | ¥{models.get('coder', {}).get('cost', 0):.2f} | {QUOTAS['coder']['daily'] - coder_usage}/{QUOTAS['coder']['daily']} | {coder_rate:.1f}% |

---

## 📈 统计汇总

| 指标 | 数值 |
|------|------|
| **总任务数** | {total_tasks} |
| **总 Token 数** | {total_tokens:,} |
| **总成本** | ¥{total_cost:.2f} |
| **本地化率** | {localization_rate:.1f}% |
| **平均每任务成本** | {avg_cost} |

---

## 🎯 配额状态

| 模型 | 已用 | 总额度 | 使用率 | 状态 |
|------|------|--------|--------|------|
| 百炼 (日) | {qwen_usage} | {QUOTAS['qwen-plus']['daily']} | {qwen_rate:.1f}% | {'🔴' if qwen_rate >= 98 else '🟡' if qwen_rate >= 90 else '🟢'} |
| Gemini (日) | {gemini_usage} | {QUOTAS['gemini']['daily']} | {gemini_rate:.1f}% | {'🔴' if gemini_rate >= 98 else '🟡' if gemini_rate >= 90 else '🟢'} |
| 代码模型 (日) | {coder_usage} | {QUOTAS['coder']['daily']} | {coder_rate:.1f}% | {'🔴' if coder_rate >= 98 else '🟡' if coder_rate >= 90 else '🟢'} |

---

## 🚨 告警

{chr(10).join(f'- {alert}' for alert in alerts)}

---

## 💡 优化建议

{generate_optimization_suggestions(localization_rate, qwen_rate, gemini_rate)}

---

*自动追踪 · 每 5 分钟更新 · 下次更新：{(datetime.now().replace(minute=(datetime.now().minute // 5 * 5 + 5) % 60, second=0)).strftime('%H:%M')}*
"""
    return markdown


def generate_optimization_suggestions(localization_rate, qwen_rate, gemini_rate):
    """生成优化建议"""
    suggestions = []
    
    if localization_rate < 35:
        suggestions.append('- ⚠️ 本地化率偏低，建议将更多简单任务路由到本地模型')
    elif localization_rate >= 45:
        suggestions.append('- ✅ 本地化率良好，继续保持')
    
    if qwen_rate > 90:
        suggestions.append('- 🚨 百炼配额紧张，建议降级到本地模型或 Gemini')
    elif qwen_rate < 50:
        suggestions.append('- 💡 百炼配额充足，可正常使用')
    
    if gemini_rate > 90:
        suggestions.append('- 🚨 Gemini 配额紧张，建议减少长文档分析')
    elif gemini_rate < 50:
        suggestions.append('- 💡 Gemini 配额充足，可用于更多长文本任务')
    
    if not suggestions:
        suggestions.append('- ✅ 一切正常，无需优化')
    
    return '\n'.join(suggestions)


def record_usage(model, tokens, task_type='unknown'):
    """记录一次模型使用"""
    stats = load_today_usage()
    
    # 更新模型统计
    if model not in stats['models']:
        stats['models'][model] = {
            'calls': 0,
            'tokens': 0,
            'cost': 0.0
        }
    
    stats['models'][model]['calls'] += 1
    stats['models'][model]['tokens'] += tokens
    stats['models'][model]['cost'] += calculate_cost(model, tokens)
    
    # 更新总计
    stats['total_tasks'] += 1
    stats['total_tokens'] += tokens
    stats['total_cost'] += calculate_cost(model, tokens)
    
    # 保存
    save_usage(stats)
    
    # 检查配额告警
    check_quota_alerts(stats, model)
    
    return stats


def calculate_cost(model, tokens):
    """计算成本"""
    rate = COST_RATES.get(model, 0)
    return rate * (tokens / 1000)


def check_quota_alerts(stats, model):
    """检查配额告警"""
    if model == 'qwen-plus':
        usage = stats['models'].get('qwen-plus', {}).get('calls', 0)
        quota = QUOTAS['qwen-plus']['daily']
        rate = usage / quota
        
        if rate >= ALERT_THRESHOLDS['exhausted']:
            send_alert('百炼配额已耗尽', 'critical')
        elif rate >= ALERT_THRESHOLDS['critical']:
            send_alert('百炼配额紧急 (98%)', 'critical')
        elif rate >= ALERT_THRESHOLDS['warning']:
            send_alert('百炼配额告警 (90%)', 'warning')
    
    elif model == 'gemini':
        usage = stats['models'].get('gemini', {}).get('calls', 0)
        quota = QUOTAS['gemini']['daily']
        rate = usage / quota
        
        if rate >= ALERT_THRESHOLDS['exhausted']:
            send_alert('Gemini 配额已耗尽', 'critical')
        elif rate >= ALERT_THRESHOLDS['critical']:
            send_alert('Gemini 配额紧急 (98%)', 'critical')
        elif rate >= ALERT_THRESHOLDS['warning']:
            send_alert('Gemini 配额告警 (90%)', 'warning')


def send_alert(message, level='warning'):
    """发送告警通知"""
    # 保存告警到文件
    alert_file = MEMORY_DIR / 'model-alerts.json'
    
    alerts = []
    if alert_file.exists():
        try:
            with open(alert_file, 'r') as f:
                alerts = json.load(f)
        except:
            pass
    
    alerts.append({
        'timestamp': datetime.now().isoformat(),
        'level': level,
        'message': message
    })
    
    # 只保留最近 10 条告警
    alerts = alerts[-10:]
    
    with open(alert_file, 'w') as f:
        json.dump(alerts, f, indent=2)
    
    # TODO: 发送微信通知
    print(f"[ALERT {level.upper()}] {message}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='模型使用追踪器')
    parser.add_argument('--model', type=str, default='local',
                       choices=['local', 'qwen-plus', 'gemini', 'coder'],
                       help='使用的模型')
    parser.add_argument('--tokens', type=int, default=1000,
                       help='Token 数量')
    parser.add_argument('--task-type', type=str, default='unknown',
                       help='任务类型')
    parser.add_argument('--show', action='store_true',
                       help='显示当前统计')
    
    args = parser.parse_args()
    
    if args.show:
        stats = load_today_usage()
        print(generate_markdown_report(stats))
    else:
        stats = record_usage(args.model, args.tokens, args.task_type)
        print(f"✅ 已记录：{args.model} ({args.tokens} tokens, {args.task_type})")
        print(f"   今日总任务：{stats['total_tasks']}, 总成本：¥{stats['total_cost']:.2f}")


if __name__ == '__main__':
    main()
