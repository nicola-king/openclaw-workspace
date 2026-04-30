#!/usr/bin/env python3
"""
自进化模块
版本：v1.0.0
作者：太一 AGI
"""

import json
import time
import logging
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class EvolutionMetrics:
    """进化指标"""
    timestamp: float
    success_rate: float
    average_response_time: float
    anti_scraping_success_rate: float
    data_quality_score: float
    total_requests: int
    successful_requests: int
    failed_requests: int
    engine_performance: Dict[str, float]
    region_performance: Dict[str, float]

@dataclass
class KnowledgeBase:
    """知识库"""
    successful_strategies: List[dict]
    failed_strategies: List[dict]
    optimal_parameters: Dict[str, any]
    last_update: float

class SelfEvolution:
    """自进化系统"""
    
    def __init__(self, config_path: str = "config/evolution_config.json"):
        """初始化自进化系统"""
        self.config_path = config_path
        self.config = self._load_config()
        self.metrics_history = []
        self.knowledge_base = self._load_knowledge_base()
        
        logger.info("🧬 自进化系统初始化完成")
    
    def _load_config(self) -> dict:
        """加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """获取默认配置"""
        return {
            "evolution": {
                "enabled": True,
                "update_interval": 3600,
                "min_samples": 10,
                "learning_rate": 0.1,
                "exploration_rate": 0.1
            },
            "metrics": {
                "success_rate_threshold": 0.7,
                "response_time_threshold": 5.0,
                "quality_threshold": 0.8
            }
        }
    
    def _load_knowledge_base(self) -> KnowledgeBase:
        """加载知识库"""
        kb_path = "data/knowledge_base.json"
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return KnowledgeBase(**data)
        except FileNotFoundError:
            return KnowledgeBase(
                successful_strategies=[],
                failed_strategies=[],
                optimal_parameters={},
                last_update=time.time()
            )
    
    def record_metrics(self, metrics: EvolutionMetrics):
        """记录指标"""
        self.metrics_history.append(metrics)
        
        # 保留最近 100 条记录
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        logger.info(f"📊 记录指标: 成功率={metrics.success_rate:.2%}")
    
    def analyze_performance(self) -> Dict[str, float]:
        """分析性能"""
        if not self.metrics_history:
            return {}
        
        # 计算平均指标
        avg_success_rate = sum(m.success_rate for m in self.metrics_history) / len(self.metrics_history)
        avg_response_time = sum(m.average_response_time for m in self.metrics_history) / len(self.metrics_history)
        avg_quality = sum(m.data_quality_score for m in self.metrics_history) / len(self.metrics_history)
        
        return {
            "avg_success_rate": avg_success_rate,
            "avg_response_time": avg_response_time,
            "avg_quality": avg_quality,
            "total_samples": len(self.metrics_history)
        }
    
    def optimize_strategy(self) -> Dict[str, any]:
        """优化策略"""
        performance = self.analyze_performance()
        
        if not performance:
            return {}
        
        optimized = {}
        
        # 优化搜索引擎选择
        if performance["avg_success_rate"] < 0.7:
            optimized["preferred_engine"] = "google"  # 切换到高质量引擎
            optimized["retry_count"] = 3
        else:
            optimized["preferred_engine"] = "bing"
            optimized["retry_count"] = 2
        
        # 优化代理策略
        if performance["avg_response_time"] > 5.0:
            optimized["proxy_rotation"] = True
            optimized["delay_range"] = [0.5, 1.5]
        else:
            optimized["proxy_rotation"] = False
            optimized["delay_range"] = [1, 3]
        
        # 优化数据提取
        if performance["avg_quality"] < 0.8:
            optimized["validation_threshold"] = 0.5
            optimized["confidence_weight"] = 0.7
        else:
            optimized["validation_threshold"] = 0.3
            optimized["confidence_weight"] = 0.5
        
        logger.info(f"🔧 策略优化完成: {optimized}")
        return optimized
    
    def update_knowledge_base(self):
        """更新知识库"""
        performance = self.analyze_performance()
        
        if not performance:
            return
        
        # 更新最优参数
        self.knowledge_base.optimal_parameters = self.optimize_strategy()
        self.knowledge_base.last_update = time.time()
        
        # 保存知识库
        self._save_knowledge_base()
        
        logger.info("📚 知识库更新完成")
    
    def _save_knowledge_base(self):
        """保存知识库"""
        kb_path = "data/knowledge_base.json"
        os.makedirs(os.path.dirname(kb_path), exist_ok=True)
        
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.knowledge_base), f, indent=2, ensure_ascii=False)
    
    def learn_from_success(self, strategy: dict, result: dict):
        """从成功中学习"""
        self.knowledge_base.successful_strategies.append({
            "strategy": strategy,
            "result": result,
            "timestamp": time.time()
        })
        
        # 限制历史记录
        if len(self.knowledge_base.successful_strategies) > 50:
            self.knowledge_base.successful_strategies = self.knowledge_base.successful_strategies[-50:]
    
    def learn_from_failure(self, strategy: dict, error: str):
        """从失败中学习"""
        self.knowledge_base.failed_strategies.append({
            "strategy": strategy,
            "error": error,
            "timestamp": time.time()
        })
        
        # 限制历史记录
        if len(self.knowledge_base.failed_strategies) > 50:
            self.knowledge_base.failed_strategies = self.knowledge_base.failed_strategies[-50:]
    
    def should_evolve(self) -> bool:
        """判断是否需要进化"""
        if not self.config.get("evolution", {}).get("enabled", True):
            return False
        
        # 检查时间间隔
        last_update = self.knowledge_base.last_update
        interval = self.config.get("evolution", {}).get("update_interval", 3600)
        
        return (time.time() - last_update) >= interval
    
    def evolve(self) -> Dict[str, any]:
        """执行进化"""
        if not self.should_evolve():
            logger.info("⏭️ 暂不需要进化")
            return {}
        
        logger.info("🧬 开始进化...")
        
        # 分析性能
        performance = self.analyze_performance()
        
        # 优化策略
        optimized = self.optimize_strategy()
        
        # 更新知识库
        self.update_knowledge_base()
        
        # 保存进化记录
        evolution_record = {
            "timestamp": time.time(),
            "performance": performance,
            "optimized": optimized,
            "metrics_count": len(self.metrics_history)
        }
        
        self._save_evolution_record(evolution_record)
        
        logger.info("✅ 进化完成")
        return evolution_record
    
    def _save_evolution_record(self, record: dict):
        """保存进化记录"""
        record_path = "data/evolution_records.json"
        os.makedirs(os.path.dirname(record_path), exist_ok=True)
        
        # 加载现有记录
        try:
            with open(record_path, 'r', encoding='utf-8') as f:
                records = json.load(f)
        except FileNotFoundError:
            records = []
        
        # 添加新记录
        records.append(record)
        
        # 保留最近 100 条
        if len(records) > 100:
            records = records[-100:]
        
        # 保存
        with open(record_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    
    def get_evolution_status(self) -> dict:
        """获取进化状态"""
        performance = self.analyze_performance()
        
        return {
            "enabled": self.config.get("evolution", {}).get("enabled", True),
            "last_update": self.knowledge_base.last_update,
            "metrics_count": len(self.metrics_history),
            "performance": performance,
            "optimal_parameters": self.knowledge_base.optimal_parameters,
            "should_evolve": self.should_evolve()
        }

if __name__ == "__main__":
    # 测试代码
    evolution = SelfEvolution()
    
    # 模拟记录指标
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
            engine_performance={"bing": 0.8, "google": 0.9},
            region_performance={"Southeast Asia": 0.75, "Middle East": 0.8}
        )
        evolution.record_metrics(metrics)
    
    # 分析性能
    performance = evolution.analyze_performance()
    print(f"性能分析: {performance}")
    
    # 优化策略
    optimized = evolution.optimize_strategy()
    print(f"优化策略: {optimized}")
    
    # 获取状态
    status = evolution.get_evolution_status()
    print(f"进化状态: {status}")