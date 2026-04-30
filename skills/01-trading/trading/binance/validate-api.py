#!/usr/bin/env python3
"""
币安 API 验证脚本

功能:
- 测试 API Key 连通性
- 验证账户信息 (需要 Secret Key)
- 检查账户权限和余额
- 生成验证报告
"""

import os
import json
import hashlib
import hmac
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ 缺少依赖：pip install requests")
    exit(1)

# 配置
API_KEY = "ufHaoQRuMLI0HScM99mt3ZGUMc7xFJt0hwZGsKqS9MYRW7Y2SzQ7jzsuN834JcVe"
SECRET_KEY = "PGilezOeAzuNq4ZwrNGIUgpVYDMOBUjhhp10SGMKRoTrpoqHqkTvs86qJWqvhox3"
BASE_URL = "https://api.binance.com"

class BinanceValidator:
    """币安 API 验证器"""
    
    def __init__(self, api_key: str, secret_key: str = None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = BASE_URL
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "api_key": api_key[:10] + "..." + api_key[-6:],
            "tests": [],
            "account_info": None,
            "balance": None,
            "permissions": [],
            "errors": [],
            "status": "UNKNOWN"
        }
    
    def generate_signature(self, query_string: str) -> str:
        """生成 HMAC SHA256 签名"""
        if not self.secret_key:
            return None
        return hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def test_ping(self) -> bool:
        """测试 API 连通性 (不需要认证)"""
        try:
            url = f"{self.base_url}/api/v3/ping"
            response = requests.get(url, timeout=10)
            result = response.status_code == 200
            self.report["tests"].append({
                "name": "API Ping",
                "status": "✅ PASS" if result else "❌ FAIL",
                "details": f"Status: {response.status_code}"
            })
            return result
        except Exception as e:
            self.report["errors"].append(f"Ping failed: {str(e)}")
            self.report["tests"].append({
                "name": "API Ping",
                "status": "❌ FAIL",
                "details": str(e)
            })
            return False
    
    def test_time(self) -> bool:
        """测试服务器时间 (不需要认证)"""
        try:
            url = f"{self.base_url}/api/v3/time"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                server_time = datetime.fromtimestamp(data['serverTime'] / 1000)
                self.report["tests"].append({
                    "name": "Server Time",
                    "status": "✅ PASS",
                    "details": f"Server time: {server_time.isoformat()}"
                })
                return True
            return False
        except Exception as e:
            self.report["errors"].append(f"Time check failed: {str(e)}")
            self.report["tests"].append({
                "name": "Server Time",
                "status": "❌ FAIL",
                "details": str(e)
            })
            return False
    
    def test_exchange_info(self) -> bool:
        """获取交易对信息 (不需要认证)"""
        try:
            url = f"{self.base_url}/api/v3/exchangeInfo"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                symbols = data.get('symbols', [])
                btc_eth = [s for s in symbols if s['symbol'] in ['BTCUSDT', 'ETHUSDT']]
                self.report["tests"].append({
                    "name": "Exchange Info",
                    "status": "✅ PASS",
                    "details": f"Total symbols: {len(symbols)}, BTC/ETH available: {len(btc_eth) == 2}"
                })
                return True
            return False
        except Exception as e:
            self.report["errors"].append(f"Exchange info failed: {str(e)}")
            self.report["tests"].append({
                "name": "Exchange Info",
                "status": "❌ FAIL",
                "details": str(e)
            })
            return False
    
    def test_account_info(self) -> bool:
        """获取账户信息 (需要 Secret Key)"""
        if not self.secret_key:
            self.report["tests"].append({
                "name": "Account Info",
                "status": "⚠️ SKIP",
                "details": "Secret Key not provided"
            })
            return False
        
        try:
            timestamp = int(time.time() * 1000)
            params = f"timestamp={timestamp}"
            signature = self.generate_signature(params)
            
            url = f"{self.base_url}/api/v3/account"
            headers = {"X-MBX-APIKEY": self.api_key}
            params_dict = {"timestamp": timestamp, "signature": signature}
            
            response = requests.get(url, headers=headers, params=params_dict, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.report["account_info"] = {
                    "maker_commission": data.get('makerCommission', 0),
                    "taker_commission": data.get('takerCommission', 0),
                    "buyer": data.get('canTrade', False),
                    "seller": data.get('canSell', False),
                    "withdraw": data.get('canWithdraw', False),
                    "deposit": data.get('canDeposit', False)
                }
                self.report["permissions"] = [
                    f"Trading: {'✅' if data.get('canTrade') else '❌'}",
                    f"Selling: {'✅' if data.get('canSell') else '❌'}",
                    f"Withdrawal: {'⚠️' if data.get('canWithdraw') else '✅ (Disabled)'}",
                    f"Deposit: {'✅' if data.get('canDeposit') else '❌'}"
                ]
                
                # 检查余额
                balances = data.get('balances', [])
                usdt_balance = next((b for b in balances if b['asset'] == 'USDT'), None)
                btc_balance = next((b for b in balances if b['asset'] == 'BTC'), None)
                eth_balance = next((b for b in balances if b['asset'] == 'ETH'), None)
                
                self.report["balance"] = {
                    "USDT": float(usdt_balance['free']) if usdt_balance else 0,
                    "BTC": float(btc_balance['free']) if btc_balance else 0,
                    "ETH": float(eth_balance['free']) if eth_balance else 0
                }
                
                self.report["tests"].append({
                    "name": "Account Info",
                    "status": "✅ PASS",
                    "details": f"USDT: {self.report['balance']['USDT']:.2f}, BTC: {self.report['balance']['BTC']:.4f}, ETH: {self.report['balance']['ETH']:.4f}"
                })
                return True
            else:
                error_msg = response.text
                self.report["errors"].append(f"Account info failed: {error_msg}")
                self.report["tests"].append({
                    "name": "Account Info",
                    "status": "❌ FAIL",
                    "details": f"HTTP {response.status_code}: {error_msg[:100]}"
                })
                return False
        except Exception as e:
            self.report["errors"].append(f"Account info failed: {str(e)}")
            self.report["tests"].append({
                "name": "Account Info",
                "status": "❌ FAIL",
                "details": str(e)
            })
            return False
    
    def run_all_tests(self) -> dict:
        """运行所有测试"""
        print("🔍 开始币安 API 验证...")
        print("=" * 50)
        
        # 基础测试 (不需要 Secret Key)
        print("\n📡 基础连接测试...")
        self.test_ping()
        self.test_time()
        self.test_exchange_info()
        
        # 账户测试 (需要 Secret Key)
        if self.secret_key:
            print("\n🔐 账户验证测试...")
            self.test_account_info()
        else:
            print("\n⚠️  跳过账户验证 (缺少 Secret Key)")
            self.report["tests"].append({
                "name": "Account Verification",
                "status": "⚠️ SKIP",
                "details": "Secret Key required but not provided"
            })
        
        # 确定总体状态
        passed = sum(1 for t in self.report["tests"] if t["status"] == "✅ PASS")
        total = len([t for t in self.report["tests"] if t["status"] != "⚠️ SKIP"])
        
        if total > 0 and passed == total:
            self.report["status"] = "✅ VALID"
        elif passed > 0:
            self.report["status"] = "⚠️ PARTIAL"
        else:
            self.report["status"] = "❌ INVALID"
        
        return self.report
    
    def generate_report(self) -> str:
        """生成验证报告"""
        report = f"""# 币安 API 验证报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**API Key**: `{self.report['api_key']}`
**验证状态**: {self.report['status']}

---

## 📊 测试结果

| 测试项 | 状态 | 详情 |
|--------|------|------|
"""
        for test in self.report["tests"]:
            report += f"| {test['name']} | {test['status']} | {test['details']} |\n"
        
        report += "\n---\n\n"
        
        # 账户信息
        if self.report["account_info"]:
            report += """## 🔐 账户权限

| 权限 | 状态 |
|------|------|
"""
            for perm in self.report["permissions"]:
                report += f"| {perm.split(':')[0]} | {perm.split(':')[1]} |\n"
            
            report += "\n### 💰 账户余额\n\n"
            if self.report["balance"]:
                report += f"""
- **USDT**: `{self.report['balance']['USDT']:.2f}`
- **BTC**: `{self.report['balance']['BTC']:.4f}`
- **ETH**: `{self.report['balance']['ETH']:.4f}`
"""
        
        # 错误信息
        if self.report["errors"]:
            report += "\n---\n\n## ❌ 错误信息\n\n"
            for error in self.report["errors"]:
                report += f"- {error}\n"
        
        # 结论和建议
        report += "\n---\n\n## ✅ 验证结论\n\n"
        
        if self.report["status"] == "✅ VALID":
            report += """
**API Key 有效，可以正常使用。**

### 建议:
1. ✅ 配置 IP 白名单 (仅允许工控机 IP)
2. ✅ 确认已禁用提现权限
3. ✅ 开始策略集成测试
"""
        elif self.report["status"] == "⚠️ PARTIAL":
            report += """
**API Key 部分验证通过，需要补充配置。**

### 待办事项:
1. ⚠️ **补充 Secret Key** - 需要用户提供
2. ⚠️ 验证账户权限和余额
3. ⚠️ 配置 IP 白名单

### 如何获取 Secret Key:
1. 登录币安账户
2. 进入 API 管理页面
3. 找到对应 API Key
4. 查看/复制 Secret Key (仅显示一次)
"""
        else:
            report += """
**API Key 验证失败。**

### 可能原因:
1. API Key 已过期或被删除
2. API Key 权限不足
3. IP 白名单限制
4. Secret Key 错误

### 建议:
1. 重新生成 API Key
2. 检查 API 权限配置
3. 确认 IP 白名单设置
"""
        
        report += "\n---\n\n*太一 AGI · 币安 API 验证工具 v1.0*\n"
        
        return report
    
    def save_report(self, output_path: str):
        """保存报告到文件"""
        report_md = self.generate_report()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_md)
        print(f"\n📝 报告已保存：{output_path}")


def main():
    """主函数"""
    # 检查是否有 Secret Key
    secret_key = None
    env_file = Path("/home/nicola/.openclaw/.env.binance")
    
    print(f"📁 检查配置文件：{env_file}")
    print(f"配置文件存在：{env_file.exists()}")
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith("BINANCE_SECRET_KEY="):
                    secret_key = line.split("=", 1)[1].strip()
                    print(f"✅ 找到 Secret Key: {secret_key[:10]}...{secret_key[-6:]}")
                    break
    
    print(f"Secret Key 已加载：{secret_key is not None}")
    
    # 创建验证器
    validator = BinanceValidator(API_KEY, secret_key)
    
    # 运行测试
    report = validator.run_all_tests()
    
    # 保存报告
    output_path = "/home/nicola/.openclaw/workspace/reports/binance-api-test.md"
    validator.save_report(output_path)
    
    # 保存 JSON 报告
    json_path = "/home/nicola/.openclaw/workspace/reports/binance-api-test.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print(f"最终状态：{report['status']}")
    
    if report['status'] == "⚠️ PARTIAL":
        print("\n⚠️  需要补充 Secret Key 才能完成验证")
        print("请查看配置文件：/home/nicola/.openclaw/.env.binance")


if __name__ == "__main__":
    main()
