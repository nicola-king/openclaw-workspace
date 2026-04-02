# 知几-E 链上交易增强方案

> 整合 GMGN + debot.ai 能力  
> 版本：v1.0  
> 状态：🟡 规划中

---

## 🎯 目标

增强知几-E 的链上交易能力，从单一 Polymarket 扩展到多链 DEX 交易。

---

## 📊 竞品分析

### GMGN.ai

| 维度 | 信息 |
|------|------|
| **定位** | Solana/Base/BSC 链上交易 Bot |
| **优势** | 秒级交易、KOL 追踪、鲸鱼监控 |
| **功能** | 限价单/市价单、自动跟单、安全检测 |
| **状态** | ✅ 已配置（TOOLS.md） |

### debot.ai

| 维度 | 信息 |
|------|------|
| **定位** | AI 行情分析 + 抓全网金狗 |
| **优势** | AI 分析、跨链监控、早期项目发现 |
| **功能** | 行情分析、信号推送、风险评估 |
| **状态** | 🟡 待测试 |

---

## 🛠️ 增强方案

### Phase 1：GMGN 集成（1 周）

**任务**：
1. 测试 GMGN BSC Bot 功能
2. 分析 API 接口（如有）
3. 集成到知几-E 命令系统

**命令设计**：
```bash
# 知几-E 链上交易命令
zhiji swap --chain solana --from SOL --to USDC --amount 1
zhiji limit --chain base --token 0x123... --price 1.5
zhiji whale-track --address 0x456...
zhiji safety-check --token 0x789...
```

### Phase 2：debot.ai 集成（2 周）

**任务**：
1. 注册 debot.ai 账号
2. 测试 AI 行情分析功能
3. 集成信号推送

**命令设计**：
```bash
# AI 行情分析
zhiji analyze --token SOL --timeframe 1h
zhiji signal --chain bsc --min-confidence 80%

# 金狗发现
zhiji gem-hunt --chain solana --min-liquidity 50000
```

### Phase 3：多链套利（3 周）

**任务**：
1. 跨链价格监控
2. 套利机会检测
3. 自动执行（需用户授权）

**命令设计**：
```bash
# 套利监控
zhiji arbitrage --from solana --to base --token USDC
zhiji monitor --chains sol,base,bsc --tokens SOL,ETH,BNB
```

---

## 📈 策略扩展

### 当前策略（Polymarket）
- 气象套利（置信度 96%）
- 预期收益：+5-10%/月

### 新增策略（链上交易）
- 鲸鱼跟随（15-30%/月，高风险）
- 早期项目（50-100%/月，极高风险）
- 跨链套利（5-15%/月，中风险）

### 资金分配建议

| 策略 | 比例 | 风险 |
|------|------|------|
| Polymarket 套利 | 50% | 低 |
| 鲸鱼跟随 | 20% | 中 |
| 早期项目 | 10% | 高 |
| 跨链套利 | 20% | 中 |

---

## 🔐 风险控制

### 安全基线

1. **单笔风险**：≤2% 总资金
2. **日风险**：≤10% 总资金
3. **合约检测**：必须通过安全检测
4. **流动性**：≥$50K

### 止损策略

| 场景 | 止损线 | 执行 |
|------|--------|------|
| 单笔亏损 | -20% | 自动止损 |
| 日亏损 | -10% | 暂停交易 |
| 周亏损 | -30% | 重新评估策略 |

---

## 📋 执行清单

### Phase 1（GMGN 集成）
- [ ] 测试 GMGN BSC Bot
- [ ] 分析 API 接口
- [ ] 编写集成代码
- [ ] 测试交易流程
- [ ] 文档更新

### Phase 2（debot.ai 集成）
- [ ] 注册 debot.ai 账号
- [ ] 测试 AI 分析功能
- [ ] 集成信号推送
- [ ] 回测验证
- [ ] 文档更新

### Phase 3（多链套利）
- [ ] 跨链价格监控
- [ ] 套利机会检测
- [ ] 自动执行机制
- [ ] 风险评估
- [ ] 文档更新

---

## 🎯 验收标准

### 功能验收
- [ ] GMGN 交易命令可用
- [ ] debot.ai 信号推送正常
- [ ] 跨链套利检测准确

### 性能验收
- [ ] 交易执行 <5 秒
- [ ] 信号延迟 <1 分钟
- [ ] 套利检测 <10 秒

### 安全验收
- [ ] 合约检测 100% 覆盖
- [ ] 止损机制可靠
- [ ] 私钥安全存储

---

## 🔗 参考资源

- GMGN.ai: https://gmgn.ai
- debot.ai: https://debot.ai
- 知几-E 仓库：https://github.com/nicola-king/zhiji-e

---

*版本：v1.0 | 创建时间：2026-04-02 | 状态：规划中*
