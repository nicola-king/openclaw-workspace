# 智能分流配置指南

> **版本**: v1.0  
> **创建**: 2026-04-20 22:43  
> **状态**: ✅ 待部署  
> **功能**: 飞书/微信访问海外服务时自动切换代理流量

---

## 🎯 目标

当飞书/微信需要访问海外互联网资源时，系统自动智能分流：
- **国内流量** → 直连 (低延迟)
- **海外流量** → 代理 (127.0.0.1:7890)

---

## 📊 分流规则

### 国内流量 (直连)
| 服务 | 域名 | 端口 |
|------|------|------|
| 微信 API | `api.weixin.qq.com` | 443 |
| 飞书 API | `open.feishu.cn` | 443 |
| 微信公众号 | `mp.weixin.qq.com` | 443 |
| 企业微信 | `qyapi.weixin.qq.com` | 443 |

### 海外流量 (代理)
| 服务 | 域名 | 端口 |
|------|------|------|
| Telegram | `api.telegram.org` | 443 |
| Google API | `*.googleapis.com` | 443 |
| GitHub | `api.github.com` | 443 |
| OpenAI | `api.openai.com` | 443 |
| Anthropic | `api.anthropic.com` | 443 |

---

## 🛠️ 部署方案

### 方案 1: Clash 规则分流 (推荐)

**配置文件**: `~/.config/clash/config.yaml`

```yaml
rules:
  # 国内服务 - 直连
  - DOMAIN-SUFFIX,weixin.qq.com,DIRECT
  - DOMAIN-SUFFIX,wechat.com,DIRECT
  - DOMAIN,api.weixin.qq.com,DIRECT
  - DOMAIN,mp.weixin.qq.com,DIRECT
  - DOMAIN,qyapi.weixin.qq.com,DIRECT
  
  - DOMAIN-SUFFIX,feishu.cn,DIRECT
  - DOMAIN-SUFFIX,feishucdn.com,DIRECT
  - DOMAIN,open.feishu.cn,DIRECT
  - DOMAIN,api.feishu.cn,DIRECT
  
  - DOMAIN-SUFFIX,aliyuncs.com,DIRECT
  - DOMAIN-SUFFIX,aliyun.com,DIRECT
  
  # 海外服务 - 代理
  - DOMAIN-SUFFIX,telegram.org,PROXY
  - DOMAIN-SUFFIX,telegram.me,PROXY
  - DOMAIN,api.telegram.org,PROXY
  
  - DOMAIN-SUFFIX,googleapis.com,PROXY
  - DOMAIN-SUFFIX,googleapi.com,PROXY
  
  - DOMAIN-SUFFIX,github.com,PROXY
  - DOMAIN,api.github.com,PROXY
  
  - DOMAIN-SUFFIX,openai.com,PROXY
  - DOMAIN,api.openai.com,PROXY
  
  - DOMAIN-SUFFIX,anthropic.com,PROXY
  - DOMAIN,api.anthropic.com,PROXY
  
  # 默认规则
  - GEOIP,CN,DIRECT
  - MATCH,PROXY
```

**应用配置**:
```bash
# 重载 Clash 配置
curl -X PUT http://127.0.0.1:9090/configs -d '{"path": "~/.config/clash/config.yaml"}' -H "Authorization: Bearer your_secret"

# 或使用 Clash Nyanpasu/Mihomo 界面重载
```

---

### 方案 2: 应用层智能路由 (Python)

**文件**: `/home/nicola/.openclaw/workspace/skills/04-integration/smart-router/smart_http_adapter.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能 HTTP 适配器 - 自动选择直连/代理

功能:
- 根据目标域名自动选择是否使用代理
- 支持飞书/微信/Telegram 等服务的智能分流
"""

import requests
from typing import Dict, Optional
from urllib.parse import urlparse

# 域名白名单 (直连)
DIRECT_DOMAINS = {
    # 微信
    "api.weixin.qq.com",
    "mp.weixin.qq.com",
    "qyapi.weixin.qq.com",
    "weixin.qq.com",
    
    # 飞书
    "open.feishu.cn",
    "api.feishu.cn",
    "feishu.cn",
    
    # 阿里云 (国内服务)
    "dashscope.aliyuncs.com",
    "aliyun.com",
}

# 代理配置
PROXY_CONFIG = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}


def should_use_proxy(url: str) -> bool:
    """判断是否需要使用代理"""
    parsed = urlparse(url)
    domain = parsed.netloc.split(":")[0]
    
    # 检查是否在直连白名单
    if domain in DIRECT_DOMAINS:
        return False
    
    # 检查是否为国内 IP
    import socket
    try:
        ip = socket.gethostbyname(domain)
        if ip.startswith(("127.", "192.168.", "10.", "172.16.")):
            return False
    except:
        pass
    
    # 默认使用代理
    return True


def smart_get(url: str, **kwargs) -> requests.Response:
    """智能 GET 请求"""
    proxies = PROXY_CONFIG if should_use_proxy(url) else None
    return requests.get(url, proxies=proxies, **kwargs)


def smart_post(url: str, **kwargs) -> requests.Response:
    """智能 POST 请求"""
    proxies = PROXY_CONFIG if should_use_proxy(url) else None
    return requests.post(url, proxies=proxies, **kwargs)


# 测试
if __name__ == "__main__":
    test_urls = [
        "https://api.weixin.qq.com/cgi-bin/token",  # 应直连
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",  # 应直连
        "https://api.telegram.org/bot123/getMe",  # 应代理
        "https://api.openai.com/v1/models",  # 应代理
    ]
    
    for url in test_urls:
        use_proxy = should_use_proxy(url)
        print(f"{url} → {'🌐 代理' if use_proxy else '🇨🇳 直连'}")
```

---

### 方案 3: 环境变量智能切换

**文件**: `/home/nicola/.openclaw/load-env-smart.sh`

```bash
#!/bin/bash
# 智能环境变量加载脚本

# 检测目标服务
detect_service() {
    local url="$1"
    
    case "$url" in
        *weixin.qq.com*|*feishu.cn*)
            # 国内服务 - 不使用代理
            unset HTTP_PROXY
            unset HTTPS_PROXY
            unset http_proxy
            unset https_proxy
            echo "🇨🇳 直连模式：$url"
            ;;
        *)
            # 海外服务 - 使用代理
            export HTTP_PROXY="http://127.0.0.1:7890"
            export HTTPS_PROXY="http://127.0.0.1:7890"
            export http_proxy="http://127.0.0.1:7890"
            export https_proxy="http://127.0.0.1:7890"
            echo "🌐 代理模式：$url"
            ;;
    esac
}

# 使用示例
# source load-env-smart.sh
# detect_service "https://api.weixin.qq.com/..."
# curl "$url"
```

---

## 📁 项目结构

```
/home/nicola/.openclaw/workspace/skills/04-integration/smart-router/
├── smart_http_adapter.py      # Python 智能 HTTP 适配器
├── smart_curl.sh              # Shell 智能 curl 封装
├── load-env-smart.sh          # 智能环境变量脚本
├── clash_rules.yaml           # Clash 分流规则
└── README.md                  # 使用文档
```

---

## 🚀 快速部署

### 步骤 1: 创建目录
```bash
mkdir -p /home/nicola/.openclaw/workspace/skills/04-integration/smart-router
```

### 步骤 2: 部署智能适配器
```bash
# 复制上述 Python 代码
nano /home/nicola/.openclaw/workspace/skills/04-integration/smart-router/smart_http_adapter.py
```

### 步骤 3: 更新 Clash 规则
```bash
# 编辑 Clash 配置
nano ~/.config/clash/config.yaml

# 添加上述规则
```

### 步骤 4: 测试验证
```bash
cd /home/nicola/.openclaw/workspace/skills/04-integration/smart-router
python3 smart_http_adapter.py
```

**预期输出**:
```
https://api.weixin.qq.com/cgi-bin/token → 🇨🇳 直连
https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal → 🇨🇳 直连
https://api.telegram.org/bot123/getMe → 🌐 代理
https://api.openai.com/v1/models → 🌐 代理
```

---

## 📊 效果对比

| 场景 | 优化前 | 优化后 |
|------|--------|--------|
| 微信消息发送 | 可能走代理 (慢) | 直连 (快) ✅ |
| 飞书文档创建 | 可能走代理 (慢) | 直连 (快) ✅ |
| Telegram 通知 | 直连 (失败) | 代理 (成功) ✅ |
| Google API | 直连 (失败) | 代理 (成功) ✅ |

---

## 🔗 相关文档

- `skills/07-system/geo-model-router/` - 地理模型路由
- `skills/04-integration/feishu-integration/` - 飞书集成
- `skills/04-integration/wechat/` - 微信集成

---

*太一 AGI · 智能分流配置指南 · 2026-04-20 22:43*
