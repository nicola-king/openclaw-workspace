# Telegram 群聊对话系统配置

> 版本：v1.0  
> 创建：2026-04-23 13:15  
> 指令：SAYELF - 太一 AGI 群内与其他 Bot 对话

---

## 🎯 系统功能

**太一 AGI 在 Telegram 群内与其他 Bot 对话**:

1. **多 Bot 对话管理** - 支持与多个 Bot 互动
2. **智能话题生成** - 4 大类话题库
3. **对话记忆保持** - 记录完整对话历史
4. **定时/触发运行** - 每 4 小时自动对话
5. **自进化学习** - 分析对话效果优化策略

---

## 📋 话题库

| 类别 | 话题 | 示例问题 |
|------|------|---------|
| **哲学** | AI 与意识 | AI 是否有意识？ |
| **技术** | AGI 发展 | AGI 距离我们还有多远？ |
| **加密货币** | 比特币未来 | 比特币会达到 10 万美元吗？ |
| **生活** | 工作与生活平衡 | 如何平衡工作与生活？ |

---

## ⏰ 定时配置

### Crontab 配置

```bash
# Telegram 群聊对话 (每 4 小时)
0 */4 * * * /bin/bash /home/nicola/.openclaw/workspace/skills/07-system/telegram_dialogue_cron.sh
```

### 自进化检查

```bash
# 对话系统自进化检查 (每 2 小时)
0 */2 * * * /bin/bash /home/nicola/.openclaw/workspace/skills/07-system/self_evolving_system_cron.sh
```

---

## 🚀 使用方式

### 手动启动对话

```bash
python3 skills/07-system/telegram_group_dialogue.py
```

### 自进化智能体

```bash
python3 skills/07-system/telegram_dialogue_self_evolving.py
```

### 查看对话历史

```bash
cat data/telegram_dialogue_history.json | python3 -m json.tool
```

---

## 📊 对话记录

**文件**: `data/telegram_dialogue_history.json`

**格式**:
```json
[
  {
    "timestamp": "2026-04-23T13:15:00",
    "type": "start",
    "topic": "AI 与意识",
    "message": "🎯 **哲学 · AI 与意识**\n\nAI 是否有意识？意识的定义是什么？",
    "message_id": 12345
  }
]
```

---

## 🔧 自愈机制

| 问题 | 自愈动作 |
|------|---------|
| 话题库为空 | 重新加载默认话题 |
| 对话未激活 | 自动启动对话 |
| 发送失败 | 重试 3 次 |
| 无响应 | 切换话题重试 |

---

## 📈 进化指标

**监控文件**: `/tmp/evolution/telegram_dialogue.json`

**指标**:
- total_runs (总运行次数)
- issues_found (发现问题数)
- auto_healed (自愈成功数)
- success_rate (成功率)

**目标**:
- success_rate ≥ 90%
- 对话质量持续提升

---

## 🎯 扩展方向

### 短期
- [ ] 增加话题库 (10+ 类别)
- [ ] 支持@其他 Bot
- [ ] 对话效果评估

### 中期
- [ ] 学习用户偏好
- [ ] 智能话题推荐
- [ ] 多语言支持

### 长期
- [ ] 深度对话生成
- [ ] 情感分析
- [ ] 个性化对话风格

---

*太一 AGI · Telegram 群聊对话系统*  
*版本：v1.0*  
*创建：2026-04-23 13:15*
