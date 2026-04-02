# 知几首笔下注 · API 凭证已更新

> TASK-050 | 更新时间：2026-04-02 10:52  
> 状态：✅ API Key 已更新，待执行首笔下注

---

## ✅ 新 API 凭证（2026-04-02 创建）

| 项目 | 值 |
|------|-----|
| **API Key** | `019d4c16-9ffe-79e9-b2be-368220456a98` |
| **API Secret** | `F9S22wrVQ63j7I7HACqKiCuNj3zsRTULCW3nuU2pPbw=` |
| **API Passphrase** | `985f6d27a0fc540a8e9a126a9e8c0a0411918d9a79571cf187be4e4f13a79265` |
| **钱包地址** | `0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5` |
| **USDC 余额** | `$39.88` |

---

## ⚠️ 重要提醒

**API 凭证 ≠ 钱包私钥**

| 项目 | API 凭证 | 钱包私钥 |
|------|---------|---------|
| 用途 | CLOB API 交易 | 钱包签名 |
| 格式 | Key + Secret + Passphrase | 64 字符 hex |
| 过期 | 可能过期/被禁用 | 永久有效 |
| 风险 | 仅交易权限 | 完全控制钱包 |

**当前状态**：
- ✅ API 凭证已配置（用于 CLOB 下单）
- ❌ 钱包私钥未配置（用于签名）

---

## 🚀 下一步：执行首笔下注

### 方案 A：脚本自动执行（需钱包私钥）

**仍需要钱包私钥**（secp256k1 hex 格式）：

1. 从 MetaMask / Trust Wallet 导出私钥
2. 更新配置文件
3. 运行脚本：
   ```bash
   python3 /home/nicola/.openclaw/workspace/scripts/zhiji-first-bet.py
   ```

---

### 方案 B：手动首笔（推荐，无需私钥）

**使用 Polymarket 网页 + 新 API 凭证**：

1. 打开 https://polymarket.com
2. 连接钱包（已有钱包，余额 $39.88）
3. 搜索市场：`NYC Temperature` 或 `Weather`
4. 下注 **$5 USDC**（BUY YES，基于 96% 置信度）
5. 记录交易哈希

**优势**：
- ✅ 无需配置钱包私钥
- ✅ API 凭证已就绪
- ✅ 10 分钟完成

---

## 📊 推荐市场

**NYC Temperature**（纽约气温）

| 项目 | 值 |
|------|-----|
| 流动性 | >$100K |
| 知几-E 置信度 | 96%+ |
| 优势 | 3.5% |
| 建议方向 | BUY YES |
| 下注金额 | $5（测试） |

---

## 📝 执行记录（待填写）

```markdown
### 首笔下注记录

- 时间：2026-04-02 HH:MM
- 市场：NYC Temperature
- 方向：BUY YES
- 金额：$5 USDC
- 价格：0.50
- 交易哈希：`0x...`
- 状态：⏳ 待结算
```

---

*创建时间：2026-04-02 10:52 | 太一 AGI | API 凭证已更新*
