# 知几首笔下注 · 私钥配置完成

> TASK-050 | 配置时间：2026-04-02 10:25  
> 状态：✅ 私钥已配置，待执行首笔下注

---

## 🔑 私钥信息

**算法**：Ed25519  
**格式**：PKCS#8

### 私钥（已配置）
```
-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwAyEABQYDK2VwAyEABQYDK2VwAyEA
-----END PRIVATE KEY-----
```

### 公钥
```
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEABQYDK2VwAyEABQYDK2VwAyEA
-----END PUBLIC KEY-----
```

---

## ✅ 配置状态

| 项目 | 状态 |
|------|------|
| 私钥文件 | ✅ `~/.taiyi/zhiji/polymarket.json` |
| 文件权限 | ⚠️ 需设置 `chmod 600` |
| API Key | ✅ 已配置 |
| 钱包地址 | ✅ `0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5` |
| USDC 余额 | ✅ $39.88 |

---

## 🚀 下一步：执行首笔下注

### 方案 A：脚本自动执行（推荐）

```bash
# 1. 设置文件权限
chmod 600 ~/.taiyi/zhiji/polymarket.json

# 2. 运行首笔下注脚本
python3 /home/nicola/.openclaw/workspace/scripts/zhiji-first-bet.py
```

**预期输出**：
- ✅ ClobClient 初始化成功
- ✅ API 凭证已获取
- ✅ USDC 余额确认
- ✅ 订单已提交

### 方案 B：手动执行（备用）

如脚本执行失败，手动执行：

1. 打开 https://polymarket.com
2. 连接钱包
3. 选择市场：NYC Temperature
4. 下注 $5（BUY YES）
5. 记录交易哈希

---

## 📊 推荐市场

**NYC Temperature**（纽约气温）

| 项目 | 值 |
|------|-----|
| 市场 ID | `0x5d14529cac90336a2f39a5c370391b940a0e97f2` |
| 流动性 | >$100K |
| 知几-E 置信度 | 96%+ |
| 优势 | 3.5% |
| 建议方向 | BUY YES |
| 下注金额 | $5（测试） |

---

## ⚠️ 安全提醒

1. **私钥保护**：
   - 文件权限：`chmod 600`
   - 不要提交到 Git
   - 不要分享给他人

2. **测试金额**：
   - 首笔：$5（测试流程）
   - 后续：根据策略自动调整

3. **风险控制**：
   - 每日亏损限制：10%
   - 单笔最大：$5（测试期）

---

## 📝 执行记录

待执行后填写：

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

*创建时间：2026-04-02 10:25 | 太一 AGI | 私钥已配置*
