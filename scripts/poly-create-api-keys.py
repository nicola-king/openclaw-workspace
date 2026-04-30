#!/usr/bin/env python3
"""
Polymarket API Key 创建工具
使用现有私钥生成 L2 API Key 三元组 (api_key, secret, passphrase)

注意：此脚本只需要运行一次，生成后可重复使用
"""

import json
from py_clob_client.client import ClobClient
from py_clob_client.clob_auth import create_or_update_api_keys
from py_clob_client.signing import create_poly_signature

# 配置
HOST = "https://clob.polymarket.com"
CHAIN_ID = 137  # Polygon

def main():
    print("=" * 60)
    print("Polymarket API Key 创建工具")
    print("=" * 60)
    print()
    print("⚠️  重要说明:")
    print("   1. 此脚本用于生成 L2 API Key 三元组")
    print("   2. 生成后只需保存 api_key, api_secret, api_passphrase")
    print("   3. 之后交易无需私钥，只用三元组即可")
    print()
    
    # 检查是否已有私钥配置
    config_file = "/home/nicola/.taiyi/zhiji/polymarket.json"
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # 检查是否已有三元组
        if all(k in config.get('polymarket', {}) for k in ['api_key', 'api_secret', 'api_passphrase']):
            print("✅ 已找到完整的 API Key 三元组:")
            print(f"   api_key: {config['polymarket']['api_key']}")
            print(f"   api_secret: {config['polymarket']['api_secret'][:20]}...")
            print(f"   api_passphrase: {config['polymarket']['api_passphrase']}")
            print()
            print("可以直接使用，无需重新生成!")
            return
        
        # 检查是否有私钥
        private_key = config.get('polymarket', {}).get('signer_private_key')
        if not private_key:
            print("❌ 未找到私钥配置")
            print()
            print("请在 Polymarket 官网手动创建 API Key:")
            print("   1. 登录 https://polymarket.com")
            print("   2. 点击头像 → Profile")
            print("   3. 找到 'Builder Keys' 或 'API Keys'")
            print("   4. 点击 '+ Create New'")
            print("   5. 复制 api_key, api_secret, api_passphrase")
            print("   6. 配置到 ~/.taiyi/zhiji/polymarket.json")
            print()
            print("配置文件模板:")
            print(json.dumps({
                "polymarket": {
                    "api_key": "你的 api_key",
                    "api_secret": "你的 api_secret",
                    "api_passphrase": "你的 api_passphrase",
                    "wallet_address": "0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5"
                }
            }, indent=2))
            return
        
        print("✅ 找到私钥，开始生成 API Key 三元组...")
        print()
        
        # 创建客户端并生成 API Key
        client = ClobClient(HOST, key=private_key, chain_id=CHAIN_ID)
        
        # 创建或更新 API Key
        api_creds = create_or_update_api_keys(client, private_key)
        
        print("✅ API Key 三元组生成成功!")
        print()
        print("请保存以下信息 (secret 和 passphrase 只显示一次):")
        print("-" * 60)
        print(f"api_key: {api_creds.api_key}")
        print(f"api_secret: {api_creds.api_secret}")
        print(f"api_passphrase: {api_creds.api_passphrase}")
        print("-" * 60)
        print()
        
        # 更新配置文件
        config['polymarket']['api_key'] = api_creds.api_key
        config['polymarket']['api_secret'] = api_creds.api_secret
        config['polymarket']['api_passphrase'] = api_creds.api_passphrase
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ 配置文件已更新：{config_file}")
        print()
        print("现在可以使用 API Key 三元组进行交易，无需私钥!")
        
    except FileNotFoundError:
        print(f"❌ 配置文件不存在：{config_file}")
    except Exception as e:
        print(f"❌ 错误：{e}")
        print()
        print("请在 Polymarket 官网手动创建 API Key")

if __name__ == "__main__":
    main()
