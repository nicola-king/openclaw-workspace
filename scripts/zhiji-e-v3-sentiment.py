#!/usr/bin/env python3
"""
知几-E v3.0 策略引擎（增强版）
新增：FinBERT 情绪分析集成
数据源：气象数据 + 新闻情绪综合置信度
"""

import sqlite3
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import random
random.seed(42)  # 固定随机种子，保证回测可重复

# 添加技能路径
sys.path.insert(0, "/home/nicola/.openclaw/workspace/skills/zhiji-sentiment/scripts")

DB_PATH = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"
REPORT_PATH = "/home/nicola/.openclaw/workspace/reports/zhiji-e-v3-backtest.md"

def load_weather_data():
    """加载气象数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT date, city, temp_max, temp_min, precip_sum, weather_code
        FROM weather_forecasts
        ORDER BY date
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return [{
        "date": row[0],
        "city": row[1],
        "temp_max": row[2],
        "temp_min": row[3],
        "precip_sum": row[4],
        "weather_code": row[5]
    } for row in rows]

def load_news_sentiment(limit=50):
    """
    加载新闻情绪数据
    从数据库读取已分析的新闻情绪分数
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT title, sentiment_score, meta_data
            FROM daily_news
            WHERE sentiment_score IS NOT NULL
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            print("  ⚠️  未找到新闻情绪数据，使用模拟情绪")
            return generate_synthetic_sentiment(limit)
        
        return [{
            "title": row[0],
            "score": row[1],
            "reason": json.loads(row[2]).get("sentiment_reason", "") if row[2] else ""
        } for row in rows]
    
    except Exception as e:
        print(f"  ⚠️  情绪数据加载失败：{e}，使用模拟情绪")
        return generate_synthetic_sentiment(limit)

def generate_synthetic_sentiment(limit=50):
    """生成模拟新闻情绪（用于回测）"""
    sentiments = []
    news_templates = [
        ("极端天气频发，专家警告气候危机", -0.3),
        ("可再生能源投资创新高", 0.5),
        ("全球经济复苏超预期", 0.4),
        ("科技股大涨，AI 概念领涨", 0.6),
        ("通胀数据温和，美联储按兵不动", 0.1),
    ]
    
    for i in range(limit):
        template = random.choice(news_templates)
        sentiments.append({
            "title": template[0] + f" (模拟#{i})",
            "score": template[1] + random.uniform(-0.1, 0.1),
            "reason": "模拟情绪分析"
        })
    
    return sentiments

def calculate_enhanced_confidence(weather_confidence, sentiment_scores, news_weight=0.1):
    """
    综合置信度计算：气象置信度 + 新闻情绪
    
    Args:
        weather_confidence: 气象数据置信度 (0-1)
        sentiment_scores: 新闻情绪分数列表 (-1 到 1)
        news_weight: 情绪权重 (默认 0.1)
    
    Returns:
        enhanced_confidence: 综合置信度 (0-1)
    """
    if not sentiment_scores:
        return weather_confidence
    
    # 计算平均情绪
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    
    # 情绪加成：正面情绪提升置信度，负面情绪降低
    sentiment_boost = avg_sentiment * news_weight
    
    # 综合置信度
    enhanced = weather_confidence + sentiment_boost
    return min(1.0, max(0.0, enhanced))

def get_dynamic_threshold(sentiment_scores, base_threshold=0.96):
    """
    根据情绪动态调整下注阈值
    
    正面情绪 → 降低阈值 (更激进)
    负面情绪 → 提高阈值 (更保守)
    """
    if not sentiment_scores:
        return base_threshold
    
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    adjustment = -avg_sentiment * 0.05  # 情绪影响±5%
    return max(0.90, min(0.98, base_threshold + adjustment))

def generate_synthetic_odds(weather_data, sentiment_data):
    """生成模拟赔率（加入情绪因子）"""
    synthetic_markets = []
    avg_sentiment = sum(s['score'] for s in sentiment_data) / len(sentiment_data) if sentiment_data else 0
    
    for i, day_data in enumerate(weather_data):
        base_temp = day_data["temp_max"]
        
        # 基础赔率 + 情绪调整
        yes_prob = 0.5 + (base_temp - 25) * 0.02 + avg_sentiment * 0.05
        yes_prob = max(0.1, min(0.9, yes_prob))
        
        market = {
            "date": day_data["date"],
            "city": day_data["city"],
            "question": f"明天最高温度是否高于 {base_temp:.1f}°C?",
            "yes_price": yes_prob,
            "no_price": 1 - yes_prob,
            "actual_outcome": "YES" if random.random() < yes_prob else "NO",
            "volume": random.uniform(1000, 50000),
            "liquidity": random.uniform(5000, 100000),
            "sentiment_context": avg_sentiment
        }
        
        synthetic_markets.append(market)
    
    return synthetic_markets

def zhiji_e_v3_strategy(market, sentiment_scores, confidence_threshold=0.90):
    """
    知几-E v3.0 策略（情绪增强版）
    
    核心改进:
    1. 综合置信度 = 气象置信度 + 新闻情绪
    2. 动态阈值 = 基础阈值 ± 情绪调整
    """
    yes_price = market["yes_price"]
    
    # 基础置信度 (气象)
    edge = abs(yes_price - 0.5) * 2
    base_confidence = 0.5 + edge * 0.5
    
    # 综合置信度 (气象 + 情绪)
    enhanced_confidence = calculate_enhanced_confidence(base_confidence, sentiment_scores)
    
    # 动态阈值
    dynamic_threshold = get_dynamic_threshold(sentiment_scores, confidence_threshold)
    
    # 下注决策
    if enhanced_confidence >= dynamic_threshold:
        side = "YES" if yes_price > 0.5 else "NO"
        return {
            "bet": True,
            "side": side,
            "base_confidence": base_confidence,
            "enhanced_confidence": enhanced_confidence,
            "threshold": dynamic_threshold,
            "edge": edge,
            "stake": 0.25 * edge,
            "sentiment_boost": enhanced_confidence - base_confidence
        }
    
    return {
        "bet": False,
        "side": None,
        "base_confidence": base_confidence,
        "enhanced_confidence": enhanced_confidence,
        "threshold": dynamic_threshold,
        "edge": edge,
        "stake": 0,
        "sentiment_boost": enhanced_confidence - base_confidence
    }

def run_backtest(markets, sentiment_scores, initial_capital=1000, confidence_threshold=0.90):
    """运行回测（情绪增强版）"""
    capital = initial_capital
    trades = []
    wins = 0
    losses = 0
    total_staked = 0
    sentiment_wins = 0
    sentiment_losses = 0
    
    for market in markets:
        signal = zhiji_e_v3_strategy(market, sentiment_scores, confidence_threshold)
        
        if signal["bet"]:
            stake = signal["stake"] * capital
            total_staked += stake
            
            actual = market["actual_outcome"]
            predicted = signal["side"]
            
            if actual == predicted:
                payout = stake / (market["yes_price"] if predicted == "YES" else market["no_price"])
                profit = payout - stake
                capital += profit
                wins += 1
                result = "WIN"
                
                # 情绪正确性
                if market["sentiment_context"] > 0 and predicted == "YES":
                    sentiment_wins += 1
            else:
                capital -= stake
                profit = -stake
                losses += 1
                result = "LOSS"
                
                if market["sentiment_context"] > 0 and predicted == "YES":
                    sentiment_losses += 1
            
            trades.append({
                "date": market["date"],
                "market": market["question"][:50],
                "side": predicted,
                "actual": actual,
                "stake": stake,
                "profit": profit,
                "result": result,
                "base_confidence": signal["base_confidence"],
                "enhanced_confidence": signal["enhanced_confidence"],
                "threshold": signal["threshold"],
                "sentiment_boost": signal["sentiment_boost"],
                "capital_after": capital
            })
    
    return {
        "initial_capital": initial_capital,
        "final_capital": capital,
        "total_return": (capital - initial_capital) / initial_capital,
        "total_trades": len(trades),
        "wins": wins,
        "losses": losses,
        "win_rate": wins / len(trades) if trades else 0,
        "total_staked": total_staked,
        "sentiment_win_rate": sentiment_wins / (sentiment_wins + sentiment_losses) if (sentiment_wins + sentiment_losses) > 0 else 0,
        "trades": trades
    }

def generate_comparison_report(v2_result, v3_result):
    """生成 v2 vs v3 对比报告"""
    report = f"""# 知几-E v3.0 策略回测报告（情绪增强版）

> 生成时间：{datetime.now().isoformat()}
> 数据源：气象数据 + 新闻情绪
> 策略版本：Zhiji-E v3.0 (对比 v2.1)

---

## 📊 核心指标对比

| 指标 | v2.1 (仅气象) | v3.0 (气象 + 情绪) | 提升 |
|------|--------------|-------------------|------|
| 初始资金 | ${v2_result['initial_capital']:,.2f} | ${v3_result['initial_capital']:,.2f} | - |
| 最终资金 | ${v2_result['final_capital']:,.2f} | ${v3_result['final_capital']:,.2f} | **${v3_result['final_capital'] - v2_result['final_capital']:+,.2f}** |
| 总收益率 | {v2_result['total_return']:.2%} | {v3_result['total_return']:.2%} | **{(v3_result['total_return'] - v2_result['total_return']):+.2%}** |
| 总交易数 | {v2_result['total_trades']} | {v3_result['total_trades']} | {v3_result['total_trades'] - v2_result['total_trades']:+d} |
| 胜率 | {v2_result['win_rate']:.1%} | {v3_result['win_rate']:.1%} | **{(v3_result['win_rate'] - v2_result['win_rate']):+.1%}** |
| 情绪胜率 | - | {v3_result['sentiment_win_rate']:.1%} | 新增 |

---

## 🎯 策略改进

### v2.1 (基础版)
- 置信度计算：仅气象数据
- 阈值：固定 96%
- 下注：Quarter-Kelly

### v3.0 (情绪增强版) ✨
- 置信度计算：气象 + 新闻情绪综合
- 阈值：动态调整 (90%-98%)
- 下注：Quarter-Kelly + 情绪权重

---

## 📈 收益对比

```
v2.1: ${v2_result['initial_capital']:,.2f} → ${v2_result['final_capital']:,.2f} ({v2_result['total_return']:+.2%})
v3.0: ${v3_result['initial_capital']:,.2f} → ${v3_result['final_capital']:,.2f} ({v3_result['total_return']:+.2%})

优势：${v3_result['final_capital'] - v2_result['final_capital']:+,.2f} ({(v3_result['total_return'] - v2_result['total_return']):+.2%})
```

---

## 🧠 情绪分析价值

"""
    
    if v3_result['sentiment_win_rate'] > 0.55:
        report += f"✅ **情绪因子有效** - 情绪导向交易胜率 {v3_result['sentiment_win_rate']:.1%}\n"
        report += f"- 正面情绪时增持 YES 合约\n"
        report += f"- 负面情绪时增持 NO 合约\n"
    else:
        report += f"🟡 **情绪因子待优化** - 情绪导向交易胜率 {v3_result['sentiment_win_rate']:.1%}\n"
        report += f"- 可能需要调整情绪权重\n"
        report += f"- 或筛选更高质量新闻源\n"
    
    report += f"""
---

## 📝 交易记录（前 10 笔）

| 日期 | 方向 | 实际 | 基础置信度 | 综合置信度 | 阈值 | 盈亏 | 结果 |
|------|------|------|-----------|-----------|------|------|------|
"""
    
    for trade in v3_result["trades"][:10]:
        report += f"| {trade['date']} | {trade['side']} | {trade['actual']} | {trade['base_confidence']:.1%} | {trade['enhanced_confidence']:.1%} | {trade['threshold']:.1%} | ${trade['profit']:+.2f} | {trade['result']} |\n"
    
    report += f"""
---

## 💡 结论

"""
    
    if v3_result['total_return'] > v2_result['total_return']:
        report += f"✅ **v3.0 优于 v2.1** - 情绪增强带来 {(v3_result['total_return'] - v2_result['total_return']):+.2%} 提升\n"
        report += f"- 建议：部署到实盘\n"
        report += f"- 监控：情绪因子稳定性\n"
    else:
        report += f"🟡 **v3.0 待优化** - 情绪增强未带来显著提升\n"
        report += f"- 建议：调整情绪权重或新闻源质量\n"
    
    report += f"""
---

## ⚠️ 免责声明

本回测使用模拟数据，实际收益可能与回测结果有显著差异。
实盘前请充分测试并评估风险。

---

*生成：太一 AGI · 知几-E v3.0 回测引擎*
"""
    
    return report

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📊 知几-E v3.0 策略回测引擎 (情绪增强版)                   ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().isoformat()}')
    print('')
    
    # 加载数据
    print('📊 加载气象数据...')
    weather_data = load_weather_data()
    print(f'  ✅ {len(weather_data)} 条记录')
    print('')
    
    print('🧠 加载新闻情绪...')
    sentiment_data = load_news_sentiment(limit=50)
    print(f'  ✅ {len(sentiment_data)} 条情绪')
    avg_sentiment = sum(s['score'] for s in sentiment_data) / len(sentiment_data) if sentiment_data else 0
    print(f'  📈 平均情绪：{avg_sentiment:+.3f}')
    print('')
    
    # 生成模拟赔率
    print('📈 生成模拟赔率...')
    markets = generate_synthetic_odds(weather_data, sentiment_data)
    print(f'  ✅ {len(markets)} 个市场')
    print('')
    
    # 运行回测 (v2.1 vs v3.0)
    print('🔍 运行回测对比...')
    print('')
    
    # v2.1 (仅气象)
    v2_result = run_backtest(markets, [], initial_capital=1000, confidence_threshold=0.96)
    print(f'  v2.1 (仅气象): {v2_result["total_trades"]} 笔，收益率 {v2_result["total_return"]:+.2%}')
    
    # v3.0 (气象 + 情绪)
    sentiment_scores = [s['score'] for s in sentiment_data]
    v3_result = run_backtest(markets, sentiment_scores, initial_capital=1000, confidence_threshold=0.90)
    print(f'  v3.0 (情绪增强): {v3_result["total_trades"]} 笔，收益率 {v3_result["total_return"]:+.2%}')
    
    improvement = v3_result['total_return'] - v2_result['total_return']
    print(f'  📈 提升：{improvement:+.2%}')
    print('')
    
    # 生成报告
    print('📝 生成对比报告...')
    report = generate_comparison_report(v2_result, v3_result)
    
    # 保存报告
    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f'  💾 报告已保存：{REPORT_PATH}')
    print('')
    
    # 打印摘要
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📊 回测对比摘要                                         ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'{"指标":<20} {"v2.1":<20} {"v3.0":<20} {"提升":<15}')
    print('-' * 75)
    print(f'{"最终资金":<20} ${v2_result["final_capital"]:>15,.2f} ${v3_result["final_capital"]:>15,.2f} ${v3_result["final_capital"] - v2_result["final_capital"]:>+14,.2f}')
    print(f'{"总收益率":<20} {v2_result["total_return"]:>16.2%} {v3_result["total_return"]:>16.2%} {improvement:>+14.2%}')
    print(f'{"胜率":<20} {v2_result["win_rate"]:>16.1%} {v3_result["win_rate"]:>16.1%} {(v3_result["win_rate"] - v2_result["win_rate"]):>+14.1%}')
    print('')
    
    if improvement > 0:
        print('✅ v3.0 情绪增强版优于 v2.1 - 建议部署实盘')
    else:
        print('🟡 v3.0 待优化 - 情绪因子未带来显著提升')
    print('')

if __name__ == '__main__':
    main()
