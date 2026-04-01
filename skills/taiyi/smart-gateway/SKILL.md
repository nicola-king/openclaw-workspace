# 太一智能网关自动化路由

> 版本：v1.0 | 创建：2026-03-28 22:11
> 原则：国内服务走国内流量，国外服务走代理流量

---

## 🎯 路由规则

### 流量分类

| 服务类型 | 目标 | 路由 | 说明 |
|---------|------|------|------|
| **百炼 API** | dashscope.aliyun.com | 🇨🇳 国内流量 | 阿里云国内服务 |
| **Gemini API** | generativelanguage.googleapis.com | 🌐 代理流量 | Google 服务 |
| **国内互联网** | .cn 域名/国内服务 | 🇨🇳 国内流量 | 微信/微博/知乎等 |
| **国外互联网** | .com/.org等国际域名 | 🌐 代理流量 | Twitter/GitHub 等 |
| **本地 AI** | localhost:11434 | 🏠 本地流量 | Ollama 本地服务 |

---

## 📋 国内域名白名单

```
# 云服务
aliyun.com
aliyuncs.com
dashscope.aliyun.com  # 百炼 API
oss.aliyuncs.com

# 社交媒体
wechat.com
weibo.com
zhihu.com
bilibili.com

# 开发服务
gitee.com
coding.net

# 其他国内服务
qq.com
163.com
baidu.com
```

---

## 🌐 国外域名白名单

```
# AI 服务
googleapis.com  # Gemini API
anthropic.com   # Claude API
openai.com      # GPT API

# 开发服务
github.com
gitlab.com
stackoverflow.com

# 社交媒体
twitter.com
x.com
facebook.com
instagram.com

# 其他国际服务
google.com
youtube.com
```

---

## 🔧 智能网关实现

### 方案 1: 环境变量自动切换

```python
# smart-gateway.py

import os
from urllib.parse import urlparse

class SmartGateway:
    """智能网关路由器"""
    
    def __init__(self):
        # 国内域名白名单
        self.domestic_domains = [
            'aliyun.com',
            'aliyuncs.com',
            'dashscope.aliyun.com',
            'wechat.com',
            'weibo.com',
            'zhihu.com',
            'bilibili.com',
            'gitee.com',
            'qq.com',
            '163.com',
            'baidu.com',
        ]
        
        # 代理配置
        self.proxy_config = {
            'http': 'http://127.0.0.1:7890',  # Clash 默认端口
            'https': 'http://127.0.0.1:7890',
        }
    
    def is_domestic(self, url: str) -> bool:
        """判断是否为国内域名"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # 检查是否在白名单中
        for domestic in self.domestic_domains:
            if domestic in domain:
                return True
        
        # 检查.cn 域名
        if domain.endswith('.cn'):
            return True
        
        return False
    
    def get_proxies(self, url: str) -> dict:
        """根据 URL 获取代理配置"""
        if self.is_domestic(url):
            # 国内流量，不使用代理
            return {}
        else:
            # 国外流量，使用代理
            return self.proxy_config
    
    def request(self, method, url, **kwargs):
        """智能请求 (自动选择路由)"""
        import requests
        
        proxies = self.get_proxies(url)
        
        if proxies:
            print(f"🌐 代理流量：{url}")
        else:
            print(f"🇨🇳 国内流量：{url}")
        
        return requests.request(method, url, proxies=proxies, **kwargs)
    
    def get(self, url, **kwargs):
        """GET 请求"""
        return self.request('GET', url, **kwargs)
    
    def post(self, url, **kwargs):
        """POST 请求"""
        return self.request('POST', url, **kwargs)
```

---

### 方案 2: 系统级路由 (推荐)

```bash
#!/bin/bash
# smart-gateway.sh - 智能网关脚本

# 国内域名列表
DOMESTIC_DOMAINS=(
    "aliyun.com"
    "aliyuncs.com"
    "dashscope.aliyun.com"
    "wechat.com"
    "weibo.com"
    "zhihu.com"
    "bilibili.com"
    "gitee.com"
    "qq.com"
    "163.com"
    "baidu.com"
)

# 代理配置
PROXY_SERVER="127.0.0.1:7890"

# 判断是否为国内域名
is_domestic() {
    local url=$1
    for domain in "${DOMESTIC_DOMAINS[@]}"; do
        if [[ "$url" == *"$domain"* ]]; then
            return 0  # 是国内
        fi
    done
    
    # 检查.cn 域名
    if [[ "$url" == *".cn"* ]]; then
        return 0  # 是国内
    fi
    
    return 1  # 是国外
}

# 设置代理环境变量
set_proxy() {
    if is_domestic "$1"; then
        # 国内流量，清除代理
        unset http_proxy
        unset https_proxy
        echo "🇨🇳 国内流量：$1"
    else
        # 国外流量，设置代理
        export http_proxy="http://$PROXY_SERVER"
        export https_proxy="http://$PROXY_SERVER"
        echo "🌐 代理流量：$1"
    fi
}

# 使用示例
# source smart-gateway.sh
# set_proxy "https://dashscope.aliyun.com/api"
# curl "https://dashscope.aliyun.com/api"
```

---

### 方案 3: Python requests 集成

```python
# 在太一代码中使用

from smart_gateway import SmartGateway

# 创建智能网关实例
gateway = SmartGateway()

# 百炼 API (自动走国内流量)
response = gateway.post(
    'https://dashscope.aliyun.com/api/v1/services/aigc/text-generation/generation',
    headers={'Authorization': 'Bearer YOUR_API_KEY'},
    json={'model': 'qwen-coder', 'input': '...'}
)

# Gemini API (自动走代理流量)
response = gateway.post(
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
    params={'key': 'YOUR_API_KEY'},
    json={'contents': [{'parts': [{'text': '...'}]}]}
)
```

---

## 📊 路由规则总结

| 服务 | 域名 | 路由 | 端口 |
|------|------|------|------|
| **百炼 API** | dashscope.aliyun.com | 🇨🇳 国内 | 443 |
| **Gemini API** | generativelanguage.googleapis.com | 🌐 代理 | 443 |
| **Ollama 本地** | localhost:11434 | 🏠 本地 | 11434 |
| **微信 API** | api.weixin.qq.com | 🇨🇳 国内 | 443 |
| **GitHub API** | api.github.com | 🌐 代理 | 443 |

---

## 🚀 快速启动

```bash
# 1. 创建智能网关脚本
cd ~/.openclaw/workspace/skills/taiyi
cat > smart-gateway.py << 'EOF'
# (复制上面的 Python 代码)
EOF

# 2. 测试智能路由
python3 smart-gateway.py

# 3. 集成到太一代码
from smart_gateway import SmartGateway
gateway = SmartGateway()
```

---

## 🔒 安全配置

**代理配置**:
```bash
# Clash 默认端口
HTTP_PROXY="http://127.0.0.1:7890"
HTTPS_PROXY="http://127.0.0.1:7890"

# 如使用其他代理，修改端口
# V2Ray: 10808
# Shadowsocks: 1080
```

**域名白名单更新**:
```bash
# 定期更新国内/国外域名列表
# 确保路由准确性
```

---

*版本：v1.0 | 创建时间：2026-03-28 22:11*
*原则：国内服务走国内流量，国外服务走代理流量*
*太一 AGI · 智能网关自动化*
