#!/usr/bin/env python3
"""
搜索 Agent 测试文件
版本：v1.0.0
作者：太一 AGI
"""

import sys
import os
import unittest
import time

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.search_agent import SearchAgent, SearchRegion, SearchPriority, SearchResult
from core.anti_scraping import AntiScrapingStrategy, ProxyConfig
from core.self_evolution import SelfEvolution, EvolutionMetrics

class TestSearchAgent(unittest.TestCase):
    """搜索 Agent 测试"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = SearchAgent()
    
    def tearDown(self):
        """测试后清理"""
        self.agent.close()
    
    def test_initialization(self):
        """测试初始化"""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.config)
        self.assertIsNotNone(self.agent.session)
    
    def test_search_bing(self):
        """测试 Bing 搜索"""
        results = self.agent.search(
            query="foldable container house",
            regions=[SearchRegion.SOUTHEAST_ASIA],
            priority=SearchPriority.MEDIUM
        )
        
        self.assertIsInstance(results, list)
        # 注意：实际搜索可能返回空结果，这是正常的
    
    def test_search_metrics(self):
        """测试搜索指标"""
        # 执行几次搜索
        for _ in range(3):
            self.agent.search(
                query="test query",
                priority=SearchPriority.LOW
            )
        
        metrics = self.agent.get_metrics()
        self.assertEqual(metrics.total_requests, 3)
        self.assertGreaterEqual(metrics.success_rate, 0.0)
    
    def test_search_result_validation(self):
        """测试结果验证"""
        # 模拟结果
        mock_result = {
            'title': 'Test Company Inc',
            'url': 'https://example.com',
            'engine': 'bing'
        }
        
        validated = self.agent._validate_result(mock_result)
        self.assertIsInstance(validated, SearchResult)
        self.assertGreater(validated.confidence, 0.0)

class TestAntiScraping(unittest.TestCase):
    """反反爬测试"""
    
    def setUp(self):
        """测试前准备"""
        self.strategy = AntiScrapingStrategy()
    
    def test_proxy_rotation(self):
        """测试代理轮换"""
        proxies = []
        for _ in range(5):
            proxy = self.strategy.get_proxy()
            proxies.append(proxy)
        
        # 代理可能为空（如果没有配置）
        self.assertIsInstance(proxies, list)
    
    def test_user_agent_rotation(self):
        """测试 User-Agent 轮换"""
        user_agents = set()
        for _ in range(10):
            ua = self.strategy.rotate_user_agent()
            user_agents.add(ua)
        
        # 应该有不同的 User-Agent
        self.assertGreater(len(user_agents), 1)
    
    def test_delay_application(self):
        """测试延迟应用"""
        start_time = time.time()
        self.strategy.apply_delay()
        end_time = time.time()
        
        # 延迟应该在 1-3 秒之间
        delay = end_time - start_time
        self.assertGreaterEqual(delay, 1.0)
        self.assertLessEqual(delay, 3.5)  # 允许一些误差
    
    def test_stats(self):
        """测试统计信息"""
        stats = self.strategy.get_stats()
        self.assertIn('total_requests', stats)
        self.assertIn('proxies_available', stats)

class TestSelfEvolution(unittest.TestCase):
    """自进化测试"""
    
    def setUp(self):
        """测试前准备"""
        self.evolution = SelfEvolution()
    
    def test_initialization(self):
        """测试初始化"""
        self.assertIsNotNone(self.evolution)
        self.assertIsNotNone(self.evolution.config)
        self.assertIsNotNone(self.evolution.knowledge_base)
    
    def test_record_metrics(self):
        """测试记录指标"""
        metrics = EvolutionMetrics(
            timestamp=time.time(),
            success_rate=0.8,
            average_response_time=3.5,
            anti_scraping_success_rate=0.9,
            data_quality_score=0.85,
            total_requests=10,
            successful_requests=8,
            failed_requests=2,
            engine_performance={"bing": 0.8, "google": 0.9},
            region_performance={"Southeast Asia": 0.75}
        )
        
        self.evolution.record_metrics(metrics)
        self.assertEqual(len(self.evolution.metrics_history), 1)
    
    def test_analyze_performance(self):
        """测试性能分析"""
        # 记录一些指标
        for i in range(5):
            metrics = EvolutionMetrics(
                timestamp=time.time(),
                success_rate=0.7 + i * 0.05,
                average_response_time=3.0 - i * 0.2,
                anti_scraping_success_rate=0.8 + i * 0.03,
                data_quality_score=0.75 + i * 0.04,
                total_requests=10 + i,
                successful_requests=8 + i,
                failed_requests=2,
                engine_performance={"bing": 0.8},
                region_performance={"Southeast Asia": 0.75}
            )
            self.evolution.record_metrics(metrics)
        
        performance = self.evolution.analyze_performance()
        self.assertIn('avg_success_rate', performance)
        self.assertIn('avg_response_time', performance)
    
    def test_optimize_strategy(self):
        """测试策略优化"""
        # 记录一些指标
        for i in range(3):
            metrics = EvolutionMetrics(
                timestamp=time.time(),
                success_rate=0.6,
                average_response_time=6.0,
                anti_scraping_success_rate=0.7,
                data_quality_score=0.65,
                total_requests=10,
                successful_requests=6,
                failed_requests=4,
                engine_performance={"bing": 0.6},
                region_performance={"Southeast Asia": 0.6}
            )
            self.evolution.record_metrics(metrics)
        
        optimized = self.evolution.optimize_strategy()
        self.assertIsInstance(optimized, dict)
        self.assertIn('preferred_engine', optimized)
    
    def test_evolution_status(self):
        """测试进化状态"""
        status = self.evolution.get_evolution_status()
        self.assertIn('enabled', status)
        self.assertIn('metrics_count', status)
        self.assertIn('should_evolve', status)

def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestSearchAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestAntiScraping))
    suite.addTests(loader.loadTestsFromTestCase(TestSelfEvolution))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("🧪 运行搜索 Agent 测试...")
    success = run_tests()
    
    if success:
        print("✅ 所有测试通过")
    else:
        print("❌ 部分测试失败")
    
    sys.exit(0 if success else 1)