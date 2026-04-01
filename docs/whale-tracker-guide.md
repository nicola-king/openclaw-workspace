# 🐋 鲸鱼追踪器使用指南

> 版本：v1.0 | 创建：2026-03-30 | 状态：🟡 待配置鲸鱼地址

---

## 🎯 功能概述

**目标**: 追踪 Solana 链上鲸鱼钱包 (majorexploiter) 的大额交易  
**数据源**: GMGN API  
**告警**: 微信通知  
**阈值**: ≥$10,000 交易

---

## 📋 配置步骤

### 1️⃣ 获取鲸鱼钱包地址

**方法 A: GMGN 网站查找**
1. 访问 https://gmgn.ai
2. 搜索 "majorexploiter"
3. 复制钱包地址 (格式：`xxxx...xxxx`)

**方法 B: Solscan 查找**
1. 访问 https://solscan.io
2. 搜索鲸鱼用户名
3. 复制地址

### 2️⃣ 更新配置文件

编辑 `config/whale-tracker-config.json`:

```json
{
  "target_whales": [
    {
      "name": "majorexploiter",
      "address": "这里填入钱包地址",
      "chain": "solana",
      "min_trade_usd": 10000,
      "notify": true
    }
  ]
}
```

### 3️⃣ 测试运行

```bash
cd /home/nicola/.openclaw/workspace
python3 scripts/whale-tracker.py
```

### 4️⃣ 启动持续监控

```bash
nohup python3 scripts/whale-tracker.py --continuous > logs/whale-tracker.log 2>&1 &
```

---

## 📊 API 端点

| 端点 | 用途 | 参数 |
|------|------|------|
| `/defi/swap/v1/transactions` | 获取交易记录 | chain, user_addr, limit |
| `/defi/token/v1/info` | 代币信息 | chain, address |
| `/defi/whale/v1/list` | 鲸鱼榜单 | chain, limit |

---

## 🚨 告警格式

```
🚨 鲸鱼追踪告警

📛 鲸鱼：majorexploiter
💰 交易：BUY SOL
💵 金额：$50,000.00
📊 信号：MEDIUM
🔗 Hash: `0x1234...`
⏰ 时间：2026-03-30T20:00:00

建议：WATCH
```

---

## 📁 数据保存

**位置**: `whale-data/whale_majorexploiter_YYYY-MM-DD.json`

**内容**:
- 交易哈希
- 交易类型 (BUY/SELL)
- 金额 (USD)
- 代币信息
- 信号强度

---

## ⚠️ 注意事项

1. **API 限流**: 60 次/分钟，避免频繁请求
2. **地址验证**: 确保钱包地址格式正确 (Solana: 44 位 base58)
3. **网络环境**: 可能需要代理访问 GMGN API
4. **数据延迟**: 链上数据约 5-10 秒延迟

---

## 🔗 相关链接

- GMGN 官网：https://gmgn.ai
- GMGN Bot: @GMGN_bot (Telegram)
- Solscan: https://solscan.io

---

*创建：2026-03-30 20:00 | 太一 AGI · 罔两数据分析军团*
