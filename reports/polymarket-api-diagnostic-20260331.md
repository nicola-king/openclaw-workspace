# Polymarket API Key 问题完整诊断报告

> 生成时间：2026-03-31 18:28 | 状态：🔴 配置不完整 | 负责人：太一

---

## 📋 问题总结

**SAYELF 诉求**: "只叫你交易，没有叫你转移财产"

**核心问题**: 缺少 Polymarket CLOB API 的完整认证凭证

---

## 🔍 当前配置状态

| 配置项 | 状态 | 值 |
|--------|------|-----|
| `api_key` | ✅ 已配置 | `019d2561-d2df-785c-b619-852216ccc00d` |
| `api_secret` | ❌ 缺失 | - |
| `api_passphrase` | ❌ 缺失 | - |
| `signer_private_key` | ❌ 缺失 | - |
| `wallet_address` | ✅ 已配置 | `0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5` |
| USDC 余额 | ✅ 已充值 | $39.88 |

---

## 🚫 为什么无法交易

Polymarket CLOB API 使用 **两级认证**:

### L1 认证 (私钥签名)
- 用途：创建/派生 API Key 三元组
- 只需一次：生成 L2 凭证后不再需要
- **当前状态**: ❌ 未配置

### L2 认证 (API Key 三元组)
- 用途：日常交易 (下单/取消/查询)
- 需要三个值：`api_key` + `api_secret` + `api_passphrase`
- **当前状态**: ❌ 不完整 (只有 api_key)

---

## ✅ 基础设施测试结果

| 测试项 | 结果 | 说明 |
|--------|------|------|
| py-clob-client 安装 | ✅ 通过 | v0.34.6 |
| 公开 API 查询 | ✅ 通过 | 可获取市场数据 |
| 配置文件格式 | ✅ 正确 | JSON 格式有效 |
| USDC 余额 | ✅ 充足 | $39.88 |

**结论**: 基础设施 100% 就绪，只差 API Key 三元组

---

## 🛠️ 解决方案

### 方案 A: 官网手动创建 (推荐 ⭐)

**优点**: 
- ✅ 无需私钥
- ✅ 官方推荐方式
- ✅ 5 分钟完成
- ✅ 安全可靠

**步骤**:
1. 登录 https://polymarket.com
2. 点击右上角头像 → **Profile**
3. 找到 **Builder Keys** 或 **API Keys** 部分
4. 点击 **+ Create New**
5. **立即复制三个值** (secret 和 passphrase 只显示一次):
   ```
   api_key: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   api_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   api_passphrase: xxxxxxxxxxxxx
   ```
6. 编辑 `~/.taiyi/zhiji/polymarket.json`
7. 添加三个字段到 `polymarket` 部分:
   ```json
   {
     "polymarket": {
       "api_key": "你的 api_key",
       "api_secret": "你的 api_secret",
       "api_passphrase": "你的 api_passphrase",
       "wallet_address": "0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5"
     }
   }
   ```

---

### 方案 B: 使用私钥生成 (不推荐)

**缺点**: 
- ❌ 需要私钥 (用户拒绝提供)
- ❌ 安全风险

**步骤** (仅供参考):
1. 配置私钥到 `polymarket.json`
2. 运行：`python3 scripts/poly-create-api-keys.py`

---

## 📊 配置完成后自动执行

一旦 API Key 三元组配置完成，我将自动执行:

1. ✅ **认证测试** (`poly-clob-test.py`)
   - 验证 API Key 三元组
   - 测试订单簿查询
   - 测试中间价获取

2. ✅ **市场扫描**
   - 查询高置信度市场
   - 筛选流动性 >$50K 的市场
   - 计算 Kelly 下注比例

3. ✅ **首笔下注**
   - 金额：~$10 (Quarter-Kelly)
   - 置信度：≥96%
   - 优势：≥2%
   - 市场：BTC/ETH/气象/体育/政治

4. ✅ **交易记录**
   - 写入 `bet_records.jsonl`
   - 发送 Telegram 通知
   - 生成交易报告

---

## 🔒 安全说明

**API Key 三元组 vs 私钥**:

| 凭证类型 | 权限 | 风险 | 建议 |
|---------|------|------|------|
| **私钥** | 完全控制 (转账/交易) | 🔴 高风险 | 绝不分享 |
| **API Key 三元组** | 仅交易 (无法转账) | 🟡 中风险 | 可配置用于交易 |

**重要**: API Key 三元组 **无法转账**，只能用于交易。这是 Polymarket 的安全设计。

---

## 📁 相关文件

| 文件 | 用途 |
|------|------|
| `~/.taiyi/zhiji/polymarket.json` | 主配置文件 |
| `scripts/poly-clob-test.py` | API 测试脚本 |
| `scripts/poly-api-diagnostic.py` | 诊断工具 |
| `scripts/poly-create-api-keys.py` | API Key 生成脚本 |
| `docs/POLYMARKET-CONFIG.md` | 配置文档 |

---

## ✅ 验收标准

配置完成后，运行以下命令验证:

```bash
python3 /home/nicola/.openclaw/workspace/scripts/poly-api-diagnostic.py
```

预期输出:
```
✅ 完整配置：API Key 三元组已完整配置
   可以直接进行交易!
```

---

*报告生成：太一 AGI | 2026-03-31 18:28*
