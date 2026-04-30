#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APILayer API 集成 - 公共 API 统一调用

功能:
1. IPstack - IP 地址定位
2. Marketstack - 股票市场数据
3. Weatherstack - 天气信息
4. Fixer - 汇率数据
5. Aviationstack - 航班状态
6. 统一 API 调用接口

来源：APILayer 公共 API 平台
https://apilayer.com/marketplace

作者：太一 AGI
创建：2026-04-14
"""

import os
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
DATA_DIR = WORKSPACE / "data" / "apilayer"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# API 配置 (从环境变量获取)
APILAYER_BASE_URL = "https://api.apilayer.com"
API_KEYS = {
    "ipstack": os.getenv("APILAYER_IPSTACK_KEY", ""),
    "marketstack": os.getenv("APILAYER_MARKETSTACK_KEY", ""),
    "weatherstack": os.getenv("APILAYER_WEATHERSTACK_KEY", ""),
    "fixer": os.getenv("APILAYER_FIXER_KEY", ""),
    "aviationstack": os.getenv("APILAYER_AVIATIONSTACK_KEY", ""),
}


class APILayerClient:
    """APILayer API 客户端"""
    
    def __init__(self):
        self.base_url = APILAYER_BASE_URL
        self.api_keys = API_KEYS
        self.session = requests.Session()
        self.session.headers.update({
            "apikey": "",  # 动态设置
        })
    
    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """通用请求方法"""
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ========== IPstack - IP 地址定位 ==========
    def ipstack_lookup(self, ip: str) -> Dict:
        """
        IP 地址定位
        
        Args:
            ip: IP 地址
        
        Returns:
            定位信息
        """
        if not self.api_keys["ipstack"]:
            return {"success": False, "error": "API Key 未配置"}
        
        self.session.headers.update({"apikey": self.api_keys["ipstack"]})
        result = self._request(f"/ipstack/{ip}")
        
        if result.get("success"):
            print(f"✅ IP 定位成功：{ip}")
            print(f"  国家：{result.get('country_name', 'N/A')}")
            print(f"  城市：{result.get('city', 'N/A')}")
            print(f"  时区：{result.get('time_zone', {}).get('id', 'N/A')}")
        else:
            print(f"❌ IP 定位失败：{result.get('error', {}).get('info', 'Unknown error')}")
        
        return result
    
    # ========== Marketstack - 股票市场数据 ==========
    def marketstack_eod(self, symbol: str, date: Optional[str] = None) -> Dict:
        """
        股票收盘数据
        
        Args:
            symbol: 股票代码 (如 AAPL)
            date: 日期 (YYYY-MM-DD)
        
        Returns:
            股票数据
        """
        if not self.api_keys["marketstack"]:
            return {"success": False, "error": "API Key 未配置"}
        
        self.session.headers.update({"apikey": self.api_keys["marketstack"]})
        params = {"symbols": symbol}
        if date:
            params["date"] = date
        
        result = self._request("/marketstack/eod", params)
        
        if result.get("data"):
            data = result["data"][0]
            print(f"✅ 股票数据成功：{symbol}")
            print(f"  日期：{data.get('date', 'N/A')}")
            print(f"  开盘：{data.get('open', 'N/A')}")
            print(f"  收盘：{data.get('close', 'N/A')}")
            print(f"  最高：{data.get('high', 'N/A')}")
            print(f"  最低：{data.get('low', 'N/A')}")
        else:
            print(f"❌ 股票数据失败：{result.get('error', {}).get('message', 'Unknown error')}")
        
        return result
    
    # ========== Weatherstack - 天气信息 ==========
    def weatherstack_current(self, location: str) -> Dict:
        """
        当前天气
        
        Args:
            location: 地点 (城市名或经纬度)
        
        Returns:
            天气信息
        """
        if not self.api_keys["weatherstack"]:
            return {"success": False, "error": "API Key 未配置"}
        
        self.session.headers.update({"apikey": self.api_keys["weatherstack"]})
        result = self._request("/weatherstack/current", {"query": location})
        
        if result.get("current"):
            current = result["current"]
            print(f"✅ 天气查询成功：{location}")
            print(f"  温度：{current.get('temperature', 'N/A')}°C")
            print(f"  天气：{current.get('weather_descriptions', ['N/A'])[0]}")
            print(f"  湿度：{current.get('humidity', 'N/A')}%")
            print(f"  风速：{current.get('wind_speed', 'N/A')} km/h")
        else:
            print(f"❌ 天气查询失败：{result.get('error', {}).get('info', 'Unknown error')}")
        
        return result
    
    # ========== Fixer - 汇率数据 ==========
    def fixer_latest(self, base: str = "USD", symbols: Optional[str] = None) -> Dict:
        """
        最新汇率
        
        Args:
            base: 基础货币 (默认 USD)
            symbols: 目标货币 (逗号分隔，如 EUR,CNY,JPY)
        
        Returns:
            汇率数据
        """
        if not self.api_keys["fixer"]:
            return {"success": False, "error": "API Key 未配置"}
        
        self.session.headers.update({"apikey": self.api_keys["fixer"]})
        params = {"base": base}
        if symbols:
            params["symbols"] = symbols
        
        result = self._request("/fixer/latest", params)
        
        if result.get("success"):
            print(f"✅ 汇率查询成功：{base}")
            print(f"  日期：{result.get('date', 'N/A')}")
            rates = result.get("rates", {})
            for currency, rate in list(rates.items())[:5]:  # 只显示前 5 个
                print(f"  {currency}: {rate:.4f}")
        else:
            print(f"❌ 汇率查询失败：{result.get('error', {}).get('info', 'Unknown error')}")
        
        return result
    
    # ========== Aviationstack - 航班状态 ==========
    def aviationstack_flights(self, access_key: str, params: Optional[Dict] = None) -> Dict:
        """
        航班状态
        
        Args:
            access_key: API Key
            params: 查询参数 (如 flight_iata, dep_iata, arr_iata)
        
        Returns:
            航班数据
        """
        if not access_key:
            return {"success": False, "error": "API Key 未配置"}
        
        self.session.headers.update({"apikey": access_key})
        result = self._request("/aviationstack/flights", params)
        
        if result.get("data"):
            print(f"✅ 航班查询成功")
            print(f"  航班数量：{len(result['data'])}")
            for flight in result["data"][:3]:  # 只显示前 3 个
                print(f"  - {flight.get('flight_iata', 'N/A')}: {flight.get('dep_iata', 'N/A')} → {flight.get('arr_iata', 'N/A')}")
        else:
            print(f"❌ 航班查询失败：{result.get('error', {}).get('info', 'Unknown error')}")
        
        return result
    
    def save_result(self, result: Dict, filename: str):
        """保存结果到文件"""
        import json
        output_file = DATA_DIR / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 结果已保存：{output_file}")
        return output_file


def main():
    """测试"""
    print("=" * 60)
    print("🌐 APILayer API 集成测试")
    print("=" * 60)
    
    client = APILayerClient()
    
    # 测试 1: IP 定位 (使用示例 IP)
    print("\n📍 测试 1: IP 定位")
    result = client.ipstack_lookup("8.8.8.8")
    client.save_result(result, "ipstack_test")
    
    # 测试 2: 股票数据 (AAPL)
    print("\n📈 测试 2: 股票数据")
    result = client.marketstack_eod("AAPL", "2024-01-01")
    client.save_result(result, "marketstack_test")
    
    # 测试 3: 天气查询 (北京)
    print("\n🌤️ 测试 3: 天气查询")
    result = client.weatherstack_current("Beijing")
    client.save_result(result, "weatherstack_test")
    
    # 测试 4: 汇率查询
    print("\n💱 测试 4: 汇率查询")
    result = client.fixer_latest("USD", "EUR,CNY,JPY,GBP")
    client.save_result(result, "fixer_test")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    
    print("\n📁 输出文件:")
    print(f"  数据目录：{DATA_DIR}")


if __name__ == "__main__":
    main()
