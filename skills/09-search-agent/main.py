#!/usr/bin/env python3
"""
智能搜索 Agent - 主入口 (综合搜索方案 v2.0)
作者：太一 AGI
"""

import sys
import os
import argparse
import json
import logging
from typing import List

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

from core.search_agent import SearchAgent, SearchRegion, SearchPriority
from core.anti_scraping import AntiScrapingStrategy
from core.self_evolution import SelfEvolution
from modules.comprehensive_search import ComprehensiveSearch

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/search_agent.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='智能搜索 Agent - 综合搜索方案 v2.0')
    
    parser.add_argument('--query', '-q', type=str, help='搜索查询')
    parser.add_argument('--regions', '-r', type=str, nargs='+', help='目标区域')
    parser.add_argument('--priority', '-p', type=str, choices=['high', 'medium', 'low'], 
                       default='medium', help='搜索优先级')
    parser.add_argument('--engine', '-e', type=str, choices=['bing', 'google', 'duckduckgo', 'baidu', 'comprehensive'],
                       help='搜索引擎')
    parser.add_argument('--output', '-o', type=str, default='results.json', help='输出文件')
    parser.add_argument('--evolve', action='store_true', help='执行进化')
    parser.add_argument('--test', action='store_true', help='运行测试')
    parser.add_argument('--status', action='store_true', help='显示状态')
    parser.add_argument('--comprehensive', action='store_true', help='使用综合搜索方案')
    parser.add_argument('--proxy-config', type=str, default='config/proxy_config.json', help='代理配置文件路径')
    
    return parser.parse_args()

def get_region_enum(region_str: str) -> SearchRegion:
    """获取区域枚举"""
    region_map = {
        'Southeast Asia': SearchRegion.SOUTHEAST_ASIA,
        'Middle East': SearchRegion.MIDDLE_EAST,
        'Eastern Europe': SearchRegion.EASTERN_EUROPE,
        'Ukraine': SearchRegion.UKRAINE,
        'Europe': SearchRegion.EUROPE,
        'UK/USA': SearchRegion.UK_USA,
        'Australia': SearchRegion.AUSTRALIA
    }
    
    return region_map.get(region_str, SearchRegion.SOUTHEAST_ASIA)

def load_proxy_config(proxy_config_path: str) -> dict:
    """加载代理配置"""
    try:
        with open(proxy_config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"代理配置文件未找到: {proxy_config_path}")
        return {}

def run_comprehensive_search(query: str, regions: List[str], proxy_config: dict) -> list:
    """运行综合搜索"""
    logger.info(f"🔍 开始综合搜索: {query}")
    
    searcher = ComprehensiveSearch(proxy_config)
    results = searcher.search(query, regions)
    searcher.close()
    
    return results

def run_search(agent: SearchAgent, query: str, regions: List[str], 
               priority: str, engine: str = None) -> list:
    """运行搜索"""
    logger.info(f"🔍 开始搜索: {query}")
    
    # 转换区域
    region_enums = [get_region_enum(r) for r in regions] if regions else [SearchRegion.SOUTHEAST_ASIA]
    
    # 转换优先级
    priority_map = {
        'high': SearchPriority.HIGH,
        'medium': SearchPriority.MEDIUM,
        'low': SearchPriority.LOW
    }
    priority_enum = priority_map.get(priority, SearchPriority.MEDIUM)
    
    # 执行搜索
    results = agent.search(query, region_enums, priority_enum)
    
    return results

def save_results(results: list, output_file: str):
    """保存结果"""
    # 转换结果为可序列化格式
    serializable_results = []
    for result in results:
        serializable_results.append({
            'company_name': result.company_name if hasattr(result, 'company_name') else result.name,
            'website': result.website if hasattr(result, 'website') else result.url,
            'email': getattr(result, 'email', ''),
            'phone': getattr(result, 'phone', ''),
            'address': getattr(result, 'address', ''),
            'region': getattr(result, 'region', ''),
            'industry': getattr(result, 'industry', ''),
            'confidence': result.confidence,
            'source': result.source,
            'timestamp': result.timestamp,
            'description': getattr(result, 'description', '')
        })
    
    # 保存
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"💾 结果已保存到: {output_file}")

def show_status(agent: SearchAgent, evolution: SelfEvolution):
    """显示状态"""
    metrics = agent.get_metrics()
    evolution_status = evolution.get_evolution_status()
    
    print("\n" + "="*50)
    print("🔍 智能搜索 Agent 状态")
    print("="*50)
    print(f"📊 搜索指标:")
    print(f"  - 总请求: {metrics.total_requests}")
    print(f"  - 成功: {metrics.successful_requests}")
    print(f"  - 失败: {metrics.failed_requests}")
    print(f"  - 成功率: {metrics.success_rate:.2%}")
    print(f"  - 平均响应时间: {metrics.average_response_time:.2f}秒")
    print()
    print(f"🧬 进化状态:")
    print(f"  - 启用: {evolution_status['enabled']}")
    print(f"  - 指标数量: {evolution_status['metrics_count']}")
    print(f"  - 需要进化: {evolution_status['should_evolve']}")
    print("="*50)

def main():
    """主函数"""
    args = parse_args()
    
    # 创建组件
    agent = SearchAgent()
    evolution = SelfEvolution()
    
    # 加载代理配置
    proxy_config = load_proxy_config(args.proxy_config)
    
    try:
        if args.test:
            # 运行测试
            logger.info("🧪 运行测试...")
            from tests.test_search_agent import run_tests
            success = run_tests()
            sys.exit(0 if success else 1)
        
        elif args.status:
            # 显示状态
            show_status(agent, evolution)
        
        elif args.evolve:
            # 执行进化
            logger.info("🧬 执行进化...")
            result = evolution.evolve()
            print(f"进化结果: {result}")
        
        elif args.query:
            # 执行搜索
            if args.comprehensive:
                # 综合搜索方案
                results = run_comprehensive_search(args.query, args.regions, proxy_config)
            else:
                # 传统搜索
                results = run_search(agent, args.query, args.regions, args.priority, args.engine)
            
            # 保存结果
            if results:
                save_results(results, args.output)
                print(f"\n找到 {len(results)} 条结果")
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result.company_name if hasattr(result, 'company_name') else result.name}")
                    print(f"   网站: {result.website if hasattr(result, 'website') else result.url}")
                    print(f"   置信度: {result.confidence:.2%}")
                    print()
            else:
                print("未找到结果")
        
        else:
            # 显示帮助
            print("智能搜索 Agent v2.0.0 - 综合搜索方案")
            print("使用 --help 查看帮助")
    
    finally:
        agent.close()

if __name__ == "__main__":
    main()
