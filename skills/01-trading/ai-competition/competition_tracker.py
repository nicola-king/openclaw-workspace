#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 交易系统竞争追踪器 v1.0

太一 (OpenClaw) vs Hermes
- 共用账号，不同 API
- 每日统计盈亏
- 每周测评
- 胜者自主配置算力

作者：太一 AGI
创建：2026-04-22
"""

import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
import logging

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/ai_competition.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AICompetitionTracker')

# 数据目录
DATA_DIR = Path("/home/nicola/.openclaw/workspace/data/ai-competition")
DATA_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class DailyResult:
    """每日交易结果"""
    date: str
    agent: str  # 'taiyi' or 'hermes'
    spot_pnl: float = 0.0  # 现货盈亏
    margin_pnl: float = 0.0  # 杠杆盈亏
    futures_pnl: float = 0.0  # 合约盈亏
    total_pnl: float = 0.0  # 总盈亏
    trades_count: int = 0  # 交易次数
    win_rate: float = 0.0  # 胜率
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        # 自动计算总盈亏
        if self.total_pnl == 0.0:
            self.total_pnl = self.spot_pnl + self.margin_pnl + self.futures_pnl


@dataclass
class WeeklyReport:
    """每周测评报告"""
    week_start: str
    week_end: str
    taiyi_total_pnl: float
    hermes_total_pnl: float
    taiyi_win_days: int
    hermes_win_days: int
    winner: str
    prize: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CompetitionConfig:
    """竞赛配置"""
    # 账户资金
    spot_balance: float = 100.0  # 现货 100U
    margin_balance: float = 20.0  # 杠杆 20U
    futures_balance: float = 20.0  # 合约 20U
    total_balance: float = 140.0  # 总计 140U
    
    # 竞赛配置
    competition_days: int = 7  # 竞赛天数
    evaluation_day: str = "Sunday"  # 测评日
    prize_type: str = "compute_power"  # 奖励类型
    auto_purchase: bool = True  # 自动购买算力
    independent_competition: bool = True  # 独立竞争模式


class AICompetitionTracker:
    """AI 竞争追踪器"""
    
    def __init__(self):
        self.config = CompetitionConfig()
        self.daily_results: List[DailyResult] = []
        self.weekly_reports: List[WeeklyReport] = []
        self.current_week_start = self._get_week_start()
        
        # 加载历史数据
        self.load_data()
        
        logger.info("🏆 AI 竞争追踪器 v1.0 已初始化")
        logger.info(f"  竞赛模式：独立竞争")
        logger.info(f"  参赛方：太一 (OpenClaw) vs Hermes")
        logger.info(f"  共同账户资金:")
        logger.info(f"    现货：${self.config.spot_balance}")
        logger.info(f"    杠杆：${self.config.margin_balance}")
        logger.info(f"    合约：${self.config.futures_balance}")
        logger.info(f"    总计：${self.config.total_balance}")
        logger.info(f"  竞赛周期：{self.config.competition_days} 天")
        logger.info(f"  测评日：{self.config.evaluation_day}")
        logger.info(f"  Hermes 状态：独立运行 (不管理)")
    
    def _get_week_start(self) -> str:
        """获取本周开始日期"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        return week_start.strftime("%Y-%m-%d")
    
    def record_daily_result(self, agent: str, spot_pnl: float = 0.0,
                           margin_pnl: float = 0.0, futures_pnl: float = 0.0,
                           trades_count: int = 0, win_rate: float = 0.0) -> DailyResult:
        """记录每日交易结果 (太一/Hermes 共同账户，独立统计盈亏)"""
        total_pnl = spot_pnl + margin_pnl + futures_pnl
        
        result = DailyResult(
            date=datetime.now().strftime("%Y-%m-%d"),
            agent=agent,
            spot_pnl=spot_pnl,
            margin_pnl=margin_pnl,
            futures_pnl=futures_pnl,
            total_pnl=total_pnl,
            trades_count=trades_count,
            win_rate=win_rate,
        )
        
        self.daily_results.append(result)
        logger.info(f"📊 记录 {agent} 每日结果：总盈亏=${total_pnl:.2f} (现货${spot_pnl:.2f} + 杠杆${margin_pnl:.2f} + 合约${futures_pnl:.2f})")
        
        # 保存数据
        self.save_data()
        
        return result
    
    def sync_hermes_result(self, hermes_result: Dict):
        """同步 Hermes 结果 (Hermes 自主上报)"""
        logger.info(f"📡 接收 Hermes 上报结果")
        
        result = DailyResult(
            date=hermes_result.get('date', datetime.now().strftime("%Y-%m-%d")),
            agent='hermes',
            spot_pnl=hermes_result.get('spot_pnl', 0.0),
            margin_pnl=hermes_result.get('margin_pnl', 0.0),
            futures_pnl=hermes_result.get('futures_pnl', 0.0),
            total_pnl=hermes_result.get('total_pnl', 0.0),
            trades_count=hermes_result.get('trades_count', 0),
            win_rate=hermes_result.get('win_rate', 0.0),
        )
        
        self.daily_results.append(result)
        logger.info(f"✅ Hermes 结果已同步：总盈亏=${result.total_pnl:.2f}")
        
        self.save_data()
        return result
    
    def generate_weekly_report(self) -> WeeklyReport:
        """生成每周测评报告"""
        logger.info("\n📈 生成每周测评报告...")
        
        # 筛选本周数据
        week_results = [r for r in self.daily_results 
                       if r.date >= self.current_week_start]
        
        # 分离太一和 Hermes 的结果
        taiyi_results = [r for r in week_results if r.agent == 'taiyi']
        hermes_results = [r for r in week_results if r.agent == 'hermes']
        
        # 计算总盈亏 (现货 + 杠杆 + 合约)
        taiyi_total_pnl = sum(r.total_pnl for r in taiyi_results)
        hermes_total_pnl = sum(r.total_pnl for r in hermes_results)
        
        # 计算获胜天数
        taiyi_win_days = 0
        hermes_win_days = 0
        
        # 按日期配对比较
        taiyi_by_date = {r.date: r for r in taiyi_results}
        hermes_by_date = {r.date: r for r in hermes_results}
        
        for date in set(list(taiyi_by_date.keys()) + list(hermes_by_date.keys())):
            taiyi_pnl = taiyi_by_date.get(date, DailyResult(date, 'taiyi')).total_pnl
            hermes_pnl = hermes_by_date.get(date, DailyResult(date, 'hermes')).total_pnl
            
            if taiyi_pnl > hermes_pnl:
                taiyi_win_days += 1
            elif hermes_pnl > taiyi_pnl:
                hermes_win_days += 1
        
        # 确定获胜者
        if taiyi_total_pnl > hermes_total_pnl:
            winner = 'taiyi'
            prize = '算力配置自主权 + 系统升级优先权'
        elif hermes_total_pnl > taiyi_total_pnl:
            winner = 'hermes'
            prize = '算力配置自主权 + 系统升级优先权'
        else:
            winner = 'tie'
            prize = '共享算力配置权'
        
        week_end = datetime.now().strftime("%Y-%m-%d")
        
        report = WeeklyReport(
            week_start=self.current_week_start,
            week_end=week_end,
            taiyi_total_pnl=taiyi_total_pnl,
            hermes_total_pnl=hermes_total_pnl,
            taiyi_win_days=taiyi_win_days,
            hermes_win_days=hermes_win_days,
            winner=winner,
            prize=prize,
        )
        
        self.weekly_reports.append(report)
        
        # 打印报告
        self._print_weekly_report(report)
        
        # 如果产生获胜者，执行奖励
        if winner != 'tie':
            self._award_prize(winner, prize)
        
        # 重置下周
        self.current_week_start = self._get_week_start()
        
        # 保存数据
        self.save_data()
        
        return report
    
    def _print_weekly_report(self, report: WeeklyReport):
        """打印每周报告"""
        print("\n" + "=" * 70)
        print("🏆 AI 交易系统竞争 - 每周测评报告")
        print("=" * 70)
        print(f"竞赛周期：{report.week_start} 至 {report.week_end}")
        print(f"共同账户：现货${100} + 杠杆${20} + 合约${20} = 总计${140}")
        print()
        print("📊 盈亏对比 (现货 + 杠杆 + 合约):")
        print(f"  太一 (OpenClaw):  ${report.taiyi_total_pnl:>10.2f}")
        print(f"  Hermes:          ${report.hermes_total_pnl:>10.2f}")
        print()
        print("📈 获胜天数:")
        print(f"  太一：{report.taiyi_win_days} 天")
        print(f"  Hermes: {report.hermes_win_days} 天")
        print()
        print("🏅 获胜者:")
        if report.winner == 'taiyi':
            print(f"  🎉 太一 (OpenClaw) 获胜！")
        elif report.winner == 'hermes':
            print(f"  🎉 Hermes 获胜！")
        else:
            print(f"  🤝 平局！")
        print()
        print(f"🎁 奖励：{report.prize}")
        print("=" * 70)
    
    def _award_prize(self, winner: str, prize: str):
        """执行奖励"""
        logger.info(f"🎁 执行奖励：{winner} 获得 {prize}")
        
        # 记录奖励
        award_record = {
            'date': datetime.now().isoformat(),
            'winner': winner,
            'prize': prize,
            'status': 'pending',
        }
        
        # 保存奖励记录
        award_file = DATA_DIR / "awards.json"
        awards = []
        if award_file.exists():
            with open(award_file, 'r', encoding='utf-8') as f:
                awards = json.load(f)
        awards.append(award_record)
        
        with open(award_file, 'w', encoding='utf-8') as f:
            json.dump(awards, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 奖励记录已保存")
    
    def check_compute_purchase(self, agent: str, compute_type: str, 
                               cost: float) -> bool:
        """检查算力购买"""
        logger.info(f"💻 {agent} 申请购买算力：{compute_type} (${cost})")
        
        # 检查是否是获胜者
        award_file = DATA_DIR / "awards.json"
        if not award_file.exists():
            logger.warning("⚠️ 无奖励记录，无法购买")
            return False
        
        with open(award_file, 'r', encoding='utf-8') as f:
            awards = json.load(f)
        
        # 检查最新奖励
        if not awards:
            logger.warning("⚠️ 无有效奖励")
            return False
        
        latest_award = awards[-1]
        if latest_award['winner'] != agent:
            logger.warning(f"⚠️ {agent} 不是获胜者，无权购买")
            return False
        
        if latest_award['status'] == 'used':
            logger.warning(f"⚠️ 奖励已使用")
            return False
        
        # 批准购买
        logger.info(f"✅ 批准 {agent} 购买 {compute_type}")
        latest_award['status'] = 'used'
        latest_award['purchase'] = {
            'type': compute_type,
            'cost': cost,
            'date': datetime.now().isoformat(),
        }
        
        with open(award_file, 'w', encoding='utf-8') as f:
            json.dump(awards, f, indent=2, ensure_ascii=False)
        
        return True
    
    def save_data(self):
        """保存数据"""
        # 保存每日结果
        daily_file = DATA_DIR / "daily_results.json"
        with open(daily_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(r) for r in self.daily_results], 
                     f, indent=2, ensure_ascii=False)
        
        # 保存每周报告
        weekly_file = DATA_DIR / "weekly_reports.json"
        with open(weekly_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(r) for r in self.weekly_reports], 
                     f, indent=2, ensure_ascii=False)
        
        # 保存配置
        config_file = DATA_DIR / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.config), f, indent=2, ensure_ascii=False)
        
        logger.debug("💾 数据已保存")
    
    def load_data(self):
        """加载数据"""
        # 加载每日结果
        daily_file = DATA_DIR / "daily_results.json"
        if daily_file.exists():
            with open(daily_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.daily_results = [DailyResult(**r) for r in data]
        
        # 加载每周报告
        weekly_file = DATA_DIR / "weekly_reports.json"
        if weekly_file.exists():
            with open(weekly_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.weekly_reports = [WeeklyReport(**r) for r in data]
        
        # 加载配置
        config_file = DATA_DIR / "config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.config = CompetitionConfig(**data)
        
        logger.debug("📂 数据已加载")
    
    def get_standings(self) -> Dict:
        """获取当前排名"""
        week_results = [r for r in self.daily_results 
                       if r.date >= self.current_week_start]
        
        taiyi_results = [r for r in week_results if r.agent == 'taiyi']
        hermes_results = [r for r in week_results if r.agent == 'hermes']
        
        taiyi_pnl = sum(r.total_pnl for r in taiyi_results)
        hermes_pnl = sum(r.total_pnl for r in hermes_results)
        
        return {
            'week_start': self.current_week_start,
            'account_info': {
                'spot': self.config.spot_balance,
                'margin': self.config.margin_balance,
                'futures': self.config.futures_balance,
                'total': self.config.total_balance,
            },
            'taiyi': {
                'pnl': taiyi_pnl,
                'trades': sum(r.trades_count for r in taiyi_results),
                'win_rate': sum(r.win_rate for r in taiyi_results) / max(1, len(taiyi_results)),
            },
            'hermes': {
                'pnl': hermes_pnl,
                'trades': sum(r.trades_count for r in hermes_results),
                'win_rate': sum(r.win_rate for r in hermes_results) / max(1, len(hermes_results)),
            },
            'leader': 'taiyi' if taiyi_pnl > hermes_pnl else 'hermes' if hermes_pnl > taiyi_pnl else 'tie',
        }


def main():
    """主函数"""
    tracker = AICompetitionTracker()
    
    logger.info("=" * 70)
    logger.info("🏆 AI 交易系统竞争追踪器")
    logger.info("=" * 70)
    
    # 获取当前排名
    standings = tracker.get_standings()
    
    logger.info(f"📊 当前排名 ({standings['week_start']}):")
    logger.info(f"  太一：PnL=${standings['taiyi']['pnl']:.2f}, 交易{standings['taiyi']['trades']}笔")
    logger.info(f"  Hermes: PnL=${standings['hermes']['pnl']:.2f}, 交易{standings['hermes']['trades']}笔")
    logger.info(f"  领先者：{standings['leader']}")
    
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
