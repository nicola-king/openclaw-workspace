# 📋 PolyAlert 待办事项

## 🔴 紧急（明天完成）

### 1. 获取真实市场 slug

**问题**: 当前配置的市场 slug 在 API 中找不到

**解决**:
1. 访问 https://polymarket.com
2. 浏览活跃市场
3. 从 URL 复制真实 slug
4. 更新 config.py

**示例 URL**:
```
https://polymarket.com/event/will-bitcoin-reach-100k-in-2026
                                          ↑ 这是 slug
```

### 2. 测试 API 连接

**命令**:
```bash
curl -s "https://gamma-api.polymarket.com/events?active=true&limit=5" | jq '.[].slug'
```

**预期输出**:
```
"will-btc-reach-100k-2026"
"will-eth-reach-5k-2026"
...
```

### 3. 更新市场列表

**编辑**: `skills/polyalert/config.py`

```python
MARKETS_TO_MONITOR = [
    "will-btc-reach-100k-2026",  # 从官网复制
    "will-eth-reach-5k-2026",
    # ...
]
```

---

## 🟡 重要（本周完成）

### 4. 邀请测试用户

- [ ] Telegram 群发布
- [ ] 5-10 个种子用户
- [ ] 收集反馈

### 5. 第一次真实触发

- [ ] 等待市场波动
- [ ] 验证提醒发送
- [ ] 记录触发时间

---

## 🟢 一般（下周完成）

### 6. PNG 卡片功能

- [ ] 集成 ljj-card
- [ ] 设计卡片模板
- [ ] 测试发送

### 7. 聪明钱排行榜

- [ ] 数据源接入
- [ ] 排名算法
- [ ] 展示界面

---

*更新时间：2026-03-26 21:00*
