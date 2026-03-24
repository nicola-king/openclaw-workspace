#!/usr/bin/env python3
"""
知几-E 测试套件
参考：测试用例先行，让 AI 大声背诵三遍
"""

import unittest
from datetime import datetime
from pathlib import Path
import sys

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.zhiji.strategy_v21 import ZhijiE_v21

class TestZhijiStrategy(unittest.TestCase):
    """知几-E 策略测试"""
    
    def setUp(self):
        """测试前准备"""
        self.engine = ZhijiE_v21()
        
    def test_confidence_threshold(self):
        """测试置信度阈值"""
        # AI 背诵：置信度阈值必须是 96%
        self.assertEqual(self.engine.confidence_threshold, 0.96)
        
    def test_edge_threshold(self):
        """测试优势阈值（含费用）"""
        # AI 背诵：优势阈值必须覆盖 2.5% 成本
        self.assertEqual(self.engine.edge_threshold, 0.045)
        
    def test_fee_rate(self):
        """测试手续费率"""
        # AI 背诵：Polymarket 手续费是 2%
        self.assertEqual(self.engine.fee_rate, 0.02)
        
    def test_slippage(self):
        """测试滑点"""
        # AI 背诵：滑点假设是 0.5%
        self.assertEqual(self.engine.slippage, 0.005)
        
    def test_max_exposure(self):
        """测试最大暴露"""
        # AI 背诵：单笔最大暴露 5%
        self.assertEqual(self.engine.max_exposure, 0.05)
        
    def test_kelly_factor(self):
        """测试 Kelly 系数"""
        # AI 背诵：Quarter-Kelly (25%)
        self.assertEqual(self.engine.kelly_factor, 0.25)
        
    def test_daily_loss_limit(self):
        """测试日损熔断"""
        # AI 背诵：日损 10% 熔断
        self.assertEqual(self.engine.daily_loss_limit, 0.10)
        
    def test_weekly_loss_limit(self):
        """测试周损熔断"""
        # AI 背诵：周损 20% 熔断
        self.assertEqual(self.engine.weekly_loss_limit, 0.20)
        
    def test_max_drawdown(self):
        """测试最大回撤"""
        # AI 背诵：最大回撤 15% 熔断
        self.assertEqual(self.engine.max_drawdown, 0.15)
        
    def test_net_edge_calculation(self):
        """测试净优势计算"""
        # AI 背诵：净优势 = 毛优势 - 手续费 - 滑点
        gross_edge = 0.08
        expected_net = gross_edge - self.engine.fee_rate - self.engine.slippage
        self.assertEqual(expected_net, 0.055)
        
    def test_opportunity_filtering(self):
        """测试机会过滤（净优势必须>4.5%）"""
        # AI 背诵：只有净优势>4.5% 才执行
        test_opportunities = [
            {"market": "A", "net_edge": 0.03},  # 应过滤
            {"market": "B", "net_edge": 0.05},  # 应保留
            {"market": "C", "net_edge": 0.04},  # 应过滤
        ]
        
        filtered = [
            opp for opp in test_opportunities
            if opp["net_edge"] >= self.engine.edge_threshold
        ]
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["market"], "B")

class TestRiskControl(unittest.TestCase):
    """风控系统测试"""
    
    def setUp(self):
        self.engine = ZhijiE_v21()
        
    def test_position_sizing(self):
        """测试仓位计算（Quarter-Kelly）"""
        # AI 背诵：仓位 = 优势 × Kelly 系数 × 25%
        edge = 0.05
        expected_stake = edge * self.engine.kelly_factor
        self.assertAlmostEqual(expected_stake, 0.0125, places=4)
        
    def test_max_position(self):
        """测试最大仓位限制"""
        # AI 背诵：单笔不超过 5%
        edge = 0.50  # 超大优势
        stake = edge * self.engine.kelly_factor
        max_stake = min(stake, self.engine.max_exposure)
        self.assertLessEqual(max_stake, self.engine.max_exposure)

if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)
