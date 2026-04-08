#!/usr/bin/env python3
"""
知几-E 失败轨迹分析 v1.0
灵感来源：AutoAgent 失败轨迹分析

功能:
1. 记录每笔失败交易的完整上下文
2. 分析失败模式
3. 自动生成策略调整建议
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from collections import Counter

class LossTrajectoryAnalyzer:
    """失败轨迹分析器"""
    
    def __init__(self, db_path: str = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"):
        self.db_path = Path(db_path)
        self.trades_file = Path("/home/nicola/.openclaw/workspace/logs/paper-trades-offline.jsonl")
        self.analysis_file = Path("/home/nicola/.openclaw/workspace/logs/loss-trajectory-analysis.json")
    
    def load_trades(self) -> List[Dict]:
        """加载交易记录"""
        if not self.trades_file.exists():
            print("⚠️ 交易日志不存在")
            return []
        
        trades = []
        with open(self.trades_file, 'r') as f:
            for line in f:
                if line.strip():
                    trade = json.loads(line)
                    # 标准化字段：profit < 0 视为 LOSS
                    if 'result' not in trade:
                        trade['result'] = 'LOSS' if trade.get('profit', 0) < 0 else 'WIN'
                    trades.append(trade)
        return trades
    
    def analyze_losses(self, trades: List[Dict]) -> Dict:
        """分析失败交易"""
        losses = [t for t in trades if t.get('result') == 'LOSS']
        
        if not losses:
            return {
                "total_losses": 0,
                "total_loss_amount": 0,
                "win_rate": self._calculate_win_rate(trades),
                "patterns": [],
                "suggestions": []
            }
        
        # 分析失败模式
        patterns = {
            "time_distribution": Counter(),
            "market_type": Counter(),
            "confidence_range": Counter(),
            "loss_amount_range": Counter()
        }
        
        total_loss = 0
        for loss in losses:
            # 时间分布
            ts = loss.get('timestamp', '')
            if ts:
                hour = ts.split('T')[1][:2] if 'T' in ts else '00'
                patterns["time_distribution"][hour] += 1
            
            # 置信度分布
            conf = loss.get('confidence', 0)
            if conf < 0.6:
                patterns["confidence_range"]["低置信度 (<60%)"] += 1
            elif conf < 0.7:
                patterns["confidence_range"]["中置信度 (60-70%)"] += 1
            else:
                patterns["confidence_range"]["高置信度 (>70%)"] += 1
            
            # 损失金额分布
            profit = loss.get('profit', 0)
            total_loss += profit
            if profit > -10000:
                patterns["loss_amount_range"]["小额 (<$10K)"] += 1
            elif profit > -50000:
                patterns["loss_amount_range"]["中额 ($10K-$50K)"] += 1
            else:
                patterns["loss_amount_range"]["大额 (>$50K)"] += 1
        
        # 识别主要失败模式
        top_patterns = []
        for category, counter in patterns.items():
            if counter:
                most_common = counter.most_common(3)
                top_patterns.append({
                    "category": category,
                    "top_patterns": most_common
                })
        
        # 生成建议
        suggestions = []
        
        # 低置信度失败多
        low_conf = patterns["confidence_range"].get("低置信度 (<60%)", 0)
        if low_conf > len(losses) * 0.3:
            suggestions.append({
                "issue": "低置信度交易失败率高",
                "action": "提高置信度阈值从 60% 到 65%",
                "priority": "P0"
            })
        
        # 大额损失多
        large_loss = patterns["loss_amount_range"].get("大额 (>$50K)", 0)
        if large_loss > len(losses) * 0.2:
            suggestions.append({
                "issue": "大额损失频发",
                "action": "降低单笔下注比例 (Kelly/4 → Kelly/6)",
                "priority": "P0"
            })
        
        # 特定时间段失败多
        time_dist = patterns["time_distribution"]
        if time_dist:
            peak_hour, peak_count = time_dist.most_common(1)[0]
            if peak_count > len(losses) * 0.3:
                suggestions.append({
                    "issue": f"{peak_hour}点时段失败集中",
                    "action": f"分析{peak_hour}点时段市场特征，考虑避开该时段",
                    "priority": "P1"
                })
        
        return {
            "total_losses": len(losses),
            "total_loss_amount": total_loss,
            "win_rate": self._calculate_win_rate(trades),
            "patterns": top_patterns,
            "suggestions": suggestions,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def _calculate_win_rate(self, trades: List[Dict]) -> float:
        """计算胜率"""
        if not trades:
            return 0.0
        wins = sum(1 for t in trades if t.get('result') == 'WIN')
        return wins / len(trades)
    
    def save_analysis(self, analysis: Dict):
        """保存分析结果"""
        with open(self.analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        print(f"✅ 分析已保存：{self.analysis_file}")
    
    def generate_report(self, analysis: Dict) -> str:
        """生成人类可读报告"""
        report = []
        report.append("# 知几-E 失败轨迹分析报告")
        report.append(f"\n分析时间：{analysis.get('analyzed_at', 'N/A')}")
        report.append(f"\n## 核心指标")
        report.append(f"- 总失败次数：{analysis['total_losses']}")
        report.append(f"- 总损失金额：${analysis['total_loss_amount']:,.2f}")
        report.append(f"- 胜率：{analysis['win_rate']*100:.1f}%")
        
        report.append(f"\n## 失败模式")
        for pattern in analysis.get('patterns', []):
            report.append(f"\n### {pattern['category']}")
            for item, count in pattern['top_patterns']:
                report.append(f"- {item}: {count}次")
        
        report.append(f"\n## 改进建议")
        for sug in analysis.get('suggestions', []):
            report.append(f"\n### [{sug['priority']}] {sug['issue']}")
            report.append(f"**行动**: {sug['action']}")
        
        return "\n".join(report)

# 使用示例
if __name__ == "__main__":
    analyzer = LossTrajectoryAnalyzer()
    
    print("📊 加载交易记录...")
    trades = analyzer.load_trades()
    print(f"  找到 {len(trades)} 笔交易")
    
    if trades:
        print("\n🔍 分析失败轨迹...")
        analysis = analyzer.analyze_losses(trades)
        
        print(f"\n✅ 分析完成:")
        print(f"  失败次数：{analysis['total_losses']}")
        print(f"  胜率：{analysis['win_rate']*100:.1f}%")
        print(f"  建议数：{len(analysis['suggestions'])}")
        
        # 保存分析
        analyzer.save_analysis(analysis)
        
        # 生成报告
        report = analyzer.generate_report(analysis)
        print("\n" + "="*50)
        print(report)
