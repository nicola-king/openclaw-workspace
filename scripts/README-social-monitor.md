# 5 账号数据监控日报

## 功能

每日 09:00 自动推送 5 账号数据到 Telegram：
- 小红书 × 2（SAYELF 山野精灵、AI 缪斯｜龙虾研究所）
- 视频号 × 2（SAYELF 山野精灵、微景漫语）
- 公众号 × 1（SAYELF 山野精灵）

## 数据更新

### 自动模式（每日 09:00）
```bash
# 定时任务自动执行
python3 scripts/social-media-monitor.py --send
```

### 手动更新数据
```bash
# 交互模式，输入今日数据
python3 scripts/social-media-monitor.py --update --send
```

### 仅查看报告（不发送）
```bash
python3 scripts/social-media-monitor.py
```

## 数据存储

数据保存在：`data/social-media-stats.json`

保留最近 90 天记录，自动清理旧数据。

## 修改通知接收人

编辑 `scripts/social-media-monitor.py`：

```python
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7073481596")  # 改为你的 Telegram ID
```

## 示例输出

```
【5 账号日报 · 2026-03-28】

📕 小红书
- SAYELF 山野精灵：4262 粉 (+15)
- AI 缪斯｜龙虾研究所：4661 粉 (+23)

📹 视频号
- SAYELF 山野精灵：1497 关 (+8)
- 微景漫语：11 关 (+2)

📖 公众号
- SAYELF 山野精灵：23 关 (+1)

📊 总计：~10,454 (+49)

💡 爆款预警：无
```

## 未来扩展

- [ ] 小红书 API 自动抓取（需 Cookie）
- [ ] 视频号 API 自动抓取（需开放平台）
- [ ] 公众号 API 自动抓取（需 IP 白名单）
- [ ] 爆款内容自动识别（单篇数据监控）
- [ ] 周报/月报自动生成
