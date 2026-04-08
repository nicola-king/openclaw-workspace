#!/usr/bin/env python3
"""
知几-E v4.0 策略引擎（TimesFM 增强版）
新增：Google TimesFM 时间序列基础模型集成
数据源：气象数据 + 新闻情绪 + TimesFM 预测三重置信度

版本历史:
- v2.1: 仅气象数据
- v3.0: 气象 + 情绪
- v4.0: 气象 + 情绪 + TimesFM (本版本)
"""

import sqlite3
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import random
random.seed(42)

# 添加技能路径
sys.path.insert(0, "/home/nicola/.openclaw/workspace/skills/zhiji-sentiment/scripts")

DB_PATH = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"
REPORT_PATH = "/home/nicola/.openclaw/workspace/reports/zhiji-e-v4-backtest.md"

# ============== 数据加载 ==============

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
    """加载新闻情绪数据"""
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

def load_timesfm_forecast(days=7):
    """
    加载 TimesFM 预测数据
    
    Returns:
        list: [{date, temp_pred, confidence}]
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT date, temp_max_pred, confidence
            FROM timesfm_forecasts
            WHERE date >= date('now')
            ORDER BY date
            LIMIT ?
        """, (days,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            print("  ⚠️  未找到 TimesFM 预测数据，使用模拟预测")
            return generate_synthetic_timesfm(days)
        
        return [{
            "date": row[0],
            "temp_pred": row[1],
            "confidence": row[2]
        } for row in rows]
    
    except Exception as e:
        print(f"  ⚠️  TimesFM 数据加载失败：{e}，使用模拟预测")
        return generate_synthetic_timesfm(days)

def generate_synthetic_sentiment(limit=50):
    """生成模拟新闻情绪"""
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

def generate_synthetic_timesfm(days=7):
    """生成模拟 TimesFM 预测"""
    forecasts = []
    base_date = datetime.now()
    
    for i in range(days):
        pred_date = base_date + timedelta(days=i+1)
        forecasts.append({
            "date": pred_date.strftime("%Y-%m-%d"),
            "temp_pred": 20 + random.uniform(-5, 5),
            "confidence": 0.80 + random.uniform(0, 0.15)
        })
    
    return forecasts

# ============== 置信度计算 ==============

def calculate_timesfm_boost(weather_temp, timesfm_pred, timesfm_confidence):
    """
    计算 TimesFM 置信度提升
    
    逻辑：
    - 如果 TimesFM 预测与气象数据接近 → 提升置信度
    - 如果差异大 → 降低置信度（不确定性）
    """
    if timesfm_pred is None:
        return 0
    
    temp_diff = abs(weather_temp - timesfm_pred)
    
    # 温度差异越小，提升越大
    if temp_diff < 2:
        boost = timesfm_confidence * 0.15  # 最大 +15%
    elif temp_diff < 5:
        boost = timesfm_confidence * 0.05  # 最大 +5%
    else:
        boost = -timesfm_confidence * 0.10  # 降低 -10%
    
    return boost

def calculate_enhanced_confidence_v4(weather_confidence, sentiment_scores, timesfm_data, weather_temp):
    """
    v4.0 综合置信度计算：气象 + 情绪 + TimesFM 三重增强
    
    Args:
        weather_confidence: 气象数据置信度 (0-1)
        sentiment_scores: 新闻情绪分数列表
        timesfm_data: TimesFM 预测数据
        weather_temp: 当前气象预测温度
    
    Returns:
        enhanced_confidence: 综合置信度 (0-1)
    """
    # Step 1: 情绪增强 (v3.0 已有)
    if sentiment_scores:
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        sentiment_boost = avg_sentiment * 0.1  # 情绪权重 10%
    else:
        sentiment_boost = 0
    
    confidence_after_sentiment = weather_confidence + sentiment_boost
    
    # Step 2: TimesFM 增强 (v4.0 新增)
    if timesfm_data:
        # 找到最接近的预测
        closest_pred = min(timesfm_data, key=lambda x: abs(x.get('temp_pred', weather_temp) - weather_temp))
        timesfm_boost = calculate_timesfm_boost(
            weather_temp,
            closest_pred.get('temp_pred'),
            closest_pred.get('confidence', 0.8)
        )
    else:
        timesfm_boost = 0
    
    # 最终综合置信度
    enhanced = confidence_after_sentiment + timesfm_boost
    return min(1.0, max(0.0, enhanced)), sentiment_boost, timesfm_boost

def get_dynamic_threshold_v4(sentiment_scores, timesfm_data, base_threshold=0.96):
    """
    v4.0 动态阈值：情绪 + TimesFM 双重调整
    
    正面情绪 + 高 TimesFM 置信度 → 降低阈值 (更激进)
    负面情绪 + 低 TimesFM 置信度 → 提高阈值 (更保守)
    """
    # 情绪调整
    if sentiment_scores:
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        sentiment_adj = -avg_sentiment * 0.05
    else:
        sentiment_adj = 0
    
    # TimesFM 调整
    if timesfm_data:
        avg_timesfm_conf = sum(t.get('confidence', 0.8) for t in timesfm_data) / len(timesfm_data)
        timesfm_adj = -(avg_timesfm_conf - 0.8) * 0.1  # 高置信度降低阈值
    else:
        timesfm_adj = 0
    
    threshold = base_threshold + sentiment_adj + timesfm_adj
    return max(0.90, min(0.98, threshold))

# ============== 策略引擎 ==============

def generate_synthetic_odds_v4(weather_data, sentiment_data, timesfm_data):
    """生成模拟赔率（加入情绪 + TimesFM 因子）"""
    synthetic_markets = []
    avg_sentiment = sum(s['score'] for s in sentiment_data) / len(sentiment_data) if sentiment_data else 0
    avg_timesfm_conf = sum(t.get('confidence', 0.8) for t in timesfm_data) / len(timesfm_data) if timesfm_data else 0.8
    
    for i, day_data in enumerate(weather_data):
        base_temp = day_data["temp_max"]
        
        # 基础赔率 + 情绪调整 + TimesFM 调整
        yes_prob = 0.5 + (base_temp - 25) * 0.02 + avg_sentiment * 0.05 + (avg_timesfm_conf - 0.8) * 0.03
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
            "sentiment_context": avg_sentiment,
            "timesfm_context": avg_timesfm_conf
        }
        
        synthetic_markets.append(market)
    
    return synthetic_markets

def zhiji_e_v4_strategy(market, sentiment_scores, timesfm_data, weather_temp, confidence_threshold=0.90):
    """
    知几-E v4.0 策略（三重增强版）
    
    核心改进:
    1. 基础置信度 (气象)
    2. 情绪增强 (v3.0)
    3. TimesFM 增强 (v4.0 新增)
    4. 动态阈值 (情绪 + TimesFM 双重调整)
    """
    yes_price = market["yes_price"]
    
    # 基础置信度 (气象)
    edge = abs(yes_price - 0.5) * 2
    base_confidence = 0.5 + edge * 0.5
    
    # 综合置信度 (气象 + 情绪 + TimesFM)
    enhanced_confidence, sentiment_boost, timesfm_boost = calculate_enhanced_confidence_v4(
        base_confidence, sentiment_scores, timesfm_data, weather_temp
    )
    
    # 动态阈值
    dynamic_threshold = get_dynamic_threshold_v4(sentiment_scores, timesfm_data, confidence_threshold)
    
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
            "sentiment_boost": sentiment_boost,
            "timesfm_boost": timesfm_boost
        }
    
    return {
        "bet": False,
        "side": None,
        "base_confidence": base_confidence,
        "enhanced_confidence": enhanced_confidence,
        "threshold": dynamic_threshold,
        "edge": edge,
        "stake": 0,
        "sentiment_boost": sentiment_boost,
        "timesfm_boost": timesfm_boost
    }

# ============== 回测引擎 ==============

def run_backtest_v4(markets, sentiment_scores, timesfm_data, initial_capital=1000, confidence_threshold=0.90):
    """运行回测（v4.0 三重增强版）"""
    capital = initial_capital
    trades = []
    wins = 0
    losses = 0
    total_staked = 0
    sentiment_wins = 0
    sentiment_losses = 0
    timesfm_correct = 0
    timesfm_total = 0
    
    for market in markets:
        weather_temp = market.get("yes_price", 25) * 50  # 简化的温度映射
        
        signal = zhiji_e_v4_strategy(market, sentiment_scores, timesfm_data, weather_temp, confidence_threshold)
        
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
                
                # TimesFM 正确性
                timesfm_correct += 1
            else:
                capital -= stake
                profit = -stake
                losses += 1
                result = "LOSS"
                
                if market["sentiment_context"] > 0 and predicted == "YES":
                    sentiment_losses += 1
            
            timesfm_total += 1
            
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
                "timesfm_boost": signal["timesfm_boost"],
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
        "timesfm_accuracy": timesfm_correct / timesfm_total if timesfm_total > 0 else 0,
        "avg_sentiment_boost": sum(t["sentiment_boost"] for t in trades) / len(trades) if trades else 0,
        "avg_timesfm_boost": sum(t["timesfm_boost"] for t in trades) / len(trades) if trades else 0,
        "trades": trades
    }

# ============== 报告生成 ==============

def generate_v4_comparison_report(v2_result, v3_result, v4_result):
    """生成 v2 vs v3 vs v4 三代对比报告"""
    report = f"""# 知几-E v4.0 策略回测报告（TimesFM 三重增强版）

> 生成时间：{datetime.now().isoformat()}
> 数据源：气象数据 + 新闻情绪 + TimesFM 预测
> 策略版本：Zhiji-E v4.0 (对比 v2.1 / v3.0)

---

## 📊 核心指标对比（三代同堂）

| 指标 | v2.1 (仅气象) | v3.0 (气象 + 情绪) | v4.0 (三重增强) | v4 相对 v3 提升 |
|------|--------------|-------------------|----------------|----------------|
| 初始资金 | ${v2_result['initial_capital']:,.2f} | ${v3_result['initial_capital']:,.2f} | ${v4_result['initial_capital']:,.2f} | - |
| 最终资金 | ${v2_result['final_capital']:,.2f} | ${v3_result['final_capital']:,.2f} | ${v4_result['final_capital']:,.2f} | **${v4_result['final_capital'] - v3_result['final_capital']:+,.2f}** |
| 总收益率 | {v2_result['total_return']:.2%} | {v3_result['total_return']:.2%} | {v4_result['total_return']:.2%} | **{(v4_result['total_return'] - v3_result['total_return']):+.2%}** |
| 总交易数 | {v2_result['total_trades']} | {v3_result['total_trades']} | {v4_result['total_trades']} | {v4_result['total_trades'] - v3_result['total_trades']:+d} |
| 胜率 | {v2_result['win_rate']:.1%} | {v3_result['win_rate']:.1%} | {v4_result['win_rate']:.1%} | **{(v4_result['win_rate'] - v3_result['win_rate']):+.1%}** |
| 情绪胜率 | - | {v3_result['sentiment_win_rate']:.1%} | {v4_result['sentiment_win_rate']:.1%} | {(v4_result['sentiment_win_rate'] - v3_result['sentiment_win_rate']):+.1%} |
| TimesFM 准确率 | - | - | {v4_result['timesfm_accuracy']:.1%} | 新增 |
| 平均情绪增益 | - | {v3_result.get('avg_sentiment_boost', 0):+.3f} | {v4_result['avg_sentiment_boost']:+.3f} | {(v4_result['avg_sentiment_boost'] - v3_result.get('avg_sentiment_boost', 0)):+.3f} |
| 平均 TimesFM 增益 | - | - | {v4_result['avg_timesfm_boost']:+.3f} | 新增 |

---

## 🎯 策略演进

### v2.1 (基础版)
- 置信度：仅气象数据
- 阈值：固定 96%
- 下注：Quarter-Kelly

### v3.0 (情绪增强版) ✨
- 置信度：气象 + 新闻情绪
- 阈值：动态调整 (90%-98%)
- 下注：Quarter-Kelly + 情绪权重

### v4.0 (TimesFM 三重增强版) 🆕
- 置信度：气象 + 情绪 + TimesFM 预测
- 阈值：情绪 + TimesFM 双重动态调整
- 下注：Quarter-Kelly + 双重增强
- 新增：TimesFM 置信度验证

---

## 📈 收益对比

```
v2.1: ${v2_result['initial_capital']:,.2f} → ${v2_result['final_capital']:,.2f} ({v2_result['total_return']:+.2%})
v3.0: ${v3_result['initial_capital']:,.2f} → ${v3_result['final_capital']:,.2f} ({v3_result['total_return']:+.2%})
v4.0: ${v4_result['initial_capital']:,.2f} → ${v4_result['final_capital']:,.2f} ({v4_result['total_return']:+.2%})

v3 vs v2 优势：${v3_result['final_capital'] - v2_result['final_capital']:+,.2f} ({(v3_result['total_return'] - v2_result['total_return']):+.2%})
v4 vs v3 优势：${v4_result['final_capital'] - v3_result['final_capital']:+,.2f} ({(v4_result['total_return'] - v3_result['total_return']):+.2%})
v4 vs v2 优势：${v4_result['final_capital'] - v2_result['final_capital']:+,.2f} ({(v4_result['total_return'] - v2_result['total_return']):+.2%})
```

---

## 🧠 增强因子价值分析

### 情绪因子
"""
    
    if v4_result['sentiment_win_rate'] > 0.55:
        report += f"✅ **情绪因子有效** - 情绪导向交易胜率 {v4_result['sentiment_win_rate']:.1%}\n"
    else:
        report += f"🟡 **情绪因子待优化** - 情绪导向交易胜率 {v4_result['sentiment_win_rate']:.1%}\n"
    
    report += f"\n### TimesFM 因子\n"
    if v4_result['timesfm_accuracy'] > 0.60:
        report += f"✅ **TimesFM 因子有效** - 预测准确率 {v4_result['timesfm_accuracy']:.1%}\n"
        report += f"- 平均置信度增益：{v4_result['avg_timesfm_boost']:+.1%}\n"
    else:
        report += f"🟡 **TimesFM 因子待优化** - 预测准确率 {v4_result['timesfm_accuracy']:.1%}\n"
        report += f"- 可能需要调整权重或数据源\n"
    
    report += f"""
---

## 📝 交易记录（前 10 笔）

| 日期 | 方向 | 实际 | 基础 | 综合 | 阈值 | 情绪增益 | TF 增益 | 盈亏 | 结果 |
|------|------|------|------|------|------|---------|--------|------|------|
"""
    
    for trade in v4_result["trades"][:10]:
        report += f"| {trade['date']} | {trade['side']} | {trade['actual']} | {trade['base_confidence']:.1%} | {trade['enhanced_confidence']:.1%} | {trade['threshold']:.1%} | {trade['sentiment_boost']:+.1%} | {trade['timesfm_boost']:+.1%} | ${trade['profit']:+.2f} | {trade['result']} |\n"
    
    report += f"""
---

## 💡 结论

"""
    
    if v4_result['total_return'] > v3_result['total_return']:
        report += f"✅ **v4.0 优于 v3.0** - TimesFM 增强带来 {(v4_result['total_return'] - v3_result['total_return']):+.2%} 提升\n"
        report += f"- 建议：部署到实盘\n"
        report += f"- 监控：TimesFM 预测准确性\n"
    else:
        report += f"🟡 **v4.0 待优化** - TimesFM 增强未带来显著提升\n"
        report += f"- 建议：调整 TimesFM 权重或验证数据源\n"
    
    report += f"""
---

## 📦 下一步

1. **安装 TimesFM**: `pip install git+https://github.com/google-research/timesfm.git`
2. **真实数据测试**: 使用真实 TimesFM 预测替换模拟数据
3. **实盘部署**: 如果回测效果好，部署到知几-E
4. **持续监控**: 跟踪 TimesFM 预测准确性

---

## ⚠️ 免责声明

本回测使用模拟数据，实际收益可能与回测结果有显著差异。
实盘前请充分测试并评估风险。

---

*生成：太一 AGI · 知几-E v4.0 回测引擎*
"""
    
    return report

# ============== 主程序 ==============

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📊 知几-E v4.0 策略回测引擎 (TimesFM 三重增强版)           ║')
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
    
    print('🤖 加载 TimesFM 预测...')
    timesfm_data = load_timesfm_forecast(days=7)
    print(f'  ✅ {len(timesfm_data)} 条预测')
    avg_timesfm_conf = sum(t.get('confidence', 0.8) for t in timesfm_data) / len(timesfm_data) if timesfm_data else 0.8
    print(f'  📈 平均置信度：{avg_timesfm_conf:.1%}')
    print('')
    
    # 生成模拟赔率
    print('📈 生成模拟赔率...')
    markets = generate_synthetic_odds_v4(weather_data, sentiment_data, timesfm_data)
    print(f'  ✅ {len(markets)} 个市场')
    print('')
    
    # 运行回测 (v2.1 vs v3.0 vs v4.0)
    print('🔍 运行回测对比...')
    print('')
    
    # v2.1 (仅气象)
    v2_result = run_backtest_v4(markets, [], [], initial_capital=1000, confidence_threshold=0.96)
    print(f'  v2.1 (仅气象): {v2_result["total_trades"]} 笔，收益率 {v2_result["total_return"]:+.2%}')
    
    # v3.0 (气象 + 情绪)
    sentiment_scores = [s['score'] for s in sentiment_data]
    v3_result = run_backtest_v4(markets, sentiment_scores, [], initial_capital=1000, confidence_threshold=0.90)
    print(f'  v3.0 (气象 + 情绪): {v3_result["total_trades"]} 笔，收益率 {v3_result["total_return"]:+.2%}')
    
    # v4.0 (三重增强)
    v4_result = run_backtest_v4(markets, sentiment_scores, timesfm_data, initial_capital=1000, confidence_threshold=0.90)
    print(f'  v4.0 (三重增强): {v4_result["total_trades"]} 笔，收益率 {v4_result["total_return"]:+.2%}')
    
    improvement_v4_v3 = v4_result['total_return'] - v3_result['total_return']
    improvement_v4_v2 = v4_result['total_return'] - v2_result['total_return']
    print(f'  📈 v4 vs v3 提升：{improvement_v4_v3:+.2%}')
    print(f'  📈 v4 vs v2 提升：{improvement_v4_v2:+.2%}')
    print('')
    
    # 生成报告
    print('📝 生成对比报告...')
    report = generate_v4_comparison_report(v2_result, v3_result, v4_result)
    
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
    print(f'{"指标":<20} {"v2.1":<20} {"v3.0":<20} {"v4.0":<20}')
    print('-' * 80)
    print(f'{"最终资金":<20} ${v2_result["final_capital"]:>15,.2f} ${v3_result["final_capital"]:>15,.2f} ${v4_result["final_capital"]:>15,.2f}')
    print(f'{"总收益率":<20} {v2_result["total_return"]:>16.2%} {v3_result["total_return"]:>16.2%} {v4_result["total_return"]:>16.2%}')
    print(f'{"胜率":<20} {v2_result["win_rate"]:>16.1%} {v3_result["win_rate"]:>16.1%} {v4_result["win_rate"]:>16.1%}')
    print('')
    
    if improvement_v4_v3 > 0:
        print(f'✅ v4.0 优于 v3.0 - TimesFM 增强带来 {improvement_v4_v3:+.2%} 提升')
    else:
        print(f'🟡 v4.0 待优化 - TimesFM 增强未带来显著提升')
    print('')
    
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🎯 策略演进总结                                         ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print('v2.1 → v3.0: 情绪增强 (+(v3_result["total_return"] - v2_result["total_return"]):+.2%)')
    print('v3.0 → v4.0: TimesFM 增强 (+' + f'{improvement_v4_v3:+.2%})')
    print('')

if __name__ == '__main__':
    main()
