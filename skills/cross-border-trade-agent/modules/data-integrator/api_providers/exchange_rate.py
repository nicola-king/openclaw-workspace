#!/usr/bin/env python3
"""
Exchange Rate API Provider v10.0
实时汇率数据源 - 接入真实 API
"""
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

class ExchangeRateAPI:
    """汇率 API 提供者"""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.logger = logging.getLogger("exchange-rate-api")
        self.cache = {}
        self.cache_ttl = self.config.get("cache_ttl", 3600)

    def get_rate(self, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """获取实时汇率"""
        cache_key = f"{from_currency}_{to_currency}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if datetime.now().timestamp() - cached["cached_at"] < self.cache_ttl:
                return cached["data"]

        rate = None
        source = None

        # 1. Frankfurter API (免费，无需 key)
        try:
            if HAS_REQUESTS:
                resp = requests.get(
                    "https://api.frankfurter.app/latest",
                    params={"from": from_currency, "to": to_currency},
                    timeout=10
                )
                if resp.status_code == 200:
                    data = resp.json()
                    rate = data["rates"][to_currency]
                    source = "frankfurter"
        except Exception as e:
            self.logger.warning(f"Frankfurter API failed: {e}")

        # 2. ExchangeRate API (免费，无需 key)
        if not rate:
            try:
                if HAS_REQUESTS:
                    resp = requests.get(
                        f"https://api.exchangerate-api.com/v4/latest/{from_currency}",
                        timeout=10
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        rate = data["rates"][to_currency]
                        source = "exchangerate-api"
            except Exception as e:
                self.logger.warning(f"ExchangeRate API failed: {e}")

        result = {
            "from": from_currency,
            "to": to_currency,
            "rate": rate,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }

        if rate:
            self.cache[cache_key] = {"data": result, "cached_at": datetime.now().timestamp()}

        return result

    def convert(self, amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """货币换算"""
        rate_data = self.get_rate(from_currency, to_currency)
        if rate_data.get("rate"):
            return {
                "amount": amount,
                "from": from_currency,
                "to": to_currency,
                "rate": rate_data["rate"],
                "converted": round(amount * rate_data["rate"], 2),
                "source": rate_data["source"],
                "timestamp": rate_data["timestamp"]
            }
        return rate_data


if __name__ == "__main__":
    api = ExchangeRateAPI()
    print(json.dumps(api.get_rate("CNY", "AUD"), ensure_ascii=False, indent=2))
