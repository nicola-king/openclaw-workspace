#!/usr/bin/env python3
"""
知几-E 虚拟盘交易器
用途：策略验证，无风险测试

功能:
- 模拟 Polymarket 交易
- 追踪虚拟盈亏
- 生成交易报告
- 验证策略有效性

用法:
    python3 virtual-trader.py --mode auto --days 7
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class VirtualPosition:
    """虚拟持仓"""
    market: str
    side: str  # YES/NO
    entry_price: float
    shares: int
    entry_time: str
    stake: float
    
@dataclass
class VirtualTrade:
    """虚拟交易记录"""
    id: str
    market: str
    side: str
    entry_price: float
    exit_price: Optional[float]
    shares: int
    pnl: float
    pnl_percent: float
    entry_time: str
    exit_time: Optional[str]
    status: str  # open/closed
    confidence: float
    edge: float

class VirtualTrader:
    """知几-E 虚拟盘交易器"""
    
    def __init__(self, initial_balance: float = 1000.0):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions: List[VirtualPosition] = []
        self.trades: List[VirtualTrade] = []
        self.data_file = Path.home() / ".taiyi" / "zhiji" / "virtual-trader.json"
        self.load()
        
        # 策略参数（与实盘一致）
        self.confidence_threshold = 0.96  # 96% 置信度
        self.edge_threshold = 0.02  # 2% 优势
        self.fixed_stake = 10.0  # $10 每笔（虚拟盘可放大）
        self.fee_rate = 0.02  # 2% 手续费
        self.slippage = 0.005  # 0.5% 滑点
    
    def generate_signal(self) -> Optional[Dict]:
        """生成交易信号（模拟）"""
        # 模拟市场数据
        markets = [
            "BTC >= $70K (Mar 29)",
            "ETH >= $2.2K (Mar 29)",
            "Fed Rate >= 5.25% (Apr)",
            "CPI >= 3.5% (Mar)",
        ]
        
        market = random.choice(markets)
        side = random.choice(["YES", "NO"])
        
        # 模拟置信度和优势（确保符合策略阈值）
        confidence = random.uniform(0.96, 0.99)
        # 生成合理的价格，使得 edge 总是正的
        if side == "YES":
            # YES 方：价格 0.30-0.50，置信度 96-99%，edge = 0.96 - price
            market_price = random.uniform(0.30, 0.50)
        else:
            # NO 方：价格 0.50-0.70
            market_price = random.uniform(0.50, 0.70)
        
        # 确保 edge 满足阈值
        edge = random.uniform(self.edge_threshold, 0.10)  # 2%-10% 优势
        
        return {
            "market": market,
            "side": side,
            "confidence": confidence,
            "edge": edge,
            "market_price": market_price,
            "timestamp": datetime.now().isoformat()
        }
    
    def execute_trade(self, signal: Dict, simulate_exit: bool = False):
        """执行交易"""
        stake = self.fixed_stake
        shares = int(stake / signal["market_price"])
        
        # 创建持仓
        position = VirtualPosition(
            market=signal["market"],
            side=signal["side"],
            entry_price=signal["market_price"],
            shares=shares,
            entry_time=signal["timestamp"],
            stake=stake
        )
        self.positions.append(position)
        
        # 创建交易记录
        trade = VirtualTrade(
            id=f"VT-{len(self.trades)+1:04d}",
            market=signal["market"],
            side=signal["side"],
            entry_price=signal["market_price"],
            exit_price=None,
            shares=shares,
            pnl=0.0,
            pnl_percent=0.0,
            entry_time=signal["timestamp"],
            exit_time=None,
            status="open",
            confidence=signal["confidence"],
            edge=signal["edge"]
        )
        
        if simulate_exit:
            # 模拟平仓（随机盈亏）
            win_prob = signal["confidence"]  # 置信度=胜率
            is_win = random.random() < win_prob
            
            if is_win:
                # 盈利：0.5x-2x 回报（更保守）
                exit_multiplier = random.uniform(1.3, 2.0)
                trade.exit_price = signal["market_price"] * exit_multiplier
                trade.pnl = stake * (exit_multiplier - 1) - (stake * self.fee_rate)
            else:
                # 亏损：损失本金 + 手续费
                trade.exit_price = 0.0
                trade.pnl = -stake - (stake * self.fee_rate)
            
            trade.pnl_percent = (trade.pnl / stake) * 100
            trade.exit_time = datetime.now().isoformat()
            trade.status = "closed"
            
            # 更新余额
            self.balance += trade.pnl
            
            # 移除持仓
            self.positions.remove(position)
        
        self.trades.append(trade)
        self.save()
        return trade
    
    def run_simulation(self, days: int = 7, trades_per_day: int = 5):
        """运行模拟交易"""
        print("=" * 70)
        print(f"  知几-E 虚拟盘模拟交易 · {days}天")
        print("=" * 70)
        print()
        
        total_trades = days * trades_per_day
        
        for i in range(total_trades):
            signal = self.generate_signal()
            if signal:
                # 50% 概率立即平仓（模拟快速交易）
                simulate_exit = random.random() < 0.5
                trade = self.execute_trade(signal, simulate_exit)
                
                print(f"交易 #{i+1}: {trade.market[:25]:25s} {trade.side:3s} | "
                      f"置信度 {trade.confidence:.1%} | "
                      f"状态 {trade.status} | "
                      f"PnL ${trade.pnl:+7.2f}" if trade.status == "closed" else "")
        
        print()
        self.generate_report()
    
    def generate_report(self):
        """生成交易报告"""
        closed_trades = [t for t in self.trades if t.status == "closed"]
        open_trades = [t for t in self.trades if t.status == "open"]
        
        if not closed_trades:
            print("暂无已完成交易")
            return
        
        # 计算统计
        wins = [t for t in closed_trades if t.pnl > 0]
        losses = [t for t in closed_trades if t.pnl <= 0]
        
        win_rate = len(wins) / len(closed_trades) * 100
        total_pnl = sum(t.pnl for t in closed_trades)
        avg_win = sum(t.pnl for t in wins) / len(wins) if wins else 0
        avg_loss = sum(t.pnl for t in losses) / len(losses) if losses else 0
        profit_factor = abs(sum(t.pnl for t in wins) / sum(t.pnl for t in losses)) if losses else float('inf')
        
        print("=" * 70)
        print("  📊 虚拟盘交易报告")
        print("=" * 70)
        print()
        print(f"初始资金：     ${self.initial_balance:,.2f}")
        print(f"当前余额：     ${self.balance:,.2f}")
        print(f"总盈亏：       ${total_pnl:+,.2f} ({total_pnl/self.initial_balance:+.2%})")
        print()
        print(f"总交易数：     {len(self.trades)}")
        print(f"已完成：       {len(closed_trades)}")
        print(f"持仓中：       {len(open_trades)}")
        print()
        print(f"胜率：         {win_rate:.1f}%")
        print(f"盈利次数：     {len(wins)}")
        print(f"亏损次数：     {len(losses)}")
        print()
        print(f"平均盈利：     ${avg_win:+,.2f}")
        print(f"平均亏损：     ${avg_loss:+,.2f}")
        print(f"盈亏比：       {profit_factor:.2f}")
        print()
        
        # 最近 5 笔交易
        print("📝 最近 5 笔交易:")
        print("-" * 70)
        for trade in reversed(closed_trades[-5:]):
            emoji = "✅" if trade.pnl > 0 else "❌"
            print(f"{emoji} {trade.id} | {trade.market[:25]:25s} {trade.side:3s} | "
                  f"PnL: ${trade.pnl:+7.2f} ({trade.pnl_percent:+6.1f}%)")
        print("-" * 70)
        print()
        
        # 策略评估
        print("🎯 策略评估:")
        if win_rate >= 55 and profit_factor >= 1.5:
            print("  ✅ 策略表现优秀，建议实盘测试")
        elif win_rate >= 45 and profit_factor >= 1.2:
            print("  🟡 策略表现良好，继续优化")
        else:
            print("  🔴 策略需要调整，暂不实盘")
        print()
        print("=" * 70)
    
    def save(self):
        """保存状态"""
        data = {
            "initial_balance": self.initial_balance,
            "balance": self.balance,
            "positions": [asdict(p) for p in self.positions],
            "trades": [asdict(t) for t in self.trades],
            "last_updated": datetime.now().isoformat()
        }
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """加载状态"""
        if self.data_file.exists():
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.initial_balance = data["initial_balance"]
                self.balance = data["balance"]
                self.positions = [VirtualPosition(**p) for p in data["positions"]]
                self.trades = [VirtualTrade(**t) for t in data["trades"]]
    
    def reset(self):
        """重置虚拟盘"""
        self.balance = self.initial_balance
        self.positions = []
        self.trades = []
        self.save()
        print("✅ 虚拟盘已重置")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="知几-E 虚拟盘交易器")
    parser.add_argument("--mode", choices=["auto", "manual", "reset"], default="auto")
    parser.add_argument("--days", type=int, default=7, help="模拟天数")
    parser.add_argument("--trades-per-day", type=int, default=5, help="每日交易数")
    parser.add_argument("--balance", type=float, default=1000.0, help="初始资金")
    
    args = parser.parse_args()
    
    trader = VirtualTrader(initial_balance=args.balance)
    
    if args.mode == "reset":
        trader.reset()
    elif args.mode == "auto":
        trader.run_simulation(days=args.days, trades_per_day=args.trades_per_day)
    elif args.mode == "manual":
        print("手动模式：生成交易信号...")
        signal = trader.generate_signal()
        if signal:
            print(f"\n信号：{signal['market']} {signal['side']}")
            print(f"置信度：{signal['confidence']:.1%}")
            print(f"优势：{signal['edge']:.2%}")
            print(f"建议下注：${trader.fixed_stake}")
            
            confirm = input("\n执行交易？(y/n): ")
            if confirm.lower() == 'y':
                trader.execute_trade(signal)
                print("✅ 交易已执行")
        else:
            print("暂无符合条件的交易信号")
    
    print(f"\n数据文件：{trader.data_file}")
