#!/usr/bin/env python3
"""
API 监控面板 - 实时监控 API 健康、限流、状态
执行：python scripts/api-monitor.py
Dashboard: python scripts/api-dashboard.py --port 8080
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path

# 配置
API_CONFIG = {
    'coingecko': {
        'name': 'CoinGecko',
        'base_url': 'https://api.coingecko.com/api/v3',
        'health_endpoint': '/simple/price?ids=bitcoin&vs_currencies=usd',
        'rate_limit': 60,  # 每分钟
        'cache_ttl': 300,  # 5 分钟
        'category': 'Cryptocurrency',
        'backup': ['coincap', 'binance']
    },
    'newsapi': {
        'name': 'NewsAPI',
        'base_url': 'https://newsapi.org/v2',
        'health_endpoint': '/top-headlines?country=us&apiKey={API_KEY}',
        'rate_limit': 100,  # 每天
        'cache_ttl': 1800,  # 30 分钟
        'category': 'News',
        'backup': ['guardian', 'currents']
    },
    'open-meteo': {
        'name': 'Open-Meteo',
        'base_url': 'https://api.open-meteo.com/v1',
        'health_endpoint': '/forecast?latitude=31.23&longitude=121.47&current_weather=true',
        'rate_limit': 99999,  # 无限
        'cache_ttl': 900,  # 15 分钟
        'category': 'Weather',
        'backup': ['wttr']
    },
    'alpha-vantage': {
        'name': 'Alpha Vantage',
        'base_url': 'https://www.alphavantage.co/query',
        'health_endpoint': '?function=GLOBAL_QUOTE&symbol=IBM&apikey={API_KEY}',
        'rate_limit': 5,  # 每分钟
        'cache_ttl': 600,  # 10 分钟
        'category': 'Finance',
        'backup': ['yahoo', 'iex']
    },
    'unsplash': {
        'name': 'Unsplash',
        'base_url': 'https://api.unsplash.com',
        'health_endpoint': '/photos/random?client_id={API_KEY}&count=1',
        'rate_limit': 50,  # 每小时
        'cache_ttl': 3600,  # 1 小时
        'category': 'Images',
        'backup': ['pexels', 'pixabay']
    }
}

# 文件路径
RATE_LIMIT_FILE = Path('/tmp/api-rate-limits.json')
CACHE_DIR = Path('/tmp/api-cache')
LOG_FILE = Path('/tmp/api-monitor.log')

def load_rate_limits():
    """加载限流状态"""
    if RATE_LIMIT_FILE.exists():
        with open(RATE_LIMIT_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_rate_limits(limits):
    """保存限流状态"""
    with open(RATE_LIMIT_FILE, 'w') as f:
        json.dump(limits, f, indent=2, default=str)

def check_health(api_id):
    """检查 API 健康状态"""
    config = API_CONFIG[api_id]
    api_key = os.getenv(f"{api_id.replace('-', '_').upper()}_API_KEY", "")
    
    url = config['base_url'] + config['health_endpoint']
    if '{API_KEY}' in url:
        url = url.replace('{API_KEY}', api_key)
    
    start_time = time.time()
    try:
        response = requests.get(url, timeout=10)
        response_time = (time.time() - start_time) * 1000  # ms
        
        if response.status_code == 200:
            return {
                'status': '✅',
                'response_time': f"{response_time:.0f}ms",
                'status_code': response.status_code
            }
        elif response.status_code == 429:
            return {
                'status': '⚠️',
                'response_time': f"{response_time:.0f}ms",
                'status_code': response.status_code,
                'error': 'Rate Limit'
            }
        else:
            return {
                'status': '❌',
                'response_time': f"{response_time:.0f}ms",
                'status_code': response.status_code
            }
    except Exception as e:
        return {
            'status': '❌',
            'response_time': 'Timeout',
            'error': str(e)
        }

def get_rate_limit_status(api_id):
    """获取限流状态"""
    limits = load_rate_limits()
    config = API_CONFIG[api_id]
    
    if api_id not in limits:
        return {
            'used': 0,
            'limit': config['rate_limit'],
            'remaining': config['rate_limit'],
            'percentage': 0
        }
    
    limit_info = limits[api_id]
    return {
        'used': limit_info.get('used', 0),
        'limit': config['rate_limit'],
        'remaining': config['rate_limit'] - limit_info.get('used', 0),
        'percentage': (limit_info.get('used', 0) / config['rate_limit']) * 100
    }

def update_rate_limit(api_id):
    """更新限流计数"""
    limits = load_rate_limits()
    config = API_CONFIG[api_id]
    
    if api_id not in limits:
        limits[api_id] = {
            'used': 1,
            'reset_at': (datetime.now() + timedelta(minutes=1)).isoformat()
        }
    else:
        limits[api_id]['used'] += 1
    
    save_rate_limits(limits)

def generate_markdown_report():
    """生成 Markdown 格式报告"""
    print("=" * 70)
    print("📊 API 健康状态")
    print("=" * 70)
    print(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    healthy_count = 0
    warning_count = 0
    total_response_time = 0
    api_count = 0
    
    # 健康 API
    print("### ✅ 正常")
    print()
    print("| API | 状态 | 响应时间 | 限流 | 缓存 |")
    print("|-----|------|---------|------|------|")
    
    for api_id, config in API_CONFIG.items():
        health = check_health(api_id)
        rate_status = get_rate_limit_status(api_id)
        
        if health['status'] == '✅':
            healthy_count += 1
            percentage = rate_status['percentage']
            limit_str = f"{rate_status['used']}/{rate_status['limit']} ({percentage:.0f}%)"
            
            if percentage > 80:
                limit_str = f"⚠️ {limit_str}"
            
            print(f"| {config['name']} | {health['status']} | {health['response_time']} | {limit_str} | ✅ {config['cache_ttl']/60:.0f}m |")
            total_response_time += float(health['response_time'].replace('ms', ''))
            api_count += 1
    
    print()
    
    # 警告 API
    print("### ⚠️  警告")
    print()
    warning_apis = []
    for api_id, config in API_CONFIG.items():
        health = check_health(api_id)
        if health['status'] == '⚠️':
            warning_apis.append((api_id, config, health))
    
    if warning_apis:
        print("| API | 状态 | 响应时间 | 限流 | 原因 |")
        print("|-----|------|---------|------|------|")
        for api_id, config, health in warning_apis:
            rate_status = get_rate_limit_status(api_id)
            percentage = rate_status['percentage']
            print(f"| {config['name']} | {health['status']} | {health['response_time']} | {rate_status['used']}/{rate_status['limit']} ({percentage:.0f}%) | {health.get('error', 'N/A')} |")
            warning_count += 1
    else:
        print("无")
    
    print()
    
    # 统计
    print("### 📈 统计")
    print()
    total_apis = len(API_CONFIG)
    health_rate = (healthy_count / total_apis) * 100 if total_apis > 0 else 0
    avg_response = total_response_time / api_count if api_count > 0 else 0
    
    print(f"- **总 API**: {total_apis}")
    print(f"- **健康率**: {health_rate:.0f}%")
    print(f"- **平均响应**: {avg_response:.0f}ms")
    print(f"- **缓存命中率**: 78% (模拟)")
    print()
    print("=" * 70)

def main():
    """主函数"""
    # 确保缓存目录存在
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成报告
    generate_markdown_report()
    
    # 检查是否有预警
    limits = load_rate_limits()
    alerts = []
    
    for api_id, config in API_CONFIG.items():
        rate_status = get_rate_limit_status(api_id)
        if rate_status['percentage'] > 80:
            alerts.append(f"⚠️  {config['name']} 限流预警：{rate_status['percentage']:.0f}%")
    
    if alerts:
        print("\n🚨 预警信息:")
        for alert in alerts:
            print(alert)

if __name__ == '__main__':
    main()
