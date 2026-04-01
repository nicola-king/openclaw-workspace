# Polymarket API Key 三元组 - 最终解决方案

> 生成时间：2026-03-31 18:45 | 状态：🔴 需要用户操作 | 负责人：太一

---

## 🔍 问题诊断完成

### 深度搜索结果

**搜索范围**: 全系统配置文件、备份、环境变量

**发现**:
| 文件 | 凭证 | 状态 |
|------|------|------|
| `~/.taiyi/zhiji/polymarket.json` | api_key ✅, api_secret ❌, api_passphrase ❌ | 不完整 |
| `~/.taiyi/accounts/polymarket.json` | api_key ✅, secret_key ✅, passphrase ❌ | 旧配置 (钱包不匹配) |

**结论**: 
- ❌ 系统中**没有存储**完整的 API Key 三元组
- ❌ `api_passphrase` 从未被保存或已丢失
- ❌ 旧凭证的钱包地址与当前不匹配 (`0x2b45...` vs `0x6e0c...`)

---

## 🎯 唯一解决方案

### 在 Polymarket 官网创建新的 API Key 三元组

**原因**:
- `api_passphrase` 只在创建时显示一次，无法找回
- 旧凭证的钱包地址与当前 USDC 余额钱包不匹配
- 必须为当前钱包 (`0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5`) 创建新凭证

---

## 📋 操作步骤 (5 分钟)

### 第 1 步：登录 Polymarket

```
https://polymarket.com
```

使用与钱包 `0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5` 关联的账户登录

---

### 第 2 步：进入 API Key 管理

1. 点击右上角 **头像**
2. 选择 **Profile** (个人资料)
3. 找到 **Builder Keys** 或 **API Keys** 部分
4. 点击 **+ Create New** (创建新的 API Key)

---

### 第 3 步：创建 API Key

1. 系统会生成三个值：
   ```
   API Key: 019xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   Passphrase: xxxxxxxxxxxxx
   ```

2. **⚠️ 重要**: Secret 和 Passphrase **只显示一次**！
3. **立即复制**三个值到安全的地方

---

### 第 4 步：配置到系统

编辑文件：`~/.taiyi/zhiji/polymarket.json`

在 `polymarket` 部分添加/更新：

```json
{
  "polymarket": {
    "api_key": "复制的 api_key",
    "api_secret": "复制的 secret",
    "api_passphrase": "复制的 passphrase",
    "wallet_address": "0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5"
  }
}
```

**完整命令**:
```bash
nano ~/.taiyi/zhiji/polymarket.json
```

---

### 第 5 步：验证配置

运行诊断工具：
```bash
python3 /home/nicola/.openclaw/workspace/scripts/poly-api-diagnostic.py
```

**预期输出**:
```
✅ 完整配置：API Key 三元组已完整配置
   可以直接进行交易!
```

---

## ✅ 配置完成后自动执行

一旦验证通过，我将立即执行：

### 1. 认证测试
```bash
python3 /home/nicola/.openclaw/workspace/scripts/poly-clob-test.py
```
- 验证 API Key 三元组
- 测试订单簿查询
- 测试用户余额查询

### 2. 市场扫描
- 查询高置信度市场 (≥96%)
- 筛选流动性 >$50K
- 计算 Kelly 下注比例

### 3. 首笔下注
- 金额：~$10 (Quarter-Kelly)
- 市场：最高置信度的市场
- 策略：知几-E 气象套利 v3.0

### 4. 交易记录
- 写入 `~/.taiyi/zhiji/bet_records.jsonl`
- 发送 Telegram 通知
- 生成交易报告

---

## 🔒 安全说明

### API Key 三元组权限

| 操作 | 权限 |
|------|------|
| 查询市场数据 | ✅ 允许 |
| 下单交易 | ✅ 允许 |
| 取消订单 | ✅ 允许 |
| 查询余额 | ✅ 允许 |
| **转账/提现** | ❌ **禁止** |
| **修改钱包** | ❌ **禁止** |
| **访问私钥** | ❌ **禁止** |

**符合 SAYELF 要求**: "只叫你交易，没有叫你转移财产"

---

## 📁 相关文件

| 文件 | 用途 |
|------|------|
| `~/.taiyi/zhiji/polymarket.json` | 主配置文件 |
| `scripts/poly-api-diagnostic.py` | 诊断工具 |
| `scripts/poly-clob-test.py` | API 测试脚本 |
| `docs/POLYMARKET-CLOB-API.md` | API 文档 |
| `reports/polymarket-api-diagnostic-20260331.md` | 诊断报告 |

---

## 🆘 常见问题

### Q: 找不到 Builder Keys / API Keys 选项？
A: 可能在 Profile 页面的底部，或者在 Settings → Developer 中

### Q: 创建后忘记复制 passphrase？
A: 必须重新创建新的 API Key，passphrase 无法找回

### Q: 钱包地址不匹配？
A: 确保登录的账户与钱包 `0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5` 关联

### Q: USDC 余额在哪个钱包？
A: Gnosis Safe 多签钱包 `0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5` (余额 $39.88)

---

## ✅ 验收标准

配置完成后，运行：
```bash
python3 /home/nicola/.openclaw/workspace/scripts/poly-api-diagnostic.py
```

看到以下输出即为成功：
```
✅ 完整配置：API Key 三元组已完整配置
   可以直接进行交易!
```

---

*报告生成：太一 AGI | 2026-03-31 18:45*
