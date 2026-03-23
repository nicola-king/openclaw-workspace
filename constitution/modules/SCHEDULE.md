# 定时任务模块

**层级：** Tier 3 (术层)
**生效：** 立即生效

---

## 每日定时任务

| 时间 (北京) | 任务 | 输出 | 格式 |
|-------------|------|------|------|
| **07:00** | 晨间汇报 | SAYELF 消息 | 完整 |
| **09:00** | 跨境外贸需求 | 摘要推送 | 精简 Top 5 |
| **09:00** | 晨间检查 | HEARTBEAT | 完整 |
| **12:00** | 午间进度 | 进度汇报 | 精简 |
| **17:00** | 晚间检查 | 进度汇报 | 精简 |
| **23:00** | Agent 日记 | memory/diary/ | 完整 |
| **00:00** | 自主行动 | 夜间行动 | 完整 |
| **06:00** | 行动汇总 | 晨间汇报 | 完整 |

---

## 跨境外贸优先级

### 区域优先级（重要！）

| 优先级 | 区域 | 比例 | 说明 |
|--------|------|------|------|
| **P1** | 乌克兰 | 40% | 重点搜索 |
| **P2** | 中东 | 30% | 次要搜索 |
| **P3** | 东南亚 | 20% | 常规搜索 |
| **P4** | 欧美 | 10% | 辅助搜索 |

### Top 5 推送排序

```
每日 9:00 推送 Top 5：
- 1-2 条：乌克兰（优先）
- 2-3 条：中东（次要）
- 0-1 条：东南亚
- 0-1 条：欧美
```

---

## 搜索关键词配置

### 乌克兰（P1 重点）

```
Ukraine OR Ukrainian
tender OR procurement OR bid
transformer OR 3D printer OR medical OR machinery
budget > $50,000 USD
deadline > 60 days
```

### 中东（P2 次要）

```
Saudi Arabia OR UAE OR Qatar OR Kuwait OR Oman
tender OR procurement
transformer OR 3D printer OR medical OR machinery
budget > $50,000 USD
```

### 东南亚（P3 常规）

```
Thailand OR Vietnam OR Indonesia OR Malaysia OR Philippines
tender OR procurement
transformer OR 3D printer OR medical OR machinery
```

### 欧美（P4 辅助）

```
Europe OR USA OR Poland OR Germany OR France
tender OR procurement
transformer OR 3D printer OR medical OR machinery
```

---

## 推送格式

```
【跨境采购日报 · YYYY-MM-DD】

🇺🇦 乌克兰（重点）
1. 产品 | $额度 | 截止 | 邮箱
2. 产品 | $额度 | 截止 | 邮箱

🇸🇦 中东（次要）
3. 产品 | $额度 | 截止 | 邮箱
4. 产品 | $额度 | 截止 | 邮箱

🌏 东南亚/欧美
5. 产品 | $额度 | 截止 | 邮箱

验证：✅ 平台已验证
详情：cross-border-YYYY-MM-DD.txt
```

---

*版本：1.5 | 更新：2026-03-23 09:18 | 状态：✅ 乌克兰优先已配置*
