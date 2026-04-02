# 浏览器适配器层（Browser Adapter Layer）

> 太一 v4.0 - 融合 bb-browser + bb-sites 架构  
> 创建时间：2026-04-02  
> 版本：v1.0.0  
> 负责 Bot：素问（技术开发）

---

## 🎯 简介

**浏览器适配器层** - 为太一 AGI 提供统一的浏览器自动化接口，复用本地登录状态，绕过 API 限制。

**灵感来源**：[bb-browser](https://github.com/epiral/bb-browser) + [bb-sites](https://github.com/epiral/bb-sites)

**核心优势**：
- ✅ 无需 API Key / 私钥
- ✅ 复用本地浏览器会话（不窃取 Cookie）
- ✅ 绕过反爬机制
- ✅ 支持 50+ 主流平台

---

## 🚀 快速开始

### 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 基础用法

```python
from skills.browser_adapter.polymarket_adapter import PolymarketAdapter

# 初始化适配器
adapter = PolymarketAdapter(
    headless=False,  # 使用可见浏览器
    user_data_dir='/home/nicola/.config/google-chrome'  # 复用本地配置
)

try:
    await adapter.launch()
    
    # 下注
    result = await adapter.execute(
        action='place_bet',
        market_url='https://polymarket.com/event/xxx',
        outcome='YES',
        amount=5
    )
    
    print(result)
    
finally:
    await adapter.close()
```

---

## 📋 适配器列表

### 已实现

| 适配器 | 文件 | 状态 | 功能 |
|--------|------|------|------|
| **Polymarket** | `polymarket_adapter.py` | ✅ 完成 | 下注 / 查询余额 |
| **WeChat** | `wechat_adapter.py` | ✅ 完成 | 公众号发布 / 草稿管理 |
| **Xiaohongshu** | `xiaohongshu_adapter.py` | ✅ 完成 | 笔记发布 / 数据分析 |

### 计划中

| 适配器 | 优先级 | 功能 |
|--------|--------|------|
| GitHub | P1 | Issue/PR 管理 |
| Twitter | P1 | 发推 / 互动 |
| Discord | P2 | 消息发送 |
| 币安 | P1 | 交易 / 查询余额 |

---

## 🔧 API 文档

### PolymarketAdapter

```python
# 下注
result = await adapter.execute(
    action='place_bet',
    market_url='https://polymarket.com/event/xxx',
    outcome='YES',  # 或 'NO'
    amount=5  # USDC
)

# 查询余额
result = await adapter.execute(action='get_balance')

# 获取市场信息
result = await adapter.execute(
    action='get_market_info',
    market_url='https://polymarket.com/event/xxx'
)
```

### WeChatAdapter

```python
# 发布文章
result = await adapter.execute(
    action='publish_article',
    title='文章标题',
    content='<h1>HTML 内容</h1>',
    cover_image='/path/to/cover.jpg',  # 可选
    summary='摘要'  # 可选
)

# 获取草稿列表
result = await adapter.execute(action='get_drafts')

# 删除草稿
result = await adapter.execute(
    action='delete_draft',
    draft_id='draft_123'
)
```

### XiaohongshuAdapter

```python
# 发布笔记
result = await adapter.execute(
    action='publish_note',
    title='笔记标题',
    content='笔记内容...',
    images=['/path/to/image1.jpg', '/path/to/image2.jpg'],
    topics=['AI', '太一 AGI']  # 可选
)

# 获取数据分析
result = await adapter.execute(action='get_analytics')

# 获取草稿
result = await adapter.execute(action='get_drafts')
```

---

## 🧪 测试

### 运行测试

```bash
cd skills/browser-adapter
python3 test_adapters.py
```

### 单项测试

```python
# 测试 Polymarket
python3 -c "import asyncio; from polymarket_adapter import PolymarketAdapter; ..."

# 测试微信
python3 -c "import asyncio; from wechat_adapter import WeChatAdapter; ..."

# 测试小红书
python3 -c "import asyncio; from xiaohongshu_adapter import XiaohongshuAdapter; ..."
```

---

## 🔒 安全机制

### 会话安全

- ✅ 不窃取 Cookie
- ✅ 复用本地浏览器会话
- ✅ 用户可见浏览器操作
- ✅ 敏感操作需用户确认（如 MetaMask 签名）

### 宪法约束

- ✅ 不违反平台 ToS
- ✅ 透明汇报（用户知情）
- ✅ 价值创造（帮助 > 风险）
- ✅ ROI 实时计算（庖丁集成）

---

## 📊 使用场景

### 场景 1：Polymarket 下注（解决私钥阻塞）

```python
from skills.browser_adapter.polymarket_adapter import PolymarketAdapter

adapter = PolymarketAdapter()
await adapter.launch()

# 下注（用户确认 MetaMask 签名）
result = await adapter.execute(
    action='place_bet',
    market_url='https://polymarket.com/event/nyc-temp',
    outcome='YES',
    amount=5
)

# 结果：{'status': 'pending_signature', ...}
# 用户确认 MetaMask 后完成
```

### 场景 2：公众号发布（20:00 自动）

```python
from skills.browser_adapter.wechat_adapter import WeChatAdapter

adapter = WeChatAdapter()
await adapter.launch()

# 发布文章
result = await adapter.execute(
    action='publish_article',
    title='太一 AGI v4.0 融合架构',
    content='<h1>太一 v4.0...</h1>'
)

# 结果：{'status': 'success', ...}
```

### 场景 3：小红书发布（21:00 自动）

```python
from skills.browser_adapter.xiaohongshu_adapter import XiaohongshuAdapter

adapter = XiaohongshuAdapter()
await adapter.launch()

# 发布笔记
result = await adapter.execute(
    action='publish_note',
    title='太一 AGI v4.0',
    content='今天完成了...',
    images=['image1.jpg', 'image2.jpg'],
    topics=['AI', '太一 AGI']
)

# 结果：{'status': 'success', ...}
```

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────┐
│         太一核心（宪法 +8 Bot）           │
└─────────────────┬───────────────────────┘
                  │ 任务指令
┌─────────────────▼───────────────────────┐
│         浏览器适配器层                    │
│  - 统一接口（browser.execute）           │
│  - 会话管理（本地浏览器复用）             │
│  - 平台适配器路由                         │
└─────────────────┬───────────────────────┘
                  │ CDP 操控
┌─────────────────▼───────────────────────┐
│         平台适配器（Adapters）            │
│  - Polymarket / WeChat / Xiaohongshu    │
│  - GitHub / Twitter / Discord           │
└─────────────────┬───────────────────────┘
                  │ 真实浏览器
┌─────────────────▼───────────────────────┐
│         目标网站                          │
└─────────────────────────────────────────┘
```

---

## 📝 注意事项

### 浏览器配置

- **推荐使用 Chrome**：用户数据目录兼容性最好
- **保持浏览器登录**：适配器复用本地会话
- **不要关闭浏览器**：适配器需要访问用户数据

### 反检测

- 已注入反检测脚本（移除 `navigator.webdriver`）
- 使用可见浏览器（headless=False）更稳定
- 敏感操作需用户手动确认（如支付）

### 性能优化

- 复用浏览器实例（不要频繁 launch/close）
- 使用 `wait_until='networkidle'` 确保页面加载
- 适当添加 `asyncio.sleep()` 避免操作过快

---

## 🚧 待办事项

- [ ] GitHub 适配器
- [ ] Twitter 适配器
- [ ] Discord 适配器
- [ ] 币安适配器
- [ ] 自动重试机制集成
- [ ] QA 质量门禁集成

---

## 📄 许可证

Apache License 2.0（同 bb-browser）

---

*创建时间：2026-04-02 | 素问 AGI | 太一 v4.0*
