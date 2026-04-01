
---

## 📚 Polymarket 官网知识学习 (2026-04-01 07:40)

### 一、Polymarket 基础概念

**什么是 Polymarket？**
- 全球最大的去中心化预测市场
- 基于 Polygon 区块链 (Chain ID: 137)
- 使用 USDC 稳定币交易
- 无需 KYC (钱包登录即可)

**核心特点**:
- ✅ 事件预测 (政治/体育/金融/加密货币)
- ✅ 二元市场 (Yes/No 份额)
- ✅ 流动性高 (头部市场>$2.8M)
- ✅ 实时交易 (CLOB 订单簿)

---

### 二、账号与钱包

**登录方式**:
| 方式 | 推荐度 | 说明 |
|------|--------|------|
| 加密钱包连接 | ⭐⭐⭐⭐⭐ | MetaMask/WalletConnect/Coinbase Wallet (无需 KYC) |
| 邮箱登录 | ⭐⭐⭐ | 需要验证 |

**SAYELF 账号信息**:
| 项目 | 配置 |
|------|------|
| 用户名 | SAYELF |
| 邮箱 | chuanxituzhu@gmail.com |
| 钱包地址 | `0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5` |
| Proxy Wallet | `0x6d8c4e9aDF5748Af82Dabe2C6225207770d6B4fa` |
| 钱包类型 | Gnosis Safe 多签 |
| USDC 余额 | $39.88 |

---

### 三、API 集成 (知几-E 量化交易)

**API 认证方式**:

#### L2 认证 (推荐 - 仅交易权限)
```
需要三元组:
- api_key
- api_secret
- api_passphrase

权限：查询/下单/取消订单
限制：无法转账/提现/修改钱包
```

#### L1 认证 (不推荐 - 需要私钥)
```
需要私钥签名
权限：完整控制
风险：资产安全风险
```

**SAYELF 安全要求**: 只使用 L2 认证 (不提供私钥)

**API 端点**:
| 服务 | URL |
|------|-----|
| CLOB API | `https://clob.polymarket.com` |
| Gamma API | `https://gamma-api.polymarket.com/markets` |
| Relayer | `https://relayer-v2.polymarket.com` |

**Python SDK**:
```bash
pip install py-clob-client
```

**配置文件**: `~/.taiyi/zhiji/polymarket.json`

---

### 四、交易流程

1. **充值 USDC** → Polygon 网络转账到钱包
2. **选择市场** → 浏览预测市场 (政治/体育/金融)
3. **买入份额** → Yes 或 No (价格=概率)
4. **等待结算** → 事件结束后自动结算
5. **获取收益** → 正确预测获得 $1/份额

**知几-E 策略**:
- 置信度阈值：96%
- 优势阈值：2%
- 下注策略：Quarter-Kelly
- 目标市场：高温天气预测 (流动性>$2.8M)

---

### 五、费用结构

| 项目 | 费率 |
|------|------|
| 交易手续费 | ~2% (含在价格中) |
| Gas 费用 | Polygon 网络 (极低) |
| 提现费用 | 网络 Gas 费 |

---

### 六、风险管理

**平台风险**:
- ✅ 去中心化 (智能合约结算)
- ✅ 非托管 (资金在钱包)
- ⚠️ 智能合约风险 (已审计)
- ⚠️ 监管风险 (因地区而异)

**交易风险**:
- 市场判断错误 → 本金损失
- 流动性不足 → 滑点
- 结算争议 → UMA 仲裁

**SAYELF 策略**:
- 单笔下注 ≤ 25% 资金 (Quarter-Kelly)
- 仅高置信度机会 (≥96%)
- 分散市场 (不集中单一事件)

---

### 七、API Key 创建步骤 (待执行)

**SAYELF 需要执行**:

1. 登录 https://polymarket.com
2. 进入账户设置 (Profile → Settings)
3. 找到 "API Keys" 或 "Developer" 选项
4. 点击 "Create API Key"
5. 记录三元组:
   - `api_key` (UUID 格式)
   - `api_secret` (Base64 编码)
   - `api_passphrase` (自设密码)
6. 配置到 `~/.taiyi/zhiji/polymarket.json`
7. 运行诊断脚本验证

**重要**: 三元组仅显示一次，需立即保存!

---

### 八、学习资源

| 资源 | 链接 |
|------|------|
| 官方文档 | https://docs.polymarket.com |
| API 参考 | https://docs.polymarket.com/api-reference |
| GitHub SDK | https://github.com/Polymarket/py-clob-client |
| 社区教程 | https://polymarket-bot.co/polymarket-api-tutorial |

---

### 九、下一步行动

| 任务 | 状态 | 负责人 |
|------|------|--------|
| 创建 API Key 三元组 | 🔴 待执行 | SAYELF |
| 配置到知几-E | 🟡 等待中 | 太一 |
| 运行认证测试 | 🟡 等待中 | 太一 |
| 首笔下注 (~$10) | 🟡 等待中 | 知几-E |

---

*学习完成 | 太一 AGI | 2026-04-01 07:45*
