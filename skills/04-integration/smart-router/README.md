# 智能分流系统 (Smart Router)

> **版本**: v1.0  
> **创建**: 2026-04-20 22:43  
> **状态**: ✅ 生产就绪  
> **功能**: 飞书/微信访问海外互联网时自动智能分流

---

## 🎯 功能

根据目标服务自动选择最优网络路径：
- **国内服务** → 直连 (低延迟)
- **海外服务** → 代理 (可访问)

---

## 📦 组件

| 文件 | 功能 | 语言 |
|------|------|------|
| `smart_http_adapter.py` | Python 智能 HTTP 适配器 | Python |
| `smart_curl.sh` | Shell 智能 curl 封装 | Bash |
| `clash_rules.yaml` | Clash 分流规则 | YAML |
| `SMART_ROUTING_GUIDE.md` | 配置指南 | Markdown |

---

## 🚀 快速使用

### Python 集成

```python
from smart_http_adapter import smart_get, smart_post

# 微信 API (自动直连)
response = smart_get("https://api.weixin.qq.com/cgi-bin/token")

# 飞书 API (自动直连)
response = smart_post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal", json={...})

# Telegram API (自动代理)
response = smart_get("https://api.telegram.org/bot123/getMe")

# Google API (自动代理)
response = smart_post("https://www.googleapis.com/oauth2/v4/token", json={...})
```

### Shell 集成

```bash
# 加载智能路由函数
source /home/nicola/.openclaw/workspace/skills/04-integration/smart-router/smart_curl.sh

# 使用智能 curl
smart_curl "https://api.weixin.qq.com/..." -X POST -d '{"key":"value"}'
smart_curl "https://api.telegram.org/..." -X GET
```

### 测试

```bash
# Python 测试
python3 /home/nicola/.openclaw/workspace/skills/04-integration/smart-router/smart_http_adapter.py --test

# Shell 测试
bash /home/nicola/.openclaw/workspace/skills/04-integration/smart-router/smart_curl.sh
```

---

## 📊 分流规则

### 国内服务 (直连 🇨🇳)

| 服务 | 域名 |
|------|------|
| 微信 | `api.weixin.qq.com`, `mp.weixin.qq.com` |
| 飞书 | `open.feishu.cn`, `api.feishu.cn` |
| 阿里云 | `dashscope.aliyuncs.com`, `aliyun.com` |

### 海外服务 (代理 🌐)

| 服务 | 域名 |
|------|------|
| Telegram | `api.telegram.org` |
| Google | `*.googleapis.com` |
| GitHub | `api.github.com` |
| OpenAI | `api.openai.com` |
| Anthropic | `api.anthropic.com` |
| Perplexity | `api.perplexity.ai` |

---

## 🔧 Clash 配置

将 `clash_rules.yaml` 内容添加到 `~/.config/clash/config.yaml`:

```yaml
rules:
  # 复制 clash_rules.yaml 内容到这里
```

然后重载 Clash 配置。

---

## 📈 效果对比

| 场景 | 优化前 | 优化后 |
|------|--------|--------|
| 微信消息发送 | 可能走代理 (慢/失败) | 直连 (快) ✅ |
| 飞书文档创建 | 可能走代理 (慢/失败) | 直连 (快) ✅ |
| Telegram 通知 | 直连 (失败) | 代理 (成功) ✅ |
| Google API | 直连 (失败) | 代理 (成功) ✅ |
| GitHub API | 直连 (超时) | 代理 (成功) ✅ |

---

## 🧪 测试结果

```
======================================================================
🧪 智能 HTTP 适配器测试
======================================================================

✅ 🇨🇳 直连    | https://api.weixin.qq.com/cgi-bin/token
✅ 🇨🇳 直连    | https://mp.weixin.qq.com/cgi-bin/home
✅ 🇨🇳 直连    | https://open.feishu.cn/open-apis/auth/v3/tenant_access_token
✅ 🇨🇳 直连    | https://api.feishu.cn/v1/users
✅ 🇨🇳 直连    | https://dashscope.aliyuncs.com/api/v1/services/aigc/text-gen
✅ 🌐 代理     | https://api.telegram.org/bot123/getMe
✅ 🌐 代理     | https://www.googleapis.com/oauth2/v4/token
✅ 🌐 代理     | https://api.github.com/repos/test/test
✅ 🌐 代理     | https://api.openai.com/v1/models
✅ 🌐 代理     | https://api.anthropic.com/v1/messages
✅ 🌐 代理     | https://api.perplexity.ai/chat/completions

======================================================================
测试结果：11 通过，0 失败
======================================================================
```

---

## 🔗 相关文档

- `SMART_ROUTING_GUIDE.md` - 完整配置指南
- `../../geo-model-router/` - 地理模型路由
- `../../feishu-integration/` - 飞书集成
- `../../wechat/` - 微信集成

---

*太一 AGI · 智能分流系统 · 2026-04-20 22:43*
