#!/usr/bin/env python3
"""
公共 API 测试脚本 - P0+P1 验证
执行：python scripts/test-public-apis.py
"""

import requests
import json
from datetime import datetime

def test_coingecko():
    """测试 CoinGecko API (无需 API Key)"""
    print("=" * 60)
    print("🔴 CoinGecko API 测试")
    print("=" * 60)
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum,solana,cardano,dogecoin',
        'vs_currencies': 'usd,cny',
        'include_24hr_change': True
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ 请求成功")
        print(f"\n📊 加密货币价格 (实时更新)")
        print(f"{'币种':<12} {'USD':>12} {'CNY':>12} {'24h 涨跌':>10}")
        print("-" * 60)
        
        coins = {
            'bitcoin': '比特币 (BTC)',
            'ethereum': '以太坊 (ETH)',
            'solana': '索拉纳 (SOL)',
            'cardano': '卡尔达诺 (ADA)',
            'dogecoin': '狗狗币 (DOGE)'
        }
        
        for coin_id, coin_name in coins.items():
            if coin_id in data:
                usd = data[coin_id]['usd']
                cny = data[coin_id].get('cny', usd * 7.2)
                change = data[coin_id].get('usd_24h_change', 0)
                change_str = f"{change:+.2f}%"
                print(f"{coin_name:<12} ${usd:>10,} ¥{cny:>10,} {change_str:>10}")
        
        print(f"\n数据来源：CoinGecko API")
        print(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


def test_newsapi(api_key=None):
    """测试 NewsAPI (需要 API Key)"""
    print("\n" + "=" * 60)
    print("📰 NewsAPI 测试")
    print("=" * 60)
    
    if not api_key:
        print("⚠️  API Key 未提供")
        print("\n获取方式:")
        print("1. 访问：https://newsapi.org/register")
        print("2. 注册免费账号")
        print("3. 复制 API Key")
        print("4. 添加到 .env 文件：NEWS_API_KEY=your_key")
        print("\n或手动测试:")
        print("curl 'https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_KEY'")
        return False
    
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'us',
        'category': 'technology',
        'pageSize': 5,
        'apiKey': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'error':
            print(f"❌ API 错误：{data.get('message')}")
            return False
        
        print(f"✅ 请求成功")
        print(f"\n📰 美国科技头条 (共 {data['totalResults']} 条)")
        print(f"{'序号':<4} {'标题':<50} {'来源':<15}")
        print("-" * 60)
        
        for i, article in enumerate(data['articles'][:5], 1):
            title = article['title'][:47] + "..." if len(article['title']) > 50 else article['title']
            source = article['source']['name'][:13] + "..." if len(article['source']['name']) > 15 else article['source']['name']
            print(f"{i:<4} {title:<50} {source:<15}")
        
        print(f"\n免费层限制：100 请求/天")
        print(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


def test_open_meteo():
    """测试 Open-Meteo 天气 API (无需 API Key)"""
    print("\n" + "=" * 60)
    print("🌤️  Open-Meteo 天气 API 测试")
    print("=" * 60)
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': 31.2304,  # 上海
        'longitude': 121.4737,
        'current_weather': True
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ 请求成功")
        print(f"\n🌤️  上海天气 (实时)")
        print(f"温度：{data['current_weather']['temperature']}°C")
        print(f"风速：{data['current_weather']['windspeed']} km/h")
        print(f"风向：{data['current_weather']['winddirection']}°")
        print(f"时间：{data['current_weather']['time']}")
        print(f"\n数据来源：Open-Meteo (免费，无需 API Key)")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("🚀 公共 API 测试 - P0+P1 验证")
    print("=" * 60)
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        'CoinGecko': test_coingecko(),
        'Open-Meteo': test_open_meteo(),
    }
    
    # NewsAPI 需要 Key
    import os
    news_api_key = os.getenv('NEWS_API_KEY')
    results['NewsAPI'] = test_newsapi(news_api_key)
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    for api, success in results.items():
        status = "✅ 通过" if success else "❌ 失败" if api != 'NewsAPI' else "⚠️  需配置"
        print(f"{api:<15} {status}")
    
    print("\n💡 下一步:")
    print("1. CoinGecko ✅ 可直接使用")
    print("2. Open-Meteo ✅ 可直接使用")
    print("3. NewsAPI ⚠️  需要注册获取 API Key")
    print("\n注册链接：https://newsapi.org/register")
    print("=" * 60)


if __name__ == '__main__':
    main()
