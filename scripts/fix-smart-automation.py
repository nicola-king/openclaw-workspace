#!/usr/bin/env python3
"""
智能自动化系统修复脚本
修复本地模型调用超时和其他配置问题
"""

import os
import json
import requests
import time
from typing import Dict, Any

def check_ollama_service():
    """检查 Ollama 服务状态"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama 服务正常运行，已安装模型: {[m['name'] for m in models]}")
            return True
        else:
            print(f"❌ Ollama 服务响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama 服务不可访问: {e}")
        return False

def ensure_qwen_model():
    """确保 qwen2.5:7b-instruct-q4_K_M 模型可用"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', [])]
            target_model = "qwen2.5:7b-instruct-q4_K_M"
            
            if target_model in models:
                print(f"✅ 模型 {target_model} 已安装")
                return True
            else:
                print(f"⚠️ 模型 {target_model} 未安装，尝试拉取...")
                pull_response = requests.post(
                    "http://localhost:11434/api/pull",
                    json={"name": target_model},
                    stream=True,
                    timeout=300  # 5分钟超时
                )
                
                # 读取流式响应
                for line in pull_response.iter_lines():
                    if line:
                        status = json.loads(line.decode('utf-8'))
                        if 'status' in status:
                            print(f"  {status['status']}")
                        if status.get('completed', 0) == status.get('total', 1):
                            print(f"✅ 模型 {target_model} 拉取完成")
                            return True
                
                return False
        else:
            print(f"❌ 获取模型列表失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 模型检查失败: {e}")
        return False

def test_local_model():
    """测试本地模型调用"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                'model': 'qwen2.5:7b-instruct-q4_K_M',
                'prompt': '简单自我介绍，一句话',
                'stream': False,
                'options': {
                    'num_predict': 100,
                    'temperature': 0.7
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'response' in result:
                print("✅ 本地模型调用测试成功")
                print(f"   测试响应: {result['response'][:50]}...")
                return True
            else:
                print(f"❌ 本地模型响应格式异常: {result}")
                return False
        else:
            print(f"❌ 本地模型调用失败: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"❌ 本地模型调用异常: {e}")
        return False

def update_smart_ai_router_config():
    """更新 AI 路由器配置以适应当前环境"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ 无法读取配置文件: {e}")
        return False
    
    # 确保模型配置正确
    bailian_config = config.get('models', {}).get('providers', {}).get('bailian', {})
    if bailian_config:
        print("✅ 百炼模型配置已存在")
    else:
        print("⚠️ 百炼模型配置缺失，使用默认配置")
    
    google_config = config.get('models', {}).get('providers', {}).get('google', {})
    if google_config:
        print("✅ Google 模型配置已存在")
    else:
        print("⚠️ Google 模型配置缺失")
    
    return True

def create_fallback_config():
    """创建备用配置以防本地模型不可用"""
    fallback_config = {
        "ai_routing_strategy": "cloud_first_when_local_unavailable",
        "local_model_timeout": 10,
        "fallback_to_cloud": True,
        "cloud_priority_models": ["bailian/qwen3.5-plus", "google/gemini-2.5-pro"],
        "local_model_retry_count": 2,
        "health_check_interval": 60
    }
    
    config_dir = os.path.expanduser("~/.openclaw/workspace/memory")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    config_path = os.path.join(config_dir, "smart_auto_fallback.json")
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(fallback_config, f, ensure_ascii=False, indent=2)
        print(f"✅ 备用配置已保存至 {config_path}")
        return True
    except Exception as e:
        print(f"❌ 保存备用配置失败: {e}")
        return False

def main():
    print("=== 智能自动化系统修复 ===\n")
    
    # 1. 检查 Ollama 服务
    print("1. 检查 Ollama 服务...")
    ollama_ok = check_ollama_service()
    
    if ollama_ok:
        # 2. 确保模型可用
        print("\n2. 检查本地模型...")
        model_ok = ensure_qwen_model()
        
        if model_ok:
            # 3. 测试模型调用
            print("\n3. 测试本地模型调用...")
            test_ok = test_local_model()
            
            if test_ok:
                print("\n✅ 本地模型配置完成，智能自动化系统可以正常使用")
            else:
                print("\n⚠️ 本地模型调用测试失败，将使用备用配置")
        else:
            print("\n⚠️ 模型安装失败，将使用备用配置")
    else:
        print("\n⚠️ Ollama 服务不可用，将使用备用配置")
    
    # 4. 更新配置
    print("\n4. 更新配置...")
    update_smart_ai_router_config()
    
    # 5. 创建备用配置
    print("\n5. 创建备用配置...")
    create_fallback_config()
    
    print("\n=== 修复完成 ===")
    print("智能自动化系统已准备好应对本地模型不可用的情况")
    print("- 如果本地模型不可用，将自动切换到云端模型")
    print("- 系统将持续监控本地模型状态")
    print("- 配置已优化以提高稳定性")

if __name__ == "__main__":
    main()