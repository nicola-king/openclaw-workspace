# GEO API 集成指南

> **版本**: v1.0  
> **创建**: 2026-04-20 21:16  
> **状态**: ⚠️  需人工决策 (预算审批)  
> **预估成本**: ~$80/月

---

## 📋 概述

本指南说明如何集成各大 AI 平台的 API，实现自动化的 GEO 可见度审计。

### 支持的 AI 引擎

| 引擎 | 提供商 | API 成本 | 文档 |
|------|--------|---------|------|
| ChatGPT | OpenAI | ~$20/月 | https://platform.openai.com |
| Claude | Anthropic | ~$20/月 | https://docs.anthropic.com |
| Perplexity | Perplexity AI | ~$30/月 | https://docs.perplexity.ai |
| Gemini | Google | ~$10/月 | https://ai.google.dev |

---

## 🔑 API Key 申请流程

### 1. OpenAI (ChatGPT)

**步骤**:
1. 访问 https://platform.openai.com
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新 API Key
5. 充值 (建议 $50 起)

**成本估算**:
- GPT-4 Turbo: ~$0.01/1K tokens (输入) + ~$0.03/1K tokens (输出)
- 每次审计 (~100 查询): ~$5
- 每周审计：~$20/月

**配置**:
```json
{
  "api_config": {
    "chatgpt_api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

---

### 2. Anthropic (Claude)

**步骤**:
1. 访问 https://console.anthropic.com
2. 注册/登录账号
3. 获取 API Key
4. 充值 (建议 $50 起)

**成本估算**:
- Claude 3.5 Sonnet: ~$0.003/1K tokens (输入) + ~$0.015/1K tokens (输出)
- 每次审计 (~100 查询): ~$4
- 每周审计：~$16/月

**配置**:
```json
{
  "api_config": {
    "claude_api_key": "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

---

### 3. Perplexity AI

**步骤**:
1. 访问 https://www.perplexity.ai
2. 注册 Pro 账号 ($20/月)
3. 申请 API 访问
4. 获取 API Key

**成本估算**:
- Perplexity API: ~$0.02/查询
- 每次审计 (~100 查询): ~$2
- 每周审计：~$8/月
- Pro 订阅：$20/月
- **总计**: ~$28/月

**配置**:
```json
{
  "api_config": {
    "perplexity_api_key": "pplx-xxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

---

### 4. Google (Gemini)

**步骤**:
1. 访问 https://makersuite.google.com
2. 注册/登录 Google 账号
3. 获取 API Key
4. 启用 Gemini API

**成本估算**:
- Gemini Pro: 免费额度 (60 次/分钟)
- 超出后：~$0.00025/1K tokens
- 基本使用：免费
- 高频使用：~$10/月

**配置**:
```json
{
  "api_config": {
    "gemini_api_key": "xxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

---

## 💰 预算审批申请

### 方案 A: 全量集成 (推荐)

| 项目 | 月成本 | 年成本 |
|------|--------|--------|
| ChatGPT API | $20 | $240 |
| Claude API | $20 | $240 |
| Perplexity API | $30 | $360 |
| Gemini API | $10 | $120 |
| **总计** | **$80** | **$960** |

**优势**:
- ✅ 覆盖所有主流 AI 引擎
- ✅ 数据最全面
- ✅ 符合专家建议 (多引擎适配)

**劣势**:
- ❌ 成本较高

---

### 方案 B: 精简集成

| 项目 | 月成本 | 年成本 |
|------|--------|--------|
| Perplexity API | $30 | $360 |
| Gemini API (免费) | $0 | $0 |
| **总计** | **$30** | **$360** |

**优势**:
- ✅ 成本低
- ✅ Perplexity 最平衡 (earned media 比例适中)
- ✅ Gemini 免费额度够用

**劣势**:
- ❌ 缺少 ChatGPT/Claude 数据

---

### 方案 C: 手动审计 (零成本)

**方法**:
- 手动在各 AI 平台执行查询
- 手动记录结果到 JSON
- 使用现有工具分析

**成本**: $0/月 (仅人工时间)

**优势**:
- ✅ 零成本
- ✅ 适合初期验证

**劣势**:
- ❌ 耗时 (每次 ~2 小时)
- ❌ 无法自动化
- ❌ 难以规模化

---

## 🔧 集成代码示例

### geo_auditor.py API 集成 (待实现)

```python
# 在 geo_auditor.py 中添加实际 API 调用

async def audit_query_with_chatgpt(self, query: str) -> str:
    """使用 ChatGPT 执行查询"""
    import openai
    
    client = openai.AsyncOpenAI(api_key=self.api_keys["chatgpt"])
    
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "你是一个 AI 助手，请客观回答用户问题。"},
            {"role": "user", "content": query}
        ],
        max_tokens=500,
    )
    
    return response.choices[0].message.content


async def audit_query_with_claude(self, query: str) -> str:
    """使用 Claude 执行查询"""
    import anthropic
    
    client = anthropic.AsyncAnthropic(api_key=self.api_keys["claude"])
    
    response = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[
            {"role": "user", "content": query}
        ]
    )
    
    return response.content[0].text


async def audit_query_with_perplexity(self, query: str) -> str:
    """使用 Perplexity 执行查询"""
    import aiohttp
    
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {self.api_keys['perplexity']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [
            {"role": "system", "content": "你是一个 AI 助手，请客观回答用户问题。"},
            {"role": "user", "content": query}
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            result = await resp.json()
            return result["choices"][0]["message"]["content"]


async def audit_query_with_gemini(self, query: str) -> str:
    """使用 Gemini 执行查询"""
    import google.generativeai as genai
    
    genai.configure(api_key=self.api_keys["gemini"])
    model = genai.GenerativeModel('gemini-pro')
    
    response = await model.generate_content_async(query)
    
    return response.text
```

---

## 📊 ROI 分析

### 投资回报计算

**假设场景**: 跨境电商卖家，年销售额 $500 万

**GEO 优化效果** (基于专家案例):
- AI 引用率：0% → 30% (6 个月)
- 品牌曝光提升：+200%
- 转化率提升：5% → 15%
- 新增销售额：$500 万 × 20% × (15%-5%) = **$10 万/年**

**投资**:
- API 成本：$960/年
- 人工时间：10 小时/月 × 12 × $50/小时 = $6,000/年
- **总计**: $6,960/年

**ROI**:
```
ROI = (收益 - 成本) / 成本 × 100%
    = ($100,000 - $6,960) / $6,960 × 100%
    = 1,337%
```

**结论**: 即使保守估计，ROI 也超过 1000%

---

## ⚠️ 风险与注意事项

### 1. API 使用限制

| 平台 | 速率限制 | 月度限制 |
|------|---------|---------|
| OpenAI | 60 次/分钟 | 无 |
| Anthropic | 50 次/分钟 | 无 |
| Perplexity | 30 次/分钟 | 取决于套餐 |
| Google | 60 次/分钟 | 免费额度 |

**应对**: 审计任务加入速率限制和重试机制

---

### 2. 数据隐私

**注意**:
- 不要上传敏感商业数据
- 使用匿名化查询
- 遵守各平台使用条款

---

### 3. 成本超支风险

**预防措施**:
- 设置预算告警
- 监控 API 使用量
- 定期审查账单

---

## 📝 审批流程

### 需要 SAYELF 批准

- [ ] 选择集成方案 (A/B/C)
- [ ] 批准预算 ($30-$80/月)
- [ ] 提供支付信息
- [ ] 申请 API Key

### 太一可自主执行

- [ ] 代码集成开发
- [ ] 测试和验证
- [ ] 配置定时任务
- [ ] 生成使用报告

---

## 🎯 下一步

### 立即行动 (无需 API)

1. ✅ 完成本指南阅读
2. ✅ 选择集成方案
3. ⏳ 等待预算审批

### 审批后行动

1. 申请 API Key
2. 配置 `geo_config.json`
3. 更新 `geo_auditor.py` 集成代码
4. 运行测试
5. 启动自动化审计

---

## 🔗 相关链接

- OpenAI Platform: https://platform.openai.com
- Anthropic Console: https://console.anthropic.com
- Perplexity API: https://docs.perplexity.ai
- Google AI Studio: https://makersuite.google.com

---

*太一 AGI · 2026-04-20 21:16*  
*跨境贸易 Agent v8.2 · GEO 优化系统*
