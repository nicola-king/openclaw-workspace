# daily-wisdom - 每日智慧推送

## 职责
每日早晨 8 点随机推送一句道家或佛家智慧给用户。

## 触发方式
- 定时触发：每天 08:00
- 手动触发：用户发送 `/智慧` 或 `/每日智慧`

## 执行流程
1. 读取 `wisdom/dao-buddha-quotes.md`
2. 随机选择一句智慧语录
3. 通过微信通道推送给用户
4. 记录推送日志到 `memory/YYYY-MM-DD.md`

## 推送格式
```
📿 晨间智慧 · YYYY-MM-DD

[道家/佛家] · 《出处》

「智慧语录」

—— 太一 · 晨起静心
```

## 文件位置
- 智慧库：`wisdom/dao-buddha-quotes.md`
- 推送记录：`memory/daily-wisdom-log.md`

## 定时任务
```bash
# 每天 8:00 执行
0 8 * * * openclaw send "SAYELF" "/智慧"
```

---

*创建时间：2026-04-12*
*状态：✅ 已激活*
