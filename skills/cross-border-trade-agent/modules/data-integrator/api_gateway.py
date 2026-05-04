#!/usr/bin/env python3
"""
API Gateway v10.0
统一 API 网关 - 汇率/海关/法规数据源
"""
import sys
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_providers.exchange_rate import ExchangeRateAPI
from api_providers.customs_data import CustomsDataAPI
from api_providers.regulation_tracker import RegulationTracker

class APIGateway:
    """统一 API 网关"""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.logger = logging.getLogger("api-gateway")
        self.exchange_rate = ExchangeRateAPI(self.config.get("exchange_rate", {}))
        self.customs_data = CustomsDataAPI(self.config.get("customs_data", {}))
        self.regulation_tracker = RegulationTracker(self.config.get("regulation_tracker", {}))

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Dict[str, Any]:
        return self.exchange_rate.get_rate(from_currency, to_currency)

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
        return self.exchange_rate.convert(amount, from_currency, to_currency)

    def get_hs_code_info(self, hs_code: str) -> Dict[str, Any]:
        return self.customs_data.get_hs_code_info(hs_code)

    def get_tariff_rate(self, hs_code: str, country: str) -> Dict[str, Any]:
        return self.customs_data.get_tariff_rate(hs_code, country)

    def get_regulations(self, country: str, category: str) -> Dict[str, Any]:
        return self.regulation_tracker.get_regulations(country, category)

    def check_compliance(self, country: str, category: str, certifications: list) -> Dict[str, Any]:
        return self.regulation_tracker.check_compliance(country, category, certifications)

    def health_check(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "module": "api-gateway",
            "version": "10.0.0",
            "providers": {
                "exchange_rate": "active",
                "customs_data": "active",
                "regulation_tracker": "active"
            },
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    gateway = APIGateway()
    print(json.dumps(gateway.health_check(), ensure_ascii=False, indent=2))
    print("\n=== 汇率测试 ===")
    print(json.dumps(gateway.get_exchange_rate("CNY", "AUD"), ensure_ascii=False, indent=2))
    print("\n=== 关税测试 ===")
    print(json.dumps(gateway.get_tariff_rate("9406.00", "Australia"), ensure_ascii=False, indent=2))
