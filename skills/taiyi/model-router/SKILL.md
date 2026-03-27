# model-router - 大模型智能路由

> 自动识别国内/海外模型，智能分流请求

---

## 规则

1. **国内模型**（百炼/DeepSeek/Kimi）→ 直连，不走代理
2. **海外模型**（Google/Gemini/Claude/OpenAI）→ 走 Clash 代理
3. **智能分流** → Clash 每月 300GB 流量限制
4. **自动识别** → 无需手动切换

---

## 支持的模型

### 国内模型（直连）

| 服务商 | 模型 | 状态 |
|--------|------|------|
| **阿里云百炼** | qwen / qwen-turbo / qwen-plus / qwen-max | ✅ |
| **阿里云百炼** | qwen-coder / qwen3.5-plus | ✅ |
| **DeepSeek** | deepseek / deepseek-chat / deepseek-coder | ✅ |
| **Kimi** (月之暗面) | kimi / kimi-chat | ✅ |
| **智谱 AI** | glm / glm-4 | ✅ |
| **百度文心** | ernie / ernie-bot | ✅ |

### 海外模型（代理）

| 服务商 | 模型 | 状态 |
|--------|------|------|
| **Google** | gemini / gemini-pro / gemini-2.5-pro | ✅ |
| **OpenAI** | gpt / gpt-4 / gpt-4o / gpt-3.5-turbo | ✅ |
| **Claude** (Anthropic) | claude / claude-3 / claude-sonnet | ✅ |
| **Meta** | llama / llama-3 | ✅ |

---

## 安装

```bash
npx clawhub install taiyi-model-router
```

---

## 配置

编辑 `~/.taiyi/model-router/config.json`：

```json
{
  "clash_proxy": "http://127.0.0.1:7890",
  "clash_monthly_limit_gb": 300,
  "api_keys": {
    "qwen": "YOUR_DASHSCOPE_API_KEY",
    "deepseek": "YOUR_DEEPSEEK_API_KEY",
    "gemini": "YOUR_GEMINI_API_KEY",
    "openai": "YOUR_OPENAI_API_KEY"
  }
}
```

---

## 使用

### 方式 1：命令行

```bash
# 国内模型（自动直连）
python3 model-router.py --model qwen-plus --prompt "你好" --api-key "sk-xxx"

# 海外模型（自动走代理）
python3 model-router.py --model gemini-pro --prompt "Hello" --api-key "xxx"
```

### 方式 2：Python 调用

```python
from model_router import ModelRouter

router = ModelRouter()

# 自动识别，智能路由
result = router.send_request(
    model="qwen-plus",
    prompt="你好",
    api_key="sk-xxx"
)
```

### 方式 3：环境变量

```bash
export MODEL_ROUTER_PROXY="http://127.0.0.1:7890"
export MODEL_ROUTER_LIMIT_GB=300

python3 model-router.py --model claude-3 --prompt "Hello"
```

---

## 流量监控

### 查看本月流量

```bash
cat ~/.taiyi/model-router/traffic.log | grep $(date +%Y-%m)
```

### 流量预警

- 80% 用量 → 警告提示
- 90% 用量 → 严重警告
- 100% 用量 → 停止海外模型请求

---

## 智能路由逻辑

```
用户请求
   ↓
识别模型名称
   ↓
国内模型？───是───→ 直连（不走代理）
   ↓
  否
   ↓
海外模型？───是───→ Clash 代理
   ↓
  否
   ↓
默认海外 → Clash 代理
```

---

## 优势

| 特性 | 传统方式 | model-router |
|------|---------|-------------|
| **代理切换** | 手动配置 | ✅ 自动识别 |
| **流量控制** | 无 | ✅ 300GB/月限制 |
| **模型支持** | 单一 | ✅ 多服务商 |
| **配置复杂度** | 高 | ✅ 一次配置 |

---

## 价格

**免费**（内部使用）

---

## 技术支持

- 公众号：SAYELF 山野精灵
- GitHub: github.com/nicola-king/zhiji-e

---

*太一 · 2026 年 3 月*

*「智能分流，自动识别」*
