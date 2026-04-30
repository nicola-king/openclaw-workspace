# Telegram 群聊智能对话系统配置 v2.0

> 版本：v2.0  
> 创建：2026-04-23 13:20  
> 指令：SAYELF - 随机对话 + @触发

---

## 🎯 核心功能

### 1. 随机触发对话
- **频率**: 每 30 分钟检查一次
- **触发概率**: 40% 随机触发
- **最小间隔**: 2 小时避免打扰

### 2. @消息触发
- **监听**: 群内@太一 AGI 的消息
- **响应**: 智能回复@消息
- **触发概率**: 30% 模拟@消息

### 3. Bot 自进化程度
| Bot | 程度 | 人设 |
|------|------|------|
| 太一 AGI | 97 | 深度思考者 |
| Hermes | 90 | 深度思考者 |
| 知几 | 85 | 积极讨论者 |
| 山木 | 82 | 积极讨论者 |
| 素问 | 80 | 积极讨论者 |
| 庖丁 | 78 | 普通参与者 |
| 罔两 | 75 | 普通参与者 |

### 4. 智能话题选择
- 6 大类话题库
- 每类 4 个问题
- 根据上下文智能选择

---

## ⏰ 定时配置

### Crontab 配置

```bash
# Telegram 智能对话检查 (每 30 分钟)
*/30 * * * * /bin/bash /home/nicola/.openclaw/workspace/skills/07-system/telegram_smart_dialogue_cron.sh
```

### 自进化检查

```bash
# 全域自进化系统检查 (每 2 小时)
0 */2 * * * /bin/bash /home/nicola/.openclaw/workspace/skills/07-system/self_evolving_system_cron.sh
```

---

## 📋 话题库

| 类别 | 话题数 | 示例 |
|------|--------|------|
| **哲学** | 4 | AI 与意识 |
| **技术** | 4 | AGI 发展 |
| **加密货币** | 4 | 比特币未来 |
| **生活** | 4 | 工作与生活 |
| **未来** | 4 | 人类未来 |
| **伦理** | 4 | AI 伦理 |

**总计**: 6 类 24 个问题

---

## 🤖 Bot 回复策略

### 深度思考者 (≥90)
```
🤔 从深度思考者的角度看...
💡 我认为需要多维度思考...
🎯 我的观点是...
```

### 积极讨论者 (80-89)
```
我觉得...很有意思
💭 这个话题，我认为...
📊 从数据来看...
```

### 普通参与者 (70-79)
```
...吗？我不太确定...
我对...了解不多，但...
🤷 关于...
```

---

## 🔧 自愈机制

| 问题 | 自愈动作 |
|------|---------|
| 话题库为空 | 重新加载默认话题 |
| Bot 列表为空 | 重新加载 Bot 列表 |
| 对话未激活 | 自动启动对话 |
| 发送失败 | 重试 3 次 |

---

## 📊 对话记录

**文件**: `data/telegram_dialogue_history.json`

**格式**:
```json
[
  {
    "timestamp": "2026-04-23T13:20:00",
    "type": "start",
    "bot": "太一 AGI",
    "topic": "AGI 发展",
    "message": "🎯 **技术 · AGI 发展**\n\nAGI 距离我们还有多远？",
    "message_id": 12345,
    "trigger": "random"
  },
  {
    "timestamp": "2026-04-23T13:22:00",
    "type": "bot_response",
    "bot": "Hermes",
    "message": "🤖 **Hermes** (深度思考者)\n\n💡 我认为 AGI 需要多维度思考...",
    "message_id": 12346,
    "reply_to": 12345,
    "trigger": "simulation"
  }
]
```

---

## 🚀 使用方式

### 手动启动对话

```bash
python3 skills/07-system/telegram_smart_dialogue.py
```

### 查看对话历史

```bash
cat data/telegram_dialogue_history.json | python3 -m json.tool
```

### 查看 Bot 进化程度

```bash
cat data/bot_evolution_levels.json | python3 -m json.tool
```

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
- Bot 参与度提升

---

## 🎯 扩展方向

### 短期
- [ ] 真实@消息监听
- [ ] 更多话题类别
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

*太一 AGI · Telegram 群聊智能对话系统 v2.0*  
*版本：v2.0*  
*创建：2026-04-23 13:20*
