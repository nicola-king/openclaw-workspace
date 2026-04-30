#!/usr/bin/env python3
"""
太一 - 大模型智能路由
自动识别国内/海外模型，智能分流请求

规则：
1. 国内模型（百炼/DeepSeek/Kimi）→ 直连，不走代理
2. 海外模型（Google/Gemini/Claude/OpenAI）→ 走代理
3. 智能分流 → Clash 每月 300GB 流量限制
4. 自动识别 → 无需手动切换

用法：
    python3 model-router.py --model qwen --prompt "你好"
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# 模型分类
DOMESTIC_MODELS = {
    # 阿里云百炼
    "qwen": "https://dashscope.aliyuncs.com/api/v1",
    "qwen-turbo": "https://dashscope.aliyuncs.com/api/v1",
    "qwen-plus": "https://dashscope.aliyuncs.com/api/v1",
    "qwen-max": "https://dashscope.aliyuncs.com/api/v1",
    "qwen-coder": "https://dashscope.aliyuncs.com/api/v1",
    "qwen3.5-plus": "https://dashscope.aliyuncs.com/api/v1",
    # DeepSeek
    "deepseek": "https://api.deepseek.com/v1",
    "deepseek-chat": "https://api.deepseek.com/v1",
    "deepseek-coder": "https://api.deepseek.com/v1",
    # Kimi (月之暗面)
    "kimi": "https://api.moonshot.cn/v1",
    "kimi-chat": "https://api.moonshot.cn/v1",
    # 智谱 AI
    "glm": "https://open.bigmodel.cn/api/paas/v4",
    "glm-4": "https://open.bigmodel.cn/api/paas/v4",
    # 百度文心
    "ernie": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1",
    "ernie-bot": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1",
}

OVERSEAS_MODELS = {
    # Google
    "gemini": "https://generativelanguage.googleapis.com/v1",
    "gemini-pro": "https://generativelanguage.googleapis.com/v1",
    "gemini-2.5-pro": "https://generativelanguage.googleapis.com/v1",
    # OpenAI
    "gpt": "https://api.openai.com/v1",
    "gpt-4": "https://api.openai.com/v1",
    "gpt-4o": "https://api.openai.com/v1",
    "gpt-3.5-turbo": "https://api.openai.com/v1",
    # Claude (Anthropic)
    "claude": "https://api.anthropic.com/v1",
    "claude-3": "https://api.anthropic.com/v1",
    "claude-sonnet": "https://api.anthropic.com/v1",
    "claude-opus": "https://api.anthropic.com/v1",
    # Meta
    "llama": "https://api.llama.com/v1",
    "llama-3": "https://api.llama.com/v1",
}

class ModelRouter:
    """大模型智能路由器"""
    
    def __init__(self):
        self.config_path = Path.home() / ".taiyi" / "model-router" / "config.json"
        self.config = self.load_config()
        
        # Clash 代理配置
        self.proxy = self.config.get("clash_proxy", "")
        self.clash_limit_gb = self.config.get("clash_monthly_limit_gb", 300)
        
        # 流量统计
        self.traffic_log_path = Path.home() / ".taiyi" / "model-router" / "traffic.log"
        self.monthly_traffic = self.load_traffic()
    
    def load_config(self):
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {
            "clash_proxy": "http://127.0.0.1:7890",
            "clash_monthly_limit_gb": 300,
            "domestic_models": DOMESTIC_MODELS,
            "overseas_models": OVERSEAS_MODELS
        }
    
    def load_traffic(self):
        """加载流量统计"""
        if not self.traffic_log_path.exists():
            return 0
        
        current_month = datetime.now().strftime("%Y-%m")
        with open(self.traffic_log_path, "r") as f:
            for line in f:
                if line.startswith(current_month):
                    return float(line.split(",")[1])
        return 0
    
    def log_traffic(self, bytes_used):
        """记录流量"""
        current_month = datetime.now().strftime("%Y-%m")
        mb_used = bytes_used / (1024 * 1024)
        
        with open(self.traffic_log_path, "a") as f:
            f.write(f"{current_month},{mb_used:.2f}\n")
    
    def identify_model(self, model_name):
        """识别模型类型"""
        model_name_lower = model_name.lower()
        
        # 检查国内模型
        for key in DOMESTIC_MODELS:
            if key in model_name_lower:
                return "domestic", DOMESTIC_MODELS[key]
        
        # 检查海外模型
        for key in OVERSEAS_MODELS:
            if key in model_name_lower:
                return "overseas", OVERSEAS_MODELS[key]
        
        # 默认：海外模型（保守策略）
        return "overseas", None
    
    def check_traffic_limit(self):
        """检查流量限制"""
        limit_mb = self.clash_limit_gb * 1024
        used_mb = self.monthly_traffic
        
        if used_mb > limit_mb * 0.9:
            print(f"⚠️  警告：Clash 流量已使用 {used_mb:.0f}MB / {limit_mb:.0f}MB (90%)")
            return False
        
        if used_mb > limit_mb:
            print(f"❌ 错误：Clash 流量已用尽 ({used_mb:.0f}MB / {limit_mb:.0f}MB)")
            return False
        
        return True
    
    def get_proxies(self, model_type):
        """获取代理配置"""
        if model_type == "domestic":
            # 国内模型：直连，不走代理
            return {}
        else:
            # 海外模型：走 Clash 代理
            if not self.check_traffic_limit():
                raise Exception("Clash 流量已用尽")
            
            return {
                "http": self.proxy,
                "https": self.proxy
            } if self.proxy else {}
    
    def send_request(self, model, prompt, **kwargs):
        """发送请求"""
        model_type, base_url = self.identify_model(model)
        
        print(f"🎯 模型识别：{model}")
        print(f"📍 类型：{model_type.upper()}")
        print(f"🌐 路由：{'直连' if model_type == 'domestic' else 'Clash 代理'}")
        print()
        
        proxies = self.get_proxies(model_type)
        
        # 构建请求（简化版，实际需根据模型 API 调整）
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {kwargs.get('api_key', '')}"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            **kwargs
        }
        
        try:
            response = requests.post(
                base_url + "/chat/completions",
                headers=headers,
                json=data,
                proxies=proxies,
                timeout=60
            )
            
            # 记录流量
            self.log_traffic(len(response.content))
            
            return response.json()
            
        except Exception as e:
            print(f"❌ 请求失败：{e}")
            raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="大模型智能路由器")
    parser.add_argument("--model", required=True, help="模型名称")
    parser.add_argument("--prompt", required=True, help="提示词")
    parser.add_argument("--api-key", help="API Key")
    
    args = parser.parse_args()
    
    router = ModelRouter()
    result = router.send_request(args.model, args.prompt, api_key=args.api_key)
    
    print("\n✅ 响应:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
